import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import copy
import plotly_express as px
from datetime import date, timedelta
from utils import (
    DATASET_OPTIONS,
    filter_dataframe,
    return_wanted_dataset,
    drop_non_dates,
    setup_data,
)
import plotly.graph_objs as go
from dash.dependencies import Input, Output


# Loading data and external assets
df_deaths, df_recovered, df_total = setup_data()

# Preprocessing
for df in [df_total, df_recovered, df_deaths]:
    df.dropna(subset=["continent", "Country/Region"], inplace=True)

# Input Values and Labels
CONTINENTS_OPTIONS = [{"label": "All", "value": "All"}]
CONTINENTS_OPTIONS.extend(
    [
        {"label": continent, "value": continent}
        for continent in df_total["continent"].unique()
    ]
)
COUNTRIES_OPTIONS = [{"label": "All", "value": "All"}]
COUNTRIES_OPTIONS.extend(
    [
        {"label": country, "value": country}
        for country in df_total["Country/Region"].unique()
    ]
)

LOGO = (
    "https://images.plot.ly/logo/new-branding/plotly-logomark.png"  # TODO: Update logo
)

THEME = {
    "dark": True,
    "detail": "#375a7f",
    "primary": "#303030",
    "secondary": "#444",
}

# Defining app
app = dash.Dash(external_stylesheets=[dbc.themes.DARKLY])

app.layout = dbc.Container(
    [
        dcc.Store(id="data-store"),
        # Navbar
        dbc.Navbar(
            [
                html.A(
                    # Use row and col to control vertical alignment of logo / brand
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src=LOGO, height="30px")),
                            dbc.Col(dbc.NavbarBrand("vira!ert", className="ml-2")),
                        ],
                        align="center",
                        no_gutters=True,
                    ),
                    href="#",
                ),
            ],
            dark=True,
        ),
        # Padding
        dbc.Row(html.Div(className="padding-row")),
        # First Row
        dbc.Row(
            [
                # Controls
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                html.H4("Plot Filters", className="card-title-custom"),
                                dbc.CardBody(
                                    [
                                        html.P("Filter by date"),
                                        dcc.DatePickerSingle(
                                            id="dp_date",
                                            date=f"{date.today()-timedelta(days=2)}",
                                            display_format="D-MMM-YY",
                                            max_date_allowed=f"{date.today()-timedelta(days=2)}",
                                            className="dash-bootstrap",
                                            style={
                                                # "width": "360px",
                                                "margin": "0 0 0 0",
                                            },
                                        ),
                                        html.P(
                                            "Filter by type of case",
                                            className="filter-paragraph",
                                        ),
                                        dcc.Dropdown(
                                            id="dd_dataset",
                                            options=DATASET_OPTIONS,
                                            multi=False,
                                            value="Confirmed",
                                            className="dash-bootstrap",
                                        ),
                                        html.P(
                                            "Filter by continent",
                                            className="filter-paragraph",
                                        ),
                                        dcc.Dropdown(
                                            id="dd_continent",
                                            options=CONTINENTS_OPTIONS,
                                            multi=False,
                                            value="All",
                                            className="dash-bootstrap",
                                        ),
                                        html.P(
                                            "Data transformation",
                                            className="filter-paragraph",
                                        ),
                                        dbc.RadioItems(
                                            id="radio_scale",
                                            options=[
                                                {
                                                    "label": "Normal Scale",
                                                    "value": "normal",
                                                },
                                                {
                                                    "label": "Logarithmic scale",
                                                    "value": "log",
                                                },
                                            ],
                                            value="normal",
                                            inline=True,
                                            className="dash-bootstrap",
                                        ),
                                        html.P(
                                            "Country with highest number of cases",
                                            className="filter-paragraph",
                                        ),
                                        html.Img(
                                            id="img_country",
                                            style={
                                                "height": "150px",
                                                "width": "250px",
                                                "marginBottom": "15px",
                                                "marginLeft": "10px",
                                            },
                                        ),
                                    ]
                                ),
                            ]
                        )
                    ],
                    width=4,
                ),
                # Statistics and Plot
                dbc.Col(
                    [
                        dbc.Row(
                            # Statistics
                            dbc.Col(
                                dbc.Card(
                                    [
                                        html.H4(
                                            "Summary Statistics",
                                            className="card-title-custom",
                                        ),
                                        dbc.CardBody(
                                            [
                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            [
                                                                html.P(
                                                                    "Number of Confirmed Cases"
                                                                ),
                                                                html.H4(
                                                                    "1346234",
                                                                    id="h4_confirmed",
                                                                ),
                                                            ],
                                                            width=4,
                                                            style={
                                                                "text-align": "center"
                                                            },
                                                        ),
                                                        dbc.Col(
                                                            [
                                                                html.P(
                                                                    "Number of Deaths"
                                                                ),
                                                                html.H4(
                                                                    "1346234",
                                                                    id="h4_deaths",
                                                                ),
                                                            ],
                                                            width=4,
                                                            style={
                                                                "text-align": "center"
                                                            },
                                                        ),
                                                        dbc.Col(
                                                            [
                                                                html.P(
                                                                    "Number of Recoveries"
                                                                ),
                                                                html.H4(
                                                                    "1346234",
                                                                    id="h4_recoveries",
                                                                ),
                                                            ],
                                                            width=4,
                                                            style={
                                                                "text-align": "center"
                                                            },
                                                        ),
                                                    ]
                                                ),
                                            ],
                                        ),
                                    ]
                                ),
                                width=12,
                            ),
                        ),  # End Statistics
                        # Padding
                        dbc.Row(html.Div(className="padding-row")),
                        # Plot
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Card(
                                        [
                                            html.H4(
                                                "Main Graph",
                                                className="card-title-custom",
                                            ),
                                            dbc.CardBody(
                                                dcc.Graph(
                                                    id="graph_main",
                                                    style={"height": "35em"},
                                                )
                                            ),
                                        ]
                                    ),
                                    width=12,
                                ),
                            ]
                        ),
                    ],
                    width=8,
                ),
            ],
        ),
        # Padding
        dbc.Row(html.Div(className="padding-row")),
        # Second row
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                html.H4(
                                    "Number of Cases",
                                    className="card-title-custom",
                                ),
                                dbc.CardBody(
                                    [
                                        html.P("Filter by type of plot"),
                                        dbc.RadioItems(
                                            id="radio_graph",
                                            options=[
                                                {
                                                    "label": "Geoplot",
                                                    "value": "total",
                                                },
                                                {
                                                    "label": "Barplot",
                                                    "value": "percentage",
                                                },
                                            ],
                                            value="total",
                                            inline=True,
                                            className="dash-bootstrap",
                                            style={"marginBottom": "2em"},
                                        ),
                                        dcc.Graph(id="graph_map"),
                                    ]
                                ),
                            ]
                        ),
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                html.H4(
                                    "Cases Over Time",
                                    className="card-title-custom",
                                ),
                                dbc.CardBody(
                                    [
                                        html.P(
                                            "Filter by Country",
                                        ),
                                        dcc.Dropdown(
                                            id="dd_country",
                                            options=COUNTRIES_OPTIONS,
                                            multi=False,
                                            value="All",
                                            className="dash-bootstrap",
                                            style={"marginBottom": "1em"},
                                        ),
                                        dcc.Graph(id="graph_time"),
                                    ]
                                ),
                            ]
                        ),
                    ],
                    width=6,
                ),
            ],
        ),
    ],
    fluid=True,
)


