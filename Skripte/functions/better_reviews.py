import numpy as np
from scipy.stats import norm
import pandas as pd

def agresti_coull(game_data: pd.DataFrame, days_30 = True):
    #Agresti Coull-Intervall

    if not days_30:
        k = game_data["positive_reviews"]
        n = game_data["total_reviews"]
    else:
        positive_reviews = game_data["reviews_30_days_percentage"]
        n = game_data["reviews_30_days_total"]
        k = round(positive_reviews*n)

    from scipy.stats import norm

    # z-Wert für 95% Konfidenzintervall
    alpha = 0.05
    z = norm.ppf(1 - alpha/2)

    #adjustierten werte: 

    k_tilde = k + z**2 / 2
    n_tilde = n + z**2
    p_tilde = k_tilde/n_tilde
    SE_ac = np.sqrt((p_tilde*(1-p_tilde)/n_tilde))


    agresti_coull_intervall_lower_bound = p_tilde - z*SE_ac
    agresti_coull_intervall_lower_bound  = pd.Series(agresti_coull_intervall_lower_bound, name="agresti_coull_intervall_lower_bound")
    return agresti_coull_intervall_lower_bound