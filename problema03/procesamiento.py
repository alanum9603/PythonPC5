import pandas as pd
import requests

def get_cambio_sunat() :
    try :
        url = f'https://api.apis.net.pe/v1/tipo-cambio-sunat'
        response = requests.get(url)
        data = response.json()
        compra = data['compra']
    except Exception as err :
        print(f'Error: {err}')
    else : 
        return compra

def columns_PEN_to_US(df) :
    cambio = get_cambio_sunat()
    df['Monto de inversión en US'] = df['MONTO DE INVERSIÓN'] * cambio
    df['Monto de transferencia en US'] = df['MONTO DE TRANSFERENCIA 2020'] * cambio
    return df

def replace_values_column(df, column) :
    df[column] = df[column].str.replace(',', '')
    df[column] = df[column].str.replace(' ', '')
    return df

def new_column_Estado1(x) :
    match x :
        case 'Actos Previos' :
            return 'Actos Previos'
        case 'Convenio y/o Contrato Resuelto' :
            return 'Resuelto'
        case 'En Ejecución' :
            return 'Ejecucion'
        case 'Concluido' :
            return 'Concluido'  

def new_column_Estado2(x) :
    match x :
        case 'Actos Previos' :
            return 1
        case 'Resuelto' :
            return 2
        case 'Ejecucion' :
            return 3
        case 'Concluido' :
            return 4

def __init__() :
    ruta = '/workspaces/PythonPC5/problema03/src/reactiva.xlsx'

    df = pd.read_excel(ruta, 'TRANSFERENCIAS 2020')

    # Eliminando columnas repetidas
    df = df.drop(columns=['ID','TIPO MONEDA.1'])

    #Reemplazando valores de columnas con datos que contienen ',', espacios
    df = replace_values_column(df=df,column='DISPOSITIVO LEGAL')
    
    #Creando nuevas columnas para cambio a dolares
    df = columns_PEN_to_US(df=df)

    #Hacemos el reemplazo de los valores Estado a versiones abreviadas usando la función new_column_Estado1 creada
    df['ESTADO'] = df['ESTADO'].apply(new_column_Estado1)
    print(df['ESTADO'])

    #Hacemos el reemplazo de los valores Estado a versiones abreviadas usando la función new_column_Estado1 creada
    df['PUNTUACION'] = df['ESTADO'].apply(new_column_Estado2)
    print(df['PUNTUACION'])

if __name__ == '__main__' :
    __init__()