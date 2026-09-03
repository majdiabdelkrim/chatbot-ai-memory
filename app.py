
import uuid

import chainlit as cl


from src.llm.prompt_service import (
    build_system_message
)
from src.llm.groq_service import (
    generate_response
)
from src.memory.memory_service import (
    search_memories,
    save_memory
)

from src.memory.memory_filter import (
    should_save_memory,
    detect_memory_type,
    is_memory_related_query,
    detect_memory_query_type,
    detect_memory_key
)





@cl.on_chat_start
async def start():

    cl.user_session.set(
        "history",
        []
    )


@cl.on_message
async def main(message: cl.Message):

    history = cl.user_session.get(
        "history"
    )

    # ==========================================
    # 1. Déterminer si le message est une mémoire
    # ==========================================

    is_memory = should_save_memory(
        message.content
    )

    memory_type = None
    memory_key = None
    saved = False

    if is_memory:

        print(
            "💾 Ce message contient une information à mémoriser."
        )

        # ------------------------------------------
        # Déterminer le type de mémoire
        # ------------------------------------------

        memory_type = detect_memory_type(
            message.content
        )

        print(
            "🏷️ Type de mémoire :",
            memory_type
        )

        # ------------------------------------------
        # Déterminer la clé de mémoire
        # ------------------------------------------

        memory_key = detect_memory_key(
            message.content
        )

        print(
            "🔑 Clé de mémoire :",
            memory_key
        )

        # ------------------------------------------
        # Générer un identifiant unique
        # ------------------------------------------

        memory_id = f"memory-{uuid.uuid4()}"

        # ------------------------------------------
        # Sauvegarder / mettre à jour la mémoire
        # ------------------------------------------

        saved = save_memory(
            memory_id=memory_id,
            text=message.content,
            memory_type=memory_type,
            memory_key=memory_key
        )

        if saved:

            print(
                "✅ Nouvelle mémoire sauvegardée dans Pinecone."
            )

        else:

            print(
                "⚠️ Cette mémoire existe déjà. Aucun doublon créé."
            )

    else:

        print(
            "⏭️ Ce message ne contient pas d'information à mémoriser."
        )

    # ==========================================
    # 2. Rechercher les mémoires pertinentes
    # ==========================================

    memories = []

    if is_memory_related_query(
        message.content
    ):

        print(
            "🧠 Question liée à la mémoire."
        )

        # ------------------------------------------
        # Déterminer le type de mémoire recherché
        # ------------------------------------------

        query_memory_type = detect_memory_query_type(
            message.content
        )

        print(
            "🏷️ Type de mémoire recherché :",
            query_memory_type
        )

        # ------------------------------------------
        # Recherche dans Pinecone
        # ------------------------------------------

        memories = search_memories(
            query=message.content,
            top_k=3,
            memory_type=query_memory_type
        )

    else:

        print(
            "💬 Question générale. Recherche mémoire ignorée."
        )

    # ==========================================
    # 3. Utiliser directement la nouvelle mémoire
    # ==========================================

    if is_memory and saved:

        print(
            "🔄 Utilisation directe de la nouvelle mémoire."
        )

        memories = [
            {
                "text": message.content,
                "type": memory_type,
                "key": memory_key,
                "score": 1.0
            }
        ]

    # ==========================================
    # 4. Afficher les mémoires utilisées
    # ==========================================

    print(
        "\n🧠 Mémoires utilisées :"
    )

    for memory in memories:

        print(
            f"- [{memory['type']}] "
            f"(key: {memory['key']}) "
            f"(score: {memory['score']:.3f}) "
            f"{memory['text']}"
        )

    # ==========================================
    # 5. Construire le contexte mémoire
    # ==========================================

    memory_context = "\n".join(
        f"[{memory['type']}] {memory['text']}"
        for memory in memories
    )

    # ==========================================
    # 6. Gestion de l'historique
    # ==========================================

    if not is_memory:

        history.append(
            {
                "role": "user",
                "content": message.content
            }
        )

    else:

        print(
            "🧠 Message mémoire non ajouté à l'historique."
        )

    # ==========================================
    # 7. Construire le message système
    # ==========================================

    system_message = build_system_message(
        memory_context
    )

    # ==========================================
    # 8. Préparer les messages pour Groq
    # ==========================================

    messages_with_memory = [
        system_message
    ] + history

    # Si le message actuel contient une information
    # mémoire, il doit quand même être envoyé à Groq.

    if is_memory:

        messages_with_memory.append(
            {
                "role": "user",
                "content": message.content
            }
        )

    # ==========================================
    # 9. Appel Groq
    # ==========================================

    reply_text = generate_response(
        messages_with_memory
    )
    # ==========================================
    # 11. Ajouter la réponse à l'historique
    # ==========================================

    history.append(
        {
            "role": "assistant",
            "content": reply_text
        }
    )

    cl.user_session.set(
        "history",
        history
    )

    # ==========================================
    # 12. Afficher la réponse
    # ==========================================

    await cl.Message(
        content=reply_text
    ).send()

