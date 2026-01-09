from django.contrib import admin
from .models import (
    Utilisateur, Administrateur, Academie, College, Departement,
    Enseignant, Salle, Matiere, Eleve, Notes, Cours, Presence
)

admin.site.register(Utilisateur)
admin.site.register(Administrateur)
admin.site.register(Academie)
admin.site.register(College)
admin.site.register(Departement)
admin.site.register(Enseignant)
admin.site.register(Salle)
admin.site.register(Matiere)
admin.site.register(Eleve)
admin.site.register(Notes)
admin.site.register(Cours)
admin.site.register(Presence)