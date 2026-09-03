
from src.embeddings.embedding_service import generate_embedding

from src.vectorstore.pinecone_service import (
    upsert_vector,
    search_vectors,
    find_similar_memory,
    find_memory_by_key,
    delete_vector
)


def save_memory(
    memory_id: str,
    text: str,
    memory_type: str,
    memory_key: str
):
    """
    Sauvegarde une mémoire dans Pinecone.

    Si une mémoire avec la même clé existe déjà,
    elle est remplacée par la nouvelle mémoire.

    La nouvelle mémoire est sauvegardée avant
    la suppression de l'ancienne afin d'éviter
    une perte de données en cas d'erreur.
    """

    # ==========================================
    # 1. Générer l'embedding
    # ==========================================

    embedding = generate_embedding(text)

    if len(embedding) != 384:
        raise ValueError(
            f"Dimension incorrecte : "
            f"{len(embedding)} au lieu de 384"
        )

    # ==========================================
    # 2. Chercher une mémoire avec la même clé
    # ==========================================

    existing_memory = find_memory_by_key(
        memory_key=memory_key,
        memory_type=memory_type
    )

    old_memory_id = None
    old_text = None

    if existing_memory:

        old_memory_id = existing_memory["id"]

        old_text = existing_memory["metadata"].get(
            "text"
        )

        print(
            "🔄 Mise à jour d'une mémoire existante."
        )

        print(
            "🔑 Clé :",
            memory_key
        )

        print(
            "📝 Ancienne mémoire :",
            old_text
        )

        print(
            "🆔 Ancien ID :",
            old_memory_id
        )

    # ==========================================
    # 3. Vérification des doublons sémantiques
    # ==========================================

    similar_memory = find_similar_memory(
        query_vector=embedding,
        threshold=0.90
    )

    if similar_memory:

        similar_memory_id = similar_memory["id"]

        # ------------------------------------------
        # Si la mémoire similaire est justement
        # l'ancienne mémoire de la même clé,
        # ce n'est pas un doublon problématique.
        # C'est simplement une mise à jour similaire.
        # ------------------------------------------

        if (
            old_memory_id is not None
            and similar_memory_id == old_memory_id
        ):

            print(
                "ℹ️ La mémoire similaire correspond "
                "à l'ancienne mémoire de la même clé."
            )

        else:

            print(
                "⚠️ Mémoire très similaire déjà existante."
            )

            print(
                "🆔 ID :",
                similar_memory_id
            )

            print(
                "Score :",
                similar_memory["score"]
            )

            print(
                "Mémoire :",
                similar_memory["metadata"]["text"]
            )

            return False

    # ==========================================
    # 4. Sauvegarder la nouvelle mémoire
    # ==========================================

    print(
        "💾 Sauvegarde de la nouvelle mémoire..."
    )

    upsert_vector(
        vector_id=memory_id,
        values=embedding,
        metadata={
            "text": text,
            "type": memory_type,
            "key": memory_key
        }
    )

    print(
        "✅ Nouvelle mémoire sauvegardée."
    )

    print(
        "🏷️ Type :",
        memory_type
    )

    print(
        "🔑 Clé :",
        memory_key
    )

    # ==========================================
    # 5. Supprimer l'ancienne mémoire
    # ==========================================

    if old_memory_id:

        print(
            "🗑️ Suppression de l'ancienne mémoire..."
        )

        delete_vector(
            old_memory_id
        )

        print(
            "✅ Ancienne mémoire supprimée."
        )

    # ==========================================
    # 6. Terminé
    # ==========================================

    return True


def search_memories(
    query: str,
    top_k: int = 3,
    threshold: float = 0.35,
    memory_type: str | None = None
):
    """
    Recherche les mémoires pertinentes.

    Si memory_type est fourni, la recherche
    est filtrée par type dans Pinecone.
    """

    # ==========================================
    # 1. Générer l'embedding de la question
    # ==========================================

    query_embedding = generate_embedding(query)

    if len(query_embedding) != 384:
        raise ValueError(
            f"Dimension incorrecte : "
            f"{len(query_embedding)} au lieu de 384"
        )

    print(
        "🧠 Type de mémoire reçu :",
        memory_type
    )

    # ==========================================
    # 2. Recherche Pinecone
    # ==========================================

    results = search_vectors(
        query_vector=query_embedding,
        top_k=top_k,
        memory_type=memory_type
    )

    memories = []

    # ==========================================
    # 3. Traiter les résultats
    # ==========================================

    for match in results["matches"]:

        score = match["score"]

        metadata = match.get(
            "metadata",
            {}
        )

        text = metadata.get(
            "text"
        )

        stored_memory_type = metadata.get(
            "type",
            "unknown"
        )

        memory_key = metadata.get(
            "key",
            "unknown"
        )

        print(
            "Score :",
            score
        )

        print(
            "Type :",
            stored_memory_type
        )

        print(
            "Clé :",
            memory_key
        )

        print(
            "Texte :",
            text
        )

        # ==========================================
        # Filtrer selon le score
        # ==========================================

        if score < threshold:
            continue

        if text:

            memories.append(
                {
                    "text": text,
                    "type": stored_memory_type,
                    "key": memory_key,
                    "score": score
                }
            )

    return memories

