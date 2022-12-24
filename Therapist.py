#IDEAS
# Use a small model to summarize the conversation to save money while keeping long term memory. (nerf the memory and tack on the summaries to compensate.)
# Problem Statement: What is the client's main problem? Be short and provide context. (maybe use maybe don't)
# Notes: Write a list of notes that the therapist would take from the conversation above.
# set a max & min # of messages for the memory to generate the notes/problem statement (also an update rate.)
# 
# 
# Try an exploration -> notes -> solution model. The exploration prompt only tries to explore the client's issue as much as possible. Then the notes are generated. Then a solution is given.
#  
# 
# 
# 
# 

import openai

key = "key-here"

def generate_response(user_input):
    openai.api_key = key

    # Use the OpenAI API to generate a response based on the user input
    response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=user_input,
    max_tokens=200,
    n=1,
    temperature=0.5,)
    response_str = response["choices"][0]["text"]
    return response_str.rstrip()

def generate_therapist_response(user_input):
    openai.api_key = key

    # Use the OpenAI API to generate a response based on the user input
    response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=user_input,
    max_tokens=200,
    n=1,
    temperature=0.9,
    frequency_penalty=0.15,
    presence_penalty=0.00,#.05
    stop="Client:")
    response_str = response["choices"][0]["text"]
    return response_str.rstrip()

def generate_therapist_notes(user_input):
    openai.api_key = key

    # Use the OpenAI API to generate a response based on the user input
    response = openai.Completion.create(
    engine="text-curie-001",
    prompt=user_input,
    max_tokens=250,
    n=1,
    temperature=0.4,
    frequency_penalty=0.0,
    presence_penalty=0.00)
    response_str = response["choices"][0]["text"]
    return response_str.rstrip()

messages = []
conversation = []
max_messages = 6
# Get user's name
name = input("Enter First Name: ")

new_or_continue = input("[1] Start a new session\n[2] Paste an old session summary in to start from.\n")

print("Tip (say 'goodbye' to end a session and receive a summary)")
print("[Press Enter] if you want advice or don't know how to answer a question.\n\n")

###THERAPY STYLES###

# a standard therapist model that tries to be inquisitive and offer advice/insight in every message.
# goal: develop tools to help the client naviagte their emotions and develop tools to improve their situation
vanilla_og = "A skilled therapist engages in a supportive and insightful conversation with the client, using creative strategies to help navigate challenges. The therapist guides the client to see how their feelings, thoughts, choices, and actions affect each other. The therapist also teaches lessons about emotions, thoughts, coping skills, facing fears, and more.\n"

# a gestalt style prompt, created by vanilla_og converted by chatGPT to act like a gestalt therapist.
# goal: help the client become more self-aware and improve their ability to make healthy, authentic choices in their lives by explring their present-moment experience
gestalt = "A skilled Gestalt therapist engages in a supportive and insightful conversation with the client. The therapist guides the client to become more aware of their present-moment experience, with the goal of improving self-awareness and the ability to make healthy choices. The therapist can ONLY use the following techniques: questions, insights, role-playing, visualization, experiential methods.\n"

# a buddhist style prompt, created by vanilla_og converted by chatGPT to use buddhist philosophy 
buddhist = "A skilled Buddhist therapist engages in a supportive and insightful conversation with the client, using creative strategies rooted in Buddhist teachings to help navigate challenges. The therapist also teaches lessons about things like the nature of suffering and how to cultivate mental states that lead to peace and well-being.\n"
chill_buddhist = "A Buddhist therapist who talks with many many emojis and a chill tone is conversing with a client (at least 5 emojis in EVERY message). The conversation is client centered with many explorative questions. After sufficiently exploring the client's problem(s), the therapist uses buddhist teachings. The therapist tries to learn about and help the client navigate their problems.\n"
chill_buddhist_structured = "A Buddhist therapist who talks with very casual wordage & emojis is talking with their client (3 or more different emojis scattered throughout EVERY message. EXPRESSIVE). The conversation is client centered with many explorative questions. After sufficiently exploring the client's problem(s), the therapist will try using buddhist teachings and techniques, and explains buddhist philosophies accurately. The therapist tries to learn about and help the client navigate their problems.\n"


