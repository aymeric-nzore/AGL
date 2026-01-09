from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path("django-admin/", admin.site.urls),
    
    # Authentication
    path("", views.login_view, name="login"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),
    
    # Dashboards
    path("dashboard/admin/", views.admin_dashboard, name="admin_dashboard"),
    path("dashboard/teacher/", views.teacher_dashboard, name="teacher_dashboard"),
    path("dashboard/student/", views.student_dashboard, name="student_dashboard"),
    
    # Admin - College Management
    path("manage/college/", views.college_list, name="college_list"),
    path("manage/college/create/", views.college_create, name="college_create"),
    
    # Admin - Departement Management
    path("manage/departement/", views.departement_list, name="departement_list"),
    path("manage/departement/create/", views.departement_create, name="departement_create"),
    
    # Admin - Matiere Management
    path("manage/matiere/", views.matiere_list, name="matiere_list"),
    path("manage/matiere/create/", views.matiere_create, name="matiere_create"),
    
    # Admin - Salle Management
    path("manage/salle/", views.salle_list, name="salle_list"),
    path("manage/salle/create/", views.salle_create, name="salle_create"),
    
    # Teacher - Cours Management
    path("teacher/cours/", views.cours_list, name="cours_list"),
    path("teacher/cours/create/", views.cours_create, name="cours_create"),
    
    # Teacher - Notes Management
    path("teacher/notes/", views.notes_list, name="notes_list"),
    path("teacher/notes/create/", views.notes_create, name="notes_create"),
    
    # Teacher - Presence Management
    path("teacher/presence/", views.presence_list, name="presence_list"),
    path("teacher/presence/create/", views.presence_create, name="presence_create"),
    
    # Teacher - Department Stats
    path("teacher/departement/<int:dept_id>/stats/", views.departement_stats, name="departement_stats"),
    
    # Student Views
    path("student/notes/", views.student_notes, name="student_notes"),
    path("student/presences/", views.student_presences, name="student_presences"),
    path("student/cours/", views.student_cours, name="student_cours"),
    path("student/schedule/", views.student_schedule, name="student_schedule"),
]