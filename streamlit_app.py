import streamlit as st
import pandas as pd

st.set_page_config(page_title="Le Quiz de la Bande", layout="centered")

# --- STYLE ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; height: 50px; border-radius: 10px; font-size: 18px; }
    .score-box { padding: 20px; background-color: #f0f2f6; border-radius: 15px; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# Initialisation du "Tableau des scores" global (partagé par tous les utilisateurs)
if 'global_scores' not in st.session_state:
    st.session_state.global_scores = {}

# Variables individuelles
if 'question_index' not in st.session_state:
    st.session_state.question_index = 0
if 'my_score' not in st.session_state:
    st.session_state.my_score = 0
if 'pseudo' not in st.session_state:
    st.session_state.pseudo = ""

# --- QUESTIONS ---
quiz_data = [
    {"q": "Quel pays a inventé les frites ?", "a": ["France", "Belgique", "USA"], "c": "Belgique"},
    {"q": "Quelle planète est surnommée la planète rouge ?", "a": ["Vénus", "Jupiter", "Mars"], "c": "Mars"},
    {"q": "Combien de cœurs possède une pieuvre ?", "a": ["1", "3", "8"], "c": "3"}
]

st.title("🥇 Compétition Quiz")

# 1. ÉTAPE PSEUDO
if st.session_state.pseudo == "":
    st.write("### Bienvenue ! Entrez votre nom pour commencer :")
    nom = st.text_input("Pseudo", placeholder="Ex: Jean-Mi, Ma Chérie...")
    if st.button("Valider et Jouer"):
        if nom:
            st.session_state.pseudo = nom
            st.rerun()
else:
    # 2. LE QUIZ
    if st.session_state.question_index < len(quiz_data):
        current_q = quiz_data[st.session_state.question_index]
        st.write(f"Joueur : **{st.session_state.pseudo}**")
        st.progress(st.session_state.question_index / len(quiz_data))
        
        st.info(f"Question {st.session_state.question_index + 1} : {current_q['q']}")

        for option in current_q['a']:
            if st.button(option):
                if option == current_q['c']:
                    st.toast("Correct !", icon="✅")
                    st.session_state.my_score += 1
                else:
                    st.toast("Faux...", icon="❌")
                
                st.session_state.question_index += 1
                st.rerun()

    # 3. LE RÉSULTAT FINAL ET CLASSEMENT
    else:
        # Enregistrement du score final dans la session globale
        st.session_state.global_scores[st.session_state.pseudo] = st.session_state.my_score
        
        st.balloons()
        st.header("🏁 Quiz Terminé !")
        
        st.markdown(f"<div class='score-box'><h2>Ton score : {st.session_state.my_score} / {len(quiz_data)}</h2></div>", unsafe_allow_html=True)
        
        st.write("---")
        st.subheader("📊 Classement des joueurs")
        
        # Affichage des scores de tout le monde sous forme de tableau
        if st.session_state.global_scores:
            df = pd.DataFrame(st.session_state.global_scores.items(), columns=['Joueur', 'Points'])
            df = df.sort_values(by='Points', ascending=False)
            st.table(df)
        
        if st.button("🔄 Recommencer"):
            st.session_state.question_index = 0
            st.session_state.my_score = 0
            st.rerun()
