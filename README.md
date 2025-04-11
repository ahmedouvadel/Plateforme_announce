# 📢 Plateforme d'annonces

Bienvenue sur la plateforme d'annonces en ligne ! Cette application permet aux utilisateurs de publier, gérer et filtrer des annonces facilement, tandis que les administrateurs peuvent modérer et valider les contenus.

## 🔗 Démo vidéo (YouTube)
📺 Pour une démonstration complète, cliquez sur l'image ci-dessus ou regardez directement sur YouTube :
[Démo de l'application Plateforme d'annonces: AxamPlateforme Django + Tailwind CSS ](https://www.youtube.com/watch?v=fGGX80UEj2U)


<p align="center">
  <a href="https://www.youtube.com/watch?v=0T2A_rSh6HQ" target="_blank">  
    <img src="https://img.youtube.com/vi/fGGX80UEj2U/0.jpg" alt="Démo de l'application Plateforme d'annonces: AxamPlateforme Django" width="600"/>
  </a>
</p>
> Cette vidéo vous guide à travers toutes les fonctionnalités principales :
> - 🔐 Authentification (Inscription / Connexion)
> - 👤 Gestion de profil utilisateur avec photo
> - 📝 Ajout, modification et suppression d'annonces
> - ✅ Validation ou rejet des annonces côté admin
> - 📊 Tableau de bord avec statistiques dynamiques
> - 🔍 Filtrage par statut (en attente, validées, rejetées)

## 🚀 Fonctionnalités principales

### Utilisateurs
- Création de compte avec informations personnelles (email, téléphone, adresse, photo...)
- Connexion et mise à jour du profil
- Ajout d'annonces avec image, titre, description, catégorie
- Visualisation des annonces avec leur statut (en attente, validée, rejetée)

### Administrateur
- Interface de modération centralisée
- Dashboard statistiques (total, validées, rejetées...)
- Changement du statut d'une annonce (en temps réel)
- Liste complète de toutes les annonces avec filtrage

## 🛠️ Technologies utilisées
- Backend : Django 5.1 (Python)
- Frontend : HTML + TailwindCSS
- Authentification : Custom User model avec rôles (`admin` / `client`)
- Base de données : PostgreSQL ou SQLite

## 📁 Structure principale
```
├── authentication/      # Gestion des utilisateurs
├── announces/           # Modèle et logique des annonces
├── dashboard/           # Interfaces utilisateurs/admin
├── static/              # Fichiers CSS, logos, icônes
├── templates/           # Pages HTML avec Tailwind
├── media/               # Upload des images utilisateur / annonces
├── manage.py
└── README.md            # Ce fichier
```

## 📎 Liens utiles
- 🔗 URL de production / test : `http://127.0.0.1:8000/`
- 🔗 Lien de la démo YouTube : [https://www.youtube.com/watch?v=VOTRE_VIDEO_ID](https://www.youtube.com/watch?v=fGGX80UEj2U)

## 👨‍💻 Auteur
Développé par Ahmedou vadel && Dahoud Elatigh 🇲🇷

---

🧡 N'hésitez pas à mettre une ⭐ sur le repo si vous aimez le projet !

