import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import time
from datetime import datetime
import os
from Fonction import *


st.set_page_config(page_title="FORMULAIRE EVALUATION DES ENSEIGNANTS", page_icon="📊", layout="wide")

import_users_from_excel()  # Importer les utilisateurs depuis Excel au démarrage de l'application
# ==================== FONCTIONS POUR GÉRER LE FICHIER EXCEL ====================

def initialize_data_excel():
    """Initialise le fichier Data.xlsx avec les trois feuilles requises"""
    data_file = "Data.xlsx"
    
    if not os.path.exists(data_file):
        question_dict = {
            "Q_01": "GLOBALEMENT, ÊTES-VOUS SATISFAIT DE L'ENSEIGNANT ?",
            "Q_02": "ÉNONCÉ DES OBJECTIFS DU COURS",
            "Q_03": "CONTENU DU COURS",
            "Q_04": "TAUX DE COUVERTURE DU PROGRAMME",
            "Q_05": "CONNAISSANCES THÉORIQUES ACQUISES",
            "Q_06": "CONNAISSANCES PRATIQUES",
            "Q_07": "CONFORMITÉ DES ÉVALUATIONS AU CONTENU",
            "Q_08": "RAPPORT DURÉE/CONTENU DE L'ÉPREUVE",
            "Q_09": "ASSIDUITÉ",
            "Q_10": "PONCTUALITÉ",
            "Q_11": "TENUE VESTIMENTAIRE",
            "Q_12": "UTILISATION DES OUTILS ET MATÉRIELS DIDACTIQUES",
            "Q_13": "DISPONIBILITÉ À ÉCOUTER LES ÉTUDIANTS",
            "Q_14": "MAÎTRISE DE LA SALLE DE COURS",
            "Q_15": "INTERACTION ENSEIGNANTS-ÉTUDIANTS (QUESTIONS-RÉPONSES)",
            "Q_16": "INTÉGRATION DES TIC DANS LES COURS (VIDÉO PROJECTEUR, INTERNET OU COURS SAISIS)",
            "Q_17": "ORGANISATION ET SUIVI DES TP, TPE ET TD",
            "Q_18": "CAPACITÉ DE TRANSMISSION DU COURS",
            "Q_19": "COMMENTEZ LES ASPECTS POSITIFS",
            "Q_20": "COMMENTEZ LES ASPECTS NÉGATIFS",
            "Q_21": "SUGGESTIONS"
        }
        
        with pd.ExcelWriter(data_file, engine='openpyxl') as writer:
            # Feuille Evaluations
            evaluations_df = pd.DataFrame(columns=[
                'Classe', 'Date', 'Enseignant', 'Cours', 
                'Q_01', 'Q_02', 'Q_03', 'Q_04', 'Q_05', 'Q_06', 'Q_07', 'Q_08', 'Q_09', 'Q_10',
                'Q_11', 'Q_12', 'Q_13', 'Q_14', 'Q_15', 'Q_16', 'Q_17', 'Q_18',
                'Q_19', 'Q_20', 'Q_21'
            ])
            evaluations_df.to_excel(writer, sheet_name='Evaluations', index=False)
            
            # Feuille Student
            student_df = pd.DataFrame(columns=[
                'Classe', 'Nom', 'Prénom', 'Sexe', 'Matricule', 'Date', 'Enseignant'
            ])
            student_df.to_excel(writer, sheet_name='Student', index=False)
            
            # Feuille Labels
            labels_df = pd.DataFrame(list(question_dict.items()), columns=['Code', 'Question'])
            labels_df.to_excel(writer, sheet_name='Labels', index=False)

def load_excel_data():
    """Charge les données du fichier Excel"""
    initialize_data_excel()
    
    try:
        student_eval = pd.read_excel("Data.xlsx", sheet_name="Student")
        data_eval = pd.read_excel("Data.xlsx", sheet_name="Evaluations")
        return student_eval, data_eval
    except Exception as e:
        st.error(f"Erreur de lecture du fichier Excel: {e}")
        return pd.DataFrame(), pd.DataFrame()

