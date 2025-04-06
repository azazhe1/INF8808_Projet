import pandas as pd 
import math
import plotly.colors as pc
import plotly.express as px
import numpy as np

    
# Define custom colors for the markers in your Waffle chart
CUSTOM_COLORS = [
    '#FFFFFF',  # White
    '#000000',  # Black
    '#BE8F4D',  # Bronze
    '#FFDA6E',  # Gold
    '#C56D65',  # Rose
    '#593A1E'   # Brown
]

TRANSPARENT = 'rgba(0,0,0,0)'

class DataLoader():

    def __init__(self):
        self.data = None

    def load_data(self, path):
        self.data = pd.read_csv(path)
    
    def preprocess_data(self):
        self.data['Birth_Date'] = pd.to_datetime(self.data['Birth_Date'], format='%Y-%m-%d', errors='coerce')
        self.data['Ceremony_Date'] = pd.to_datetime(self.data['Year_Ceremony'], format='%Y').apply(lambda x: x.replace(month=3, day=1))
        self.data['Age'] = ((self.data['Ceremony_Date'] - self.data['Birth_Date']).dt.days / 365.25).apply(math.floor, 0)
        self.data = self.data.drop(columns=['Birth_Date', 'Birth_Place', 'Ceremony_Date', 'Link', 'Ceremony_Date'])
        return self.data
    
    def filter_data(self, start_year, end_year, is_winner=None):
        """
        Filter the data based on the start and end years and winner status.
        
        Args:
            start_year (int): The start year for filtering
            end_year (int): The end year for filtering
            is_winner (bool, optional): If True, only winners are included. 
                                      If False, only non-winners. 
                                      If None, both winners and nominees are included.
        
        Returns:
            pandas.DataFrame: The filtered dataframe
        """
        filtered_df = self.data[(self.data['Year_Ceremony'] >= start_year) & 
                              (self.data['Year_Ceremony'] <= end_year)]
        
        # Apply the winner filter if specified
        if is_winner is not None:
            filtered_df = filtered_df[filtered_df['Win_Oscar?'] == is_winner]
            
        return filtered_df
    
    def get_unique_distribution(self, data):
        """ 
        Exemple de résultat attendu:
        (
        {'Straight': 246,
        'Na': 11,
        'Matter of Dispute': 7,
        'Gay': 6,
        'Bisexual': 3,
        'Lesbian': 2},
        275)
        """
        df = data.copy()    
        df.drop(columns=['Category', 'Name', 'Film', 'Year_Ceremony', 'Win_Oscar?'], inplace=True)
        df = df.reindex(sorted(df.columns), axis=1)

        result_dict = {}
        for col in df.columns:
            result_dict[col] = df.groupby(col).size().to_dict()
            result_dict[col] = dict(sorted(result_dict[col].items(), key=lambda item: item[1], reverse=True))

        total = len(df)

        return result_dict, total
    
    def get_yearly_distribution(self, data, selected_categories=None):
        """
        Fonction qui retourne un dictionnaire contenant la distribution des valeurs uniques pour chaque année.
        En entrée elle prend un dataframe contenant la colonne étudiée ainsi que la colonne Year_Ceremony.

        Exemple de dataframe:
         data:      Year_Ceremony      Race or Ethnicity
                    1928                White
                    1928                White
                    1928                White

        Exemple de résultat attendu:
        {
            1928: {'Straight': 4, 'Na': 1},
            1929: {'Straight': 3, 'Na': 1},
            ...
        }
        """
        df = data.copy()
        df = df.groupby(['Year_Ceremony', df.columns[1]]).size().unstack(fill_value=0)
        df = df.astype(int)
        df = df.reindex(sorted(df.columns), axis=1)
        distribution_dict = {year: row.to_dict() for year, row in df.iterrows()}
        # Sort by year
        distribution_dict = dict(sorted(distribution_dict.items(), key=lambda item: item[0]))

        # Si on a besoin, on ajoute une catégorie "Other" qui contient la somme des autres catégories
        need_other = False
        if selected_categories is not None:
            if 'Other' in selected_categories:
                selected_categories.remove('Other')
                need_other = True

        if selected_categories is not None:
            for year, distribution in distribution_dict.items():
                filtered_distribution = {key: distribution[key] for key in selected_categories if key in distribution}
                if need_other:
                    filtered_distribution['Other'] = sum(value for key, value in distribution.items() if key not in selected_categories)
                distribution_dict[year] = filtered_distribution

        return distribution_dict


# def generate_color_dict():
#     return {
#         'White': '#FFFFFF',   # White
#         'Black': '#000000',   # Black
#         'Asian': '#BE8F4D',   # Brown
#         'Hispanic': '#FFDA6E', # Yellow
#         'Other': '#C56D65',   # Reddish
#         'Mixed': '#593A1E'    # Dark Brown
#     }


def generate_color_dict(identifiers=None, n_colors=None, colorscale_name='Set1'):
    """
    Generate a dictionary mapping identifiers to colors from a Plotly colorscale
    
    Parameters:
    -----------
    identifiers : list, optional
        List of category identifiers to map to colors
    n_colors : int, optional
        Number of colors to generate if identifiers not provided
    colorscale_name : str, default='Set1'
        Name of the Plotly colorscale to use
        Options include: 'Plotly', 'D3', 'G10', 'T10', 'Alphabet', 
        'Dark24', 'Light24', 'Set1', 'Set2', 'Set3', 'Pastel1', 'Pastel2'
    
    Returns:
    --------
    dict
        Dictionary mapping each identifier to a color
    """
    # Determine number of colors needed
    if identifiers is not None:
        n_colors = len(identifiers)
    elif n_colors is None:
        raise ValueError("Either identifiers or n_colors must be provided")
    
    # Get colors from the specified colorscale
    try:
        # For qualitative/discrete colorscales
        if colorscale_name in ['Plotly', 'D3', 'G10', 'T10', 'Alphabet', 
                              'Dark24', 'Light24', 'Set1', 'Set2', 'Set3', 
                              'Pastel1', 'Pastel2']:
            colors = getattr(pc.qualitative, colorscale_name)
            # Repeat colors if we need more than available
            colors = (colors * (n_colors // len(colors) + 1))[:n_colors]
        else:
            # For continuous colorscales, sample n_colors from the scale
            colorscale = getattr(px.colors.sequential, colorscale_name, None)
            if colorscale is None:
                colorscale = getattr(px.colors.diverging, colorscale_name, None)
            if colorscale is None:
                colorscale = getattr(px.colors.cyclical, colorscale_name, None)
            if colorscale is None:
                # Default to built-in continuous colorscale and sample it
                color_positions = np.linspace(0, 1, n_colors)
                colorscale = px.colors.sample_colorscale(colorscale_name, color_positions)
                colors = colorscale
            else:
                # For color lists from sequential/diverging modules
                step = max(1, len(colorscale) // n_colors)
                colors = colorscale[::step][:n_colors]
                # Add more if needed
                if len(colors) < n_colors:
                    indices = np.linspace(0, len(colorscale)-1, n_colors-len(colors)).astype(int)
                    colors.extend([colorscale[i] for i in indices])
    except (AttributeError, ValueError):
        # Fallback to default colorscale
        color_positions = np.linspace(0, 1, n_colors)
        colors = px.colors.sample_colorscale("Viridis", color_positions)
    
    # Create the mapping
    if identifiers is not None:
        color_dict = {id_val: colors[i % len(colors)] for i, id_val in enumerate(identifiers)}
    else:
        color_dict = {i: colors[i % len(colors)] for i in range(n_colors)}
        
    return color_dict