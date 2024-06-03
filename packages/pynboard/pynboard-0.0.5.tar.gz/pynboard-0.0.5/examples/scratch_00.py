# %%
import numpy as np
import pandas as pd

pd.set_option('display.max_columns', 10)

import plotly.io as pio
from plotly import express as px
import plotly.graph_objects as go

pio.templates.default = "seaborn"
pio.templates[pio.templates.default].layout.width = 800
pio.templates[pio.templates.default].layout.height = 400

# %%
import pynboard as pbo


# %%
n = 750
dates = pd.bdate_range("2019-1-1", periods=n)
eps = np.random.standard_cauchy(size=n)
val = np.cumsum(eps) * 1e4
data = pd.DataFrame({"date": dates, "eps": eps, "val": val})

# %%
fig = px.line(data, x="date", y="val")


# %%
pbo.append(fig)
pbo.append(data, index=False)
pbo.render()


# %%
pbo.append([[fig, fig], [fig, data.sample(20)]])
pbo.render()


# %%