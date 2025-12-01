import pandas as pd
import numpy as np
from faker import Faker
import random
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor

# Configuration
fake = Faker()
np.random.seed(42)
random.seed(42)

# 1. Génération de Données
print("Génération des données...")
def generate_data(n=800):
    data = []
    villes = ['Tunis', 'Ariana', 'Sfax', 'Sousse', 'Monastir', 'Bizerte', 'Nabeul']
    
    ville_coef = {
        'Tunis': 1.5, 'Ariana': 1.4, 'Sousse': 1.2, 
        'Sfax': 1.0, 'Monastir': 1.1, 'Nabeul': 1.1, 'Bizerte': 0.9
    }
    
    for _ in range(n):
        ville = random.choice(villes)
        superficie = random.randint(30, 250)
        nb_pieces = random.randint(1, 6)
        standing = random.choices([1, 2, 3], weights=[0.3, 0.5, 0.2])[0]
        meuble = random.choice([0, 1])
        etage = random.randint(0, 10)
        distance_centre = round(random.uniform(0.5, 20), 1)
        
        base_price = 300 + (superficie * 5) + (nb_pieces * 50)
        multiplier = ville_coef[ville]
        multiplier += (standing - 1) * 0.3
        multiplier += 0.2 if meuble else 0
        multiplier -= (distance_centre * 0.02)
        loyer = base_price * multiplier
        loyer += np.random.normal(0, 50)
        
        data.append([ville, superficie, standing, nb_pieces, meuble, etage, distance_centre, int(loyer)])
        
    return pd.DataFrame(data, columns=['Ville', 'Superficie', 'Standing', 'Nb_pieces', 'Meuble', 'Etage', 'Distance_centre', 'Loyer'])

df = generate_data(800)

# Création des dossiers si nécessaire
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, 'data')
models_dir = os.path.join(script_dir, 'models')

os.makedirs(data_dir, exist_ok=True)
os.makedirs(models_dir, exist_ok=True)

# Charger le dataset existant avec Type et Prix_vente
csv_path = os.path.join(data_dir, 'dataset_loyers_tunisie.csv')
print(f"Chargement du fichier: {csv_path}")
df_existing = pd.read_csv(csv_path)
print(f"Données chargées: {len(df_existing)} lignes")
print(f"Colonnes disponibles: {list(df_existing.columns)}")
print(f"\nPremières lignes:")
print(df_existing.head())

# Vérifier que Type et Prix_vente existent
if 'Type' not in df_existing.columns or 'Prix_vente' not in df_existing.columns:
    print("ERREUR: Les colonnes 'Type' et 'Prix_vente' doivent exister dans le dataset.")
    print("Veuillez d'abord exécuter modify_dataset.py")
    exit(1)

# 2. Prétraitement et Entraînement
print("\nEntraînement du modèle...")

# Utiliser Loyer pour Location et Prix_vente pour Vente comme target
# On crée une colonne Prix qui combine les deux
df_existing['Prix'] = df_existing.apply(
    lambda row: row['Loyer'] if row['Type'] == 'Location' else row['Prix_vente'], 
    axis=1
)

print(f"\nDistribution des types:")
print(df_existing['Type'].value_counts())
print(f"\nStatistiques des prix:")
print(df_existing.groupby('Type')['Prix'].describe())

X = df_existing[['Ville', 'Superficie', 'Standing', 'Nb_pieces', 'Meuble', 'Etage', 'Distance_centre', 'Type']]
y = df_existing['Prix']

categorical_features = ['Ville', 'Type']
numerical_features = ['Superficie', 'Standing', 'Nb_pieces', 'Meuble', 'Etage', 'Distance_centre']

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ])

# Utilisation de Random Forest comme meilleur modèle
model = Pipeline(steps=[('preprocessor', preprocessor),
                        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))])

model.fit(X, y)

# 3. Sauvegarde
model_path = os.path.join(models_dir, 'model_loyer.joblib')
joblib.dump(model, model_path)
print(f"\nModèle sauvegardé dans {model_path}")
print("Le modèle peut maintenant prédire les prix pour Location et Vente!")
