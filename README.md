# SYS-BOT
Un bot qui va analyser l'état des applications déployés sur un serveur et alerter automatiquement les administrateurs en cas d'erreur ou de dysfonctionnement.

- 🔧 Type de services et outils à vérifier 
  - Service WEB + API accessibilité et erreurs interne
  - Services Linux status
  - Container Docker status
  - Base de données connéctivité
  - SSH connectivité

### Pour le script qui verifier la connexion à la base de données:
  * Il faut installer le module "**mysql.connector**"
  * Installation du module: lancer la commande *pip install mysql-connector-python*
  * Puis, importer le module: *import mysql.connector*
    Merci ! 😊