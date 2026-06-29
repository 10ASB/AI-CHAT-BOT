import tkinter as tk
from tkinter import scrolledtext
import random
from datetime import datetime
import re

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

API_KEY = "YOUR_OPENWEATHERMAP_API_KEY_HERE"

flirting_lines = [

"Are you a shadow? 🌑 Because I want to get lost in your darkness... 🖤",

"You must be made of dark matter... 🪐 because you pull me in with a force I can't resist. 😏",

"If you were a virus ☣️, I'd let you infect every part of me. 🖤",

"Are you midnight? 🌙 Because everything feels better when you're around. ✨",

"You don't need to hack me... 💻 my firewalls already came down the moment I saw you. ❤️‍🔥",

"Are you a black hole? 🕳️ Because I'm falling into you with no escape. 💫",

"Your voice is like velvet darkness... 🎶 I could drown in it. 🖤",

"I don't need light ✨ if you're the one guiding me through the shadows. 🌌",

"You must be forbidden code... ⚠️ because the more I look at you, the more I want to break all the rules. 😈",

"Are you a ghost in the machine? 👻 Because you've been haunting my thoughts all night. 🌙",

"I'd let you corrupt my data... 💾 as long as you're the one doing it. 🔥",

"You're not just my type... 😏 you're my favorite kind of danger. 🖤",

"In a world full of noise 🌍, you are my favorite silence. 🤫",

"They say the devil wears Prada... 😈 but you wear darkness better. 🖤",

"Careful... ⚠️ if you keep looking at me like that, I might let you ruin me completely. 🥀",

"ur hand looks heavy 🤝 cause, can i holding it for u!? 😊",

"r u a magician? 🎩 cause whenever I look at u, everyone else disappears! ✨",

"Are you a camera? 📸 cause every time I look at u, I smile! 😊",

"r u a MCD burger ? 🍔, bcz i am loving it! ❤️",

"r u my mom's chappal? 🩴, cauese ur hitting me so hard soniya! 😂",

"is ur father a terrorist? 💣 bomb banaya hai uncle ne! 😉",

"i would love to take u to movie 🎬, but they won't let's us bring our own snack! 🍿😋",

"r u google? 🔍 ...bcz u have everything i'm searching for! ❤️",

"r u my dad's chappal? 🩴, cauese ur hitting me so hard soniya! 🤣",

"bro!! tie your shoes 👟 i don't want u falling for anybody else 😏"

]   

# Local fallback jokes
jokes = [
    "Why don't programmers prefer dark mode? Because light attracts bugs! 😂",

    "Why did the scarecrow win an award? He was outstanding in his field!",

    "I'm reading a book on anti-gravity. It's impossible to put down.",

     "I have a lot of jokes about unemployed people.None of them work.",

    "Why was the computer cold? bcz It's dead.",

    "Why do programmers prefer dark mode? Because light attracts bugs!",

    "My wallet is like an onion. Opening it makes me cry.",

    "I'm not lazy. I'm on energy-saving mode."
]

last_local_joke = ""
last_flirt = ""

fun_facts = [
    "Octopuses have three hearts!",

    "Honey never spoils.",

    "A flock of flamingos is called a flamboyance.",

    "Honey never spoils.",

    "Bananas are berries.",

    "A day on Venus is longer than a year on Venus.",

    "Your skeleton is always wet.",

    "One day you'll hear your favorite song for the last time and won't know it.",

    "Most people have already met someone who will attend their funeral ⚰️",

    "we never saw dinosaurs and humans together, but we have seen dinosaurs and birds together 🦖🦅",
]

greetings = ["Hi there!", "Hello!", "Hey! How can I help you today?","BYE","hlo","hii","hiii","ha bol BSDK","wha agaya","bye"]

knowledge_base = {
    "hello": "Hey there! 👋",
    "how are you": "I'm doing great, thanks for asking!",
    # Magic happens here! %I is 12-hour format, %p is AM/PM
    "time": lambda: f"The current time is {datetime.now().strftime('%I:%M %p')}",
    "date": lambda: f"Today's date is {datetime.now().strftime('%B %d, %Y')}"
}

def get_joke():
    global last_local_joke
    if REQUESTS_AVAILABLE:
        try:
            # Fetch unlimited fresh jokes from the web
            res = requests.get("https://official-joke-api.appspot.com/random_joke", timeout=2)
            if res.status_code == 200:
                data = res.json()
                return f"{data['setup']}\n... {data['punchline']} 😂"
        except:
            pass # Fall back to local list if offline
            
    # Smart local fallback prevents immediate repetition
    available_jokes = [j for j in jokes if j != last_local_joke]
    if not available_jokes:
        available_jokes = jokes
        
    chosen_joke = random.choice(available_jokes)
    last_local_joke = chosen_joke
    return chosen_joke

def get_weather(city):
    if not REQUESTS_AVAILABLE:
        return "⚠️ 'requests' module missing.\nRun: pip install requests"
    if API_KEY == "YOUR_OPENWEATHERMAP_API_KEY_HERE":
        return "⚠️ Add your OpenWeatherMap API key!"

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": API_KEY, "units": "metric"}

    try:
        response = requests.get(url, params=params, timeout=8)
        if response.status_code == 200:
            data = response.json()
            return f"🌤️ {data['name']}: {data['main']['temp']}°C, {data['weather'][0]['description'].capitalize()}"
        return f"❌ City '{city}' not found."
    except Exception as e:
        return f"🌐 Connection error: {str(e)}"

