import io
import re
from contextlib import redirect_stdout
from typing import Optional

import openai
import pandas as pd
from dotenv import load_dotenv
from plotly import express as px
from plotly import graph_objects as go
from plotly.graph_objects import Figure

from .llm import LLM
from .prompts.generate_python_code import GeneratePythonCodePrompt

load_dotenv()


class ChartGPT:
    def __init__(
        self,
        llm: Optional[str] = "openai",
        conversational: bool = True,
        verbose: bool = False,
    ) -> None:
        """_summary_

        Args:
            llm (Optional[str], optional): _description_. Defaults to "openai".
            conversational (bool, optional): _description_. Defaults to True.
            verbose (bool, optional): _description_. Defaults to False.
        """
        self.llm = LLM()

    def load(self, data: pd.DataFrame) -> None:
        """Load a DataFrame.

        Args:
            df (pd.DataFrame): A DataFrame.

        Returns:
            None
        """
        self.data = data
        self.data_columns = data.columns

    def plot(self, prompt: str) -> Figure:
        """Run the model on a prompt.

        Args:
            prompt (Optional[str]): _description_

        Returns:
            str: _description_
        """

        df_columns = self.data.columns

        self._original_instructions = {
            "question": prompt,
            "df_columns": df_columns,
        }

        code = self.llm.generate_code(
            GeneratePythonCodePrompt(
                df_columns=df_columns,
            ),
            prompt,
        )

        answer = self.run_code(
            code,
            self.data,
            use_error_correction_framework=False,
        )
        self.code_output = answer

        return answer

    def ask(self, prompt: str) -> str:
        """Run the model on a prompt.

        Args:
            prompt (Optional[str]): _description_

        Returns:
            str: _description_
        """

        df_columns = self.data.columns

        self._original_instructions = {
            "question": prompt,
            "df_columns": df_columns,
        }

        code = self.llm.generate_code(
            GeneratePythonCodePrompt(
                df_columns=df_columns,
            ),
            prompt,
        )

        answer = self.run_code(
            code,
            self.data,
            use_error_correction_framework=False,
        )
        self.code_output = answer

        return answer

    def run_code(
        self,
        code: str,
        df: pd.DataFrame,
        use_error_correction_framework: bool = True,
    ) -> str:
        """
        A method to execute the python code generated by LLMs to answer the question about the
        input dataframe. Run the code in the current context and return the result.
        Args:
            code (str): A python code to execute
            df (pd.DataFrame): A full Pandas DataFrame
            use_error_correction_framework (bool): Turn on Error Correction mechanism.
            Default to True

        Returns:

        """
        code_to_run = code.strip()
        self.last_run_code = code_to_run

        environment: dict = {"pd": pd, "go": go, "px": px, "df": df}

        # Redirect standard output to a StringIO buffer
        with redirect_stdout(io.StringIO()) as output:
            count = 0
            while count < 2:
                try:
                    # Execute the code
                    exec(code_to_run, environment)
                    code = code_to_run
                    break
                except Exception as e:
                    if not use_error_correction_framework:
                        raise e
                    count += 1

        captured_output = output.getvalue()

        # Evaluate the last line and return its value or the captured output
        lines = code.strip().split("\n")
        last_line = lines[-1].strip()

        match = re.match(r"^print\((.*)\)$", last_line)
        if match:
            last_line = match.group(1)

        try:
            return eval(last_line, environment)
        except Exception:  # pylint: disable=W0718
            return captured_output
