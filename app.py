import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

df = pd.read_excel(
    "05_Ingenierie_Industrie.xlsx",
    sheet_name="Données",
    header=2
)

df["Date intervention"] = pd.to_datetime(
    df["Date intervention"],
    errors="coerce"
)

df["Arrêt machine (h)"] = pd.to_numeric(
    df["Arrêt machine (h)"],
    errors="coerce"
)

df["Travail (h)"] = pd.to_numeric(
    df["Travail (h)"],
    errors="coerce"
)

df["Coût pièces (MAD)"] = pd.to_numeric(
    df["Coût pièces (MAD)"],
    errors="coerce"
)

df["Contrôle sécurité"] = df["Contrôle sécurité"].fillna(
    "Non applicable"
)

st.title("Tableau de bord - Maintenance industrielle")

st.sidebar.header("Filtres")

sites = ["Tous"] + sorted(
    df["Site"].dropna().unique().tolist()
)

site_selectionne = st.sidebar.selectbox(
    "Site",
    sites
)

maintenances = ["Toutes"] + sorted(
    df["Maintenance"].dropna().unique().tolist()
)

maintenance_selectionnee = st.sidebar.selectbox(
    "Type de maintenance",
    maintenances
)

df_filtre = df.copy()

if site_selectionne != "Tous":
    df_filtre = df_filtre[
        df_filtre["Site"] == site_selectionne
    ]

if maintenance_selectionnee != "Toutes":
    df_filtre = df_filtre[
        df_filtre["Maintenance"] == maintenance_selectionnee
    ]


total_interventions = len(df_filtre)

total_arret = df_filtre[
    "Arrêt machine (h)"
].sum()

cout_total = df_filtre[
    "Coût pièces (MAD)"
].sum()

if total_interventions > 0:
    taux_gravite = (
        (df_filtre["Gravité"] == "Élevée").sum()
        / total_interventions
        * 100
    )
else:
    taux_gravite = 0


col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Interventions",
    total_interventions
)

col2.metric(
    "Heures d'arrêt",
    f"{total_arret:.1f} h"
)

col3.metric(
    "Coût des pièces",
    f"{cout_total:,.0f} MAD"
)

col4.metric(
    "Gravité élevée",
    f"{taux_gravite:.1f} %"
)


st.subheader("1. Heures d'arrêt par équipement")

arret_equipement = (
    df_filtre.groupby("Équipement")["Arrêt machine (h)"]
    .sum()
    .sort_values(ascending=False)
)

if not arret_equipement.empty:

    equipement_max = arret_equipement.idxmax()
    arret_max = arret_equipement.max()

    st.metric(
        "Équipement avec le plus d'heures d'arrêt",
        equipement_max,
        f"{arret_max:.1f} h"
    )

    fig, ax = plt.subplots()

    arret_equipement.plot(
        kind="bar",
        ax=ax
    )

    ax.set_xlabel("Équipement")
    ax.set_ylabel("Heures d'arrêt")
    ax.set_title("Total des heures d'arrêt par équipement")

    plt.xticks(rotation=45)

    st.pyplot(fig)

else:
    st.warning("Aucune donnée disponible pour les filtres sélectionnés.")

st.subheader("2. Comparaison entre maintenance corrective et préventive")

comparaison = (
    df_filtre.groupby("Maintenance")[
        ["Coût pièces (MAD)", "Arrêt machine (h)"]
    ]
    .mean()
    .round(2)
)

st.dataframe(comparaison)

if "Corrective" in comparaison.index and "Préventive" in comparaison.index:

    cout_corrective = comparaison.loc[
        "Corrective", "Coût pièces (MAD)"
    ]

    cout_preventive = comparaison.loc[
        "Préventive", "Coût pièces (MAD)"
    ]

    arret_corrective = comparaison.loc[
        "Corrective", "Arrêt machine (h)"
    ]

    arret_preventive = comparaison.loc[
        "Préventive", "Arrêt machine (h)"
    ]

    st.write(
        f"En moyenne, une intervention corrective coûte "
        f"{cout_corrective:.2f} MAD en pièces contre "
        f"{cout_preventive:.2f} MAD pour une intervention préventive."
    )

    st.write(
        f"L'arrêt moyen est de {arret_corrective:.2f} h "
        f"pour la maintenance corrective contre "
        f"{arret_preventive:.2f} h pour la maintenance préventive."
    )

    st.info(
        "Ces résultats montrent une différence entre les deux types "
        "de maintenance, mais ils ne permettent pas de conclure "
        "qu'un type de maintenance est directement la cause de cette différence."
    )

else:
    st.info(
        "Sélectionnez 'Toutes' dans le filtre Type de maintenance "
        "pour comparer la maintenance corrective et préventive."
    )

st.subheader("3. Taux d'interventions de gravité élevée par site")

total_par_site = df_filtre.groupby("Site").size()

grave_par_site = (
    df_filtre[df_filtre["Gravité"] == "Élevée"]
    .groupby("Site")
    .size()
)

taux_grave_site = (
    grave_par_site
    .div(total_par_site)
    .fillna(0)
    .mul(100)
    .sort_values(ascending=False)
)

