from fpdf import FPDF
import tempfile
import numpy as np
from utils import get_guarantee_cost, price_guarantee_put
from utils import days_between_ages
import datetime
import os

class BasePDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)

    def header(self):
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, "Confronto delle prestazioni (profilo MiFID)", ln=True, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Pagina {self.page_no()}", 0, 0, "C")



def generate_mifid_summary_pdf(age, contribution, death_age, mifid_class, mu, sigma, costs_percent, n_paths, total_paths_by_guarantee):

    """
    Generiert ein PDF mit Simulationszusammenfassung je Garantielevel.
    Args:
        age (int)
        contribution (float)
        death_age (int)
        mifid_class (str)
        mu (float): Erwartete Rendite
        sigma (float): Volatilität
        costs_percent (float): jährliche Kosten
        n_paths (int)
        total_paths_by_guarantee (dict): {guarantee_level: ndarray [days, n_paths]}
    Returns:
        str: Pfad zur PDF-Datei

    """

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "📄 Simulazione UL Morte – Profilo MiFID", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Età: {age} anni", ln=True)
    pdf.cell(0, 10, f"Età alla morte simulata: {death_age} anni", ln=True)
    pdf.cell(0, 10, f"Contributo iniziale: {contribution:,.2f} €", ln=True)
    pdf.cell(0, 10, f"Classe di rischio: {mifid_class}", ln=True)
    pdf.cell(0, 10, f"Rendimento atteso: {mu*100:.2f} %", ln=True)
    pdf.cell(0, 10, f"Volatilità stimata: {sigma*100:.2f} %", ln=True)
    pdf.cell(0, 10, f"Costi annuali complessivi: {costs_percent:.2f} %", ln=True)
    pdf.cell(0, 10, f"Numero simulazioni Monte Carlo: {n_paths}", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "📊 Risultati per livello di garanzia:", ln=True)
    pdf.set_font("Arial", "", 12)

    for guarantee, paths in total_paths_by_guarantee.items():
        final_values = paths[-1, :]
        guaranteed_amount = contribution * guarantee
        end_values = np.maximum(final_values, guaranteed_amount)
        mean = np.mean(end_values)
        min_ = np.min(end_values)
        max_ = np.max(end_values)
        var_5 = np.percentile(end_values, 5)
        cvar = np.mean(end_values[end_values <= var_5])
        pdf.ln(5)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, f"🔒 Garanzia {int(guarantee * 100)}%", ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.cell(0, 8, f"- Capitale garantito: {guaranteed_amount:,.2f} €", ln=True)
        pdf.cell(0, 8, f"- Prestazione media simulata: {mean:,.2f} €", ln=True)
        pdf.cell(0, 8, f"- Minimo / Massimo: {min_:,.2f} € / {max_:,.2f} €", ln=True)
        pdf.cell(0, 8, f"- VaR 95%: {var_:,.2f} €", ln=True)
        pdf.cell(0, 8, f"- CVaR (media sotto 5%): {cvar:,.2f} €", ln=True)

    # Speichern
    folder = "pdf_output"
    os.makedirs(folder, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(folder, f"mifid_simulation_{timestamp}.pdf")
    pdf.output(file_path)
    return file_path

