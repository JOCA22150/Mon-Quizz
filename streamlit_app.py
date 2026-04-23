import streamlit as st
import pandas as pd

st.set_page_config(page_title="Le Quiz des Champions", layout="centered")

# --- STYLE ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; height: 55px; border-radius: 12px; font-size: 18px; font-weight: bold; background-color: #f0f2f6; }
    .score-box { padding: 25px; background-color: #e8f0fe; border-radius: 20px; text-align: center; border: 2px solid #4285f4; }
    </style>
""", unsafe_allow_html=True)

if 'global_scores' not in st.session_state:
    st.session_state.global_scores = {}
if 'question_index' not in st.session_state:
    st.session_state.question_index = 0
if 'my_score' not in st.session_state:
    st.session_state.my_score = 0
if 'pseudo' not in st.session_state:
    st.session_state.pseudo = ""

# --- QUESTIONS ---
quiz_data = [
    {"q": "Qui a peint la Joconde ?", "a": ["Van Gogh", "Picasso", "Léonard de Vinci"], "c": "Léonard de Vinci"},
    {"q": "Quelle est la capitale de l'Islande ?", "a": ["Oslo", "Reykjavik", "Helsinki"], "c": "Reykjavik"},
    {"q": "Quel groupe chante 'Bohemian Rhapsody' ?", "a": ["The Beatles", "Queen", "U2"], "c": "Queen"}
]

st.title("🏆 Le Quiz de la Soirée")

if st.session_state.pseudo == "":
    st.write("### 👋 Salut ! Entrez votre pseudo :")
    nom = st.text_input("", placeholder="Ton prénom ici...")
    if st.button("Lancer le Quiz !"):
        if nom:
            st.session_state.pseudo = nom
            st.rerun()
else:
    if st.session_state.question_index < len(quiz_data):
        current_q = quiz_data[st.session_state.question_index]
        st.write(f"Joueur : **{st.session_state.pseudo}**")
        st.progress(st.session_state.question_index / len(quiz_data))
        st.info(f"Question {st.session_state.question_index + 1} : {current_q['q']}")

        for option in current_q['a']:
            if st.button(option):
                if option == current_q['c']:
                    st.toast("Bravo ! ✅")
                    st.session_state.my_score += 1
                else:
                    st.toast("Raté... ❌")
                st.session_state.question_index += 1
                st.rerun()
    else:
        st.session_state.global_scores[st.session_state.pseudo] = st.session_state.my_score
        st.balloons()
        st.header("🏁 C'est fini !")
        
        # --- ASTUCE AUTO-PLAY ---
        # On utilise un petit bout de code invisible qui force la lecture
        audio_url = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
        st.markdown(f'<audio src="{audio_url}" autoplay="true"></audio>', unsafe_allow_html=True)
        st.write("🎶 *La musique de victoire se lance...*")

        st.markdown(f"<div class='score-box'><h2>Ton score final : {st.session_state.my_score} / {len(quiz_data)}</h2></div>", unsafe_allow_html=True)
        
        st.write("---")
        st.subheader("📊 Classement en direct")
        if st.session_state.global_scores:
            df = pd.DataFrame(st.session_state.global_scores.items(), columns=['Joueur', 'Points'])
            df = df.sort_values(by='Points', ascending=False)
            st.table(df)
        
        if st.button("🔄 Rejouer"):
            st.session_state.question_index = 0
            st.session_state.my_score = 0
            st.rerun()
