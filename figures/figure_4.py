import math
import pandas as pd
import plotly.colors as pc
import plotly.express as px
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from helper import TRANSPARENT, generate_color_dict

# Stacked Area Chart with Normalized Values

class StackedAreaChart():
    def __init__(self):
        pass

    def plot_stacked_area_chart(self, data, height=700):
        """
        Cette fonction génère un graphique en aires empilées à partir des données fournies.
        Exemple de données:
        {1928: {'White': 10, 'Black': 0, 'Hispanic': 0, 'Asian': 0, 'Multiracial': 0, 'Other': 0}, 
        1929: {'White': 17, 'Black': 0, 'Hispanic': 0, 'Asian': 0, 'Multiracial': 0, 'Other': 0}, 
        1930: {'White': 17, 'Black': 0, 'Hispanic': 0, 'Asian': 0, 'Multiracial': 0, 'Other': 0}}

Args:
            data: Dictionnaire de données par année et catégorie
            height: Hauteur du graphique (défaut: 700px)

        Retourne la figure
        """

        # Convertir les données en DataFrame
        df = pd.DataFrame(data).T.fillna(0)
        df.index = df.index.astype(str)

        # Normaliser les valeurs
        df_normalized = df.div(df.sum(axis=1), axis=0)
        
        # Convertir en pourcentage (multiplier par 100)
        df_percentage = df_normalized * 100
        
        # Obtenir les couleurs pour chaque catégorie
        color_dict = generate_color_dict(identifiers=df_normalized.columns, colorscale_name='Oranges')
        color_sequence = [color_dict[cat] for cat in df_normalized.columns]

        # Créer une figure
        fig = go.Figure()
        
        # Ajouter chaque catégorie comme une série d'aires empilées
        for i, col in enumerate(df_percentage.columns):
            fig.add_trace(go.Scatter(
                x=df_percentage.index,
                y=df_percentage[col],
                mode='lines',
                stackgroup='one',
                name=col,
                line=dict(width=0),
                fillcolor=color_sequence[i],
                hoverinfo='skip'  # Désactiver le hover standard
            ))
        
        # Créer textes personnalisés pour le hover
        hover_texts = []
        for year in df_percentage.index:
            text = f"Année : {year}<br>"
            for col in df_percentage.columns:
                percentage = df_percentage.loc[year, col]
                absolute = df.loc[year, col]  # Valeur absolue
                text += f"{col} : {percentage:.1f}% ({int(absolute)})<br>"
            hover_texts.append(text)
        
        # Ajouter une trace invisible avec le hover personnalisé
        fig.add_trace(go.Scatter(
            x=df_percentage.index,
            y=[50] * len(df_percentage),  # Au milieu du graphique
            mode='markers',
            marker=dict(opacity=0),  # Invisible
            hoverinfo='text',
            hovertext=hover_texts,
            showlegend=False,
        ))
        
        # Configurer le layout
        fig.update_layout(
            # Enlever le titre
            title=None,
            # Définir une hauteur fixe
            height=height,
            autosize=False,
            xaxis=dict(
                # Enlever le "Year"
                title=None,
                showgrid=False,
                showspikes=True,  # Afficher une ligne verticale au survol
                spikecolor='black',
                spikethickness=1,
                spikedash='solid',
                spikemode='across'
            ),
            yaxis=dict(
                title={'text': 'Proportion (%)', 'font': {'family': 'Jost', 'size': 16}},
                showgrid=False,
                # Correction du format pour afficher correctement 0-100%
                tickformat='.0f',  # Format sans % et sans multiplier par 100
                ticksuffix='%',    # Ajouter le symbole % après chaque valeur
                range=[0, 100],    # Garder l'échelle de 0 à 100
                tickfont={'family': 'Jost'}
            ),
            legend_title={
                'text': 'Catégories',
                'font': {'family': 'Jost', 'size': 16}
            },
            legend={'font': {'family': 'Jost', 'size': 14}},
            hovermode='x',  # Hover mode sur l'axe x
            hoverdistance=100,  # Distance pour activer le hover
            hoverlabel=dict(
                bgcolor='white', 
                font_size=16,
                font_family='Jost'
            ),
            plot_bgcolor=TRANSPARENT,
            paper_bgcolor=TRANSPARENT,
            font={'family': 'Jost'},  # Police par défaut pour tout le graphique
            margin=dict(l=50, r=50, t=30, b=50)  # Ajuster les marges pour maximiser l'espace
        )
        
        return fig