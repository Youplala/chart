import pandas as pd

import chartgpt as cg

df = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/2014_usa_states.csv"
)
chart = cg.Chart(df, api_key=None, model="huggingface/mistralai/Mistral-7B-Instruct-v0.2", stream=False)
chart.plot("show me a bar graph", return_fig=False, show_code=True)
