import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from the .env file
load_dotenv()

client = Groq(
    api_key=os.environ.get("VISION_API_KEY"),
)

st.title("🦙 Chat-Assistant (llama-3.3-70b)")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history first (like ChatGPT)
st.subheader("Chat History")
for chat in st.session_state.chat_history:
    with st.chat_message("user"):
        st.markdown(chat["user"])
    with st.chat_message("assistant"):
        st.markdown(chat["assistant"])

# Input at the bottom
user_input = st.chat_input("Ask me anything...")

# When user submits
if user_input:
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Construct full context for model
    messages = []
    for chat in st.session_state.chat_history:
        messages.append({"role": "user", "content": chat["user"]})
        messages.append({"role": "assistant", "content": chat["assistant"]})
    messages.append({"role": "user", "content": user_input})

    # Get response from Groq
    try:
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile",
        )
        response = chat_completion.choices[0].message.content
    except Exception as e:
        response = f"❌ Error: {e}"

    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(response)

    # Save interaction (limit to last 10)
    st.session_state.chat_history.append({"user": user_input, "assistant": response})
    st.session_state.chat_history = st.session_state.chat_history[-10:]






# import os
# import streamlit as st
# from dotenv import load_dotenv
# from groq import Groq

# # Load environment variables from the .env file
# load_dotenv()

# client = Groq(
#     api_key=os.environ.get("VISION_API_KEY"),
# )

# st.title("Chat-Assistant with llama-3.3-70b")

# # Initialize session state for chat history
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []

# # Function to get response from Groq API
# def get_response(user_input):
#     try:
#         # Include chat history in the prompt
#         messages = [{"role": "user", "content": msg["user"]} if i % 2 == 0 
#                     else {"role": "assistant", "content": msg["assistant"]}
#                     for i, msg in enumerate(st.session_state.chat_history)]
        
#         messages.append({"role": "user", "content": user_input})
        
#         chat_completion = client.chat.completions.create(
#             messages=messages,
#             model="llama-3.3-70b-versatile",
#         )
#         return chat_completion.choices[0].message.content
#     except Exception as e:
#         st.error(f"Error: {e}")
#         return "There was an error in getting the response."

# # Input and Button
# user_input = st.text_input("You: ", "")

# if st.button("Send"):
#     if user_input:
#         response = get_response(user_input)

#         # Add new interaction to chat history
#         st.session_state.chat_history.append({"user": user_input, "assistant": response})

#         # Limit to 10 messages
#         if len(st.session_state.chat_history) > 10:
#             st.session_state.chat_history = st.session_state.chat_history[-10:]
#     else:
#         st.warning("Please enter a message.")

# # Display the conversation
# if st.session_state.chat_history:
#     st.subheader("Chat History")
#     for i, chat in enumerate(st.session_state.chat_history):
#         st.markdown(f"**You:** {chat['user']}")
#         st.markdown(f"**Groq:** {chat['assistant']}")










# import os
# import streamlit as st
# from dotenv import load_dotenv
# from groq import Groq

# # Load environment variables from the .env file
# load_dotenv()

# client = Groq(
#     api_key=os.environ.get("VISION_API_KEY"),
# )

# st.title("Chat-Assistant with llama-3.3-70b")

# # Function to get the response from Groq API
# def get_response(user_input):
#     try:
#         chat_completion = client.chat.completions.create(
#             messages=[{"role": "user", "content": user_input}],
#             model="llama-3.3-70b-versatile",
#         )
#         return chat_completion.choices[0].message.content
#     except Exception as e:
#         st.error(f"Error: {e}")
#         return "There was an error in getting the response."

# user_input = st.text_input("You: ", "Explain the importance of fast language models")

# if st.button("Send"):
#     if user_input:
#         response = get_response(user_input)
#         st.write(f"Groq: {response}")
#     else:
#         st.write("Please enter a message.")









# import os
# import streamlit as st
# from dotenv import load_dotenv
# from groq import Groq

# # Load environment variables from the .env file
# load_dotenv()

# client = Groq(
#     api_key=os.environ.get("VISION_API_KEY"),
# )

# st.title("Chat with llama-3.3-70b")

# # Function to get the response from Groq API
# def get_response(user_input):
#     chat_completion = client.chat.completions.create(
#         messages=[
#             {
#                 "role": "user",
#                 "content": user_input,
#             }
#         ],
#         model="llama-3.3-70b-versatile",
#     )
#     return chat_completion.choices[0].message.content

# user_input = st.text_input("You: ", "Explain the importance of fast language models")

# if st.button("Send"):
#     response = get_response(user_input)
#     st.write(f"Groq: {response}")
