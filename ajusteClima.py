import pandas as pd
import numpy as np
clima = pd.read_csv (r'Entrada\Clima_2012_2021.csv', decimal=",", sep=";")
clima.replace(-9999.0, None, inplace=True)

clima.columns=['DATA','HORA','PRECIPITACAO','PRESSAO ATMOSFERICA','RADIACAO GLOBAL','TEMPERATURA','PONTO DE ORVALHO','UMIDADE RELATIVA DO AR','VELOCIDADE DO VENTO']
clima["DATA"] = pd.to_datetime(clima["DATA"],format="%d/%m/%Y").dt.date
clima = clima.sort_values(by="DATA")


agrupados=clima.groupby('DATA').agg({
    'PRECIPITACAO':['sum','mean'],
    'PRESSAO ATMOSFERICA':'mean',
    'RADIACAO GLOBAL':'mean',
    'TEMPERATURA':['min','max','mean'],
    'PONTO DE ORVALHO':'mean',
    'UMIDADE RELATIVA DO AR':['min','mean'],
    'VELOCIDADE DO VENTO':'mean'
})

agrupados.columns=['PRECIPITACAO TOTAL','PRECIPITACAO MEDIA','PRESSAO ATMOSFERICA MEDIA','RADIACAO GLOBAL MEDIA','TEMPERATURA MINIMA',
'TEMPERATURA MAXIMA','TEMPERATURA MEDIA','PONTO DE ORVALHO MEDIA','UMIDADE RELATIVA DO AR MINIMA','UMIDADE RELATIVA DO AR MEDIA','VELOCIDADE DO VENTO MEDIA']
agrupados=agrupados.reset_index()

focos = pd.read_csv(r'Entrada\Focos_2012_2021.CSV', decimal=",", sep=";")
focos["datahora"] = pd.to_datetime(focos["datahora"]).dt.date

focos=focos.groupby("datahora").size().sort_values().reset_index("datahora")
focos.columns = ["DATA","QUANTIDADE FOCOS"]

merjado = pd.merge(agrupados, focos, on="DATA", how="left")

merjado["QUANTIDADE FOCOS"] = merjado["QUANTIDADE FOCOS"].fillna(0)
merjado["OCORREU FOGO"] = np.where(merjado['QUANTIDADE FOCOS'] > 0, True, False)
merjado.to_csv(r'Saida\dados_finais.csv', index=False)