### Módulo 1 — Exercício 1: Meu Primeiro Modelo

Neste exercício, você treina uma Regressão Linear simples usando scikit-learn.

**Objetivo**: entender o fluxo básico (carregar dados, treinar e visualizar a linha de predição).

#### Conteúdo
- Dataset 1: `datasets/temperatura_vs_sorvete.csv` (Temperatura → Vendas de sorvete)
- Dataset 2: `datasets/pizza_size_vs_price.csv` (Tamanho da pizza → Preço)
- Script: `scripts/linear_regression_sklearn.py`

#### Como rodar
1. Instale as dependências deste exercício:
   ```bash
   pip install -r requirements.txt
   ```
2. Execute o script de exemplo (usa o dataset de sorvete por padrão):
   ```bash
   python scripts/linear_regression_sklearn.py
   ```

#### Desafio Complementar

Prever o preço da pizza baseado no tamanho usando o dataset `datasets/pizza_size_vs_price.csv`.
- Copie o script `scripts/linear_regression_sklearn.py` e troque o caminho do dataset e os nomes das colunas (`tamanho_polegadas`, `preco`).
