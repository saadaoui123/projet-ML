import streamlit as st
import pandas as pd
import joblib
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configuration de la page
st.set_page_config(
    page_title="Prédiction Prix Tunisie",
    page_icon="",
    layout="wide"
)

# Chargement du modèle
@st.cache_resource
def load_model():
    try:
        # Essayer d'abord de charger le meilleur modèle du notebook
        model = joblib.load('models/best_model.joblib')
        st.success("✅ Modèle best_model.joblib chargé (meilleur modèle du notebook)")
        return model
    except FileNotFoundError:
        try:
            # Fallback sur l'ancien modèle si best_model n'existe pas
            model = joblib.load('models/model_loyer.joblib')
            st.warning("⚠️ Utilisation de model_loyer.joblib. Exécutez le notebook pour générer best_model.joblib")
            return model
        except FileNotFoundError:
            st.error(" Aucun modèle trouvé. Veuillez exécuter le notebook prediction_loyer.ipynb ou generate_model.py")
            return None

model = load_model()

# Titre et Description
st.title("🏠 Estimateur de Prix - Tunisie")
st.markdown("""
Cette application utilise un modèle de Machine Learning pour estimer le prix d'un bien immobilier en Tunisie.
Remplissez les caractéristiques ci-dessous pour obtenir une estimation.
""")

col1, col2 = st.columns([1, 2])

with col1:
    st.header("Caractéristiques du Bien")
    
    with st.form("prediction_form"):
        # Sélection du type (Location ou Vente)
        type_bien = st.radio(
            "Type de transaction",
            options=["Location", "Vente"],
            horizontal=True,
            help="Choisissez si vous voulez estimer un loyer ou un prix de vente"
        )
        
        ville = st.selectbox(
            "Ville",
            ['Tunis', 'Ariana', 'Sfax', 'Sousse', 'Monastir', 'Bizerte', 'Nabeul']
        )
        
        superficie = st.slider("Superficie (m²)", 20, 300, 80)
        
        nb_pieces = st.number_input("Nombre de pièces (S+...)", min_value=1, max_value=10, value=2)
        
        standing = st.select_slider(
            "Standing",
            options=[1, 2, 3],
            format_func=lambda x: {1: "Économique", 2: "Moyen", 3: "Haut Standing"}[x]
        )
        
        etage = st.number_input("Étage", min_value=0, max_value=20, value=1)
        
        distance_centre = st.slider("Distance du centre-ville (km)", 0.0, 20.0, 5.0)
        
        meuble = st.checkbox("Meublé")
        
        # Bouton avec label dynamique
        button_label = f"Estimer le {'Loyer' if type_bien == 'Location' else 'Prix de Vente'}"
        submitted = st.form_submit_button(button_label)

with col2:
    if submitted and model is not None:
        # Préparation des données pour le modèle
        input_data = pd.DataFrame({
            'Ville': [ville],
            'Superficie': [superficie],
            'Standing': [standing],
            'Nb_pieces': [nb_pieces],
            'Meuble': [1 if meuble else 0],
            'Etage': [etage],
            'Distance_centre': [distance_centre],
            'Type': [type_bien]
        })
        
        # Prédiction
        prediction = model.predict(input_data)[0]
        
        st.success("Estimation réussie !")
        
        # Affichage du résultat avec label dynamique
        label_prix = "Loyer Mensuel Estimé" if type_bien == "Location" else "Prix de Vente Estimé"
        st.metric(
            label=label_prix,
            value=f"{int(prediction):,} TND".replace(',', ' '),
            delta=None
        )
        
        # Visualisation contextuelle
        st.subheader("Analyse du Prix")
        
        # Simulation de données pour le contexte
        if type_bien == "Location":
            avg_prices = {
                'Tunis': 1800, 'Ariana': 1700, 'Sousse': 1400, 
                'Sfax': 1200, 'Monastir': 1300, 'Nabeul': 1300, 'Bizerte': 1100
            }
        else:  # Vente
            avg_prices = {
                'Tunis': 270000, 'Ariana': 255000, 'Sousse': 210000, 
                'Sfax': 180000, 'Monastir': 195000, 'Nabeul': 195000, 'Bizerte': 165000
            }
        
        ref_price = avg_prices.get(ville, 150000 if type_bien == "Vente" else 1000)
        
        fig, ax = plt.subplots(figsize=(8, 4))
        
        # Comparaison simple
        categories = ['Moyenne Ville', 'Votre Estimation']
        values = [ref_price, prediction]
        colors = ['gray', 'green']
        
        sns.barplot(x=categories, y=values, palette=colors, ax=ax)
        ax.set_ylabel("Prix (TND)")
        ax.set_title(f"Comparaison avec la moyenne estimée à {ville}")
        
        for i, v in enumerate(values):
            ax.text(i, v + (v * 0.02), f"{int(v):,} TND".replace(',', ' '), ha='center')
            
        st.pyplot(fig)
        
        st.info(f"""
        **Note :** Cette estimation est basée sur des données synthétiques. 
        Les facteurs réels comme l'état précis du bien, le quartier exact et la vue peuvent influencer le prix final.
        
        💡 **Type sélectionné**: {type_bien}
        """)
    elif submitted and model is None:
        st.error("Impossible de faire une prédiction sans le modèle.")
    else:
        st.info("👈 Remplissez le formulaire et cliquez sur le bouton pour voir le résultat.")
        
        # Image d'illustration ou texte d'accueil
        st.markdown("### Comment ça marche ?")
        st.markdown("""
        1. **Type**: Choisissez entre Location (loyer) ou Vente (prix d'achat).
        2. **Ville** : La localisation influence fortement le prix.
        3. **Superficie & Pièces** : Plus c'est grand, plus c'est cher.
        4. **Standing** : La qualité des finitions joue un rôle clé.
        5. **Distance** : La proximité du centre-ville est valorisée.
        """)