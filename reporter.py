import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
import pandas as pd

def generate_report(df: pd.DataFrame, filename: str, stats: dict):
    doc = SimpleDocTemplate(f"output/Report_{filename}.pdf", pagesize=letter)

    story = []
    styles = getSampleStyleSheet()

    text = f"Reporte de {filename}"
    par = Paragraph(text, styles["Title"])
    story.append(par)

    story.append(Spacer(1, 12))

    for key, value in stats.items():
        info = f"{key} = {value}"
        par = Paragraph(info, styles["Normal"])
        story.append(par)
        story.append(Spacer(1, 5))

    null_table_data = [["Columna", "Nulos", "% Completitud"]]
    for col in df.columns:
        nulls = df[col].isnull().sum()
        completeness = round((1 - nulls / len(df)) * 100, 1)
        null_table_data.append([col, str(nulls), f"{completeness}%"])

    null_table_title = f"Datos Nulos"
    par = Paragraph(null_table_title, styles["Title"])
    story.append(par)

    story.append(Spacer(1, 12))

    null_table = Table(null_table_data)
    story.append(null_table)

    doc.build(story)