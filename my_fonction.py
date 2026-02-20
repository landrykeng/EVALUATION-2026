#==========IMPORTATION DES BIBLIOTHEQUES NECESSAIRES===================================
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import geopandas as gpd
import streamlit as st
from scipy.stats import chi2_contingency
from scipy.stats import ttest_ind
from scipy.stats import levene
import random
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import io
import os
import json
import branca.colormap as cm
import folium
from folium.plugins import MarkerCluster
from branca.colormap import linear
from streamlit_folium import folium_static
import datetime
from datetime import datetime, timedelta
from streamlit_echarts import st_echarts
import base64
import hashlib
import time
import requests

#==================================================================================================

#============Variables Globales====================================================================
police=dict(size=25,family="Berlin Sans FB",)
police_label=dict(size=15,family="Berlin Sans FB",)
police_annot=dict(size=15,family="Berlin Sans FB",)
palette = ['#FDC7D3', '#F61A49', '#640419', '#49030D','#4575B4', '#74ADD1', '#ABD9E9', '#E0F3F8']
val_couleur=[['#FDC7D3'], ['#F61A49'], ['#640419'],['#49030D'],['#4575B4'],["#74ADD1"]]
sequence_couleur=['reds', 'agsunset', 'algae', 'amp', 'armyrose', 'balance',
             'blackbody', 'bluered', 'blues', 'blugrn', 'bluyl', 'brbg',
             'brwnyl', 'bugn', 'bupu', 'burg', 'burgyl', 'cividis', 'curl',
             'darkmint', 'deep', 'delta', 'dense', 'earth', 'edge', 'electric',
             'emrld', 'fall', 'geyser', 'gnbu', 'gray', 'greens', 'greys',
             'haline', 'hot', 'hsv', 'ice', 'icefire', 'inferno', 'jet',
             'magenta', 'magma', 'matter', 'mint', 'mrybm', 'mygbm', 'oranges',
             'orrd', 'oryel', 'oxy', 'peach', 'phase', 'picnic', 'pinkyl',
             'piyg', 'plasma', 'plotly3', 'portland', 'prgn', 'pubu', 'pubugn',
             'puor', 'purd', 'purp', 'purples', 'purpor', 'rainbow', 'rdbu',
             'rdgy', 'rdpu', 'rdylbu', 'rdylgn', 'redor', 'aggrnyl', 'solar',
             'spectral', 'speed', 'sunset', 'sunsetdark', 'teal', 'tealgrn',
             'tealrose', 'tempo', 'temps', 'thermal', 'tropic', 'turbid',
             'turbo', 'twilight', 'viridis', 'ylgn', 'ylgnbu', 'ylorbr',
             'ylorrd']

useless_style="""
<style>
.sidebar-link {
    display: block;
    margin-bottom: 15px;
    padding: 10px 15px;
    text-decoration: none;
    color: #333;
    background-color: #f8f9fa;
    border-radius: 8px;
    transition: all 0.3s ease;
    font-weight: 500;
}

.sidebar-link-right {
    display: block;
    margin-bottom: 15px;
    padding: 10px 15px;
    text-decoration: none;
    color: #333;
    background-color: #f8f9fa;
    border-radius: 8px;
    transition: all 0.3s ease;
    font-weight: 500;
    text-align: right;
}

.sidebar-link-center {
    display: block;
    margin-bottom: 15px;
    padding: 10px 15px;
    text-decoration: none;
    color: #333;
    background-color: #f8f9fa;
    border-radius: 8px;
    transition: all 0.3s ease;
    font-weight: 500;
    text-align: center;
}
</style>
"""

echart_style="""
        <style>
        /* Styles de base pour tous les thèmes */
        .stContainer {
            border-radius: 10px;  /* Coins arrondis */
            border: 2px solid transparent;  /* Bordure transparente par défaut */
            padding: 20px;  /* Espacement intérieur */
            margin-bottom: 20px;  /* Espace entre les conteneurs */
            transition: all 0.3s ease;  /* Animation douce */
        }

        /* Mode Clair (par défaut) */
        body:not(.dark) .stContainer {
            background-color: rgba(255, 255, 255, 0.9);  /* Fond blanc légèrement transparent */
            border-color: rgba(224, 224, 224, 0.7);  /* Bordure grise légère */
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.08);  /* Ombre douce */
        }

        /* Mode Sombre */
        body.dark .stContainer {
            background-color: rgba(30, 30, 40, 0.9);  /* Fond sombre légèrement transparent */
            border-color: rgba(60, 60, 70, 0.7);  /* Bordure sombre légère */
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);  /* Ombre plus marquée */
        }

        /* Effet de survol - Mode Clair */
        body:not(.dark) .stContainer:hover {
            box-shadow: 0 8px 12px rgba(0, 0, 0, 0.5);  /* Ombre plus prononcée */
            transform: translateY(-5px);  /* Léger soulèvement */
            border-color: rgba(200, 200, 200, 0.9);  /* Bordure plus visible */
        }

        /* Effet de survol - Mode Sombre */
        body.dark .stContainer:hover {
            box-shadow: 0 8px 12px rgba(255, 255, 255, 0.5);  /* Ombre claire */
            transform: translateY(-5px);  /* Léger soulèvement */
            border-color: rgba(100, 100, 110, 0.9);  /* Bordure plus visible */
        }

        /* Style spécifique pour les graphiques - Mode Clair */
        body:not(.dark) .stPlotlyChart {
            background-color: rgba(250, 250, 250, 0.95);  /* Fond très légèrement gris */
            border-radius: 8px;  /* Coins légèrement arrondis */
            padding: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);  /* Ombre très légère */
        }

        /* Style spécifique pour les graphiques - Mode Sombre */
        body.dark .stPlotlyChart {
            background-color: rgba(40, 40, 50, 0.95);  /* Fond sombre légèrement transparent */
            border-radius: 8px;  /* Coins légèrement arrondis */
            padding: 10px;
            box-shadow: 0 2px 4px rgba(255, 255, 255, 0.05);  /* Ombre très légère */
        }

        /* Style spécifique pour les graphiques ECharts */
        .echarts-container {
            border-radius: 10px;
            padding: 5px;
            margin-bottom: 20px;
            transition: all 0.3s ease;
        }

        body:not(.dark) .echarts-container {
            background-color: rgba(255, 255, 255, 0.9);
            border: 2px solid rgba(224, 224, 224, 0.7);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.08);
        }

        body.dark .echarts-container {
            background-color: rgba(30, 30, 40, 0.9);
            border: 2px solid rgba(60, 60, 70, 0.7);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        }

        body:not(.dark) .echarts-container:hover {
            box-shadow: 0 8px 12px rgba(0, 0, 0, 0.15);
            transform: translateY(-3px);
        }

        body.dark .echarts-container:hover {
            box-shadow: 0 8px 12px rgba(255, 255, 255, 0.1);
            transform: translateY(-3px);
        }
        </style>
    """

#st.set_page_config(layout="wide")
#==================================================================================================

#==================================================================================================
# FONCTIONS
#==================================================================================================
#1. Fonction pour faire les regroupement de classe d'âge
def class_age(age):
    if age < 20:
        return "- 20 ans"
    elif age < 30:
        return "20-30 ans"
    elif age < 40:
        return "30-40 ans"
    elif age < 50:
        return "40-50 ans"
    elif age < 60:
        return "50-60 ans"
    else:
        return "+60 ans"

#2. Fonction de tranduction 



