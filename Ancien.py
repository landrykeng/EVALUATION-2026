import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import time
import supabase 
from supabase import create_client, Client


st.set_page_config(page_title="FORMULAIRE EVALUATION DES ENSEIGNANTS", page_icon="📊", layout="wide")

# Create a custom container with fancy styling for the title
head=st.columns([4,30,4])
with head[0]:
    st.image("Logo.png", width=150)
with head[1]: 
    st.markdown("""
    <div style='padding: 1.5rem; 
                margin: 2rem 0; 
                background: linear-gradient(135deg, #6e8efb, #4776E6);
                border-radius: 15px;
                box-shadow: 0 8px 16px rgba(0,0,0,0.2);
                animation: glow 2s ease-in-out infinite alternate;'>
        <h1 style='color: white; 
                   text-align: center; 
                   font-size: 2.5rem; 
                   font-weight: bold;
                   text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                   margin: 0;
                   letter-spacing: 2px;'>
            EVALUATION DES ENSEIGNENTS DE LA FORMATION CONTINUE
        </h1>
    </div>
    <style>
        @keyframes glow {
            from {
                box-shadow: 0 8px 16px rgba(0,0,0,0.2);
            }
            to {
                box-shadow: 0 8px 24px rgba(78,137,247,0.4);
            }
        }
    </style>
""", unsafe_allow_html=True)
with head[2]:
    st.image("Logo.png", width=150)

#st.title("EVALUATION DES ENSEIGNENTS DE LA FORMATION CONTINUE, SEMESTRE 1")


