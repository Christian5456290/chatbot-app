import random 
import requests
import nltk
from nltk.tokenize import word_tokenize

def chatbot():                                 
    print("Chatbot: Hi! ...")   
    name = None
    last_intent = None 
    joke_triggers = ["joke", "funny", "make me laugh"]
    advice_triggers = ["advice", "suggestion", "tip", "what should i do"]
              
    
    while True:                                
        user_input = input("You: ").lower() 
        tokens = word_tokenize(user_input)
        #print("Tokens:", tokens)
        print("DEBUG last_intent:", last_intent)
        print("DEBUG name:", name)

        if any(word in tokens for word in ["bye", "goodbye", "see ya", "later"]):                 
            print("Chatbot: Goodbye! ...")
            break                              

        elif any(word in tokens for word in ["hello","hi","hey","sup","howdy"]):
            response = ["Hello there!", "Hi!", "Hey, nice to see you!", "Yo!"] 
            print("Chatbot:", random.choice(response))

        elif "name" in tokens and "what" in tokens and "my" in tokens:
            if name:
                print(f"Chatbot: You told me your name is {name}.")
            else:
                print("Chatbot: I don’t know your name yet!")

        elif "name" in tokens and "my" in tokens:
            if "is" in tokens:
                is_index = tokens.index("is")   # find where "is" occurs
                name_tokens = tokens[is_index + 1:]   # everything after "is"
                name = " ".join(name_tokens).title()  # join into a string, capitalize
                print(f"Chatbot: Nice to meet you, {name}!")
            else:
                print("Chatbot: I didn’t catch your name clearly.")

        elif "name" in tokens and "your" in tokens:
            print("Chatbot: I'm Chatty, your friendly bot.")

        elif "how are you" in user_input:       
            print("Chatbot: I'm just a bot...")

        elif "your name" in user_input:         
            print("Chatbot: I'm Chatty...")

        elif any(phrase in user_input for phrase in joke_triggers):
            response = requests.get("https://api.chucknorris.io/jokes/random")
            if response.status_code == 200:
                joke = response.json()["value"]
                print("Chatbot:", joke)
                last_intent = "joke"
            else:
                print("Chatbot: Sorry, I couldn’t fetch a joke right now.")
                
        elif any(word in tokens for word in ["another", "more", "again"]) and last_intent == "joke":
            response = requests.get("https://api.chucknorris.io/jokes/random")
            if response.status_code == 200:
                joke = response.json()["value"]
                print("Chatbot:", joke)
            else:
                print("Chatbot: Sorry, I couldn’t fetch a joke right now.")
                
        elif any(phrase in user_input for phrase in advice_triggers):
            response = requests.get("https://api.adviceslip.com/advice")
            if response.status_code == 200:
                advice = response.json()["slip"]["advice"]
                print("Chatbot:", advice)
                last_intent = "advice"
            else:
                print("Chatbot: Sorry, I couldn’t fetch advice right now.")

        elif any(word in tokens for word in ["another", "more", "again"]) and last_intent == "advice":
            response = requests.get("https://api.adviceslip.com/advice")
            if response.status_code == 200:
                advice = response.json()["slip"]["advice"]
                print("Chatbot:", advice)
            else:
                print("Chatbot: Sorry, I couldn’t fetch advice right now.")

        else:                                   
            print("Chatbot: Sorry, I don’t understand that yet.")

chatbot()                                     
