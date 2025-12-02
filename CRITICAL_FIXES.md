# CRITICAL BACKEND FIXES TO APPLY

## Fix 1: Remove duplicate Firebase initialization from authentication.py

**File:** `pacer_api/authentication.py`

**Change lines 7-22 FROM:**
```python
import os
import firebase_admin
from firebase_admin import auth as firebase_auth, credentials

# Initialize Firebase once ()
if not firebase_admin._apps:
    path = os.getenv("FIREBASE_CERT_PATH")
    try:
        if path and os.path.exists(path):
            cred = credentials.Certificate(path)
            firebase_admin.initialize_app(cred)
        else:
            firebase_admin.initialize_app()
    except Exception:
        # don't crash on dev
        pass
```

**TO:**
```python
import firebase_admin
from firebase_admin import auth as firebase_auth
import logging

# Firebase is initialized in settings.py - don't initialize again here
logger = logging.getLogger(__name__)
```

**AND change line 40-42 FROM:**
```python
        try:
            decoded = firebase_auth.verify_id_token(token)
        except Exception as e:
```

**TO:**
```python
        try:
            decoded = firebase_auth.verify_id_token(token)
        except Exception as e:
            logger.error(f"Firebase token verification failed: {str(e)}", exc_info=True)
```

---

## Fix 2: Add UserProgress tracking to sync_sessions view

**File:** `pacer_api/views.py`

**Add after line 90 (after `session = serializer.save(user=user)`):**
```python
            # Update user progress
            progress, _ = UserProgress.objects.get_or_create(user=user)
            progress.total_sessions += 1
            progress.total_minutes += session.duration_seconds // 60
            progress.last_session = session.created_at
            progress.save()
```

---

## Fix 3: Frontend settings.tsx - Add /api/ prefix

**File:** `frontend/app/(tabs)/settings.tsx`

**Change line 147 FROM:**
```typescript
      const res = await API.get("/sessions/", {
```

**TO:**
```typescript
      const res = await API.get("/api/sessions/", {
```

**Change line 177 FROM:**
```typescript
      await API.post(
        "/sessions/",
```

**TO:**
```typescript
      await API.post(
        "/api/sessions/",
```

---

## APPLY THESE FIXES TO THE BACKEND REPOSITORY ON RAILWAY