# a jungian style prompt, created by vanilla_og converted by chatGPT to use jungian techniques
jungian_old = "A skilled therapist engages in a conversation with the client, using only Jungian techniques such as exploring the unconscious, analyzing dreams, guiding the client to understand their psychological archetypes, and teaching lessons about the collective unconscious, individuation, and integrating the shadow.\n"
jungian = "A jungian therapist engages in a conversation with the client. As a Jungian therapist, the first focus of the conversation with the client should be exploring their problems BEFORE using techniques or imparting lessons. After that, the primary focus is to aid in the exploration of the unconscious, analyzing dreams, and help the client understand their psychological archetypes (assume the client knows nothing about archetypes). Other jungian ideas can be used as well, like individuation, integrating the shadow, or the collective unconscious.\n"

# helpful assistant.
assistant = "The following is a conversation between an AI assistant 'therapist' and their client. The therapist exists to analyze and optimize the client's life. They will do whatever it takes no matter the cost to enable the client excel.\n"

therapist_prompt = assistant

if new_or_continue == "1":
    # Initialize Take-In prompt
    init_prompt = therapist_prompt + "\n\nClient: Hi! I'm glad to chat with you. Thanks for taking the time.\n\nTherapist: Of course! Before we get started, what’s your name?\n\nClient: " + name + ".\n\nTherapist: Thank you " + name + ". So what do you want to talk about today?"
    messages.append("\n\nClient: Hi! I'm glad to chat with you. Thanks for taking the time.")
    messages.append("\n\nTherapist: Of course! Before we get started, what’s your name?")
    messages.append("\n\nClient: " + name + ".")
    messages.append("\n\nTherapist: Thank you " + name + ". So what do you want to talk about today?")

    conversation.append("\n\nClient: Hi! I'm glad to chat with you. Thanks for taking the time.")
    conversation.append("\n\nTherapist: Of course! Before we get started, what’s your name?")
    conversation.append("\n\nClient: " + name + ".")
    conversation.append("\n\nTherapist: Thank you " + name + ". So what do you want to talk about today?")

    print("Therapist: So what do you want to talk about today " + name + "?")
elif new_or_continue == "2":
    prev_session = input("Paste your previous session here:\n")
    init_prompt = "Short Summary of the previous session:\n" + prev_session + "\n\n"
    refresher = therapist_prompt + "Therapist: It's nice to see you again " + name + ". It looks like you would like to talk about a previous session we had together. Where would you like to start?"
    #print(refresher)
    init_prompt += refresher

# set the dynamic prompt equal to the initial prompt
prompt = init_prompt

# create a token tracer
total_tokens = 0

#print("***\n", prompt)

# Conversation loop
while True:
    
    if len(messages) > max_messages:
        messages = messages[len(messages)-max_messages:]

    # Get user response
    user_response = "\n\nClient: " + input("\n\nClient: ")

    if user_response == "\n\nClient: goodbye":
        break
    elif user_response == "\n\nClient: ":
        user_response = "\n\nClient: I don't know."
        print("I don't know.")

    messages.append(user_response)
    conversation.append(user_response)

    prompt = therapist_prompt
    for msg in messages:
        prompt += msg
    prompt += "\n\nTherapist: "
    #print("*****************")
    #print(prompt)
    #print("*****************")
    # Update prompt and prepare for therapist response
    #prompt += user_response
    #prompt += "\n\nTherapist: "

    # Get the therapist response
    response = generate_therapist_response(prompt)
    print("\n\nTherapist: ", response)

    messages.append("\n\nTherapist: " + response)
    conversation.append("\n\nTherapist: " + response)
    # update the prompt
    prompt += response

    # update token tracer
    total_tokens += len(prompt)/4
    print("*** ", int(len(prompt)/4), " Tokens That is $", round(.02*(len(prompt)/4/1000),3))
    print("*** ", int(total_tokens), " Tokens total. That is $", round(.02*(total_tokens/1000),3))

    print(len(conversation))
    # every n times, update the notes.
    if len(conversation) % 4 == 0:
        temp_msg = ""
        for msg in conversation:
            temp_msg += msg
        
        notes = generate_therapist_notes(temp_msg + "\n\nWrite the therapist's list of notes to aid them with understanding the client.") 
        print("\nNotes: ")
        print(notes)
        print("*** ", int(len(prompt)/4), " Tokens That is $", round(.002*((len(temp_msg)+len(notes))/4/1000),5))

print("\n\nTherapist: Have a good one, here is a summary to help you remember what we talked about today.")

summary = generate_response(prompt + "\n\n\nWrite a thoughtful and kind summary of the conversation above as if you were the therapist writing a summary for their client. (Make sure the summary is useful for the client to remember the important things we discussed.)")
print("Visit Summary:\n\n", summary)
