import os
import re
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel

import litellm

litellm.drop_params = True

from .constants import END_CODE_TAG, START_CODE_TAG


class LLM(BaseModel):
    model: str = "huggingface/mistralai/Mistral-7B-Instruct-v0.2"
    temperature: Optional[float] = None
    max_tokens: Optional[float] = 500
    top_p: Optional[float] = None
    n: Optional[int] = None  # typically only one completion is needed
    stream: Optional[bool] = None
    stop: Optional[Union[str, List[str]]] = None
    messages: List = []

    def _extract_code(self, response: str, separator: str = "```") -> str:
        """
        Extract code from the response.
        """
        response = response.replace("python", "").replace("fig.show()", "fig")
        code = re.search(rf"{separator}(.+?){separator}", response, re.DOTALL)
        if code:
            code = code.group(1).strip()
        else:
            code = response
        return code

    def generate_code(self, instruction: str) -> str:
        """
        Generate code based on the instruction using the chat completion.
        """
        self.add_message(instruction, "user")
        response = self.chat_completion()
        code = self._extract_code(response)
        self.add_message(response, "assistant")  # Store the assistant's response
        return code

    def add_message(self, content: str, role: str):
        """
        Add a message to the history with appropriate role.
        """
        if content and role in ["user", "assistant"]:
            self.messages.append({"role": role, "content": content})
        else:
            raise ValueError("Role must be either 'user' or 'assistant'.")

    def chat_completion(self) -> str:
        """
        Query the chat completion API using the class's stream setting.
        """
        response = litellm.completion(**self.model_dump(exclude_none=True))

        # Handle response based on whether streaming is enabled
        if not self.stream:
            complete_response = response["choices"][0]["message"]["content"]
        else:
            # Collect streamed chunks and rebuild the response
            chunks = [chunk for chunk in response]
            complete_response = litellm.stream_chunk_builder(chunks, messages=self.messages)["choices"][0][
                "message"
            ]["content"]

        return complete_response