def save_evaluation_to_excel(evaluation_data, student_data):
    """Sauvegarde l'évaluation et les données étudiant dans le fichier Excel et Supabase"""
    try:
        # Lire les données existantes
        student_eval = pd.read_excel("Data.xlsx", sheet_name="Student")
        evaluations = pd.read_excel("Data.xlsx", sheet_name="Evaluations")
        
        # Ajouter les nouvelles données
        student_eval = pd.concat([student_eval, pd.DataFrame([student_data])], ignore_index=True)
        evaluations = pd.concat([evaluations, pd.DataFrame([evaluation_data])], ignore_index=True)
        
        # Écrire les données mises à jour
        with pd.ExcelWriter("Data.xlsx", engine='openpyxl', mode='w') as writer:
            evaluations.to_excel(writer, sheet_name='Evaluations', index=False)
            student_eval.to_excel(writer, sheet_name='Student', index=False)
            
            # Réécrire la feuille Labels
            question_dict = {
                "Q_01": "GLOBALEMENT, ÊTES-VOUS SATISFAIT DE L'ENSEIGNANT ?",
                "Q_02": "ÉNONCÉ DES OBJECTIFS DU COURS",
                "Q_03": "CONTENU DU COURS",
                "Q_04": "TAUX DE COUVERTURE DU PROGRAMME",
                "Q_05": "CONNAISSANCES THÉORIQUES ACQUISES",
                "Q_06": "CONNAISSANCES PRATIQUES",
                "Q_07": "CONFORMITÉ DES ÉVALUATIONS AU CONTENU",
                "Q_08": "RAPPORT DURÉE/CONTENU DE L'ÉPREUVE",
                "Q_09": "ASSIDUITÉ",
                "Q_10": "PONCTUALITÉ",
                "Q_11": "TENUE VESTIMENTAIRE",
                "Q_12": "UTILISATION DES OUTILS ET MATÉRIELS DIDACTIQUES",
                "Q_13": "DISPONIBILITÉ À ÉCOUTER LES ÉTUDIANTS",
                "Q_14": "MAÎTRISE DE LA SALLE DE COURS",
                "Q_15": "INTERACTION ENSEIGNANTS-ÉTUDIANTS (QUESTIONS-RÉPONSES)",
                "Q_16": "INTÉGRATION DES TIC DANS LES COURS (VIDÉO PROJECTEUR, INTERNET OU COURS SAISIS)",
                "Q_17": "ORGANISATION ET SUIVI DES TP, TPE ET TD",
                "Q_18": "CAPACITÉ DE TRANSMISSION DU COURS",
                "Q_19": "COMMENTEZ LES ASPECTS POSITIFS",
                "Q_20": "COMMENTEZ LES ASPECTS NÉGATIFS",
                "Q_21": "SUGGESTIONS"
            }
            labels_df = pd.DataFrame(list(question_dict.items()), columns=['Code', 'Question'])
            labels_df.to_excel(writer, sheet_name='Labels', index=False)
        
        # Sauvegarder dans Supabase
        # Insérer l'étudiant
        nom_complet = f"{student_data['Nom']}"
        insert_student_to_supabase(student_data['Classe'], nom_complet, student_data['Sexe'], student_data['Matricule'],student_data['enseignant'],student_data['cours'])
        
        # Insérer l'évaluation
        insert_evaluation_to_supabase(evaluation_data, student_data['Matricule'])
        
        return True
    except Exception as e:
        st.error(f"Erreur lors de la sauvegarde: {e}")
        return False

# CSS personnalisé pour un design moderne et professionnel
st.markdown("""
    <style>
    /* Importation de Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    /* Reset et styles de base */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    
    /* Masquer les éléments par défaut */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* En-tête vert style INS */
    .top-header {
        background: linear-gradient(90deg, #1e3a5f 0%, #2c5282 100%); 
        padding: 1rem 2rem; 
        border-bottom: 4px solid #f39c12;
        margin-bottom: 2rem;'
  
        padding: 0.8rem 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: -5rem -5rem 0 -5rem;
        margin-bottom: 0;
    }
    
    .header-left {
        display: flex;
        align-items: center;
        gap: 2rem;
        font-size: 0.95rem;
    }
 
    </style>
""", unsafe_allow_html=True)

# En-tête supérieur vert
st.markdown("""
    <div class="top-header";>
        <div style='display: flex; align-items: center; justify-content: space-between;'>
            <h1 style='margin: 0; font-size: 1.2rem; font-weight: 500;'>
                    EVALUATION DES ENSEIGNANTS DE LA FORMATION INITIALE
            </h1>
        </div>
    </div>
""", unsafe_allow_html=True)


with st.sidebar:
    st.markdown("###  :material/person: Concepteurs")
    st.write("- **Landry KENGNE**, *ISE 3*")
    st.write("- **Marc ABENA**, *ISE L3*")
    st.write("- **Kintin EBALA**, *ISE L2*")
    
    st.info(" *Pour tout problème, veuillez contacter Marc ABENA de ISE L3.*")

