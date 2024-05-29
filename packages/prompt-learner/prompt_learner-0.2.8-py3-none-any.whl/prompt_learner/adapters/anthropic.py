"""This module contains the Anthropic class,
which is an adapter for the Anthropic language model API."""

import os
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv
from .adapter import Adapter


class Anthropic(Adapter):
    """An adapter for an Anthropic language model call"""
    def __init__(self, temperature: float = 0.0, max_tokens: int = 1024, model_name: str = "claude-3-haiku-20240307"):
        super().__init__(temperature, max_tokens)
        load_dotenv()
        self.llm = ChatAnthropic(
                anthropic_api_key=os.getenv('ANTHROPIC_API_KEY'),
                model=model_name,
                temperature=self.temperature,
                max_tokens=self.max_tokens)

    def __repr__(self):
        return f"""Anthropic Adapter(model_name={self.llm.model})"""