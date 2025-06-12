# config.py
FONDS = {
   "MACFX": "MFS Conservative Allocation Fund",
   "AOK": "iShares Core 30/70 ETF",
   "OICAX": "JPM Conservative Growth A",
   "MCKKX": "MainStay Conservative Allocation Fund",
   "FTCIX": "Franklin Conservative Allocation"
}
GARANTIEN = {
   "100%": 1.0,
   "90%": 0.9,
   "80%": 0.8
}
# Mapping: Risikoklasse → Liste von Fonds-Tickern
MIFID_FONDS = {

    "1 - Prudente": [  # Sehr konservativ
        {
            "name": "iShares 7-10 Year Treasury Bond ETF",
            "isin": "US4642874402",
            "ticker": "IEF",  # Xetra
        },
        {
            "name": "DWS Invest Euro Money Market",
            "isin": "LU0145646145",
            "ticker": "0P00000T5A.F",  # Morningstar Notation
        },
        {
            "name": "Lyxor Euro Government Bond 1–3Y UCITS ETF",
            "isin": "LU1598698815",
            "ticker": "EG13.DE",
        }
    ],

    "2 - Moderato": [  # Konservativ
        {
            "name": "iShares Euro Aggregate Bond 1–5y",
            "isin": "IE00B1FZS913",
            "ticker": "EUNA.DE"
        },
        {
            "name": "UBS Strategy Balanced Sustainable (EUR)",
            "isin": "LU0067412154",
            "ticker": "0P00000KFX.F"
        }
    ],

    "3 - Bilanciato": [  #    Moderat
        {
            "name": "iShares Core MSCI World UCITS ETF",
            "isin": "IE00B4L5Y983",
            "ticker": "IWDA.AS"
        },
        {
            "name": "Vanguard LifeStrategy 40% Equity",
            "isin": "IE00BMVB5P51",
            "ticker": "VLS40.L"
        }
   ],
   "4 - Dinamico": "848182.DE",          # Allianz Wachstum Europa A EUR
    "5 - Aggressivo": "DWS0QF.DE"         # DWS Invest GLobal Emerging Markets Equities LC
}
