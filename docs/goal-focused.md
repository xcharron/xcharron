# Goal Prompt — Focused MVP 1 Build

Use this when you want a controlled, decisions-locked build. Paste into `/goal`.

---

Build MVP 1 of "PantryChef" — an iOS app (Expo / React Native) where an AI
assistant suggests recipes based on what the user photographs in their fridge,
pantry, and cupboards.

## Core loop (MVP 1 scope)
0. Voice-first: the user can SPEAK to the assistant and it speaks back
   (realtime speech-to-speech), or fall back to typing — user's choice, either
   way. This is required for MVP 1; hands-free at the fridge is the ground-floor
   interaction. Put it behind a swappable voice interface (OpenAI Realtime /
   Gemini Live / Grok voice) so the provider can be changed freely.
1. User opens the camera and takes one or more photos of their food storage.
2. A multimodal LLM identifies the food items it can see.
3. When something is ambiguous (a covered bowl, an unlabeled leftover container,
   a wedge of cheese), the assistant ASKS a clarifying question rather than
   guessing — this Q&A loop is a core feature, not an afterthought.
4. The assistant maintains a running "pantry inventory" from the conversation.
5. On request, it suggests 2–3 recipes the user can make from what's on hand,
   noting any small missing items.
6. For a chosen recipe it returns: step-by-step instructions, a generated image
   of the finished dish, and a calorie/macro matrix (protein/carbs/fat + total
   calories).

## Tech decisions (already made — do not re-litigate)
- Expo (React Native), TypeScript. Target iOS first; keep it Android-compatible.
- A thin backend (FastAPI or a serverless function) holds all API keys and
  orchestrates model calls. The phone app NEVER holds provider keys.
- Multimodal LLM for vision + conversation + recipe generation (Claude or a
  GPT-4o-class model — make it swappable behind one interface).
- Voice via a swappable realtime speech interface (OpenAI Realtime / Gemini
  Live / Grok voice).
- Image generation via an image API (Gemini image / DALL·E / Flux) — also
  behind a swappable interface.
- Nutrition: LLM estimate for MVP, with the code structured so a real nutrition
  API (Nutritionix/Edamam/USDA) can drop in later.
- Persistence: Supabase (auth + Postgres + storage for photos and saved pantry
  state).

## Explicitly OUT of scope for MVP 1 (do not build yet)
- Grocery ordering. Leave a clean seam for it: MVP 1.5 will deep-link a
  pre-filled shopping list into DoorDash/Instacart, and MVP 2 will use a
  marketplace API (lean toward Instacart Connect). Just don't wire any of it.
- The shared cross-user learning engine — design the inventory/label schema so
  collective learning is possible later (labels and corrections stored as data
  that could be aggregated), but no cross-user ML/personalization work now.

## Deliverables
- A runnable Expo app: camera screen, voice + chat screen with the
  clarify-and-suggest loop, and a recipe detail view (steps + image + macro
  matrix).
- The backend orchestration layer with clearly mocked responses I can flip to
  real API calls by adding keys.
- A short README: how to run it, where to put API keys, and where the MVP 1.5 /
  MVP 2 / collective-learning seams are.
- Use mocked/stubbed model + image + voice responses where keys aren't set so
  the app runs end-to-end out of the box.

Start by proposing the file/folder structure and the swappable-provider
interfaces, then build the voice/chat → camera → recipe flow.
