import random
import requests
import nltk
from nltk.tokenize import word_tokenize
import streamlit as st
from datetime import datetime
import time as systime 


# Download tokenizer data (only first run)
nltk.download('punkt')
nltk.download('punkt_tab')

def chatbot_response(user_input, name, last_intent):
    tokens = word_tokenize(user_input.lower())

    # Exit condition
    if any(word in tokens for word in ["bye", "goodbye", "later"]):
        return "Goodbye! Have a great day 😊", name, None

    # Greetings
    elif any(word in tokens for word in ["hello", "hi", "hey", "sup", "howdy"]):
        responses = ["Hello there!", "Hi!", "Hey, nice to see you!", "Yo!"]
        return random.choice(responses), name, last_intent

    # Multi-word greetings
    elif "long time no see" in user_input or "how ya been" in user_input:
        return "It's been a while! How are you?", name, last_intent

    # Asking about your name
    elif "name" in tokens and "what" in tokens and "my" in tokens:
        if name:
            return f"You told me your name is {name}.", name, last_intent
        else:
            return "I don’t ktime your name yet!", name, last_intent

    # Introduce yourself
    elif "name" in tokens and "my" in tokens:
        if "is" in tokens:
            is_index = tokens.index("is")
            name_tokens = tokens[is_index + 1:]
            name = " ".join(name_tokens).title()
            return f"Nice to meet you, {name}!", name, last_intent
        else:
            return "I didn’t catch your name clearly.", name, last_intent

    # Bot’s name
    elif "name" in tokens and "your" in tokens:
        return "I'm Chatty, your friendly bot.", name, last_intent

    # How are you
    elif "how are you" in user_input:
        return "I'm just a bot, but I'm doing great!", name, last_intent

    # Joke
    elif "joke" in tokens:
        response = requests.get("https://api.chucknorris.io/jokes/random")
        if response.status_code == 200:
            joke = response.json()["value"]
            return joke, name, "joke"
        else:
            return "Sorry, I couldn’t fetch a joke right time.", name, last_intent

    elif any(word in tokens for word in ["another", "more", "again"]) and last_intent == "joke":
        response = requests.get("https://api.chucknorris.io/jokes/random")
        if response.status_code == 200:
            joke = response.json()["value"]
            return joke, name, "joke"
        else:
            return "Sorry, I couldn’t fetch a joke right time.", name, last_intent

    # Advice
    elif "advice" in tokens:
        response = requests.get("https://api.adviceslip.com/advice")
        if response.status_code == 200:
            advice = response.json()["slip"]["advice"]
            return advice, name, "advice"
        else:
            return "Sorry, I couldn’t fetch advice right time.", name, last_intent

    elif any(word in tokens for word in ["another", "more", "again"]) and last_intent == "advice":
        response = requests.get("https://api.adviceslip.com/advice")
        if response.status_code == 200:
            advice = response.json()["slip"]["advice"]
            return advice, name, "advice"
        else:
            return "Sorry, I couldn’t fetch advice right time.", name, last_intent

    # Fallback
    else:
        return "Sorry, I don’t understand that yet.", name, last_intent


# --- Streamlit UI ---
st.title("💬 My Simple Chatbot")

# --- CSS for chat bubbles and typing animation ---
st.markdown("""
    <style>
    /* Default (light mode) */
    .user-msg {
        background-color: #DCF8C6;
        color: #000000;
        display: inline-block;
        max-width: 70%;
        padding: 6px 12px;
        border-radius: 23px;
        margin: 5px;
        text-align: right;
        float: right;
        clear: both;
        word-wrap: break-word;
    }
    .bot-msg {
        background-color: #EAEAEA;
        color: #000000;
        display: inline-block;
        max-width: 70%;
        padding: 6px 12px;
        border-radius: 23px;
        margin: 5px;
        text-align: left;
        float: left;
        clear: both;
        word-wrap: break-word;
    }

    /* Typing bubble */
    .typing-msg {
        background-color: #EAEAEA;
        color: #000000;
        display: inline-block;
        max-width: 70%;
        padding: 6px 12px;
        border-radius: 23px;
        margin: 5px;
        text-align: left;
        float: left;
        clear: both;
        word-wrap: break-word;
    }
    .typing-dot {
        display: inline-block;
        width: 6px;
        height: 6px;
        margin: 0 2px;
        background-color: #666;
        border-radius: 50%;
        animation: blink 1.4s infinite both;
    }
    .typing-dot:nth-child(2) {
        animation-delay: 0.2s;
    }
    .typing-dot:nth-child(3) {
        animation-delay: 0.4s;
    }
    @keyframes blink {
        0% { opacity: .2; }
        20% { opacity: 1; }
        100% { opacity: .2; }
    }

    /* Dark mode override */
    @media (prefers-color-scheme: dark) {
        .user-msg {
            background-color: #4CAF50;
            color: #ffffff;
        }
        .bot-msg {
            background-color: #333333;
            color: #ffffff;
        }
        .typing-msg {
            background-color: #444;
        }
        .typing-dot {
            background-color: #aaa;
        }
    }
    </style>
""", unsafe_allow_html=True)


