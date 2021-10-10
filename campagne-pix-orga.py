import pandas as pd
import os
from datetime import datetime
# Décommenter la ligne suivante pour ne générer de pdf
# from xhtml2pdf import pisa

# Le fichier csv eleves permet de connaitre les élèves n'ayant PAS fait la campagne
# Fichier facultatif
nom_fichier_csv_eleves="eleves.csv"
# Nom des colonnes du fichier csv eleves
colonne_nom="Nom"
colonne_prenom="Prénom"
colonne_classe="Classe"

fichier_csv_eleves_present=False

formatageA4portrait = '<style type="text/css">'\
' @page {@frame content_frame {left: 10pt;width: 556pt;top: 10pt;height: 802pt;}'\
' size: A4 portrait}'\
' h1 {font-size: 16px}'\
' h2 {font-size: 14px}'\
' table{ font-size: 12px ;font-family: sans-serif; border-collapse: collapse;  }'\
' td, th{border: 1px solid #ddd; padding: 3px;}'\
' th{text-align: left;  background-color: #1e7375;  color: white;}'\
' tr{padding:2px}'\
' tr:nth-child(even){background-color: #f2f2f2;}'\
' </style>'

# Lecture et formatage du fichier eleves.csv si il existe
try:
    eleves = pd.read_csv(nom_fichier_csv_eleves,sep=';',quotechar='"',usecols=[colonne_nom,colonne_prenom,colonne_classe])
    try:
        eleves.rename(columns = {colonne_prenom:'Prénom du Participant',colonne_nom:'Nom du Participant',colonne_classe:'Classe'}, inplace = True)
        eleves = eleves[['Classe', 'Nom du Participant','Prénom du Participant']]
        eleves.sort_values(by=['Classe', 'Nom du Participant','Prénom du Participant'],inplace = True)
        fichier_csv_eleves_present=True
    except:
        print("! Problème de formatage du fichier élèves :"+colonne_nom+";"+colonne_prenom+";"+colonne_classe)
except:
    print("! Pas fichier élèves, on ne pourra pas connaitre les élèves n'ayant PAS fait la campagne")
    print("! Fournir un fichier csv nommé : "+nom_fichier_csv_eleves+" muni des colonnes : "+colonne_nom+";"+colonne_prenom+";"+colonne_classe)





#Exploitation des résultats

date_du_jour=datetime.now().strftime('%Y-%m-%d')

liste_fichiers = os.listdir()
liste_fichier_afaire =[]

for chemin_fichier in liste_fichiers :
    if chemin_fichier.partition(".")[2] == "csv":
        nom_fichier = chemin_fichier.partition(".")[0].rsplit("-")
        if '-'.join(nom_fichier[-4:-1]) == date_du_jour :
            titre = '-'.join(nom_fichier[:-5])
            titre += '-'+date_du_jour
            liste_fichier_afaire.append(chemin_fichier)
            resultats = pd.read_csv(chemin_fichier,sep=';',quotechar='"',decimal=',')

            resultats.sort_values(by=['Classe', 'Nom du Participant','Prénom du Participant'],inplace = True)
            
         
            
            #Simplification du tableau
            # Pour traiter les campagnes de rentrée de type "Pour commencer ..."
            if 'Palier obtenu (/3)' in resultats.columns :
                resultats = resultats[[ 'Nom du Participant','Prénom du Participant','Classe','% de progression','Palier obtenu (/3)']]
                masque=pd.notna(resultats['Palier obtenu (/3)'])
                resultats['Palier obtenu (/3)'] = resultats['Palier obtenu (/3)'].where(masque,'Non finalisé')
            # Pour traiter la campagne de vérification des certifiables
            elif 'Certifiable (O/N)' in resultats.columns :
                resultats = resultats[[ 'Nom du Participant','Prénom du Participant','Classe','Nombre de pix total','Certifiable (O/N)','Nombre de compétences certifiables']]
            # Pour traiter les autres campagnes
            else :
                resultats = resultats[[ 'Nom du Participant','Prénom du Participant','Classe','% de progression','Partage (O/N)']]
                resultats.rename(columns = {'Partage (O/N)':'Finalisé (O/N)'}, inplace = True)
                
            #Mise en forme colonne progression
            if '% de progression' in resultats.columns :
                #"resultats['% de progression'] = resultats['% de progression'].str.replace(',','.')
                resultats['% de progression'] = resultats['% de progression'].apply(lambda x: str(round(float(x)*100,1))+ '%')
            
            liste_des_classes = resultats['Classe'].unique()

            # Fusion avec la liste de tous les élèves
            if fichier_csv_eleves_present: 
                resultats=pd.merge(left=resultats,right=eleves,how='outer',on=['Classe', 'Nom du Participant','Prénom du Participant'])

            texte_HTML=formatageA4portrait +'<h1>'+ titre +'</h1>'
            
            for classe in liste_des_classes :
                resultats_classe = resultats[resultats['Classe']==classe]
                texte_HTML += '<h2>'+ classe +'</h2>'+ resultats_classe.to_html(index=False,na_rep=" ")+ '<div style="page-break-before:always">&nbsp;</div>'

            nom_du_fichier_HTML = titre +'.html'
            fichier_HTML = open(nom_du_fichier_HTML, "w")
            fichier_HTML.write(texte_HTML)
            fichier_HTML.close()

# Décommenter pour ne pas générer un pdf
# Ne pas oublier de Dé/Commenter la bibliothèque xhtml2pdf
#            nom_du_fichier_PDF = titre + '.pdf'
#            fichier_PDF = open(nom_du_fichier_PDF, "w+b")
#            pisa.CreatePDF(texte_HTML,fichier_PDF)
#            fichier_PDF.close() 
            

        
