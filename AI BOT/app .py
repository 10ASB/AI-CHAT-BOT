import tkinter as tk
from tkinter import scrolledtext
import random
from datetime import datetime

# ---------------- DATA ---------------- #

jokes = [
    "I have a lot of jokes about unemployed people.None of them work.",
    "Why was the computer cold? bcz It's dead.",
    "Why do programmers prefer dark mode? Because light attracts bugs!",
    "My wallet is like an onion. Opening it makes me cry.",
    "I'm not lazy. I'm on energy-saving mode."
]

fun_facts = [
    "Honey never spoils.",
    "Octopuses have three hearts.",
    "Bananas are berries.",
    "A day on Venus is longer than a year on Venus.",
    "Octopuses have three hearts.",
    "Your skeleton is always wet.",
    "One day you'll hear your favorite song for the last time and won't know it.",
    "Most people have already met someone who will attend their funeral ⚰️"
]

greetings = [
    "Hello there!",
    "Hi, nice to meet you!",
    "Hey! How are you?"
]

help_responses = [
    "I can tell jokes, facts, date, time and solve calculations.",
    "Try typing: joke, fact, date, time, calc 5+6",
    "I'm here to assist you."
]

chat_history = []

# ---------------- BOT LOGIC ---------------- #

def get_response(user_input):

    text = user_input.lower()

    if any(word in text for word in ["hi", "hello", "hey","oi","hlo"]):
        return random.choice(greetings)

    elif any(word in text for word in ["help", "support", "assist","wtf"]):
        return random.choice(help_responses)

    elif any(word in text for word in ["joke", "funny", "laugh"]):
        return random.choice(jokes)

    elif any(word in text for word in ["fact", "knowledge","jk"]):
        return random.choice(fun_facts)
    
    elif "ur name" in text:
        return "My name is Chatty AI."
    
    elif "your name" in text:
        return "My name is Chatty AI."

    elif "time" in text:
        return datetime.now().strftime("Current Time: %H:%M:%S")

    elif "date" in text:
        return datetime.now().strftime("Today's Date: %d-%m-%Y")

    elif text.startswith("calc"):
        try:
            expression = text.replace("calc", "").strip()
            allowed = "0123456789+-*/ "

            if all(char in allowed for char in expression):
                result = eval(expression)
                return f"The answer is {result} 🧮"
            else:
                return "Only numbers and + - * / are allowed 🚫"

        except ZeroDivisionError:
            return "Nice try 😏, you can't divide by zero."

        except:
            return "Invalid calculation 🤔"
    
    elif "history" in text:
        return "\n".join(chat_history[-5:])

    else:
        return "Sorry, I don't understand."

# ---------------- SEND MESSAGE ---------------- #

def send_message():

    user_text = entry.get()

    if user_text.strip() == "":
        return

    chat_window.insert(tk.END, f"You: {user_text}\n")

    chat_history.append("You: " + user_text)

    if user_text.lower() in ["bye", "exit", "quit"]:
        chat_window.insert(tk.END, "Bot: Goodbye!\n")
        root.after(1000, root.destroy)
        return

    response = get_response(user_text)

    chat_window.insert(tk.END, f"Bot: {response}\n\n")

    chat_history.append("Bot: " + response)

    entry.delete(0, tk.END)

# ---------------- GUI ---------------- #

root = tk.Tk()
root.title("🤖 Chatty AI")
root.geometry("900x700")
root.configure(bg="#0f172a")

# Header
header = tk.Frame(root, bg="#1e293b", height=80)
header.pack(fill="x")

title = tk.Label(
    header,
    text="🤖 Chatty AI",
    font=("Segoe UI", 22, "bold"),
    fg="white",
    bg="#1e293b"
)
title.pack(pady=20)

# Chat Area
chat_window = scrolledtext.ScrolledText(
    root,
    wrap=tk.WORD,
    font=("Segoe UI", 12),
    bg="#111827",
    fg="white",
    insertbackground="white",
    relief="flat"
)

chat_window.pack(
    padx=20,
    pady=20,
    fill="both",
    expand=True
)

# Bottom Bar
bottom = tk.Frame(root, bg="#0f172a")
bottom.pack(fill="x", padx=20, pady=10)

entry = tk.Entry(
    bottom,
    font=("Segoe UI", 12),
    bg="white",
    fg="black",
    relief="flat"
)

entry.pack(
    side="left",
    fill="x",
    expand=True,
    ipady=10
)

send_btn = tk.Button(
    bottom,
    text="Send",
    bg="#06b6d4",
    fg="white",
    font=("Segoe UI", 11, "bold"),
    relief="flat",
    command=send_message,
    cursor="hand2"
)

send_btn.pack(
    side="right",
    padx=10,
    ipadx=15,
    ipady=8
)
root.bind('<Return>', lambda event: send_message())

chat_window.insert(
    tk.END,
    "🤖 Welcome! Type help to see available commands.\n\n"
)

root.mainloop()