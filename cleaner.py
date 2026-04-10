import unicodedata
import re
import pandas as pd

date_formats = [
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

def is_rut(value):
    try:
        return bool(re.match(r'^\d{1,2}\.?\d{3}\.?\d{3}-[\dkK]$', str(value)))
    except:
        return False

def is_date(value):
    if pd.isna(value):
        return False
    for fmt in date_formats:
        try:
            date = pd.to_datetime(str(value), format=fmt).strftime('%Y-%m-%d')
            return True
        except Exception:
            continue
    return False

def is_phone(value):
    if pd.isna(value):
        return False
    try:
        if isinstance(value, float):
            value = int(value)
    except Exception:
        return False

    numbers = re.sub(r'\D', '', str(value))
    if numbers.startswith('56') and len(numbers) == 11:
        phone = numbers[2:]
    else:
        phone = numbers

    if re.match(r'^[2-9]\d{8}$', phone):
        return True
    return False

def is_email(value):
    if pd.isna(value):
        return False
    try:
        if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', str(value)):
            return True
    except Exception:
        return False

def detect_column_type(series: pd.Series) -> str:
    values = series.dropna()
    if len(values) == 0:
        return "unknown"

    rut_matches = sum(1 for v in values if is_rut(v))
    if rut_matches / len(values) > 0.7:
        return "rut"

    date_matches = sum(1 for v in values if is_date(v))
    if date_matches / len(values) > 0.7:
        return "date"

    phone_matches = sum(1 for v in values if is_phone(v))
    if phone_matches / len(values) > 0.7:
        return "phone"

    email_matches = sum(1 for v in values if is_email(v))
    if email_matches / len(values) > 0.7:
        return "email"

    num_matches = pd.to_numeric(values, errors='coerce').notna().sum()
    if num_matches / len(values) > 0.7:
        return "numeric"

    return "text"


def auto_clean(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.columns:
        col_type = detect_column_type(df[col])
        print(f"{col} → {col_type}")

        if col_type == "rut":
            df = normalize_rut(df, [col])
        elif col_type == "date":
            df = normalize_dates(df, [col])
        elif col_type == "text":
            df = normalize_text_values(df, [col])
        elif col_type == "phone":
            df = normalize_phone(df, [col])
        elif col_type == "email":
            df = normalize_email(df, [col])
    return df

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
    for fmt in date_formats:
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

def format_phone(value):
    if pd.isna(value):
        return None
    try:
        if isinstance(value, float):
            value = int(value)
    except:
        return None
    numbers = re.sub(r'\D', '', str(value))
    if numbers.startswith('56') and len(numbers) == 11:
        return f"+{numbers}"
    elif len(numbers) == 9:
        return f"+56{numbers}"
    else:
        return None

def format_email(value):
    if pd.isna(value):
        return None
    email = value.strip().lower()
    return email

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

def normalize_phone(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    for col in columns:
        df[col] = df[col].apply(format_phone)
        df[col] = df[col].astype(str)
        df[col] = df[col].replace('None', None)
    return df

def normalize_email(df: pd.DataFrame, columns: list):
    for col in columns:
        df[col] = df[col].apply(format_email)
    return df

def normalize_price():
    pass #Despues

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