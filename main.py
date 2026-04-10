from cleaner import clean_excel, normalize_text_values, normalize_dates, normalize_rut
import json

with open('config.json', 'r', encoding='utf-8') as file:
    config_json = json.load(file)


if __name__ == "__main__":
    df = clean_excel(config_json['input_file'])
    if config_json['text_columns']:
        df = normalize_text_values(df,config_json['text_columns'])
    if config_json['date_columns']:
        df = normalize_dates(df, config_json['date_columns'])
    if config_json['rut_columns']:
        df = normalize_rut(df, config_json['rut_columns'])

    df.to_excel(config_json['output_file'], index=False)


