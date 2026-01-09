# Système de Gestion Académique (AGL)

## Description

Système d'information pour la gestion centralisée et efficace des cours, enseignants, étudiants, départements et notes au sein de plusieurs collèges d'une même académie.

## Fonctionnalités

### Authentification
- Connexion sécurisée pour les administrateurs, enseignants et élèves
- Gestion de session
- Contrôle d'accès basé sur les rôles

### Administrateurs
- **Tableau de bord** avec statistiques (collèges, départements, enseignants, élèves)
- **Gestion des Collèges** : Créer, lister, modifier et supprimer des collèges
- **Gestion des Départements** : Créer, lister et assigner des responsables de département
- **Gestion des Matières** : Créer, lister, modifier et supprimer des matières
- **Gestion des Salles** : Créer, lister, modifier et supprimer des salles de classe
- **Affectation des ressources** : Assigner des enseignants et des salles aux matières

### Enseignants
- **Tableau de bord** avec statistiques personnelles
- **Gestion des Cours** : Ajouter, modifier et supprimer des cours et exercices
- **Gestion des Notes** : Attribuer et modifier les notes des élèves
- **Gestion des Présences** : Marquer les présences et absences des élèves
- **Responsable de Département** : Calculer les moyennes du département (pour les chefs de département)
- **Fiche Signalétique** : Consulter et imprimer sa fiche d'informations

### Élèves
- **Tableau de bord** avec statistiques personnelles (moyenne générale, heures d'absence)
- **Consultation des Notes** : Voir toutes les notes par matière
- **Consultation des Présences** : Voir l'historique des présences/absences
- **Accès aux Cours** : Consulter les cours et exercices mis en ligne par les enseignants
- **Emploi du Temps** : Voir les matières, enseignants et salles
- **Fiche Signalétique** : Consulter et imprimer sa fiche d'informations

## Technologies Utilisées

- **Backend** : Django 6.0.1
- **Base de données** : SQLite (développement), PostgreSQL (production possible)
- **Frontend** : Tailwind CSS (via CDN)
- **Langage** : Python 3.12+

## Installation

### Prérequis
- Python 3.12 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. **Cloner le dépôt**
```bash
git clone https://github.com/aymeric-nzore/AGL.git
cd AGL
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3. **Appliquer les migrations**
```bash
python manage.py migrate
```

4. **Créer des données de test** (optionnel)
```bash
python create_sample_data.py
```

5. **Lancer le serveur de développement**
```bash
python manage.py runserver
```

6. **Accéder à l'application**
Ouvrir un navigateur et aller à : `http://localhost:8000/`

## Identifiants de Test

Après avoir exécuté le script `create_sample_data.py`, vous pouvez utiliser les identifiants suivants :

### Administrateur
- **Identifiant** : `admin001`

### Enseignants
- **Identifiant** : `prof001` (Marie Dupont - Responsable du département Mathématiques)
- **Identifiant** : `prof002` (Pierre Martin - Responsable du département Sciences)
- **Identifiant** : `prof003` (Sophie Bernard)

### Élèves
- **Identifiant** : `eleve001` (Jean Dubois - Moyenne: 14,75/20)
- **Identifiant** : `eleve002` (Julie Laurent)
- **Identifiant** : `eleve003` (Lucas Moreau)

## Structure du Projet

```
AGL/
├── agl/                    # Configuration Django
│   ├── settings.py        # Paramètres de l'application
│   ├── urls.py            # Routes principales
│   └── wsgi.py            # Point d'entrée WSGI
├── core/                   # Application principale
│   ├── models.py          # Modèles de données
│   ├── views.py           # Vues et logique métier
│   ├── admin.py           # Configuration admin Django
│   └── migrations/        # Migrations de base de données
├── templates/              # Templates HTML
│   ├── base.html          # Template de base
│   ├── login.html         # Page de connexion
│   ├── profile.html       # Fiche signalétique
│   ├── admin_dashboard.html
│   ├── teacher_dashboard.html
│   ├── student_dashboard.html
│   ├── form_generic.html  # Template générique de formulaire
│   └── list_generic.html  # Template générique de liste
├── create_sample_data.py  # Script de création de données de test
├── manage.py              # Script de gestion Django
└── requirements.txt       # Dépendances Python
```

## Modèles de Données

### Utilisateur
- Nom, Prénom, Téléphone, Email, Identifiant
- Relations : Administrateur, Enseignant ou Élève

### Académie
- Nom

### Collège
- Nom, Adresse, Téléphone
- Relation : Académie

### Département
- Nom, Code département
- Relations : Collège, Responsable (Enseignant)

### Enseignant
- Indice, Date de prise de fonction
- Relations : Utilisateur, Département

### Matière
- Libellé
- Relations : Département, Enseignant, Salle

### Salle
- Numéro, Capacité

### Élève
- Année d'entrée
- Relation : Utilisateur

### Notes
- Valeur (sur 20)
- Relations : Élève, Matière

### Cours
- Titre, Type (cours/exercice), Contenu
- Relations : Matière, Enseignant

### Présence
- Date, Présent (booléen)
- Relations : Élève, Matière, Enseignant

## Configuration

### Base de données

Par défaut, le projet utilise SQLite. Pour utiliser PostgreSQL en production :

1. Installer psycopg2 : `pip install psycopg2-binary`
2. Modifier `agl/settings.py` :

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "nom_base",
        "USER": "utilisateur",
        "PASSWORD": "mot_de_passe",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
```

## Administration Django

Le panneau d'administration Django est accessible à : `http://localhost:8000/django-admin/`

Pour créer un superutilisateur :
```bash
python manage.py createsuperuser
```

## Développement

### Créer de nouvelles migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Lancer les tests
```bash
python manage.py test
```

## Contribution

1. Fork le projet
2. Créer une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## Licence

Ce projet est développé dans un cadre académique.

## Auteurs

- Développé pour l'académie de gestion des collèges

## Support

Pour toute question ou problème, veuillez ouvrir une issue sur GitHub.
