from cleaner import clean_excel, normalize_text_values


if __name__ == "__main__":
    df = clean_excel("input/test_clientes.xlsx")
    print(df)
    print(df.columns.tolist())
    print(normalize_text_values(df,['nombre_cliente', 'ciudad']))