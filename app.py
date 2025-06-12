# app.py
import streamlit as st
import os
import numpy as np
from ui_components import get_user_inputs
from simulation import run_simulation, simulate_paths_for_all_guarantees
from results_display import display_results, display_costs_summary
from mortality import load_istat_table, survival_probability
from utils import days_between_ages, get_guarantee_cost, price_guarantee_put
from summary_pdf import generate_summary_pdf

# Titel & Layout
st.set_page_config(page_title="UL Morte – Simulazione", layout="wide")
st.title("Simulazione della prestazione in caso di morte (con garanzia)")

# Lade Sterbetafel
df_mortality = load_istat_table("Tavole_di_mortalità.csv")

# Eingaben
inputs = get_user_inputs()
age = inputs["age"]
death_age = inputs["death_age"]
contribution = inputs["contribution"]
guarantee = inputs["guarantee"]
fonds_weights = inputs["fonds_weights"]
costs_percent = inputs["costs_percent"]
n_paths = inputs["n_paths"]

days = days_between_ages(age, death_age)
T = death_age - age

# Simulation starten
if inputs["ready"] and st.button("▶️ Avvia simulazione"):
    try:
        total_paths, total_sigma = run_simulation(contribution, fonds_weights, n_paths, days, initial_costs_pct=0.0)

        # Kostenschätzung
        K = contribution * guarantee
        put_price = price_guarantee_put(S0=contribution, K=K, T=T, sigma=total_sigma)
        guarantee_cost_pct = get_guarantee_cost(contribution, guarantee, T, total_sigma)
        total_annual_cost = costs_percent + guarantee_cost_pct

        # Laufende Kosten anwenden
        if total_annual_cost > 0:
            for year in range(1, days // 252 + 1):
                idx = year * 252
                if idx < total_paths.shape[0]:
                    total_paths[idx:] *= (1 - total_annual_cost / 100)

        # Endwerte berechnen
        final_fund_values = total_paths[-1]
        guaranteed_amount = contribution * guarantee
        end_values = np.maximum(final_fund_values, guaranteed_amount)

        # Statistiken
        payout_mean = np.mean(end_values)
        payout_min = np.min(end_values)
        payout_max = np.max(end_values)
        raw_prob = survival_probability(age, death_age, df_mortality)
        prob = min(max(raw_prob, 0.0), 1.0)

        # Value at Risk (95%)
        var_value = np.percentile(end_values, 5)
        cvar = np.mean(end_values[end_values <= var_value])

        # Ergebnisanzeige
        st.success(f"Ètà alla morte pianificata: {death_age} anni")
        st.caption(f"Probabilità di raggiungere {death_age} anni: {prob * 100:.2f}%")
        st.info(
            "ℹ️ La prestazione è garantita fino all'età pianificata. Se la persona vive più a lungo, "
            "il fondo resta investito e la prestazione sarà calcolata al momento del decesso."
        )

        display_results(end_values, total_paths, death_age)
        display_costs_summary(costs_percent, guarantee_cost_pct, total_annual_cost)

        st.markdown(
            f"### 📉 Value at Risk (VaR 95%)\n"
            f"- **VaR (5%-Quantile):** {var_value:,.2f} €\n"
            f"- **Conditional VaR (Media sotto il 5%)**: {cvar:,.2f} €"
        )

        # Speichere PDF-Daten in Session State
        st.session_state["pdf_ready"] = True
        st.session_state["pdf_args"] = {
            "age": age,
            "contribution": contribution,
            "death_age": death_age,
            "fonds_weights": fonds_weights,
            "total_sigma": total_sigma,
            "costs_percent": costs_percent,
            "n_paths": n_paths,
            "df_mortality": df_mortality
        }

    except Exception as e:
        st.error(f"❌ Errore: {e}")

else:
    st.info("🔐 La simulazione è attiva solo con una somma di allocazione del 100%.")

# PDF Exportblock nach Simulation
if st.session_state.get("pdf_ready"):
    if st.button("📄 Esporta confronto garanzie in PDF"):
        args = st.session_state["pdf_args"]
        guarantee_levels = [0.8, 0.9, 1.0]

        total_paths_by_guarantee, _ = simulate_paths_for_all_guarantees(
            args["contribution"], args["fonds_weights"], args["n_paths"],
            days_between_ages(args["age"], args["death_age"]), guarantee_levels
        )

        pdf_path = generate_summary_pdf(
            args["age"], args["contribution"], args["death_age"],
            args["fonds_weights"], args["total_sigma"],
            args["costs_percent"], args["n_paths"],
            args["df_mortality"], total_paths_by_guarantee
        )

        if pdf_path and os.path.exists(pdf_path):
            st.success("✅ Il PDF è stato generato con successo!")
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="📅 Scarica il PDF del confronto",
                    data=f.read(),
                    file_name="confronto_garanzie.pdf",
                    mime="application/pdf"
                )
        else:
            st.error("❌ Errore durante la generazione del PDF.")
