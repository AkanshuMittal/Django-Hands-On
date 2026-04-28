"""
========================================================
  HireHub — hirehub/urls.py
  STEP 1: Root URL Configuration
========================================================
 
WHY THIS FILE:
  This is the "entry gate" for all incoming requests.
  Django reads this file first and routes the request
  to the correct app's urls.py.
 
URL DESIGN IN REAL PROJECTS:
  /accounts/...   → Auth (register, login, logout)
  /jobs/...       → Job board (HTML pages)
  /api/accounts/  → Auth APIs (register, JWT login)
  /api/jobs/      → Job & Application APIs
  /api/token/     → JWT token endpoints (get + refresh)
  /admin/         → Django admin panel
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # ── HTML Template URLs (for browser users) ────────────────────────────
    path('accounts/', include('accounts.urls')),   # register, login, logout
    path('jobs/', include('jobs.urls')),            # dashboard, job list, detail

    # ── API URLs (for Postman / mobile / React frontend) ──────────────────
    path('api/accounts/', include('accounts.api_urls')),  # /api/accounts/register/
    path('api/jobs/', include('jobs.api_urls')),  

    # ── JWT Token Endpoints ───────────────────────────────────────────────
    # WHY: These are the standard JWT endpoints from simplejwt.
    # POST /api/token/        → Send username+password, get access+refresh tokens
    # POST /api/token/refresh/→ Send refresh token, get new access token
    # POST /api/token/verify/ → Send any token, check if it's still valid
    path('api/token/', include('accounts.token_urls')),         # /api/jobs/
]

# Serve media files during development

# WHY: In dev mode, Django itself serves uploaded files (resumes, images).
#      In production, your web server (Nginx) handles this instead.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

