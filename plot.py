from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
from dash_bootstrap_templates import load_figure_template
import dash_bootstrap_components as dbc
import pandas as pd

def main():

    # Load the data from the CSV file
    df = pd.read_csv('medals.csv')
    print(df.head())

    load_figure_template("SIMPLEX")
    app = Dash(__name__, external_stylesheets=[dbc.themes.SIMPLEX])

    # Sort the DataFrame by Total, Gold, Silver, then Bronze
    df_sorted = df.sort_values(by=['Total', 'Gold', 'Silver', 'Bronze'], ascending=[False, False, False, False])

    # Melt the DataFrame to have a single column of medal type to split the histogram
    df_medals = df_sorted.melt(id_vars=["Country", "Country Code", "Total"], value_vars=["Gold", "Silver", "Bronze"], 
                               var_name="Medal Type", value_name="Total Medals")

    # Define the color map for gold, silver, and bronze
    color_map = {
        "Gold": "goldenrod",
        "Silver": "silver",
        "Bronze": "peru"
    }

    fig_perf = px.histogram(
        df_medals,
        x="Country Code",
        y="Total Medals",
        color="Medal Type",
        color_discrete_map=color_map,
        labels={"Country Code": "Country", "Total Medals": "Number of medals"},
        title="Table of Medals ordered by total of medals",
        text_auto=True
    )

    # Add the individual medal counts inside each bar
    fig_perf.update_traces(texttemplate='%{y}', textposition='inside')

    # Add total number of medals on top of each bar
    for i, row in df_sorted.iterrows():
        fig_perf.add_annotation(
            x=row["Country Code"],
            y=row["Total"],
            text=str(row["Total"]),
            showarrow=False,
            yshift=10,
            font=dict(size=12, color="black")
        )

    # Center the legend at the top
    fig_perf.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        )    
    )

    app.layout = html.Div(
        [
            html.H1("Olympic Medals", style={'textAlign': 'center'}),
            dcc.Graph(id="graph", figure=fig_perf, style={'width': '100%', 'height': '100vh'}),
        ],
        style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center', 'justifyContent': 'center', 'height': '100vh'}
    )

    app.run_server(debug=False)


if __name__ == "__main__":
    main()