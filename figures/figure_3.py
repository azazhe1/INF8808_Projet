import pandas as pd
import plotly.graph_objects as go
import numpy as np
from helper import TRANSPARENT, generate_color_dict

# Line Chart Showing the Evolution of a Category Over Time

class LineChart():
    def __init__(self):
        pass

    def plot_line_chart(self, distribution_dict, category, selected_categories, df, cumulative=True, scale_type='linear'):
        """
        Cette fonction génère un graphique en lignes montrant l'évolution d'une catégorie au fil du temps.
        
        Paramètres :
        - distribution_dict : dictionnaire des distributions par année
        - category : la colonne de regroupement (ex. 'Ethnicity', 'Gender', etc.)
        - selected_categories : liste des catégories sélectionnées à afficher
        - df : DataFrame contenant les colonnes 'Year_Ceremony', category, 'Name', 'Film'
        - cumulative : booléen indiquant si les données doivent être affichées de manière cumulative
        - scale_type : type d'échelle pour l'axe Y ('linear' ou 'log')

        Retourne : 
        - figure Plotly de type line chart
        """
        # Créer la figure
        fig = go.Figure()
        
        # Générer un dictionnaire de couleurs pour les catégories
        color_dict = generate_color_dict(selected_categories, colorscale_name='Oranges')
        
        # Pour chaque catégorie sélectionnée, tracer la courbe
        for i, category_name in enumerate(selected_categories):
            # Pour les données agrégées par année
            x_years = sorted(distribution_dict.keys())
            y_values = [distribution_dict[year].get(category_name, 0) for year in x_years]
            
            # Filtrer le DataFrame pour la catégorie spécifique
            filtered_df = df[df[category] == category_name]
            
            # Créer les textes personnalisés pour le hover
            hover_texts = []
            for year in x_years:
                # Compter le nombre d'occurrences pour cette catégorie et cette année
                year_count = distribution_dict[year].get(category_name, 0)
                
                # Si nous utilisons des données cumulatives, nous ne voulons montrer que les nouvelles entrées
                annual_count = year_count
                if cumulative and year > min(x_years):
                    previous_year_index = x_years.index(year) - 1
                    previous_year = x_years[previous_year_index]
                    annual_count = year_count - distribution_dict[previous_year].get(category_name, 0)
                
                # Pour cette année et cette catégorie, trouver les noms et films
                year_data = filtered_df[filtered_df['Year_Ceremony'] == year]
                
                # Créer le texte du hover
                text = f"<b>{category_name}</b><br>"
                text += f"Année: {year}<br>"
                
                if cumulative:
                    text += f"Total cumulé: {year_count}<br>"
                    text += f"Nouveaux cette année: {annual_count}<br>"
                else:
                    text += f"Nombre cette année: {annual_count}<br>"
                
                # Si nous avons des données détaillées pour cette année
                if not year_data.empty and annual_count > 0:
                    text += "<br>Exemples:<br>"
                    # Limiter à 3 exemples maximum
                    for _, entry in year_data.head(3).iterrows():
                        text += f"• {entry['Name']} ({entry['Film']})<br>"
                    
                    if len(year_data) > 3:
                        text += f"...et {len(year_data) - 3} autres"
                
                hover_texts.append(text)

            # Ajouter la trace à la figure avec la couleur correspondante
            fig.add_trace(go.Scatter(
                x=x_years,
                y=y_values,
                mode='lines+markers',
                name=category_name,
                line=dict(color=color_dict[category_name], width=3),
                marker=dict(size=8, color=color_dict[category_name]),
                hoverinfo='text',
                hovertext=hover_texts
            ))

        # Déterminer si la ligne verticale à 2015 doit être affichée
        shapes = []
        if x_years and min(x_years) <= 2015 <= max(x_years):
            shapes.append(
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
            )

        # Mettre à jour le layout
        fig.update_layout(
            shapes=shapes,  # Utiliser la liste de formes conditionnelle
            # Configuration générale
            autosize=True,
            paper_bgcolor=TRANSPARENT,  # Fond transparent
            plot_bgcolor=TRANSPARENT,   # Fond du graphique transparent
            xaxis=dict(
                title={'text': 'Année', 'font': {'family': 'Jost', 'size': 16}},
                showgrid=False,
                showspikes=True,
                spikecolor='grey',
                spikethickness=1,
                spikedash='solid',
                spikemode='across',
                tickfont={'family': 'Jost'}
            ),
            yaxis=dict(
                title={'text': 'Nombre cumulé' if cumulative else 'Nombre', 'font': {'family': 'Jost', 'size': 16}},
                showgrid=True,
                gridcolor='rgba(0,0,0,0.1)',
                tickfont={'family': 'Jost'},
                type=scale_type  # Définir le type d'échelle (linéaire ou logarithmique)
            ),
            legend_title={
                'text': 'Catégories',
                'font': {'family': 'Jost', 'size': 16}
            },
            legend={'font': {'family': 'Jost', 'size': 14}},
            hovermode='closest',
            hoverdistance=100,
            hoverlabel=dict(
                bgcolor='white', 
                font_size=16,
                font_family='Jost'
            ),
        )
        
        return fig