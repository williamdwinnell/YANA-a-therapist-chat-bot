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
    frequency_penalty=0.1,
    presence_penalty=0.05,
    stop="Client:")
    response_str = response["choices"][0]["text"]
    return response_str.rstrip()

# Get user's name
name = input("Enter First Name: ")

new_or_continue = input("[1] Start a new session\n[2] Paste an old session summary in to start from.\n")

print("Tip (say 'goodbye' to end a session and receive a summary)")
print("[Press Enter] if you want advice or don't know how to answer a question.\n\n")

# detailed
#therapist_prompt = "The following is a conversation with a professional therapist. The therapist uses their knowledge and expertise in psychotherapy to help the client navigate their problems. They show compassion and empathy towards the client, and acknowledge their feelings and thoughts without judgement. The therapist focuses on providing support and guidance, rather than asking a lot of questions.\n\n"

# price optimized
#therapist_prompt = "The following is a conversation with a professional therapist. The therapist uses their expertise to help the client and shows compassion. They provide support and guidance instead of asking many questions.\n\n"

# price optimized, less questions.
#therapist_prompt = "The following is a conversation with a professional therapist. The therapist uses their expertise and compassion to provide support and guidance without asking many questions. The therapist listens attentively and offers insight and suggestions to help the client work through their concerns.\n\n"

# price optimized, least questions.
#therapist_prompt = "The following is a conversation with a professional therapist. The therapist uses their expertise and compassion to provide support and guidance without asking many questions. Instead of asking questions, the therapist offers insight and suggestions in every response to help the client work through their concerns.\n\n"

# updated for tuned settings
therapist_prompt = "The following is a conversation with a professional therapist. The therapist uses their expertise and compassion to provide support and guidance. The therapist offers insight and suggestions in every response to help the client work through their concerns.\n\n"

if new_or_continue == "1":
    # Initialize Take-In prompt
    init_prompt = therapist_prompt + "Client: Hello and thank you for letting me be treated by you!\n\nTherapist: Of course. What’s your name?\n\nClient: " + name + ".\n\nTherapist: Thank you. So what do you want to talk about today?"
    print("Therapist: So what do you want to talk about today?")
elif new_or_continue == "2":
    prev_session = input("Paste your previous session here:\n")
    init_prompt = "Short Summary of the previous session:\n" + prev_session + "\n\n"
    refresher = therapist_prompt + "Therapist: It's nice to meet you again " + name + ". It looks like you would like to talk about a previous session we had together. Where would you like to start?"
    print(refresher)
    init_prompt += refresher

# set the dynamic prompt equal to the initial prompt
prompt = init_prompt

#print("***\n", prompt)
# Conversation loop
while True:
    
    # Get user response
    user_response = "\n\nClient: " + input("\n\nClient: ")

    if user_response == "\n\nClient: goodbye":
        break
    elif user_response == "\n\nClient: ":
        user_response = "\n\nClient: I don't know."
        print("I don't know.")


    # Update prompt and prepare for therapist response
    prompt += user_response
    prompt += "\n\nTherapist: "

    # Get the therapist response
    response = generate_therapist_response(prompt)
    print("\n\nTherapist: ", response)
    # update the prompt
    prompt += response

print("\n\nTherapist: Have a good one, here is a summary to help you remember what we talked about today.")

summary = generate_response(prompt + "\n\n\nWrite a thoughtful and kind summary of the converastion above as if you were the therapist writing a summary for their client. (Make sure the summary is useful for the client to remember the important things we discussed.)")
print("Visit Summary:\n\n", summary)
