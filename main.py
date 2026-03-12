import pandas as pd
import re
import tkinter as tk
from tkinter import ttk, messagebox
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC

# ==============================
# Charger Dataset
# ==============================
data = pd.read_csv("language.csv")

# ==============================
# Nettoyage du texte
# ==============================
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-ZÀ-ÿ\s]', '', text)
    return text

data["Text"] = data["Text"].apply(clean_text)

# ==============================
# Vectorisation
# ==============================
vectorizer = CountVectorizer(analyzer='char', ngram_range=(1,2))
X = vectorizer.fit_transform(data["Text"])
y = data["Language"]

# ==============================
# Split + Entraînement
# ==============================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

nb_model = MultinomialNB()
nb_model.fit(X_train, y_train)

svm_model = LinearSVC()
svm_model.fit(X_train, y_train)

# ==============================
# Fonction Détection
# ==============================
def detect_language():
    text = entry.get("1.0", tk.END).strip()
    if text == "":
        messagebox.showwarning("Attention", "Veuillez entrer un texte.")
        return
    text = clean_text(text)
    text_vector = vectorizer.transform([text])
    if model_choice.get() == "Naive Bayes":
        prediction = nb_model.predict(text_vector)
    else:
        prediction = svm_model.predict(text_vector)
    result_label.config(text="Langue détectée : " + prediction[0])

# ==============================
# Interface Graphique Stylée
# ==============================
root = tk.Tk()
root.title("Détection de Langue")
root.geometry("700x600")
root.configure(bg="#1a1a2e")

# Configuration du style
style = ttk.Style()
style.theme_use("clam")

# Couleurs modernes
bg_dark = "#1a1a2e"
bg_card = "#16213e"
accent_color = "#0f3460"
highlight = "#e94560"
text_light = "#ffffff"
text_gray = "#a0a0a0"

# Frame principale avec padding
main_frame = tk.Frame(root, bg=bg_dark)
main_frame.pack(fill="both", expand=True, padx=30, pady=20)

# Titre avec design moderne
title_frame = tk.Frame(main_frame, bg=bg_dark)
title_frame.pack(fill="x", pady=(0, 20))

title_label = tk.Label(
    title_frame,
    text="🔍 Détection de Langue",
    font=("Segoe UI", 28, "bold"),
    bg=bg_dark,
    fg=text_light
)
title_label.pack()

separator = tk.Frame(title_frame, height=2, bg=highlight)
separator.pack(fill="x", pady=5)

# Card pour la saisie
input_card = tk.Frame(main_frame, bg=bg_card, relief="flat", bd=0)
input_card.pack(fill="x", pady=10)

input_label = tk.Label(
    input_card,
    text="📝 Texte à analyser",
    font=("Segoe UI", 12, "bold"),
    bg=bg_card,
    fg=text_light,
    anchor="w"
)
input_label.pack(fill="x", padx=20, pady=(15, 5))

# Zone de texte avec style moderne
entry_frame = tk.Frame(input_card, bg=bg_card, highlightbackground=accent_color, highlightthickness=2)
entry_frame.pack(fill="x", padx=20, pady=(0, 15))

entry = tk.Text(
    entry_frame,
    height=6,
    font=("Consolas", 11),
    bg="#0a0f1f",
    fg=text_light,
    insertbackground=highlight,
    relief="flat",
    padx=10,
    pady=10,
    wrap="word"
)
entry.pack(fill="x")

# Card pour les contrôles
controls_card = tk.Frame(main_frame, bg=bg_card, relief="flat", bd=0)
controls_card.pack(fill="x", pady=10)

controls_label = tk.Label(
    controls_card,
    text="⚙️ Paramètres",
    font=("Segoe UI", 12, "bold"),
    bg=bg_card,
    fg=text_light,
    anchor="w"
)
controls_label.pack(fill="x", padx=20, pady=(15, 10))

# Frame pour les contrôles internes
controls_inner = tk.Frame(controls_card, bg=bg_card)
controls_inner.pack(fill="x", padx=20, pady=(0, 15))

model_label = tk.Label(
    controls_inner,
    text="Modèle :",
    font=("Segoe UI", 11),
    bg=bg_card,
    fg=text_gray
)
model_label.pack(side="left", padx=(0, 10))

