# LinguaFlowCore
A project to create a tool for working in English to memorize words and phrases

## General concept of the project
### Title (working) 
LinguaFlowCore

###Goal: 
To create a personalized English learning system where ML algorithms adjust repetition frequency, material complexity, and learning pace to the specific user.

## Architecture (high-level)

Components:

1. **Frontend Web (React / Next.js)** — card interface, statistics, profile, text reading.

2. **Mobile App (Flutter / React Native)** — syncs with the same server.

3. **Backend (FastAPI or Spring Boot)** — REST API, user logic, iteration plan, statistics.

4. **ML Service (Python, FastAPI separate microservice)** — personalization, recommendations, complexity classification.

5. **Database (PostgreSQL)** — users, cards, iteration history, text.

6. **Storage (S3 / MinIO)** — audio, images, user content.

**Optional:**

7. **Redis** — cache and task broker (e.g., for asynchronous card generation).

8. **Celery / RabbitMQ** — background processing (voiceover, text analysis).

## Main functions
### 1. Working with Flashcards

- Create flashcards (word, translation, example, audio).

- Group by topic or book.

- Automatic generation of flashcards from a text/book.

- Word difficulty is determined by an ML model (CEFR levels: A1–C2).

### 2. Repetition with ML

- Spaced Repetition (SRS) algorithm, enhanced with ML:

- The model predicts the probability of forgetting (p(forgotten)).

- Repetition intervals are dynamically adjusted.

- Use models like LightGBM/CatBoost for a personalized repetition schedule.

### 3. Voice-over

- Integration with TTS (e.g., ElevenLabs API, gTTS, or a local VITS model).

- Ability to compare user pronunciation (Speech-to-Text + accuracy assessment).

### 4. Reading Progress

- The user loads a text/book.

- Automatic highlighting of unfamiliar words (based on user history).

- Ability to add words from the text to a personal dictionary.

- Counting the number of unique words by difficulty level (A1–C2).

### 5. Analytics and Gamification

- Graphs of word learning and forgetting.

- Progress by topic/level.

- Achievements, streaks, rankings.

## ML components
| ML task | Goal | Technologies |
| ------------- | ------------- | -------- |
| 1. Word difficulty assessment | Determine the CEFR level of a word (A1–C2) | BERT / DistilBERT + classifier |
| 2. Forgetting Model | Predict how many days it will take for a user to forget a word | CatBoost / XGBoost |
| 3. Flashcard Recommendation | Select words for review | RL / Bandit algorithm |
| 4. Speech Analysis | Pronunciation check (Speech2Text + phoneme error rate) | Whisper / Wav2Vec2 |
| 5. Automatic Example | GPT Model / LLM on the  server | OpenAI / Mistral API |


## API examples (REST, FastAPI)
GET /api/words/today         — get words to repeat
POST /api/words/review       — submit revision results
POST /api/texts/upload       — download the book text
GET /api/stats/progress      — get statistics
GET /api/tts/{word_id}       — get a link to the audio


##Libraries versions:
SQLAlchemy == 1.4.17

psycopg2 == 2.9.11

pydantic == 2.11.7

passlib == 1.7.4

pytest == 8.4.1

httpx == 0.28.1

python-jose == 3.5.0

spacy == 3.8.11

python -m spacy download en_core_web_sm

sentence-transformers == 5.2.0