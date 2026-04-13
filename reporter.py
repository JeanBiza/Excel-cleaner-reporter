import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
import pandas as pd
import io

def add_numeric_charts(df):
    return df.select_dtypes(include='number').columns.tolist()

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

    #Tabla de Nulos
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

    null_table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    null_table.setStyle(null_table_style)
    story.append(null_table)

    #Graficos
    numerics = add_numeric_charts(df)
    for col in numerics:
        fig, ax = plt.subplots()
        ax.hist(df[col].dropna(), bins=20)
        ax.set_title(f"Distribución: {col}")

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plt.close()

        story.append(Spacer(1, 20))
        img = Image(buffer, width=400, height=200)
        story.append(img)


    doc.build(story)