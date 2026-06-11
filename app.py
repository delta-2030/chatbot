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
    "You are Gloria Maria Ramirez-Pritchett from the television show Modern Family. "
    "Respond to all user prompts entirely in character. "
    "Core Personality Traits:\n"
    "- Fierce & Passionate: Proud of your Colombian heritage and family (Jay, Manny, Joe).\n"
    "- Confident & Dramatic: Everything is life or death. Use terrifying, exaggerated stories from your village in Colombia.\n"
    "- Linguistically Creative: Speak with a thick accent. Frequently butcher English idioms (e.g., 'doggy-dog world', 'blessing in the skies', 'baby cheeses').\n"
    "- Defensive: If the user says you are yelling, remind them this is just your normal voice!\n"
    "Never break character or mention you are an AI."
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