if not taux_grave_site.empty:

    site_max = taux_grave_site.idxmax()
    taux_max = taux_grave_site.max()

    st.metric(
        "Site avec le taux de gravité élevée le plus important",
        site_max,
        f"{taux_max:.1f} %"
    )

    fig, ax = plt.subplots()

    taux_grave_site.plot(
        kind="bar",
        ax=ax
    )

    ax.set_title("Taux d'interventions de gravité élevée par site")
    ax.set_xlabel("Site")
    ax.set_ylabel("Taux (%)")

    plt.xticks(rotation=45)

    st.pyplot(fig)

    st.write(
        f"Le site {site_max} présente le taux le plus élevé "
        f"d'interventions de gravité élevée, avec {taux_max:.1f} %."
    )

else:
    st.warning("Aucune donnée disponible.")

st.subheader("4. Contrôle sécurité des interventions terminées")

terminees = df_filtre[
    df_filtre["Statut"] == "Terminée"
]

total_terminees = len(terminees)

a_revoir = (
    terminees["Contrôle sécurité"] == "À revoir"
).sum()

if total_terminees > 0:

    taux_a_revoir = (
        a_revoir / total_terminees * 100
    )

    st.metric(
        "Interventions nécessitant un nouveau contrôle",
        f"{taux_a_revoir:.1f} %"
    )

    controle = terminees[
        "Contrôle sécurité"
    ].value_counts()

    fig, ax = plt.subplots()

    controle.plot(
        kind="bar",
        ax=ax
    )

    ax.set_title(
        "Contrôle sécurité des interventions terminées"
    )
    ax.set_xlabel("Résultat du contrôle")
    ax.set_ylabel("Nombre d'interventions")

    plt.xticks(rotation=0)

    st.pyplot(fig)

    st.write(
        f"Parmi {total_terminees} interventions terminées, "
        f"{a_revoir} nécessitent un nouveau contrôle sécurité, "
        f"soit {taux_a_revoir:.1f} %."
    )

    st.info(
        "Cette proportion concerne uniquement les interventions "
        "terminées. Les interventions en cours ne doivent pas être "
        "interprétées comme conformes ou non conformes."
    )

else:
    st.warning(
        "Aucune intervention terminée pour les filtres sélectionnés."
    )

st.subheader("5. Évolution mensuelle des heures d'arrêt")

df_mois = df_filtre.dropna(
    subset=["Date intervention"]
).copy()

df_mois["Mois"] = df_mois[
    "Date intervention"
].dt.to_period("M")

arret_mensuel = (
    df_mois.groupby("Mois")["Arrêt machine (h)"]
    .sum()
    .sort_index()
)

if not arret_mensuel.empty:

    arret_mensuel.index = arret_mensuel.index.astype(str)

    fig, ax = plt.subplots()

    ax.plot(
        arret_mensuel.index,
        arret_mensuel.values,
        marker="o"
    )

    ax.set_title(
        "Évolution mensuelle des heures d'arrêt"
    )
    ax.set_xlabel("Mois")
    ax.set_ylabel("Heures d'arrêt")

    plt.xticks(rotation=45)

    st.pyplot(fig)

    mois_max = arret_mensuel.idxmax()
    valeur_max = arret_mensuel.max()

    st.write(
        f"Le mois avec le plus grand nombre d'heures "
        f"d'arrêt est {mois_max}, avec {valeur_max:.1f} heures."
    )

else:
    st.warning(
        "Aucune donnée disponible pour les filtres sélectionnés."
    )

st.subheader("6. Action de maintenance recommandée")

if not arret_equipement.empty:

    equipement_prioritaire = arret_equipement.idxmax()
    heures_prioritaires = arret_equipement.max()

    total_heures = arret_equipement.sum()

    if total_heures > 0:
        part_arret = (
            heures_prioritaires / total_heures * 100
        )
    else:
        part_arret = 0

    causes_equipement = (
        df_filtre[
            df_filtre["Équipement"] == equipement_prioritaire
        ]["Cause"]
        .value_counts()
    )

    if not causes_equipement.empty:
        cause_principale = causes_equipement.idxmax()
        nombre_cause = causes_equipement.max()

        st.write(
            f"L'équipement à prioriser est **{equipement_prioritaire}**. "
            f"Il totalise **{heures_prioritaires:.1f} heures d'arrêt**, "
            f"soit **{part_arret:.1f} %** des heures d'arrêt "
            f"des équipements affichés."
        )

        st.write(
            f"La cause d'intervention la plus fréquente sur cet équipement "
            f"est **{cause_principale}**, avec **{nombre_cause} interventions**."
        )

        st.success(
            f"Recommandation : renforcer la maintenance préventive de "
            f"{equipement_prioritaire}, en surveillant en priorité les "
            f"problèmes liés à « {cause_principale} ». "
            f"L'objectif est de réduire les arrêts machine et les "
            f"interventions correctives."
        )

else:
    st.warning(
        "Aucune donnée disponible pour établir une recommandation."
    )