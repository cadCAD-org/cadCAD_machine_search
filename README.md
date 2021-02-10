# cadCAD_machine_search
cadCAD tools for preparing & analyzing experiments where
 large-scale machine search for selecting parameters are involved.

 *Sensitivity analysis for the Prey vs Predator populations in regards to 
 parameters*

![Sensitivity analysis on the Prey & Predator model](https://i.imgur.com/CkQsjU2.png)

## Installation

The recommended way is through pip:

```sh
pip install cadCAD_machine_search
```

Alternatively, you can install a branch directly from the repository through:

```sh
pip install git+https://github.com/danlessa/cadCAD_machine_search@master
```

## Usage
### Tools

#### Cartesian product for parameter sweeping

```python
# The sweep_cartesian_product makes it easy to create large-scale simulations
from cadcad_machine_search.tools import sweep_cartesian_product

PARAMS_TO_SWEEP = {    
    "predator_death_const": np.linspace(0.9, 1.1, 5),
    "prey_death_const": np.linspace(0.02, 0.04, 5),
    "dt": np.linspace(0.04, 0.06, 4)
    }

sweep_params = sweep_cartesian_product(PARAMS_TO_SWEEP)

params = {
    "prey_birth_rate": [1.0],
    "predator_birth_rate": [0.01],
    **sweep_params
```

### Visualizations

#### Sensitivity of a KPI towards a set of control parameters

```python
from cadcad_machine_search.visualizations import kpi_sensitivity_plot

# KPI: prey population is 3x above the predator populaton at least 90% of the time
control_params = set(sweep_params.keys())
WEIGHT = 3.0
kpi = lambda df: (df.prey_population > WEIGHT * df.predator_population).mean() > 0.9
kpi_sensitivity_plot(df, kpi, control_params)
```

## Examples

We recommend having a look on the notebooks/ folder, as we have a P&P model
that makes usage of the parameter sweep helpers together with the KPI sensitivity
visualization.