#
# Callbacks
#
@app.callback(
    Output("h4_confirmed", "children"),
    [
        Input("dd_continent", "value"),
        Input("dp_date", "date"),
    ],
)
def cb_confirmed_cases(continent_types, date_picker):
    dff, month = filter_dataframe(df_total, continent_types, date_picker)
    return f"{dff[month].sum():,}"


@app.callback(
    Output("h4_deaths", "children"),
    [
        Input("dd_continent", "value"),
        Input("dp_date", "date"),
    ],
)
def cb_deaths(continent_types, date_picker):
    dff, month = filter_dataframe(df_deaths, continent_types, date_picker)
    return f"{dff[month].sum():,}"


@app.callback(
    Output("h4_recoveries", "children"),
    [
        Input("dd_continent", "value"),
        Input("dp_date", "date"),
    ],
)
def cb_recoveries(continent_types, date_picker):
    dff, month = filter_dataframe(df_recovered, continent_types, date_picker)
    return f"{dff[month].sum():,}"


@app.callback(
    Output("img_country", "src"),
    [
        Input("dd_continent", "value"),
        Input("dp_date", "date"),
        Input("dd_dataset", "value"),
    ],
)
def cb_country_with_max_cases(continent_types, date_picker, dataset_types):
    ds = return_wanted_dataset(df_total, df_deaths, df_recovered, dataset_types)
    dff, month = filter_dataframe(ds, continent_types, date_picker)
    highest_country = dff[dff[month] == dff[month].max()]
    country: str = highest_country["iso_code"].iloc[0]
    flag_link = f"https://cdn.jsdelivr.net/gh/hampusborgos/country-flags@main/svg/{str(country[:2]).lower()}.svg"
    return flag_link


