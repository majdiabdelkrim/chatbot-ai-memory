# 🧠 AI Chatbot with Long-Term Memory

A personal AI chatbot built with **Python, Chainlit, Groq, Sentence Transformers and Pinecone**, capable of remembering relevant information about the user, retrieving memories when needed, and automatically updating outdated information.

The project implements a **long-term semantic memory system** using vector embeddings and a vector database.

---

## 📌 Overview

Traditional chatbots generally forget information once a conversation ends.

This project aims to solve this problem by giving the chatbot a **persistent long-term memory**.

The chatbot can:

* 🧠 Detect information that should be remembered
* 💾 Store user memories in Pinecone
* 🔎 Retrieve relevant memories using semantic search
* 🏷️ Classify memories by type
* 🔑 Associate memories with a specific key
* 🔄 Update outdated memories
* 🚫 Avoid storing normal questions
* ♻️ Prevent duplicate memories
* 🎯 Filter memory searches by type
* 💬 Maintain short-term conversation history
* 🤖 Use Groq as the LLM provider
* 📝 Generate natural responses using the relevant memories

---

## ✨ Main Features

### 🧠 Long-Term Memory

The chatbot detects personal or important information from user messages.

For example:

text
Je m'appelle Majdi et je suis développeur Full Stack.


The chatbot detects that this information should be stored and saves it in Pinecone.

---

### 🔎 Semantic Memory Search

Memories are converted into vector embeddings using:

text
sentence-transformers/all-MiniLM-L6-v2


The embeddings are stored in Pinecone.

When the user asks a personal question, the chatbot generates an embedding for the question and searches for semantically relevant memories.

Example:

text
User:
Sur quel projet je travaille ?


The chatbot retrieves the relevant project memory from Pinecone.

---

### 🏷️ Memory Classification

Each memory receives a type.

Current memory types include:

text
personal
project
preference
goal
other


Example:

text
Je m'appelle Majdi et je suis développeur Full Stack.
→ personal


text
Je travaille actuellement sur un projet de chatbot.
→ project


text
Je préfère travailler avec React.
→ preference


text
Mon objectif est de devenir développeur IA.
→ goal


---

### 🔑 Memory Keys

Each memory is also associated with a key representing its subject.

Examples:

text
personal_identity
profession
current_project
technology_preference
programming_language_preference
career_goal
location


This allows the system to identify memories that refer to the same subject.

---

### 🔄 Memory Updates

The chatbot can update an existing memory when the user provides new information about the same subject.

Example:

text
User:
Je travaille sur un projet React.


The system stores:

text
current_project → React


Later:

text
User:
Je travaille sur un projet Python.


The system detects the same memory key:

text
current_project


The old memory is replaced by the new one.

The chatbot can therefore answer:

text
Sur quel projet je travaille ?


with:

text
Vous travaillez sur un projet Python.


---

### 🚫 Duplicate Detection

Before storing a new memory, the system checks whether a very similar memory already exists.

A similarity threshold is used to avoid unnecessary duplicate vectors.

This helps keep the memory database clean.

---

### 🎯 Memory Type Filtering

The chatbot does not always search the entire memory database.

For personal questions, it first determines what type of memory is required.

For example:

text
Quel est mon métier ?


→ searches:

text
personal


or:

text
Sur quel projet je travaille ?


→ searches:

text
project


This improves memory relevance.

---

### 💬 Short-Term Conversation Memory

The project also maintains the current conversation history using Chainlit's session storage.

The architecture therefore combines:

text
Short-Term Memory
        +
Long-Term Memory


Short-term memory maintains the current conversation, while Pinecone stores persistent user information.

---

## 🏗️ Architecture

The main processing flow is:

