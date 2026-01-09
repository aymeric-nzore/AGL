from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import (
    Utilisateur, Administrateur, College, Departement, 
    Enseignant, Eleve, Matiere, Salle, Notes, Cours, Presence
)

# Authentication Views
def login_view(request):
    if request.method == 'POST':
        identifiant = request.POST.get('identifiant')
        user_type = request.POST.get('user_type')
        
        try:
            utilisateur = Utilisateur.objects.get(identifiant=identifiant)
            request.session['user_id'] = utilisateur.id
            request.session['user_type'] = user_type
            
            # Verify user type matches
            if user_type == 'admin' and hasattr(utilisateur, 'administrateur'):
                messages.success(request, 'Connexion réussie!')
                return redirect('admin_dashboard')
            elif user_type == 'enseignant' and hasattr(utilisateur, 'enseignant'):
                messages.success(request, 'Connexion réussie!')
                return redirect('teacher_dashboard')
            elif user_type == 'eleve' and hasattr(utilisateur, 'eleve'):
                messages.success(request, 'Connexion réussie!')
                return redirect('student_dashboard')
            else:
                messages.error(request, 'Type d\'utilisateur incorrect.')
                del request.session['user_id']
                del request.session['user_type']
        except Utilisateur.DoesNotExist:
            messages.error(request, 'Identifiant invalide.')
    
    return render(request, 'login.html')

def logout_view(request):
    request.session.flush()
    messages.info(request, 'Vous avez été déconnecté.')
    return redirect('login')

