import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="La Vie d'un Étudiant du 237", layout="wide", page_icon="🇨🇲")

# --- STYLE CSS PERSONNALISÉ POUR LE DESIGN ---
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
    }
    </style>
    """, unsafe_allow_input=True)

# --- BARRE LATÉRALE (MENU) ---
with st.sidebar:
    st.image("https://www.gstatic.com/lamda/images/gemini_sparkle_v002_d47353046511514565658.svg", width=50)
    st.title("Menu Principal")
    choice = st.radio("Navigation", ["🏠 Accueil", "📝 Faire le Sondage", "📊 Statistiques en Direct"])
    
    st.markdown("---")
    st.info(f"Développeur : **{st.session_state.get('user_name', 'FOUDA ENAMA MARIE FERNANDE')}**\n\nNiveau : Informatique L2")

# --- PAGE D'ACCUEIL ---
if choice == "🏠 Accueil":
    st.title("🇨🇲 LA VIE D'UN ÉTUDIANT DU 237")
    st.subheader("Bienvenue sur la plateforme officielle d'analyse de la vie étudiante.")
    st.write("""
    Cette application permet de collecter des données cruciales sur le quotidien des étudiants au Cameroun 
    afin d'élaborer des solutions de soutien adaptées.
    """)
    st.image("https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&q=80&w=1000", caption="Soutien à la réussite universitaire")

# --- PAGE DU SONDAGE (LES 15 QUESTIONS) ---
elif choice == "📝 Faire le Sondage":
    st.title("📝 Formulaire de Sondage")
    st.write("Veuillez remplir les 15 points suivants avec précision.")
    
    with st.form("survey_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            nom = st.text_input("1. Nom & Prénom")
            matricule = st.text_input("2. Matricule")
            niveau = st.selectbox("3. Niveau d'étude", ["L1", "L2", "L3", "Master 1", "Master 2", "Doctorat"])
            quartier = st.text_input("4. Quartier de résidence")
            situation = st.selectbox("5. Situation matrimoniale", ["Célibataire", "Marié(e)", "En relation"])
            logement = st.radio("6. Type de logement", ["Cité U", "Studio / Chambre", "Chez les parents/tuteurs"])
            transport = st.selectbox("7. Moyen de transport", ["Marche", "Taxi / Moto", "Véhicule personnel", "Bus"])
            budget = st.number_input("8. Budget mensuel estimé (FCFA)", min_value=0)

        with col2:
            repas = st.slider("9. Nombre de repas par jour", 1, 5, 2)
            stress = st.select_slider("10. Niveau de stress (1=Bas, 10=Élevé)", options=range(1, 11))
            sommeil = st.number_input("11. Heures de sommeil moyennes", 0, 24, 7)
            ordi = st.radio("12. Possédez-vous un ordinateur ?", ["Oui", "Non"])
            internet = st.select_slider("13. Qualité connexion internet", options=["Mauvaise", "Moyenne", "Bonne", "Excellente"])
            job = st.radio("14. Travaillez-vous en parallèle ?", ["Oui", "Non"])
            satisfaction = st.radio("15. Êtes-vous satisfait de vos études ?", ["Très satisfait", "Satisfait", "Peu satisfait", "Pas du tout"])

        submit = st.form_submit_button("Envoyer mes données")
        
        if submit:
            # Ici nous ajouterons plus tard le code pour envoyer vers Supabase
            st.success(f"Merci {nom} ! Vos données ont été préparées pour l'envoi.")
            st.balloons()

# --- PAGE DES STATISTIQUES ---
elif choice == "📊 Statistiques en Direct":
    st.title("📊 Analyse des Statistiques")
    st.write("Visualisation des données collectées auprès des étudiants.")
    
    # Simulation de données (En attendant la connexion à la base de données)
    data_demo = pd.DataFrame({
        'Niveau': ['L1', 'L2', 'L3', 'Master'],
        'Nombre': [45, 30, 25, 10],
        'Satisfaction': [70, 60, 50, 80]
    })
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("Répartition par Niveau")
        fig1 = px.bar(data_demo, x='Niveau', y='Nombre', color='Niveau', title="Nombre d'étudiants par niveau")
        st.plotly_chart(fig1, use_container_width=True)
        
    with c2:
        st.subheader("Taux de Satisfaction")
        fig2 = px.pie(data_demo, values='Satisfaction', names='Niveau', hole=0.4, title="Satisfaction par cycle")
        st.plotly_chart(fig2, use_container_width=True)

    st.warning("⚠️ Les données affichées ci-dessus sont des exemples. Une fois la base de données connectée, elles seront réelles.")
          
