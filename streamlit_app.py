import streamlit as st

# Configuration
st.set_page_config(page_title="Notre Quiz Privé", layout="centered")

# Initialisation du score et de la question
if 'question_index' not in st.session_state:
    st.session_state.question_index = 0
if 'score' not in st.session_state:
    st.session_state.score = 0

# Tes questions
quiz_data = [
    {"q": "Quelle est la capitale de l'Islande ?", "a": ["Oslo", "Reykjavik", "Helsinki"], "c": "Reykjavik"},
    {"q": "Qui a gagné la coupe du monde 2022 ?", "a": ["France", "Argentine", "Brésil"], "c": "Argentine"},
    {"q": "Quel groupe chante 'Bohemian Rhapsody' ?", "a": ["The Beatles", "Queen", "Led Zeppelin"], "c": "Queen"}
]

st.title("🏆 Notre Quiz Personnalisé")

if st.session_state.question_index < len(quiz_data):
    current_q = quiz_data[st.session_state.question_index]
    st.subheader(f"Question {st.session_state.question_index + 1}")
    st.write(f"### {current_q['q']}")

    # Affichage des boutons
    for option in current_q['a']:
        if st.button(option):
            if option == current_q['c']:
                st.success("Bravo ! ✅")
                st.session_state.score += 1
            else:
                st.error(f"Raté ! La réponse était {current_q['c']} ❌")
            
            st.session_state.question_index += 1
            st.button("Question suivante ➡️")

else:
    st.balloons()
    st.header("Quiz terminé !")
    st.write(f"### Ton score final : {st.session_state.score} / {len(quiz_data)}")
    if st.button("Recommencer"):
        st.session_state.question_index = 0
        st.session_state.score = 0
        st.rerun()
