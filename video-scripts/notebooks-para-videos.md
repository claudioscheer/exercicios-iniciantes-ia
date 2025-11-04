# Notebooks de Apoio para os Vídeos

Cada vídeo deve ter um notebook correspondente no GitHub que permite a audiência **experimentar** os conceitos explicados.

---

## Vídeo 1: Como Máquinas Realmente Aprendem

### Notebook: `01-gradient-descent-do-zero.ipynb`

**Objetivo:** Implementar gradient descent do absoluto zero, sem bibliotecas de ML.

**Estrutura:**

```python
# Seção 1: O Problema
"""
Vamos prever preços de casas baseado no tamanho.
Dataset simples, criado manualmente.
"""

import numpy as np
import matplotlib.pyplot as plt

# Dados de treino (tamanho em m², preço em R$ 1000)
tamanhos = np.array([50, 70, 100, 120, 150, 180, 200])
precos = np.array([150, 200, 300, 350, 430, 500, 580])

# Visualizar
plt.scatter(tamanhos, precos)
plt.xlabel('Tamanho (m²)')
plt.ylabel('Preço (R$ 1000)')
plt.show()


# Seção 2: A Função (nosso modelo)
def prever_preco(tamanho, peso):
    """
    Modelo mais simples possível: y = w * x
    """
    return peso * tamanho


# Seção 3: Medir o Erro
def calcular_erro(tamanhos, precos_reais, peso):
    """
    MSE (Mean Squared Error)
    Quanto maior, pior a previsão
    """
    previsoes = prever_preco(tamanhos, peso)
    erros = precos_reais - previsoes
    mse = np.mean(erros ** 2)
    return mse


# Seção 4: O Aprendizado (Gradient Descent)
def treinar_modelo(tamanhos, precos, peso_inicial=1.0, taxa_aprendizado=0.0001, num_iteracoes=100):
    """
    Aqui está a MÁGICA do Machine Learning!
    """
    peso = peso_inicial
    historico_erro = []
    historico_peso = []

    for i in range(num_iteracoes):
        # Fazer previsões
        previsoes = prever_preco(tamanhos, peso)

        # Calcular erro
        erros = precos - previsoes
        erro_medio = calcular_erro(tamanhos, precos, peso)

        # Calcular gradiente (direção para diminuir erro)
        # Matemática: derivada parcial de MSE em relação ao peso
        gradiente = -2 * np.mean(erros * tamanhos)

        # AJUSTAR O PESO (o aprendizado acontece aqui!)
        peso = peso - taxa_aprendizado * gradiente

        # Guardar histórico
        historico_erro.append(erro_medio)
        historico_peso.append(peso)

        # Imprimir progresso
        if i % 10 == 0:
            print(f"Iteração {i}: Erro = {erro_medio:.2f}, Peso = {peso:.2f}")

    return peso, historico_erro, historico_peso


# Seção 5: Treinar e ver a máquina aprendendo!
peso_final, historico_erro, historico_peso = treinar_modelo(
    tamanhos, precos,
    peso_inicial=1.0,
    taxa_aprendizado=0.0001,
    num_iteracoes=100
)

print(f"\n✅ Treinamento completo!")
print(f"Peso final: {peso_final:.2f}")


# Seção 6: Visualizar o aprendizado
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# Gráfico 1: Erro diminuindo
axes[0].plot(historico_erro)
axes[0].set_xlabel('Iteração')
axes[0].set_ylabel('Erro (MSE)')
axes[0].set_title('Erro diminuindo = Máquina aprendendo!')

# Gráfico 2: Peso convergindo
axes[1].plot(historico_peso)
axes[1].set_xlabel('Iteração')
axes[1].set_ylabel('Valor do Peso')
axes[1].set_title('Peso encontrando valor ideal')

# Gráfico 3: Fit final
axes[2].scatter(tamanhos, precos, label='Dados reais')
tamanhos_plot = np.linspace(50, 200, 100)
previsoes_plot = prever_preco(tamanhos_plot, peso_final)
axes[2].plot(tamanhos_plot, previsoes_plot, 'r-', label='Modelo treinado')
axes[2].set_xlabel('Tamanho (m²)')
axes[2].set_ylabel('Preço (R$ 1000)')
axes[2].legend()
axes[2].set_title('Resultado final')

plt.tight_layout()
plt.show()


# Seção 7: Testar com dados novos
novo_tamanho = 130
preco_previsto = prever_preco(novo_tamanho, peso_final)
print(f"\n🏠 Casa de {novo_tamanho}m² → Preço previsto: R$ {preco_previsto:.0f} mil")


# Seção 8: Experimentos para você fazer
"""
DESAFIOS:
1. Mude a taxa_aprendizado para 0.001. O que acontece?
2. Mude para 0.00001. E agora?
3. Mude para 0.1. Explodiu? Por quê?
4. Adicione mais dados. O modelo melhora?
5. Comece com peso_inicial=10. Ainda converge?

PRÓXIMO NÍVEL:
- Adicione bias (intercepto): y = w*x + b
- Use múltiplas features: y = w1*x1 + w2*x2 + b
- Compare com sklearn.linear_model.LinearRegression()
"""
```