@app.callback(
    Output("graph_main", "figure"),
    [
        Input("dd_continent", "value"),
        Input("dp_date", "date"),
        Input("dd_dataset", "value"),
        Input("radio_scale", "value"),
    ],
)
def cb_graph_main(continent_types, date_picker, dataset_types, data_transformation):
    df = return_wanted_dataset(df_total, df_deaths, df_recovered, dataset_types)

    dff, month = filter_dataframe(df, continent_types, date_picker)
    dff = copy.deepcopy(dff)
    dff["cases_per_capita"] = dff[month] / dff["population"]

    if data_transformation == "log":
        log_x = True
        log_y = True
    else:
        log_x = False
        log_y = False

    figure = px.scatter(
        dff,
        x="gdp_per_capita",
        y="cases_per_capita",
        log_x=log_x,
        log_y=log_y,
        color="continent",
        hover_data=["Country/Region"],
        template="plotly_dark",
        labels={  # replaces default labels by column name
            "gdp_per_capita": f"GDP Per Capita",
            "cases_per_capita": "Cases Per Capita",
            "continent": "Continent",
        },
    )

    return figure


@app.callback(
    Output("graph_map", "figure"),
    [
        Input("dd_continent", "value"),
        Input("dp_date", "date"),
        Input("dd_dataset", "value"),
        Input("radio_graph", "value"),
    ],
)
def cb_graph_map_bar(
    continent_types,
    date_picker,
    dataset_types,
    first_insight_graph_radio_items,
):
    ds = return_wanted_dataset(df_total, df_deaths, df_recovered, dataset_types)

    dff, month = filter_dataframe(ds, continent_types, date_picker)
    dff_sorted = dff.sort_values(by=[month], ascending=False)

    if first_insight_graph_radio_items == "total":
        fig = px.choropleth(
            dff_sorted,
            locations="iso_code",
            color=f"{month}",  # month is a date of the dff dataframe
            hover_name="Country/Region",  # column to add to hover information
            color_continuous_scale=list(reversed(px.colors.sequential.Plasma)),
            labels={  # replaces default labels by column name
                f"{month}": f"Confirmed Cases",
            },
        )
        fig.update_layout(height=450, margin={"r": 0, "t": 0, "l": 0, "b": 0})
        fig.update_layout(geo=dict(bgcolor="rgba(0,0,0,1)"))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,1)",
            plot_bgcolor="rgba(0,0,0,1)",
        )
    else:
        fig = px.bar(
            dff_sorted.head(20),
            x="Country/Region",
            y=f"{month}",
            template="plotly_dark",
            labels={  # replaces default labels by column name
                f"{month}": f"Confirmed Cases",
            },
        )

    return fig


@app.callback(
    Output("graph_time", "figure"),
    [Input("dd_country", "value")],
)
def cb_graph_time(country_type):
    if country_type == "All" or country_type is None:
        dff_total = drop_non_dates(df_total)
        dff_recoveries = drop_non_dates(df_recovered)
        dff_deaths = drop_non_dates(df_deaths)

        dff_total = dff_total.sum(axis=0)
        dff_recoveries = dff_recoveries.sum(axis=0)
        dff_deaths = dff_deaths.sum(axis=0)
        date = dff_total.index.tolist()
        listval_total = dff_total.values.tolist()
        listval_recoveries = dff_recoveries.values.tolist()
        listval_deaths = dff_deaths.values.tolist()
    else:
        dff_total = df_total[df_total["Country/Region"] == country_type]
        dff_recoveries = df_recovered[df_recovered["Country/Region"] == country_type]
        dff_deaths = df_deaths[df_deaths["Country/Region"] == country_type]

        dff_total = drop_non_dates(dff_total)
        dff_recoveries = drop_non_dates(dff_recoveries)
        dff_deaths = drop_non_dates(dff_deaths)

        listval_total = dff_total.values.tolist()[0]
        listval_recoveries = dff_recoveries.values.tolist()[0]
        listval_deaths = dff_deaths.values.tolist()[0]

        date = dff_recoveries.columns.tolist()

    data = []
    third_insight_total = go.Scatter(
        x=date, y=listval_total, mode="lines", name="Confirmed Cases"
    )

    third_insight_deaths = go.Scatter(
        x=date, y=listval_deaths, mode="lines", name="Deaths"
    )

    third_insight_recovered = go.Scatter(
        x=date, y=listval_recoveries, mode="lines", name="Recovered Cases"
    )

    data.append(third_insight_total)
    data.append(third_insight_deaths)
    data.append(third_insight_recovered)

    third_insight_layout = {
        "title": "Nr. of Covid Confirmed, Recovered, Deaths",
        "yaxis": {
            "title": "Nr of Covid-19 Cases",
            "gridcolor": "#283442",
            "linecolor": "#506784",
        },
        "xaxis": {"gridcolor": "#283442", "linecolor": "#506784"},
        "paper_bgcolor": "rgba(0,0,0,1)",
        "plot_bgcolor": "rgba(0,0,0,1)",
    }

    figure = dict(data=data, layout=third_insight_layout)
    return figure


if __name__ == "__main__":
    app.run_server(debug=True, port=8888)
