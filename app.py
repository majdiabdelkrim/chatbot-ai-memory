import uuid

import streamlit as st

from src.llm.prompt_service import build_system_message
from src.llm.groq_service import generate_response

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


# ============================================================
# Configuration de la page
# ============================================================

st.set_page_config(
    page_title="Chatbot IA avec Mémoire",
    page_icon="🧠",
    layout="centered"
)


# ============================================================
# Initialisation de l'historique
# ============================================================

if "history" not in st.session_state:
    st.session_state.history = []


# ============================================================
# Titre
# ============================================================

st.title("🧠 Chatbot IA avec Mémoire")

st.write(
    "Un assistant personnel capable de mémoriser, "
    "rechercher et mettre à jour les informations "
    "importantes vous concernant."
)


# ============================================================
# Afficher l'historique
# ============================================================

for message in st.session_state.history:

    with st.chat_message(message["role"]):

        st.markdown(
            message["content"]
        )


# ============================================================
# Entrée utilisateur
# ============================================================

user_message = st.chat_input(
    "Écrivez votre message..."
)


if user_message:

    # ==========================================
    # 1. Afficher le message utilisateur
    # ==========================================

    with st.chat_message("user"):

        st.markdown(
            user_message
        )


    # ==========================================
    # 2. Déterminer si le message est une mémoire
    # ==========================================

    is_memory = should_save_memory(
        user_message
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
            user_message
        )

        print(
            "🏷️ Type de mémoire :",
            memory_type
        )


        # ------------------------------------------
        # Déterminer la clé de mémoire
        # ------------------------------------------

        memory_key = detect_memory_key(
            user_message
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
            text=user_message,
            memory_type=memory_type,
            memory_key=memory_key
        )


        if saved:

            print(
                "✅ Nouvelle mémoire sauvegardée dans Pinecone."
            )

        else:

            print(
                "⚠️ Cette mémoire existe déjà. "
                "Aucun doublon créé."
            )


    else:

        print(
            "⏭️ Ce message ne contient pas "
            "d'information à mémoriser."
        )


    # ==========================================
    # 3. Rechercher les mémoires pertinentes
    # ==========================================

    memories = []


    if is_memory_related_query(
        user_message
    ):

        print(
            "🧠 Question liée à la mémoire."
        )


        # ------------------------------------------
        # Déterminer le type recherché
        # ------------------------------------------

        query_memory_type = detect_memory_query_type(
            user_message
        )

        print(
            "🏷️ Type de mémoire recherché :",
            query_memory_type
        )


        # ------------------------------------------
        # Recherche Pinecone
        # ------------------------------------------

        memories = search_memories(
            query=user_message,
            top_k=3,
            memory_type=query_memory_type
        )


    else:

        print(
            "💬 Question générale. "
            "Recherche mémoire ignorée."
        )


    # ==========================================
    # 4. Utiliser directement la nouvelle mémoire
    # ==========================================

    if is_memory and saved:

        print(
            "🔄 Utilisation directe de la nouvelle mémoire."
        )

        memories = [
            {
                "text": user_message,
                "type": memory_type,
                "key": memory_key,
                "score": 1.0
            }
        ]


    # ==========================================
    # 5. Afficher les mémoires utilisées
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
    # 6. Construire le contexte mémoire
    # ==========================================

    memory_context = "\n".join(
        f"[{memory['type']}] {memory['text']}"
        for memory in memories
    )


    # ==========================================
    # 7. Ajouter le message à l'historique
    # ==========================================

    if not is_memory:

        st.session_state.history.append(
            {
                "role": "user",
                "content": user_message
            }
        )

    else:

        print(
            "🧠 Message mémoire non ajouté "
            "à l'historique."
        )


    # ==========================================
    # 8. Construire le message système
    # ==========================================

    system_message = build_system_message(
        memory_context
    )


    # ==========================================
    # 9. Préparer les messages pour Groq
    # ==========================================

    messages_with_memory = [
        system_message
    ] + st.session_state.history


    # ==========================================
    # 10. Envoyer le message mémoire à Groq
    # ==========================================

    if is_memory:

        messages_with_memory.append(
            {
                "role": "user",
                "content": user_message
            }
        )


    # ==========================================
    # 11. Appel Groq
    # ==========================================

    with st.chat_message("assistant"):

        with st.spinner("🧠 Réflexion..."):

            reply_text = generate_response(
                messages_with_memory
            )

        st.markdown(
            reply_text
        )


    # ==========================================
    # 12. Ajouter la réponse à l'historique
    # ==========================================

    st.session_state.history.append(
        {
            "role": "assistant",
            "content": reply_text
        }
    )