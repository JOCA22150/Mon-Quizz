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
    {"q": "Quelle est la capitale de l'Islande ?", "a": ["Oslo", "Reykjavik", "Helsinki"], "c": "Reykjavik"},
    {"q": "Combien de coeurs a une pieuvre ?", "a": ["1", "3", "8"], "c": "3"},
    {"q": "Quel est le métal le plus cher ?", "a": ["Or", "Platine", "Rhodium"], "c": "Rhodium"}
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
