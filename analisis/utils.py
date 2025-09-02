import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

def resumen_nulos(df):
    nulos = df.isnull().sum()
    pct_nulos = df.isnull().mean() * 100
    resumen = pd.concat([nulos, pct_nulos], axis=1)
    resumen.columns = ['nulos', 'pct_nulos']
    return resumen.sort_values('nulos', ascending=False)

def columnas_mayor_nulos(resumen, umbral=50):
    return resumen[resumen['pct_nulos'] > umbral].index.tolist()

def candidatas_fecha(df):
    return [c for c in df.columns if any(k in c.lower() for k in ['date','time','fecha','hora','pickup','drop'])]

def resumen_numericas(df):
    num = df.select_dtypes(include=['number']).columns.tolist()
    resumen = df[num].describe().T
    resumen['mediana'] = df[num].median()
    modos = {}
    for c in num:
        m = df[c].mode(dropna=True)
        modos[c] = m.iloc[0] if len(m)>0 else None
    resumen['moda'] = pd.Series(modos)
    resumen['suma'] = df[num].sum()
    return resumen.sort_values('count', ascending=False)

def acumulado_columna(df):
    num = df.select_dtypes(include=['number']).columns.tolist()
    if len(num)>0:
        col = num[0]
        return df[col].fillna(0).cumsum().head(20).to_dict()
    return {}

def tipo_dato_pastel(df):
    data_types = df.dtypes.value_counts()
    labels = [str(dt) for dt in data_types.index]
    values = data_types.values.tolist()
    return {'labels': labels, 'values': values}

def total_datos_no_nulos(df):
    column_sizes = df.count().sort_values(ascending=False)
    labels = column_sizes.index.tolist()
    values = column_sizes.values.tolist()
    total_filas = len(df)
    return {
        'labels': labels,
        'values': values,
        'total_filas': total_filas
    }