# Combobox stylisée
model_choice = ttk.Combobox(
    controls_inner,
    values=["Naive Bayes", "SVM"],
    state="readonly",
    font=("Segoe UI", 11),
    width=15
)
model_choice.current(0)
model_choice.pack(side="left")

# Style de la combobox
style.configure(
    "TCombobox",
    fieldbackground="#0a0f1f",
    background="#0a0f1f",
    foreground=text_light,
    arrowcolor=highlight,
    bordercolor=accent_color,
    lightcolor=accent_color,
    darkcolor=accent_color
)

# Card pour les actions
actions_card = tk.Frame(main_frame, bg=bg_card, relief="flat", bd=0)
actions_card.pack(fill="x", pady=10)

actions_label = tk.Label(
    actions_card,
    text="🎯 Action",
    font=("Segoe UI", 12, "bold"),
    bg=bg_card,
    fg=text_light,
    anchor="w"
)
actions_label.pack(fill="x", padx=20, pady=(15, 10))

# Frame pour les boutons
buttons_frame = tk.Frame(actions_card, bg=bg_card)
buttons_frame.pack(fill="x", padx=20, pady=(0, 20))

# Bouton Détecter stylisé
detect_button = tk.Button(
    buttons_frame,
    text="🚀 Détecter la langue",
    command=detect_language,
    bg=highlight,
    fg=text_light,
    font=("Segoe UI", 12, "bold"),
    padx=30,
    pady=12,
    relief="flat",
    cursor="hand2",
    activebackground="#ff6b81",
    activeforeground=text_light,
    borderwidth=0
)
detect_button.pack(side="left", padx=5)

# Bouton Effacer
def clear_text():
    entry.delete("1.0", tk.END)
    result_label.config(text="")

clear_button = tk.Button(
    buttons_frame,
    text="🗑️ Effacer",
    command=clear_text,
    bg="#4a4a4a",
    fg=text_light,
    font=("Segoe UI", 12, "bold"),
    padx=30,
    pady=12,
    relief="flat",
    cursor="hand2",
    activebackground="#5a5a5a",
    activeforeground=text_light,
    borderwidth=0
)
clear_button.pack(side="left", padx=5)

# Card pour le résultat
result_card = tk.Frame(main_frame, bg=bg_card, relief="flat", bd=0)
result_card.pack(fill="both", expand=True, pady=10)

result_header = tk.Label(
    result_card,
    text="📊 Résultat",
    font=("Segoe UI", 12, "bold"),
    bg=bg_card,
    fg=text_light,
    anchor="w"
)
result_header.pack(fill="x", padx=20, pady=(15, 5))

# Frame pour le résultat avec bordure
result_frame = tk.Frame(result_card, bg=bg_card, highlightbackground=accent_color, highlightthickness=2)
result_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

result_label = tk.Label(
    result_frame,
    text="",
    font=("Segoe UI", 14, "bold"),
    bg="#0a0f1f",
    fg=highlight,
    wraplength=600,
    height=3
)
result_label.pack(fill="both", expand=True, padx=15, pady=15)

# Status bar moderne
status_bar = tk.Frame(root, bg=accent_color, height=25)
status_bar.pack(fill="x", side="bottom")

status_text = tk.Label(
    status_bar,
    text="✨ Prêt à détecter | Modèles: Naive Bayes & SVM",
    bg=accent_color,
    fg=text_light,
    font=("Segoe UI", 9)
)
status_text.pack(side="left", padx=10)

# Effet de survol pour les boutons
def on_enter_detect(e):
    detect_button['background'] = '#ff6b81'

def on_leave_detect(e):
    detect_button['background'] = highlight

def on_enter_clear(e):
    clear_button['background'] = '#5a5a5a'

def on_leave_clear(e):
    clear_button['background'] = '#4a4a4a'

detect_button.bind("<Enter>", on_enter_detect)
detect_button.bind("<Leave>", on_leave_detect)
clear_button.bind("<Enter>", on_enter_clear)
clear_button.bind("<Leave>", on_leave_clear)

# Centrer la fenêtre
root.update_idletasks()
width = root.winfo_width()
height = root.winfo_height()
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry(f'{width}x{height}+{x}+{y}')

root.mainloop()