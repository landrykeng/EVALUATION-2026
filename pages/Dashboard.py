import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from my_fonction import *
from Fonction import *
from streamlit_echarts import st_echarts
import io
from datetime import datetime, timedelta
import os
import google.generativeai as genai

# ==================== CHARGEMENT DES DONNÉES DEPUIS EXCEL ====================



def load_data_from_excel():
    """Charge les données depuis Supabase"""
    try:
        students_df = load_students_from_supabase()
        evaluations_df = load_evaluations_from_supabase()
        
        # Fusionner pour créer student_eval similaire à Excel Student sheet
        # evaluations_df a matricule, classe, date, enseignant
        # students_df a matricule, classe, nom, sexe
        # Supposons nom est "Nom Prénom"
        
        
        students_df[['Nom', 'Prénom']] = students_df['nom'].str.split(' ', n=1, expand=True)
        students_df = students_df.rename(columns={'nom': 'Nom_complet'})
        
        student_eval = students_df
        
        
        data_eval = evaluations_df.rename(columns={
            'matricule': 'Matricule',
            'classe': 'Classe',
            'date': 'Date',
            'enseignant': 'Enseignant',
            'cours': 'Cours'
        })
        
        return student_eval, data_eval
    except Exception as e:
        st.error(f"Erreur lors du chargement des données: {e}")
        return pd.DataFrame(), pd.DataFrame()

# Charger les données
student_eval, data_eval = load_data_from_excel()

# ==================== STYLES CSS ====================

