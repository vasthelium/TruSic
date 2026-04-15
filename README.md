# TruSic
**"Less Skip More Play"**  Heart/ Core of TruSic
"Play what you feel, not what you usually play"

## IDEA 
Most music systems optimize for:
- history, genre, patterns across millions of users
But real listening doesn’t always work like that.
We Sometimes:
- Sing a song based on what we feel currently
- we hum a song without realizing	
- a memory brings back a track
- a moment triggers something specific
This project starts from a simple observation:
Music is often recalled from biographical memory, not preference.
MEAM - Musically Evoked Autobiographical Memory - LOL #Meme of this #MEAM
- Read the thinking behind this [Medium link here]

TruSic explores:
**Can we play the song closest to what a person is feeling right now?*
This is approached through a lightweight AI-driven system combining embeddings, 
behavioral signals, and state modeling.

##  CORE DIRECTION
Instead of "what do users like?" , we now ask “What is the user closest to right now?”

Current Approach MVP :This is an EARLY STAGE - EXPERIMENTAL SYSTEM.
Current flow:
- User triggers are manually written (moments, thoughts, internal states)
- Triggers are stored in a project-level data file (data/trusic_triggers.md)
- Each trigger is associated with songs
- Associated songs are captured manually recorded audio layer
- Embeddings are generated and stored
- Retrieval is done via vector similarity (pgvector)
- Closest emotional associations are returned as suggestions

In parallel:
- Basic mental / physiological state is derived from wearable data
- Currently integrated with Oura (Wearable data)
- Designed to be vendor-agnostic (expandable to other wearables)
Current usage is self-experimental (single-user system)

Mental State Layer:
Beyond explicit triggers
TruSic derives a baseline cognitive state (proxy) from wearable data.
- Uses Oura data (sleep, HRV, readiness, heart rate)
- Transforms it into a cognitive_state score
- Injects this directly into the states pipeline

Audio handling layer:
- audio files are currently manually placed
- Multimodal AI pipeline audio loading, classification, movement
- future direction → foreground recorder inside app

## RESEARCH DIRECTION
This is not just a recommendation system.

Core question?:
How do we relate music to a human’s current internal state and not just their past behavior?

What we are exploring:
- Music recall from memory (not search)
- State + trigger → association
- Moving from TASTE-based systems → STATE-based systems
- TASTE - STATE (Change it a bit lol, but deep)

Open directions:
- capturing triggers from real interactions (text, voice, passive signals)
- capturing audio inputs (hums / recordings) — currently manual, moving toward foreground 
Audio recording Layer
- combining mental state + trigger memory
- understanding signals like skip, replay, and full play
- evolving toward a simple but meaningful learning loop

## SYSTEM STRUCTURE
TruSic is built as a modular system:
- services → audio loading, classification, movement - Multi Modal AI
- ml → embeddings + state vector generation - (lightweight ML / AI modeling)
- db → PostgreSQL + vector similarity (pgvector) - Similarity Search
- pipeline → orchestration flow
- ingestion → wearable data (Oura for now)
- data/ → trigger inputs (music_triggers.md)
This structure allows:
- clean separation of logic
- easy iteration on ML vs system layers
- visibility into how triggers are formed

## 📚 REFERENCES / LEARNING
This project is shaped by: 
- Deep Learning  — Goodfellow, Bengio, Courville
- Hands-On Machine Learning — Aurélien Géron
- Behave — Robert Sapolsky
- Doug Eck (Google/DeepMind) — music + ML inspiration
- Music + memory research (MEAM concepts)
- Cornell low-power music recognition [(https://arxiv.org/abs/1711.10958)]
- Attention Is All You Need — Google Research
Used conceptually, not mathematically deep but just enough to build.
(non-academia,. I was a mischevious last bencher)

## NOTE
This is an evolving system.Some parts, especially learning logic, 
Multi Layer Perceptropn are intentionally kept simple / abstract for now.
Focus is on: getting the idea working first, then refining it

## FUTURE ROADMAP
- move from manual → real trigger capture (UI / passive / voice)  
- add audio recording (hums / voice) inside the app (currently manual file placement)  
- refine learning loop using behavioral signals (skip / replay / duration)  
- transition from simulated signals → real user interaction data  
- improve embedding quality and trigger–state associations  
- deepen integration of mental state into retrieval + learning  
- build a simple interface for real-time interaction

Closing Thought..
Music feels right not because it matches taste, but because it matches a moment.
......TruSic is an attempt to explore that.




