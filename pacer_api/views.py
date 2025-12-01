from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes  # ✅ added
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now
from django.db.models import Sum
from .models import BreathingSession
from .serializers import BreathingSessionSerializer

from .models import BreathingSession, UserProgress, BreathPlan
from .serializers import (
    BreathingSessionSerializer, UserProgressSerializer, BreathPlanSerializer
)
from .permissions import IsOwnerOrReadOnly
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

@csrf_exempt
@require_http_methods(["GET", "POST", "OPTIONS"])
def ping(request):
    if request.method == "OPTIONS":
        response = HttpResponse()
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "*"
        return response
    return JsonResponse({"message": "Backend connected successfully!"})


class BreathPlanViewSet(viewsets.ModelViewSet):
    queryset = BreathPlan.objects.all()
    serializer_class = BreathPlanSerializer
    permission_classes = [IsAuthenticated]


class BreathingSessionViewSet(viewsets.ModelViewSet):
    serializer_class = BreathingSessionSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return BreathingSession.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        session = serializer.save(user=self.request.user)
        # update progress
        progress, _ = UserProgress.objects.get_or_create(user=self.request.user)
        progress.total_sessions += 1
        progress.total_minutes += session.duration_seconds // 60
        progress.last_session = session.created_at
        progress.save()


class UserProgressViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserProgressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProgress.objects.filter(user=self.request.user)

    @action(detail=False, methods=["get"])
    def summary(self, request):
        qs = BreathingSession.objects.filter(user=request.user)
        total_time = qs.aggregate(total=Sum("duration_seconds"))["total"] or 0
        return Response({
            "total_sessions": qs.count(),
            "total_minutes": total_time // 60,
        })


# OFFLINE SYNC ENDPOINT (added below)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def sync_sessions(request):
    """
    Accepts one or multiple breathing sessions (for offline uploads).
    The frontend can send an array of sessions or a single object.
    """
    user = request.user
    data = request.data
    if isinstance(data, dict):
        data = [data]  # handle single upload gracefully

    saved = []
    errors = []

    for entry in data:
        serializer = BreathingSessionSerializer(data=entry)
        if serializer.is_valid():
            session = serializer.save(user=user)
            saved.append(session.id)
        else:
            errors.append(serializer.errors)

    return Response(
        {
            "synced": len(saved),
            "errors": errors,
        },
        status=status.HTTP_201_CREATED if saved else status.HTTP_400_BAD_REQUEST,
    )