# Project Report: AI-Assisted Development

## 1. Initial Approach

**Understanding:**
My strategy was to first break down the game into core components: game state, logic, and user interaction. I focused on identifying the minimum functional requirements (word selection, guessing system, lives tracking) and then structured the code to clearly separate the logic layer from the UI layer. I implemented the core function `update_game_state` early, since it represents the heart of the game logic.

**Assumptions:**
I assumed the game would follow a standard Hangman structure with a fixed number of lives and a predefined list of words. I also assumed that inputs would be simple (single letters) and that edge cases like invalid input could be handled minimally due to time constraints.

---

## 2. Prompting & AI Interaction

**Successes:**
AI assistance worked best when I asked for:

* Small, well-defined functions (e.g., updating game state)
* Code structure suggestions (separating logic vs UI)
* Quick debugging help when something didn’t work

Providing clear context and constraints (like “no loops” or “pure function”) significantly improved the quality of responses.

**Failures:**
There were cases where AI:

* Suggested overly complex solutions for simple problems
* Ignored constraints (e.g., adding unnecessary loops or global variables)
* Produced logically correct but impractical designs for this project size

**Analysis:**
These failures likely happened because the AI tries to generalize solutions for broader use cases rather than optimizing for simplicity. This sometimes slowed progress because I had to simplify or rewrite parts of the suggested code to better fit the assignment requirements.

---

## 3. Key Learnings

**Technical Skills:**

* Better understanding of state management in simple games
* Importance of separating logic and user interface
* Writing cleaner and more modular Python functions
* Basic use of randomness and control flow in game design

**AI Workflow:**
In future projects, I will:

* Use AI for smaller, controlled tasks instead of full solutions
* Always validate AI output instead of trusting it directly
* Be more precise with prompts to avoid irrelevant or overcomplicated answers

Overall, AI improved development speed, but maintaining control over the code was essential to ensure correctness and simplicity.