#3. Fonction d'affichage des métriques version 1
def display_single_metric_advanced(label, value, delta, unit="", caption="", color_scheme="blue"):
    """Affiche une seule métrique avec un style avancé et personnalisable."""

    color = {
        "blue": {"bg": "#e6f2ff", "text": "#336699", "delta_pos": "#007bff", "delta_neg": "#dc3545"},
        "green": {"bg": "#e6ffe6", "text": "#28a745", "delta_pos": "#28a745", "delta_neg": "#dc3545"},
        "red": {"bg": "#ffe6e6", "text": "#dc3545", "delta_pos": "#28a745", "delta_neg": "#dc3545"},
    }.get(color_scheme, {"bg": "#f0f0f0", "text": "#333", "delta_pos": "#28a745", "delta_neg": "#dc3545"})

    delta_color = "green" if delta >= 0 else "red"
    st.markdown(
        f"""
        <div style="background-color: {color['bg']}; padding: 2px; border-radius: 5px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); text-align: center;">
            <h4 style="color: {color['text']}; margin-bottom: 1.5px;">{label}</h4>
            <div style="font-size: 1.5em; font-weight: bold; color: {color['text']};">{value} {unit}</div>
            <div style="font-size: 1em; color: {delta_color};">{'▲' if delta >= 0 else '▼'} {abs(delta)}  {"-----"}  {'▲' if delta >= 0 else '▼'} {abs(delta)}</div>
            <p style="font-size: 1em; color: {color['text']};">{caption}{"-----"}{caption}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

#4. Fonction pour tracer l'histogramme croisé de deux variables  version 1
def make_cross_hist(df,var1,var2,titre="",typ_bar=1,width=500, height=400,sens="v"):
    bar_mode= "relative" if typ_bar==1 else "group"
    cross_df=pd.crosstab(df[var1],df[var2])
    table_cross = cross_df.reset_index().melt(id_vars=var1, var_name=var2, value_name='Effectif')
    table_cross=table_cross.sort_values("Effectif",ascending=False)
    fig = px.bar(table_cross, x=var2 if sens=="v" else 'Effectif' , y=var2 if sens=="h" else 'Effectif', color=var1, text_auto='.2s', 
                            title=titre, barmode=bar_mode,orientation=sens,)
    fig.update_layout(margin=dict(l=5, r=1, t=30, b=10),width=width, height=height,
                    title=dict(
        text=titre,
        x=0.0,  
        y=0.95, 
        xanchor='left', 
        yanchor='top'),
            legend=dict(
            x=0.8,  # Position horizontale (à droite)
            y=1,  # Position verticale (en haut)
            traceorder='normal',
            xanchor='center',  # Alignement horizontal de la légende
            yanchor='top',  # Alignement vertical de la légende
            bgcolor='rgba(255,255,255,0.1)',  # Fond semi-transparent de la légende
        ))
    
    st.plotly_chart(fig)
 
#5. Fonction pour tracer l'histogramme croisé de deux variables  version 2   
def make_cross_hist_2(df,var1,var2,titre="",typ_bar=2,width=500, height=400,sens="v"):
    bar_mode= "stack" if typ_bar==1 else "group"
    cross_df=pd.crosstab(df[var1],df[var2])
    table_cross = cross_df.reset_index().melt(id_vars=var1, var_name=var2, value_name='Effectif')
    table_cross=table_cross.sort_values("Effectif",ascending=False)
    fig = go.Figure()
    y_var=list(df[var1].unique())
    x_var=list(df[var2].unique())
    for i in range(len(y_var)):
        y_data = list(table_cross[table_cross[var1] == y_var[i]]["Effectif"])
        fig.add_trace(go.Bar(name=y_var[i],x=x_var if sens=='v' else y_data, y=x_var if sens=='h' else y_data,
                             text=y_data,  # Ajouter les valeurs sur les barres
            textposition='auto' ,
            orientation=sens,# Positionner les étiquettes automatiquement
            ))
    fig.update_layout(width=width, height=height, barmode=bar_mode,
                    title=dict(
        text=titre,
        x=0.0,  # Centre horizontalement
        y=0.95,  # Légèrement en dessous du bord supérieur
        xanchor='left', 
        yanchor='top'),)
    fig.update_layout(
        barmode=bar_mode,
        title=titre,
        margin=dict(l=5, r=1, t=30, b=10),
        legend=dict(
            x=0.8,  # Position horizontale (à droite)
            y=1,  # Position verticale (en haut)
            traceorder='normal',
            xanchor='center',  # Alignement horizontal de la légende
            yanchor='top',  # Alignement vertical de la légende
            bgcolor='rgba(255,255,255,0.1)',  # Fond semi-transparent de la légende
        )
    )
    st.plotly_chart(fig)
 
 #4. Fonction pour tracer l'histogramme croisé de deux variables    

#6. Fonction pour tracer graphique type anneau de progression
def make_progress_char(value,couleur,titre="",width=500, height=300,ecart=50):
    n=int(ecart*value)
    p=ecart-n
    values = [1 for i in range(n+p)]
    col2=["rgba(0, 0, 0, 0.2)" for i in range(p)]
    col1=[couleur for i in range(n)]
    colors = col2 + col1

    fig = go.Figure(data=[go.Pie( values=values,hole=.7, 
                                pull=[0.07 for i in range(n+p)],
                                hoverinfo="none",
                                marker=dict(colors=colors),
                                textinfo='none')],)
    fig.add_trace(go.Pie(
        labels=["labels2","ajcn"],
        values=[13,42],
        hoverinfo="none",
        textinfo='none',
        opacity=0.15,
        #hole=0.75, 
        marker=dict(colors=[couleur,couleur]),
        domain={'x': [0.2, 0.8], 'y': [0.2, 0.8]}
    ))
    fig.update_layout(width=width, height=height,
                        title=dict(
                                    text=titre,
                                    x=0.1,  # Centre horizontalement
                                    y=0.99,  # Légèrement en dessous du bord supérieur
                                    xanchor='left', 
                                    yanchor='top'),
                        showlegend=False,
                        margin=dict(l=0, r=0, t=30, b=10),
                        paper_bgcolor='rgba(248,248,250,0)',
                        plot_bgcolor='rgba(248,248,250,0)',
                        annotations=[dict(text=str(round(100*value,2))+'%', x=0.5, y=0.5,
                        font_size=40, showarrow=False, xanchor="center",font=dict(color=couleur, family="Berlin Sans FB"))])
    st.plotly_chart(fig)
 
#7. Fonction pour tracer graphique type barre de progression version 3    
def make_cross_hist_3(df,var_alpha,var_num,titre,width=500,height=300,bar_mode=1,agregation="count",color="blue",sens='v'):
    bar_mode="relative" if bar_mode==1 else "group"
    fig = go.Figure()
    fig.add_trace(go.Histogram(histfunc=agregation, y=df[var_num], x=df[var_alpha], name=var_num,marker=dict(color=color),opacity=0.7))
    fig.update_layout(width=width, height=height, barmode=bar_mode,
                        title=dict(
            text=titre,
            x=0.0,  # Centre horizontalement
            y=0.95,  # Légèrement en dessous du bord supérieur
            xanchor='left', 
            yanchor='top'),)
    fig.update_layout(
            barmode=bar_mode,
            title=titre,
            margin=dict(l=5, r=1, t=30, b=10),
            legend=dict(
                x=0.8,  # Position horizontale (à droite)
                y=1,  # Position verticale (en haut)
                traceorder='normal',
                orientation=sens,  # Orientation verticale
                xanchor='center',  # Alignement horizontal de la légende
                yanchor='top',  # Alignement vertical de la légende
                bgcolor='rgba(255,255,255,0.1)',  # Fond semi-transparent de la légende
            )
        )

    st.plotly_chart(fig)
    
#7. Fonction de test d'indépendance de Khi 2
def test_independance_khi2(df, var1, var2):
    # Création de la table de contingence
    contingency_table = pd.crosstab(df[var1], df[var2])
    index_labels = list(df[var1].unique())
    table_cross = pd.DataFrame(contingency_table, index=index_labels)
    # Application du test Khi-2
    chi2, p, dof, expected = chi2_contingency(contingency_table)
    
    # Conclusion
    if p < 0.05:
        conclusion = f"Le test du Khi-deux rejette/accepte l'hypothèse nulle d'indépendance (ou d'ajustement) à 5% (χ² = {chi2}, p-value = {p}). La statistique calculée excède la critique, indiquant une association significative entre les variables. Au seuil de 10%, la conclusion persiste, consolidant la significativité. L'analyse des résidus standardisés révèle les catégories contribuant majoritairement à la statistique. Les effectifs théoriques étant supérieurs à 5 (conditions de Cochran respectées), l'approximation par la loi χ² reste valide. Ainsi, l'hypothèse d'indépendance est infirmée avec une robustesse confirmée."
    else:
        conclusion = "Les variables sont indépendantes."
    
    
    
    # Retour des résultats
    return  conclusion, table_cross,chi2, p,dof
  
#8. Fonction de test de comparaison de la moyenne
def test_comparaison_moyenne(df, var1, var2):
    # Séparation des groupes
    groupe1 = df[df[var1] == 1]  
    groupe2 = df[df[var1] == 0]
    # Test de Student pour comparer les moyennes
    t_stat, p_value = ttest_ind(groupe1[var2], groupe2[var2])
    # Conclusion
    
    fig=px.histogram(df,x=var2,color=var1,marginal="box",color_discrete_sequence=palette,opacity=0.8)
    if p_value < 0.05:
        result=f"Au seuil de significativité de 5%, l'hypothèse nulle d'égalité des moyennes est rejetée / acceptée (p-value = {p_value}, t = {t_stat}). Cela indique une différence statistiquement significative entre les groupes comparés, avec un risque d'erreur de première espèce contrôlé à 5%. Toutefois, au seuil de 10%, la conclusion demeure robuste, renforçant l'évidence contre l'hypothèse nulle. "
    else:
        result="Les moyennes des deux groupes ne sont pas significativement différentes."
    return result, fig

#9. Fonction d'affichage des métriques version 2
def plot_metric(label, value, prefix="", suffix="", show_graph=False, color_graph=""):
    fig = go.Figure()

    fig.add_trace(
        go.Indicator(
            value=value,
            gauge={"axis": {"visible": False}},
            number={
                "prefix": prefix,
                "suffix": suffix,
                "font.size": 30,
                "font": {"size": 30, 
                         "family":"Berlin Sans FB"}
            },
            title={
                "text": label,
                "font": {"size": 30, 
                         "family":"Berlin Sans FB"},
            },
        )
    )

    if show_graph:
        fig.add_trace(
            go.Scatter(
                y=random.sample(range(0, 101), 30),
                hoverinfo="skip",
                fill="tozeroy",
                fillcolor=color_graph,
                line={
                    "color": color_graph,
                },
            )
        )

    fig.update_xaxes(visible=False, fixedrange=True)
    fig.update_yaxes(visible=False, fixedrange=True)
    fig.update_layout(
        # paper_bgcolor="lightgrey",
        margin=dict(t=0, b=0),
        showlegend=False,
        #plot_bgcolor="white",
        height=100,
        paper_bgcolor='rgba(248,248,250,0)',
        plot_bgcolor='rgba(248,248,250,0)',
    )

    st.plotly_chart(fig, use_container_width=True)

#10. Fonction d'affichage des métriques version 3
def plot_metric_2(label,df,var, prefix="", suffix="", show_graph=False, color_graph="#330C73",val_bin=60):
    fig = go.Figure()
    value=df[var].mean()
    fig.add_trace(
        go.Indicator(
            value=value,
            gauge={"axis": {"visible": False}},
            number={
                "prefix": prefix,
                "suffix": suffix,
                "font.size": 30,
                "font": {"size": 30, 
                         "family":"Berlin Sans FB"}
            },
            title={
                "text": label,
                "font": {"size": 30, 
                         "family":"Berlin Sans FB"},
            },
        )
    )

    if show_graph:
        x_graph=df[var]
        n_bin=(max(x_graph) - min(x_graph)) / val_bin
        fig.add_trace(go.Histogram(x=x_graph,marker_color=color_graph,opacity=0.75, xbins=dict(
                    start=min(x_graph),  # Début des bins
                    end=max(x_graph),    # Fin des bins
                    size=n_bin))
                                )

    fig.update_xaxes(visible=False, fixedrange=True)
    fig.update_yaxes(visible=False, fixedrange=True)
    fig.update_layout(
        paper_bgcolor='rgba(248,248,250,0)',
        plot_bgcolor='rgba(248,248,250,0)',
        # paper_bgcolor="lightgrey",
        margin=dict(t=0, b=0),
        showlegend=False,
        #plot_bgcolor="white",
        height=100,
    )

    st.plotly_chart(fig, use_container_width=True)

#10. Fonction pour tracer un demi aneau de progression
def plot_gauge(
    indicator_number, indicator_color, indicator_suffix, indicator_title, max_bound
):
    fig = go.Figure(
        go.Indicator(
            value=indicator_number,
            mode="gauge+number",
            domain={"x": [0, 1], "y": [0, 1]},
            number={
                "suffix": indicator_suffix,
                "font.size": 26,
            },
            gauge={
                "axis": {"range": [0, max_bound], "tickwidth": 1},
                "bar": {"color": indicator_color},
            },
            title={
                "text": indicator_title,
                "font": {"size": 28},
            },
        )
    )
    fig.update_layout(
        # paper_bgcolor="lightgrey",
        height=200,
        margin=dict(l=10, r=10, t=50, b=10, pad=8),
    )
    st.plotly_chart(fig, use_container_width=True)

#11. Fonction pour tracer un heatmap
def make_heat_map(df,vars,oder_var,label_var,titre="",width=500, height=300):
    data_mp = df.groupby(vars).agg({
        oder_var: 'size',
    }).reset_index()
    data_mp=data_mp.rename(columns={oder_var: 'Effectif'})
    path_vars=[px.Constant('All')]+ vars
    fig = px.icicle(data_mp, path=path_vars, values='Effectif',
                    color='Effectif', hover_data=[label_var],
                    color_continuous_scale="sunsetdark")
    fig.update_traces(
        textinfo="label+value",  # Affiche le nom du segment et sa valeur
        textposition="middle center",  # Position du texte au centre des segments
        insidetextfont=dict(color='white', size=12)  # Personnalisation du texte
    )
    fig.update_layout(
            title=titre,
            width=width, height=height,
            margin=dict(l=5, r=1, t=30, b=10),
        )
    st.plotly_chart(fig)

#12. Fonction pour tracer des graphiques type barre de progression
def make_multi_progress_bar(labels,values,colors,titre="",width=500,height=400):
    # Configuration
    max_blocks = 100  # Nombre total de segments
    block_size = 1  # Chaque bloc représente 1%
    space_factor = 0.1  # Espace entre les blocs (réduit à 20% de la largeur d'un bloc)

    fig = go.Figure()

    # Création des barres segmentées
    for i, (label, value, color) in enumerate(zip(labels, values, colors)):
        num_filled_blocks = int(value*100) // block_size  # Nombre de blocs colorés
        num_empty_blocks = max_blocks - num_filled_blocks  # Blocs restants

        # Blocs colorés (progression) avec espacement
        fig.add_trace(go.Bar(
            x=[block_size - space_factor] * num_filled_blocks,  # Réduction pour l'espacement
            y=[label] * num_filled_blocks,
            orientation='h',
            hoverinfo="skip",
            marker=dict(color=color),
            showlegend=False,
            width=0.5  # Réduction de la largeur des blocs
        ))

        # Blocs vides (fond) avec le même espacement
        fig.add_trace(go.Bar(
            x=[block_size - space_factor] * num_empty_blocks,
            y=[label] * num_empty_blocks,
            orientation='h',
            hoverinfo="skip",
            marker=dict(color="rgba(0, 0, 0, 0.2)"),
            showlegend=False,
            width=0.5  # Même largeur que les blocs colorés
        ))

    # Personnalisation du layout
    fig.update_layout(
        title=titre,
        barmode="stack",
        width=width,height=height,
        annotations=[dict(text= str(round(100*values[i],2))+'%', x=100*values[i], y=i,
            font_size=25, showarrow=False,xanchor='left',font=dict(color=colors[i], family="Berlin Sans FB")) for i in range(len(values))] + 
        [dict(text= labels[i], x=-1, y=i+0.5,
            font_size=20, showarrow=False,xanchor='left',font=dict(color=colors[i], family="Berlin Sans FB")) for i in range(len(values))],
        xaxis=dict(visible=False), 
        yaxis=dict(visible=False),
        margin=dict(l=50, r=20, t=20, b=20),
        paper_bgcolor='rgba(248,248,250,0)',
        plot_bgcolor='rgba(248,248,250,0)',
    )

    st.plotly_chart(fig)

#13. Fonction pour afficher un dataframe personalisé
def make_dataframe(df,col_alpha,col_num,hide_index=False):
    st.dataframe(df,
                 column_order=(col_alpha, col_num),
                 hide_index=hide_index,
                 width=None,
                 column_config={
                    col_alpha: st.column_config.TextColumn(
                        col_alpha,
                    ),
                    col_num: st.column_config.ProgressColumn(
                        col_num,
                        format="%f",
                        min_value=0,
                        max_value=float(df[col_num].max()),
                     )})

#14. Fonction pour tracer la distribution d'un variable quantitative version 1
def make_distribution(df,var_alpha,var_num,add_vline,add_vline2,titre="",width=500, height=300):
    fig = go.Figure()
    valeur=[]
    for i in list(df[var_alpha].unique()):
        df_to_print=df[df[var_alpha]==i]
        moy=float(df_to_print[var_num].mean())
        ecart=float(df_to_print[var_num].std()/4)**(1/300)
        occurrences_mode = df_to_print[(df_to_print[var_num]<=moy+ecart) & (df_to_print[var_num]>=moy-ecart)].shape[0]
        valeur=valeur+[occurrences_mode]
        fig.add_trace(go.Histogram(x=df_to_print[var_num],name=i,opacity=0.7))
        #fig.add_trace(go.Histogram(x=x1))

    # The two histograms are drawn on top of another
    fig.add_shape(
        type="line",  # Type de forme: ligne
        x0=add_vline,        # Position de départ sur l'axe x
        x1=add_vline,        # Position de fin sur l'axe x (identique pour une droite verticale)
        y0=0,         # Position de départ sur l'axe y
        y1=40,         # Position de fin sur l'axe y (selon l'échelle de ton graphique)
        line=dict(color="green", width=2)  # Style de la ligne
    )
    
    fig.add_shape(
        type="line",  # Type de forme: ligne
        x0=add_vline2,        # Position de départ sur l'axe x
        x1=add_vline2,        # Position de fin sur l'axe x (identique pour une droite verticale)
        y0=0,         # Position de départ sur l'axe y
        y1=40,         # Position de fin sur l'axe y (selon l'échelle de ton graphique)
        line=dict(color="green", width=2))
    fig.update_layout(barmode='stack',xaxis=dict(visible=True), 
        yaxis=dict(visible=True),)
    fig.update_layout(margin=dict(l=5, r=1, t=30, b=10),
                      paper_bgcolor='rgba(248,248,250,0)',
                      plot_bgcolor='rgba(248,248,250,0)',
                      width=width, height=height,
                    title=dict(
        text=titre,
        x=0.0,  
        y=0.95, 
        xanchor='left', 
        yanchor='top'),
            legend=dict(
            x=0.8,  # Position horizontale (à droite)
            y=1,  # Position verticale (en haut)
            traceorder='normal',
            xanchor='center',  # Alignement horizontal de la légende
            yanchor='top',  # Alignement vertical de la légende
            bgcolor='rgba(255,255,255,0.1)',  # Fond semi-transparent de la légende
        ))
    fig.update_xaxes(title_text=var_num)  # Titre de l'axe X
    fig.update_yaxes(title_text="Effectif")
    st.plotly_chart(fig)

#16. Fonction pour afficher un nuage de mot 
def make_wordcloud(texte,titre="",width=800, height=400):
    mot=texte.split(" ")
    mots_exclus = ["de", "à", "et"," et", "et "," de","de "," et "," de ","NON"," ","pas", "les"]
    mot = [m for m in mot if m not in mots_exclus]
    # Génération du nuage de mots
    wordcloud = WordCloud(width=width, height=height, background_color="white", colormap="viridis").generate(texte)
    # Sauvegarde de l'image en mémoire
    img = io.BytesIO()
    wordcloud.to_image().save(img, format='PNG')
    img.seek(0)
    # Convertir en tableau numpy pour Plotly
    img_array = np.array(Image.open(img))
    # Affichage avec Plotly
    fig = px.imshow(img_array)
    fig.update_layout(
        title=titre,
        margin=dict(l=1, r=1, t=30, b=10),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False)
    )
    st.plotly_chart(fig)
 
 #13. Fonction pour afficher un dataframe personalisé   

#17. Fonction pour afficher un double anneau de progression 
def make_dbl_progress_char(labels,vars,colors,titre="",n_secteur=50):
    # Données pour l'anneau externe
    labels2 = ["a"+str(i) for i in range(n_secteur)]
    sizes_2 = [1 for i in range(n_secteur)]
    labels_1= ["b"+str(i) for i in range(n_secteur + 10)]
    sizes_1 = [1 for i in range(n_secteur + 10)] 
    lab1=labels[0]
    lab2=labels[1]
    val1=vars[0]
    val2=vars[1]
    col1=colors[0]
    col2=colors[1]
    fig = go.Figure()
    # Ajout de l'anneau externe
    fig.add_trace(go.Pie(
        labels=labels2,
        values=sizes_2,
        pull=[0.1 for i in range(n_secteur)],
        hoverinfo="none",
        textinfo='none',
        hole=0.75, 
        marker=dict(colors=["rgba(0, 0, 0, 0.2)" for i in range(n_secteur-(int(n_secteur*val2)))] + [col2 for i in range(int(n_secteur*val2))]),
        domain={'x': [0.1, 0.9], 'y': [0.1, 0.9]}
    ))

    # Ajout de l'anneau interne
    fig.add_trace(go.Pie(
        labels=labels_1,
        values=sizes_1,
        pull=[0.1 for i in range(n_secteur +10)],
        hoverinfo="none",
        textinfo='none',
        hole=0.8, 
        marker=dict(colors= ["rgba(0, 0, 0, 0.2)" for i in range(n_secteur-(int((n_secteur+10)*val1)) + 10)] + [col1 for i in range(int((n_secteur+10)*val1))]),
        domain={'x': [0, 1], 'y': [0, 1]}
    ))

    # Mise en forme
    fig.update_layout(
        title=dict(text=titre,
                        x=0.1,  # Centre horizontalement
                        y=0.99,  # Légèrement en dessous du bord supérieur
                        xanchor='left', 
                        yanchor='top'),
        showlegend=False,
        margin=dict(l=0, r=0, t=40, b=10),
        paper_bgcolor='rgba(248,248,250,0)',
        plot_bgcolor='rgba(248,248,250,0)',
        annotations=[dict(text= str(round(100*val2,2))+'%', x=0.5, y=0.25,
        font_size=50, showarrow=False, xanchor="center",font=dict(color=col2, family="Berlin Sans FB")),
                    dict(text=str(round(100*val1,2))+'%', x=0.5, y=0.6,
        font_size=50, showarrow=False, xanchor="center",font=dict(color=col1, family="Berlin Sans FB")),
                    dict(text=lab1, x=0.5, y=0.75,
        font_size=30, showarrow=False, xanchor="center",font=dict(color=col1, family="Berlin Sans FB")),
                    dict(text=lab2, x=0.5, y=0.4,
        font_size=30, showarrow=False, xanchor="center",font=dict(color=col2, family="Berlin Sans FB"))]
    )

    # Affichage
    st.plotly_chart(fig)

#18. Fonction pour afficher une carte chlorophete version 1: avec plotly   
def make_chlorophet_map_2(df, style_carte="carto-positron", palet_color="Blues", opacity=0.8, width=700, height=600):
    """
    Fonction pour créer une carte choroplèthe interactive montrant la distribution des candidats
    par statut d'éligibilité à travers différents quartiers et arrondissements.
    
    Parameters:
    -----------
    df : GeoDataFrame
        DataFrame contenant les données géospatiales des candidats
    style_carte : str, default="carto-positron"
        Style de fond de carte Mapbox (options: "carto-positron", "carto-darkmatter", "open-street-map", etc.)
    palet_color : str, default="Blues"
        Palette de couleurs pour la choroplèthe (options: "Blues", "Reds", "Greens", "Viridis", etc.)
    opacity : float, default=0.8
        Opacité des polygones de la choroplèthe (0-1)
    width : int, default=900
        Largeur de la carte en pixels
    height : int, default=600
        Hauteur de la carte en pixels
    """
    # Définition des catégories d'éligibilité et des couleurs associées
    eligibility_categories = {
        "Eligible": {"color": "#0073E6", "size_factor": 27, "opacity": 0.75},
        "Temporairement Non-eligible": {"color": "#B3D9FF", "size_factor": 17, "opacity": 0.7},
        "Définitivement non-eligible": {"color": "#FF5733", "size_factor": 10, "opacity": 0.7}
    }
    
    # Préparation des données par statut d'éligibilité
    dfs_by_eligibility = {}
    for category in eligibility_categories.keys():
        geo_data = df[df["Eligibilite"] == category]
        
        if not geo_data.empty:
            dfs_by_eligibility[category] = geo_data.groupby("Quartier").agg({
                'Quartier': 'size',
                'Lat': 'first',
                'Long': 'first'
            }).rename(columns={'Quartier': 'nb_donateur'})
            dfs_by_eligibility[category]["Qrt"] = dfs_by_eligibility[category].index

    # Préparation des données pour la choroplèthe par arrondissement
    df_chlph = df.groupby("Arrondissement").agg({
        'Arrondissement': 'size',
        'geometry': 'first',
        'Long': 'first',
        'Lat': 'first'
    }).rename(columns={'Arrondissement': 'nb_donateur'})
    df_chlph["Arr"] = df_chlph.index
    df_chlph = gpd.GeoDataFrame(df_chlph, geometry='geometry')

    # Total des candidats par quartier
    df_pts = df.groupby("Quartier").agg({
        'Quartier': 'size',
        'Lat': 'first',
        'Long': 'first'
    }).rename(columns={'Quartier': 'nb_donateur'})
    df_pts["Qrt"] = df_pts.index
    
    # Création de la figure
    fig = go.Figure()
    
    # Ajout de la couche choroplèthe pour les arrondissements
    fig.add_trace(go.Choroplethmapbox(
        geojson=df_chlph.geometry.__geo_interface__,
        locations=df_chlph.index,
        z=df_chlph["nb_donateur"],
        colorscale=palet_color,
        marker_opacity=opacity,
        marker_line_width=0.5,
        marker_line_color='white',  # Bordure blanche pour meilleure délimitation
        colorbar=dict(
            title="Nombre de Candidats",
            thickness=15,
            len=0.7,
            x=0.95,
            y=0.5,
        ),
        hovertext=df_chlph['Arr'],
        hovertemplate="<b>%{hovertext}</b><br>Nombre de candidats: %{z}<extra></extra>",
        name="Arrondissements",
    ))
    
    # Ajout des étiquettes d'arrondissement
    fig.add_trace(go.Scattermapbox(
        lat=df_chlph["Lat"],
        lon=df_chlph["Long"],
        mode='text',
        text=df_chlph["Arr"],
        textfont=dict(
            size=12,
            color="black",
            family="Arial Bold"
        ),
        hoverinfo='none',
        name="Labels"
    ))

    # Ajout des marqueurs pour le total des candidats
    fig.add_trace(go.Scattermapbox(
        lat=df_pts["Lat"],
        lon=df_pts["Long"],
        mode='markers',
        name="Total candidats",
        marker=dict(
            size=df_pts["nb_donateur"],
            sizemode='area',
            sizeref=2. * max(df_pts["nb_donateur"]) / (45.**2),
            color='#003F80',
            opacity=0.8
            # Suppression de line=dict(width=1, color='white') qui n'est pas supporté
        ),
        hovertemplate=(
            "<b>%{text}</b><br>"
            "Total candidats: <b>%{marker.size}</b><extra></extra>"
        ),
        text=df_pts["Qrt"]
    ))
    
    # Ajout des marqueurs pour chaque catégorie d'éligibilité
    for category, df_pts_cat in dfs_by_eligibility.items():
        config = eligibility_categories[category]
        fig.add_trace(go.Scattermapbox(
            lat=df_pts_cat["Lat"],
            lon=df_pts_cat["Long"],
            mode='markers',
            name=category,
            marker=dict(
                size=df_pts_cat["nb_donateur"],
                sizemode='area',
                sizeref=2. * max(df_pts_cat["nb_donateur"]) / (config["size_factor"]**2),
                color=config["color"],
                opacity=config["opacity"]
                # Suppression de line=dict(width=1, color='white') qui n'est pas supporté
            ),
            hovertemplate=(
                "<b>%{text}</b><br>"
                f"Candidats {category}: <b>%{{marker.size}}</b><extra></extra>"
            ),
            text=df_pts_cat["Qrt"]
        ))
    
    # Optimisation de la mise en page
    fig.update_layout(
        title=dict(
            text="Distribution des Candidats par Éligibilité",
            font=dict(size=20, family="Arial", color="#333"),
            x=0.5,
            y=0.98
        ),
        showlegend=True,
        legend=dict(
            x=0.01,
            y=0.01,
            bgcolor="rgba(255, 255, 255, 0.2)",
            bordercolor="#ddd",
            borderwidth=1,
            orientation='v',
            itemsizing='constant',
            font=dict(family="Arial", size=12,color="black")
        ),
        mapbox=dict(
            style=style_carte,
            center=dict(lat=df_pts["Lat"].mean(), lon=df_pts["Long"].mean()),
            zoom=10.5,
            accesstoken=None  # À définir si vous utilisez un token Mapbox
        ),
        margin=dict(l=1, r=1, t=10, b=1),
        width=width,
        height=height,
        paper_bgcolor='white',
        autosize=True,
    )

    # Affichage avec Streamlit
    st.plotly_chart(fig, use_container_width=True)

#19. Fonction pour afficher une carte chlorophete version 2: avec folium
def make_chlorophet_map_folium_2(df, style_carte="OpenStreetMap", palet_color="blues", opacity=0.8, width=700, height=600):
    """
    Fonction pour créer une carte choroplèthe interactive montrant la distribution des candidats
    par statut d'éligibilité à travers différents quartiers et arrondissements, en utilisant Folium.
    
    Parameters:
    -----------
    df : GeoDataFrame
        DataFrame contenant les données géospatiales des candidats
    style_carte : str, default="OpenStreetMap"
        Style de fond de carte Folium (options: "OpenStreetMap", "cartodbpositron", "cartodbdark_matter", etc.)
    palet_color : str, default="Blues"
        Palette de couleurs pour la choroplèthe (options: "Blues", "Reds", "Greens", "YlOrRd", etc.)
    opacity : float, default=0.8
        Opacité des polygones de la choroplèthe (0-1)
    width : int, default=700
        Largeur de la carte en pixels
    height : int, default=600
        Hauteur de la carte en pixels
    """
    
    
    # Nettoyer les données en supprimant les lignes avec des coordonnées NaN
    df_clean = df.dropna(subset=['Lat', 'Long']).copy()
    
    # Définition des catégories d'éligibilité et des couleurs associées
    eligibility_categories = {
        "Eligible": {"color": "#0073E6", "size_factor": 12, "opacity": 0.75},
        "Temporairement Non-eligible": {"color": "#B3D9FF", "size_factor": 8, "opacity": 0.7},
        "Définitivement non-eligible": {"color": "#FF5733", "size_factor": 4, "opacity": 0.7}
    }
    
    # Préparation des données par statut d'éligibilité
    dfs_by_eligibility = {}
    for category in eligibility_categories.keys():
        geo_data = df_clean[df_clean["Eligibilite"] == category]
        
        if not geo_data.empty:
            dfs_by_eligibility[category] = geo_data.groupby("Quartier").agg({
                'Quartier': 'size',
                'Lat': 'first',
                'Long': 'first'
            }).rename(columns={'Quartier': 'nb_donateur'})
            dfs_by_eligibility[category]["Qrt"] = dfs_by_eligibility[category].index
            # S'assurer qu'il n'y a pas de NaN dans les coordonnées agrégées
            dfs_by_eligibility[category] = dfs_by_eligibility[category].dropna(subset=['Lat', 'Long'])

    # Préparation des données pour la choroplèthe par arrondissement
    df_chlph = df_clean.groupby("Arrondissement").agg({
        'Arrondissement': 'size',
        'geometry': 'first',
        'Long': 'first',
        'Lat': 'first'
    }).rename(columns={'Arrondissement': 'nb_donateur'})
    df_chlph["Arr"] = df_chlph.index
    # S'assurer qu'il n'y a pas de NaN dans les coordonnées agrégées
    df_chlph = df_chlph.dropna(subset=['Lat', 'Long'])
    df_chlph = gpd.GeoDataFrame(df_chlph, geometry='geometry')
    
    # S'assurer que le CRS est défini - Utiliser EPSG:4326 (WGS84) pour compatibilité avec Folium
    if df_chlph.crs is None:
        df_chlph.set_crs(epsg=4326, inplace=True)
    else:
        # Si un CRS est déjà défini mais différent de WGS84, le convertir
        if df_chlph.crs != 'EPSG:4326':
            df_chlph = df_chlph.to_crs(epsg=4326)

    # Total des candidats par quartier
    df_pts = df_clean.groupby("Quartier").agg({
        'Quartier': 'size',
        'Lat': 'first',
        'Long': 'first'
    }).rename(columns={'Quartier': 'nb_donateur'})
    df_pts["Qrt"] = df_pts.index
    # S'assurer qu'il n'y a pas de NaN dans les coordonnées agrégées
    df_pts = df_pts.dropna(subset=['Lat', 'Long'])
    
    # Vérifier si df_pts est vide après filtrage
    if df_pts.empty:
        st.error("Aucune coordonnée valide trouvée dans les données. Impossible de créer la carte.")
        return None
    
    # Création de la carte Folium
    center_lat = df_pts["Lat"].mean()
    center_lon = df_pts["Long"].mean()
    
    # Dictionnaire de correspondance entre les styles dans votre fonction originale et ceux de Folium
    tile_styles = {
        "carto-positron": "cartodbpositron",
        "carto-darkmatter": "cartodbdark_matter",
        "open-street-map": "OpenStreetMap",
        "CartoDB positron": "cartodbpositron", 
        "CartoDB dark_matter": "cartodbdark_matter"
    }
    
    # Utiliser le style approprié ou OpenStreetMap par défaut
    actual_style = tile_styles.get(style_carte, style_carte)
    
    # Création de la carte avec le style approprié
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=12,
        tiles=actual_style,
        width=width,
        height=height
    )
    
    # Ajout de la couche choroplèthe pour les arrondissements
    # Création d'une échelle de couleur avec la bonne classe de branca.colormap
    if palet_color == "blues":
        color_range = ['#f7fbff', '#08519c']
    elif palet_color == "reds":
        color_range = ['#fee5d9', '#a50f15']
    elif palet_color == "greens":
        color_range = ['#edf8e9', '#006d2c']
    elif palet_color == "viridis":
        color_range = ['#fde725', '#440154']
    else:
        color_range = ['#f7fbff', '#08519c']  # Default to Blues
    
    # Création des clusters uniquement pour les arrondissements
    arrondissement_cluster = MarkerCluster(name="Arrondissements").add_to(m)
    
    if not df_chlph.empty:
        colormap = cm.LinearColormap(
            colors=color_range, 
            vmin=df_chlph["nb_donateur"].min(),
            vmax=df_chlph["nb_donateur"].max(),
            caption="Nombre de Candidats par Arrondissement"
        )
        
        # Convertir le GeoDataFrame en GeoJSON
        geo_json_data = df_chlph.__geo_interface__
        
        # Ajout des polygones des arrondissements en utilisant le GeoJSON préparé
        folium.GeoJson(
            geo_json_data,
            style_function=lambda feature: {
                'fillColor': colormap(feature['properties']['nb_donateur']),
                'color': 'white',
                'weight': 0.5,
                'fillOpacity': opacity
            },
            tooltip=folium.GeoJsonTooltip(
                fields=['Arr', 'nb_donateur'],
                aliases=['Arrondissement:', 'Nombre de candidats:'],
                style="background-color: white; color: #333333; font-family: arial; font-size: 14px; padding: 10px;"
            )
        ).add_to(m)
        
        # Ajout des étiquettes d'arrondissement et des marqueurs au cluster d'arrondissements
        for idx, row in df_chlph.iterrows():
            # Étiquettes d'arrondissement
            folium.Marker(
                location=[row['Lat'], row['Long']],
                icon=folium.DivIcon(
                    icon_size=(150, 40),
                    icon_anchor=(75, 28),
                    html=f'<div style="font-size: 12px; font-weight: bold; text-align: center">{row["Arr"]}</div>'
                )
            ).add_to(m)
            
            # Marqueurs d'arrondissement pour le cluster
            folium.Marker(
                location=[row['Lat'], row['Long']],
                popup=f"<b>Arrondissement {row['Arr']}</b><br>Total candidats: <b>{row['nb_donateur']}</b>",
                icon=folium.Icon(color='blue')
            ).add_to(arrondissement_cluster)
        
        # Ajout de la légende de couleur
        colormap.add_to(m)

    # Fonction pour calculer la taille du cercle en fonction du nombre de candidats
    def calculate_radius(count, max_count, base_size=5):
        return base_size * np.sqrt(count / max_count * 100)
    
    max_count = df_pts["nb_donateur"].max() if not df_pts.empty else 1
    
    # Création d'un groupe de features pour les cercles des quartiers
    quartier_feature_group = folium.FeatureGroup(name="Total candidats par quartier")
    
    # Ajout des marqueurs pour le total des candidats (directement à la carte, pas de cluster)
    for idx, row in df_pts.iterrows():
        radius = calculate_radius(row["nb_donateur"], max_count)
        popup_text = f"<b>{row['Qrt']}</b><br>Total candidats: <b>{row['nb_donateur']}</b>"
        
        folium.CircleMarker(
            location=[row['Lat'], row['Long']],
            radius=radius,
            color='#003F80',
            fill=True,
            fill_color='#003F80',
            fill_opacity=0.8,
            popup=folium.Popup(popup_text, max_width=300)
        ).add_to(quartier_feature_group)
    
    # Ajout du groupe de features à la carte
    quartier_feature_group.add_to(m)
        
    # Ajout des marqueurs pour chaque catégorie d'éligibilité (directement à la carte, pas de cluster)
    for category, df_pts_cat in dfs_by_eligibility.items():
        if df_pts_cat.empty:
            continue
            
        config = eligibility_categories[category]
        
        # Création d'un groupe de features pour cette catégorie
        category_feature_group = folium.FeatureGroup(name=category)
        
        max_count_cat = df_pts_cat["nb_donateur"].max() if not df_pts_cat.empty else 1
        
        for idx, row in df_pts_cat.iterrows():
            radius = calculate_radius(row["nb_donateur"], max_count_cat, base_size=config["size_factor"]/4)
            popup_text = f"<b>{row['Qrt']}</b><br>Candidats {category}: <b>{row['nb_donateur']}</b>"
            
            folium.CircleMarker(
                location=[row['Lat'], row['Long']],
                radius=radius,
                color=config["color"],
                fill=True,
                fill_color=config["color"],
                fill_opacity=config["opacity"],
                popup=folium.Popup(popup_text, max_width=300)
            ).add_to(category_feature_group)
        
        # Ajout du groupe de features à la carte
        category_feature_group.add_to(m)
            
    # Ajout du contrôle de couches
    folium.LayerControl(collapsed=False).add_to(m)
    
    # Ajout d'une légende pour les cercles des points
    legend_html = '''
        <div style="position: fixed; 
                    bottom: 50px; right: 50px; 
                    width: 220px;
                    background-color: white;
                    border: 2px solid grey;
                    border-radius: 5px;
                    z-index: 9999;
                    font-size: 14px;
                    padding: 10px;
                    opacity: 0.9;">
            <div style="text-align: center; margin-bottom: 5px;"><b>Légende des points</b></div>
    '''
    
    # Ajouter une entrée de légende pour les cercles totaux
    legend_html += f'''
        <div style="margin-bottom: 7px;">
            <div style="display: inline-block; 
                      width: 15px; 
                      height: 15px; 
                      border-radius: 50%; 
                      background-color: #003F80;
                      margin-right: 5px;
                      vertical-align: middle;"></div>
            <span style="vertical-align: middle;">Total candidats</span>
        </div>
    '''
    
    # Ajouter des entrées pour chaque catégorie d'éligibilité
    for category, config in eligibility_categories.items():
        if category in dfs_by_eligibility and not dfs_by_eligibility[category].empty:
            legend_html += f'''
                <div style="margin-bottom: 7px;">
                    <div style="display: inline-block; 
                              width: 15px; 
                              height: 15px; 
                              border-radius: 50%; 
                              background-color: {config['color']};
                              opacity: {config['opacity']};
                              margin-right: 5px;
                              vertical-align: middle;"></div>
                    <span style="vertical-align: middle;">{category}</span>
                </div>
            '''
    
    # Fermer la div de la légende
    legend_html += '</div>'
    
    # Ajouter la légende à la carte
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Ajout d'un titre 
    title_html = '''
        <div style="position: fixed; 
                    top: 10px; left: 50px; width: 600px; height: 45px; 
                    background-color: white; border-radius: 5px;
                    z-index: 9999; font-size: 20px; font-family: Arial;
                    padding: 10px; text-align: center; color: #333;">
            <b>Distribution des Candidats par Éligibilité</b>
        </div>
    '''
    m.get_root().html.add_child(folium.Element(title_html))
    
    # Affichage avec Streamlit
    folium_static(m, width=width, height=height)
    
    return m

#20. Fonction pour afficher histogramme croisé version 4
def make_cross_hist_b(df, var1, var2, titre="", typ_bar=1, width=800, height=500, sens="v", 
                    palette=None, show_legend=True,bordure=None):
    """
    Crée un histogramme croisé optimisé pour les données de campagne de don de sang.
    
    Args:
        df: DataFrame contenant les données
        var1: Variable pour grouper (apparaîtra dans la légende)
        var2: Variable pour l'axe des x/y selon l'orientation
        titre: Titre du graphique
        typ_bar: 1 pour empilé, 2 pour groupé
        width: Largeur du graphique
        height: Hauteur du graphique
        sens: Orientation - "v" (vertical) ou "h" (horizontal)
        palette: Liste de couleurs personnalisée (si None, utilise la palette de don de sang par défaut)
        show_legend: Afficher ou masquer la légende
        bordure: pour les bordure
        
    Returns:
        Affiche le graphique dans Streamlit
    """
    # Définition des couleurs pour le thème don de sang si non spécifiées
    if palette is None:
        # Palette de couleurs orientée sang (rouge) et médical (bleu) #FDC7D3,
        palette = ['#FDC7D3', '#F61A49', '#640419', '#49030D', '#4575B4', '#74ADD1', '#ABD9E9', '#E0F3F8']  # nuances de bleu
    
    bar_mode = "relative" if typ_bar == 1 else "group"
    
    # Création du tableau croisé et formatage
    cross_df = pd.crosstab(df[var1], df[var2])
    table_cross = cross_df.reset_index().melt(id_vars=var1, var_name=var2, value_name='Effectif')
    table_cross = table_cross.sort_values("Effectif", ascending=False)
    
    # Déterminer les axes selon l'orientation
    x_axis = var2 if sens == "v" else 'Effectif'
    y_axis = var1 if sens == "h" else 'Effectif'
    
    # Création du graphique avec une meilleure disposition
    fig = px.bar(table_cross, 
                 x=x_axis, 
                 y=y_axis, 
                 color=var1, 
                 text_auto=True,  # Affiche automatiquement les valeurs
                 barmode=bar_mode,
                 orientation=sens,
                 color_discrete_sequence=palette
                 )
                 
    # Améliorations stylistiques
    fig.update_layout(barcornerradius=bordure,
        width=width, 
        height=height,
        paper_bgcolor='rgba(248,248,250,0)',  # Fond légèrement grisé pour le graphique
        plot_bgcolor='rgba(248,248,250,0)',   # Fond légèrement grisé pour les axes
        title={
            'text': f"<b>{titre}</b>",
            'x': 0.5,  # Centrer le titre
            'y': 1,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 22, 'family': 'Arial, sans-serif'}
        },
        margin=dict(l=1, r=5, t=20, b=5),  # Marges plus généreuses
        legend={
            #'title': var1,
            'orientation': 'h',              # Légende horizontale
            'y': 0.9,                      # Position sous le graphique
            'x': 0.8,
            'xanchor': 'center',
            'yanchor': 'top',
            'bgcolor': 'rgba(255,255,255,0)',
            'bordercolor': 'rgba(0,0,0,0)',
            'borderwidth': 1,
            'font': police_label
        } if show_legend else None
    )
    
    # Amélioration des axes et des annotations
    fig.update_xaxes(
        showgrid=True,
        gridwidth=0.5,
        gridcolor='rgba(211,211,211,0)',
        title_font=police_label,
        tickfont=police_label
    )
    
    fig.update_yaxes(
        showgrid=True,
        gridwidth=0.5,
        gridcolor='rgba(211,211,211,0)',
        title_font={'size': 14},
        tickfont=police_label
    )
    
    # Amélioration des barres et du texte
    fig.update_traces(
        textfont_size=20,
        textposition='auto',
        marker_line_width=0.5,
        marker_line_color='rgba(0,0,0,0.3)',
    )
    
    # Affichage dans Streamlit
    st.plotly_chart(fig, use_container_width=True)

#21. Fonction pour afficher un heatmap version 2
def make_heat_map_2(df, vars, order_var, label_var, titre="", width=500, height=300, 
                   color_scale=None, show_titles=True, text_size=12):
    """
    Crée un diagramme en cascade (icicle chart) optimisé pour visualiser les données
    hiérarchiques de campagne de don de sang.
    
    Args:
        df: DataFrame contenant les données
        vars: Liste des variables pour la hiérarchie
        order_var: Variable à utiliser pour calculer les effectifs
        label_var: Variable à afficher dans les info-bulles
        titre: Titre du graphique
        width: Largeur du graphique
        height: Hauteur du graphique
        color_scale: Échelle de couleurs personnalisée (si None, utilise une échelle du bleu au rouge)
        show_titles: Afficher les titres des axes
        text_size: Taille du texte dans les segments
        
    Returns:
        Affiche le graphique dans Streamlit
    """
    # Création du dataframe agrégé pour le graphique
    data_mp = df.groupby(vars).agg({
        order_var: 'size',
    }).reset_index()
    data_mp = data_mp.rename(columns={order_var: 'Effectif'})
    
    # Ajout d'une colonne de pourcentage pour l'affichage
    total = data_mp['Effectif'].sum()
    data_mp['Pourcentage'] = (data_mp['Effectif'] / total * 100).round(1)
    
    # Définir une échelle de couleurs allant du bleu au rouge foncé si non spécifiée
    if color_scale is None:
        # Du bleu clair au rouge foncé
        color_scale = ["#EFF3FF", "#C6DBEF", "#9ECAE1", "#6BAED6", "#4292C6", "#2171B5", 
                       "#FEE0D2", "#FCBBA1", "#FC9272", "#FB6A4A", "#EF3B2C", "#CB181D", "#A50F15", "#67000D"]
    
    # Créer le chemin hiérarchique avec 'All' comme racine
    path_vars = [px.Constant('Tous les donneurs')] + vars
    # Création du graphique avec des paramètres améliorés
    fig = px.icicle(
        data_mp, 
        path=path_vars, 
        values='Effectif',
        color='Effectif', 
        hover_data=['Pourcentage', label_var],
        color_continuous_scale=color_scale,
        branchvalues='total'  # S'assure que les valeurs sont correctement agrégées
    )
    
    # Amélioration de l'apparence des segments
    fig.update_traces(
        textinfo="label+value",         # Affiche le nom du segment et sa valeur
        texttemplate='%{label}<br>%{value} donneurs',  # Format personnalisé
        textposition="middle center",   # Position du texte au centre des segments
        insidetextfont=dict(
            color='black',              # Couleur de texte de base
            size=text_size,             # Taille du texte ajustable
            family="Arial, sans-serif"  # Police plus moderne
        ),
        outsidetextfont=dict(
            color='black',
            size=text_size,
            family="Arial, sans-serif"
        ),
        marker=dict(
            line=dict(width=1, color='rgba(255,255,255,0)')  # Bordure fine pour distinguer les segments
        ),
        hovertemplate='<b>%{label}</b><br>Effectif: %{value} donneurs<br>Pourcentage: %{customdata[0]}%<br>%{customdata[1]}<extra></extra>'
    )
    
    # Amélioration de la mise en page générale
    fig.update_layout(
        title={
            'text': f"<b>{titre}</b>" if titre else "",
            'x': 0.5,
            'y': 1,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 20,  'family': 'Arial, sans-serif'}
        },
        width=width, 
        height=height,
        margin=dict(l=2, r=2, t=8, b=2),
        paper_bgcolor='rgba(248,248,250,0)',  # Fond légèrement grisé
        coloraxis_colorbar=dict(
            title={
                'text': "Nombre de<br>donneurs",
                'font': police_label
            },
            tickfont=police_label,
            len=0.6,                  # Longueur de la barre de couleur
            thickness=15,             # Épaisseur de la barre de couleur
            x=0.95                    # Position horizontale
        )
    )
    
    # Ajuster le texte en fonction des valeurs
    # Les petits segments auront un texte blanc pour contraster avec les couleurs foncées
    for i in range(len(fig.data)):
        # Vérification corrigée pour éviter l'erreur de valeur de vérité ambiguë
        has_values = hasattr(fig.data[i], 'values')
        has_labels = hasattr(fig.data[i], 'labels')
        
        if has_values and has_labels:
            values = fig.data[i].values
            
            # Assurez-vous que values est non vide avant de continuer
            if len(values) > 0:
                text_colors = []
                for val in values:
                    # Pour les segments plus petits, utiliser du blanc pour le contraste
                    if val < total * 0.05:  # Seuil de 5% du total
                        text_colors.append('white')
                    else:
                        text_colors.append('black')
                
                fig.data[i].insidetextfont.color = text_colors
    
    # Affichage dans Streamlit
    st.plotly_chart(fig, use_container_width=True)
    
    return fig  # Retourne le graphique pour référence ultérieure

#22. Fonction pour afficher un anneau
def make_donutchart(df, var, titre="", width=600, height=450, color_palette=None,part=True):
    """
    Crée un graphique en anneau (donut chart) avec des améliorations visuelles.
    
    Args:
        df: DataFrame contenant les données
        var: Variable à visualiser
        titre: Titre du graphique
        width: Largeur du graphique
        height: Hauteur du graphique
        color_palette: Liste de couleurs personnalisées pour le graphique
        
    Returns:
        Affiche le graphique dans Streamlit
    """
    # Agrégation des données
    data_grouped = df.groupby(var).size().reset_index(name='Effectif')
    
    # Calculer les pourcentages pour l'affichage dans les étiquettes
    total = data_grouped['Effectif'].sum()
    data_grouped['Pourcentage'] = (data_grouped['Effectif'] / total * 100).round(1)
    
    # Trier par effectif décroissant pour une meilleure présentation
    data_grouped = data_grouped.sort_values('Effectif', ascending=False)
    
    
    # Construction du graphique
    fig = go.Figure()
    
    # Ajout du graphique en anneau
    fig.add_trace(go.Pie(
        labels=data_grouped[var], 
        values=data_grouped['Effectif'],
        textinfo='label+percent',
        textposition='inside',
        texttemplate='%{label}<br>%{percent}',
        hovertemplate='<b>%{label}</b><br>Effectif: %{value} (%{percent})<extra></extra>',
        hole=0.5,
        pull=[0.03 if (i == 0) & (len(data_grouped)>2)  else 0 for i in range(len(data_grouped))],  # Léger détachement du plus grand segment
        marker=dict(
            colors=palette,
            #line=dict(color='white', width=2)
        ),
        rotation=0,  # Rotation pour un meilleur positionnement des étiquettes
        sort=False  ,  # Respecter l'ordre du tri effectué
        textfont=police_label
        
    ))
    
    # Ajout du nombre total au centre du donut
    fig.add_annotation(
        text=f"{total:,}<br>Total",
        x=0.5, y=0.5,
        font=police,
        showarrow=False
    )
    
    # Optimisation de la mise en page
    fig.update_layout(
        title={
            'text': f"<b>{titre}</b>" if titre else "",
            'x': 0.5,
            'y': 1,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=18)
        },
        width=width,
        height=height,
        margin=dict(l=3, r=3, t=12, b=2),
        paper_bgcolor='rgba(248,248,250,0)',  # Fond légèrement grisé
        legend=dict(
            orientation='h',           # Disposition horizontale
            yanchor='bottom',
            y=-0.15,                   # Position sous le graphique
            xanchor='center',
            x=0.5,                     # Centré
            font=dict(size=16),
            bgcolor='rgba(255,255,255,0)',
            bordercolor='rgba(0,0,0,0)',
            borderwidth=1
        ),
        uniformtext=dict(
            minsize=15,
            #mode='hide'                # Cache le texte s'il est trop petit pour s'adapter
        )
    )
    
    # Affichage dans Streamlit avec option de largeur adaptative
    st.plotly_chart(fig, use_container_width=True)
    
    return fig  # Retourne le graphique pour référence ultérieure

#23. Fonction pour afficher un diagpramme barre simple
def make_bar(df, var, color=1, titre="", titre_x="", titre_y="", width=500, height=300, ordre=2, sens='v',bordure=None):
    """
    Crée un graphique à barres amélioré avec un style professionnel.
    
    Args:
        df: DataFrame contenant les données
        var: Variable à regrouper
        color: Couleur(s) pour les barres
        titre: Titre du graphique
        titre_x: Titre de l'axe X
        titre_y: Titre de l'axe Y
        width: Largeur du graphique
        height: Hauteur du graphique
        ordre: Tri (1=ascendant, 2=aucun, autre=descendant)
        sens: Orientation - "v" (vertical) ou "h" (horizontal)
    """
    # Agrégation des données
    data_plot = df.groupby(var).agg({"ID": "size"})
    # Tri selon le paramètre ordre
    data_plot=data_plot.rename(columns={"ID":"Effectif"})
    if ordre != 2:
        data_plot = data_plot.sort_values("Effectif", ascending=(ordre == 1))
    # Définition des axes selon l'orientation
    x_axis = data_plot.index if sens == 'v' else "Effectif"
    y_axis = "Effectif" if sens == 'v' else data_plot.index
    
    # Création du graphique
    fig = px.bar(
        data_plot, 
        x=x_axis, 
        y=y_axis, 
        text="Effectif",
        color_discrete_sequence=val_couleur[color],
        orientation=sens,
        
    )
    # Configuration des étiquettes de texte
    fig.update_traces(
        texttemplate='%{text}',
        textposition='outside',
        textfont=police_label,
        marker_line_width=0.5,
        marker_line_color='rgba(0, 0, 0, 0)',
    )
    # Mise en page améliorée
    fig.update_layout(barcornerradius=bordure,
        title={
            'text': f"<b>{titre}</b>" if titre else "",
            'x': 0.5,
            'y': 0.95,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': police_label
        },
        width=width,
        height=height,
        margin=dict(l=10, r=10, t=50, b=10 if sens == 'v' else 80),
        paper_bgcolor='rgba(248, 248, 250, 0)',
        plot_bgcolor='rgba(248, 248, 250, 0)',
        xaxis=dict(
            title=dict(
                text=titre_x,
                font=police_label
            ),
            showgrid=True,
            gridwidth=0.5,
            gridcolor='rgba(211, 211, 211, 0)',
            tickfont=police_label
        ),
        yaxis=dict(
            title=dict(
                text=titre_y,
                font=police_label
            ),
            showgrid=True,
            gridwidth=0.5,
            gridcolor='rgba(211, 211, 211, 0)',
            tickfont=police_label
        )
    )
    
    # Ajout d'une bordure légère et d'un effet d'ombre pour chaque barre
    if sens == 'v':
        fig.update_layout(
            bargap=0.15,  # Espacement entre les barres
            bargroupgap=0.1  # Espacement entre les groupes de barres
        )
    st.plotly_chart(fig, use_container_width=True)

#24. Fonction pour afficher une courbe de surface
def make_area_chart(df,var,titre="",color=1,width=500,height=300):
    df_rempl=df.groupby(var).agg({ "ID":'size'})
    df_rempl=df_rempl.rename(columns={"ID":"Effectif"})
    fig=px.area(df_rempl,x=df_rempl.index,y="Effectif",color_discrete_sequence=val_couleur[color])
    fig.update_layout(width=width, height=height,
                    title=dict(
        text=titre,
        x=0.0,  # Centre horizontalement
        y=0.95,  # Légèrement en dessous du bord supérieur
        xanchor='left', 
        yanchor='top'),)
    fig.update_layout(
        title=titre,
        paper_bgcolor='rgba(248,248,250,0)',
        plot_bgcolor='rgba(248,248,250,0)',
        margin=dict(l=5, r=1, t=30, b=10),
        legend=dict(
            x=0.8,  # Position horizontale (à droite)
            y=1,  # Position verticale (en haut)
            traceorder='normal',
            xanchor='center',  # Alignement horizontal de la légende
            yanchor='top',  # Alignement vertical de la légende
            bgcolor='rgba(255,255,255,0.1)',  # Fond semi-transparent de la légende
        )
    )
    st.plotly_chart(fig) 

#26. Fonction pour afficher histogramme amplilé à barres relatif      
def make_relative_bar(df, var1, var2, titre="", colors=None, width=650, height=400, 
                     show_values=True, round_digits=1):
    """
    Crée un graphique à barres empilées représentant des proportions relatives.
    
    Args:
        df: DataFrame contenant les données
        var1: Variable pour l'axe X
        var2: Variable pour la couleur/catégorie
        titre: Titre du graphique
        colors: Liste de couleurs (utilise Plotly Vivid par défaut)
        width: Largeur du graphique
        height: Hauteur du graphique
        show_values: Afficher les valeurs sur les barres
        round_digits: Nombre de décimales pour les pourcentages
    """
    
    # Utiliser les couleurs Vivid de Plotly par défaut si aucune couleur n'est spécifiée
    if colors is None:
        colors = palette
    
    # Calculer les proportions relatives
    cross_tab = pd.crosstab(df[var1], df[var2])  
    cross_tab_pct = cross_tab.div(cross_tab.sum(axis=1), axis=0) * 100 
    data_long = cross_tab_pct.reset_index().melt(id_vars=var1, var_name=var2, value_name='Pourcentage')
    
    # Créer le graphique
    fig = px.bar(
        data_long,
        x=var1,
        y='Pourcentage',
        color=var2,
        title=titre,
        labels={'Pourcentage': 'Proportion (%)', var1: var1, var2: var2},
        barmode='stack',
        text='Pourcentage' if show_values else None,
        color_discrete_sequence=colors
    )
    
    # Optimiser l'apparence
    fig.update_traces(
        texttemplate=f'%{{text:.{round_digits}f}}%', 
        textposition='inside',
        textfont=dict(size=25)
    )
    
    fig.update_layout(
        width=width, 
        height=height,
        yaxis=dict(visible=False),
        title=dict(
            text=titre,
            x=0.5,  # Centrer le titre
            xanchor='center',
            font=dict(size=20)
        ),
        margin=dict(l=10, r=5, t=20, b=40),
        paper_bgcolor='rgba(248,248,250,0)',
        plot_bgcolor='rgba(248,248,250,0)',
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.25,
            xanchor='center',
            x=0.1
        )
    )
    
    # Afficher le graphique
    st.plotly_chart(fig, use_container_width=True)
    
    return fig  # Retourner la figure pour utilisation possible ailleurs

def Make_Global_DataFrame(df, title="", height=None, pagination=True, filters=True, width="100%", search=True, sort=True, selection=False, hide_columns=None, column_config=None, download=False, download_filename="data.csv", cle="key1"):
    """
    Affiche un DataFrame de façon stylée avec des options de filtrage, tri, pagination et téléchargement.
    
    Args:
        df: DataFrame pandas à afficher
        title: Titre à afficher au-dessus du tableau (optionnel)
        height: Hauteur du tableau en pixels (None = automatique)
        pagination: Activer la pagination (True par défaut)
        filters: Activer les filtres par colonne (True par défaut)
        width: Largeur du tableau ("100%" par défaut)
        search: Activer la recherche globale (True par défaut)
        sort: Activer le tri des colonnes (True par défaut)
        selection: Activer la sélection de lignes (False par défaut)
        hide_columns: Liste des colonnes à masquer (None par défaut)
        column_config: Configuration personnalisée des colonnes (dictionnaire)
        download: Activer l'option de téléchargement (False par défaut)
        download_filename: Nom du fichier à télécharger ("data.csv" par défaut)
        
    Returns:
        En mode sélection, retourne les données sélectionnées, sinon None
    """

    # Vérifier si le DataFrame est vide
    if df.empty:
        st.warning("Le DataFrame est vide.")
        return None
    
    # Afficher le titre si fourni
    if title:
        st.subheader(title)
    
    # Créer une copie du DataFrame pour éviter de modifier l'original
    df_display = df.copy()
    
    # Masquer les colonnes spécifiées
    if hide_columns:
        df_display = df_display.drop(columns=[col for col in hide_columns if col in df_display.columns])
    
    # Section de filtrage manuel (avant le tableau)
    if filters:
        with st.expander("Filtres avancés", expanded=False):
            cols = st.columns(min(3, len(df_display.columns)))
            filter_conditions = []
            
            for i, column in enumerate(df_display.columns):
                col_idx = i % 3
                with cols[col_idx]:
                    # Adapter le type de filtre en fonction du type de données
                    if pd.api.types.is_numeric_dtype(df_display[column]):
                        min_val, max_val = float(df_display[column].min()), float(df_display[column].max())
                        if min_val != max_val:
                            filter_val = st.slider(f"Filtrer par {column}", min_val, max_val, (min_val, max_val),key=random.randint(1, 1000000))
                            if filter_val != (min_val, max_val):
                                filter_conditions.append(f"{filter_val[0]} <= `{column}` <= {filter_val[1]}")
                    elif pd.api.types.is_datetime64_any_dtype(df_display[column]):
                        min_date, max_date = df_display[column].min(), df_display[column].max()
                        if min_date != max_date:
                            filter_date = st.date_input(f"Filtrer par {column}", (min_date, max_date),key=random.randint(1, 1000000))
                            if len(filter_date) == 2 and (filter_date[0] != min_date or filter_date[1] != max_date):
                                filter_conditions.append(f"`{column}` >= '{filter_date[0]}' and `{column}` <= '{filter_date[1]}'")
                    else:
                        # Pour les colonnes textuelles ou catégorielles
                        unique_values = df_display[column].dropna().unique()
                        if len(unique_values) < 20:  # Utiliser une liste déroulante si peu de valeurs
                            selected_values = st.multiselect(f"Filtrer par {column}", unique_values, key=random.randint(1, 1000000))
                            if selected_values:
                                filter_conditions.append(f"`{column}` in {selected_values}")
                        else:  # Utiliser un champ texte pour beaucoup de valeurs
                            filter_text = st.text_input(f"Chercher dans {column}",key=random.randint(1, 1000000))
                            if filter_text:
                                filter_conditions.append(f"`{column}`.str.contains('{filter_text}', case=False, na=False)")
            
            # Appliquer les filtres
            if filter_conditions:
                combined_filter = " and ".join(filter_conditions)
                try:
                    df_display = df_display.query(combined_filter)
                    st.info(f"{len(df_display)} lignes après filtrage")
                except Exception as e:
                    st.error(f"Erreur de filtrage: {e}")
    
    # Configuration des options de st.dataframe
    df_kwargs = {
        "use_container_width": width == "100%",
        "hide_index": True,
    }
    
    # Ajout des options conditionnelles
    if height:
        df_kwargs["height"] = height
    
    # Configuration avancée des colonnes
    if column_config:
        df_kwargs["column_config"] = column_config
    
    # Configuration des options d'affichage
    config = {}
    if pagination:
        config["page_size"] = 10
    if not sort:
        config["sorting"] = False
    if search:
        config["search_bar"] = True
    if selection:
        config["selection"] = "multi"
    
    if config:
        df_kwargs["column_order"] = list(df_display.columns)
        if selection:  # Ajouter column_labels uniquement pour data_editor
            df_kwargs["column_labels"] = {col: col.replace("_", " ").title() for col in df_display.columns}
    
    # Option de téléchargement
    #if download:
        # Préparation des formats disponibles
    download_formats = {
            "CSV": ".csv",
            "Excel": ".xlsx",
            "JSON": ".json"
        }
        
    col1, col2, col3 = st.columns([3, 2, 1])
    with col1:
            selected_format = st.selectbox("Format:", options=list(download_formats.keys()), index=0,key=random.randint(1, 1000000))
        
    with col2:  
            filename = st.text_input("Nom du fichier:", download_filename.split('.')[0], key=random.randint(1, 1000000))
        
    with col3:
            ext = download_formats[selected_format]
            download_filename = f"{filename}{ext}"
            
            buffer = io.BytesIO()
            
            if selected_format == "CSV":
                df_display.to_csv(buffer, index=False)
            elif selected_format == "Excel":
                df_display.to_excel(buffer, index=False)
            elif selected_format == "JSON":
                buffer.write(df_display.to_json(orient="records").encode())
            
            buffer.seek(0)
            
            st.download_button(
                label="Télécharger",
                data=buffer,
                file_name=download_filename,
                mime="application/octet-stream", key=random.randint(1, 1000000)
            )
    
    # Affichage du DataFrame avec les options configurées
    if selection:
        return st.data_editor(df_display, **df_kwargs,key=random.randint(1, 1000000))
    else:
        if "column_labels" in df_kwargs:
            # Retirer l'argument non supporté pour st.dataframe
            labels_dict = df_kwargs.pop("column_labels")
        st.dataframe(df_display,**df_kwargs, key=cle)
        
    # Information sur le nombre de lignes
    st.caption(f"Total: {len(df_display)} lignes affichées (sur {len(df)} au total)")
    
    return None


               