text
                    User Message
                         │
                         ▼
                ┌─────────────────┐
                │ Memory Detection│
                └────────┬────────┘
                         │
              ┌──────────┴──────────┐
              │                     │
         Memory Message       Normal Message
              │                     │
              ▼                     │
      Detect Memory Type            │
              │                     │
              ▼                     │
       Detect Memory Key            │
              │                     │
              ▼                     │
       Generate Embedding           │
              │                     │
              ▼                     │
          Pinecone                  │
              │                     │
              ▼                     │
       Update / Deduplicate         │
              │                     │
              └──────────┬──────────┘
                         │
                         ▼
                Memory Related Query?
                         │
                  ┌──────┴──────┐
                  │             │
                 Yes            No
                  │             │
                  ▼             │
          Detect Query Type      │
                  │             │
                  ▼             │
        Semantic Search          │
          in Pinecone            │
                  │             │
                  └──────┬───────┘
                         │
                         ▼
                 Memory Context
                         │
                         ▼
                  Prompt Builder
                         │
                         ▼
                       Groq
                         │
                         ▼
                    AI Response


---

## 🛠️ Technologies

### Backend / Application

* **Python**
* **Chainlit**

### LLM

* **Groq**
* Model: `openai/gpt-oss-120b`

### Embeddings

* **Sentence Transformers**
* Model: `sentence-transformers/all-MiniLM-L6-v2`

### Vector Database

* **Pinecone**

### Configuration

* **python-dotenv**

---

## 📁 Project Structure

text
chatbot-ai-memory/
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
└── src/
    │
    ├── __init__.py
    ├── config.py
    │
    ├── embeddings/
    │   ├── __init__.py
    │   └── embedding_service.py
    │
    ├── llm/
    │   ├── __init__.py
    │   ├── groq_service.py
    │   └── prompt_service.py
    │
    ├── memory/
    │   ├── memory_service.py
    │   └── memory_filter.py
    │
    └── vectorstore/
        └── pinecone_service.py


---

## ⚙️ Installation

### 1. Clone the repository

bash
git clone https://github.com/majdiabdelkrim/chatbot-ai-memory.git


Then:

bash
cd chatbot-ai-memory


---

### 2. Create a virtual environment

Windows:

powershell
python -m venv .venv


Activate it:

powershell
.venv\Scripts\activate


Linux / macOS:

bash
python3 -m venv .venv
source .venv/bin/activate


---

### 3. Install dependencies

bash
pip install -r requirements.txt


---

## 🔐 Environment Variables

Create a `.env` file at the root of the project.

You can use `.env.example` as a template.

env
GROQ_API_KEY=your_groq_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=chatbot


### Important

Never commit your `.env` file to GitHub.

The project already includes `.env` in `.gitignore`.

---

## 🌲 Pinecone Configuration

Create a Pinecone index with the following configuration:

text
Index name:
chatbot

Dimension:
384


The dimension must match the embedding model:

text
sentence-transformers/all-MiniLM-L6-v2


which produces vectors with **384 dimensions**.

---

## ▶️ Running the Application

Start Chainlit with:

bash
chainlit run app.py


The application will be available locally through the Chainlit interface.

---

## 🧪 Example

### First interaction

text
User:
Je travaille sur un projet React.


The chatbot detects:

text
Type:
project

Key:
current_project


and stores the memory in Pinecone.

---

### Memory retrieval

text
User:
Sur quel projet je travaille ?


The system:

text
1. Detects a memory-related question
2. Detects the required memory type
3. Generates the question embedding
4. Searches Pinecone
5. Retrieves the relevant memory
6. Adds the memory to the LLM context
7. Generates the answer


Result:

text
Vous travaillez sur un projet React.


---

### Memory update

Later:

text
User:
Je travaille sur un projet Python.


The system identifies:

text
Key:
current_project


and updates the previous memory.

The next question:

text
Sur quel projet je travaille ?


returns:

text
Vous travaillez sur un projet Python.


---

## 🧩 Memory Processing

The memory system is divided into several responsibilities.

### `memory_filter.py`

Responsible for:

