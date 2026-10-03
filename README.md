# Tableau de bord - Maintenance industrielle

## Description

Ce projet présente un tableau de bord interactif consacré aux interventions de maintenance industrielle réalisées entre janvier et août 2026.

L'application permet d'analyser les heures d'arrêt des équipements, les coûts des pièces, les types de maintenance, la gravité des interventions et les contrôles de sécurité.

Les données utilisées sont entièrement fictives et destinées à un exercice de formation.

## Fonctionnalités

- Indicateurs clés sur les interventions de maintenance
- Filtres par site et type de maintenance
- Analyse des heures d'arrêt par équipement
- Comparaison entre maintenance corrective et préventive
- Analyse des interventions de gravité élevée par site
- Analyse des contrôles de sécurité
- Évolution mensuelle des heures d'arrêt
- Recommandation d'une action de maintenance prioritaire

## Technologies utilisées

- Python
- Pandas
- Matplotlib
- Streamlit
- OpenPyXL

## Lancer l'application

Installer les dépendances :

pip install -r requirements.txt

Puis lancer l'application :

streamlit run app.py

## Données

Le fichier utilisé est `05_Ingenierie_Industrie.xlsx`.

Une ligne représente une intervention sur un équipement de production.

## Auteur

Projet réalisé dans le cadre d'un exercice d'analyse de données et de création d'un tableau de bord avec Streamlit.