st.markdown("""
    <style>

        /* Masquer les éléments par défaut */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        .stTabs [data-baseweb="tab-list"] {
            gap: 20px;
            background-color: #f8f9fa;
            border-radius: 15px;
            padding: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .stTabs [data-baseweb="tab"] {
            background-color: transparent;
            border-radius: 10px;
            padding: 10px 20px;
            color: #495057;
            font-weight: 600;
        }
        .stTabs [aria-selected="true"] {
            background-color: #0066cc !important;
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)

if not authentication_system():
    st.stop()

# Vérifier si les données sont disponibles
if data_eval.empty or student_eval.empty:
    st.warning("⚠️ Aucune donnée d'évaluation n'a été trouvée.")
    st.info("Les données seront chargées automatiquement une fois que les étudiants complètent leurs évaluations.")
    st.stop()

API_KEY=st.secrets["API_IA"]
# Configuration des questions et couleurs
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

reversed_question_dict = {value: key for key, value in question_dict.items()}
colors_palette = ["#81DBF7", "#0FAADB", "#0B7A9D", "#06465A", "#4CF2BF", "#0EC48C","#09855F","#064E38","#F77DF1","#F127E7","#9E0A97","#660661"]
colors_palette2 = ["#FC1414", "#F61AEC", "#7F09E1", "#074BE3", "#05B0E5", "#06E49F","#08E212","#BEE208","#E47A06","#E13709","#9E0A97","#660661"]

# ==================== EN-TÊTE ====================

head = st.columns([4, 30, 4])
with head[0]:
    st.image("Logo.png", width=150)
with head[1]:
    st.title("Tableau de bord - Évaluations des enseignants")
with head[2]:
    st.image("Logo.png", width=150)

# ==================== VUE D'ENSEMBLE ====================

st.markdown("## :material/trending_up: Vue d'ensemble")

try:
    etudiant = pd.read_excel("Base.xlsx", sheet_name="Liste")
    df_classes = pd.read_excel('Base.xlsx', sheet_name="Classification")
    
    #tableau contenant le maritcule, le nom, classe,nombre de matière de sa classe
    matieres_par_classe = df_classes.groupby("Classe")["Cours"].nunique()
    matieres_dict = matieres_par_classe.to_dict()
    df_all=etudiant
    df_all["Nombre de matières"] = df_all["Classe"].map(matieres_dict)
    
    df_all["Matricule"] = df_all["Matricule"].astype(str)
    # dictionnaire du nombre de matière évalué par étudiant
    eval_counts = student_eval.groupby("matricule").size().to_dict()
    df_all["Nombre de matières évaluées"] = df_all["Matricule"].map(eval_counts).fillna(0).astype(int)
    df_all["Progression"] = df_all.apply(lambda row: 100*row["Nombre de matières évaluées"] / row["Nombre de matières"] if row["Nombre de matières"] > 0 else 0, axis=1)
    global_progress = df_all["Nombre de matières évaluées"].sum() / df_all["Nombre de matières"].sum() if df_all["Nombre de matières"].sum() > 0 else 0
    
    progrss = st.columns(2)
    with progrss[0]:
        make_progress_char(global_progress, couleur="#BB4415", titre=f"Progression globale")
    
    with progrss[1]:
        #Tableau de la progression par classe
        class_progress = df_all.groupby("Classe").agg({"Nombre de matières": "sum", "Nombre de matières évaluées": "sum"})
        class_progress["Classe"] = class_progress.index
        class_progress = class_progress.reset_index(drop=True)
        class_progress=class_progress.rename(columns={"Nombre de matières": "Total evaluation", "Nombre de matières évaluées": "Total évaluées"})
        
        #class_progress=class_progress.sort_values(by="Total évaluées", ascending=False)
        
        class_progress["Progression"] = class_progress["Total évaluées"] / class_progress["Total evaluation"]
        class_progress=class_progress[["Classe", "Total evaluation", "Total évaluées", "Progression"]]
        
        colors_palette_class = [f"rgb({int(0)}, {int(1 + i*10)}, {int(255)})" for i in range(len(class_progress))]
        
        make_multi_progress_bar(labels=class_progress["Classe"], values=class_progress["Progression"], 
                               titre="Progression par classe", colors=colors_palette_class, height=400)
        
    # tableau croisé de toutes les reponses par modalité
    cross_all = pd.DataFrame()
    for q in [f"Q_{i:02d}" for i in range(1, 19)]:
        if q in data_eval.columns:
            responses = data_eval[q].value_counts()
            for rep in ["Très satisfait", "Satisfait", "Moyen", "Mauvais"]:
                if rep not in responses.index:
                    responses[rep] = 0
            cross_all[q] = responses.loc[["Très satisfait", "Satisfait", "Moyen", "Mauvais"]]   
            
    for col in cross_all.columns:
        cross_all[col] = round(100 * cross_all[col] / cross_all[col].sum(), 2)
    cross_all = cross_all.T
    cl=st.columns(2)
    with cl[0]:
        make_st_heatmap_echat2(cross_all, cle="heatmap_overview2", title="Distribution globale (%) des réponses par question")
        labels_df = pd.DataFrame(list(question_dict.items()), columns=['Code', 'Question'])
        with st.expander("Labels des questions"):
            st.dataframe(labels_df, use_container_width=True, hide_index=True)
    with cl[1]:
        # calcul du nombre de matière par classe
        matieres_par_classe = df_classes.groupby("Classe")["Cours"].nunique()
        matieres_dict = matieres_par_classe.to_dict()
        
        #Afficher le tableau avec la barre de progression dans la colonne "Progression"
        st.subheader("Progression individuelle des étudiants dans l'évaluation de leurs matières")
        
        choosed_class = st.selectbox("Sélectionner une classe pour voir la progression individuelle", ["Toutes"] + df_all["Classe"].unique().tolist(), key="class_progress_select")
        df_all_ = df_all if choosed_class == "Toutes" else df_all[df_all["Classe"] == choosed_class]
        
        df_all_ = df_all_[["Matricule", "Nom", "Classe", "Progression"]]
        df_all_["Progression"] = df_all_["Progression"] / 100
        st.dataframe(df_all_, use_container_width=True, hide_index=True,
                     column_config={
                         "Progression": st.column_config.ProgressColumn("Progression", 
                                                                        help="Progression de l'étudiant dans l'évaluation de ses matières", 
                                                                        min_value=0.0, 
                                                                        max_value=1.0)
                     }  )
        
   
except Exception as e:
    st.warning(f"Erreur lors du calcul de la progression: {e}")



# ==================== ANALYSES DÉTAILLÉES ====================

st.markdown("---")
st.markdown("## 📈 Analyses par aspect")

ligne1 = st.columns(2)

with ligne1[0]:
    selected_classe = st.selectbox("Sélectionner une classe", data_eval["Classe"].unique(), key="class_overview_select0")
    class_data = data_eval[data_eval["Classe"] == selected_classe]
    if not class_data.empty:
        cross_class = pd.DataFrame()
        for q in [f"Q_{i:02d}" for i in range(1, 19)]:
            if q in class_data.columns:
                responses = class_data[q].value_counts()
                for rep in ["Très satisfait", "Satisfait", "Moyen", "Mauvais"]:
                    if rep not in responses.index:
                        responses[rep] = 0
                cross_class[q] = responses.loc[["Très satisfait", "Satisfait", "Moyen", "Mauvais"]]
        
        for col in cross_class.columns:
            cross_class[col] = round(100 * cross_class[col] / cross_class[col].sum(), 2)
        cross_class = cross_class.T
        make_st_heatmap_echat2(cross_class, cle="heatmap_overview0", title=f"Distribution des réponses (%) pour la classe {selected_classe}")


# Colonne 1: Par aspect
with ligne1[1]:
    
    try:
        selected_question = st.selectbox("Sélectionner un aspect", list(reversed_question_dict.keys()), key="aspect_select")
        question_code = reversed_question_dict[selected_question]
        
        if question_code not in ["Q_19", "Q_20", "Q_21"] and question_code in data_eval.columns:
            dict_quest = {}
            for classe in data_eval["Classe"].unique():
                data_classe = data_eval[data_eval["Classe"] == classe][[question_code]]
                response_counts = data_classe[question_code].value_counts()
                for rep in ["Très satisfait", "Satisfait", "Moyen", "Mauvais"]:
                    if rep not in response_counts.index:
                        response_counts[rep] = 0
                dict_quest[classe] = response_counts.loc[["Très satisfait", "Satisfait", "Moyen", "Mauvais"]].to_dict()
            cross_df = pd.DataFrame(dict_quest)
            for col in cross_df.columns:
                cross_df[col] = round(100 * cross_df[col] / cross_df[col].sum(), 2)
            cross_df=cross_df.T
            make_cross_echart(cross_df, x_label_rotation=0, cle="aspect_chart")
        else:
            st.info("Cet aspect n'a pas de données de réponses")
    except Exception as e:
        st.warning(f"Erreur: {e}")
    with st.expander("Labels des questions"):
        labels_df = pd.DataFrame(list(question_dict.items()), columns=['Code', 'Question'])
        st.dataframe(labels_df, use_container_width=True, hide_index=True)


st.markdown("---")
st.markdown("### 👨‍🏫 Analyse par enseignant")
classes_enseignant = st.selectbox("Sélectionner une classe pour filtrer les enseignants", data_eval["Classe"].unique(), key="teacher_class_filter_overview")
df_for_teachers = data_eval[data_eval["Classe"] == classes_enseignant] if not data_eval.empty else pd.DataFrame()
# tableau des score de tous les enseignants de la classe sélectionnée par question
if not df_for_teachers.empty:
    teacher_scores = {}
    for enseignant in df_for_teachers["Enseignant"].unique():
        data_teacher = df_for_teachers[df_for_teachers["Enseignant"] == enseignant]
        teacher_scores[enseignant] = {}
        for q in [f"Q_{i:02d}" for i in range(1, 19)]:
            if q in data_teacher.columns:
                responses = data_teacher[q].value_counts()
                for rep in ["Très satisfait", "Satisfait", "Moyen", "Mauvais"]:
                    if rep not in responses.index:
                        responses[rep] = 0
                teacher_scores[enseignant][q] = responses.loc[["Très satisfait", "Satisfait", "Moyen", "Mauvais"]].to_dict()

#teacher_scores

ligne2 = st.columns(2)
# Colonne 2: Par enseignant
with ligne2[0]:
    try:
        if "Enseignant" in data_eval.columns and len(data_eval["Enseignant"].unique()) > 0:
            teacher = st.selectbox("Sélectionner un enseignant", data_eval["Enseignant"].unique(), key="teacher_select")
            data_teacher = data_eval[data_eval["Enseignant"] == teacher]
            teacher_classes = data_teacher["Classe"].unique()
            
            if not data_teacher.empty:
                dict_teacher = {}
                for classe in data_teacher["Classe"].unique():
                    data_teach=data_teacher[data_teacher["Classe"]==classe]
                    responses = []
                    for q in [f"Q_{i:02d}" for i in range(1, 19)]:
                        if q in data_teach.columns:
                            responses.extend(data_teach[q].tolist())
                    
                    counter = pd.Series(responses).value_counts()
                    for rep in ["Très satisfait", "Satisfait", "Moyen", "Mauvais"]:
                        if rep not in counter.index:
                            counter[rep] = 0
                    dict_teacher[classe] = counter.loc[["Très satisfait", "Satisfait", "Moyen", "Mauvais"]].to_dict()
                
                if len(dict_teacher) == 1:
                    df_to_plot = dict_teacher[list(dict_teacher.keys())[0]]
                    make_donut_chart(dict_teacher[list(dict_teacher.keys())[0]], cle="teacher_donut")
                else:
                    cross_df = pd.DataFrame(dict_teacher)
                    for col in cross_df.columns:
                        cross_df[col] = round(100 * cross_df[col] / cross_df[col].sum(), 2)
                    cross_df=cross_df.T
                    make_cross_echart(cross_df, x_label_rotation=40, cle="teacher_chart")
                
                genai.configure(api_key=API_KEY)
                model = genai.GenerativeModel("gemini-3-flash-preview")
                
                positive_comments= data_teacher["Q_19"].dropna().tolist() if "Q_19" in data_teacher.columns else []
                negative_comments= data_teacher["Q_20"].dropna().tolist() if "Q_20" in data_teacher.columns else []
                suggestions= data_teacher["Q_21"].dropna().tolist() if "Q_21" in data_teacher.columns else []
                
                promt = f"Voici les commentaires positifs pour l'enseignant:\n" + "\n".join(positive_comments) + "\n\n" + \
                        f"Voici les commentaires négatifs pour l'enseignant:\n" + "\n".join(negative_comments) + "\n\n" + \
                        f"Voici les suggestions pour l'enseignant:\n" + "\n".join(suggestions) + "\n\n" + \
                        "Peux-tu me faire une synthèse de ces commentaires en mettant en avant les points forts et les points à améliorer pour cet enseignant ? pour chacun, tu fera une analyse" + \
                        "analyse en un paragraphe de 3 à 4 lignes maximum. Fais une analyse objective et constructive en te basant uniquement sur les commentaires fournis. Ne fais pas d'analyse basée sur des préjugés ou des stéréotypes. Sois précis et concis dans ta synthèse."
                comment= st.button("Générer la synthèse des commentaires", key="generate_summary",help="Faire une analyse des questions qualitatives sur les points positifs, les points négatifs et les suggestions")
                if comment:
                    response = model.generate_content(promt)
                    st.markdown("#### Synthèse des commentaires de l'enseignant " + teacher)
                    st.write(response.text)
                
        else:
            st.info("Aucun enseignant disponible")
    except Exception as e:
        st.warning(f"Erreur: {e}")
        
with ligne2[1]:
    selected_teacher_classes = st.multiselect("Sélectionner une classe pour l'analyse de l'enseignant " + teacher, teacher_classes, default=teacher_classes, key="teacher_class_filter")
    data_teacher_filtered = data_teacher[data_teacher["Classe"].isin(selected_teacher_classes)]
    if not data_teacher_filtered.empty:
        cross_teacher_class = pd.DataFrame()
        for q in [f"Q_{i:02d}" for i in range(1, 19)]:
            if q in data_teacher_filtered.columns:
                responses = data_teacher_filtered[q].value_counts()
                for rep in ["Très satisfait", "Satisfait", "Moyen", "Mauvais"]:
                    if rep not in responses.index:
                        responses[rep] = 0
                cross_teacher_class[q] = responses.loc[["Très satisfait", "Satisfait", "Moyen", "Mauvais"]]
        for col in cross_teacher_class.columns:
            cross_teacher_class[col] = round(100 * cross_teacher_class[col] / cross_teacher_class[col].sum(), 2)
        cross_teacher_class = cross_teacher_class.T
        make_st_heatmap_echat2(cross_teacher_class, cle="teacher_class_heatmap", title=f"Distribution des réponses (%) pour l'enseignant {teacher} dans les classes sélectionnées")

st.markdown("---")
st.markdown("### 📚 Analyse par cours")
ligne3 = st.columns(2)
# Colonne 3: Par cours
with ligne3[0]:
    try:
        if len(data_eval["Classe"].unique()) > 0:
            classe = st.selectbox("Sélectionner une classe", data_eval["Classe"].unique(), key="class_select")
            class_data = data_eval[data_eval["Classe"] == classe]
            
            if not class_data.empty and "Cours" in class_data.columns and len(class_data["Cours"].unique()) > 0:
                cours = st.selectbox("Sélectionner un cours", class_data["Cours"].unique(), key="course_select")
                course_data = class_data[class_data["Cours"] == cours]
                
                if not course_data.empty:
                    responses = []
                    for q in [f"Q_{i:02d}" for i in range(1, 19)]:
                        if q in course_data.columns:
                            responses.extend(course_data[q].tolist())
                    
                    counter = pd.Series(responses).value_counts()
                    dict_course = {}
                    for rep in ["Très satisfait", "Satisfait", "Moyen", "Mauvais"]:
                        dict_course[rep] = counter.get(rep, 0)
                    
                    make_donut_chart(dict_course, cle="course_donut")
        else:
            st.info("Aucune classe disponible")
    except Exception as e:
        st.warning(f"Erreur: {e}")

# ==================== EXPORT DES DONNÉES ====================

st.markdown("---")
st.markdown("## :material/download: Export des données")

exp1, exp2 = st.columns(2)

with exp1:
    st.markdown("### Étudiants")
    try:
        if not student_eval.empty and "classe" in student_eval.columns:
            selected_class = st.multiselect("Classes", student_eval["classe"].unique(), 
                                          default=student_eval["classe"].unique(), key="export_students")
            filtered_students = student_eval[student_eval["classe"].isin(selected_class)]
            
            if st.button("Télécharger", key="download_students",icon=":material/download:"):
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                    filtered_students.to_excel(writer, index=False, sheet_name="Étudiants")
                output.seek(0)
                st.download_button("Télécharger Excel", output, "etudiants.xlsx",
                                 mime="application/vnd.ms-excel", key="btn_students",icon=":material/download:")
    except Exception as e:
        st.warning(f"Erreur: {e}")

with exp2:
    st.markdown("### Évaluations")
    try:
        if not data_eval.empty and "Classe" in data_eval.columns:
            selected_class = st.multiselect("Classes", data_eval["Classe"].unique(),
                                          default=data_eval["Classe"].unique(), key="export_evals")
            filtered_evals = data_eval[data_eval["Classe"].isin(selected_class)]
            
            if st.button("Télécharger", key="download_evals",icon=":material/download:"):
                output = io.BytesIO()
                labels = pd.DataFrame(list(question_dict.items()), columns=['Code', 'Question'])
                with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                    filtered_evals.to_excel(writer, index=False, sheet_name="Evaluations")
                    labels.to_excel(writer, index=False, sheet_name="Labels")
                output.seek(0)
                st.download_button("Télécharger Excel", output, "evaluations.xlsx",
                                 mime="application/vnd.ms-excel", key="btn_evals",icon=":material/download:")
    except Exception as e:
        st.warning(f"Erreur: {e}")

# ==================== AFFICHAGE DES DONNÉES ====================

st.markdown("---")
st.markdown("## :material/table_chart: Données détaillées")

tab1, tab2 = st.tabs(["Étudiants", "Évaluations"])

with tab1:
    if not student_eval.empty:
        #st.dataframe(student_eval, use_container_width=True, hide_index=True)
        Make_Global_DataFrame(student_eval)
    else:
        st.info("Aucune donnée d'étudiant")

with tab2:
    if not data_eval.empty:
        st.dataframe(data_eval, use_container_width=True, hide_index=True)
    else:
        st.info("Aucune donnée d'évaluation")


