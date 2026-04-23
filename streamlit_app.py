import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="Le Quiz de la Soirée", layout="centered")

# --- LE CERVEAU COMMUN (PARTAGÉ) ---
@st.cache_resource
def get_leaderboard():
    return {} # Un dictionnaire partagé entre tous les joueurs

leaderboard = get_leaderboard()

# --- STYLE ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; height: 55px; border-radius: 12px; font-weight: bold; }
    .points-display { font-size: 24px; color: #4285f4; font-weight: bold; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# Variables individuelles
if 'question_index' not in st.session_state:
    st.session_state.question_index = 0
if 'total_points' not in st.session_state:
    st.session_state.total_points = 0
if 'pseudo' not in st.session_state:
    st.session_state.pseudo = ""
if 'timer' not in st.session_state:
    st.session_state.timer = time.time()

# --- QUESTIONS ---
quiz_data = [
    {"q": "Quel pays a offert la Statue de la Liberté aux USA ?", "a": ["France", "Angleterre", "Allemagne"], "c": "France"},
    {"q": "Quelle est la capitale du Portugal ?", "a": ["Madrid", "Lisbonne", "Porto"], "c": "Lisbonne"},
    {"q": "Quel film a pour héros un petit poisson clown ?", "a": ["Le Monde de Nemo", "Gang de Requins", "La Petite Sirène"], "c": "Le Monde de Nemo"},
    {"q": "Combien de pattes ont les araignées ?", "a": ["6 pattes", "8 pattes", "10 pattes"], "c": "8 pattes"},
    {"q": "Qui est l'auteur de Harry Potter ?", "a": ["J.R.R. Tolkien", "J.K. Rowling", "George R.R. Martin"], "c": "J.K. Rowling"},
    {"q": "Quel est le plus grand océan du monde ?", "a": ["Atlantique", "Indien", "Pacifique"], "c": "Pacifique"},
    {"q": "Quelle est la couleur du cheval blanc d'Henri IV ?", "a": ["Noir", "Blanc", "Gris"], "c": "Blanc"},
    {"q": "Dans quel sport utilise-t-on un 'palet' ?", "a": ["Rugby", "Hockey sur glace", "Golf"], "c": "Hockey sur glace"},
    {"q": "Quelle est la monnaie utilisée au Japon ?", "a": ["Le Yuan", "Le Won", "Le Yen"], "c": "Le Yen"},
    {"q": "Comment s'appelle le cri du cochon ?", "a": ["Il grogne", "Il glousse", "Il braie"], "c": "Il grogne"},
    {"q": "Quel est l'organe qui permet de respirer ?", "a": ["Le Foie", "Les Poumons", "L'Estomac"], "c": "Les Poumons"},
    {"q": "Quelle planète est la plus proche du Soleil ?", "a": ["Mercure", "Vénus", "Mars"], "c": "Mercure"},
    {"q": "Quel super-héros porte un costume de chauve-souris ?", "a": ["Superman", "Spider-Man", "Batman"], "c": "Batman"},
    {"q": "Quelle est la langue la plus parlée au Brésil ?", "a": ["Espagnol", "Portugais", "Anglais"], "c": "Portugais"},
    {"q": "En quelle année a eu lieu la chute du mur de Berlin ?", "a": ["1985", "1989", "1991"], "c": "1989"}
]

st.title("⚡ Quiz Challenge")

if st.session_state.pseudo == "":
    nom = st.text_input("Ton pseudo :")
    if st.button("Démarrer !"):
        if nom:
            st.session_state.pseudo = nom
            st.session_state.timer = time.time()
            st.rerun()
else:
    if st.session_state.question_index < len(quiz_data):
        current_q = quiz_data[st.session_state.question_index]
        
        c1, c2 = st.columns(2)
        c1.write(f"Joueur : **{st.session_state.pseudo}**")
        c2.markdown(f"<p class='points-display'>✨ {st.session_state.total_points} pts</p>", unsafe_allow_html=True)
        
        st.info(f"Question {st.session_state.question_index + 1} : {current_q['q']}")

        for option in current_q['a']:
            if st.button(option):
                temps_pris = time.time() - st.session_state.timer
                if option == current_q['c']:
                    gain = max(10, 100 - int(temps_pris * 5))
                    st.session_state.total_points += gain
                
                st.session_state.question_index += 1
                st.session_state.timer = time.time()
                st.rerun()
    else:
        # ON ENREGISTRE DANS LE TABLEAU COMMUN
        leaderboard[st.session_state.pseudo] = st.session_state.total_points
        
        st.balloons()
        st.header("🏁 Classement Général")
        
        # Création du tableau avec les scores de TOUT LE MONDE
        df = pd.DataFrame(list(leaderboard.items()), columns=['Joueur', 'Points'])
        df = df.sort_values(by='Points', ascending=False)
        st.table(df)
        
        st.write("👉 *Si un score manque, cliquez sur le bouton ci-dessous :*")
        if st.button("Rafraîchir le classement 🔄"):
            st.rerun()
