# Blog Application Web

## Description

Ce projet est une application web de blog développée en utilisant React pour le frontend et Django pour le backend. L'application permet aux utilisateurs de créer, gérer et interagir avec des articles de blog, tout en offrant une expérience utilisateur fluide et moderne.

## Technologies Utilisées

- **Backend :** Le backend est construit avec Django, utilisant Django REST Framework pour créer une API RESTful robuste. L'authentification est gérée via JSON Web Tokens (JWT) pour assurer une sécurité optimale. Nous avons également intégré Swagger pour la documentation de l'API, facilitant ainsi le développement et les tests.
  
- **Frontend :** Le frontend de l'application est développé en React, permettant une interface utilisateur réactive et dynamique. Grâce à React, les utilisateurs bénéficient d'une navigation fluide et d'interactions riches.

## Fonctionnalités Principales

- **Authentification :** Inscription, connexion et gestion de compte sécurisé avec JWT.
- **Création de blog :** Créez et publiez vos articles de blog directement sur la plateforme.
- **Gestion de blog :** Modifiez ou supprimez vos articles de blog à tout moment.
- **Consultation des blogs :** Parcourez et lisez les articles de blog publiés par d'autres utilisateurs.
- **Commentaires :** Commentez les articles de blog et engagez des discussions avec d'autres utilisateurs.
- **Likes :** Aimez les articles de blog et les commentaires, et recevez des notifications lorsque vos articles sont aimés.
- **Notifications :** Soyez notifié lorsque quelqu'un commente ou aime vos articles ou commentaires.
- **Autres fonctionnalités :** L'application est conçue pour évoluer avec de nouvelles fonctionnalités, afin d'enrichir l'expérience utilisateur.

## Installation et Déploiement

Pour exécuter ce projet localement, suivez les étapes ci-dessous :

1. **Clonez le dépôt :** `git https://github.com/felladib/Blog_app_UsingDjangoReact.git`
2. **Installez les dépendances backend :**
   ```bash
   cd backend
   pip install -r requirements.txt
3.**Lancez le serveur Django :**
  ```bash
  python manage.py runserver
  ```
4.**Installez les dépendances frontend :**
   ```bash
  cd frontend
  npm install
  ```
5.**Lancez l'application React :**
   ```bash
  npm start
  ```