# --- Initialize session state ---
if "history" not in st.session_state or not st.session_state.history:
    st.session_state.history = []
    now = datetime.now().strftime("%I:%M %p")
    st.session_state.history.append(("Chatbot", "Hi! I'm Chatty, your AI chatbot.", now))
    st.session_state.history.append(("Chatbot", "How can I help you today?", now))

if "name" not in st.session_state:
    st.session_state.name = None
if "last_intent" not in st.session_state:
    st.session_state.last_intent = None


# --- User input box ---
user_input = st.chat_input("Type your message")

# --- Handle new user input ---
if user_input:
    now = datetime.now().strftime("%I:%M %p")
    st.session_state.history.append(("You", user_input, now))
    st.session_state.history.append(("Chatbot", "⋯ typing", now))  # add typing as a normal message
    st.session_state.pending = user_input
    st.rerun()

# --- Display chat history ---
for i, (speaker, text, time) in enumerate(st.session_state.history):
    if text == "⋯ typing" and speaker == "Chatbot":
        st.session_state.typing_index = i
        st.markdown(
            f"""
            <div style='display:flex; justify-content:flex-start; align-items:flex-end; margin-bottom:10px;'>
                <img src='https://cdn-icons-png.flaticon.com/512/4712/4712109.png' 
                    style='width:30px; height:30px; border-radius:50%; margin-right:6px;'/>
                <div class='bot-msg'>
                    <span class='typing-dot'></span>
                    <span class='typing-dot'></span>
                    <span class='typing-dot'></span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
    )
    elif speaker == "You":
        # User bubble
        st.markdown(
            f"""
            <div style='display:flex; justify-content:flex-end; align-items:flex-end; margin-bottom:10px;'>
                <div class='user-msg'>
                    {text}
                    <div style='font-size:12px; color:#555; margin-top:2px;'>{time}</div>
                </div>
                <img src='https://cdn-icons-png.flaticon.com/512/1077/1077114.png' 
                     style='width:30px; height:30px; border-radius:50%; margin-left:6px;'/>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        # Bot bubble
        st.markdown(
            f"""
            <div style='display:flex; justify-content:flex-start; align-items:flex-end; margin-bottom:10px;'>
                <img src='https://cdn-icons-png.flaticon.com/512/4712/4712109.png' 
                     style='width:30px; height:30px; border-radius:50%; margin-right:6px;'/>
                <div class='bot-msg'>
                    {text}
                    <div style='font-size:12px; color:#555; margin-top:2px;'>{time}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# --- After rendering, replace typing with real response ---
if st.session_state.get("pending"):
    systime.sleep(1.5)  # show typing bubble visibly
    response, st.session_state.name, st.session_state.last_intent = chatbot_response(
        st.session_state.pending,
        st.session_state.name,
        st.session_state.last_intent
    )
    now = datetime.now().strftime("%I:%M %p")

    idx = st.session_state.typing_index
    st.session_state.history[idx] = ("Chatbot", response, now)

    st.session_state.pending = None
    st.rerun()

# --- Auto scroll ---
st.markdown("<div id='chat-end'></div>", unsafe_allow_html=True)
st.markdown("""
    <script>
    var chatEnd = document.getElementById('chat-end');
    if (chatEnd) {
        chatEnd.scrollIntoView({behavior: 'smooth'});
    }
    </script>
""", unsafe_allow_html=True)



