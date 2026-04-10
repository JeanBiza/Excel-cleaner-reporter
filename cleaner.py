import unicodedata
import pandas as pd



def transform(col: str) -> str:
    col = col.lower()
    col = col.strip()
    col = col.replace(' ', '_')
    normalized = unicodedata.normalize('NFKD', col)
    col = normalized.encode('ASCII', 'ignore').decode('ASCII')
    return col

def parse_date(value):
    if pd.isna(value):
        return None
    formats = [
        '%Y-%m-%d',  # 1990-05-12
        '%d-%m-%Y',  # 12-05-1990
        '%m-%d-%Y',  # 05-12-1990
        '%d-%m-%y',  # 12-05-90
        '%y-%m-%d',  # 90-05-12

        '%d/%m/%Y',  # 12/05/1990
        '%m/%d/%Y',  # 05/12/1990
        '%Y/%m/%d',  # 1990/05/12
        '%d/%m/%y',  # 12/05/90
        '%m/%d/%y',  # 05/12/90

        '%Y.%m.%d',  # 1990.05.12
        '%d.%m.%Y',  # 12.05.1990
        '%m.%d.%Y',  # 05.12.1990
        '%d.%m.%y',  # 12.05.90

        '%d %m %Y',  # 12 05 1990
        '%d %B %Y',  # 12 Mayo 1990
        '%d %b %Y',  # 12 May 1990
        '%B %d %Y',  # Mayo 12 1990

        '%Y%m%d',  # 19900512
        '%d%m%Y',  # 12051990
    ]
    for fmt in formats:
        try:
            return pd.to_datetime(str(value), format=fmt).strftime('%Y-%m-%d')
        except Exception:
            continue
    return None

def format_rut(value):
    if pd.isna(value):
        return None
    clean = value.replace(' ', '').replace('.', '').replace('-', '').replace(',', '')
    num = clean[-1:]
    body = f"{int(clean[:-1]):,}".replace(',', '.')
    rut = f"{body}-{num.upper()}"
    return rut

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

def normalize_dates(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    for col in columns:
        df[col] = df[col].apply(parse_date)
    return df

def normalize_rut(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    for col in columns:
        df[col] = df[col].apply(format_rut)
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