**Extras no notebook:**
- Seção explicando a matemática do gradiente (opcional, colapsável)
- Animação do gradient descent (usando matplotlib.animation)
- Comparação com sklearn

---

## Vídeo 2: Overfitting - O Erro Fatal

### Notebook: `02-overfitting-na-pratica.ipynb`

**Objetivo:** MOSTRAR overfitting acontecendo, não apenas explicar.

**Estrutura:**

```python
# Seção 1: Criar dados simples
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Função verdadeira (que queremos aprender)
np.random.seed(42)
X = np.linspace(0, 10, 30).reshape(-1, 1)
y = 2 * X.ravel() + 3 + np.random.normal(0, 2, X.shape[0])  # y = 2x + 3 + ruído

# Visualizar
plt.scatter(X, y)
plt.xlabel('X')
plt.ylabel('y')
plt.title('Nossos dados (com ruído natural)')
plt.show()


# Seção 2: Dividir em treino, validação, teste
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.4, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

print(f"Treino: {len(X_train)} exemplos")
print(f"Validação: {len(X_val)} exemplos")
print(f"Teste: {len(X_test)} exemplos")


# Seção 3: Testar diferentes complexidades de modelo
graus = [1, 2, 3, 5, 10, 15]  # Grau do polinômio
resultados = []

for grau in graus:
    # Criar features polinomiais
    poly = PolynomialFeatures(degree=grau)
    X_train_poly = poly.fit_transform(X_train)
    X_val_poly = poly.transform(X_val)

    # Treinar modelo
    modelo = LinearRegression()
    modelo.fit(X_train_poly, y_train)

    # Avaliar
    y_train_pred = modelo.predict(X_train_poly)
    y_val_pred = modelo.predict(X_val_poly)

    erro_treino = mean_squared_error(y_train, y_train_pred)
    erro_val = mean_squared_error(y_val, y_val_pred)

    resultados.append({
        'grau': grau,
        'erro_treino': erro_treino,
        'erro_val': erro_val
    })

    print(f"Grau {grau:2d} | Treino: {erro_treino:.2f} | Val: {erro_val:.2f}")


# Seção 4: O GRÁFICO CRUCIAL - Visualizar overfitting
import pandas as pd

df = pd.DataFrame(resultados)

plt.figure(figsize=(10, 6))
plt.plot(df['grau'], df['erro_treino'], 'o-', label='Erro Treino', linewidth=2)
plt.plot(df['grau'], df['erro_val'], 's-', label='Erro Validação', linewidth=2)
plt.xlabel('Complexidade do Modelo (Grau do Polinômio)')
plt.ylabel('Erro (MSE)')
plt.title('O Padrão do Overfitting')
plt.legend()
plt.grid(True, alpha=0.3)

# Marcar o sweet spot
sweet_spot_idx = df['erro_val'].idxmin()
sweet_spot_grau = df.loc[sweet_spot_idx, 'grau']
plt.axvline(sweet_spot_grau, color='green', linestyle='--', label=f'Sweet Spot (grau {sweet_spot_grau})')
plt.legend()
plt.show()


# Seção 5: Visualizar os modelos
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
axes = axes.ravel()

X_plot = np.linspace(0, 10, 100).reshape(-1, 1)

for idx, grau in enumerate(graus):
    poly = PolynomialFeatures(degree=grau)
    X_train_poly = poly.fit_transform(X_train)
    X_plot_poly = poly.transform(X_plot)

    modelo = LinearRegression()
    modelo.fit(X_train_poly, y_train)
    y_plot = modelo.predict(X_plot_poly)

    # Plot
    axes[idx].scatter(X_train, y_train, alpha=0.6, label='Treino')
    axes[idx].plot(X_plot, y_plot, 'r-', linewidth=2, label='Modelo')
    axes[idx].set_title(f'Grau {grau}')
    axes[idx].set_ylim(-10, 35)
    axes[idx].legend()

plt.tight_layout()
plt.show()


# Seção 6: Early Stopping simulado
"""
Simulando treinamento de uma rede neural
"""
epochs = 100
train_loss = []
val_loss = []

for epoch in range(epochs):
    # Simulando loss diminuindo (treino)
    train_loss.append(10 * np.exp(-0.05 * epoch) + np.random.normal(0, 0.1))

    # Validação: diminui, depois sobe (overfitting)
    if epoch < 30:
        val_loss.append(10 * np.exp(-0.04 * epoch) + np.random.normal(0, 0.2))
    else:
        val_loss.append(2 + 0.05 * (epoch - 30) + np.random.normal(0, 0.2))

plt.figure(figsize=(10, 6))
plt.plot(train_loss, label='Loss Treino')
plt.plot(val_loss, label='Loss Validação')
plt.axvline(30, color='red', linestyle='--', label='Early Stopping')
plt.xlabel('Época')
plt.ylabel('Loss')
plt.title('Early Stopping: Pare quando validação começar a subir!')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()


# Seção 7: DESAFIOS
"""
1. Mude o ruído nos dados (linha 11). Mais ruído = mais overfitting?
2. Mude o tamanho do dataset de treino (menos dados = mais overfitting?)
3. Implemente regularização L2 (Ridge)
4. Qual grau você escolheria para produção? Por quê?
"""
```