titre=st.columns([1, 6])
with titre[0]:
    st.image("Logo.png", width=150)
with titre[1]:
    pass

# Initialize Excel file and load data
initialize_data_excel()
student_eval, data_eval = load_excel_data()
liste_etudiant = pd.read_excel("Base.xlsx", sheet_name="Liste")
data = pd.read_excel('Base.xlsx', sheet_name="Classification")

dico_etudiant = liste_etudiant.set_index('Matricule').T.to_dict('list')
# Create nested dictionary for classes, teachers, and courses
nested_dict = {}
for _, row in data.iterrows():
    classe = row['Classe']
    cours = row['Cours']
    enseignant = row['Enseignant']
    
    if classe not in nested_dict:
        nested_dict[classe] = {}
    
    nested_dict[classe][enseignant] = cours


# Initialize session state for tracking evaluations
if 'evaluated_teachers' not in st.session_state:
    st.session_state.evaluated_teachers = []
if 'current_teacher_index' not in st.session_state:
    st.session_state.current_teacher_index = 0
if 'student_authenticated' not in st.session_state:
    st.session_state.student_authenticated = False
if 'authenticated_student' not in st.session_state:
    st.session_state.authenticated_student = {'nom': '', 'matricule': '', 'prenom': '', 'classe': '', 'sexe': ''}

st.write("## :material/edit_document: Formulaire d'évaluation des enseignants")

# ==================== AUTHENTIFICATION ÉTUDIANT ====================
if not st.session_state.student_authenticated:
    st.markdown("### :material/key: Authentification")
    st.info("Veuillez entrer vos informations pour accéder au formulaire d'évaluation")
    
    col1, col2 = st.columns(2)
    with col1:
        auth_matricule = st.text_input("Votre Matricule", placeholder="Entrez votre matricule")
    with col2:
        pass
    
    if st.button("Accéder au formulaire", use_container_width=True, icon=":material/key:"):
        if auth_matricule == "":
            st.error("⚠️ Veuillez entrer votre matricule")
        else:
            try:
                matricule_int = auth_matricule
                if matricule_int not in dico_etudiant or int(matricule_int) not in dico_etudiant:
                    st.error("⚠️ Votre matricule n'est pas valide. Veuillez vérifier sur la fiche de présence de votre classe.")
                else:
                    # Vérifier si l'étudiant a déjà complété ses évaluations
                    #if not student_eval.empty and matricule_int in student_eval["Matricule"].values:
                        #st.warning(f"⚠️ Vous avez déjà complété vos évaluations. Si ce n'est pas vous, rassurez-vous que votre matricule est correct.")
                    #else:
                    st.session_state.student_authenticated = True
                    st.session_state.authenticated_student = {
                            'nom': dico_etudiant[matricule_int][0] if matricule_int in dico_etudiant else '',
                            'matricule': matricule_int,
                            'prenom': dico_etudiant[matricule_int][0] if matricule_int in dico_etudiant else '',
                            'classe': '',
                            'sexe': ''
                        }
                    st.rerun()
            except ValueError:
                st.error("⚠️ Le matricule doit être un nombre")
    
    st.stop()

# ==================== FORMULAIRE D'ÉVALUATION ====================
students_df = load_students_from_supabase()
students_df=students_df[['matricule', 'nom', 'classe', 'sexe','enseignant', 'cours']]
user_df = students_df[students_df['matricule'] == str(st.session_state.authenticated_student['matricule'])]
st.session_state.evaluated_teachers = user_df["enseignant"].unique().tolist()
st.write("### Informations de l'étudiant")
col1, col2 = st.columns(2)

with col1:
    c="#083eee"
    st.markdown(f"### **Matricule:** <span style='color: #083eee;'>{st.session_state.authenticated_student['matricule']}</span>", unsafe_allow_html=True)
    nom_etudiant = st.text_input("Nom", value=st.session_state.authenticated_student['nom'])
    
with col2:
    classe_selectionnee = st.selectbox("Classe", [dico_etudiant[st.session_state.authenticated_student['matricule']][1]] + list(nested_dict.keys()), index=0)

sexe = st.radio("Sexe", ["", "Masculin", "Féminin"], index=0, horizontal=True)

matricule = st.session_state.authenticated_student['matricule']
pre_nom = st.session_state.authenticated_student['prenom']


