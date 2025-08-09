import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

CAMINHO_CSV = "../datasets/temperatura_vs_sorvete.csv"
COLUNA_TEMPERATURA = "temperatura_c"
COLUNA_VENDAS = "vendas_sorvete"

tabela_dados = pd.read_csv(CAMINHO_CSV)
entrada = tabela_dados[[COLUNA_TEMPERATURA]].values
alvo = tabela_dados[COLUNA_VENDAS].values

modelo = LinearRegression()
modelo.fit(entrada, alvo)
print(f"y = {modelo.coef_[0]:.4f} * x + {modelo.intercept_:.4f}")

previsao = modelo.predict(entrada)

plt.figure(figsize=(7, 5))
plt.scatter(entrada, alvo, color="blue", label="dados")
plt.plot(entrada, previsao, color="red", label="reta de regressao")
plt.xlabel(COLUNA_TEMPERATURA)
plt.ylabel(COLUNA_VENDAS)
plt.title("Regressão Linear Simples")
plt.legend()
plt.tight_layout()
plt.show()
