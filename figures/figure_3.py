# TODO rajouter figure

import pandas as pd
import plotly.graph_objects as go

from helper import TRANSPARENT

# Line Chart Showing the Evolution of a Category Over Time

class LineChart():
    def __init__(self):
        pass

    def plot_line_chart(self, distribution_dict, category, selected_categories, df):
        """
        Cette fonction génère un graphique en lignes montrant l'évolution d'une catégorie au fil du temps.
        
        Paramètres :
        - distribution_dict : dictionnaire des distributions par année (non utilisé ici, peut être retiré ou intégré plus tard)
        - category : la colonne de regroupement (ex. 'Ethnicity', 'Gender', etc.)
        - selected_categories : liste des catégories sélectionnées à afficher
        - df : DataFrame contenant les colonnes 'Year_Ceremony', category, 'Name', 'Film'

        Retourne : 
        - figure Plotly de type line chart avec des informations détaillées sur le hover.
        """

        # Créer la figure
        fig = go.Figure()

        # Pour chaque catégorie sélectionnée, tracer la courbe
        for category_name in selected_categories:
            # Filtrer le DataFrame pour la catégorie spécifique
            filtered_df = df[df[category] == category_name]
            
            # Regrouper par année et effectuer des agrégations
            grouped_df = filtered_df.groupby('Year_Ceremony').agg(
                Count=('Name', 'count'),  # Nombre de gagnants par année
                Names=('Name', 'first'),  # Afficher seulement le premier nom pour chaque année
                Films=('Film', 'first')   # Afficher seulement le premier film pour chaque année
            ).reset_index()  # Réinitialiser l'index pour obtenir une DataFrame propre

            # Créer les textes personnalisés pour le hover
            hover_texts = []
            for _, row in grouped_df.iterrows():
                text = f"Name: {row['Names']}<br>"
                text += f"Category: {category_name}<br>"
                text += f"Movie: {row['Films']}<br>"
                text += f"Year: {int(row['Year_Ceremony'])}"
                hover_texts.append(text)

            # Ajouter la trace à la figure
            fig.add_trace(go.Scatter(
                x=grouped_df['Year_Ceremony'],
                y=grouped_df['Count'],
                mode='lines',
                name=category_name,
                hoverinfo='text',
                hovertext=hover_texts
            ))

        # Mettre à jour le layout
        fig.update_layout(
            shapes=[
                # Ajouter une ligne verticale pour l'année 2015
                dict(
                    type='line',
                    x0=2015,
                    x1=2015,
                    y0=0,
                    y1=1,
                    xref='x',
                    yref='paper',
                    line=dict(
                        color='grey',
                        width=2,
                        dash='dashdot'
                    )
                )
            ],
            # Titre
            title=None,
            autosize=True,
            xaxis=dict(
                title=None,
                showgrid=False,
                showspikes=True,
                spikecolor='black',
                spikethickness=1,
                spikedash='solid',
                spikemode='across'
            ),
            yaxis=dict(
                title={'text': 'Count', 'font': {'family': 'Jost', 'size': 16}},
                showgrid=False,
                tickfont={'family': 'Jost'}
            ),
            legend_title={
                'text': 'Catégories',
                'font': {'family': 'Jost', 'size': 16}
            },
            legend={'font': {'family': 'Jost', 'size': 14}},
            hovermode='closest',  # Change hovermode to 'closest' to show hover info for only one point
            hoverdistance=100,
            hoverlabel=dict(
                bgcolor='white',
                font_size=16,
                font_family='Jost'
            ),
            plot_bgcolor=TRANSPARENT,
            paper_bgcolor=TRANSPARENT,
            font={'family': 'Jost'},
            margin=dict(l=50, r=50, t=30, b=50)
        )

        return fig