def profile_view(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    utilisateur = get_object_or_404(Utilisateur, id=request.session['user_id'])
    user_type = request.session.get('user_type')
    
    context = {
        'utilisateur': utilisateur,
        'user_type': user_type,
        'now': timezone.now()
    }
    
    if user_type == 'enseignant':
        context['enseignant'] = utilisateur.enseignant
    elif user_type == 'eleve':
        context['eleve'] = utilisateur.eleve
    
    return render(request, 'profile.html', context)

# Admin Dashboard
def admin_dashboard(request):
    if 'user_id' not in request.session or request.session.get('user_type') != 'admin':
        return redirect('login')
    
    utilisateur = get_object_or_404(Utilisateur, id=request.session['user_id'])
    
    stats = {
        'colleges': College.objects.count(),
        'departements': Departement.objects.count(),
        'enseignants': Enseignant.objects.count(),
        'eleves': Eleve.objects.count(),
    }
    
    return render(request, 'admin_dashboard.html', {
        'utilisateur': utilisateur,
        'user_type': 'admin',
        'stats': stats
    })

# Teacher Dashboard
def teacher_dashboard(request):
    if 'user_id' not in request.session or request.session.get('user_type') != 'enseignant':
        return redirect('login')
    
    utilisateur = get_object_or_404(Utilisateur, id=request.session['user_id'])
    enseignant = utilisateur.enseignant
    
    is_responsable = hasattr(enseignant, 'departement_dirige') and enseignant.departement_dirige is not None
    
    stats = {
        'matieres': enseignant.matieres.count(),
        'cours': enseignant.cours_crees.count(),
        'notes': Notes.objects.filter(matiere__enseignant=enseignant).count(),
    }
    
    context = {
        'utilisateur': utilisateur,
        'user_type': 'enseignant',
        'enseignant': enseignant,
        'is_responsable': is_responsable,
        'stats': stats
    }
    
    if is_responsable:
        context['departement_dirige'] = enseignant.departement_dirige
    
    return render(request, 'teacher_dashboard.html', context)

# Student Dashboard
def student_dashboard(request):
    if 'user_id' not in request.session or request.session.get('user_type') != 'eleve':
        return redirect('login')
    
    utilisateur = get_object_or_404(Utilisateur, id=request.session['user_id'])
    eleve = utilisateur.eleve
    
    notes = eleve.notes_set.all()
    matieres = set(note.matiere for note in notes)
    
    stats = {
        'matieres': len(matieres),
        'notes': notes.count(),
    }
    
    context = {
        'utilisateur': utilisateur,
        'user_type': 'eleve',
        'eleve': eleve,
        'moyenne_generale': eleve.calculerMoyenneGenerale(),
        'heures_absence': eleve.calculerHeuresAbsence(),
        'stats': stats,
        'recent_notes': notes.order_by('-id')[:5],
        'recent_absences': eleve.presences.filter(present=False)[:5],
    }
    
    return render(request, 'student_dashboard.html', context)

# Helper function for login requirement
def require_login(user_type=None):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if 'user_id' not in request.session:
                return redirect('login')
            if user_type and request.session.get('user_type') != user_type:
                messages.error(request, 'Accès non autorisé.')
                return redirect('login')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

# ============= ADMIN VIEWS =============

# College Management
def college_list(request):
    if 'user_id' not in request.session or request.session.get('user_type') != 'admin':
        return redirect('login')
    
    colleges = College.objects.all()
    items = []
    for college in colleges:
        items.append({
            'values': [college.nom, college.adresse, college.telephone, college.academie.nom],
            'edit_url': f'/admin/college/{college.id}/edit/',
            'delete_url': f'/admin/college/{college.id}/delete/'
        })
    
    return render(request, 'list_generic.html', {
        'title': 'Liste des Collèges',
        'headers': ['Nom', 'Adresse', 'Téléphone', 'Académie'],
        'items': items,
        'create_url': '/admin/college/create/',
        'user_type': 'admin'
    })

def college_create(request):
    if 'user_id' not in request.session or request.session.get('user_type') != 'admin':
        return redirect('login')
    
    if request.method == 'POST':
        nom = request.POST.get('nom')
        adresse = request.POST.get('adresse')
        telephone = request.POST.get('telephone')
        academie_id = request.POST.get('academie')
        
        College.objects.create(
            nom=nom,
            adresse=adresse,
            telephone=telephone,
            academie_id=academie_id
        )
        messages.success(request, 'Collège créé avec succès!')
        return redirect('college_list')
    
    academies = Academie.objects.all()
    form_fields = [
        {'name': 'nom', 'label': 'Nom du Collège', 'type': 'text', 'required': True},
        {'name': 'adresse', 'label': 'Adresse', 'type': 'textarea', 'required': False},
        {'name': 'telephone', 'label': 'Téléphone', 'type': 'text', 'required': False},
        {'name': 'academie', 'label': 'Académie', 'type': 'select', 'required': True,
         'options': [{'value': a.id, 'label': a.nom} for a in academies]},
    ]
    
    return render(request, 'form_generic.html', {
        'title': 'Créer un Collège',
        'form_fields': form_fields,
        'back_url': '/admin/college/',
        'user_type': 'admin'
    })

# Departement Management
def departement_list(request):
    if 'user_id' not in request.session or request.session.get('user_type') != 'admin':
        return redirect('login')
    
    departements = Departement.objects.all()
    items = []
    for dept in departements:
        responsable_nom = str(dept.responsable.utilisateur) if dept.responsable else 'Non assigné'
        items.append({
            'values': [dept.nom, dept.code_departement, dept.college.nom, responsable_nom],
            'edit_url': f'/admin/departement/{dept.id}/edit/',
            'delete_url': f'/admin/departement/{dept.id}/delete/'
        })
    
    return render(request, 'list_generic.html', {
        'title': 'Liste des Départements',
        'headers': ['Nom', 'Code', 'Collège', 'Responsable'],
        'items': items,
        'create_url': '/admin/departement/create/',
        'user_type': 'admin'
    })

def departement_create(request):
    if 'user_id' not in request.session or request.session.get('user_type') != 'admin':
        return redirect('login')
    
    if request.method == 'POST':
        nom = request.POST.get('nom')
        code_departement = request.POST.get('code_departement')
        college_id = request.POST.get('college')
        responsable_id = request.POST.get('responsable') or None
        
        Departement.objects.create(
            nom=nom,
            code_departement=code_departement,
            college_id=college_id,
            responsable_id=responsable_id
        )
        messages.success(request, 'Département créé avec succès!')
        return redirect('departement_list')
    
    colleges = College.objects.all()
    enseignants = Enseignant.objects.all()
    
    form_fields = [
        {'name': 'nom', 'label': 'Nom du Département', 'type': 'text', 'required': True},
        {'name': 'code_departement', 'label': 'Code du Département', 'type': 'text', 'required': True},
        {'name': 'college', 'label': 'Collège', 'type': 'select', 'required': True,
         'options': [{'value': c.id, 'label': c.nom} for c in colleges]},
        {'name': 'responsable', 'label': 'Responsable (optionnel)', 'type': 'select', 'required': False,
         'options': [{'value': e.id, 'label': str(e.utilisateur)} for e in enseignants]},
    ]
    
    return render(request, 'form_generic.html', {
        'title': 'Créer un Département',
        'form_fields': form_fields,
        'back_url': '/admin/departement/',
        'user_type': 'admin'
    })

# Matiere Management
def matiere_list(request):
    if 'user_id' not in request.session or request.session.get('user_type') != 'admin':
        return redirect('login')
    
    matieres = Matiere.objects.all()
    items = []
    for matiere in matieres:
        enseignant_nom = str(matiere.enseignant.utilisateur) if matiere.enseignant else 'Non assigné'
        salle_nom = str(matiere.salle) if matiere.salle else 'Non assignée'
        items.append({
            'values': [matiere.libelle, matiere.departement.nom, enseignant_nom, salle_nom],
            'edit_url': f'/admin/matiere/{matiere.id}/edit/',
            'delete_url': f'/admin/matiere/{matiere.id}/delete/'
        })
    
    return render(request, 'list_generic.html', {
        'title': 'Liste des Matières',
        'headers': ['Libellé', 'Département', 'Enseignant', 'Salle'],
        'items': items,
        'create_url': '/admin/matiere/create/',
        'user_type': 'admin'
    })

def matiere_create(request):
    if 'user_id' not in request.session or request.session.get('user_type') != 'admin':
        return redirect('login')
    
    if request.method == 'POST':
        libelle = request.POST.get('libelle')
        departement_id = request.POST.get('departement')
        enseignant_id = request.POST.get('enseignant') or None
        salle_id = request.POST.get('salle') or None
        
        Matiere.objects.create(
            libelle=libelle,
            departement_id=departement_id,
            enseignant_id=enseignant_id,
            salle_id=salle_id
        )
        messages.success(request, 'Matière créée avec succès!')
        return redirect('matiere_list')
    
    departements = Departement.objects.all()
    enseignants = Enseignant.objects.all()
    salles = Salle.objects.all()
    
    form_fields = [
        {'name': 'libelle', 'label': 'Libellé de la Matière', 'type': 'text', 'required': True},
        {'name': 'departement', 'label': 'Département', 'type': 'select', 'required': True,
         'options': [{'value': d.id, 'label': d.nom} for d in departements]},
        {'name': 'enseignant', 'label': 'Enseignant (optionnel)', 'type': 'select', 'required': False,
         'options': [{'value': e.id, 'label': str(e.utilisateur)} for e in enseignants]},
        {'name': 'salle', 'label': 'Salle (optionnelle)', 'type': 'select', 'required': False,
         'options': [{'value': s.id, 'label': str(s)} for s in salles]},
    ]
    
    return render(request, 'form_generic.html', {
        'title': 'Créer une Matière',
        'form_fields': form_fields,
        'back_url': '/admin/matiere/',
        'user_type': 'admin'
    })

# Salle Management
def salle_list(request):
    if 'user_id' not in request.session or request.session.get('user_type') != 'admin':
        return redirect('login')
    
    salles = Salle.objects.all()
    items = []
    for salle in salles:
        items.append({
            'values': [salle.numero, salle.capacite],
            'edit_url': f'/admin/salle/{salle.id}/edit/',
            'delete_url': f'/admin/salle/{salle.id}/delete/'
        })
    
    return render(request, 'list_generic.html', {
        'title': 'Liste des Salles',
        'headers': ['Numéro', 'Capacité'],
        'items': items,
        'create_url': '/admin/salle/create/',
        'user_type': 'admin'
    })

def salle_create(request):
    if 'user_id' not in request.session or request.session.get('user_type') != 'admin':
        return redirect('login')
    
    if request.method == 'POST':
        numero = request.POST.get('numero')
        capacite = request.POST.get('capacite')
        
        Salle.objects.create(numero=numero, capacite=capacite)
        messages.success(request, 'Salle créée avec succès!')
        return redirect('salle_list')
    
    form_fields = [
        {'name': 'numero', 'label': 'Numéro de Salle', 'type': 'text', 'required': True},
        {'name': 'capacite', 'label': 'Capacité', 'type': 'number', 'required': True},
    ]
    
    return render(request, 'form_generic.html', {
        'title': 'Créer une Salle',
        'form_fields': form_fields,
        'back_url': '/admin/salle/',
        'user_type': 'admin'
    })

# ============= TEACHER VIEWS =============

# Cours Management (for teachers)
def cours_list(request):
    if 'user_id' not in request.session or request.session.get('user_type') != 'enseignant':
        return redirect('login')
    
    utilisateur = get_object_or_404(Utilisateur, id=request.session['user_id'])
    enseignant = utilisateur.enseignant
    cours = enseignant.cours_crees.all()
    
    items = []
    for c in cours:
        items.append({
            'values': [c.titre, c.get_type_contenu_display(), c.matiere.libelle, c.date_creation.strftime('%d/%m/%Y')],
            'edit_url': f'/teacher/cours/{c.id}/edit/',
            'delete_url': f'/teacher/cours/{c.id}/delete/'
        })
    
    return render(request, 'list_generic.html', {
        'title': 'Mes Cours et Exercices',
        'headers': ['Titre', 'Type', 'Matière', 'Date de création'],
        'items': items,
        'create_url': '/teacher/cours/create/',
        'user_type': 'enseignant'
    })

def cours_create(request):
    if 'user_id' not in request.session or request.session.get('user_type') != 'enseignant':
        return redirect('login')
    
    utilisateur = get_object_or_404(Utilisateur, id=request.session['user_id'])
    enseignant = utilisateur.enseignant
    
    if request.method == 'POST':
        titre = request.POST.get('titre')
        type_contenu = request.POST.get('type_contenu')
        contenu = request.POST.get('contenu')
        matiere_id = request.POST.get('matiere')
        
        Cours.objects.create(
            titre=titre,
            type_contenu=type_contenu,
            contenu=contenu,
            matiere_id=matiere_id,
            enseignant=enseignant
        )
        messages.success(request, 'Cours/Exercice créé avec succès!')
        return redirect('cours_list')
    
    matieres = enseignant.matieres.all()
    
    form_fields = [
        {'name': 'titre', 'label': 'Titre', 'type': 'text', 'required': True},
        {'name': 'type_contenu', 'label': 'Type', 'type': 'select', 'required': True,
         'options': [{'value': 'cours', 'label': 'Cours'}, {'value': 'exercice', 'label': 'Exercice'}]},
        {'name': 'matiere', 'label': 'Matière', 'type': 'select', 'required': True,
         'options': [{'value': m.id, 'label': m.libelle} for m in matieres]},
        {'name': 'contenu', 'label': 'Contenu', 'type': 'textarea', 'required': True},
    ]
    
    return render(request, 'form_generic.html', {
        'title': 'Ajouter un Cours/Exercice',
        'form_fields': form_fields,
        'back_url': '/teacher/cours/',
        'user_type': 'enseignant'
    })

# Notes Management (for teachers)
def notes_list(request):
    if 'user_id' not in request.session or request.session.get('user_type') != 'enseignant':
        return redirect('login')
    
    utilisateur = get_object_or_404(Utilisateur, id=request.session['user_id'])
    enseignant = utilisateur.enseignant
    notes = Notes.objects.filter(matiere__enseignant=enseignant)
    
    items = []
    for note in notes:
        items.append({
            'values': [str(note.eleve.utilisateur), note.matiere.libelle, note.valeur],
            'edit_url': f'/teacher/notes/{note.id}/edit/',
            'delete_url': None
        })
    
    return render(request, 'list_generic.html', {
        'title': 'Gestion des Notes',
        'headers': ['Élève', 'Matière', 'Note'],
        'items': items,
        'create_url': '/teacher/notes/create/',
        'user_type': 'enseignant'
    })

def notes_create(request):
    if 'user_id' not in request.session or request.session.get('user_type') != 'enseignant':
        return redirect('login')
    
    utilisateur = get_object_or_404(Utilisateur, id=request.session['user_id'])
    enseignant = utilisateur.enseignant
    
    if request.method == 'POST':
        eleve_id = request.POST.get('eleve')
        matiere_id = request.POST.get('matiere')
        valeur = request.POST.get('valeur')
        
        Notes.objects.update_or_create(
            eleve_id=eleve_id,
            matiere_id=matiere_id,
            defaults={'valeur': valeur}
        )
        messages.success(request, 'Note attribuée avec succès!')
        return redirect('notes_list')
    
    matieres = enseignant.matieres.all()
    eleves = Eleve.objects.all()
    
    form_fields = [
        {'name': 'eleve', 'label': 'Élève', 'type': 'select', 'required': True,
         'options': [{'value': e.id, 'label': str(e.utilisateur)} for e in eleves]},
        {'name': 'matiere', 'label': 'Matière', 'type': 'select', 'required': True,
         'options': [{'value': m.id, 'label': m.libelle} for m in matieres]},
        {'name': 'valeur', 'label': 'Note (sur 20)', 'type': 'number', 'required': True},
    ]
    
    return render(request, 'form_generic.html', {
        'title': 'Attribuer une Note',
        'form_fields': form_fields,
        'back_url': '/teacher/notes/',
        'user_type': 'enseignant'
    })

# Presence Management (for teachers)
def presence_list(request):
    if 'user_id' not in request.session or request.session.get('user_type') != 'enseignant':
        return redirect('login')
    
    utilisateur = get_object_or_404(Utilisateur, id=request.session['user_id'])
    enseignant = utilisateur.enseignant
    presences = enseignant.presences_marquees.all()[:50]
    
    items = []
    for p in presences:
        status = 'Présent' if p.present else 'Absent'
        items.append({
            'values': [str(p.eleve.utilisateur), p.matiere.libelle, p.date.strftime('%d/%m/%Y'), status],
            'edit_url': None,
            'delete_url': None
        })
    
    return render(request, 'list_generic.html', {
        'title': 'Gestion des Présences',
        'headers': ['Élève', 'Matière', 'Date', 'Statut'],
        'items': items,
        'create_url': '/teacher/presence/create/',
        'user_type': 'enseignant'
    })

def presence_create(request):
    if 'user_id' not in request.session or request.session.get('user_type') != 'enseignant':
        return redirect('login')
    
    utilisateur = get_object_or_404(Utilisateur, id=request.session['user_id'])
    enseignant = utilisateur.enseignant
    
    if request.method == 'POST':
        eleve_id = request.POST.get('eleve')
        matiere_id = request.POST.get('matiere')
        date = request.POST.get('date')
        present = request.POST.get('present') == 'true'
        
        Presence.objects.update_or_create(
            eleve_id=eleve_id,
            matiere_id=matiere_id,
            date=date,
            defaults={'present': present, 'enseignant': enseignant}
        )
        messages.success(request, 'Présence enregistrée avec succès!')
        return redirect('presence_list')
    
    matieres = enseignant.matieres.all()
    eleves = Eleve.objects.all()
    
    form_fields = [
        {'name': 'eleve', 'label': 'Élève', 'type': 'select', 'required': True,
         'options': [{'value': e.id, 'label': str(e.utilisateur)} for e in eleves]},
        {'name': 'matiere', 'label': 'Matière', 'type': 'select', 'required': True,
         'options': [{'value': m.id, 'label': m.libelle} for m in matieres]},
        {'name': 'date', 'label': 'Date', 'type': 'date', 'required': True},
        {'name': 'present', 'label': 'Présence', 'type': 'select', 'required': True,
         'options': [{'value': 'true', 'label': 'Présent'}, {'value': 'false', 'label': 'Absent'}]},
    ]
    
    return render(request, 'form_generic.html', {
        'title': 'Marquer Présence/Absence',
        'form_fields': form_fields,
        'back_url': '/teacher/presence/',
        'user_type': 'enseignant'
    })

# Department Statistics (for department heads)
def departement_stats(request, dept_id):
    if 'user_id' not in request.session or request.session.get('user_type') != 'enseignant':
        return redirect('login')
    
    utilisateur = get_object_or_404(Utilisateur, id=request.session['user_id'])
    enseignant = utilisateur.enseignant
    departement = get_object_or_404(Departement, id=dept_id, responsable=enseignant)
    
    moyenne = departement.calculerMoyenneDepartement()
    
    return render(request, 'departement_stats.html', {
        'departement': departement,
        'moyenne': moyenne,
        'user_type': 'enseignant'
    })

# ============= STUDENT VIEWS =============

def student_notes(request):
    if 'user_id' not in request.session or request.session.get('user_type') != 'eleve':
        return redirect('login')
    
    utilisateur = get_object_or_404(Utilisateur, id=request.session['user_id'])
    eleve = utilisateur.eleve
    notes = eleve.notes_set.all()
    
    items = []
    for note in notes:
        items.append({
            'values': [note.matiere.libelle, note.valeur, note.matiere.enseignant.utilisateur if note.matiere.enseignant else 'N/A'],
            'edit_url': None,
            'delete_url': None
        })
    
    return render(request, 'list_generic.html', {
        'title': 'Mes Notes',
        'headers': ['Matière', 'Note', 'Enseignant'],
        'items': items,
        'create_url': None,
        'user_type': 'eleve'
    })

def student_presences(request):
    if 'user_id' not in request.session or request.session.get('user_type') != 'eleve':
        return redirect('login')
    
    utilisateur = get_object_or_404(Utilisateur, id=request.session['user_id'])
    eleve = utilisateur.eleve
    presences = eleve.presences.all()[:50]
    
    items = []
    for p in presences:
        status = 'Présent' if p.present else 'Absent'
        items.append({
            'values': [p.matiere.libelle, p.date.strftime('%d/%m/%Y'), status],
            'edit_url': None,
            'delete_url': None
        })
    
    return render(request, 'list_generic.html', {
        'title': 'Mes Présences',
        'headers': ['Matière', 'Date', 'Statut'],
        'items': items,
        'create_url': None,
        'user_type': 'eleve'
    })

def student_cours(request):
    if 'user_id' not in request.session or request.session.get('user_type') != 'eleve':
        return redirect('login')
    
    utilisateur = get_object_or_404(Utilisateur, id=request.session['user_id'])
    eleve = utilisateur.eleve
    
    # Get all subjects for this student (subjects where they have notes)
    matieres = set(note.matiere for note in eleve.notes_set.all())
    
    # Get all cours for these subjects
    cours_list = []
    for matiere in matieres:
        cours_list.extend(matiere.cours_set.all())
    
    items = []
    for c in cours_list:
        items.append({
            'values': [c.titre, c.get_type_contenu_display(), c.matiere.libelle, c.date_creation.strftime('%d/%m/%Y')],
            'edit_url': f'/student/cours/{c.id}/',
            'delete_url': None
        })
    
    return render(request, 'list_generic.html', {
        'title': 'Cours et Exercices',
        'headers': ['Titre', 'Type', 'Matière', 'Date'],
        'items': items,
        'create_url': None,
        'user_type': 'eleve'
    })

def student_schedule(request):
    if 'user_id' not in request.session or request.session.get('user_type') != 'eleve':
        return redirect('login')
    
    utilisateur = get_object_or_404(Utilisateur, id=request.session['user_id'])
    eleve = utilisateur.eleve
    
    # Get all subjects for this student
    matieres = set(note.matiere for note in eleve.notes_set.all())
    
    items = []
    for matiere in matieres:
        enseignant_nom = str(matiere.enseignant.utilisateur) if matiere.enseignant else 'N/A'
        salle_nom = str(matiere.salle) if matiere.salle else 'N/A'
        items.append({
            'values': [matiere.libelle, enseignant_nom, salle_nom],
            'edit_url': None,
            'delete_url': None
        })
    
    return render(request, 'list_generic.html', {
        'title': 'Mon Emploi du Temps',
        'headers': ['Matière', 'Enseignant', 'Salle'],
        'items': items,
        'create_url': None,
        'user_type': 'eleve'
    })


