import streamlit as st

# Look & Feel
st.set_page_config(page_title="Ultimate Blind Test", layout="centered")

# Style personnalisé pour des boutons plus grands sur mobile
st.markdown("""
    <style>
    div.stButton > button {
        width: 100%;
        height: 60px;
        font-size: 20px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_index=True)

if 'question_index' not in st.session_state:
    st.session_state.question_index = 0
if 'score' not in st.session_state:
    st.session_state.score = 0

# --- TA PLAYLIST AMÉLIORÉE ---
quiz_data = [
    {
        "q": "Années 80 : Qui est-ce ?", 
        "url": "https://www.youtube.com/watch?v=9jK-NcRmVcw", # Europe - The Final Countdown
        "a": ["Europe", "Scorpions", "Bon Jovi"], 
        "c": "Europe"
    },
    {
        "q": "Musique de Film :", 
        "url": "https://www.youtube.com/watch?v=y6120QOlsfU", # Darude Sandstorm (exemple)
        "a": ["Taxi", "Fast & Furious", "Drive"], 
        "c": "Taxi"
    }
]

st.title("🎮 Ultimate Blind Test")
st.progress((st.session_state.question_index) / len(quiz_data))

if st.session_state.question_index < len(quiz_data):
    current_q = quiz_data[st.session_state.question_index]
    
    st.subheader(f"Question {st.session_state.question_index + 1} / {len(quiz_data)}")
    
    with st.expander("🎵 Cliquez ici pour lancer la musique", expanded=True):
        # On affiche le lecteur mais on prévient les joueurs de ne pas tricher !
        st.video(current_q['url'])
    
    st.write("---")
    st.write(f"**{current_q['q']}**")

    # Organisation des boutons en colonnes pour le look
    col1, col2 = st.columns(2)
    
    for i, option in enumerate(current_q['a']):
        # Alterne entre colonne 1 et 2
        target_col = col1 if i % 2 == 0 else col2
        if target_col.button(option):
            if option == current_q['c']:
                st.toast("🔥 Bien joué !", icon="✅")
                st.session_state.score += 1
            else:
                st.toast("Oups... Raté !", icon="❌")
            
            st.session_state.question_index += 1
            st.rerun()

else:
    st.balloons()
    st.header("🏁 Score Final")
    st.metric(label="Précision", value=f"{st.session_state.score} / {len(quiz_data)}")
    
    if st.button("🔄 Rejouer"):
        st.session_state.question_index = 0
        st.session_state.score = 0
        st.rerun()
