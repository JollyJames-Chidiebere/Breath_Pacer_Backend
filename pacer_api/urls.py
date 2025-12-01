from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Your existing router setup
router = DefaultRouter()
router.register(r'breathing_sessions', views.BreathingSessionViewSet, basename='breathing_session')
router.register(r'sessions', views.BreathingSessionViewSet, basename='session')  # ✅ Alias for frontend compatibility
router.register(r'user_progress', views.UserProgressViewSet, basename='user_progress')
router.register(r'breath_plans', views.BreathPlanViewSet, basename='breath_plan')

urlpatterns = [
    path('', include(router.urls)),

    # Endpoint for offline session sync
    path('sync_sessions/', views.sync_sessions, name='sync_sessions'),
    path('ping/', views.ping, name='ping'),
]