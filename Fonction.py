import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from my_fonction import *
import re
from collections import Counter
import jieba
import random
from streamlit_echarts import st_echarts
import io
import hashlib
import json
import os
from datetime import datetime, timedelta



def hash_password(password):
    """Hash un mot de passe pour un stockage sécurisé"""
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    """Charge la base de données des utilisateurs depuis un fichier JSON"""
    if os.path.exists("users.json"):
        with open("users.json", "r") as f:
            return json.load(f)
    return {"users": {}}

def save_users(users):
    """Sauvegarde la base de données des utilisateurs dans un fichier JSON"""
    with open("users.json", "w") as f:
        json.dump(users, f, indent=4)

def import_users_from_excel(excel_path="Connexion.xlsx"):
    """Importe les utilisateurs depuis un fichier Excel vers la base de données JSON"""
    try:
        df = pd.read_excel(excel_path, sheet_name="Identifiant")
        users = load_users()
        
        imported_count = 0
        for _, row in df.iterrows():
            username = row['User'].strip() if isinstance(row['User'], str) else str(row['User'])
            status = row['Statut'].strip() if isinstance(row['Statut'], str) else str(row['Statut'])
            password = row['Password'].strip() if isinstance(row['Password'], str) else str(row['Password'])
            
            if username not in users["users"]:
                users["users"][username] = {
                    "password": hash_password(password),
                    "status": status,
                    "email": f"{username}@example.com",
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "active": True
                }
                imported_count += 1
        
        save_users(users)
        return True, f"{imported_count} utilisateurs importés avec succès"
    except Exception as e:
        return False, f"Erreur lors de l'importation: {str(e)}"

def check_credentials(username, password):
    """Vérifie si les identifiants sont corrects et renvoie également le statut"""
    users = load_users()
    if username in users["users"]:
        user = users["users"][username]
        if not user.get("active", True):
            return False, None
        if user["password"] == hash_password(password):
            return True, user.get("status", "Utilisateur")
    return False, None

def register_user(username, password, email, status="Utilisateur"):
    """Enregistre un nouvel utilisateur avec un statut"""
    users = load_users()
    if username in users["users"]:
        return False, "Ce nom d'utilisateur existe déjà"
    
    users["users"][username] = {
        "password": hash_password(password),
        "email": email,
        "status": status,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "active": True
    }
    save_users(users)
    return True, "Compte créé avec succès"

def update_user(username, new_data):
    """Met à jour les données d'un utilisateur"""
    users = load_users()
    if username not in users["users"]:
        return False, "Utilisateur introuvable"
    
    users["users"][username].update(new_data)
    save_users(users)
    return True, "Utilisateur mis à jour avec succès"

def delete_user(username):
    """Supprime un utilisateur"""
    users = load_users()
    if username not in users["users"]:
        return False, "Utilisateur introuvable"
    
    del users["users"][username]
    save_users(users)
    return True, "Utilisateur supprimé avec succès"

def toggle_user_status(username):
    """Active ou désactive un utilisateur"""
    users = load_users()
    if username not in users["users"]:
        return False, "Utilisateur introuvable"
    
    current_status = users["users"][username].get("active", True)
    users["users"][username]["active"] = not current_status
    save_users(users)
    return True, f"Utilisateur {'désactivé' if current_status else 'activé'} avec succès"





def hash_password2(password):
    """Hash un mot de passe pour un stockage sécurisé"""
    return hashlib.sha256(password.encode()).hexdigest()

