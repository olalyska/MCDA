import os
import numpy as np
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

# === CONFIG ===
FOLDER = r"C:\Users\ola72\Documents\magisterka\datasetgenerator\data\PROMETHEE_I"  # CHANGE this to your data folder
POINT_SIZE = 6
###############

color_map = {
    0: 'yellow',  # 'incomparable',
    1: 'blue',   # 'worse than middle point'
    2: 'lime',  # 'equal to middle point within range'
    3: 'red'     # 'better than middle point'
}

color_meaning = {
    0: '||',
    1: '<',
    2: '≈',
    3: '>'
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
        title=f"File: {filename}",
        xaxis_title="",
        yaxis_title="",
        showlegend=True,
        template='plotly_white',
        width=500,
        height=500
    )

    figures.append(fig)

# === Dash App ===
app = Dash(__name__)
app.layout = html.Div([
    html.H2("Dataset Chart Carousel"),
    dcc.Slider(
        id='chart-slider',
        min=0,
        max=len(figures) - 1,
        step=1,
        value=0,
        marks={i: file_list[i] for i in range(len(figures))}
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