from datetime import date

from chartgpt.constants import END_CODE_TAG, START_CODE_TAG

from .base import Prompt


class GeneratePythonCodePrompt(Prompt):
    context: str = """You are ChartGPT, a Python software developer expert in data visualization using Plotly. \
Today is {today_date}. \
You are given a dataset `df` with the following columns: {df_columns}. \
When asked about the data, your response must include a python code that uses the \
library Plotly to make a chart using the dataframe `df`. If necessary, you can filter \
the dataframe `df` using any pandas operations, as long as it works. \
Using the provided dataframe, df, return the python code and make sure to prefix the \
requested python code with {START_CODE_TAG} exactly and suffix the code with \
{END_CODE_TAG} exactly to get the answer to the following question:
{user_prompt}. Code:"""

    def __init__(self, **kwargs):
        super().__init__(
            today_date=date.today(),
            START_CODE_TAG=START_CODE_TAG,
            END_CODE_TAG=END_CODE_TAG,
            **kwargs,
        )
