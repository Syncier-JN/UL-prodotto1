from fund_forecast import get_mu_sigma, simulate_multiple_paths
import numpy as np

def simulate_paths_for_all_guarantees(contribution, fonds_weights, n_paths, days, guarantee_levels):
    """
    Simuliert Fondsverläufe für verschiedene Garantien (z.B. 80%, 90%, 100%).

    Args:
        contribution (float): Einmalbeitrag in EUR.
        fonds_weights (list): Liste von (Fondsname, Gewicht)-Tupeln.
        n_paths (int): Anzahl Monte-Carlo-Simulationen.
        days (int): Dauer der Simulation in Börsentagen.
        guarantee_levels (list of float): z.B. [0.8, 0.9, 1.0]

    Returns:
        dict: guarantee_level → simulated paths (ndarray)
        dict: guarantee_level → durchschnittliche Volatilität (sigma)
    """
    total_paths_by_guarantee = {}
    sigma_by_guarantee = {}

    for guarantee in guarantee_levels:
        total_paths = None
        total_sigma = 0

        for fond, weight in fonds_weights:
            mu, sigma, S0 = get_mu_sigma(fond)
            total_sigma += sigma * (weight / 100)
            fund_contribution = contribution * (weight / 100)
            scaling_factor = fund_contribution / S0

            paths = simulate_multiple_paths(S0, mu, sigma, days, n_paths)
            paths *= scaling_factor

            if total_paths is None:
                total_paths = paths
            else:
                total_paths += paths

        sigma_by_guarantee[guarantee] = total_sigma
        total_paths_by_guarantee[guarantee] = total_paths

    return total_paths_by_guarantee, sigma_by_guarantee

def run_simulation(contribution, fonds_weights, n_paths, days, initial_costs_pct=0.0):
   """
   Simuliert die Entwicklung eines Portfolios aus Fondsanteilen.
   Args:
       contribution (float): Einmaliger Beitrag in EUR (brutto).
       fonds_weights (list): Liste von (Fondsname, Gewicht)-Tupeln.
       n_paths (int): Anzahl Simulationspfade.
       days (int): Anlagedauer in Börsentagen.
       initial_costs_pct (float): Einmalige Einstiegskosten in % (optional).
   Returns:
       ndarray: Wertverlauf des Portfolios über alle Tage (EUR), shape: [days, n_paths]
       float: Durchschnittliche Volatilität (gewichtetes sigma)
   """
   total_paths = None
   total_sigma = 0
   
   net_contribution = contribution * (1 - initial_costs_pct / 100)
   
   for fond, weight in fonds_weights:
       mu, sigma, S0 = get_mu_sigma(fond)
       weight_ratio = weight / 100
       total_sigma += sigma * weight_ratio
       fund_contribution = net_contribution * weight_ratio
       n_shares = fund_contribution / S0
       # Fonds-Kursverlauf simulieren
       paths = simulate_multiple_paths(S0, mu, sigma, days, n_paths)
       # Positionwert = Kurs × Anzahl Anteile
       paths_value = paths * n_shares
       if total_paths is None:
           total_paths = paths_value
       else:
           total_paths += paths_value
   return total_paths, total_sigma