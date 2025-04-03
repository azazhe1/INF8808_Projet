import math
import pandas as pd
import plotly.colors as pc
import plotly.express as px
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from helper import TRANSPARENT

# Stacked Area Chart with Normalized Values

class StackedAreaChart():
    def __init__(self):
        pass

    def plot_stacked_area_chart(self, data):
        """
        Cette fonction génère un graphique en aires empilées à partir des données fournies.
        Exemple de données:
        {1928: {'White': 10, 'Black': 0, 'Hispanic': 0, 'Asian': 0, 'Multiracial': 0, 'Other': 0}, 
        1929: {'White': 17, 'Black': 0, 'Hispanic': 0, 'Asian': 0, 'Multiracial': 0, 'Other': 0}, 
        1930: {'White': 17, 'Black': 0, 'Hispanic': 0, 'Asian': 0, 'Multiracial': 0, 'Other': 0}}

        Retourne la figure
        """

        # Convertir les données en DataFrame
        df = pd.DataFrame(data).T.fillna(0)
        df.index = df.index.astype(str)

        # Normaliser les valeurs
        df_normalized = df.div(df.sum(axis=1), axis=0)

        # Créer le graphique
        fig = px.area(df_normalized, x=df_normalized.index, y=df_normalized.columns,
                      labels={'x': 'Year', 'y': 'Categories'},
                      title='Stacked Area Chart with Normalized Values',
                      color_discrete_sequence=px.colors.qualitative.Plotly)

        fig.update_traces(mode='lines+markers')
        fig.update_layout(legend_title_text='Categories', plot_bgcolor=TRANSPARENT, paper_bgcolor=TRANSPARENT)
        
        return fig