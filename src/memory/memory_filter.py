def should_save_memory(text: str) -> bool:
    """
    Détermine si un message contient une information
    personnelle ou importante à conserver en mémoire.
    """

    text_lower = text.lower().strip()

    question_words = [
        "qui",
        "quoi",
        "quel",
        "quelle",
        "quels",
        "quelles",
        "où",
        "quand",
        "comment",
        "pourquoi",
        "est-ce que",
    ]

    if text_lower.endswith("?"):
        return False

    if any(
        text_lower.startswith(word + " ")
        for word in question_words
    ):
        return False

    memory_patterns = [
        "je m'appelle",
        "je suis",
        "je travaille",
        "mon métier est",
        "mon travail est",
        "mon projet est",
        "j'habite",
        "je vis",
        "mon objectif est",
        "je veux devenir",
        "je préfère",
        "j'aime",
        "je n'aime pas",
    ]

    return any(
        pattern in text_lower
        for pattern in memory_patterns
    )


def detect_memory_type(text: str) -> str:
    """
    Détermine le type d'une mémoire.
    """

    text_lower = text.lower().strip()

    if any(
        pattern in text_lower
        for pattern in [
            "je m'appelle",
            "je suis"
        ]
    ):
        return "personal"

    if any(
        pattern in text_lower
        for pattern in [
            "je travaille",
            "mon projet"
        ]
    ):
        return "project"

    if any(
        pattern in text_lower
        for pattern in [
            "je préfère",
            "j'aime",
            "je n'aime pas"
        ]
    ):
        return "preference"

    if any(
        pattern in text_lower
        for pattern in [
            "mon objectif",
            "je veux devenir"
        ]
    ):
        return "goal"

    return "other"


def detect_memory_key(text: str) -> str:
    """
    Détermine le sujet précis d'une mémoire.

    La clé permet d'identifier les mémoires qui parlent
    du même sujet afin de pouvoir gérer les mises à jour
    ou les contradictions.
    """

    text_lower = text.lower().strip()

    # ==========================================
    # Identité
    # ==========================================

    if "je m'appelle" in text_lower:
        return "personal_identity"

    # ==========================================
    # Profession
    # ==========================================

    if any(
        pattern in text_lower
        for pattern in [
            "je suis développeur",
            "je suis développeuse",
            "je suis ingénieur",
            "je suis ingénieure",
            "mon métier",
            "mon travail est",
            "ma profession"
        ]
    ):
        return "profession"

    # ==========================================
    # Projet actuel
    # ==========================================

    if any(
        pattern in text_lower
        for pattern in [
            "je travaille sur",
            "je travaille actuellement sur",
            "mon projet",
            "mon projet actuel"
        ]
    ):
        return "current_project"

    # ==========================================
    # Préférences technologiques
    # ==========================================

    if any(
        pattern in text_lower
        for pattern in [
            "je préfère travailler avec",
            "je préfère utiliser",
            "je préfère",
        ]
    ):
        return "technology_preference"

    # ==========================================
    # Préférences langages
    # ==========================================

    if any(
        pattern in text_lower
        for pattern in [
            "j'aime développer avec",
            "j'aime développer des applications avec",
            "j'aime programmer avec",
            "j'aime utiliser python",
            "j'aime utiliser java",
            "j'aime utiliser javascript",
            "j'aime utiliser typescript"
        ]
    ):
        return "programming_language_preference"

    # ==========================================
    # Objectifs
    # ==========================================

    if any(
        pattern in text_lower
        for pattern in [
            "mon objectif",
            "mes objectifs",
            "je veux devenir",
            "je souhaite devenir"
        ]
    ):
        return "career_goal"

    # ==========================================
    # Localisation
    # ==========================================

    if any(
        pattern in text_lower
        for pattern in [
            "j'habite",
            "je vis"
        ]
    ):
        return "location"

    # ==========================================
    # Autre
    # ==========================================

    return "other"


def is_memory_related_query(text: str) -> bool:
    """
    Détermine si une question demande
    une information personnelle mémorisée.
    """

    text_lower = text.lower().strip()

    memory_patterns = [
        "quel est mon métier",
        "quelle est ma profession",
        "quel est mon travail",
        "sur quel projet je travaille",
        "sur quel projet est-ce que je travaille",
        "quel est mon projet",
        "quels sont mes projets",
        "quelles technologies je préfère",
        "quelles technologies est-ce que je préfère",
        "quelles sont mes technologies",
        "quelles sont mes compétences",
        "quels sont mes compétences",
        "quel est mon objectif",
        "quels sont mes objectifs",
        "qu'est-ce que je préfère",
        "qu'est-ce que j'aime",
        "qu'est ce que je préfère",
        "qu'est ce que j'aime",
        "qui suis-je",
        "que sais-tu sur moi",
        "que sais-tu de moi",
    ]

    return any(
        pattern in text_lower
        for pattern in memory_patterns
    )


def detect_memory_query_type(text: str) -> str | None:
    """
    Détermine le type de mémoire recherché
    à partir de la question de l'utilisateur.
    """

    text_lower = text.lower().strip()

    personal_patterns = [
        "quel est mon métier",
        "quelle est ma profession",
        "quel est mon travail",
        "qui suis-je",
    ]

    if any(
        pattern in text_lower
        for pattern in personal_patterns
    ):
        return "personal"

    project_patterns = [
        "sur quel projet",
        "quel est mon projet",
        "quels sont mes projets",
        "sur quoi je travaille",
        "sur quoi est-ce que je travaille",
    ]

    if any(
        pattern in text_lower
        for pattern in project_patterns
    ):
        return "project"

    preference_patterns = [
        "quelles technologies je préfère",
        "quelles technologies est-ce que je préfère",
        "quelles sont mes technologies",
        "qu'est-ce que je préfère",
        "qu'est ce que je préfère",
        "qu'est-ce que j'aime",
        "qu'est ce que j'aime",
    ]

    if any(
        pattern in text_lower
        for pattern in preference_patterns
    ):
        return "preference"

    goal_patterns = [
        "quel est mon objectif",
        "quels sont mes objectifs",
    ]

    if any(
        pattern in text_lower
        for pattern in goal_patterns
    ):
        return "goal"

    return None

