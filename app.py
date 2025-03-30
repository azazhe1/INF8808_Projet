# dash app
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

import figures.figure_1 as figure_1

print('hello')

FONT = 'Jost'

app = dash.Dash(__name__)

app.layout = \
    html.Div([
        
        html.Header(children=[
            html.Div(children=[
                        html.H2('Les'),
                        html.H1('OSCARS'),
                        html.H2('Font-ils de la discrimination?'),
                        html.Hr(),
                        html.P('Nous avons analysé les gagnants des dernières éditions pour le savoir'), 
                    ],
                    className="texte-entete"
                    ),
        ]),
        # TODO Modifier le layout 
        
        html.Main(children=[
            
            html.Div(children=[
             html.H3('Lors des 97 cérémonies des Oscars, il y a eu 416 gagnants. Voici leur distribution.'),
        
        dcc.Tabs(id='tabs', value='Race or Ethnicity', children=[
            dcc.Tab(label='Ethnie', value='Race or Ethnicity'),
            dcc.Tab(label='Genre', value='Gender'),
            dcc.Tab(label='Religion', value='Religion'),
            dcc.Tab(label='Age', value='Age'),
            dcc.Tab(label='Orientation', value='Sexual orientation')
        ]),
            html.Div([
            dcc.Checklist(
                id='category-checklist',
                options=[],
                value=[],
                inline=True,
            ),
            dcc.Graph(id='waffle-chart'),
            dcc.RangeSlider(
                id='year-slider',
                min=1928,
                max=2025,
                step=1,
                marks={i: '{}'.format(i) for i in range(1928, 2025, 10)},
                value=[1990, 2000],
                allowCross=False
            )
        ])
            ])
            ])
       

        
    ],
    style={'width': '80%', 'margin': 'auto', 'fontFamily': FONT})



# Figure 1
dataloader = figure_1.DataLoader()
dataloader.load_data('assets/The_Oscar_Award_Demographics_1928-2025 - The_Oscar_Award_Demographics_1928-2025_v3.csv')
dataloader.preprocess_data()
df = dataloader.filter_data(1990, 2000)
distribution_dict, total = dataloader.get_unique_distribution(df)

# callback pour afficher une liste de bouton en fonction de la valeur de Tabs
@app.callback(
    Output('category-checklist', 'options'),
    Output('category-checklist', 'value'),
    Input('year-slider', 'value'),
    Input('tabs', 'value'),
)
def update_category_dropdown(year_range, category):
    df = dataloader.filter_data(year_range[0], year_range[1])
    distribution_dict, _ = dataloader.get_unique_distribution(df)
    return [{'label': key, 'value': key} for key in distribution_dict[category].keys()], list(distribution_dict[category].keys())[:5]

# Callback pour change waffle-chart en fonction de la valeur de category-checklist
@app.callback(
    Output('waffle-chart', 'figure'),
    Input('year-slider', 'value'),
    Input('tabs', 'value'),
    Input('category-checklist', 'value'),
    allow_duplicate=True
)
def update_waffle_chart(year_range, category, selected_categories):
    df = dataloader.filter_data(year_range[0], year_range[1])
    distribution_dict, _ = dataloader.get_unique_distribution(df)
    wchart = figure_1.WaffleChart()
    return wchart.plot_scatter_waffle_chart({key: distribution_dict[category][key] for key in selected_categories}, df, category)

# TODO Rajouter call back des autres figures 

if __name__ == '__main__':
    app.run(port=8070, debug=True)