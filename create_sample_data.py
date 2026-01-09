#!/usr/bin/env python
import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agl.settings')
django.setup()

from core.models import (
    Utilisateur, Administrateur, Academie, College, Departement,
    Enseignant, Salle, Matiere, Eleve, Notes, Cours, Presence
)

def create_sample_data():
    print("Creating sample data...")
    
    # Create Academy
    academie = Academie.objects.create(nom="Académie de Paris")
    print(f"✓ Created academy: {academie.nom}")
    
    # Create Colleges
    college1 = College.objects.create(
        nom="Collège Victor Hugo",
        adresse="123 Rue de la République, Paris",
        telephone="0123456789",
        academie=academie
    )
    college2 = College.objects.create(
        nom="Collège Jean Moulin",
        adresse="456 Avenue des Champs, Paris",
        telephone="0987654321",
        academie=academie
    )
    print(f"✓ Created colleges: {college1.nom}, {college2.nom}")
    
    # Create Admin User
    admin_user = Utilisateur.objects.create(
        nom="Admin",
        prenom="System",
        tel="0100000001",
        mail="admin@agl.fr",
        identifiant="admin001"
    )
    admin = Administrateur.objects.create(utilisateur=admin_user)
    print(f"✓ Created admin: {admin_user.identifiant}")
    
    # Create Departments
    dept1 = Departement.objects.create(
        nom="Mathématiques",
        code_departement="MATH001",
        college=college1
    )
    dept2 = Departement.objects.create(
        nom="Sciences",
        code_departement="SCI001",
        college=college1
    )
    dept3 = Departement.objects.create(
        nom="Lettres",
        code_departement="LET001",
        college=college2
    )
    print(f"✓ Created departments")
    
    # Create Teacher Users
    teacher1_user = Utilisateur.objects.create(
        nom="Dupont",
        prenom="Marie",
        tel="0611111111",
        mail="marie.dupont@agl.fr",
        identifiant="prof001"
    )
    teacher1 = Enseignant.objects.create(
        utilisateur=teacher1_user,
        indice=500,
        datePriseFonction=date(2020, 9, 1),
        departement=dept1
    )
    
    teacher2_user = Utilisateur.objects.create(
        nom="Martin",
        prenom="Pierre",
        tel="0622222222",
        mail="pierre.martin@agl.fr",
        identifiant="prof002"
    )
    teacher2 = Enseignant.objects.create(
        utilisateur=teacher2_user,
        indice=450,
        datePriseFonction=date(2021, 9, 1),
        departement=dept2
    )
    
    teacher3_user = Utilisateur.objects.create(
        nom="Bernard",
        prenom="Sophie",
        tel="0633333333",
        mail="sophie.bernard@agl.fr",
        identifiant="prof003"
    )
    teacher3 = Enseignant.objects.create(
        utilisateur=teacher3_user,
        indice=480,
        datePriseFonction=date(2019, 9, 1),
        departement=dept3
    )
    print(f"✓ Created teachers")
    
    # Assign department heads
    dept1.responsable = teacher1
    dept1.save()
    dept2.responsable = teacher2
    dept2.save()
    print(f"✓ Assigned department heads")
    
    # Create Classrooms
    salle1 = Salle.objects.create(numero="101", capacite=30)
    salle2 = Salle.objects.create(numero="102", capacite=25)
    salle3 = Salle.objects.create(numero="201", capacite=35)
    print(f"✓ Created classrooms")
    
    # Create Subjects
    matiere1 = Matiere.objects.create(
        libelle="Algèbre",
        departement=dept1,
        enseignant=teacher1,
        salle=salle1
    )
    matiere2 = Matiere.objects.create(
        libelle="Géométrie",
        departement=dept1,
        enseignant=teacher1,
        salle=salle1
    )
    matiere3 = Matiere.objects.create(
        libelle="Physique",
        departement=dept2,
        enseignant=teacher2,
        salle=salle2
    )
    matiere4 = Matiere.objects.create(
        libelle="Français",
        departement=dept3,
        enseignant=teacher3,
        salle=salle3
    )
    print(f"✓ Created subjects")
    
    # Create Student Users
    student1_user = Utilisateur.objects.create(
        nom="Dubois",
        prenom="Jean",
        tel="0644444444",
        mail="jean.dubois@student.agl.fr",
        identifiant="eleve001"
    )
    student1 = Eleve.objects.create(
        utilisateur=student1_user,
        anneeEntree=2022
    )
    
    student2_user = Utilisateur.objects.create(
        nom="Laurent",
        prenom="Julie",
        tel="0655555555",
        mail="julie.laurent@student.agl.fr",
        identifiant="eleve002"
    )
    student2 = Eleve.objects.create(
        utilisateur=student2_user,
        anneeEntree=2022
    )
    
    student3_user = Utilisateur.objects.create(
        nom="Moreau",
        prenom="Lucas",
        tel="0666666666",
        mail="lucas.moreau@student.agl.fr",
        identifiant="eleve003"
    )
    student3 = Eleve.objects.create(
        utilisateur=student3_user,
        anneeEntree=2023
    )
    print(f"✓ Created students")
    
    # Create Course Content
    cours1 = Cours.objects.create(
        titre="Introduction à l'algèbre",
        type_contenu="cours",
        contenu="Ce cours couvre les bases de l'algèbre: équations, inéquations, systèmes...",
        matiere=matiere1,
        enseignant=teacher1
    )
    cours2 = Cours.objects.create(
        titre="Exercices d'algèbre - Niveau 1",
        type_contenu="exercice",
        contenu="Exercice 1: Résoudre 2x + 5 = 13\nExercice 2: Résoudre 3x - 7 = 2",
        matiere=matiere1,
        enseignant=teacher1
    )
    cours3 = Cours.objects.create(
        titre="Les lois de Newton",
        type_contenu="cours",
        contenu="Ce cours présente les trois lois fondamentales de la mécanique...",
        matiere=matiere3,
        enseignant=teacher2
    )
    print(f"✓ Created course content")
    
    # Create Grades
    Notes.objects.create(eleve=student1, matiere=matiere1, valeur=15.5)
    Notes.objects.create(eleve=student1, matiere=matiere2, valeur=14.0)
    Notes.objects.create(eleve=student1, matiere=matiere3, valeur=16.5)
    Notes.objects.create(eleve=student1, matiere=matiere4, valeur=13.0)
    
    Notes.objects.create(eleve=student2, matiere=matiere1, valeur=17.0)
    Notes.objects.create(eleve=student2, matiere=matiere2, valeur=16.5)
    Notes.objects.create(eleve=student2, matiere=matiere3, valeur=15.0)
    Notes.objects.create(eleve=student2, matiere=matiere4, valeur=18.0)
    
    Notes.objects.create(eleve=student3, matiere=matiere1, valeur=12.0)
    Notes.objects.create(eleve=student3, matiere=matiere2, valeur=11.5)
    Notes.objects.create(eleve=student3, matiere=matiere3, valeur=13.5)
    Notes.objects.create(eleve=student3, matiere=matiere4, valeur=14.5)
    print(f"✓ Created grades")
    
    # Create Attendance Records
    from datetime import timedelta
    today = date.today()
    
    for i in range(10):
        day = today - timedelta(days=i)
        Presence.objects.create(
            eleve=student1,
            matiere=matiere1,
            date=day,
            present=(i % 3 != 0),  # Absent every 3rd day
            enseignant=teacher1
        )
    
    for i in range(10):
        day = today - timedelta(days=i)
        Presence.objects.create(
            eleve=student2,
            matiere=matiere1,
            date=day,
            present=True,  # Always present
            enseignant=teacher1
        )
    
    for i in range(10):
        day = today - timedelta(days=i)
        Presence.objects.create(
            eleve=student3,
            matiere=matiere3,
            date=day,
            present=(i % 2 == 0),  # Absent every other day
            enseignant=teacher2
        )
    print(f"✓ Created attendance records")
    
    print("\n" + "="*50)
    print("Sample data created successfully!")
    print("="*50)
    print("\nLogin credentials:")
    print("-" * 50)
    print("Administrator:")
    print("  Identifiant: admin001")
    print("\nTeachers:")
    print("  Identifiant: prof001 (Marie Dupont - Dept Head)")
    print("  Identifiant: prof002 (Pierre Martin - Dept Head)")
    print("  Identifiant: prof003 (Sophie Bernard)")
    print("\nStudents:")
    print("  Identifiant: eleve001 (Jean Dubois)")
    print("  Identifiant: eleve002 (Julie Laurent)")
    print("  Identifiant: eleve003 (Lucas Moreau)")
    print("-" * 50)

if __name__ == "__main__":
    create_sample_data()
