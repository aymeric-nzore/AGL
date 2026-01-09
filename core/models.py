from django.db import models
from django.utils import timezone

class Utilisateur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    tel = models.CharField(max_length=30, blank=True)
    mail = models.EmailField(unique=True)
    identifiant = models.CharField(max_length=50, unique=True)

    def imprimerFiche(self):
        return f"{self.prenom} {self.nom} | {self.mail} | {self.tel}"

    def __str__(self):
        return f"{self.prenom} {self.nom}"

class Administrateur(models.Model):
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, related_name="administrateur")

    def gererSysteme(self):
        return "Gestion du système"

    def __str__(self):
        return f"Admin: {self.utilisateur}"

class Academie(models.Model):
    nom = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.nom

class College(models.Model):
    nom = models.CharField(max_length=150, unique=True)
    adresse = models.TextField(blank=True)
    telephone = models.CharField(max_length=30, blank=True)
    siteWeb = models.URLField(blank=True)
    academie = models.ForeignKey(Academie, on_delete=models.CASCADE, related_name="colleges")

    def __str__(self):
        return self.nom

class Departement(models.Model):
    nom = models.CharField(max_length=150)
    code_departement = models.CharField(max_length=50, unique=True)
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name="departements")
    responsable = models.OneToOneField('Enseignant', on_delete=models.SET_NULL, null=True, blank=True, related_name="departement_dirige")

    def __str__(self):
        return f"{self.nom} ({self.college})"
    
    def calculerMoyenneDepartement(self):
        """Calculate average for all students in department's subjects"""
        matieres = self.matieres.all()
        all_notes = []
        for matiere in matieres:
            all_notes.extend(matiere.notes_set.values_list('valeur', flat=True))
        return round(sum(all_notes) / len(all_notes), 2) if all_notes else 0.0

class Enseignant(models.Model):
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, related_name="enseignant")
    indice = models.IntegerField()
    datePriseFonction = models.DateField(default=timezone.now)
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE, related_name="enseignants")

    def __str__(self):
        return f"Ens: {self.utilisateur}"

class Salle(models.Model):
    numero = models.CharField(max_length=50)
    capacite = models.IntegerField()

    def __str__(self):
        return f"Salle {self.numero}"

class Matiere(models.Model):
    libelle = models.CharField(max_length=150)
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE, related_name="matieres")
    enseignant = models.ForeignKey(Enseignant, on_delete=models.SET_NULL, null=True, blank=True, related_name="matieres")
    salle = models.ForeignKey(Salle, on_delete=models.SET_NULL, null=True, blank=True, related_name="matieres")

    def calculerMoyenne(self):
        notes = self.notes_set.all()
        return round(sum(n.valeur for n in notes) / len(notes), 2) if notes else 0.0

    def __str__(self):
        return self.libelle

class Eleve(models.Model):
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, related_name="eleve")
    anneeEntree = models.IntegerField()

    def calculerMoyenneGenerale(self):
        notes = self.notes_set.all()
        return round(sum(n.valeur for n in notes) / len(notes), 2) if notes else 0.0
    
    def calculerHeuresAbsence(self):
        """Calculate total hours of absence"""
        absences = self.presences.filter(present=False).count()
        return absences  # Each absence = 1 hour (can be adjusted)

    def __str__(self):
        return f"Elève: {self.utilisateur}"

class Notes(models.Model):
    valeur = models.FloatField()
    eleve = models.ForeignKey(Eleve, on_delete=models.CASCADE, related_name="notes_set")
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE, related_name="notes_set")

    class Meta:
        unique_together = ("eleve", "matiere")

    def __str__(self):
        return f"{self.eleve} - {self.matiere}: {self.valeur}"

class Cours(models.Model):
    """Course content and exercises added by teachers"""
    TYPE_CHOICES = [
        ('cours', 'Cours'),
        ('exercice', 'Exercice'),
    ]
    
    titre = models.CharField(max_length=200)
    type_contenu = models.CharField(max_length=20, choices=TYPE_CHOICES, default='cours')
    contenu = models.TextField()
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE, related_name="cours_set")
    enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE, related_name="cours_crees")
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Cours"

    def __str__(self):
        return f"{self.titre} ({self.matiere})"

class Presence(models.Model):
    """Attendance tracking for students"""
    eleve = models.ForeignKey(Eleve, on_delete=models.CASCADE, related_name="presences")
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE, related_name="presences")
    date = models.DateField(default=timezone.now)
    present = models.BooleanField(default=True)
    enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE, related_name="presences_marquees")

    class Meta:
        unique_together = ("eleve", "matiere", "date")
        ordering = ['-date']

    def __str__(self):
        status = "Présent" if self.present else "Absent"
        return f"{self.eleve} - {self.matiere} ({self.date}): {status}"