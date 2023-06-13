---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.2'
      jupytext_version: 1.5.1
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

```python
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn import metrics
```

```python
housing_df = pd.read_csv("../../data/housing.csv")
values = housing_df.median_house_value
features = housing_df.drop('median_house_value', axis=1).drop('ocean_proximity', axis=1).fillna(0)
cols = list(features.columns)
```

```python
print(features.head(5))
```

```python
print(features.dtypes)
```

```python
print(features.max(), housing_df.count())
```

```python
training_size = 20000
model = LinearRegression()
model.fit(features[:training_size], values[:training_size])
preds = model.predict(features[training_size:])
real = values[training_size:]
print(real[:10], preds[:10])
r2 = metrics.r2_score(preds, real)
print(r2)
```

```python

```
