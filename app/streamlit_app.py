import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

# ---------- Chargement et préparation des données ----------

@st.cache_data
def load_data():
    # chemin relatif depuis le dossier app/
    csv_path = os.path.join("..", "data", "netflix_titles.csv")
    df = pd.read_csv(csv_path)

    # Nettoyage similaire à ton notebook
    df.columns = df.columns.str.lower().str.replace(" ", "_")

    # Conversion date_added
    df["date_added"] = pd.to_datetime(
        df["date_added"].astype(str).str.strip(),
        format="%B %d, %Y",
        errors="coerce"
    )

    # Fonction utilitaire pour garder la première valeur d'une liste séparée par des virgules
    def first_value(x):
        if pd.isna(x):
            return np.nan
        return str(x).split(",")[0].strip()

    df["main_country"] = df["country"].apply(first_value)
    df["main_genre"] = df["listed_in"].apply(first_value)

    df["year_added"] = df["date_added"].dt.year

    return df


df = load_data()

# ---------- Interface Streamlit ----------

st.title("📺 Mini EDA Netflix – 8PRO408")
st.write("Exploration interactive du catalogue Netflix (films et séries).")

# Filtre sur le type de contenu
types = df["type"].dropna().unique().tolist()
selected_types = st.multiselect(
    "Type de contenu",
    options=types,
    default=types
)

filtered_df = df[df["type"].isin(selected_types)]

# Filtre sur l'année d'ajout
min_year = int(filtered_df["year_added"].min()) if filtered_df["year_added"].notna().any() else 2010
max_year = int(filtered_df["year_added"].max()) if filtered_df["year_added"].notna().any() else 2025

year_range = st.slider(
    "Année d'ajout (year_added)",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

filtered_df = filtered_df[
    (filtered_df["year_added"] >= year_range[0]) &
    (filtered_df["year_added"] <= year_range[1])
]

st.markdown(f"**Nombre de titres après filtres :** {len(filtered_df)}")

st.write("---")

# ---------- Graphique 1 : Ajouts par année ----------

st.subheader("📈 Nombre de titres ajoutés par année")

added_per_year = (
    filtered_df
    .groupby("year_added")
    .size()
    .reset_index(name="count")
    .dropna()
    .sort_values("year_added")
)

if not added_per_year.empty:
    fig1 = px.line(
        added_per_year,
        x="year_added",
        y="count",
        markers=True,
        title="Titres ajoutés sur Netflix par année"
    )
    st.plotly_chart(fig1, use_container_width=True)
else:
    st.info("Pas de données pour la période sélectionnée.")

st.write("---")

# ---------- Graphique 2 : Top pays ----------

st.subheader("🌍 Top 10 des pays représentés")

country_counts = (
    filtered_df["main_country"]
    .value_counts()
    .head(10)
    .reset_index()
)
country_counts.columns = ["country", "count"]

if not country_counts.empty:
    fig2 = px.bar(
        country_counts,
        x="country",
        y="count",
        title="Top 10 des pays",
        text="count"
    )
    fig2.update_layout(xaxis_title="Pays", yaxis_title="Nombre de titres")
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("Aucun pays à afficher pour ces filtres.")

st.write("---")

# ---------- Graphique 3 : Top genres ----------

st.subheader("🎭 Top 10 des genres principaux")

genre_counts = (
    filtered_df["main_genre"]
    .value_counts()
    .head(10)
    .reset_index()
)
genre_counts.columns = ["genre", "count"]

if not genre_counts.empty:
    fig3 = px.bar(
        genre_counts,
        x="genre",
        y="count",
        title="Top 10 des genres",
        text="count"
    )
    fig3.update_layout(xaxis_title="Genre", yaxis_title="Nombre de titres")
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.info("Aucun genre à afficher pour ces filtres.")

st.write("---")

# ---------- Graphique 4 : Scatter interactif ----------

st.subheader("🔍 Relation entre année de sortie et année d'ajout")

scatter_df = filtered_df.dropna(subset=["release_year", "year_added"])

if not scatter_df.empty:
    fig4 = px.scatter(
        scatter_df,
        x="release_year",
        y="year_added",
        color="type",
        hover_data=["title", "main_country", "main_genre"],
        title="Release Year vs Year Added"
    )
    st.plotly_chart(fig4, use_container_width=True)
else:
    st.info("Pas de données suffisantes pour ce graphique.")

st.write("---")

st.caption("Mini-projet 8PRO408 – Analyse Netflix (Streamlit)")
