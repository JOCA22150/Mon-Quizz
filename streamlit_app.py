import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="Quiz Flash", layout="centered")

# --- STYLE ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; height: 55px; border-radius: 12px; font-size: 18px; font-weight: bold; background-color: #f0f2f6; }
    .score-box { padding: 25px; background-color: #e8f0fe; border-radius: 20px; text-align: center; border: 2px solid #4285f4; }
    .points-display { font-size: 24px; color: #4285f4; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# Mémoire globale
if 'global_scores' not in st.session_state:
    st.session_state.global_scores = {}

# Variables par joueur
if 'question_index' not in st.session_state:
    st.session_state.question_index = 0
if 'total_points' not in st.session_state:
    st.session_state.total_points = 0
if 'pseudo' not in st.session_state:
    st.session_state.pseudo = ""
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()

# --- QUESTIONS ---
quiz_data = [
    {"q": "Qui a peint la Joconde ?", "a": ["Van Gogh", "Picasso", "Léonard de Vinci"], "c": "Léonard de Vinci"},
    {"q": "Quelle est la capitale de l'Islande ?", "a": ["Oslo", "Reykjavik", "Helsinki"], "c": "Reykjavik"},
    {"q": "Quel groupe chante 'Bohemian Rhapsody' ?", "a": ["The Beatles", "Queen", "U2"], "c": "Queen"}
]

st.title("⚡ Quiz Flash : Soyez Rapides !")

# 1. PSEUDO
if st.session_state.pseudo == "":
    st.write("### 👋 Prêt pour le défi ?")
    nom = st.text_input("Entre ton pseudo :")
    if st.button("Lancer le chrono !"):
        if nom:
            st.session_state.pseudo = nom
            st.session_state.start_time = time.time()
            st.rerun()
else:
    # 2. QUIZ
    if st.session_state.question_index < len(quiz_data):
        current_q = quiz_data[st.session_state.question_index]
        
        col1, col2 = st.columns()
        col1.write(f"Joueur : **{st.session_state.pseudo}**")
        col2.markdown(f"<p class='points-display'>✨ {st.session_state.total_points} pts</p>", unsafe_allow_html=True)
        
        st.progress(st.session_state.question_index / len(quiz_data))
        st.info(f"Question {st.session_state.question_index + 1} : {current_q['q']}")

        for option in current_q['a']:
            if st.button(option):
                # Calcul de la rapidité
                fin_chrono = time.time()
                temps_ecoule = fin_chrono - st.session_state.start_time
                
                if option == current_q['c']:
                    # On donne 100 points moins 5 points par seconde écoulée (minimum 10 pts)
                    bonus = max(10, 100 - int(temps_ecoule * 5))
                    st.session_state.total_points += bonus
                    st.toast(f"Correct ! +{bonus} pts", icon="✅")
                else:
                    st.toast("Faux ! 0 pts", icon="❌")
                
                st.session_state.question_index += 1
                st.session_state.start_time = time.time() # Reset chrono pour la suivante
                st.rerun()
    
    # 3. CLASSEMENT FINAL
    else:
        st.session_state.global_scores[st.session_state.pseudo] = st.session_state.total_points
        st.balloons()
        st.header("🏁 Classement Final")
        
        st.markdown(f"<div class='score-box'><h2>Total : {st.session_state.total_points} points</h2></div>", unsafe_allow_html=True)
        
        st.write("---")
        st.subheader("📊 Tableau des Médailles")
        if st.session_state.global_scores:
            df = pd.DataFrame(st.session_state.global_scores.items(), columns=['Joueur', 'Points'])
            df = df.sort_values(by='Points', ascending=False).reset_index(drop=True)
            # Ajout d'emojis pour le podium
            df.index = df.index + 1
            st.table(df)
        
        if st.button("🔄 Rejouer"):
            st.session_state.question_index = 0
            st.session_state.total_points = 0
            st.session_state.start_time = time.time()
            st.rerun()
