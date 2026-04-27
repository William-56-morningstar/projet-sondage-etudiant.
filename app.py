import streamlit as st
import pandas as pd
import plotly.express as px
from supabase import create_client, Client

# --- CONNEXION SÉCURISÉE À SUPABASE ---
# On utilise st.secrets pour que tes clés ne soient pas visibles sur GitHub
try:
    url: str = st.secrets["SUPABASE_URL"]
    key: str = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
except Exception as e:
    st.error("Erreur de configuration des Secrets. Vérifie Streamlit Cloud.")

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="La Vie d'un Étudiant du 237", layout="wide", page_icon="🇨🇲")

# --- STYLE CSS (CORRIGÉ) ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        background-color: #007bff;
        color: white;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- MENU LATÉRAL ---
with st.sidebar:
    st.header("🇨🇲 Navigation")
    choice = st.radio("Aller vers :", ["🏠 Accueil", "📝 Faire le Sondage", "📊 Statistiques"])
    st.markdown("---")
    st.write("📌 **Projet Académique**")
    st.write(f"Étudiante : **FOUDA ENAMA MARIE FERNANDE**")
    st.write("Niveau : **Informatique L2**")

# --- PAGE D'ACCUEIL ---
if choice == "🏠 Accueil":
    st.title("🇨🇲 LA VIE D'UN ÉTUDIANT DU 237")
    st.subheader("Plateforme d'analyse de la vie estudiantine au Cameroun")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.write("""
        Bienvenue sur cette application conçue pour recueillir les données réelles sur le quotidien 
        des étudiants. Votre participation aide à mieux comprendre nos défis (transport, logement, budget).
        """)
    with col_b:
        st.info("💡 **Note :** Les données sont traitées de manière anonyme pour des fins statistiques.")

# --- PAGE DU SONDAGE (LES 15 QUESTIONS) ---
elif choice == "📝 Faire le Sondage":
    st.title("📝 Formulaire de Sondage")
    st.write("Répondez aux 15 questions ci-dessous :")
    
    with st.form("survey_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        
        with c1:
            nom = st.text_input("1. Nom & Prénom")
            matricule = st.text_input("2. Matricule")
            niveau = st.selectbox("3. Niveau d'étude", ["L1", "L2", "L3", "M1", "M2", "Doctorat"])
            quartier = st.text_input("4. Quartier de résidence")
            situation = st.selectbox("5. Situation matrimoniale", ["Célibataire", "En couple", "Marié(e)"])
            logement = st.selectbox("6. Type de logement", ["Cité U", "Studio/Chambre", "Parents/Tuteurs"])
            transport = st.selectbox("7. Moyen de transport principal", ["Marche", "Taxi/Moto", "Bus", "Véhicule personnel"])
            budget = st.number_input("8. Budget mensuel estimé (FCFA)", min_value=0, step=5000)

        with c2:
            repas = st.slider("9. Nombre de repas par jour", 1, 5, 2)
            stress = st.select_slider("10. Niveau de stress actuel", options=range(1, 11), value=5)
            sommeil = st.number_input("11. Heures de sommeil moyennes", 0, 24, 7)
            ordi = st.radio("12. Avez-vous un ordinateur ?", ["Oui", "Non"])
            internet = st.selectbox("13. Qualité de votre connexion", ["Mauvaise", "Moyenne", "Bonne", "Excellente"])
            job = st.radio("14. Travaillez-vous en parallèle ?", ["Oui", "Non"])
            satisfaction = st.select_slider("15. Satisfaction globale des études", options=["Pas du tout", "Peu", "Satisfait", "Très satisfait"])

        submit = st.form_submit_button("ENVOYER MES RÉPONSES")
        
        if submit:
            if nom == "" or matricule == "":
                st.warning("⚠️ Veuillez remplir au moins le nom et le matricule.")
            else:
                # Préparation des données pour Supabase
                data = {
                    "nom": nom, "matricule": matricule, "niveau": niveau, 
                    "quartier": quartier, "situation": situation, "logement": logement, 
                    "transport": transport, "budget": budget, "repas": repas, 
                    "stress": stress, "sommeil": sommeil, "ordi": ordi, 
                    "internet": internet, "job": job, "satisfaction": satisfaction
                }
                
                try:
                    supabase.table("sondages").insert(data).execute()
                    st.success("✅ Félicitations ! Tes données ont été envoyées à la base de données.")
                    st.balloons()
                except Exception as e:
                    st.error(f"❌ Erreur lors de l'envoi : {e}")

# --- PAGE DES STATISTIQUES ---
elif choice == "📊 Statistiques":
    st.title("📊 Analyse des résultats")
    
    try:
        # Récupération des données réelles
        response = supabase.table("sondages").select("*").execute()
        df = pd.DataFrame(response.data)
        
        if not df.empty:
            st.write(f"Nombre total de réponses : **{len(df)}**")
            
            col_chart1, col_chart2 = st.columns(2)
            with col_chart1:
                fig1 = px.histogram(df, x="niveau", title="Répartition par Niveau", color="niveau")
                st.plotly_chart(fig1, use_container_width=True)
            
            with col_chart2:
                fig2 = px.pie(df, names="satisfaction", title="Niveau de Satisfaction Global")
                st.plotly_chart(fig2, use_container_width=True)
                
            st.markdown("---")
            st.subheader("📋 Tableau récapitulatif")
            st.dataframe(df) # Le prof pourra voir toutes les données ici
        else:
            st.info("Aucune donnée enregistrée pour le moment. Allez dans 'Faire le Sondage'.")
    except Exception as e:
        st.error("La base de données n'est pas encore connectée ou la table 'sondages' est mal configurée.")
            
