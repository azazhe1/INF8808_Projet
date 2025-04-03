import math 

import plotly.colors as pc
import plotly.express as px
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from helper import TRANSPARENT

class WaffleChart():

    def __init__(self):
        pass

    def _get_z_matrix(self, total, values, n_cols=10):
        n_rows = math.ceil(total / n_cols)
        z = values * [1] + (total - values) * [0.5] + (n_rows * n_cols - total) * [0]
        z = np.array(z).reshape(n_rows, n_cols)
        return z
    
    def _get_z_matrix_lower(self, total, values, n_cols=10):
        n_rows = math.ceil(total / n_cols)
        z = values * [1] + (total - values) * [0.5] + (n_rows * n_cols - total) * [0]
        z = np.array(z).reshape(n_rows, n_cols)
        return z
    
    def plot_waffle_chart(self, distribution, total):

        fig = make_subplots(rows=1, cols=len(distribution), 
                    shared_xaxes=True, shared_yaxes=True,
                    horizontal_spacing=0.01, vertical_spacing=0.01)

        color_scale_dict = generate_color_dict()  # Use predefined colors


        # Remove this if you want to use the same maximum for all subplots
        maximum = max(distribution.values())

        for i, id in enumerate(distribution):

            color = color_scale_dict[id]
            
            # Change this if you want to use the same maximum for all subplots
            z = self._get_z_matrix(maximum, distribution[id])
            # z = self._get_z_matrix(total, distribution[id])

            fig.add_trace(
                go.Heatmap(z=z, 
                        colorscale=[[0, TRANSPARENT], [0.5, TRANSPARENT], [1, color]],
                        xgap=3, ygap=3,
                        showscale=False,
                        ),
                        row = 1, col = i+1,
                        )

        fig.update_layout(height=800, plot_bgcolor=TRANSPARENT, paper_bgcolor=TRANSPARENT)

        for col in range(1, len(distribution)+1):
            fig.update_xaxes(showticklabels=False, showgrid=False, zeroline=False, row=1, col=col)
            fig.update_yaxes(showticklabels=False, showgrid=False, zeroline=False, row=1, col=col)

        fig.update_layout(
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False)
        )

        return fig 
    
    def plot_scatter_waffle_chart(self, distribution, df, category, font_size=16, font_family='Jost'):

        # distribution = distribution_dict[category]
        fig = make_subplots(rows=1, cols=len(distribution),
                            shared_yaxes=True, shared_xaxes=True,
                            horizontal_spacing=0.01, vertical_spacing=0.01)

        color_scale_dict = generate_color_dict(distribution.keys(), colorscale_name='Pastel2')

        # scatter plot disque
        fig = make_subplots(rows=1, cols=len(distribution), 
                            horizontal_spacing=0.01, vertical_spacing=0.01)

        y_max = math.ceil(max(distribution.values()) // 10) + 1

        for i, (key, value) in enumerate(distribution.items()):
            
            sub_df = (df[df[category] == key]
                .assign(index=lambda x: range(len(x)))
                .assign(x=lambda x: x['index'] % 10)
                .assign(y=lambda x: x['index'] // 10))
            
            fig.add_trace(go.Scatter(
    x=sub_df['x'], y=sub_df['y'],
    mode='markers',
    marker=dict(
        size=min(400/y_max, 30),
        color=[color_scale_dict[key]] * len(sub_df),  # Assign unique color to each marker
        symbol='circle'  # Change to 'circle' if you want filled markers
    ),
    customdata=sub_df[['Name', 'Category', 'Film', 'Year_Ceremony']],
    hovertemplate='Name: %{customdata[0]}<br>Category: %{customdata[1]}<br>Film: %{customdata[2]}<br>Year: %{customdata[3]} <extra></extra>'
), row=1, col=i+1)



            fig.add_annotation(x=4.5, y=-1., xref=f'x{i+1}', yref=f'y{i+1}',
                            text=key, showarrow=False, 
                                font_size=font_size, font_family=font_family)

            # xlim et ylim 
            fig.update_xaxes(range=[-1, 10], row=1, col=i+1)
            fig.update_yaxes(range=[-1, y_max+0.5], row=1, col=i+1)

            # remove axis
            fig.update_xaxes(visible=False, row=1, col=i+1)
            fig.update_yaxes(visible=False, row=1, col=i+1)

            # remove legend
            fig.update_layout(showlegend=False)

            fig.update_layout(
                hoverlabel=dict(
                    bgcolor="white",
                    font_size=font_size,
                    font_family=font_family
                )
            )

        # fig.update_layout(height=800)
        width = min(400 * len(distribution), 1200)
        # fig.update_layout(width=width, height=800)
        fig.update_layout(height=700,  width=width, plot_bgcolor=TRANSPARENT, paper_bgcolor=TRANSPARENT)

        # fig tight layout
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=10))

        return fig 
    
    def _get_hovertemplate(self, distribution):
        hovertemplate = []
        for id in distribution:
            hovertemplate += ['Name: ' + id]* distribution[id]
        return hovertemplate

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

# Function to lighten color by mixing with white
# def lighten_color(color, amount=0.8):  # amount: 0=original, 1=white
#     """
#     Lightens a color by blending it with white
#     """
#     # Convert from plotly 'rgb(r,g,b)' to tuple
#     rgb_str = color.strip('rgb(').strip(')')
#     r, g, b = [int(x) for x in rgb_str.split(',')]
    
#     # Mix with white
#     r = int(r + (255 - r) * amount)
#     g = int(g + (255 - g) * amount)
#     b = int(b + (255 - b) * amount)
    
#     return f'rgb({r},{g},{b})'