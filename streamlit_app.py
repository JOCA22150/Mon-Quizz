import streamlit as st

# Configuration de la page
st.set_page_config(page_title="Le Grand Quiz", page_icon="📝", layout="centered")

# Design personnalisé (Couleurs, bords arrondis, boutons larges)
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        height: 60px;
        border-radius: 12px;
        font-size: 20px;
        font-weight: bold;
        transition: 0.3s;
    }
    .main {
        background-color: #f5f7f9;
    }
    </style>
""", unsafe_allow_html=True)

# Initialisation des variables de session
if 'question_index' not in st.session_state:
    st.session_state.question_index = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'answered' not in st.session_state:
    st.session_state.answered = False

# --- TA BASE DE QUESTIONS ---
quiz_data = [
    {
        "q": "Quel est l'oiseau qui ne peut pas voler mais court très vite ?",
        "a": ["Le Manchot", "L'Autruche", "Le Kiwi"],
        "c": "L'Autruche",
        "info": "L'autruche peut atteindre 70 km/h !"
    },
    {
        "q": "Dans quelle ville se trouve le Colisée ?",
        "a": ["Athènes", "Rome", "Naples"],
        "c": "Rome",
        "info": "Le Colisée est le plus grand amphithéâtre jamais construit."
    },
    {
        "q": "Quel est l'élément chimique représenté par le symbole 'Au' ?",
        "a": ["Argent", "Aluminium", "Or"],
        "c": "Or",
        "info": "Le symbole vient du latin 'Aurum'."
    }
]

st.title("🏆 Le Quiz Intégré")
st.write("---")

# Affichage du score et de la progression
barre_progression = (st.session_state.question_index) / len(quiz_data)
st.progress(barre_progression)

if st.session_state.question_index < len(quiz_data):
    current_q = quiz_data[st.session_state.question_index]
    
    st.subheader(f"Question {st.session_state.question_index + 1} sur {len(quiz_data)}")
    st.info(current_q['q'])

    # Affichage des options
    for option in current_q['a']:
        # On désactive les boutons une fois qu'on a répondu
        if st.button(option, disabled=st.session_state.answered):
            st.session_state.answered = True
            if option == current_q['c']:
                st.success(f"Bravo ! C'est la bonne réponse. ✅")
                st.session_state.score += 1
            else:
                st.error(f"Dommage... La réponse était : {current_q['c']} ❌")
            
            st.write(f"💡 *{current_q['info']}*")
            st.button("Question suivante ➡️", on_click=lambda: setattr(st.session_state, 'answered', False) or st.session_state.__setitem__('question_index', st.session_state.question_index + 1))

else:
    st.balloons()
    st.header("🏁 Quiz terminé !")
    col1, col2 = st.columns(2)
    col1.metric("Score Final", f"{st.session_state.score} / {len(quiz_data)}")
    precision = int((st.session_state.score / len(quiz_data)) * 100)
    col2.metric("Précision", f"{precision}%")
    
    if st.button("🔄 Recommencer le Quiz"):
        st.session_state.question_index = 0
        st.session_state.score = 0
        st.session_state.answered = False
        st.rerun()
