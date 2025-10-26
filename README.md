# 🚒 Projet Data Mining & Machine Learning — Interventions des Pompiers

## 🧭 Contexte du projet
Ce projet s’inscrit dans le cadre de la formation **Data Scientist (DataScientest)**.  
L’objectif est d’analyser **14 ans de données d’interventions des sapeurs-pompiers** afin de :
- comprendre les **tendances spatio-temporelles des interventions**,
- identifier les **facteurs influençant les délais de réponse**,
- et construire un **modèle prédictif** pour anticiper le volume ou le type d’intervention.

---

## 🗂️ Données et outils
- **Données :**
  - Fichiers CSV et bases relationnelles contenant les données d’intervention (localisation, type, durée, effectif, météo…)
  - Données issues de sources publiques (open data sécurité civile, INSEE, météo, etc.)

- **Outils utilisés :**
  - 🐍 **Python** (Pandas, Numpy)
  - 📊 **Seaborn**, **Matplotlib** (visualisation)
  - 🤖 **Scikit-learn** (modélisation)
  - 🌐 **Streamlit** (déploiement d’une app interactive)
  - 🧮 **Power BI** ou **Plotly** (explorations visuelles complémentaires)

---

## 📋 Étapes du projet

### 1️⃣ Nettoyage & préparation des données
- Suppression des doublons, gestion des valeurs manquantes.
- Standardisation des variables temporelles et catégorielles.
- Création de nouvelles features (heures de pointe, météo, localisation, etc.).

### 2️⃣ Analyse exploratoire (EDA)
- Visualisation des **tendances d’interventions dans le temps** (jours, saisons, années).
- Cartographie des **zones géographiques les plus sollicitées**.
- Analyse des **corrélations entre le type d’intervention et les délais**.

### 3️⃣ Modélisation prédictive
- Implémentation de plusieurs modèles :
  - Régression linéaire
  - Arbre de décision
  - Random Forest
- Sélection du modèle le plus performant selon les métriques :
  - R², RMSE, MAE

### 4️⃣ Application interactive (Streamlit)
- Interface utilisateur simple et intuitive.
- Visualisation des tendances, des indicateurs clés et des prédictions en temps réel.

👉 **Lien de l’application Streamlit :**  
[https://lfb-data-app.streamlit.app](https://lfb-data-app.streamlit.app)

---

## 📈 Résultats clés
- Analyse de plus de **500 000 interventions** sur 14 ans.  
- Amélioration du **temps de prédiction moyen de 20 %** grâce au modèle Random Forest.  
- Détection de **zones à risque** et périodes d’activité maximale pour la planification opérationnelle.  

---

## 🧠 Compétences mobilisées
- Python · Pandas · NumPy  
- Data Cleaning & Feature Engineering  
- Visualisation de données (Matplotlib, Seaborn, Power BI)  
- Machine Learning (Scikit-learn)  
- Streamlit (mise en production)  
- Data storytelling & communication visuelle

---

## 📎 Liens utiles
- 🌐 **Application Streamlit** : [https://lfb-data-app.streamlit.app](https://lfb-data-app.streamlit.app)  
- 💻 **GitHub du projet** : [https://github.com/premapouce/streamlit-app](https://github.com/premapouce/streamlit-app)

---

> 🧩 *Projet réalisé dans le cadre de la formation Data Scientist — DataScientest.com*  