* Detecting whether a message should be stored
* Detecting memory type
* Detecting memory key
* Detecting whether a query is memory-related
* Detecting the type of memory requested by a query

---

### `memory_service.py`

Responsible for:

* Generating embeddings
* Saving memories
* Searching memories
* Detecting similar memories
* Updating memories

---

### `pinecone_service.py`

Responsible for communicating with Pinecone:

* Insert vectors
* Search vectors
* Filter vectors
* Find memories by key
* Delete vectors
* Clear stored memories

---

### `embedding_service.py`

Responsible for generating vector embeddings.

Model:

text
sentence-transformers/all-MiniLM-L6-v2


Output:

text
384-dimensional vector


---

### `prompt_service.py`

Responsible for building the system prompt and injecting relevant memories into the LLM context.

---

### `groq_service.py`

Responsible for communicating with the Groq API and generating the final AI response.

---

## 🧠 Memory Architecture

The project combines two different types of memory:

text
┌──────────────────────────────┐
│       Short-Term Memory      │
│                              │
│ Chainlit user session        │
│ Current conversation         │
└──────────────┬───────────────┘
               │
               +
               │
┌──────────────▼───────────────┐
│       Long-Term Memory       │
│                              │
│ Sentence Transformers        │
│          ↓                   │
│       Embeddings             │
│          ↓                   │
│        Pinecone              │
└──────────────────────────────┘


This architecture allows the chatbot to maintain both conversational context and persistent user information.

---

## 🔄 Memory Update Strategy

When a new memory is detected:

text
New Memory
    │
    ▼
Generate Embedding
    │
    ▼
Find Memory by Key
    │
    ├── No existing memory
    │       ↓
    │     Insert
    │
    └── Existing memory
            ↓
       Insert new memory
            ↓
       Delete old memory


The new memory is inserted before deleting the old memory to reduce the risk of losing the user's information if an error occurs during the update process.

---

## 🎯 Design Principles

The project follows several software engineering principles:

### Separation of Responsibilities

Each module has a specific responsibility.

text
config.py
    → configuration

embedding_service.py
    → embeddings

pinecone_service.py
    → vector database

memory_service.py
    → memory business logic

memory_filter.py
    → memory detection

prompt_service.py
    → prompt construction

groq_service.py
    → LLM communication

app.py
    → application orchestration


This makes the project easier to:

* Maintain
* Debug
* Extend
* Test
* Deploy

---

## 🚀 Future Improvements

Possible future improvements include:

* [ ] Add a dedicated memory management interface
* [ ] Add authentication and user-specific memory namespaces
* [ ] Improve memory extraction using an LLM
* [ ] Improve contradiction detection
* [ ] Add automated unit tests
* [ ] Add structured logging
* [ ] Add Docker support
* [ ] Deploy the application
* [ ] Add observability and monitoring
* [ ] Improve semantic retrieval and ranking
* [ ] Add memory expiration or temporal validity
* [ ] Add memory editing and deletion from the UI

---

## 📚 What I Learned

This project helped me understand and implement several important AI concepts:

* Vector embeddings
* Semantic search
* Vector databases
* Long-term AI memory
* Short-term conversational memory
* Retrieval-based prompting
* LLM integration
* Prompt engineering
* Memory classification
* Duplicate detection
* Memory update strategies
* Separation of concerns
* Modular Python architecture
* API integration

---

## 👨‍💻 Author

**Majdi Abdelkrim**

Software Engineer — Full-Stack & AI

Tunisia

Interested in:

* Full-Stack Development
* Artificial Intelligence
* Generative AI
* RAG
* LLM Applications
* AI Agents
* Backend Development

---

## ⭐ Project Goal

The goal of this project is to explore how modern AI applications can combine **LLMs, embeddings and vector databases** to create assistants capable of maintaining useful long-term knowledge about their users.

This project is part of my journey toward building a professional profile combining:

