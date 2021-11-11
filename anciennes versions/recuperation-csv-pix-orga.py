import requests
import shutil
import urllib.request
import pandas as pd

def donnees_perso():
    username='nom.prenom@ac-academie.fr'
    password='abc123'
    
    return username,password


def identification(username,password):
    data={'username':username,'password':password}
    r = requests.post("https://orga.pix.fr/api/token", data)
    token=str(r.json()['access_token'])
    user_id=str(r.json()['user_id'])
    return token,user_id

def choix_organisation(token,user_id):
    headers={'Authorization': 'Bearer '+ token}
    r = requests.get("https://orga.pix.fr/api/prescription/prescribers/"+user_id, headers=headers)
    organisations=[]
    print("Nom des organisations auxquelles vous êtes rattaché dans pix orga")
    for c in r.json()['included']:
        if c['type']=='organizations':
            organisations.append(c)
            print("Identifiant | Nom")
            print( c['id'],"       |",c['attributes']['name'])
        
    if len(organisations)>1:
        print("Choisissez l'organisation à traiter")
        organisation_id=input("Identifiant :")
    elif len(organisations)==1:
        organisation_id=organisations[0]['id']

    organisation_id=str(organisation_id)
    return organisation_id

def liste_campagnes(token,organisation_id,nb_campagnes_max=100):
    headers={'Authorization': 'Bearer '+ token}
    nb_campagnes_max = str(nb_campagnes_max)
    print("Récupération des résultats des "+nb_campagnes_max+" dernières campagnes non archivées (max !)")
    r = requests.get("https://orga.pix.fr/api/organizations/"+organisation_id+"/campaigns?page[number]=1&page[size]="+nb_campagnes_max, headers=headers)
    campagnes=r.json()['data']
    return campagnes
    
def creation_campagnes_csv(token,campagnes) :
    headers={'Authorization': 'Bearer '+ token}
    donnees=[]
    for campagne in campagnes :
        r = requests.get("https://orga.pix.fr/api/campaigns/"+str(campagne['id']), headers=headers)
        token_pour_csv = r.json()['data']['attributes']['token-for-campaign-results']
        if campagne['attributes']['type']=='ASSESSMENT':
            type_campagne="assessment"
        elif campagne['attributes']['type']=='PROFILES_COLLECTION':
            type_campagne="profiles-collection"
        url_csv="https://orga.pix.fr/api/campaigns/"+str(campagne['id'])+"/csv-"+type_campagne+"-results?accessToken="+token_pour_csv+"&lang=fr"
        
        try : 
            flect =  urllib.request.urlopen(url_csv) 
            nom_fichier_csv=flect.headers['content-disposition'][22:-1]
            try :
                fecrit= open(nom_fichier_csv, 'wb')
                shutil.copyfileobj(flect, fecrit)
                print(nom_fichier_csv)
                fecrit.close()
            except:
                print("Fichier en erreur d'écriture. Campagne : "+campagne['attributes']['name'])            
        except:
            print("!!! Fichier en erreur de lecture. Campagne : "+campagne['attributes']['name']+" !!!")

def creation_eleves_csv(token,organisation_id,nb_eleves_max=3000):
    listeeleves = []

    
    headers={'Authorization': 'Bearer '+ token}
    r = requests.get("https://orga.pix.fr/api/organizations/"+organisation_id+"/students?page[size]="+str(nb_eleves_max), headers=headers)
    
    for e in r.json()['data']:
        listeeleves.append((e['attributes']['last-name'],e['attributes']['first-name'],e['attributes']['division']))
        
    eleves=pd.DataFrame(listeeleves, columns=('Nom', 'Prénom', 'Classe'))
    print("Récupération de la liste des élèves")
    
    eleves.to_csv("eleves.csv",index=False,sep=';',quotechar='"')
    print("eleves.csv")
    


username,password = donnees_perso() 
token,user_id=identification(username,password)
organisation_id=choix_organisation(token,user_id)
campagnes=liste_campagnes(token,organisation_id)
creation_campagnes_csv(token,campagnes)
creation_eleves_csv(token,organisation_id)
