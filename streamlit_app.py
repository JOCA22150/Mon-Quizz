import streamlit as st
import pandas as pd
import time

# Config de la page
st.set_page_config(page_title="Quiz Flash", layout="centered")

# Design des boutons et du score
st.markdown("""
    <style>
    .stButton>button { width: 100%; height: 60px; border-radius: 12px; font-size: 18px; font-weight: bold; }
    .points-display { font-size: 26px; color: #4285f4; font-weight: bold; text-align: center; }
    .score-box { padding: 20px; background-color: #f0f2f6; border-radius: 15px; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# Initialisation
if 'global_scores' not in st.session_state:
    st.session_state.global_scores = {}
if 'question_index' not in st.session_state:
    st.session_state.question_index = 0
if 'total_points' not in st.session_state:
    st.session_state.total_points = 0
if 'pseudo' not in st.session_state:
    st.session_state.pseudo = ""
if 'timer' not in st.session_state:
    st.session_state.timer = time.time()

# --- TES QUESTIONS ---
quiz_data = [
    {"q": "Quelle est la capitale de l'Islande ?", "a": ["Oslo", "Reykjavik", "Helsinki"], "c": "Reykjavik"},
    {"q": "Combien de coeurs a une pieuvre ?", "a": ["1", "3", "8"], "c": "3"},
    {"q": "Quel est le métal le plus cher ?", "a": ["Or", "Platine", "Rhodium"], "c": "Rhodium"}
]

st.title("⚡ Quiz Flash")

if st.session_state.pseudo == "":
    st.write("### 👋 Entrez votre pseudo pour commencer :")
    nom = st.text_input("Pseudo")
    if st.button("Démarrer le chrono !"):
        if nom:
            st.session_state.pseudo = nom
            st.session_state.timer = time.time()
            st.rerun()
else:
    if st.session_state.question_index < len(quiz_data):
        current_q = quiz_data[st.session_state.question_index]
        
        # Affichage pseudo et points (Correction ici avec st.columns(2))
        c1, c2 = st.columns(2)
        c1.write(f"Joueur : **{st.session_state.pseudo}**")
        c2.markdown(f"<p class='points-display'>✨ {st.session_state.total_points} pts</p>", unsafe_allow_html=True)
        
        st.progress(st.session_state.question_index / len(quiz_data))
        st.info(f"Question {st.session_state.question_index + 1} : {current_q['q']}")

        for option in current_q['a']:
            if st.button(option):
                temps_pris = time.time() - st.session_state.timer
                if option == current_q['c']:
                    # Calcul des points : 100 de base - 5 points par seconde (mini 10)
                    gain = max(10, 100 - int(temps_pris * 5))
                    st.session_state.total_points += gain
                    st.toast(f"Bien joué ! +{gain} pts")
                else:
                    st.toast("Faux ! 0 pts")
                
                st.session_state.question_index += 1
                st.session_state.timer = time.time() # Relance le chrono
                st.rerun()
    else:
        # Enregistrement final
        st.session_state.global_scores[st.session_state.pseudo] = st.session_state.total_points
        st.balloons()
        st.header("🏁 Résultats")
        
        st.markdown(f"<div class='score-box'><h2>Total : {st.session_state.total_points} pts</h2></div>", unsafe_allow_html=True)
        
        st.write("---")
        st.subheader("📊 Tableau des scores (3 joueurs)")
        if st.session_state.global_scores:
            res = pd.DataFrame(st.session_state.global_scores.items(), columns=['Joueur', 'Points'])
            res = res.sort_values(by='Points', ascending=False)
            st.table(res)

        if st.button("Recommencer"):
            st.session_state.question_index = 0
            st.session_state.total_points = 0
            st.rerun()