def load_users2():
    """Charge la base de données des utilisateurs depuis un fichier JSON"""
    default_user = {
        "users": {
            "Evaluation FC2025": {
                "password": hash_password("Dr GONDZE"),
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        }
    }
    
    if os.path.exists("users.json"):
        with open("users.json", "r") as f:
            return json.load(f)
    
    with open("users.json", "w") as f:
        json.dump(default_user, f, indent=4)
    return default_user

def save_users2(users):
    """Sauvegarde la base de données des utilisateurs dans un fichier JSON"""
    with open("users.json", "w") as f:
        json.dump(users, f, indent=4)

def check_credentials2(username, password):
    """Vérifie si les identifiants sont corrects"""
    users = load_users()
    if username in users["users"]:
        if users["users"][username]["password"] == hash_password(password):
            return True
    return False

def change_password2(username, old_password, new_password):
    """Change le mot de passe d'un utilisateur"""
    users = load_users()
    if username in users["users"]:
        if users["users"][username]["password"] == hash_password(old_password):
            users["users"][username]["password"] = hash_password(new_password)
            save_users(users)
            return True, "Mot de passe changé avec succès"
    return False, "Ancien mot de passe incorrect"

def authentication_system():
    """Système d'authentification pour le dashboard"""
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if "username" not in st.session_state:
        st.session_state["username"] = None
    if "login_time" not in st.session_state:
        st.session_state["login_time"] = None

    if st.session_state["authenticated"]:
        if st.session_state["login_time"] and datetime.now() - st.session_state["login_time"] > timedelta(hours=8):
            st.session_state["authenticated"] = False
            st.session_state["username"] = None
            st.session_state["login_time"] = None
            st.warning("Votre session a expiré. Veuillez vous reconnecter.")
        else:
            st.sidebar.success(f"Connecté en tant que {st.session_state['username']}")
            if st.sidebar.button("Déconnexion"):
                st.session_state["authenticated"] = False
                st.session_state["username"] = None
                st.session_state["login_time"] = None
                st.rerun()
            return True

    tab1, tab2 = st.tabs(["**Connexion**", " "])

    with tab1:
        col=st.columns(2)
        with col[0]:
            username = st.text_input("Nom d'utilisateur", key="login_username")
            password = st.text_input("Mot de passe", type="password", key="login_password")
            
            if st.button("Se connecter"):
                if check_credentials(username, password):
                    st.session_state["authenticated"] = True
                    st.session_state["username"] = username
                    st.session_state["login_time"] = datetime.now()
                    st.success("Connexion réussie!")
                    st.rerun()
                else:
                    st.error("Nom d'utilisateur ou mot de passe incorrect")
        with col[1]:
            #logo de l'école
                st.image("Logo.png", width=200)
                st.markdown("<h2 style='text-align: center; color: #333;'>Bienvenue sur le Dashboard d'Évaluation des enseignants</h2>", unsafe_allow_html=True)
                st.markdown("<p style='text-align: center; color: #555;'>Veuillez vous connecter pour accéder aux données d'évaluation des étudiants.</p>", unsafe_allow_html=True)
    with tab2:
        pass

    return False


def make_heatmap_echart(data, title="", x_label_rotation=45, colors=None, height="400px", cle="heatmap"):
    """
    Generate a heatmap using st_echarts.

    Parameters:
    - data: pd.DataFrame, the data to plot (rows as y-axis, columns as x-axis).
    - title: str, the title of the chart.
    - x_label_rotation: int, rotation angle for x-axis labels.
    - colors: list, list of colors for the heatmap gradient.
    - height: str, height of the chart.

    Returns:
    - None, renders the heatmap in Streamlit.
    """
    if colors is None:
        colors = ["#B9B9FF", "#6D6DFF", "#0505FF","#00009A", "#000050", "#00000C"]  # Default gradient colors

    # Prepare data for the heatmap
    x_labels = data.columns.tolist()
    y_labels = data.index.tolist()
    heatmap_data = [
        [j, i, data.iloc[i, j]] for i in range(len(y_labels)) for j in range(len(x_labels))
    ]
    label_data = [[x[0],x[1],x[2]] for x in heatmap_data]
    
    # Create options for the heatmap
    options = {
        "title": {"text": title, "left": "center"},
        "tooltip": {"position": "top"},
        "xAxis": {
            "type": "category",
            "data": x_labels,
            "axisLabel": {"rotate": x_label_rotation},
        },
        "yAxis": {"type": "category", "data": y_labels},
        "toolbox": {
            "show": True,
            "orient": "vertical",
            "right": "0%",
            "top": "center",
            "feature": {
                "saveAsImage": {"show": True, "title": "Save"},
                "dataZoom": {"show": True, "yAxisIndex": "none"},
                "restore": {"show": True},
            },
        },
        "grid": {
            "left": "10%",
            "right": "10%",
            "bottom": "25%",
            "containLabel": False,
        },
        "visualMap": {
            "min": data.min().min(),
            "max": data.max().max(),
            "calculable": True,
            "orient": "vertical",
            "right": "5%",
            "top": "middle",
            "inRange": {"color": colors},
        },
        "series": [
            {   "name": "Evaluation",
                "type": "heatmap",
                "data": label_data,
                "label": {"show": True},
                "itemStyle": {
                    "borderColor": "#fff",
                    "borderWidth": 1,
                },
                "emphasis": {"itemStyle": {"borderColor": "#333", "borderWidth": 1}},
            }
        ],
    }

    # Render the heatmap
    st_echarts(options=options, height=height, key=cle)


def make_cross_echart(cross_table, title="", x_label_rotation=45, colors=None, height="400px",cle="b"):
    """
    Generate a grouped bar chart using st_echarts from a cross table.

    Parameters:
    - cross_table: pd.DataFrame, a cross table where rows are categories and columns are series.
    - title: str, the title of the chart.
    - x_label_rotation: int, rotation angle for x-axis labels.
    - colors: list, list of colors for the series.
    - height: str, height of the chart.

    Returns:
    - None, renders the chart in Streamlit.
    """
    if colors is None:
        # Default colors if not provided
        colors = ["#0DB329", "#E4E917", "#E79D19", "#E32B1D", "#0CA0B4", "#064C56"]
        

    # Prepare data for the chart
    categories = cross_table.index.tolist()
    series_data = [
        {
            "name": col,
            "data": cross_table[col].tolist(),
            "type": "bar",
            "stack": "total",
            "itemStyle": {"color": colors[i % len(colors)]},
        }
        for i, col in enumerate(cross_table.columns)
    ]

    # Create options for the e_chart
    # Add label formatter to show percentages
    options = {
        "title": {"text": title},
        "tooltip": {"trigger": "axis"},
        "legend": {"data": cross_table.columns.tolist()},
        "xAxis": {
            "type": "category",
            "data": categories,
            "axisLabel": {"rotate": x_label_rotation},
        },
        "yAxis": {
            "type": "value",
            "axisLabel": {"formatter": "{value}%"}
        },
        "series": [{
            **series,
            "label": {
                "show": True,
                "formatter": "{c}%",
                "position": "inside"
            }
        } for series in series_data]
    }
    
    

    # Render the chart
    st_echarts(options=options, height=height, key=cle)


def make_grouped_bar_chart(data, x_col, y_cols, title="", x_label_rotation=45, colors=None, height="400px",cle="a"):
        """
        Generate a grouped bar chart using st_echarts.

        Parameters:
        - data: pd.DataFrame, the data to plot.
        - x_col: str, the column to use for the x-axis.
        - y_cols: list, the columns to use for the y-axis (grouped bars).
        - title: str, the title of the chart.
        - x_label_rotation: int, rotation angle for x-axis labels.
        - colors: list, list of colors for the bars.
        - height: str, height of the chart.

        Returns:
        - None, renders the chart in Streamlit.
        """
        if colors is None:
            # Default colors if not provided
            colors = ["#5470C6", "#91CC75", "#FAC858", "#EE6666", "#73C0DE"]

        # Prepare data for the chart
        categories = data[x_col].tolist()
        series_data = [
            {
                "name": col,
                "data": data[col].tolist(),
                "type": "bar",
                "itemStyle": {"color": colors[i % len(colors)]},
                "label": {
                    "show": True,
                    "position": "top",
                },
            }
            for i, col in enumerate(y_cols)
        ]

        # Create options for the e_chart
        options = {
            "title": {"text": title},
            "tooltip": {"trigger": "axis"},
            "legend": {"data": y_cols},
            "xAxis": {
                "type": "category",
                "data": categories,
                "axisLabel": {"rotate": x_label_rotation},
            },
            "yAxis": {"type": "value"},
            "series": series_data,
        }

        # Render the chart
        st_echarts(options=options, height=height, key=cle)

def make_donut_chart(data, title="", colors=None, height="400px", cle="donut"):
                """
                Generate a donut chart using st_echarts.

                Parameters:
                - data: dict, keys are labels and values are corresponding numerical values.
                - title: str, the title of the chart.
                - colors: list, list of colors for the segments.
                - height: str, height of the chart.

                Returns:
                - None, renders the chart in Streamlit.
                """
                if colors is None:
                    colors = ["#0DB329", "#E4E917", "#E79D19", "#E32B1D", "#0CA0B4", "#064C56"]

                # Prepare data for the chart
                series_data = [{"value": value, "name": key} for key, value in data.items()]
                # Add percentage data to the series_data
                for item in series_data:
                    item['value'] = round(item['value'] / sum(d['value'] for d in series_data) * 100, 2)
                    item['name'] = f"{item['name']} ({item['value']}%)"
                # Create options for the donut chart
                # Update value percentages in data for the legend
                data_with_percentages = {}
                total = sum(data.values())
                for key, value in data.items():
                    percentage = round((value / total) * 100, 2)
                    data_with_percentages[f"{key} ({percentage}%)"] = value
                options = {
                    "title": {"text": title, "left": "center"},
                    "tooltip": {"trigger": "item"},
                    "legend": {
                        "orient": "horizontal",
                        "top": "top",
                        "data": list(data.keys()),
                    },
                    "series": [
                        {
                            "name": "Evaluation",
                            "type": "pie",
                            "radius": ["30%", "70%"],
                            "avoidLabelOverlap": False,
                            "itemStyle": {"borderRadius": 3, "borderColor": "#fff", "borderWidth": 4},
                            "label": {"show": True, "position": "outside"},
                            "emphasis": {
                                "label": {"show": True, "fontSize": "16", "fontWeight": "bold"}
                            },
                            "data": series_data,
                        }
                    ],
                    "color": colors,
                }

                # Render the chart
                st_echarts(options=options, height=height, key=cle)


          
def make_st_heatmap_echat2(df, title="", height="700px", cle="bdjbdc"):
    """
    Create an interactive heatmap using echarts
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The crosstab or pivot table to visualize
    title : str
        Title of the heatmap
    height : str
        Height of the chart (default "600px")
    """
    # Convert timestamps in index and columns to strings
    df.columns = [str(col) for col in df.columns]
    df.index = [str(idx) for idx in df.index]
    
    x_labels = df.columns.tolist()
    y_labels = df.index.tolist()
    
    # Determine which axis should be longer
    #if len(x_labels) < len(y_labels):
        #x_labels, y_labels = y_labels, x_labels
        #df = df.T

    data = []
    for i, y_val in enumerate(y_labels):
        for j, x_val in enumerate(x_labels):
            value = df.iloc[i, j]
            try:
                value = float(value)
            except:
                value = 0  # ou np.nan si tu veux ignorer
            data.append([j, i, value])

    options = {
        "tooltip": {"position": 'top'},
        "grid": {
            "height": '87%',
            "top": '1%'
        },
        "xAxis": {
            "type": 'category',
            "data": x_labels,
            "splitArea": {"show": True},
            "axisLabel": {
                "rotate": 45 if len(x_labels)>5 else 0,
                "interval": 0,
                "fontSize": 14,
                "width": 50,
                "overflow": "truncate"
            }
        },
        "yAxis": {
            "type": 'category',
            "data": y_labels,
            "splitArea": {"show": True}
        },
        "visualMap": {
            "min": 0,
            "max": max([d[2] for d in data]),
            "calculable": True,
            "orient": 'vertical',
            "right": '3%',
            "bottom": '50%'
        },
        "series": [{
            "name": "Charge accomplie",
            "type": 'heatmap',
            "data": data,
            "label": {"show": True},
            "emphasis": {
                "itemStyle": {
                    "shadowBlur": 10,
                    "shadowColor": 'rgba(0, 0, 0, 0.5)'
                }
            }
        }]
    }

    st.write(title)
    st_echarts(options=options, height=height, key=cle)




# Mapping des niveaux de satisfaction vers des scores numériques
SATISFACTION_SCORE = {
    "Très satisfait": 3,
    "Satisfait": 2,
    "Moyen": 1,
    "Mauvais": 0,
}

SATISFACTION_LEVELS = ["Mauvais", "Moyen", "Satisfait", "Très satisfait"]
SATISFACTION_COLORS = ["#e74c3c", "#f39c12", "#3498db", "#2ecc71"]

# Scores pour déterminer la modalité sélectionnée (valeur == 1)
LEVEL_MAP = {
    "Très satisfait": "Très satisfait",
    "Satisfait": "Satisfait",
    "Moyen": "Moyen",
    "Mauvais": "Mauvais",
}


def render_3d_bar_chart(data: dict, title: str = "Satisfaction 2BD — Vue 3D"):
    """
    Affiche un graphique à barres 3D groupées/empilées.
    - Axe X : noms des enseignants
    - Axe Y : questions (Q_01 → Q_18)
    - Axe Z : proportion (%) de chaque modalité de notation

    Args:
        data (dict): {nom_enseignant: {Q_xx: {"Très satisfait": 0|1, ...}}}
        title (str): Titre affiché sur le graphique
    """

    persons = list(data.keys())
    questions = sorted({q for p in data.values() for q in p.keys()})

    # Noms courts pour l'axe X
    short_names = [name.split()[0] for name in persons]

    # ── Construire les séries 3D empilées ────────────────────────────────
    # Chaque point = [x_idx (personne), y_idx (question), proportion_%]
    # On génère 4 séries (une par modalité), empilées sur l'axe Z.
    # La proportion = nb_répondants_ayant_choisi_ce_niveau / nb_total_répondants × 100
    # (Ici 1 répondant par cellule → 100% pour la modalité choisie, 0% pour les autres)

    # Compter par (personne, question, modalité)
    # Structure: counts[(p_idx, q_idx)][level] = count
    counts = {}
    for p_idx, (person, person_data) in enumerate(data.items()):
        for q_idx, question in enumerate(questions):
            key = (p_idx, q_idx)
            counts[key] = {lvl: 0 for lvl in SATISFACTION_LEVELS}
            if question in person_data:
                selected = next(
                    (lvl for lvl, val in person_data[question].items() if val == 1),
                    None
                )
                if selected and selected in counts[key]:
                    counts[key][selected] += 1

    # Total par cellule
    totals = {k: sum(v.values()) for k, v in counts.items()}

    series = []
    for lvl_idx, level in enumerate(SATISFACTION_LEVELS):
        bar_data = []
        for p_idx in range(len(persons)):
            for q_idx in range(len(questions)):
                key = (p_idx, q_idx)
                total = totals.get(key, 0)
                count = counts.get(key, {}).get(level, 0)
                proportion = round((count / total * 100) if total > 0 else 0, 1)
                # Inclure tous les points (même 0) pour que le stack fonctionne
                bar_data.append([p_idx, q_idx, proportion])

        series.append({
            "type": "bar3D",
            "name": level,
            "data": bar_data,
            "stack": "satisfaction",
            "shading": "lambert",
            "label": {"show": False},
            "itemStyle": {
                "color": SATISFACTION_COLORS[lvl_idx],
                "opacity": 0.90,
            },
            "emphasis": {
                "label": {
                    "show": True,
                    "textStyle": {"color": "#fff", "fontSize": 11, "fontWeight": "bold"},
                    "formatter": "function(p){ return p.data[2] + '%'; }",
                },
                "itemStyle": {"color": SATISFACTION_COLORS[lvl_idx]},
            },
        })

    option = {
        "backgroundColor": "#0d1117",
        "title": {
            "text": title,
            "left": "center",
            "top": 10,
            "textStyle": {
                "color": "#e0e0e0",
                "fontSize": 20,
                "fontWeight": "bold",
                "fontFamily": "Georgia, 'Times New Roman', serif",
            },
        },
        "tooltip": {
            "trigger": "item",
            "formatter": """function(params) {
                var levels = ['Mauvais', 'Moyen', 'Satisfait', 'Très satisfait'];
                var colors = ['#e74c3c', '#f39c12', '#3498db', '#2ecc71'];
                return '<b>' + params.seriesName + '</b><br/>'
                     + 'Enseignant : <b>' + params.name + '</b>';
            }""",
            "backgroundColor": "#1c1c2e",
            "borderColor": "#333",
            "textStyle": {"color": "#ecf0f1"},
        },
        "legend": {
            "data": SATISFACTION_LEVELS,
            "top": 50,
            "left": "center",
            "orient": "horizontal",
            "textStyle": {"color": "#ccc", "fontSize": 12},
            "itemWidth": 18,
            "itemHeight": 12,
            "itemGap": 20,
        },
        "grid3D": {
            "boxWidth": 220,
            "boxDepth": 120,
            "boxHeight": 80,
            "viewControl": {
                "projection": "perspective",
                "autoRotate": False,
                "autoRotateSpeed": 5,
                "distance": 220,
                "alpha": 25,
                "beta": 30,
                "rotateSensitivity": 2,
                "zoomSensitivity": 1.5,
            },
            "light": {
                "main": {
                    "intensity": 1.3,
                    "shadow": True,
                    "shadowQuality": "high",
                },
                "ambient": {"intensity": 0.4},
            },
            "axisLine": {
                "lineStyle": {"color": "#555", "width": 1.5}
            },
            "axisLabel": {
                "textStyle": {"color": "#aaa", "fontSize": 10}
            },
            "splitLine": {
                "lineStyle": {"color": "#333", "opacity": 0.6}
            },
            "temporalSuperSampling": {"enable": True},
        },
        "xAxis3D": {
            "type": "category",
            "name": "Enseignants",
            "data": short_names,
            "nameTextStyle": {
                "color": "#81d4fa",
                "fontSize": 13,
                "fontWeight": "bold",
            },
            "axisLabel": {
                "textStyle": {"color": "#ccc", "fontSize": 9},
                "rotate": 10,
            },
            "axisLine": {"lineStyle": {"color": "#555"}},
        },
        "yAxis3D": {
            "type": "category",
            "name": "Questions",
            "data": questions,
            "nameTextStyle": {
                "color": "#a5d6a7",
                "fontSize": 13,
                "fontWeight": "bold",
            },
            "axisLabel": {
                "textStyle": {"color": "#ccc", "fontSize": 9},
            },
        },
        "zAxis3D": {
            "type": "value",
            "name": "Proportion (%)",
            "min": 0,
            "max": 100,
            "nameTextStyle": {
                "color": "#ffcc80",
                "fontSize": 13,
                "fontWeight": "bold",
            },
            "axisLabel": {
                "textStyle": {"color": "#aaa", "fontSize": 9},
                "formatter": "function(val){ return val + '%'; }",
            },
        },
        "series": series,
    }

    # ── Rendu ─────────────────────────────────────────────────────────────
    st.markdown(
        f"""
        <div style="text-align:center; margin-bottom: 8px;">
            <span style="color:#888; font-size:13px; font-style:italic;">
                🖱️ Cliquez-glissez pour faire pivoter · Molette pour zoomer
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st_echarts(
        options=option,
        height="680px",
    )

def generate_word_cloud(df, column_name, max_words=100, min_frequency=3, 
                        width=550, height=500, title="Nuage de mots", 
                        color_range=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b'], random_seed=None):
    """
    Génère un nuage de mots interactif à partir d'une colonne de texte d'un DataFrame
    
    Paramètres:
    -----------
    df : pandas.DataFrame
        Le DataFrame contenant les données
    column_name : str
        Le nom de la colonne contenant le texte à analyser
    max_words : int, optionnel (défaut=100)
        Nombre maximum de mots à afficher
    min_frequency : int, optionnel (défaut=1)
        Fréquence minimale pour inclure un mot
    width : int, optionnel (défaut=800)
        Largeur du graphique en pixels
    height : int, optionnel (défaut=500)
        Hauteur du graphique en pixels
    title : str, optionnel (défaut="Nuage de mots")
        Titre du graphique
    color_range : list, optionnel (défaut=None)
        Liste de couleurs pour le nuage de mots, ex: ['#313695', '#4575b4', '#74add1', '#abd9e9']
    random_seed : int, optionnel (défaut=None)
        Graine aléatoire pour reproduire les résultats
    
    Retourne:
    ---------
    None - Affiche le graphique dans Streamlit
    """
    if random_seed is not None:
        random.seed(random_seed)
        np.random.seed(random_seed)
    
    # Définir les couleurs par défaut si non spécifiées
    if color_range is None:
        color_range = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
    
    # Vérifier que la colonne existe
    if column_name not in df.columns:
        st.error(f"La colonne '{column_name}' n'existe pas dans le DataFrame.")
        return
    
    # Ignorer les valeurs NaN
    texts = df[column_name].dropna().astype(str).tolist()
    
    if not texts:
        st.warning(f"La colonne '{column_name}' ne contient pas de texte valide.")
        return
    
    # Combiner tous les textes
    all_text = " ".join(texts)
    
    # Nettoyer le texte
    all_text = all_text.lower()
    all_text = re.sub(r'[^\w\s]', '', all_text)  # Enlever la ponctuation
    
    # Tokenizer le texte (utilisation de jieba qui fonctionne bien pour le texte français également)
    words = jieba.lcut(all_text)
    
    # Filtrer les mots vides (vous pouvez ajouter votre propre liste de stopwords)
    stopwords = set(['le', 'la', 'les', 'du', 'de', 'des', 'un', 'une', 'et', 'est', 'à', 'en', 'que', 'qui', 
                      'pour', 'dans', 'ce', 'il', 'elle', 'ils', 'elles', 'nous', 'vous', 'on', 'je', 'tu',
                      'avec', 'par', 'au', 'aux', 'sur', 'ou', 'donc', 'or', 'ni', 'car', 'mais', 'où',
                      'comment', 'quand', 'pourquoi', 'si', 'ne', 'pas', 'plus', 'moins', 'peu', 'très'])
    words = [word for word in words if word not in stopwords and len(word) > 1]
    
    # Compter les fréquences des mots
    word_counts = Counter(words)
    
    # Filtrer par fréquence minimale
    word_counts = {word: count for word, count in word_counts.items() if count >= min_frequency}
    
    # Limiter au nombre maximum de mots
    sorted_word_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:max_words]
    
    # Préparer les données pour ECharts avec des couleurs aléatoires pour chaque mot
    data = []
    for word, count in sorted_word_counts:
        data.append({
            "name": word, 
            "value": count,
            "textStyle": {
                "normal": {
                    "color": random.choice(color_range)
                }
            }
        })
    
    # Options pour ECharts
    options = {
        "title": {
            "text": title,
            "left": "center"
        },
        "tooltip": {},
        "series": [{
            "type": "wordCloud",
            "shape": "square",
            #"left": "left",
            "top": "center", 
            "width": "100%",
            "height": "100%",
            #"right": None,
            "bottom": None,
            "sizeRange": [12, 60],
            "rotationRange": [-90, 90],
            "rotationStep": 45,
            "gridSize": 8,
            "drawOutOfBound": False,
            "textStyle": {
                "fontFamily": "sans-serif",
                "fontWeight": "bold"
            },
            "emphasis": {
                "focus": "self",
                "textStyle": {
                    "shadowBlur": 10,
                    "shadowColor": "#333",
                    "color": color_range  
                }
            },
            "data": data
        }]
    }
    
    # Afficher le nuage de mots dans Streamlit
    st_echarts(options=options, height=height, width=width)