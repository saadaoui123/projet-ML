# Projet de Prédiction de Loyers en Tunisie 🇹🇳

Ce projet est une application complète de Machine Learning permettant de prédire les loyers d'appartements en Tunisie en fonction de plusieurs critères (Ville, Superficie, Standing, etc.).

## Structure du Projet

```
tunisian_rent_project/
├── data/
│   └── dataset_loyers_tunisie.csv  # Généré par le notebook
├── models/
│   └── model_loyer.joblib          # Modèle entraîné (à générer)
├── notebooks/
│   └── prediction_loyer.ipynb      # Notebook complet (Génération, EDA, Modélisation)
├── app.py                          # Interface utilisateur Streamlit
├── requirements.txt                # Liste des dépendances
└── README.md                       # Ce fichier
```

## Installation

1. **Prérequis** : Assurez-vous d'avoir Python installé.
2. **Installation des dépendances** :
   Ouvrez un terminal dans le dossier du projet et exécutez :
   ```bash
   pip install -r requirements.txt
   ```

## Utilisation

### Étape 1 : Générer le Modèle
Avant de lancer l'application, vous devez exécuter le notebook pour générer les données et entraîner le modèle.

1. Ouvrez Jupyter Notebook ou VS Code.
2. Ouvrez le fichier `notebooks/prediction_loyer.ipynb`.
3. Exécutez toutes les cellules ("Run All").
   - Cela va créer le fichier de données dans `data/`.
   - Cela va sauvegarder le modèle entraîné dans `models/model_loyer.joblib`.

### Étape 2 : Lancer l'Application
Une fois le modèle généré, lancez l'interface Streamlit :

```bash
streamlit run app.py
```

Une page web s'ouvrira (généralement à l'adresse `http://localhost:8501`) où vous pourrez entrer les caractéristiques d'un appartement et obtenir une estimation du loyer.

## Détails Techniques

- **Données** : 800 entrées synthétiques générées avec la librairie `Faker` et des règles logiques basées sur le marché tunisien.
- **Modèles Testés** : Régression Linéaire, Random Forest, Ridge.
- **Modèle Final** : Le meilleur modèle (généralement Random Forest) est sauvegardé via `joblib`.
- **Interface** : Développée avec `Streamlit` pour une interactivité simple et rapide.

## Auteur
Projet réalisé dans le cadre du cours de Machine Learning.