def get_response(user_input):
    user_input = user_input.lower().strip()
    if any(greet in user_input for greet in ["hi", "hello", "hey","Hi there!", "Hello!", "Hey! How can I help you today?","BYE","hlo","hii","hiii","oi","yo","sup","wassup","greetings","good morning","good afternoon","good evening","good night","bye","see you","later","cya","what ra","bsdk", "namaste","salaam"]):
        return random.choice(greetings)
    weather_match = re.search(r'weather (?:in )?(.+)', user_input)

    if any(word in user_input for word in ["flirt", "rizz", "pick up line","1 more"]):
        return random.choice(flirting_lines)

    if weather_match:
        return get_weather(weather_match.group(1).strip())
    
    if any(word in user_input for word in ["joke", "funny","lol","1 more"]):
        return get_joke()
    
    if "fact" in user_input:
        return random.choice(fun_facts)
    
    for key, response in knowledge_base.items():
        if key in user_input:
            return response() if callable(response) else response
    return "Interesting! Tell me more. 🤖"

def send_message(event=None):
    user_input = user_entry.get().strip()
    if not user_input:
        return

    chat_window.config(state=tk.NORMAL)
    chat_window.insert(tk.END, f" You: {user_input} \n", "user")
    
    user_entry.delete(0, tk.END)
    response = get_response(user_input)
    
    chat_window.insert(tk.END, f" AI: {response} \n", "bot")
    chat_window.config(state=tk.DISABLED)
    chat_window.see(tk.END)

def use_suggestion(text):
    user_entry.delete(0, tk.END)
    user_entry.insert(0, text)
    send_message()

def on_enter(e):
    send_btn['background'] = '#38bdf8'

def on_leave(e):
    send_btn['background'] = '#0ea5e9'

# Main UI Setup
root = tk.Tk()
root.title("Chatty AI - Pro Desktop")
root.geometry("800x700")
root.configure(bg="#020617")

# Chat History Area
chat_window = scrolledtext.ScrolledText(
    root, wrap=tk.WORD, state=tk.DISABLED, 
    bg="#0f172a", fg="#f8fafc", 
    font=("Segoe UI", 12), borderwidth=0, highlightthickness=0
)
chat_window.pack(padx=24, pady=(24, 10), fill=tk.BOTH, expand=True)

# Custom Tags
chat_window.tag_configure("user", foreground="#ffffff", background="#0ea5e9", font=("Segoe UI", 12, "bold"), spacing1=12, spacing3=12, lmargin1=150, lmargin2=150, rmargin=20, justify="right")
chat_window.tag_configure("bot", foreground="#f8fafc", background="#1e293b", font=("Segoe UI", 12), spacing1=12, spacing3=12, lmargin1=20, lmargin2=20, rmargin=150)

# Floating Suggestions
suggestions_frame = tk.Frame(root, bg="#020617")
suggestions_frame.pack(padx=24, pady=(0, 10), fill=tk.X)

suggestions = ["Tell me a joke", "Fun fact", "Time", "Weather at loc", "Flirt with me", "Date", "Bye","Hello" ]

for text in suggestions:
    btn = tk.Button(
        suggestions_frame, text=text, 
        bg="#1e293b", fg="#94a3b8", font=("Segoe UI", 10), 
        borderwidth=0, activebackground="#38bdf8", activeforeground="white", cursor="hand2",
        command=lambda t=text: use_suggestion(t)
    )
    btn.pack(side=tk.LEFT, padx=(0, 8), ipadx=12, ipady=6)
    
    btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#334155", fg="#f8fafc"))
    btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#1e293b", fg="#94a3b8"))

# Input Area
input_frame = tk.Frame(root, bg="#020617")
input_frame.pack(padx=24, pady=(0, 24), fill=tk.X)

user_entry = tk.Entry(
    input_frame, font=("Segoe UI", 13), 
    bg="#1e293b", fg="#f8fafc", 
    insertbackground="#38bdf8", borderwidth=0, highlightthickness=1, highlightcolor="#38bdf8"
)
user_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=14, padx=(0, 16))
user_entry.bind("<Return>", send_message)

send_btn = tk.Button(
    input_frame, text="SEND 🚀", command=send_message, 
    bg="#0ea5e9", fg="white", font=("Segoe UI", 12, "bold"), 
    borderwidth=0, activebackground="#38bdf8", activeforeground="white", cursor="hand2"
)
send_btn.pack(side=tk.RIGHT, ipadx=24, ipady=10)

send_btn.bind("<Enter>", on_enter)
send_btn.bind("<Leave>", on_leave)

# Startup Message
chat_window.config(state=tk.NORMAL)
chat_window.insert(tk.END, " ✨ AI: Wanacum. How can I assist? \n", "bot")
chat_window.config(state=tk.DISABLED)

root.mainloop()