# 🧠 AI Chatbot with Long-Term Memory

A personal AI chatbot built with **Python, Chainlit, Groq, Sentence Transformers and Pinecone**, capable of remembering relevant information about the user, retrieving memories when needed, and automatically updating outdated information.

The project implements a **long-term semantic memory system** using vector embeddings and a vector database.

---

## 📌 Overview

Traditional chatbots generally forget information once a conversation ends.

This project aims to solve this problem by giving the chatbot a **persistent long-term memory**.

The chatbot can:

* 🧠 Detect information that should be remembered
* 💾 Store user memories in Pinecone
* 🔎 Retrieve relevant memories using semantic search
* 🏷️ Classify memories by type
* 🔑 Associate memories with a specific key
* 🔄 Update outdated memories
* 🚫 Avoid storing normal questions
* ♻️ Prevent duplicate memories
* 🎯 Filter memory searches by type
* 💬 Maintain short-term conversation history
* 🤖 Use Groq as the LLM provider
* 📝 Generate natural responses using the relevant memories

---

## ✨ Main Features

### 🧠 Long-Term Memory

The chatbot detects personal or important information from user messages.

For example:

text
Je m'appelle Majdi et je suis développeur Full Stack.


The chatbot detects that this information should be stored and saves it in Pinecone.

---

### 🔎 Semantic Memory Search

Memories are converted into vector embeddings using:

text
sentence-transformers/all-MiniLM-L6-v2


The embeddings are stored in Pinecone.

When the user asks a personal question, the chatbot generates an embedding for the question and searches for semantically relevant memories.

Example:

text
User:
Sur quel projet je travaille ?


The chatbot retrieves the relevant project memory from Pinecone.

---

### 🏷️ Memory Classification

Each memory receives a type.

Current memory types include:

text
personal
project
preference
goal
other


Example:

text
Je m'appelle Majdi et je suis développeur Full Stack.
→ personal


text
Je travaille actuellement sur un projet de chatbot.
→ project


text
Je préfère travailler avec React.
→ preference


text
Mon objectif est de devenir développeur IA.
→ goal


---

### 🔑 Memory Keys

Each memory is also associated with a key representing its subject.

Examples:

text
personal_identity
profession
current_project
technology_preference
programming_language_preference
career_goal
location


This allows the system to identify memories that refer to the same subject.

---

### 🔄 Memory Updates

The chatbot can update an existing memory when the user provides new information about the same subject.

Example:

text
User:
Je travaille sur un projet React.


The system stores:

text
current_project → React


Later:

text
User:
Je travaille sur un projet Python.


The system detects the same memory key:

text
current_project


The old memory is replaced by the new one.

The chatbot can therefore answer:

text
Sur quel projet je travaille ?


with:

text
Vous travaillez sur un projet Python.


---

### 🚫 Duplicate Detection

Before storing a new memory, the system checks whether a very similar memory already exists.

A similarity threshold is used to avoid unnecessary duplicate vectors.

This helps keep the memory database clean.

---

### 🎯 Memory Type Filtering

The chatbot does not always search the entire memory database.

For personal questions, it first determines what type of memory is required.

For example:

text
Quel est mon métier ?


→ searches:

text
personal


or:

text
Sur quel projet je travaille ?


→ searches:

text
project


This improves memory relevance.

---

### 💬 Short-Term Conversation Memory

The project also maintains the current conversation history using Chainlit's session storage.

The architecture therefore combines:

text
Short-Term Memory
        +
Long-Term Memory


Short-term memory maintains the current conversation, while Pinecone stores persistent user information.

---

## 🏗️ Architecture

The main processing flow is:

text
                    User Message
                         │
                         ▼
                ┌─────────────────┐
                │ Memory Detection│
                └────────┬────────┘
                         │
              ┌──────────┴──────────┐
              │                     │
         Memory Message       Normal Message
              │                     │
              ▼                     │
      Detect Memory Type            │
              │                     │
              ▼                     │
       Detect Memory Key            │
              │                     │
              ▼                     │
       Generate Embedding           │
              │                     │
              ▼                     │
          Pinecone                  │
              │                     │
              ▼                     │
       Update / Deduplicate         │
              │                     │
              └──────────┬──────────┘
                         │
                         ▼
                Memory Related Query?
                         │
                  ┌──────┴──────┐
                  │             │
                 Yes            No
                  │             │
                  ▼             │
          Detect Query Type      │
                  │             │
                  ▼             │
        Semantic Search          │
          in Pinecone            │
                  │             │
                  └──────┬───────┘
                         │
                         ▼
                 Memory Context
                         │
                         ▼
                  Prompt Builder
                         │
                         ▼
                       Groq
                         │
                         ▼
                    AI Response


---

## 🛠️ Technologies

### Backend / Application

* **Python**
* **Chainlit**

### LLM

* **Groq**
* Model: `openai/gpt-oss-120b`

### Embeddings

* **Sentence Transformers**
* Model: `sentence-transformers/all-MiniLM-L6-v2`

### Vector Database

* **Pinecone**

### Configuration

* **python-dotenv**

---

## 📁 Project Structure

text
chatbot-ai-memory/
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
└── src/
    │
    ├── __init__.py
    ├── config.py
    │
    ├── embeddings/
    │   ├── __init__.py
    │   └── embedding_service.py
    │
    ├── llm/
    │   ├── __init__.py
    │   ├── groq_service.py
    │   └── prompt_service.py
    │
    ├── memory/
    │   ├── memory_service.py
    │   └── memory_filter.py
    │
    └── vectorstore/
        └── pinecone_service.py


---

## ⚙️ Installation

### 1. Clone the repository

bash
git clone https://github.com/YOUR_USERNAME/chatbot-ai-memory.git


Then:

bash
cd chatbot-ai-memory


---

### 2. Create a virtual environment

Windows:

powershell
python -m venv .venv


Activate it:

powershell
.venv\Scripts\activate


Linux / macOS:

bash
python3 -m venv .venv
source .venv/bin/activate


---

### 3. Install dependencies

bash
pip install -r requirements.txt


---

## 🔐 Environment Variables

Create a `.env` file at the root of the project.

You can use `.env.example` as a template.

env
GROQ_API_KEY=your_groq_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=chatbot


### Important

Never commit your `.env` file to GitHub.

The project already includes `.env` in `.gitignore`.

---

## 🌲 Pinecone Configuration

Create a Pinecone index with the following configuration:

text
Index name:
chatbot

Dimension:
384


The dimension must match the embedding model:

text
sentence-transformers/all-MiniLM-L6-v2


which produces vectors with **384 dimensions**.

---

## ▶️ Running the Application

Start Chainlit with:

bash
chainlit run app.py


The application will be available locally through the Chainlit interface.

---

## 🧪 Example

### First interaction

text
User:
Je travaille sur un projet React.


The chatbot detects:

text
Type:
project

Key:
current_project


and stores the memory in Pinecone.

---

### Memory retrieval

text
User:
Sur quel projet je travaille ?


The system:

text
1. Detects a memory-related question
2. Detects the required memory type
3. Generates the question embedding
4. Searches Pinecone
5. Retrieves the relevant memory
6. Adds the memory to the LLM context
7. Generates the answer


Result:

text
Vous travaillez sur un projet React.


---

### Memory update

Later:

text
User:
Je travaille sur un projet Python.


The system identifies:

text
Key:
current_project


and updates the previous memory.

The next question:

text
Sur quel projet je travaille ?


returns:

text
Vous travaillez sur un projet Python.


---

## 🧩 Memory Processing

The memory system is divided into several responsibilities.

### `memory_filter.py`

Responsible for:

* Detecting whether a message should be stored
* Detecting memory type
* Detecting memory key
* Detecting whether a query is memory-related
* Detecting the type of memory requested by a query

