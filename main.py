from cleaner import clean_excel, auto_clean
from pathlib import Path

if __name__ == "__main__":
    files = list(Path('input/').glob('*.xlsx'))

    if len(files) == 0:
        print("No hay archivos Excel en la carpeta input/ para procesar")
    elif len(files) == 1:
        print(f"{"-" * 20} Procesando archivo : {files[0].name} {"-" * 20}")
        df = clean_excel(str(files[0]))
        df = auto_clean(df)
        name = files[0].name
        df.to_excel(f"output/clean_{name}", index=False)
    else:
        for i, file in enumerate(files):
            print(f"{i+1}. {file.name}")

        try:
            option = int(input("Selecciona un archivo para procesar (0 para todos): "))
        except ValueError:
            print("Opcion invalida")
            exit()

        if option == 0:
            for i, file in enumerate(files):
                print(f"{"-"*20} Procesando archivo N°{i+1} : {file.name} {"-"*20}")
                df = clean_excel(str(file))
                df = auto_clean(df)
                name = file.name
                df.to_excel(f"output/clean_{name}", index=False)
        else:
            file = files[option - 1]
            print(f"{"-" * 20} Procesando archivo : {file.name} {"-" * 20}")
            df = clean_excel(str(file))
            df = auto_clean(df)
            name = file.name
            df.to_excel(f"output/clean_{name}", index=False)


