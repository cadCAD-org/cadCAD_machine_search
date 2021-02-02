import matplotlib.pyplot as plt
from sklearn.tree import plot_tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
import pandas as pd


def f(X: pd.DataFrame,
      y: pd.Series,
      target: str,
      ax_dt: object,
      ax_rf: object):
    """
    Fit DT and RF classifiers for summarizing the sensivity.
    """
    model = DecisionTreeClassifier(class_weight='balanced',
                                   max_depth=5,
                                   )
    rf = RandomForestClassifier()
    model.fit(X, y)
    rf.fit(X, y)

    df = (pd.DataFrame(list(zip(X.columns, rf.feature_importances_)),
                       columns=['features', 'importance'])
          .sort_values(by='importance', ascending=False)
          )

    plot_tree(model,
              rounded=True,
              proportion=True,
              fontsize=8,
              feature_names=X.columns,
              class_names=['threshold not met', 'threshold met'],
              filled=True,
              ax=ax_dt)
    ax_dt.set_title(
        f'Decision tree for {target}, score: {model.score(X, y) :.0%}. N: {len(X) :.2e}')
    sns.barplot(df.features, df.importance, ax=ax_rf, label='small')
    plt.setp(ax_rf.xaxis.get_majorticklabels(), rotation=45)
    ax_rf.set_title(f'Feature importance for the {target}')
    
    return df.assign(target=target)


def param_sensitivity_plot(df: pd.DataFrame, 
                         control_params: set,
                         target: str):
    """
    Plot the sensivity of the 'target' column vs
    a list of control parameters, which are data frame columns.
    """
    features = set(control_params) - {target}
    X = df.loc[:, features]
    y = (df[target] > 0)
    # Visualize
    fig, axes = plt.subplots(nrows=2,
                            figsize=(36, 12),
                            dpi=100,
                            gridspec_kw={'height_ratios': [3, 1]})
    f(X, y, 'target', axes[0], axes[1])
    return None