import logging

from groq import Groq

from src.config import (
GROQ_API_KEY,
GROQ_MODEL
)

logger = logging.getLogger(__name__)

client = Groq(
api_key=GROQ_API_KEY
)

def generate_response(
messages: list[dict]
) -> str:
    """
    Envoie les messages au modèle Groq
    et retourne la réponse générée.
    """

    completion = client.chat.completions.create(
    messages=messages,
    model=GROQ_MODEL
)

    response = (
    completion
    .choices[0]
    .message
    .content
    )

    return response

