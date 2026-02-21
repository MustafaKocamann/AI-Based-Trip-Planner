import os
from typing import Any, Literal, Optional

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field

from utils.config_loader import load_config

load_dotenv()


class ConfigLoader:
    """Thin wrapper around the YAML config dict."""

    def __init__(self) -> None:
        print("Loaded Config....")
        self._config = load_config()

    def get_item(self, key: str) -> Any:
        return self._config[key]


class ModelLoader(BaseModel):
    """
    Loads and returns a configured LLM instance.

    Supports: 'groq'
    """

    model_provider: Literal["groq"] = "groq"
    config: Optional[ConfigLoader] = Field(default=None, exclude=True)

    def model_post_init(self, context: Any) -> None:
        self.config = ConfigLoader()

    class Config:
        arbitrary_types_allowed = True

    def load_llm(self):
        """Load and return the LLM model configured for the chosen provider."""
        print(f"Loading model from provider: {self.model_provider}")

        if self.model_provider == "groq":
            print("Loading LLM from Groq...")
            groq_api_key = os.getenv("GROQ_API_KEY")
            llm_config = self.config.get_item("llm")
            model_name = llm_config["groq"]["model_name"]
            return ChatGroq(model=model_name, api_key=groq_api_key)

        raise ValueError(f"Unsupported model provider: {self.model_provider}")