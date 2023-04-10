from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import numpy as np
import statsmodels as sm
from scipy.stats import ttest_1samp
from statsmodels.stats.power import TTestPower
import plotly.express as px
import plotly.offline as pyo
import plotly.io as pio
from jupyter_dash import JupyterDash
from dash import Dash, dcc, html, Input, Output
from dash.dependencies import State
import chart_studio.plotly as py

app = Dash(__name__)

app.layout = html.Div([
    html.H1("P-value Simulation"),
    # html.Div([
    html.H4('# of Sims:', style={'display':'inline-block','margin-left':20,'margin-right':5}),
    dcc.Input(
    id='nSims',
    value='Initial Value',
    type = "number",
        ),
    # ]),
    # html.Div([
    html.H4('Sample Mean:', style={'display':'inline-block','margin-left':20,'margin-right':5}),
    dcc.Input(
    id='sample-mean',
    value='Initial Value',
    type = "number",
    ),
    # ]),
    # html.Div([
    html.H4('Sample Size:', style={'display':'inline-block','margin-left':20,'margin-right':5}),
    dcc.Input(
    id='sample-size',
    value='Initial Value',
    type = "number",
    ),
    # ])
    html.H4('Std. Dev:', style={'display':'inline-block','margin-left':20,'margin-right':5}),
    dcc.Input(
    id='std-dev',
    value='Initial Value',
    type = "number",
    ),
    html.Br(),
    html.Button('Submit', id='submit_val'),
    html.Div(id='container-button-basic',
             children='Enter all parameters and click submit'),
    html.Hr(),
    html.Label('Output'),
    html.Div(id='output-submit')
])

@app.callback(
    Output('output-submit', 'children'),
        [Input('submit_val', 'n_clicks'),
        #  Input('input-1-submit', 'n_blur'),
        #  Input('input-2-submit', 'n_submit'),
        #  Input('input-2-submit', 'n_blur')
         ],
        [State('nSims', 'value'),
        State('sample-mean', 'value'),
        State('sample-size', 'value'),
        State('std-dev', 'value')
        ]
)

# Use the below function to get all the input variables and calculate the p-values

def simulations_output(clicked, nSims, sample_mean, sample_size, std_dev):
    if clicked:
        p_value_list = [] # Initialize a list that will store all the p-values
        np.random.seed(1)
        for i in range(1,nSims):
            x = np.random.normal(loc=sample_mean, scale=std_dev, size=sample_size)
            t_stat, p_value = ttest_1samp(x, popmean=100)
            p_value_list.insert(i,p_value)
        # return p_value_list

        hist_df = pd.DataFrame({"p_values":p_value_list})
        bars = 20
        fig = px.histogram(hist_df, x="p_values")
        fig.update_traces(xbins=dict( # bins used for histogram
                start=0.0,
                end=1.0,
                size=0.05
            ))
        fig.update_layout(yaxis_range=[0,nSims], yaxis_title="Frequency of p-values", margin=dict(l=5, r=5, t=5, b=5))
        fig.add_hline(y=nSims/bars, line_width=3, line_dash="dash", line_color="red")
        return fig.show()
    
if __name__ == '__main__':
    app.run_server(debug=True)