**Extras:**
- Implementar dropout manual em rede neural simples
- Comparar L1 vs L2 regularization
- Mostrar overfitting em dataset real (MNIST, iris, etc)

---

## Vídeo 3: Dados > Algoritmos

### Notebook: `03-dados-vs-algoritmos.ipynb`

**Objetivo:** Provar com experimentos que dados importam mais.

**Estrutura:**

```python
# Seção 1: Setup
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
import pandas as pd


# Seção 2: Experimento 1 - Mesmo algoritmo, diferentes quantidades de dados
print("=" * 50)
print("EXPERIMENTO 1: Impacto da quantidade de dados")
print("=" * 50)

# Criar dataset
X, y = make_classification(n_samples=10000, n_features=20, n_informative=15,
                           n_redundant=5, random_state=42)

# Testar com diferentes quantidades de treino
tamanhos_treino = [50, 100, 200, 500, 1000, 2000, 5000]
resultados_exp1 = []

for n in tamanhos_treino:
    # Pegar n exemplos de treino
    X_train = X[:n]
    y_train = y[:n]
    X_test = X[8000:]
    y_test = y[8000:]

    # Modelo simples
    modelo = LogisticRegression(max_iter=1000)
    modelo.fit(X_train, y_train)
    acc = accuracy_score(y_test, modelo.predict(X_test))

    resultados_exp1.append({'n_treino': n, 'acuracia': acc})
    print(f"N={n:4d} treino → Acurácia: {acc:.3f}")

# Visualizar
df1 = pd.DataFrame(resultados_exp1)
plt.figure(figsize=(10, 6))
plt.plot(df1['n_treino'], df1['acuracia'], 'o-', linewidth=2, markersize=8)
plt.xlabel('Quantidade de Dados de Treino')
plt.ylabel('Acurácia no Teste')
plt.title('Mais Dados = Melhor Performance (mesmo algoritmo)')
plt.grid(True, alpha=0.3)
plt.show()


# Seção 3: Experimento 2 - Algoritmos diferentes, mesmos dados
print("\n" + "=" * 50)
print("EXPERIMENTO 2: Algoritmo simples + muitos dados VS Complexo + poucos dados")
print("=" * 50)

# Caso 1: Modelo complexo (Random Forest) com POUCOS dados
X_train_pequeno = X[:200]
y_train_pequeno = y[:200]
X_test = X[8000:]
y_test = y[8000:]

modelo_complexo = RandomForestClassifier(n_estimators=100, max_depth=10)
modelo_complexo.fit(X_train_pequeno, y_train_pequeno)
acc_complexo_poucos = accuracy_score(y_test, modelo_complexo.predict(X_test))

# Caso 2: Modelo simples (Regressão Logística) com MUITOS dados
X_train_grande = X[:5000]
y_train_grande = y[:5000]

modelo_simples = LogisticRegression(max_iter=1000)
modelo_simples.fit(X_train_grande, y_train_grande)
acc_simples_muitos = accuracy_score(y_test, modelo_simples.predict(X_test))

print(f"\nRandom Forest com 200 exemplos: {acc_complexo_poucos:.3f}")
print(f"Regressão Logística com 5000 exemplos: {acc_simples_muitos:.3f}")
print(f"\n✅ Modelo SIMPLES com MAIS dados venceu!" if acc_simples_muitos > acc_complexo_poucos else "❌ Ops...")


# Seção 4: Experimento 3 - Qualidade dos dados
print("\n" + "=" * 50)
print("EXPERIMENTO 3: Impacto de rótulos errados")
print("=" * 50)

X_train = X[:2000]
y_train = y[:2000].copy()
X_test = X[8000:]
y_test = y[8000:]

percentuais_ruido = [0, 0.05, 0.1, 0.2, 0.3, 0.5]
resultados_exp3 = []

for ruido in percentuais_ruido:
    # Adicionar ruído (trocar rótulos aleatoriamente)
    y_train_ruidoso = y_train.copy()
    n_trocar = int(len(y_train) * ruido)
    indices_trocar = np.random.choice(len(y_train), n_trocar, replace=False)
    y_train_ruidoso[indices_trocar] = 1 - y_train_ruidoso[indices_trocar]  # Flip labels

    # Treinar
    modelo = LogisticRegression(max_iter=1000)
    modelo.fit(X_train, y_train_ruidoso)
    acc = accuracy_score(y_test, modelo.predict(X_test))

    resultados_exp3.append({'ruido': ruido * 100, 'acuracia': acc})
    print(f"Ruído: {ruido*100:2.0f}% → Acurácia: {acc:.3f}")

# Visualizar
df3 = pd.DataFrame(resultados_exp3)
plt.figure(figsize=(10, 6))
plt.plot(df3['ruido'], df3['acuracia'], 'o-', linewidth=2, markersize=8, color='red')
plt.xlabel('Percentual de Rótulos Errados (%)')
plt.ylabel('Acurácia no Teste')
plt.title('Qualidade dos Dados Importa!')
plt.grid(True, alpha=0.3)
plt.show()


# Seção 5: Experimento 4 - Engenharia de Features
print("\n" + "=" * 50)
print("EXPERIMENTO 4: Features boas vs. Features ruins")
print("=" * 50)

# Dataset com features relevantes e irrelevantes
X_full, y = make_classification(n_samples=2000, n_features=20, n_informative=10,
                                n_redundant=5, n_repeated=0, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(X_full, y, test_size=0.3, random_state=42)

# Caso 1: Todas as features (incluindo ruins)
modelo = LogisticRegression(max_iter=1000)
modelo.fit(X_train, y_train)
acc_todas = accuracy_score(y_test, modelo.predict(X_test))

# Caso 2: Só features relevantes (primeiras 10)
modelo = LogisticRegression(max_iter=1000)
modelo.fit(X_train[:, :10], y_train)
acc_relevantes = accuracy_score(y_test, modelo.predict(X_test[:, :10]))

print(f"\nCom todas as features (boas + ruins): {acc_todas:.3f}")
print(f"Só features relevantes: {acc_relevantes:.3f}")
print(f"\n✅ Menos features (mas relevantes) = Melhor!" if acc_relevantes > acc_todas else "")


# Seção 6: Resumo visual de todos experimentos
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Exp 1
axes[0, 0].plot(df1['n_treino'], df1['acuracia'], 'o-', linewidth=2)
axes[0, 0].set_title('Exp 1: Mais dados → Melhor')
axes[0, 0].set_xlabel('Quantidade Treino')
axes[0, 0].set_ylabel('Acurácia')
axes[0, 0].grid(True, alpha=0.3)

# Exp 2
categorias = ['Complexo\n(poucos dados)', 'Simples\n(muitos dados)']
valores = [acc_complexo_poucos, acc_simples_muitos]
cores = ['red', 'green']
axes[0, 1].bar(categorias, valores, color=cores, alpha=0.7)
axes[0, 1].set_title('Exp 2: Simples + Dados > Complexo')
axes[0, 1].set_ylabel('Acurácia')
axes[0, 1].set_ylim(0.5, 1.0)

# Exp 3
axes[1, 0].plot(df3['ruido'], df3['acuracia'], 'o-', linewidth=2, color='red')
axes[1, 0].set_title('Exp 3: Qualidade importa')
axes[1, 0].set_xlabel('% Rótulos Errados')
axes[1, 0].set_ylabel('Acurácia')
axes[1, 0].grid(True, alpha=0.3)

# Exp 4
categorias = ['Todas features', 'Só relevantes']
valores = [acc_todas, acc_relevantes]
cores = ['orange', 'green']
axes[1, 1].bar(categorias, valores, color=cores, alpha=0.7)
axes[1, 1].set_title('Exp 4: Features relevantes > Mais features')
axes[1, 1].set_ylabel('Acurácia')
axes[1, 1].set_ylim(0.5, 1.0)

plt.tight_layout()
plt.show()


# Seção 7: Conclusões
print("\n" + "=" * 70)
print("CONCLUSÕES:")
print("=" * 70)
print("1. Dobrar dados melhora mais que trocar algoritmo")
print("2. Modelo simples + muitos dados > Modelo complexo + poucos dados")
print("3. Dados ruins limitam performance máxima")
print("4. Features relevantes > Muitas features")
print("\n💡 Antes de complicar o modelo, melhore seus dados!")
```

