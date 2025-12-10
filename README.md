# 🎬 Mini-Projet – Analyse Exploratoire du Catalogue Netflix (EDA)
Projet réalisé dans le cadre du cours **8PRO408 - Outils de Programmation Python**.  
Ce mini-projet consiste à analyser le dataset *Netflix Movies and TV Shows* à l’aide de Python, Pandas, NumPy, Plotly et Streamlit.

---

## 📌 Objectifs du projet
- Explorer le dataset Netflix (films et séries).
- Nettoyer et préparer les données.
- Réaliser une **Analyse Exploratoire de Données (EDA)**.
- Produire plusieurs visualisations (Matplotlib, Seaborn, Plotly).
- Construire une **mini-application Streamlit** interactive.
- Générer un court rapport (1–2 pages).

---

## 📁 Structure du projet

netflix-eda/
│
├─ data/
│ └─ netflix_titles.csv # dataset brut
│
├─ notebooks/
│ └─ 01_netflix_eda.ipynb # notebook principal (EDA complète)
│
├─ app/
│ └─ streamlit_app.py # mini application Streamlit
│
├─ report/
│ └─ rapport_netflix.pdf # rapport final (1–2 pages)
│
└─ README.md # ce fichier


---

## 🔧 Installation & Pré-requis

### 1. Cloner le projet
```bash
git clone https://github.com/mkebe11/miniP-notebook.git
cd miniP-notebook

2. Créer un environnement (optionnel mais recommandé)
conda create -n netflix python=3.10
conda activate netflix

3. Installer les dépendances
pip install pandas numpy matplotlib seaborn plotly streamlit

Lancer le Notebook EDA

Dans un terminal :

jupyter notebook

Puis ouvrir le fichier :

notebooks/01_netflix_eda.ipynb


Le notebook contient :

Nettoyage des données

Analyses descriptives

Visualisations Matplotlib / Seaborn

Visualisations interactives Plotly

Interprétation et conclusion

🖥️ Lancer l’application Streamlit

Depuis le dossier app/ :

cd app
streamlit run streamlit_app.py


L’application affiche :

Nombre de titres par année d’ajout

Top 10 des pays

Top 10 des genres principaux

Scatter interactif (année de sortie vs année d’ajout)