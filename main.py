from cleaner import clean_excel, auto_clean, log_file
from pathlib import Path

if __name__ == "__main__":
    path = Path('input/')
    files = list(path.glob('*.xlsx')) + list(path.glob('*.csv'))

    if len(files) == 0:
        print("No hay archivos Excel en la carpeta input/ para procesar")
    elif len(files) == 1:
        print(f"{"-" * 20} Procesando archivo : {files[0].name} {"-" * 20}")
        df, stats = clean_excel(str(files[0]))
        df = auto_clean(df)
        name = Path(files[0].name).stem
        df.to_excel(f"output/clean_{name}.xlsx", index=False)
        log_file(name, stats)
    else:
        for i, file in enumerate(files):
            print(f"{i+1}. {file.name}")

        try:
            option = int(input("Selecciona un archivo para procesar (0 para todos): "))
            if option < 0 or option > len(files):
                print("Opción fuera de rango")
                exit()
        except ValueError:
            print("Opcion invalida")
            exit()

        if option == 0:
            for i, file in enumerate(files):
                print(f"{"-"*20} Procesando archivo N°{i+1} : {file.name} {"-"*20}")
                df, stats = clean_excel(str(file))
                df = auto_clean(df)
                name = Path(file.name).stem
                df.to_excel(f"output/clean_{name}.xlsx", index=False)
                log_file(name, stats)
        else:
            file = files[option - 1]
            print(f"{"-" * 20} Procesando archivo : {file.name} {"-" * 20}")
            df, stats = clean_excel(str(file))
            df = auto_clean(df)
            name = Path(file.name).stem
            df.to_excel(f"output/clean_{name}.xlsx", index=False)
            log_file(name, stats)


