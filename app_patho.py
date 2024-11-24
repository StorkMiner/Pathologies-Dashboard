import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import json
import os

# Obtenir le chemin du fichier courant (app.py)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Charger les données de prévalence
df = pd.read_csv(os.path.join(current_dir, "data_patho_2019 - Copie.csv"), sep=";",encoding="utf-8")

pathologies_list = sorted(df['patho_niv3'].unique())
ages_list = sorted(df['AGE_ORD'].unique())

# Charger les données géographiques
with open(os.path.join(current_dir, "map_data.json")) as f:
    geojson = json.load(f)

# Création de l'application Dash
app = dash.Dash(__name__)
app.title = "Analyse des départements de France métropolitaine par l'étude de la prévalence selon la pathologie (données 2019)"
server = app.server

# Mise en page de l'application Dash
app.layout = html.Div([
    # Bandeau bleu avec le nom de l'application
    html.Div([
        html.H1(
            ["Analyse des départements de France métropolitaine par l'étude de la prévalence selon la pathologie (données 2019)"],
            style={'color': 'white', 'margin-left': '15px', 'margin-top':'5px','font-size': '20px', 'fontFamily':'Calibri'}
        ),
        html.H2(
            [
                "Par Adrien Bartoletti :      ",
                html.Span(
                    [

                        html.A("Github", href="https://github.com/StorkMiner", target="_blank", style={'color': 'White', 'textDecoration': 'underline'}),
                        "   -   ",

                        html.A("Linkedin", href="https://www.linkedin.com/in/adrien-bartoletti-9a57b4191/", target="_blank", style={'color': 'White', 'textDecoration': 'underline'})
                    ],
                    style={'font-size':'13px'}
                )
            ],
            style={'color': '#EEF2F8', 'margin-left': '15px', 'font-size': '15px', 'fontFamily':'Calibri', 'white-space':'pre'}
        ),
        html.H3(
            children=[
                html.I("Source : Assurance Maladie : ", style={'font-style': 'italic'}),
                html.A(
                    "https://www.assurance-maladie.ameli.fr/etudes-et-donnees/cartographie-effectif-patients-par-pathologie-age-sexe", 
                    href="https://www.assurance-maladie.ameli.fr/etudes-et-donnees/cartographie-effectif-patients-par-pathologie-age-sexe", 
                    target="_blank", 
                    style={'color': 'White', 'textDecoration': 'underline','font-style': 'italic'}
                )
            ],
            style={'color': '#EEF2F8', 'margin-left': '15px', 'margin-top': '15px', 'font-size': '11px', 'fontFamily':'Calibri, italic'}
        )
    ], style={'background-color': '#0C419A', 'padding': '5px', 'text-align': 'left'}),
    
    html.Div([
        # Volet gauche avec sélecteurs et statistiques
        html.Div([
            html.Label('Sélectionnez la pathologie :', style={'font-weight': 'bold','fontFamily':'calibri','font-size': '14px'}),
            dcc.Dropdown(
                id='pathology-dropdown',
                options=[{'label': pathology, 'value': pathology} for pathology in pathologies_list],
                value=pathologies_list[0],  # Valeur par défaut
                clearable=False,
                style={'width': '100%','margin-top': '5px','margin-bottom': '20px', 'fontFamily':'calibri','font-size': '13px'}
            ),
            html.Label('Sélectionnez le sexe :', style={'font-weight': 'bold', 'margin-top': '12px','fontFamily':'calibri','font-size': '14px'}),
            dcc.RadioItems(
                id='gender-radio',
                options=[
                    {'label': 'Ensemble', 'value': 9},
                    {'label': 'Homme', 'value': 0},
                    {'label': 'Femme', 'value': 1},
                ],
                value=9,
                labelStyle={'display': 'block'},
                style={'margin-top': '5px','margin-bottom': '20px','fontFamily':'calibri','font-size': '14px'}
            ),
            html.Label("Sélectionnez l'intervalle d'âge :", style={'font-weight': 'bold', 'margin-top': '11px','fontFamily':'calibri','font-size': '13px'}),
            dcc.RangeSlider(
                id='age-slider',
                min=0,
                max=95,
                step=5,
                marks={i: {'label': f'{i}', 'style': {'font-family': 'calibri', 'font-size': '10px'}} for i in range(0, 95, 10)},
                value=[0, 95],  # Valeur par défaut pour l'ensemble des âges
                tooltip={"placement": "bottom", "always_visible": True},
                updatemode='drag'
            ),
            html.Div(id='stat-text', style={'margin-top': '12px','fontFamily':'calibri','font-size': '14px'})  # Ajout de la division pour les statistiques
        ], style={'width': '20%', 'display': 'inline-block', 'vertical-align': 'top', 'padding': '20px', 'box-sizing': 'border-box'}),

        # Conteneur pour la carte à gauche
        html.Div([
            dcc.Loading(
                id="loading-1",
                type="circle",
                children=[
                    dcc.Graph(id='choropleth-map', style={'height': '80vh', 'width': '100%'})
                ]
            ),
        ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top', 'padding': '20px', 'box-sizing': 'border-box'}),

        # Conteneur pour le graphique et la table à droite
        html.Div([
            html.Label('Sélectionnez le type de graphique :', style={'font-weight': 'bold','fontFamily':'calibri','font-size': '14px'}),
            dcc.RadioItems(
                id='chart-type',
                options=[
                    {'label': 'Dispersion des départements selon la prévalence, par classe d\'âge', 'value': 'boxplot'},
                    {'label': 'Distribution du nombre de départements par la prevalence (%)', 'value': 'histogramme'}
                ],
                value='boxplot',  # Valeur par défaut
                labelStyle={'display': 'block'},
                style={'margin-top': '5px','margin-bottom': '20px','fontFamily':'calibri','font-size': '13px'}
            ),
            dcc.Loading(
                id="loading-2",
                type="circle",
                children=[
                    dcc.Graph(id='graph', style={'height': '40vh', 'width': '100%'}),
                ]
            ),
            dcc.Loading(
                id="loading-3",
                type="circle",
                children=[
                    dash_table.DataTable(
                        id='table',
                        columns=[
                            {'name': 'Classement', 'id': 'Classement'},
                            {'name': 'CODGEO', 'id': 'CODGEO'},
                            {'name': 'Département', 'id': 'NOM_DEP'},
                            {'name': 'Prévalence (%)', 'id': 'prev'}
                        ],
                        style_table={'height': '31vh', 'overflowY': 'auto'},
                        style_cell={'textAlign': 'center', 'padding': '5px', 'whiteSpace': 'normal','fontFamily':'calibri', 'fontSize': '13px'},
                        style_header={
                            'backgroundColor': '#0C419A',
                            'fontWeight': 'bold',
                            'color': 'white',
                            'textAlign': 'center'
                        },
                        style_data_conditional=[
                            {'if': {'column_id': 'Classement'}, 'width': '10%'},
                            {'if': {'column_id': 'CODGEO'}, 'width': '15%'},
                            {'if': {'column_id': 'NOM_DEP'}, 'width': '60%'},
                            {'if': {'column_id': 'prev'}, 'width': '15%'}
                        ],
                        sort_action='native',
                        sort_by=[{'column_id': 'Classement', 'direction': 'asc'}],  # Tri par défaut
                        filter_action='native',
                        page_size=10,
                    )
                ]
            ),
        ], style={'width': '30%', 'display': 'inline-block', 'vertical-align': 'top', 'padding': '20px', 'box-sizing': 'border-box'})
    ], style={ 'margin': '0 auto', 'width': '100%', 'display': 'flex', 'flex-wrap': 'wrap'})
])

@app.callback(
    [Output('choropleth-map', 'figure'),
     Output('graph', 'figure'),
     Output('table', 'data'),
     Output('stat-text', 'children')],
    [Input('gender-radio', 'value'),
     Input('pathology-dropdown', 'value'),
     Input('age-slider', 'value'),
     Input('chart-type', 'value')]
)

def update_graph(selected_gender, selected_pathology, selected_age_range, chart_type):
    min_age, max_age = selected_age_range

    if selected_gender == 9:  # Tous les genres
        filtered_df = df[(df['AGE_ORD'] >= min_age) & (df['AGE_ORD'] <= max_age) & (df['AGE_ORD'] != 99)]
    else:
        filtered_df = df[(df['sexe'] == selected_gender) & (df['AGE_ORD'] >= min_age) & (df['AGE_ORD'] <= max_age) & (df['AGE_ORD'] != 99)]

    filtered_df_boxplot = filtered_df[(filtered_df['patho_niv3'] == selected_pathology) & (filtered_df['Ntop'] != 0)]
    filtered_df_histogram = filtered_df[filtered_df['patho_niv3'] == selected_pathology]

    Npop = filtered_df_histogram.groupby(['CODGEO']).agg({'Npop': 'sum'}).reset_index()
    Ntop = filtered_df_histogram.groupby(['CODGEO']).agg({'Ntop': 'sum'}).reset_index()
    department_prevalence = pd.merge(Ntop, Npop, on="CODGEO", how="inner")
    department_prevalence["prev"] = round(department_prevalence["Ntop"] / department_prevalence["Npop"] * 100,3)
    # Ajoutez la colonne NOM_DEP avant le filtrage final
    department_prevalence = pd.merge(department_prevalence,df[['CODGEO', 'NOM_DEP']].drop_duplicates(),on="CODGEO",how="left")
    department_prevalence = department_prevalence[["CODGEO", "NOM_DEP", "prev", "Ntop", "Npop"]]
    department_prevalence = department_prevalence[department_prevalence['prev'] != 0]

    # Ajouter une colonne Classement en fonction de la prévalence
    department_prevalence['Classement'] = department_prevalence['prev'].rank(ascending=False, method='min').astype(int)


    stat = department_prevalence['prev'].describe().reset_index()
    stat['prev'] = round(stat['prev'], 3)
    Ntop_sum = department_prevalence['Ntop'].sum()
    Npop_sum = department_prevalence['Npop'].sum()
   ############################################################################################################## 

    if not department_prevalence.empty:
        department_prevalence['Intensité'] = 0

        decile = np.percentile(department_prevalence["prev"], np.arange(0, 100, 10))
        decile = decile.tolist()
        decile = sorted(decile)

        for i in range(0,len(decile)):

            if i == 0:
                department_prevalence.loc[department_prevalence['prev'] < decile[i], 'Intensité'] = 0
            else:
                if i > 0 :
                    department_prevalence.loc[(department_prevalence['prev'] >= decile[i-1]) & (department_prevalence['prev'] < decile[i]), 'Intensité'] = i

        department_prevalence.loc[department_prevalence['prev'] > decile[9], 'Intensité'] = 10    

            # Mise à jour de la carte choroplèthe
        min_prev = department_prevalence['Intensité'].min()
        max_prev = department_prevalence['Intensité'].max()
    else:
        # Gérer le cas où le DataFrame est vide : définir des valeurs par défaut
        department_prevalence['Intensité'] = [0]  # Une valeur par défaut pour éviter l'erreur
        min_prev = 0
        max_prev = 0

    
    fig_choropleth = px.choropleth_mapbox(
        department_prevalence,
        geojson=geojson,
        locations='CODGEO',
        featureidkey="properties.code",
        color='Intensité',
        color_continuous_scale="Jet",
        range_color=(min_prev, max_prev),
        mapbox_style="carto-positron",
        zoom=4.5,
        center={"lat": 46.603354, "lon": 1.888334},
        opacity=0.5,
        labels={'prev': 'Prévalence'}
    )

    fig_choropleth.update_layout(
        margin={"r": 0, "t": 30, "l": 0, "b": 0},
        title_text="Carte des départements selon l'intensité (de 0 à 10) de la prévalence. (Zoom ajustable)",
        title_font=dict(size=16, color='#0B4199', family='calibri')
    )

    # Mise à jour du graphique sélectionné
    if chart_type == 'boxplot':
        fig_graph = px.box(filtered_df_boxplot, x='AGE_ORD', y='prev')
        fig_graph.update_traces(
            marker=dict(color='#0B4199'),
            opacity=0.7
        )
        fig_graph.update_layout(
            #title_text='Dispersion des départements selon la prévalence, par classe d\'âge',
            title_font=dict(size=18, color='#0B4199'),
            xaxis_title='Classe d\'âge',
            yaxis_title='Prevalence',
            font=dict(family='calibri', size=12, color='#0B4199'),
            showlegend=False,
            margin={"r": 0, "t": 15, "l": 0, "b": 0}
        )
        fig_graph.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#CCCCCC')
        fig_graph.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#CCCCCC')
    else:
        # Créer un histogramme pour la distribution du nombre de CODGEO par prévalence
        fig_graph = px.histogram(department_prevalence, x='prev', nbins=50)
        fig_graph.update_traces(
            marker=dict(color='#0B4199'),
            opacity=0.7
        )
        fig_graph.update_layout(
            #title_text='Distribution du nombre départements par la prevalence (%)',
            title_font=dict(size=18, color='#0B4199'),
            xaxis_title='Prévalence',
            yaxis_title='Nombre de départements',
            font=dict(family='calibri', size=12, color='#0B4199'),
            showlegend=False,
            margin={"r": 0, "t": 15, "l": 0, "b": 0}
        )
        fig_graph.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#CCCCCC')
        fig_graph.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#CCCCCC')

    # Mise à jour du texte des statistiques
    stat_text = html.Div([
        html.Div([
            html.Span("Nombre de départements :", style={'font-weight': 'bold'}),
            f" {int(stat[stat['index'] == 'count']['prev'].values[0])}"
        ], style={'marginBottom': '5px','fontFamily':'calibri'}),
        html.Div([
            html.Span("Pop affectée :", style={'font-weight': 'bold'}),
            f" {Ntop_sum}"
        ], style={'marginBottom': '5px','fontFamily':'calibri'}),
        html.Div([
            html.Span("Pop totale consolidée:", style={'font-weight': 'bold'}),
            f" {Npop_sum}"
        ], style={'marginBottom': '5px','fontFamily':'calibri'}),
        html.P([],style={'marginBottom': '5px'}),
        html.Div([
            html.Span("Prévalence Nationale :", style={'font-weight': 'bold'}),
            f" {round(Ntop_sum/Npop_sum*100,3)}%"
        ], style={'marginBottom': '5px','fontFamily':'calibri'}),
        html.Div([
            html.Span("Min :", style={'font-weight': 'bold'}),
            f" {stat[stat['index'] == 'min']['prev'].values[0]}%"
        ], style={'marginBottom': '5px','fontFamily':'calibri'}),
        html.Div([
            html.Span("25% :", style={'font-weight': 'bold'}),
            f" {stat[stat['index'] == '25%']['prev'].values[0]}%"
        ], style={'marginBottom': '5px','fontFamily':'calibri'}),
        html.Div([
            html.Span("50% :", style={'font-weight': 'bold'}),
            f" {stat[stat['index'] == '50%']['prev'].values[0]}%"
        ], style={'marginBottom': '5px','fontFamily':'calibri'}),
        html.Div([
            html.Span("75% :", style={'font-weight': 'bold'}),
            f" {stat[stat['index'] == '75%']['prev'].values[0]}%"
        ], style={'marginBottom': '5px','fontFamily':'calibri'}),
        html.Div([
            html.Span("Max :", style={'font-weight': 'bold'}),
            f" {stat[stat['index'] == 'max']['prev'].values[0]}%"
        ], style={'marginBottom': '5px','fontFamily':'calibri'})
    ])

    return fig_choropleth, fig_graph, department_prevalence.to_dict('records'), stat_text

if __name__ == '__main__':
    app.run_server(debug=False, port=8050)

