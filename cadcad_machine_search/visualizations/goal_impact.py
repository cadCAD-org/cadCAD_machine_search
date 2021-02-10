from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import normalize
from sklearn.preprocessing import MinMaxScaler
import plotly.figure_factory as ff
from typing import Dict
import numpy as np
import pandas as pd

def plot_goal_ternary(df: pd.DataFrame,
                 kpis: Dict[str, callable],
                 goals: Dict[str, callable],
                 control_params: set) -> None:
    """
    Arguments
    ---
    df: Observation dataframe
    kpis: Dictionary of funtions that scores a given combination of control params
    goals: Dictionary of how the goals are metrified. One of the keys must be 'combined'
    control_params: Set of the columns to be used as features.
    """

    if len(goals.keys()) != 4:
        raise ValueError('The `goals` dictionary must have four elements')

    # Group by the control params and apply kpi to each combination
    output = []
    for kpi, kpi_function in kpis.items():
        s = df.groupby(list(control_params)).apply(kpi_function)
        s.name = kpi
        output.append(s)

    # Generate a aggregated dataframe for training a regressor
    agg_df = pd.DataFrame(output).T.reset_index()

    # Get data
    y = agg_df.loc[:, kpis.keys()]
    X = agg_df.loc[:, control_params]

    # Perform a random forest regression on X->y
    rf = RandomForestRegressor()
    rf.fit(X, y)

    # Use the regression to predict values for each simulation
    coords = rf.predict(X)

    # MinMax normalizer
    def norm(x): return (x - x.min()) / (x.max() - x.min())

    # Encapsulate RF regression results in a dict
    metrics = dict(zip(kpis.keys(), coords.T))
    metrics = {k: norm(v) for (k, v) in metrics.items()}


    labels = [k for k in goals.keys() if k != 'combined']

    x = goals[labels[0]](metrics)
    y = goals[labels[1]](metrics)
    z = goals[labels[2]](metrics)
    # Combined Goals definition
    kpi = norm(goals['combined']([x, y, z]))

    # Create a matrix for the sides of the triangle (shape: 3xN)
    xyz = np.stack([x, y, z]).T

    scaler = MinMaxScaler()
    # Normalize each side by MinMax
    xyz = scaler.fit_transform(xyz).T

    # Normalize each data point so that it sums to 1.0
    v = np.round(normalize(xyz, axis=0, norm='l2') ** 2, decimals=10)

    # Generate ternary plot
    fig = ff.create_ternary_contour(v,
                                    kpi,
                                    pole_labels=[labels[0],
                                                 labels[1],
                                                 labels[2]],
                                    interp_mode='cartesian',
                                    ncontours=15,
                                    colorscale='Viridis',
                                    showmarkers=True,
                                    showscale=True)
    fig.show()