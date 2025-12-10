import os
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# ---------- CONFIG PAGE ----------
st.set_page_config(
    page_title="Mini EDA Netflix – 8PRO408",
    page_icon="🎬",
    layout="wide"
)

# ---------- FONCTION DE CHARGEMENT DES DONNÉES ----------

@st.cache_data
def load_data():
    csv_path = os.path.join("..", "data", "netflix_titles.csv")
    df = pd.read_csv(csv_path)

    # Nettoyage de base (même logique que dans ton notebook)
    df.columns = df.columns.str.lower().str.replace(" ", "_")

    df["date_added"] = pd.to_datetime(
        df["date_added"].astype(str).str.strip(),
        format="%B %d, %Y",
        errors="coerce"
    )

    def first_value(x):
        if pd.isna(x):
            return np.nan
        return str(x).split(",")[0].strip()

    df["main_country"] = df["country"].apply(first_value)
    df["main_genre"] = df["listed_in"].apply(first_value)
    df["year_added"] = df["date_added"].dt.year

    return df


df = load_data()

# ---------- SIDEBAR (FILTRES) ----------

st.sidebar.title("⚙️ Filtres")

# Type de contenu
types = sorted(df["type"].dropna().unique().tolist())
selected_types = st.sidebar.multiselect(
    "Type de contenu",
    options=types,
    default=types
)

# Année d'ajout
if df["year_added"].notna().any():
    min_year = int(df["year_added"].min())
    max_year = int(df["year_added"].max())
else:
    min_year = 2000
    max_year = 2025

year_range = st.sidebar.slider(
    "Année d'ajout (year_added)",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

# Filtre pays (optionnel)
top_countries = (
    df["main_country"]
    .value_counts()
    .head(15)
    .index
    .tolist()
)
selected_countries = st.sidebar.multiselect(
    "Pays principaux (optionnel)",
    options=top_countries,
    default=top_countries
)

st.sidebar.markdown("---")
st.sidebar.caption("Mini-projet 8PRO408 – Maniang Kebe & Ibra Diankha")

# ---------- APPLICATION DES FILTRES ----------

filtered_df = df[df["type"].isin(selected_types)]

filtered_df = filtered_df[
    (filtered_df["year_added"].between(year_range[0], year_range[1]))
]

if selected_countries:
    filtered_df = filtered_df[filtered_df["main_country"].isin(selected_countries)]

# ---------- EN-TÊTE PRINCIPALE ----------

st.title("🎬 Analyse Exploratoire du Catalogue Netflix")
st.markdown(
    "Mini application Streamlit permettant d’explorer le dataset **Netflix Movies and TV Shows** "
    "(types de contenus, pays, genres et tendances temporelles)."
)

st.markdown(
    f"**Nombre de titres après filtres :** {len(filtered_df)}"
)

st.markdown("---")

# ---------- TABS PRINCIPALES ----------

tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Vue globale",
    "🌍 Pays & Genres",
    "🔍 Année sortie vs ajout",
    "📋 Tableau des titres"
])

# ----- TAB 1 : Vue globale -----
with tab1:
    st.subheader("Évolution des ajouts par année")

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
            title="Nombre de titres ajoutés par année (après filtres)"
        )
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.info("Aucune donnée à afficher pour la période sélectionnée.")

    st.markdown("—")
    st.subheader("Répartition Films vs Séries")

    type_counts = (
        filtered_df["type"]
        .value_counts()
        .reset_index()
    )
    type_counts.columns = ["type", "count"]

    if not type_counts.empty:
        fig_type = px.bar(
            type_counts,
            x="type",
            y="count",
            text="count",
            title="Répartition des types de contenus"
        )
        st.plotly_chart(fig_type, use_container_width=True)
    else:
        st.info("Aucun type de contenu à afficher.")

# ----- TAB 2 : Pays & Genres -----
with tab2:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top 10 des pays représentés")
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
                text="count",
                title="Top 10 des pays"
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("Aucun pays à afficher pour ces filtres.")

    with col2:
        st.subheader("Top 10 des genres principaux")
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
                text="count",
                title="Top 10 des genres"
            )
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.info("Aucun genre à afficher pour ces filtres.")

# ----- TAB 3 : Relation release_year / year_added -----
with tab3:
    st.subheader("Relation entre année de sortie et année d’ajout")

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
        st.info("Pas assez de données pour tracer ce graphique.")

# ----- TAB 4 : Tableau -----
with tab4:
    st.subheader("Aperçu des titres filtrés")

    cols_to_show = [
        "title", "type", "main_genre", "main_country",
        "release_year", "year_added", "rating", "duration"
    ]
    existing_cols = [c for c in cols_to_show if c in filtered_df.columns]

    if not filtered_df.empty:
        st.dataframe(
            filtered_df[existing_cols].sort_values(
                by=["year_added", "release_year"], ascending=[False, False]
            ),
            use_container_width=True,
            height=500
        )
    else:
        st.info("Aucune ligne à afficher avec les filtres actuels.")

st.markdown("---")
st.caption("Mini-projet 8PRO408 – Analyse Netflix | Réalisé par Maniang Kebe & Ibra Diankha ")
