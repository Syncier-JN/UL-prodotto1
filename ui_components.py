import streamlit as st
from config import FONDS, GARANTIEN

# Standard-Konfiguration (für app.py)
def get_user_inputs():
    st.sidebar.header("📋 Parametri del contratto")

    age = st.sidebar.number_input("Età di ingresso", min_value=18, max_value=100, value=38)
    death_age = st.sidebar.number_input("Età target (durata del contratto)", min_value=age + 1, max_value=120, value=90)
    contribution = st.sidebar.number_input("Contributo unico (EUR)", min_value=250, max_value=500_000, step=250, value=10_000)
    guarantee_label = st.sidebar.selectbox("Garanzia (%)", list(GARANTIEN.keys()))
    guarantee = GARANTIEN[guarantee_label]

    st.sidebar.markdown("---")
    costs_percent = st.sidebar.slider("Costi annuali di gestione (%)", 0.0, 5.0, 1.0, step=0.1)
    n_paths = st.sidebar.slider("Numero simulazioni (Monte Carlo)", 10, 200, 100, step=10)

    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Allocazione del fondo (max 5 fondi)")

    fonds_weights = []
    available_fonds = list(FONDS.keys())
    total_weight = 0

    for i in range(5):
        fond = st.sidebar.selectbox(f"Fondo {i + 1}", ["-"] + available_fonds, key=f"fond_{i}")
        weight = st.sidebar.number_input(f"% Fondo {i + 1}", min_value=0, max_value=100, step=5, value=0, key=f"weight_{i}")
        if fond != "-":
            fonds_weights.append((fond, weight))
            total_weight += weight

    ready = total_weight == 100
    if not ready:
        st.sidebar.warning("⚠️ La somma delle allocazioni deve essere 100%.")

    return {
        "age": age,
        "death_age": death_age,
        "contribution": contribution,
        "guarantee_label": guarantee_label,
        "guarantee": guarantee,
        "fonds_weights": fonds_weights,
        "costs_percent": costs_percent,
        "n_paths": n_paths,
        "ready": ready
    }

# Alternative Konfiguration (für app2.py – MiFID II Profil)
def get_user_inputs_mifid():
    st.subheader("🔧 Parametri contratto (profilo rischio MiFID)")

    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Età di ingresso", min_value=18, max_value=100, value=38)
        contribution = st.number_input("Contributo unico (EUR)", 250, 500_000, step=250, value=10_000)

    with col2:
        death_age = st.number_input("Età target (durata contratto)", min_value=age + 1, max_value=120, value=85)
        costs_percent = st.slider("Costi annuali (%)", 0.0, 5.0, 1.0, step=0.1)

    st.subheader("🧠 Profilo di rischio (MiFID II)")
    mifid_class = st.selectbox(
        "Seleziona il profilo:",
        ["1 - Prudente", "2 - Moderato", "3 - Bilanciato", "4 - Dinamico", "5 - Aggressivo"]
    )

    mifid_parameters = {
        "1 - Prudente":     {"mu": 0.02, "sigma": 0.05},
        "2 - Moderato":     {"mu": 0.03, "sigma": 0.08},
        "3 - Bilanciato":   {"mu": 0.04, "sigma": 0.12},
        "4 - Dinamico":     {"mu": 0.05, "sigma": 0.18},
        "5 - Aggressivo":   {"mu": 0.06, "sigma": 0.25}
    }

    params = mifid_parameters[mifid_class]
    n_paths = st.slider("Numero di simulazioni (Monte Carlo)", 10, 200, 100, step=10)
    ready = True if contribution > 0 else False

    return {
        "age": age,
        "death_age": death_age,
        "contribution": contribution,
        "mifid_class": mifid_class,
        "mu": params["mu"],
        "sigma": params["sigma"],
        "costs_percent": costs_percent,
        "n_paths": n_paths,
        "ready": ready
    }
