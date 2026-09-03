import os

from dotenv import load_dotenv
from pinecone import Pinecone


load_dotenv()


PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")


if not PINECONE_API_KEY:
    raise ValueError(
        "PINECONE_API_KEY est manquante dans le fichier .env"
    )


if not PINECONE_INDEX_NAME:
    raise ValueError(
        "PINECONE_INDEX_NAME est manquante dans le fichier .env"
    )


pc = Pinecone(
    api_key=PINECONE_API_KEY
)


index = pc.Index(
    PINECONE_INDEX_NAME
)


def upsert_vector(
    vector_id: str,
    values: list[float],
    metadata: dict
):
    index.upsert(
        vectors=[
            {
                "id": vector_id,
                "values": values,
                "metadata": metadata
            }
        ]
    )


def search_vectors(
    query_vector: list[float],
    top_k: int = 3,
    memory_type: str | None = None
):
    """
    Recherche les vecteurs similaires dans Pinecone.

    Si memory_type est fourni, la recherche est
    limitée à ce type de mémoire.
    """

    if memory_type:

        print(
            f"🔎 Recherche Pinecone filtrée par type : {memory_type}"
        )

        results = index.query(
            vector=query_vector,
            top_k=top_k,
            include_metadata=True,
            filter={
                "type": {
                    "$eq": memory_type
                }
            }
        )

    else:

        print(
            "🔎 Recherche Pinecone sans filtre de type."
        )

        results = index.query(
            vector=query_vector,
            top_k=top_k,
            include_metadata=True
        )

    return results


def find_similar_memory(
    query_vector: list[float],
    threshold: float = 0.90
):
    """
    Recherche une mémoire très similaire
    pour éviter les doublons.
    """

    results = index.query(
        vector=query_vector,
        top_k=1,
        include_metadata=True
    )

    if not results["matches"]:
        return None

    match = results["matches"][0]

    if match["score"] >= threshold:
        return match

    return None


def find_memory_by_key(
    memory_key: str,
    memory_type: str | None = None
):
    """
    Recherche une mémoire existante à partir
    de sa clé de sujet.

    Exemple :

    memory_key = "technology_preference"

    Pinecone recherche une mémoire possédant :

    key = technology_preference

    Le type peut également être utilisé comme
    filtre supplémentaire.
    """

    print(
        "🔍 Recherche d'une mémoire avec la clé :",
        memory_key
    )

    memory_filter = {
        "key": {
            "$eq": memory_key
        }
    }

    if memory_type:

        memory_filter["type"] = {
            "$eq": memory_type
        }

    results = index.query(
        vector=[0.0] * 384,
        top_k=10,
        include_metadata=True,
        filter=memory_filter
    )

    if not results["matches"]:

        print(
            "❌ Aucune mémoire trouvée avec cette clé."
        )

        return None

    match = results["matches"][0]

    print(
        "✅ Mémoire trouvée avec la clé :",
        memory_key
    )

    print(
        "ID :",
        match["id"]
    )

    print(
        "Type :",
        match["metadata"].get("type")
    )

    print(
        "Clé :",
        match["metadata"].get("key")
    )

    print(
        "Texte :",
        match["metadata"].get("text")
    )

    return match



def clear_memory():
    """
    Supprime toutes les mémoires de Pinecone.

    Si le namespace n'existe pas ou s'il n'y a
    aucune mémoire, le reset peut continuer normalement.
    """

    try:

        index.delete(
            delete_all=True
        )

        print(
            "🗑️ Toutes les mémoires ont été supprimées de Pinecone."
        )

    except Exception as e:

        error_message = str(e)

        if "Namespace not found" in error_message:

            print(
                "ℹ️ Aucune mémoire à supprimer : "
                "le namespace n'existe pas encore."
            )

        else:

            raise

def delete_vector(
    vector_id: str
):
    """
    Supprime une mémoire de Pinecone
    à partir de son identifiant.
    """

    print(
        "🗑️ Suppression de la mémoire :",
        vector_id
    )

    index.delete(
        ids=[vector_id]
    )

    print(
        "✅ Mémoire supprimée avec succès."
    )



