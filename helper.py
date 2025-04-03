
import pandas as pd 
import math

def generate_color_dict():
    return {
        'White': '#FFFFFF',   # White
        'Black': '#000000',   # Black
        'Asian': '#BE8F4D',   # Brown
        'Hispanic': '#FFDA6E', # Yellow
        'Other': '#C56D65',   # Reddish
        'Mixed': '#593A1E'    # Dark Brown
    }
    
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
    
    def filter_data(self, start_year, end_year):
        return self.data[(self.data['Year_Ceremony'] >= start_year) & (self.data['Year_Ceremony'] <= end_year)]
    
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