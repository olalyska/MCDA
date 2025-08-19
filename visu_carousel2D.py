import os
import numpy as np
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

# === CONFIG ===
FOLDER = r"C:\Users\ola72\Documents\magisterka\datasetgenerator\data\TOPSIS_1000x"  # CHANGE this to your data folder
POINT_SIZE = 9
import plotly.express as px
###############

# color_map = {
#     0: '#f0ab00',  # yellow 'incomparable',
#     1: '#f62a38',   # red 'worse than middle point'
#     2: '#80ea2f',  # green 'equal to middle point within range'
#     3: '#3699d5'     # blue 'better than middle point'
# }

color_map = {
    0: '#f0ab00',  # yellow 'incomparable',
    1: '#cd202c',   # red 'better than middle point'
    2: '#69be28',  # green 'equal to middle point within range'
    3: '#2a6ebb'     # blue 'worse than middle point'
}

# color_map = {
#     0: '#f0ab00',  # yellow 'incomparable',
#     3: '#cd202c',   # red 'better than middle point'
#     2: '#69be28',  # green 'equal to middle point within range'
#     1: '#2a6ebb'     # blue 'worse than middle point'
# }

color_meaning = {
    3: 'Worse',
    1: 'Better',
    2: 'Indifferent',
    0: 'Incomparable'
}

# === Load all datasets ===
file_list = [f for f in os.listdir(FOLDER) if f.endswith('.csv') or f.endswith('.txt')]
file_list.sort()

# Prepare filtered data and figures
figures = []

for filename in file_list:
    path = os.path.join(FOLDER, filename)
    data = np.loadtxt(path, delimiter=",")

    x, y, c = data[:, 0].astype(float), data[:, 1].astype(float), data[:, 2].astype(int)

    fig = go.Figure()
    # fig = px.bar(x=[0, 0.5, 1], y=[0, 0.5, 1])
    for color_value in np.unique(c):
        color_mask = c == color_value
        fig.add_trace(go.Scatter(
            x=x[color_mask],
            y=y[color_mask],
            mode='markers',
            marker=dict(color=color_map.get(color_value, 'gray'), size=POINT_SIZE, symbol='square'),
            name=color_meaning[color_value]
        ))

    fig.update_layout(
        title=f"{filename}",
        title_x=0.45,
        title_y=0.9,
        title_font_size=20,
        # xaxis_title="Criterion 1",
        # yaxis_title="Criterion 2",
        showlegend=True,
        legend_y=0.5,
        legend_font_size=20,
        legend=dict(
            itemsizing="constant",  # keeps marker size fixed
            font=dict(size=20)    # controls legend marker size
        ),
        # legend_itemwidth=50,
        template='plotly_white',
        width=800,
        height=700,
        xaxis=dict(
            title=dict(
                text="Criterion 1",
                font=dict(size=20)  # bigger x-axis title
            ),
            tickfont=dict(size=18),
            tickvals=[0, 0.25, 0.5, 0.75, 1]
        ),
        yaxis=dict(
            title=dict(
                text="Criterion 2",
                font=dict(size=20)  # bigger x-axis title
            ),
            tickfont=dict(size=18),
            tickvals=[0, 0.25, 0.5, 0.75, 1]
        ),
        shapes=[
            # Vertical dashed line at x=0.5
            dict(
                type="line",
                x0=0.5, y0=0, x1=0.5, y1=1,  # spans full y-range
                line=dict(color="#757575", width=2, dash="dash")
            ),
            # Horizontal dashed line at y=0.5
            dict(
                type="line",
                x0=0, y0=0.5, x1=1, y1=0.5,  # spans full x-range
                line=dict(color="#757575", width=1, dash="dash")
            )
        ]
    )


    figures.append(fig)

# === Dash App ===
app = Dash(__name__)
app.layout = html.Div([
    html.H2("Dataset Visualization Carousel"),
    dcc.Slider(
        id='chart-slider',
        min=0,
        max=len(figures) - 1,
        step=1,
        value=0,
        # marks={i: file_list[i] for i in range(len(figures))}
    ),
    dcc.Graph(id='chart-display')
])


@app.callback(
    Output('chart-display', 'figure'),
    Input('chart-slider', 'value')
)
def update_chart(index):
    return figures[index]


if __name__ == '__main__':
    app.run(debug=True)