import pandas as pd
import sys

def carregar_dados(caminho_arquivo):
    """Carrega os dados do arquivo Excel."""
    return pd.read_excel(caminho_arquivo)

def filtrar_dados(df):
    """Filtra e ajusta os dados de movimentação portuária."""
    df = df[~df['Mn'].isin(['ES', 'ES P/F', 'MB', 'MV SC'])]  
    df = df[~df['De Bordo'].isin(['BBCB', 'BECB'])]
    df = df[~df['Para Bordo'].isin(['BBCB', 'BECB'])]
    df = df[~((df['Mn'] == 'RM') & (df['De'] == df['Para']))]
    
    df['Mn'] = df['Mn'].replace({"DF S/P": "DS", "DF C/P": "DS", "EA C/F": "EA"})
    
    novos_registros = []
    for _, row in df[df['Mn'] == 'RM'].iterrows():
        novos_registros.append({'Mn': 'DS', 'De': row['De'], 'Para': row['Para'], 'Início': row['Início'], 'Fim': row['Início'], 'Cais': row['De'], 'Ano': None})
        novos_registros.append({'Mn': 'EA', 'De': row['De'], 'Para': row['Para'], 'Início': row['Fim'], 'Fim': row['Fim'], 'Cais': row['Para'], 'Ano': None})
    
    df = pd.concat([df, pd.DataFrame(novos_registros)], ignore_index=True)
    df = df[df['Mn'] != 'RM']

    df['Início'] = pd.to_datetime(df['Início'], errors='coerce')
    df['Fim'] = pd.to_datetime(df['Fim'], errors='coerce')

    df['Ano'] = df['Início'].dt.year
    df['Berço'] = df['Cais']

    return df

def calcular_ociosidade(df):
    """Calcula o tempo de ociosidade e ocupação."""
    df = filtrar_dados(df)
    detalhes, resultados, tempos_totais = [], [], []

    for (ano, berco), group in df.groupby(['Ano', 'Berço']):
        group = group.sort_values(by='Início')
        processados = set()
        tempo_total_ocupado = 0

        start_date = pd.Timestamp(f'{ano}-01-01 00:00:00')
        end_date = pd.Timestamp(f'{ano}-12-31 23:59:59')

        if group.iloc[0]['Mn'] == 'DS':
            tempo_total_ocupado += (group.iloc[0]['Início'] - start_date).total_seconds()
            detalhes.append({'Ano': ano, 'Berço': berco, 'Intervalo Início': start_date, 'Intervalo Fim': group.iloc[0]['Fim'], 'Tipo': 'Ocupado', 'Tempo (s)': tempo_total_ocupado})

        for i in range(len(group)):
            manobra = group.iloc[i]
            if manobra['Mn'] == 'EA' and manobra.name not in processados:
                encontrou_vinculo = False
                for j in range(i + 1, len(group)):
                    proxima = group.iloc[j]
                    if proxima['Mn'] in ['DS', 'DF S/P']:
                        tempo_total_ocupado += (proxima['Fim'] - manobra['Início']).total_seconds()
                        detalhes.append({'Ano': ano, 'Berço': berco, 'Intervalo Início': manobra['Início'], 'Intervalo Fim': proxima['Fim'], 'Tipo': 'Ocupado', 'Tempo (s)': (proxima['Fim'] - manobra['Início']).total_seconds()})
                        encontrou_vinculo = True
                        processados.update([manobra.name, proxima.name])
                        break

                if not encontrou_vinculo:
                    tempo_total_ocupado += (end_date - manobra['Início']).total_seconds()
                    detalhes.append({'Ano': ano, 'Berço': berco, 'Intervalo Início': manobra['Início'], 'Intervalo Fim': end_date, 'Tipo': 'Ocupado', 'Tempo (s)': (end_date - manobra['Início']).total_seconds()})
                    processados.add(manobra.name)

        if group.iloc[-1]['Mn'] == 'EA' and group.iloc[-1].name not in processados:
            tempo_total_ocupado += (end_date - group.iloc[-1]['Fim']).total_seconds()
            detalhes.append({'Ano': ano, 'Berço': berco, 'Intervalo Início': group.iloc[-1]['Fim'], 'Intervalo Fim': end_date, 'Tipo': 'Ocupado', 'Tempo (s)': (end_date - group.iloc[-1]['Fim']).total_seconds()})

        tempo_total_ano = 366 * 24 * 3600 if pd.Timestamp(f'{ano}-12-31').is_leap_year else 365 * 24 * 3600
        percentual_ocupado = (tempo_total_ocupado / tempo_total_ano) * 100
        percentual_ocioso = 100 - percentual_ocupado

        resultados.append({'Ano': ano, 'Berço': berco, 'Tempo Ocupado (%)': percentual_ocupado, 'Tempo Ocioso (%)': percentual_ocioso})
        tempos_totais.append({'Ano': ano, 'Berço': berco, 'Tempo Total Ocupado (s)': tempo_total_ocupado})

    return pd.DataFrame(resultados), pd.DataFrame(detalhes), pd.DataFrame(tempos_totais)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python analise_ociosidade.py <caminho_do_arquivo.xlsx>")
        sys.exit(1)

    caminho_arquivo = sys.argv[1]
    df = carregar_dados(caminho_arquivo)

    resumo, detalhes, tempos_totais = calcular_ociosidade(df)

    print(resumo)
