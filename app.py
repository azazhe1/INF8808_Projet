# dash app
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

import figures.figure_1 as figure_1
import figures.figure_4 as figure_4

from helper import DataLoader

print('hello')

FONT = 'Jost'

app = dash.Dash(__name__)

intervalle_defaut = [1928, 2025]

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
        # TODO Modifier la mise en page
        
        html.Main(children=[
            
            # Figure 1
            html.Div(children=[

                html.H3('Lors des 97 cérémonies des Oscars, il y a eu 416 gagnants. Voici leur distribution.',
                       className='figure-title'),

                html.Div([
                    dcc.Tabs(
                        id='tabs_fig_1',
                        value='Race or Ethnicity',
                        children=[
                            dcc.Tab(label='Ethnie', value='Race or Ethnicity', className='dash-tab', selected_className='dash-tab--selected'),
                            dcc.Tab(label='Genre', value='Gender', className='dash-tab', selected_className='dash-tab--selected'),
                            dcc.Tab(label='Religion', value='Religion', className='dash-tab', selected_className='dash-tab--selected'),
                            dcc.Tab(label='Âge', value='Age', className='dash-tab', selected_className='dash-tab--selected'),
                            dcc.Tab(label='Orientation', value='Sexual orientation', className='dash-tab', selected_className='dash-tab--selected')
                        ],
                        className='dash-tabs'
                    ),

                    # Ajout des boutons radio pour la Figure 1
                    html.Div([
                        dcc.RadioItems(
                            id='winner-filter_fig_1',
                            options=[
                                {'label': 'Gagnants seulement', 'value': 'winners'},
                                {'label': 'Gagnants et nominés', 'value': 'all'}
                            ],
                            value='winners',
                            inline=True,
                            className='radio-filter'
                        )
                    ], style={'margin': '10px 0'}),

                    dcc.Checklist(
                        id='category-checklist_fig_1',
                        options=[],
                        value=[],
                        inline=True,
                        className='dash-checklist'
                    ),

                    dcc.Graph(id='waffle-chart', style={'width': '100%'}),

                    dcc.RangeSlider(
                        id='year-slider_fig_1',
                        min=1928,
                        max=2025,
                        step=1,
                        marks={i: '{}'.format(i) for i in range(1928, 2025, 10)},
                        value= intervalle_defaut,
                        allowCross=False
                    )
                ], style={'width': '100%', 'margin': '0 auto'}),
                ],
                style={'margin': '0 auto', 'width': '100%', 'fontFamily': FONT, 'display': 'block', 'textAlign': 'center'}
            ),

            # Espace entre les figures
            html.Div(style={'height': '150px', 'width': '100%', 'clear': 'both'}),

            # Figure 4
            html.Div(children=[

                html.H3('L\'évolution de la diversité aux Oscars à travers les décennies.', 
                       className='figure-title'),

                html.Div([
                    dcc.Tabs(
                        id='tabs_fig_4',
                        value='Race or Ethnicity',
                        children=[
                            dcc.Tab(label='Ethnie', value='Race or Ethnicity', className='dash-tab', selected_className='dash-tab--selected'),
                            dcc.Tab(label='Genre', value='Gender', className='dash-tab', selected_className='dash-tab--selected'),
                            dcc.Tab(label='Religion', value='Religion', className='dash-tab', selected_className='dash-tab--selected'),
                            dcc.Tab(label='Âge', value='Age', className='dash-tab', selected_className='dash-tab--selected'),
                            dcc.Tab(label='Orientation', value='Sexual orientation', className='dash-tab', selected_className='dash-tab--selected')
                        ],
                        className='dash-tabs'
                    ),

                    # Ajout des boutons radio pour la Figure 4
                    html.Div([
                        dcc.RadioItems(
                            id='winner-filter_fig_4',
                            options=[
                                {'label': 'Gagnants seulement', 'value': 'winners'},
                                {'label': 'Gagnants et nominés', 'value': 'all'}
                            ],
                            value='winners',
                            inline=True,
                            className='radio-filter'
                        )
                    ], style={'margin': '10px 0'}),

                    dcc.Checklist(
                        id='category-checklist_fig_4',
                        options=[],
                        value=[],
                        inline=True,
                        className='dash-checklist'
                    ),

                    dcc.Graph(id='stacked-area-chart', style={'width': '100%'}),

                    dcc.RangeSlider(
                        id='year-slider_fig_4',
                        min=1928,
                        max=2025,
                        step=1,
                        marks={i: '{}'.format(i) for i in range(1928, 2025, 10)},
                        value= intervalle_defaut,
                        allowCross=False
                    )
                ], style={'width': '100%', 'margin': '0 auto'}),

            ],
            style={'margin': '0 auto', 'width': '100%', 'fontFamily': FONT, 'display': 'block', 'textAlign': 'center'}
            ),
        ],
        style={'width': '90%', 'margin': '0 auto', 'fontFamily': FONT, 'display': 'flex', 'flexDirection': 'column'}
        ),
       

        
    ],
    style={'width': '80%', 'margin': 'auto', 'fontFamily': FONT})



