import pandas as pd
import os
from datetime import datetime
# Décommenter pour générer un pdf
# from xhtml2pdf import pisa  

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
            resultats = pd.read_csv(chemin_fichier,sep=';',quotechar='"')

            resultats = resultats.sort_values(by=['Classe', 'Nom du Participant','Prénom du Participant'])
            
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
                resultats['% de progression'] = resultats['% de progression'].str.replace(',','.')
                resultats['% de progression'] = resultats['% de progression'].apply(lambda x: str(round(float(x)*100,1))+ '%')
            
            liste_des_classes = resultats['Classe'].unique()

            texte_HTML=formatageA4portrait +'<h1>'+ titre +'</h1>'
            
            for classe in liste_des_classes :
                resultats_classe = resultats[resultats['Classe']==classe]
                texte_HTML += '<h2>'+ classe +'</h2>'+ resultats_classe.to_html(index=False)+ '<div style="page-break-before:always">&nbsp;</div>'

            nom_du_fichier_HTML = titre +'.html'
            fichier_HTML = open(nom_du_fichier_HTML, "w")
            fichier_HTML.write(texte_HTML)
            fichier_HTML.close()

# Décommenter pour générer un pdf
# Ne pas oublier de décommenter la bilbiothèque xhtml2pdf
#            nom_du_fichier_PDF = titre + '.pdf'
#            fichier_PDF = open(nom_du_fichier_PDF, "w+b")
#            pisa.CreatePDF(texte_HTML,fichier_PDF)
#            fichier_PDF.close() 
            

        
