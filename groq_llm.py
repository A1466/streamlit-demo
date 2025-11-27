import os
from typing import Optional, List, Mapping, Any
from pydantic import BaseModel, Field
from langchain.llms.base import LLM
from groq import Groq


class GroqLLM(LLM, BaseModel):
    api_key: str = Field(default_factory=lambda: os.environ.get("GROQ_API_KEY"))
    model_name: str = "llama-3.3-70b-versatile"
    temperature: float = 0.7

    client: Groq = None

    def __init__(self, **data):
        super().__init__(**data)
        self.client = Groq(api_key=self.api_key)

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        messages = [{"role": "user", "content": prompt}]
        response = self.client.chat.completions.create(
            messages=messages,
            model=self.model_name,
            temperature=self.temperature,
            stream=False,
        )
        return response.choices[0].message.content

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        return {"model_name": self.model_name, "temperature": self.temperature}

    @property
    def _llm_type(self) -> str:
        return "groq"


# ⚡ Pydantic v2 requirement — rebuild model
GroqLLM.model_rebuild()
