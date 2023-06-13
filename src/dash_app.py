# Simple dashboard built with python dash using Boston housing price data set.
# Multiple tabs to view the data or fit a model using one of three common algorithms,
# select/deselect features, then updates a scatter plot with true vs. predicted prices.
#
# This file defines the view and controller functions, the model does the data+logic
# Note that the styling for the various panels is defined in assets/style.css
# which is automatically loaded by dash.

from model import Model

# Dash imports
from dash import Input, Output, dcc, html, Dash, dash_table
import plotly.graph_objs as go
from azure_ad import app_config

# Initialize the model and prepare the data
model = Model("data/housing.csv")

# Create the app
def init_dash_app(server):
    app = Dash(
        __name__,
        server=server,
        routes_pathname_prefix=app_config.DASH_ROUTE_PATHNAME,
        suppress_callback_exceptions=True,
    )

    app.layout = html.Div(
        [
            dcc.Tabs(
                id="tabs-controller",
                value="data_table",
                children=[
                    dcc.Tab(
                        label="Examine Data",
                        value="data_table",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        label="Data Summary",
                        value="data_summary",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        label="Model Evaluation",
                        value="show_model",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                ],
            ),
            html.Div(id="tabs-content"),
        ]
    )
    init_callbacks(app)
    return app


def init_callbacks(app):
    @app.callback(
        Output("tabs-content", "children"), [Input("tabs-controller", "value")]
    )
    def render_tab_content(tab):
        """
        Handler to update tab display when a different tab is clicked

        Parameters
        ----------
        tab
            input value which tracks which tab is clicked and showing

        Returns
        ------
        html
            structured dash component objects which get rendered to frontend layout code
        """
        if tab == "data_table":
            return html.Div(
                [
                    # Banner along top
                    html.H1("Housing Price Data", id="banner"),
                    dash_table.DataTable(
                        id="table",
                        columns=[{"name": i, "id": i} for i in model.data.columns],
                        style_table={
                            "overflowX": "auto",
                            "minWidth": "100%",
                            "width": "100%",
                            "maxWidth": "100%",
                        },
                        style_cell={
                            "overflow": "hidden",
                            "textOverflow": "ellipsis",
                            "minWidth": "80px",
                            "width": "80px",
                            "maxWidth": "80px",
                            "textAlign": "center",
                        },
                        data=model.data[:20].to_dict("records"),
                    ),
                ]
            )
        elif tab == "data_summary":
            trace1 = go.Bar(
                x=["< 1H OCEAN", "INLAND", "NEAR BAY", "NEAR OCEAN"],
                y=model.summary["young"],
                name="Houses 15yrs or newer",
                marker_color="rgb(239,179,171)",
            )
            trace2 = go.Bar(
                x=["< 1H OCEAN", "INLAND", "NEAR BAY", "NEAR OCEAN"],
                y=model.summary["medium"],
                name="Houses 15-30yrs old",
                marker_color="rgb(207, 81, 61)",
            )
            trace3 = go.Bar(
                x=["< 1H OCEAN", "INLAND", "NEAR BAY", "NEAR OCEAN"],
                y=model.summary["old"],
                name="Houses older than 30yrs",
                marker_color="rgb(147, 59, 39)",
            )
            return html.Div(
                [
                    dcc.Graph(
                        id="bar_plot",
                        figure=go.Figure(
                            data=[trace1, trace2, trace3],
                            layout=go.Layout(barmode="stack"),
                        ),
                    )
                ]
            )
        elif tab == "show_model":
            return html.Div(
                [
                    # Banner along top
                    html.H1("Housing Price Model", id="banner"),
                    # Right panel: x/y graph
                    html.Div(
                        [html.H2("Model Graph"), dcc.Graph(id="scatter")],
                        id="output_panel",
                    ),  # id of the panel is used by stylesheet
                    # Left panel: model controls
                    html.Div(
                        [
                            # Heading at top of panel
                            html.H2("Control Panel"),
                            # Drop-down list of algorithms
                            html.Label("Algorithm:", style={"fontWeight": "bold"}),
                            dcc.Dropdown(
                                id="algorithm",
                                options=[{"label": x, "value": x} for x in model.algos],
                                value=model.algos[0],
                            ),
                            # Checkboxes of features to include (by default all are on)
                            html.Label(
                                "Features to use:",
                                style={
                                    "fontWeight": "bold",
                                    "display": "block",
                                    "marginTop": "20px",
                                },
                            ),
                            dcc.Checklist(
                                id="features",
                                options=[
                                    {"label": x, "value": x}
                                    for x in model.features_list
                                ],
                                value=model.features_list,
                                labelStyle={"display": "block"},
                            ),
                        ],
                        # Id of the panel is used by stylesheet for layout
                        id="control_panel",
                    ),
                ]
            )

    # Callback handler, which updates the graph when the user chooses an algorithm
    # or selects/deselects features. When this happens, rerun the model and update
    # scatter plot of actual vs. predicted prices.
    @app.callback(
        Output("scatter", "figure"),  # The component that gets updated (only one)
        [
            Input(
                "algorithm", "value"
            ),  # The input component(s) that trigger the update
            Input("features", "value"),
        ],
    )  # (any change from these trigger function re-eval)
    def update_model(algorithm, features):  # Arguments correspond to the Inputs
        """
        Handler refits a model when algorithm/features are changed.
        Produces predictions and accuracy on training data which plotly can display

        Parameters
        ----------
        algorithm
            input value which selects which algorithm to use in fitting
        features:
            input value which is a list of checked features to use in fitting

        Returns
        ------
        dict
            data structured for a plotly chart along with display properties
        """
        housevals, predictions, r2 = model.fit_model(algorithm, features)
        print("*** %s with %d features: R2 = %.4f" % (algorithm, len(features), r2))

        # Return a dictionary that defines the graph of actual vs. predicted
        # prices; this gets interpreted and rendered in the browser by plotly
        gdata = [go.Scatter(x=housevals, y=predictions, mode="markers")]
        layout = {
            "title": "Predicted vs. Actual House Prices",
            "xaxis": {"title": "Actual Price", "rangemode": "nonnegative"},
            "yaxis": {"title": "Predicted Price", "rangemode": "nonnegative"},
            "annotations": [
                {"text": "R-squared = %.4f" % r2, "showarrow": False, "y": "top"}
            ],
        }
        return {"data": gdata, "layout": layout}