# Figure 1
dataloader = DataLoader()
dataloader.load_data('assets/The_Oscar_Award_Demographics_1928-2025 - The_Oscar_Award_Demographics_1928-2025_v3.csv')
dataloader.preprocess_data()
df = dataloader.filter_data(1928, 2025)
distribution_dict, total = dataloader.get_unique_distribution(df)

# Callback pour afficher une liste de boutons en fonction de la valeur des onglets
@app.callback(
    Output('category-checklist_fig_1', 'options'),
    Output('category-checklist_fig_1', 'value'),
    Input('year-slider_fig_1', 'value'),
    Input('tabs_fig_1', 'value'),
    Input('winner-filter_fig_1', 'value'),
)
def update_category_dropdown_fig_1(year_range, category, winner_filter):
    # Filtrer par gagnants uniquement ou tous les nominés selon la valeur du bouton radio
    is_winner = None if winner_filter == 'all' else True
    df = dataloader.filter_data(year_range[0], year_range[1], is_winner=is_winner)
    distribution_dict, _ = dataloader.get_unique_distribution(df)
    return [{'label': key, 'value': key} for key in distribution_dict[category].keys()], list(distribution_dict[category].keys())[:5]

# Callback pour changer le waffle-chart en fonction de la valeur de category-checklist
@app.callback(
    Output('waffle-chart', 'figure'),
    Input('year-slider_fig_1', 'value'),
    Input('tabs_fig_1', 'value'),
    Input('category-checklist_fig_1', 'value'),
    Input('winner-filter_fig_1', 'value'),
    allow_duplicate=True
)
def update_waffle_chart(year_range, category, selected_categories, winner_filter):
    is_winner = None if winner_filter == 'all' else True
    df = dataloader.filter_data(year_range[0], year_range[1], is_winner=is_winner)
    distribution_dict, _ = dataloader.get_unique_distribution(df)
    wchart = figure_1.WaffleChart()
    return wchart.plot_scatter_waffle_chart({key: distribution_dict[category][key] for key in selected_categories}, df, category)

@app.callback(
    Output('category-checklist_fig_4', 'options'),
    Output('category-checklist_fig_4', 'value'),
    Input('year-slider_fig_4', 'value'),
    Input('tabs_fig_4', 'value'),
    Input('winner-filter_fig_4', 'value'),
)
def update_category_dropdown_fig_4(year_range, category, winner_filter):
    is_winner = None if winner_filter == 'all' else True
    df = dataloader.filter_data(year_range[0], year_range[1], is_winner=is_winner)
    distribution_dict, _ = dataloader.get_unique_distribution(df)    
    # On ajoute une option Other pour les catégories qui n'ont pas été sélectionnées
    checklist = [{'label': key, 'value': key} for key in distribution_dict[category].keys()] + [{'label': 'Other', 'value': 'Other'}]
    selected_categories = list(distribution_dict[category].keys())[:5]
    # Si il y a plus de 5 catégories, on sélectionne les 5 premières + Other
    if len(distribution_dict[category]) > 5:
        selected_categories += ['Other']
    return checklist, selected_categories

@app.callback(
    Output('stacked-area-chart', 'figure'),
    Input('year-slider_fig_4', 'value'),
    Input('tabs_fig_4', 'value'),
    Input('category-checklist_fig_4', 'value'),
    Input('winner-filter_fig_4', 'value'),
    allow_duplicate=True
)
def update_stacked_area_chart(year_range, category, selected_categories, winner_filter):
    is_winner = None if winner_filter == 'all' else True
    df = dataloader.filter_data(year_range[0], year_range[1], is_winner=is_winner)
    # On ne garde que l'année et la colonne de la catégorie
    distribution_dict = dataloader.get_yearly_distribution(df[['Year_Ceremony', category]], selected_categories)
    stacked_chart = figure_4.StackedAreaChart()
    return stacked_chart.plot_stacked_area_chart(distribution_dict)


# TODO Ajouter les callbacks des autres figures 

if __name__ == '__main__':
    app.run(port=8070, debug=True)