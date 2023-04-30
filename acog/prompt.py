

def create(name, persona, history, input):
    conversation = ""
    for interaction in history:
        conversation = conversation + f"You: {interaction['you']}\n"
        conversation = conversation + f"{name}: {interaction['bot']}\n"

    return f"{name}'s persona: {persona}\n<START>\n{conversation}<START>\nYou: {input}\n{name}: "

def create_history(conversations):
    return conversations

def update_history(history, interaction):
    history.append(interaction)
    to_slice = -5 + len(history)
    history = history[to_slice:]
    return history
