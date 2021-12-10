# Exploitation automatique de pix-orga par classe en python

### Objectif 
Fournir des fichiers des résultats de l'avancée des campagnes PIX orga :
- par classe,
- lisibles,
- en html (ou en pdf),
- en particulier, pour fournir les résultats aux enseignants non inscrits dans Pix orga,
- en affichant les élèves n'ayant pas fait le parcours (déclencheur de l'affichage : 1 élève de la classe a fait le parcours)

Produire une synthèse de toutes les classes.

Gérer une personne administrant plusieurs établissements

### Fonctionnement
Lancer le programme python exploitation-auto-pix-orga.py puis renseigner vos identifiants pix-orga.

### Tests
- Le programme est utilisé pour une structure d'une centaine de classes.
- Il a été testé sans problèmes notables à l'aide de l'ide thonny : https://thonny.org/ (Il suffit d'installer thonny qui contient python, puis installer les bibliothèques en passant par "Tools" puis "Manage plugs-in...")

### Bilbiothèques python
- Utilise les bibliothèque pandas et requests (le plus souvent présente dans les packs python ou facilement installables)
- Facultativement utilise la bibliothèque xhtml2pdf pour générer les fichiers pdf. L'absence de la bibliothèque est gérée automatiquement. Le programme produit un document hmtl parfaitement lisible et de façon bien plus rapide que le pdf.

### Données personnelles
- Bien que ne créant pas de nouvelles données, l'usage de cette application nécessite une saisie sur le registre des traitements de données personnelles de l'établissement.
- Par ailleurs, les fichiers produits ne doivent pas être conservés au-delà de le la finalité qui est d'informer les équipes pédagogiques de l'avancée des campagnes.

### À faire
Traitement des certifications.

### Exemples
#### Parcours de rentrée

![Capture d'écran résultats d'un parcours de rentrée](Capture-%C3%A9cran-r%C3%A9sultats-parcours-rentr%C3%A9e.jpg) 

#### Parcours thématique

![Capture d'écran résultats d'un parcours de rentrée](Capture-%C3%A9cran-r%C3%A9sultats-parcours-th%C3%A9matique.jpg) 

#### Collecte de profil

![Capture d'écran résultats d'un parcours de rentrée](Capture-%C3%A9cran-collecte-profils.jpg) 