**Extras:**
- Data augmentation em imagens
- Análise exploratória de dados (EDA) exemplo
- Como identificar features relevantes (feature importance)

---

## Estrutura de pastas sugerida no GitHub

```
exercicios-iniciantes-ia/
├── notebooks/
│   ├── 01-gradient-descent-do-zero.ipynb
│   ├── 02-overfitting-na-pratica.ipynb
│   ├── 03-dados-vs-algoritmos.ipynb
│   └── requirements.txt
├── datasets/
│   └── (datasets usados nos notebooks)
├── video-scripts/
│   ├── video-01-como-maquinas-aprendem.md
│   ├── video-02-overfitting-erro-fatal.md
│   ├── video-03-dados-maior-que-algoritmos.md
│   └── README-GUIA-DE-GRAVACAO.md
└── README.md (overview do repositório)
```

---

## README.md template para o repo

```markdown
# Canal YouTube: IA na Prática

Repositório com código dos vídeos do canal [NOME DO CANAL].

## 🎯 Objetivo

Ensinar Machine Learning e IA de forma:
- Simples mas profunda
- Prática e aplicável
- Baseada em entendimento real, não decoreba

## 📚 Vídeos e Notebooks

### Vídeo 1: Como Máquinas REALMENTE Aprendem
- 📹 [Link do vídeo](...)
- 📓 [Notebook](notebooks/01-gradient-descent-do-zero.ipynb)
- 🎯 Aprenda a essência de todo ML: Função + Erro + Otimizador

### Vídeo 2: Overfitting - O Erro Fatal
- 📹 [Link do vídeo](...)
- 📓 [Notebook](notebooks/02-overfitting-na-pratica.ipynb)
- 🎯 Identifique e evite o erro que mata 90% dos projetos

### Vídeo 3: Por Que Seus DADOS Importam Mais Que Seu ALGORITMO
- 📹 [Link do vídeo](...)
- 📓 [Notebook](notebooks/03-dados-vs-algoritmos.ipynb)
- 🎯 Experimentos que provam: dados > algoritmos

## 🚀 Como usar

```bash
# Clone o repositório
git clone https://github.com/[seu-usuario]/exercicios-iniciantes-ia.git

# Entre na pasta
cd exercicios-iniciantes-ia/notebooks

# Instale dependências
pip install -r requirements.txt

# Abra o Jupyter
jupyter notebook
```

## 📦 Dependências

- Python 3.8+
- numpy
- matplotlib
- scikit-learn
- jupyter

## 🤝 Contribuir

Encontrou um erro? Tem uma sugestão? Abre uma issue ou PR!

## 📧 Contato

- YouTube: [link]
- Email: [seu email]
```

---

## requirements.txt

```
numpy>=1.21.0
matplotlib>=3.4.0
scikit-learn>=1.0.0
jupyter>=1.0.0
pandas>=1.3.0
seaborn>=0.11.0
```

---

Esses notebooks são:
- **Executáveis:** Rodam do início ao fim sem erro
- **Educacionais:** Comentários explicando cada passo
- **Experimentais:** Permitem modificar e ver o resultado
- **Autosuficientes:** Não dependem de arquivos externos

A pessoa assiste o vídeo, entende o conceito, depois EXPERIMENTA no notebook.

**Aprendizado ativo > Aprendizado passivo**
