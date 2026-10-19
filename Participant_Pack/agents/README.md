# Custom Agent: Senior Python Analyst

A Copilot **custom agent** that behaves like a patient senior analyst. It asks what you are trying to do, works in small steps, explains the pandas idea behind each change, and reminds you to check the data and the code.

## Use it

1. In your Codespace open **Copilot Chat**.
2. Choose the agent picker (the agent or mode drop-down at the bottom of the chat box) and select **senior-python-analyst**.
3. Ask for help with a demo or the Session 8 exercise, for example:
   - "Explain what `01_explore_data.py` does, step by step."
   - "I want the DNA rate by speciality. What should I do first?"
   - "Review my function and tell me what could go wrong."

The agent will not solve the exercise for you in one go: it coaches you through building it.

## Where it lives

- The agent file is `senior-python-analyst.agent.md`. Copilot reads it from `.github/agents/`, and a copy is kept here so everyone can read it.
- Both copies must stay identical. If you change one, change the other.

## Safety

Synthetic data only, no secrets, no real patient data. The agent is told this, but you are responsible for what you type.
