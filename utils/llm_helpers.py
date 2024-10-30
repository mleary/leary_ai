import os

from openai import AzureOpenAI
from anthropic import Anthropic

from config import AZURE_API_VERSION

def setup_azure_openai_client():
    """
    Set up the Azure OpenAI client.

    Returns:
        AzureOpenAI: The Azure OpenAI client.
    """
    try:
        client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"), 
            api_version=AZURE_API_VERSION,
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        return client
    except Exception as e:
        raise RuntimeError(f"An error occurred while setting up the Azure OpenAI client: {e}")
        

def setup_anthropic_client():
    try:
        client = anthropic.Anthropic(
            api_key=os.environ.get("ANTHROPIC_API_KEY"),
        )
    except Exception as e:
        raise RuntimeError(f"An error occurred while setting up the Anthropic client: {e}")