---

### `memory_service.py`

Responsible for:

* Generating embeddings
* Saving memories
* Searching memories
* Detecting similar memories
* Updating memories

---

### `pinecone_service.py`

Responsible for communicating with Pinecone:

* Insert vectors
* Search vectors
* Filter vectors
* Find memories by key
* Delete vectors
* Clear stored memories

---

### `embedding_service.py`

Responsible for generating vector embeddings.

Model:

text
sentence-transformers/all-MiniLM-L6-v2


Output:

text
384-dimensional vector


---

### `prompt_service.py`

Responsible for building the system prompt and injecting relevant memories into the LLM context.

---

### `groq_service.py`

Responsible for communicating with the Groq API and generating the final AI response.

---

## 🧠 Memory Architecture

The project combines two different types of memory:

text
┌──────────────────────────────┐
│       Short-Term Memory      │
│                              │
│ Chainlit user session        │
│ Current conversation         │
└──────────────┬───────────────┘
               │
               +
               │
┌──────────────▼───────────────┐
│       Long-Term Memory       │
│                              │
│ Sentence Transformers        │
│          ↓                   │
│       Embeddings             │
│          ↓                   │
│        Pinecone              │
└──────────────────────────────┘


This architecture allows the chatbot to maintain both conversational context and persistent user information.

---

## 🔄 Memory Update Strategy

When a new memory is detected:

text
New Memory
    │
    ▼
Generate Embedding
    │
    ▼
Find Memory by Key
    │
    ├── No existing memory
    │       ↓
    │     Insert
    │
    └── Existing memory
            ↓
       Insert new memory
            ↓
       Delete old memory


The new memory is inserted before deleting the old memory to reduce the risk of losing the user's information if an error occurs during the update process.

---

## 🎯 Design Principles

The project follows several software engineering principles:

### Separation of Responsibilities

Each module has a specific responsibility.

text
config.py
    → configuration

embedding_service.py
    → embeddings

pinecone_service.py
    → vector database

memory_service.py
    → memory business logic

memory_filter.py
    → memory detection

prompt_service.py
    → prompt construction

groq_service.py
    → LLM communication

app.py
    → application orchestration


This makes the project easier to:

* Maintain
* Debug
* Extend
* Test
* Deploy

---

## 🚀 Future Improvements

Possible future improvements include:

* [ ] Add a dedicated memory management interface
* [ ] Add authentication and user-specific memory namespaces
* [ ] Improve memory extraction using an LLM
* [ ] Improve contradiction detection
* [ ] Add automated unit tests
* [ ] Add structured logging
* [ ] Add Docker support
* [ ] Deploy the application
* [ ] Add observability and monitoring
* [ ] Improve semantic retrieval and ranking
* [ ] Add memory expiration or temporal validity
* [ ] Add memory editing and deletion from the UI

---

## 📚 What I Learned

This project helped me understand and implement several important AI concepts:

* Vector embeddings
* Semantic search
* Vector databases
* Long-term AI memory
* Short-term conversational memory
* Retrieval-based prompting
* LLM integration
* Prompt engineering
* Memory classification
* Duplicate detection
* Memory update strategies
* Separation of concerns
* Modular Python architecture
* API integration

---

## 👨‍💻 Author

**Majdi Abdelkrim**

Software Engineer — Full-Stack & AI

Tunisia

Interested in:

* Full-Stack Development
* Artificial Intelligence
* Generative AI
* RAG
* LLM Applications
* AI Agents
* Backend Development

---

## ⭐ Project Goal

The goal of this project is to explore how modern AI applications can combine **LLMs, embeddings and vector databases** to create assistants capable of maintaining useful long-term knowledge about their users.

This project is part of my journey toward building a professional profile combining:

text
Full-Stack Development
        +
Artificial Intelligence
        =
Full-Stack + AI Engineer



