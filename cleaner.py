import unicodedata
import pandas as pd

def transform(col: str) -> str:
    col = col.lower()
    col = col.strip()
    col = col.replace(' ', '_')
    normalized = unicodedata.normalize('NFKD', col)
    col = normalized.encode('ASCII', 'ignore').decode('ASCII')
    return col

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop_duplicates()
    return df

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [transform(col) for col in df.columns]
    return df

def normalize_text_values(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    for col in columns:
        if pd.api.types.is_string_dtype(df[col]):
                df[col] = df[col].str.strip()
                df[col] = df[col].str.title()
        else:
            print(f"La columna '{col}' no es de tipo texto, saltando...")
    return df

def remove_empty_rows(df: pd.DataFrame) -> pd.DataFrame:
    df = df.replace(r'^\s*$', None, regex=True)
    df = df.dropna(how='all')
    return df

def clean_excel(filepath: str) -> pd.DataFrame:
    df = pd.read_excel(filepath)
    df = remove_duplicates(df)
    df = normalize_columns(df)
    df = remove_empty_rows(df)
    return df
