"""URL configuration for the core app (viewer site + admin panel)."""
from django.urls import path

from . import admin_views, views

urlpatterns = [
    # ---------------- Public viewer ----------------
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("projects/", views.projects, name="projects"),
    path("certificates/", views.certificates, name="certificates"),
    path("achievements/", views.achievements, name="achievements"),
    path("skills/", views.skills, name="skills"),
    path("resume/", views.resume, name="resume"),
    path("contact/", views.contact, name="contact"),
    path("gallery/", views.gallery, name="gallery"),
    path("experience/", views.experience, name="experience"),
    path("timeline/", views.timeline, name="timeline"),
    path("api/faq/", views.faq_api, name="faq_api"),
    # ---------------- Admin panel ----------------
    path("admin-panel/login/", admin_views.admin_login, name="admin_login"),
    path("admin-panel/logout/", admin_views.admin_logout, name="admin_logout"),
    path("admin-panel/", admin_views.dashboard, name="dashboard"),
    path("admin-panel/profile/", admin_views.profile_edit, name="profile_edit"),
    path("admin-panel/settings/", admin_views.settings_edit, name="settings_edit"),
    path("admin-panel/messages/", admin_views.messages_list, name="messages_list"),
    path("admin-panel/messages/<int:pk>/", admin_views.message_detail, name="message_detail"),
    path("admin-panel/messages/<int:pk>/delete/", admin_views.message_delete, name="message_delete"),
    path("admin-panel/messages/<int:pk>/toggle/", admin_views.message_toggle, name="message_toggle"),
]

# Auto-generated CRUD routes for every editable resource.
for resource in admin_views.RESOURCES:
    urlpatterns += [
        path(
            f"admin-panel/{resource}/",
            admin_views.crud,
            {"resource": resource, "action": "list"},
            name=f"{resource}_list",
        ),
        path(
            f"admin-panel/{resource}/add/",
            admin_views.crud,
            {"resource": resource, "action": "add"},
            name=f"{resource}_add",
        ),
        path(
            f"admin-panel/{resource}/<int:pk>/edit/",
            admin_views.crud,
            {"resource": resource, "action": "edit"},
            name=f"{resource}_edit",
        ),
        path(
            f"admin-panel/{resource}/<int:pk>/delete/",
            admin_views.crud,
            {"resource": resource, "action": "delete"},
            name=f"{resource}_delete",
        ),
    ]
