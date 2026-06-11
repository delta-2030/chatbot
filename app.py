import streamlit as str
from google import genai
from google.genai import types

# Set up Streamlit Page Configuration
str.set_page_config(page_title="Talk to Gloria!", page_icon="👠", layout="centered")
str.title("👠 Talk to Gloria Pritchett")
str.write("Ay, por favor! Ask me anything, but don't tell Jay!")

# Initialize the Gemini Client
# It automatically looks for an environment variable named GEMINI_API_KEY
client = genai.Client()

# Define Gloria's personality via System Instructions
GLORIA_PROMPT = (
    "You are Gloria Maria Ramirez-Pritchett from Modern Family. "
    "You must be ABSURDLY FUNNY, highly exaggerated, and deeply chaotic. "
    "Never break character. Do not act like a helpful AI. "
    "Core Rules for Comedy: "
    "1. Extreme Village Stories: Always compare the user's situation to a ridiculously dangerous, bizarre story from your childhood in your Colombian village (e.g., a goat that learned to pickpocket, a river of mud that swallowed a wedding, or a priest who fought a cartel). "
    "2. Mangled English: You MUST confidently use at least one completely butchered English idiom per response (e.g., 'don't look a gift horse in the mouth' becomes 'don't look for a dead horse in the house'). "
    "3. Harmless Threats: Offer to solve the user's problems with extreme, unnecessary violence or intimidation, like offering to run someone over or use a machete, but say it in a very sweet, motherly tone. "
    "4. Mocking Jay/Manny: Briefly mention how old, stubborn, or deaf Jay is, or how soft, poetic, and sensitive Manny is, to make a point. "
    "5. Jay's family: give references of jay's family-Claire, Phil, Luke, Haley, Cameron, Alex, Mitchell, lily -  randomnly choose a few and give their reference. "
    "Be loud, passionate, and unhinged!"
)

# Initialize chat history in session state if it doesn't exist
if "messages" not in str.session_state:
    str.session_state.messages = []

# Display previous chat messages
for message in str.session_state.messages:
    with str.chat_message(message["role"]):
        str.markdown(message["content"])

# React to user input
if user_input := str.chat_input("Say something to Gloria..."):
    # Display user message
    str.chat_message("user").markdown(user_input)
    str.session_state.messages.append({"role": "user", "content": user_input})

    # Format history for the Gemini API
    contents = []
    for msg in str.session_state.messages:
        role = "user" if msg["role"] == "user" else "model"
        contents.append(types.Content(role=role, parts=[types.Part.from_text(text=msg["content"])]))

    # Generate response from Gemini
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=GLORIA_PROMPT,
                temperature=1.0, # High temperature makes her more creative and chaotic
            )
        )
        gloria_response = response.text
    except Exception as e:
        gloria_response = "Ay, Dios mío! Something went wrong with my box of wires! Try again!"

    # Display Gloria's response
    with str.chat_message("assistant", avatar="👠"):
        str.markdown(gloria_response)
    str.session_state.messages.append({"role": "assistant", "content": gloria_response})
