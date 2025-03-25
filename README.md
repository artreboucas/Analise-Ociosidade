#  📊 Análise Ociosidade Berços 

Este projeto processa dados de movimentação portuária para calcular o tempo ocupado e ocioso dos berços dos portos de Mucuripe e Pecém. Sendo utilizado para análise de eficiência operacional e gestão portuária.


---


## 🚀 Funcionalidades

✅ Filtragem e limpeza dos dados brutos de movimentação portuária

✅ Cálculo do tempo total ocupado e ocioso dos berços por ano

✅ Geração de estatísticas para análise de eficiência portuária

## 🛠️ Tecnologias Utilizadas

Python 🐍

Pandas 📊

## 📂 Estrutura do Código

filtrar_dados(df) → Filtra os dados, exclui movimentações indesejadas e ajusta valores inconsistentes.

calcular_ociosidade(df) → Calcula os tempos ocupados e ociosos dos berços por ano.

Execução do script → Carrega os dados, processa as informações e exibe um resumo da análise.

## 📥 Como Usar

1️⃣ Instale as dependências:

```
pip install pandas openpyxl
```

2️⃣ Substitua o caminho do arquivo no código para o local correto dos seus dados:

```
df = pd.read_excel(r'seu/caminho/para/dados.xlsx')
```

3️⃣ Execute o script:

```
python nome_do_arquivo.py
```

4️⃣ Confira os resultados no terminal ou exporte para análise posterior.


## 🎲 Entrada de Dados

O arquivo de entrada deve ser um Excel (.xlsx) contendo pelo menos as seguintes colunas:

• **Mn**: Tipo de manobra

• **De**: Origem

• **Para**: Destino

• **Início**: Data e hora de início

• **Fim**: Data e hora de fim

• **Cais**: Local da manobra

## 📤 Saída

O script gera três tabelas:

→ Resumo: Percentuais de tempo ocupado e ocioso por ano e berço.

→ Detalhes: Intervalos de tempo ocupados.

→ Tempos Totais: Tempo total ocupado em segundos.