# Résultats-Campagne-PIX-orga

### Objectif 
Fournir des fichiers des résultats de l'avancée des campagnes PIX orga :
- lisibles,
- en html (et/ou pdf),
- en particulier, pour les enseignants non inscrits dans Pix orga,
Fonctionne avec les parcours de rentrée, les parcours par thème, les campagnes de collecte de profils
- optionnellement afficher les élèves n'ayant pas fait le parcours (déclencheur de l'affichage : 1 élève de la classe a fait le parcours)

### Fonctionnement
#### Fichiers csv des résultats et des élèves
- Démarrer le programme recuperation-csv-pix-orga.py en ayant pris soin de renseigner vos identifiants pix
Ou
- Déposer les fichiers csv (du jour)  dans le même dossier que le programme campagne-pix-orga.py
- Optionnellement, déposer un fichier csv eleves.csv avec la liste de tous les élèves. Colonnes : Nom, Prénom, Classe
#### Traitement des résultats
- Démarrer le programme campagne-pix-orga.py
- Récupérer les fichiers html (et/ou pdf) en sortie prêt à être rendu accessibles.

### Bilbiothèques python
- Utilise la bibliothèque pandas (le plus souvent présente dans les packs python)
- Facultativement utilise la bibliothèque xhtml2pdf pour générer les fichiers pdf

### Exemples
#### Parcours de rentrée

![Capture d'écran résultats d'un parcours de rentrée](Capture-%C3%A9cran-r%C3%A9sultats-parcours-rentr%C3%A9e.jpg) 

#### Parcours thématique

![Capture d'écran résultats d'un parcours de rentrée](Capture-%C3%A9cran-r%C3%A9sultats-parcours-th%C3%A9matique.jpg) 

#### Collecte de profil

![Capture d'écran résultats d'un parcours de rentrée](Capture-%C3%A9cran-collecte-profils.jpg) 
