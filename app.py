
import json
from pathlib import Path

import streamlit as st

from src.topics import get_tracks, get_topics
from src.attempts import create_attempt, append_attempt, load_attempts
from src.report import get_learner_report

ROOT = Path(__file__).resolve().parent
QUESTION_FILE = ROOT / "data" / "questions.json"
ATTEMPT_FILE = ROOT / "data" / "attempts.jsonl"

st.set_page_config(
    page_title="MEOWNEr ♡",
    page_icon="🐈",
    layout="wide",
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #faf6ff 0%, #f4f8f1 55%, #fff6f8 100%);
}
.block-container {padding-top: 2rem; max-width: 1100px;}
h1, h2, h3 {color: #665276;}
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.72);
    border: 1px solid #e9deef;
    padding: 18px;
    border-radius: 16px;
}
.stButton button, .stFormSubmitButton button {
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_questions():
    with open(QUESTION_FILE, encoding="utf-8") as f:
        return json.load(f)


questions = load_questions()
tracks = get_tracks()

if "learner_id" not in st.session_state:
    st.session_state.learner_id = "demo-learner"

if "answered" not in st.session_state:
    st.session_state.answered = {}


st.sidebar.title("🐈 MEOWNEr")
st.sidebar.caption("your little placement-prep corner ♡")

learner_id = st.sidebar.text_input(
    "Learner ID",
    value=st.session_state.learner_id,
).strip()

if learner_id:
    st.session_state.learner_id = learner_id

page = st.sidebar.radio(
    "Your space",
    ["Home", "Learn", "Practice", "Revision", "Mock tests", "Progress"],
)

st.sidebar.markdown("---")
st.sidebar.caption("small steps count, too 🌱")


def track_label(track_id):
    return tracks.get(track_id, track_id.replace("_", " ").title())


def show_question(question, mode="Practice"):
    st.markdown(f"**{question['topic']}** · {question.get('difficulty', 'starter').title()}")
    st.write(question["question"])

    options = question.get("options", [])
    if not options:
        st.warning("This question has no answer options yet.")
        return

    key = f"{mode}_{question['id']}"
    previous = st.session_state.answered.get(key)

    with st.form(key=f"form_{key}"):
        selected = st.radio(
            "Choose your answer",
            options,
            index=options.index(previous["selected_answer"])
            if previous and previous["selected_answer"] in options else None,
            key=f"answer_{key}",
        )
        submitted = st.form_submit_button("Check answer ♡")

    if submitted:
        attempt = create_attempt(
            learner_id=st.session_state.learner_id,
            question=question,
            selected_answer=selected,
        )
        append_attempt(attempt, path=str(ATTEMPT_FILE))
        st.session_state.answered[key] = {
            "selected_answer": selected,
            "correct": attempt["correct"],
        }
        st.rerun()

    result = st.session_state.answered.get(key)
    if result:
        if result["correct"]:
            st.success("Correct! Look at you go ✨")
        else:
            st.error(f"Not quite — the correct answer is: {question['answer']}")
        st.info(question.get("explanation", "Keep practising; you'll get there."))


st.title("MEOWNEr ♡")
st.caption("learn a little. practise a little. get closer to that offer.")

if page == "Home":
    st.subheader("Welcome to your little learning meadow 🌷")
    st.write("A calm corner for placement prep — without needing to tackle everything at once.")

    cols = st.columns(3)
    track_ids = ["aptitude", "logical_reasoning", "coding"]
    friendly = ["Quantitative aptitude", "Logical reasoning", "Coding"]

    for col, track_id, name in zip(cols, track_ids, friendly):
        count = sum(q["track_id"] == track_id for q in questions)
        with col:
            st.markdown(f"### {name}")
            st.metric("Starter questions", count)

    st.markdown("---")
    st.subheader("A tiny plan for today")
    st.write("1. Pick one topic in **Learn**.")
    st.write("2. Try a few questions in **Practice**.")
    st.write("3. Check your weaker topics in **Progress**.")
    st.info("Your question bank is separate from the ASSISTments dataset used in the ML experiments.")

elif page == "Learn":
    st.subheader("Learn 🌱")
    track_id = st.selectbox(
        "Choose a track",
        list(tracks.keys()),
        format_func=track_label,
    )
    topics = get_topics(track_id)
    topic = st.selectbox("Choose a topic", topics)
    topic_questions = [
        q for q in questions
        if q["track_id"] == track_id and q["topic"] == topic
    ]

    if topic_questions:
        for q in topic_questions:
            with st.container(border=True):
                st.markdown(f"**{q['id']} · {q.get('difficulty', 'starter').title()}**")
                st.write(q["question"])
                with st.expander("Show answer and explanation"):
                    st.write(f"**Answer:** {q['answer']}")
                    st.write(q.get("explanation", ""))
    else:
        st.info("This topic is on the roadmap! More lessons and questions will be added.")

elif page == "Practice":
    st.subheader("Practice corner ✏️")
    track_id = st.selectbox(
        "Choose a track",
        list(tracks.keys()),
        format_func=track_label,
    )
    available = [q for q in questions if q["track_id"] == track_id]

    if available:
        selected_id = st.selectbox(
            "Choose a question",
            [q["id"] for q in available],
            format_func=lambda qid: next(
                f"{q['topic']} · {q['id']}" for q in available if q["id"] == qid
            ),
        )
        question = next(q for q in available if q["id"] == selected_id)
        show_question(question)
    else:
        st.info("No questions in this track yet.")

elif page == "Revision":
    st.subheader("Revision nook 🌼")
    attempts = load_attempts(str(ATTEMPT_FILE))
    mine = [a for a in attempts if a.get("learner_id") == st.session_state.learner_id]
    incorrect_ids = {a["question_id"] for a in mine if a.get("correct") == 0}
    revision_questions = [q for q in questions if q["id"] in incorrect_ids]

    if revision_questions:
        st.write("Questions you've answered incorrectly — a second look is a good thing.")
        for q in revision_questions:
            with st.container(border=True):
                st.markdown(f"**{q['topic']} · {q['id']}**")
                st.write(q["question"])
                with st.expander("Review answer"):
                    st.write(f"**Answer:** {q['answer']}")
                    st.write(q.get("explanation", ""))
    else:
        st.info("Your revision list will appear here after you attempt some questions.")

elif page == "Mock tests":
    st.subheader("Mock test room 📝")
    st.info("Mock tests are the next milestone. We'll add timed sessions, scoring, and a final review after the basic practice flow is verified.")
    st.write(f"Current question bank: **{len(questions)} questions** across three tracks.")

elif page == "Progress":
    st.subheader("Your progress 🌿")
    report = get_learner_report(
        learner_id=st.session_state.learner_id,
        attempts_path=str(ATTEMPT_FILE),
        min_attempts=1,
        top_n=5,
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Attempts", report["total_attempts"])
    c2.metric("Correct answers", report["correct_answers"])
    c3.metric("Accuracy", f"{report['accuracy']:.0%}")

    st.markdown("### Topic progress")
    if report["topic_progress"]:
        st.dataframe(
            [
                {
                    "Track": track_label(row["track_id"]),
                    "Topic": row["topic"],
                    "Attempts": row["attempts"],
                    "Correct": row["correct_answers"],
                    "Accuracy": f"{row['accuracy']:.0%}",
                }
                for row in report["topic_progress"]
            ],
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No attempts yet. Complete a practice question and your progress will appear here.")

    st.markdown("### Topics to revisit")
    if report["weak_topics"]:
        for row in report["weak_topics"]:
            st.write(
                f"• **{row['topic']}** — {row['accuracy']:.0%} accuracy "
                f"({row['attempts']} attempt(s))"
            )
        st.caption("Early recommendations are based on limited attempts, so treat them as hints.")
    else:
        st.write("Keep practising and your topic recommendations will appear here.")

st.markdown("---")
st.caption("MEOWNEr · built one small step at a time ♡")