# Main evaluation section
if classe_selectionnee != "" and nom_etudiant != "" and matricule != "" and sexe != "":
    
    # Get list of teachers for selected class
    teachers_list = data[data['Classe'] == classe_selectionnee][['Enseignant', 'Cours']].values.tolist()
    total_teachers = len(teachers_list)
    
    
    # Progress section
    st.write("---")
    st.write("### :material/trending_up: Progression de vos évaluations")
    
    
    # Calculate evaluated and remaining teachers
    evaluated_count = user_df.shape[0]
    remaining_count = total_teachers - evaluated_count
    
    # Progress bar
    progress = evaluated_count / total_teachers if total_teachers > 0 else 0
    st.progress(progress)
    st.write(f"**{evaluated_count}/{total_teachers}** enseignants évalués ({progress*100:.0f}%)")
    
    
    # Display tables in two columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("#### ✅ Enseignants déjà évalués")
        if st.session_state.evaluated_teachers:
            evaluated_df = pd.DataFrame([
                {"Enseignant": ens, "Cours": nested_dict[classe_selectionnee][ens]}
                for ens in user_df["enseignant"].unique() if ens in user_df["enseignant"].unique()
            ])
            st.dataframe(evaluated_df, hide_index=True, use_container_width=True)
        else:
            st.info("Aucun enseignant évalué pour le moment")
    
    with col2:
        st.write("#### :material/hourglass_top: Enseignants restants à évaluer")
        remaining_teachers = [
            (ens, cours) for ens, cours in teachers_list 
            if ens not in user_df["enseignant"].unique()
        ]
        if remaining_teachers:
            remaining_df = pd.DataFrame([
                {"Enseignant": ens, "Cours": cours}
                for ens, cours in remaining_teachers
            ])
            st.dataframe(remaining_df, hide_index=True, use_container_width=True)
        else:
            st.success("🎉 Tous les enseignants ont été évalués!")
    
    st.write("---")
    
    # Select teacher to evaluate
    if remaining_teachers:
        st.write("### :material/check_circle: Sélectionnez un enseignant à évaluer")
        
        teacher_options = [f"{ens} - {cours}" for ens, cours in remaining_teachers]
        selected_teacher_full = st.selectbox("Enseignant", teacher_options)
        
        # Extract teacher name and course
        enseignant_selectionne = selected_teacher_full.split(" - ")[0]
        cours_selectionne = nested_dict[classe_selectionnee][enseignant_selectionne]
        
        st.write("---")
        st.write(f"### Évaluation de <span style='color: #0066cc;'>**{enseignant_selectionne}**</span> pour le cours de <span style='color: #f39c12;'>*{cours_selectionne}*</span>", unsafe_allow_html=True)
        #st.write(f"### :material/book: Évaluation de **{enseignant_selectionne}** pour le cours de **{cours_selectionne}**")
        
        # Evaluation form for single teacher
        with st.form("Evaluation_Form"):
            
            question_dict = {
                "Q_01": "GLOBALEMENT, ÊTES-VOUS SATISFAIT DE L'ENSEIGNANT ?",
                "Q_02": "ÉNONCÉ DES OBJECTIFS DU COURS",
                "Q_03": "CONTENU DU COURS",
                "Q_04": "TAUX DE COUVERTURE DU PROGRAMME",
                "Q_05": "CONNAISSANCES THÉORIQUES ACQUISES",
                "Q_06": "CONNAISSANCES PRATIQUES",
                "Q_07": "CONFORMITÉ DES ÉVALUATIONS AU CONTENU",
                "Q_08": "RAPPORT DURÉE/CONTENU DE L'ÉPREUVE",
                "Q_09": "ASSIDUITÉ",
                "Q_10": "PONCTUALITÉ",
                "Q_11": "TENUE VESTIMENTAIRE",
                "Q_12": "UTILISATION DES OUTILS ET MATÉRIELS DIDACTIQUES",
                "Q_13": "DISPONIBILITÉ À ÉCOUTER LES ÉTUDIANTS",
                "Q_14": "MAÎTRISE DE LA SALLE DE COURS",
                "Q_15": "INTERACTION ENSEIGNANTS-ÉTUDIANTS (QUESTIONS-RÉPONSES)",
                "Q_16": "INTÉGRATION DES TIC DANS LES COURS (VIDÉO PROJECTEUR, INTERNET OU COURS SAISIS)",
                "Q_17": "ORGANISATION ET SUIVI DES TP, TPE ET TD",
                "Q_18": "CAPACITÉ DE TRANSMISSION DU COURS",
                "Q_19": "COMMENTEZ LES ASPECTS POSITIFS",
                "Q_20": "COMMENTEZ LES ASPECTS NÉGATIFS",
                "Q_21": "SUGGESTIONS"
            }
            
            responses = {}
            
            # Questions 1-18: Radio buttons
            for i in range(1, 19):
                question_key = f"Q_{i:02d}"
                responses[question_key] = st.radio(
                    question_dict[question_key],
                    ["", "Très satisfait", "Satisfait", "Moyen", "Mauvais"],
                    index=0,
                    key=f"{enseignant_selectionne}_{question_key}"
                )
            
            # Questions 19-21: Text areas
            responses["Q_19"] = st.text_area(
                question_dict["Q_19"],
                height=100,
                key=f"{enseignant_selectionne}_Q_19"
            )
            responses["Q_20"] = st.text_area(
                question_dict["Q_20"],
                height=100,
                key=f"{enseignant_selectionne}_Q_20"
            )
            responses["Q_21"] = st.text_area(
                question_dict["Q_21"],
                height=100,
                key=f"{enseignant_selectionne}_Q_21"
            )
            
            # Submit button
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                submitted = st.form_submit_button(" Soumettre cette évaluation", use_container_width=True, icon=":material/send:")
            
            if submitted:
                # Check for missing responses
                missing_responses = []
                for i in range(1, 19):
                    question_key = f"Q_{i:02d}"
                    if responses[question_key] == "":
                        missing_responses.append(
                            f"⚠️ Vous n'avez pas donné de réponse à la question: {question_dict[question_key]}"
                        )
                
                if len(missing_responses) == 0:
                    # Prepare evaluation data
                    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    evaluation_data = {
                        "Classe": classe_selectionnee,
                        "Date": current_date,
                        "Enseignant": enseignant_selectionne,
                        "Cours": cours_selectionne,
                        "Q_01": responses["Q_01"],
                        "Q_02": responses["Q_02"],
                        "Q_03": responses["Q_03"],
                        "Q_04": responses["Q_04"],
                        "Q_05": responses["Q_05"],
                        "Q_06": responses["Q_06"],
                        "Q_07": responses["Q_07"],
                        "Q_08": responses["Q_08"],
                        "Q_09": responses["Q_09"],
                        "Q_10": responses["Q_10"],
                        "Q_11": responses["Q_11"],
                        "Q_12": responses["Q_12"],
                        "Q_13": responses["Q_13"],
                        "Q_14": responses["Q_14"],
                        "Q_15": responses["Q_15"],
                        "Q_16": responses["Q_16"],
                        "Q_17": responses["Q_17"],
                        "Q_18": responses["Q_18"],
                        "Q_19": responses["Q_19"],
                        "Q_20": responses["Q_20"],
                        "Q_21": responses["Q_21"]
                    }
                    
                    student_data = {
                        "Classe": classe_selectionnee,
                        "Nom": nom_etudiant,
                        "Prénom": pre_nom,
                        "Sexe": sexe,
                        "Matricule": matricule,
                        "Date": current_date,
                        "enseignant": enseignant_selectionne,
                        "cours": cours_selectionne
                    }
                    
                    # Save to Excel
                    if save_evaluation_to_excel(evaluation_data, student_data):
                        # Add teacher to evaluated list
                        st.session_state.evaluated_teachers.append(enseignant_selectionne)
                        
                        st.success(f"✅ Évaluation de **{enseignant_selectionne}** soumise avec succès!")
                        
                        # Check if all teachers evaluated
                        if len(st.session_state.evaluated_teachers) == total_teachers:
                            st.balloons()
                            st.success(f"🎉 Félicitations {pre_nom}! Vous avez terminé toutes vos évaluations!")
                            st.info("Vous pouvez maintenant fermer cette fenêtre.")
                            
                            # Reset session state
                            st.session_state.student_authenticated = False
                            st.session_state.evaluated_teachers = []
                            if st.button("Poursuivre", use_container_width=True, icon=":material/refresh:"):
                                st.form_submit_button("Poursuivre", use_container_width=True, icon=":material/refresh:")
                                st.rerun()
                        else:
                            st.info(f"Il vous reste {total_teachers - len(st.session_state.evaluated_teachers)} enseignant(s) à évaluer.")
                            if st.form_submit_button("Poursuivre", use_container_width=True, icon=":material/refresh:"):
                                st.rerun()
                    else:
                        st.error("❌ Erreur lors de la sauvegarde des données")
                else:
                    st.error("❌ Évaluation incomplète:")
                    for message in missing_responses:
                        st.warning(message)
    
    else:
        st.success("🎉 Vous avez évalué tous vos enseignants!")
        st.info("Veuillez recharger la page pour commencer une nouvelle session.")