st.markdown("""
    <style>
        .stMarkdown {font-family: 'Helvetica', sans-serif;}
        .stButton button {
            background-color: #0066cc;
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            border: none;
            transition: background-color 0.3s;
        }
        .stButton button:hover {
            background-color: #0052a3;
        }
        .stRadio > label {
            color: #2c3e50;
            font-weight: 500;
        }
        .stExpander {
            background-color: #f8f9fa;
            border-radius: 10px;
            margin: 10px 0;
            border: 1px solid #dee2e6;
        }
        .stTextInput input {
            border-radius: 5px;
            border: 2px solid #e9ecef;
        }
        h1 {
            color: #1e3d59;
            text-align: center;
            padding: 20px 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        .stSidebar {
            background-color: #f1f3f5;
            padding: 20px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
        /* Card-like effect for expanders */
        .stExpander {
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }
        .stExpander:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 8px rgba(0,0,0,0.15);
        }
        
        /* Gradient background for header */
        h1 {
            background: linear-gradient(45deg, #1e3d59, #2c5282);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        /* Animated button hover effect */
        .stButton button {
            transition: all 0.3s ease;
        }
        .stButton button:hover {
            transform: scale(1.05);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        
        /* Radio button styling */
        .stRadio > div {
            background-color: #f8f9fa;
            padding: 10px;
            border-radius: 8px;
            transition: background-color 0.2s;
        }
        .stRadio > div:hover {
            background-color: #e9ecef;
        }
        
        /* Text input focus effect */
        .stTextInput input:focus {
            border-color: #0066cc;
            box-shadow: 0 0 0 2px rgba(0,102,204,0.2);
        }
        
        /* Sidebar hover effect */
        .stSidebar:hover {
            box-shadow: 2px 0 8px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <style>
    body {
        font-size: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


url="https://kduqsqcmcdsxmdjwxtfy.supabase.co"
cle="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtkdXFzcWNtY2RzeG1kand4dGZ5Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0ODI0OTAxOSwiZXhwIjoyMDYzODI1MDE5fQ.cQbybIOXREA67OsSr3h1bgdqzy3atk3CP7VYaMgVIXA"
supabase = create_client(url, cle)
#@st.cache_data
def load_data():
    try:
        # Délai initial pour permettre l'établissement de la connexion
        time.sleep(0.5)
        
        # Chargement des données étudiants avec délai
        with st.spinner("Chargement des données étudiants..."):
            #student_eval = supabase.table("etudiant").select("*").execute()
            student_eval=pd.read_excel("studenG.xlsx")
            time.sleep(0.3)  # Petit délai entre les requêtes
        
        # Chargement des données évaluations avec délai
        with st.spinner("Chargement des données évaluations..."):
            #data_eval = supabase.table("evaluation").select("*").execute()
            data_eval=pd.read_excel("evaluation.xlsx")
            time.sleep(0.2)
        
        # Conversion en DataFrame
        #student_eval = pd.DataFrame(student_eval.data)
        #data_eval = pd.DataFrame(data_eval.data)
        
        return student_eval, data_eval
        
    except Exception as e:
        st.error(f"Erreur de connexion: {e}")
        st.info("Veuillez vérifier votre connexion internet et vos identifiants Supabase")
        
        # Tentative de reconnexion après délai
        st.info("Tentative de reconnexion dans 2 secondes...")
        time.sleep(2)
        
        try:
            # Deuxième tentative
            with st.spinner("Nouvelle tentative de connexion..."):
                #student_eval = supabase.table("etudiant").select("*").execute()
                student_eval=pd.read_excel("studenG.xlsx")
                time.sleep(0.5)
                data_eval=pd.read_excel("evaluation.xlsx")
                
                #student_eval = pd.DataFrame(student_eval)
                #data_eval = pd.DataFrame(data_eval)
                
                st.success("Connexion rétablie avec succès!")
                return student_eval, data_eval
                
        except Exception as e2:
            st.error(f"Échec de la reconnexion: {e2}")
            return None, None

#======================================
student_eval, data_eval = load_data()
data_eval=data_eval[data_eval["Q_21"]!="Bien que je sois satisfait de l'enseignant, je pense qu'il y a des aspects à améliorer."]
liste_etudiant=pd.read_excel("Base.xlsx", sheet_name="Liste")
data=pd.read_excel('Base.xlsx',sheet_name="Classification")
#======================================

dico_etudiant=liste_etudiant.set_index('Matricule').T.to_dict('list')

nested_dict = {}
for _, row in data.iterrows():
    classe = row['Classe']
    cours = row['Cours']
    enseignant = row['Enseignant']
    
    if classe not in nested_dict:
        nested_dict[classe] = {}
    
    nested_dict[classe][enseignant] = cours



st.write("## Formulaire d'évaluation des enseignants")
# Sélection de la classe

classe_selectionnee = st.radio("Classe",[""] + list(nested_dict.keys()), index=0)
matricule = st.text_input("Matricule")
if  matricule!="":
    pre_nom=dico_etudiant[int(matricule)][0] if int(matricule) in dico_etudiant  else ""
else:
    pre_nom=""
nom_etudiant = st.text_input("Nom", value=pre_nom)
prenom_etudiant = st.text_input("Prénom")
sexe = st.radio("Sexe", ["", "Masculin", "Féminin"], index=0)
a=student_eval["Matricule"].tolist()
if matricule!= "" and a.count(int(matricule)) > 0:
    st.info(f"⚠️ Merci {pre_nom}, mais vous avez déjà fait votre évaluation pour ce semestre.")
    st.info("⚠️ Si ce n'est pas vous, rassurez-vous que votre matricule est correct.")
    st.stop()
elif matricule!= "" and int(matricule) not in dico_etudiant:
    st.info("⚠️ Votre matricule n'est pas valide. Veuillez vérifier sur la fiche de présence de votre classe.")
else:
    #enseignant_selectionne = st.selectbox("Sélectionnez un enseignant", list(nested_dict[classe_selectionnee].keys()))
    if classe_selectionnee!="" and nom_etudiant!="" and matricule !="" and sexe!="" :
        with st.form("Evaluation"):
            for enseignant, cours in nested_dict[classe_selectionnee].items():
                with st.expander(enseignant + ": " + cours, expanded=False):
                    st.write(f" Evaluation de M. **{enseignant}** pour le cours de {cours}")
                    Q_01=st.radio("GLOBALEMENT, ETES-VOUS SATISFAIT DE  ENSEIGNANT ?", ["","Très satisfait", "Satisfait", "Moyen", "Mauvais"],index=0, key=classe_selectionnee+enseignant+cours+"_01")
                    Q_02=st.radio("ENONCE DES OBJECTIFS DU COURS", ["","Très satisfait", "Satisfait", "Moyen", "Mauvais"],index=0,key=classe_selectionnee+enseignant+cours+"_02")
                    Q_03=st.radio("CONTENU DU COURS", ["","Très satisfait", "Satisfait", "Moyen", "Mauvais"],index=0,key=classe_selectionnee+enseignant+cours+"_03")
                    Q_04=st.radio("TAUX DE COUVERTURE DU PROGRAMME", ["","Très satisfait", "Satisfait", "Moyen", "Mauvais"],index=0,key=classe_selectionnee+enseignant+cours+"_04")
                    Q_05=st.radio("CONNAISSANCES THEORIQUES ACQUISES", ["","Très satisfait", "Satisfait", "Moyen", "Mauvais"],index=0,key=classe_selectionnee+enseignant+cours+"_05")
                    Q_06=st.radio("CONNAISSANCES PRATIQUES", ["","Très satisfait", "Satisfait", "Moyen", "Mauvais"],index=0,key=classe_selectionnee+enseignant+cours+"_06")
                    Q_07=st.radio("CONFORMITE DES EVALUATIONS AU CONTENU", ["","Très satisfait", "Satisfait", "Moyen", "Mauvais"],index=0,key=classe_selectionnee+enseignant+cours+"_07")
                    Q_08=st.radio("RAPPORT DUREE/CONTENU DE L'EPREUVE", ["","Très satisfait", "Satisfait", "Moyen", "Mauvais"],index=0,key=classe_selectionnee+enseignant+cours+"_08")
                    Q_09=st.radio("ASSIDUITE", ["","Très satisfait", "Satisfait", "Moyen", "Mauvais"],index=0,key=classe_selectionnee+enseignant+cours+"_09")
                    Q_10=st.radio("PONCTUALITE", ["","Très satisfait", "Satisfait", "Moyen", "Mauvais"],index=0,key=classe_selectionnee+enseignant+cours+"_10")
                    Q_11=st.radio("TENUE VESTIMENTAIRE", ["","Très satisfait", "Satisfait", "Moyen", "Mauvais"],index=0,key=classe_selectionnee+enseignant+cours+"_11")
                    Q_12=st.radio("UTILISATION DES OUTILS ET MATERIELS DIDACTIQUES", ["","Très satisfait", "Satisfait", "Moyen", "Mauvais"],index=0,key=classe_selectionnee+enseignant+cours+"_12")
                    Q_13=st.radio("DISPONIBILITE A ECOUTER LES ETUDIANTS", ["","Très satisfait", "Satisfait", "Moyen", "Mauvais"],index=0,key=classe_selectionnee+enseignant+cours+"_13")
                    Q_14=st.radio("MAITRISE DE LA SALLE DE COURS", ["","Très satisfait", "Satisfait", "Moyen", "Mauvais"],index=0,key=classe_selectionnee+enseignant+cours+"_14")
                    Q_15=st.radio("INTERACTION ENSEIGNANTS-ETUDIANTS (QUESTIONS-REPONSES)",["","Très satisfait", "Satisfait", "Moyen", "Mauvais"],index=0,key=classe_selectionnee+enseignant+cours+"_15")
                    Q_16=st.radio("INTEGRATION DES TICS DANS LES COURS (VIDEO PROJECTEUR, INTERNET OU COURS SAISIS)",["","Très satisfait", "Satisfait", "Moyen", "Mauvais"],index=0,key=classe_selectionnee+enseignant+cours+"_16")
                    Q_17=st.radio("ORGANISATION ET SUIVI DES TP, TPE ET TD",["","Très satisfait", "Satisfait", "Moyen", "Mauvais"],index=0,key=classe_selectionnee+enseignant+cours+"_17")
                    Q_18=st.radio("CAPACITE DE TRANSMISSION DU COURS",["","Très satisfait", "Satisfait", "Moyen", "Mauvais"],index=0,key=classe_selectionnee+enseignant+cours+"_18")
                    Q_19=st.text_area("COMMENTEZ LES ASPECTS POSITIFS", height=100,key=classe_selectionnee+enseignant+cours+"_19")
                    Q_20=st.text_area("COMMENTEZ LES ASPECTS NEGATIFS", height=100,key=classe_selectionnee+enseignant+cours+"_20")
                    Q_21=st.text_area("SUGGESTIONS", height=100,key=classe_selectionnee+enseignant+cours+"_21")
                    
            soumission=st.form_submit_button("Soumettre mon évaluation")
        
            question_dict={
            "Q_01":"GLOBALEMENT, ETES-VOUS SATISFAIT DE  ENSEIGNANT ?",
            "Q_02":"ENONCE DES OBJECTIFS DU COURS",
            "Q_03":"CONTENU DU COURS",
            "Q_04":"TAUX DE COUVERTURE DU PROGRAMME",
            "Q_05":"CONNAISSANCES THEORIQUES ACQUISES",
            "Q_06":"CONNAISSANCES PRATIQUES",
            "Q_07":"CONFORMITE DES EVALUATIONS AU CONTENU",
            "Q_08":"RAPPORT DUREE/CONTENU DE L'EPREUVE",
            "Q_09":"ASSIDUITE",
            "Q_10":"PONCTUALITE",
            "Q_11":"TENUE VESTIMENTAIRE",
            "Q_12":"UTILISATION DES OUTILS ET MATERIELS DIDACTIQUES",
            "Q_13":"DISPONIBILITE A ECOUTER LES ETUDIANTS",
            "Q_14":"MAITRISE DE LA SALLE DE COURS",
            "Q_15":"INTERACTION ENSEIGNANTS-ETUDIANTS (QUESTIONS-REPONSES)",
            "Q_16":"INTEGRATION DES TICS DANS LES COURS (VIDEO PROJECTEUR, INTERNET OU COURS SAISIS)",
            "Q_17":"ORGANISATION ET SUIVI DES TP, TPE ET TD",
            "Q_18":"CAPACITE DE TRANSMISSION DU COURS",
            "Q_19":"COMMENTEZ LES ASPECTS POSITIFS",
            "Q_20":"COMMENTEZ LES ASPECTS NEGATIFS",
            "Q_21":"SUGGESTIONS" }

            if soumission:
    
                etudiant_data = {
                    "Classe": classe_selectionnee,
                    "Nom": nom_etudiant,
                    "Prénom": prenom_etudiant,
                    "Sexe": sexe,
                    "Matricule": matricule
                }
                #etudiant_df = pd.DataFrame(etudiant_data)

                # Collecting evaluation data
                evaluation_data = []
                missing_responses = []
                
                if classe_selectionnee != "":
                    for enseignant, cours in nested_dict[classe_selectionnee].items():
                        responses = {
                            "Classe": classe_selectionnee,
                            "Sexe": sexe,
                            "Enseignant": enseignant,
                            "Cours": cours
                        }
                        for i in range(1, 22):
                            question_key = f"Q_{i:02d}"
                            response = st.session_state.get(classe_selectionnee + enseignant + cours + f"_{i:02d}", "")
                            responses[question_key] = response
                            if response == "":
                                missing_responses.append(
                                    f"⚠️Pour le cours de   {cours} dispensé par M. {enseignant}, vous n'avez pas donné de réponse à la question {question_dict[question_key]}."
                                )
                        evaluation_data.append(responses)

                #evaluation_df = pd.DataFrame(evaluation_data)



                if len(missing_responses)==0:
                    

                    # Insertion dans la table "evaluation"
                    rep2 = supabase.table("evaluation").insert(evaluation_data).execute()
                    
                    # Insertion dans la table "etudiant"
                    rep =supabase.table("etudiant").insert(etudiant_data).execute()
                    st.success(f"✅✅Merci {pre_nom}, votre évaluation a été soumise avec succès.")
                    
                    student_eval = supabase.table("etudiant").select("*").execute()
                    data_eval = supabase.table("evaluation").select("*").execute()
                    # Convert the results to DataFrames
                    student_eval = pd.DataFrame(student_eval.data)
                    data_eval = pd.DataFrame(data_eval.data)

                else:
                    st.error("❌❌ Evaluation non valide pour la(es) raison(s) suivante(s):")
                    for message in missing_responses:
                        st.info(message)
            
            
