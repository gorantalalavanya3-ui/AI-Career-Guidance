import streamlit as st
import pandas as pd
from career_data import CAREERS

st.set_page_config(page_title="AI Career Guidance", page_icon="🎓", layout="wide")

st.markdown("""
<style>
    .main {background: #f7f8fc;}
    .hero {padding: 1.5rem 1.8rem; border-radius: 18px; color: white;
           background: linear-gradient(120deg,#243b80,#5865d9);}
    .hero h1 {color:white; margin-bottom:.25rem;}
    .hero p {color:#eef0ff; font-size:1.05rem;}
    .metric-card {background:white; padding:1rem; border-radius:14px;
                  border:1px solid #e8eaf3; margin-bottom:.7rem;}
    .small-muted {color:#667085; font-size:.9rem;}
</style>
""", unsafe_allow_html=True)

if "results" not in st.session_state:
    st.session_state.results = None

with st.sidebar:
    st.title("🎓 Career Compass")
    page = st.radio("Navigate", ["Home", "Career Assessment", "Recommendations", "About Project"])
    st.divider()
    st.caption("Diploma CSE Mini Project")
    st.caption("Recommendation scores are guidance indicators, not guaranteed predictions.")

if page == "Home":
    st.markdown("""
    <div class="hero">
      <h1>Find a career that fits you.</h1>
      <p>Explore career paths using your interests, skills and learning preferences.</p>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    a, b, c = st.columns(3)
    a.metric("Career paths", len(CAREERS))
    b.metric("Assessment areas", "5")
    c.metric("Built with", "Python + Streamlit")
    st.subheader("How it works")
    cols = st.columns(3)
    cols[0].markdown("### 1. 👤 Tell us about you\nEnter your qualification, interests and current skills.")
    cols[1].markdown("### 2. 📝 Complete assessment\nAnswer a few questions about the work you enjoy.")
    cols[2].markdown("### 3. 🚀 Explore matches\nReview suggested careers, skill gaps and a learning roadmap.")
    st.info("Start with **Career Assessment** in the left menu. You can change your answers and reassess at any time.")

elif page == "Career Assessment":
    st.title("📝 Career Assessment")
    st.write("Complete the form. Choose what genuinely interests you; there are no right or wrong answers.")
    with st.form("assessment_form"):
        name = st.text_input("Your name", placeholder="Enter your name")
        qualification = st.selectbox("Current qualification",
            ["Diploma CSE", "Diploma (Other)", "Intermediate", "B.Sc / BCA", "B.Tech / BE", "Other"])
        interests = st.multiselect("Which areas interest you most?",
            ["Building websites", "Programming and logic", "Artificial intelligence", "Data and numbers",
             "Cybersecurity", "Mobile apps", "Design and creativity", "Helping and teaching others"],
            default=["Programming and logic"])
        skills = st.multiselect("Which skills do you currently have?",
            ["Python", "Java", "C / C++", "HTML", "CSS", "JavaScript", "SQL", "Excel",
             "Problem solving", "Communication", "Graphic design", "Networking"])
        favourite = st.selectbox("Favourite subject or activity",
            ["Programming", "Mathematics", "Computer networks", "Web design", "Working with data",
             "Electronics", "Communication", "Creative design"])
        work_style = st.radio("What type of work sounds best?",
            ["Writing code and building products", "Finding patterns in data",
             "Protecting systems and solving security problems",
             "Designing useful and attractive experiences",
             "Explaining technology and helping people"])
        learning = st.select_slider("How comfortable are you with learning new technology?",
            options=["Just starting", "A little comfortable", "Comfortable", "Very comfortable"])
        submitted = st.form_submit_button("✨ Get my career recommendations", use_container_width=True)
    if submitted:
        if not name.strip():
            st.error("Please enter your name.")
        elif not interests:
            st.error("Please select at least one interest.")
        else:
            st.session_state.profile = {
                "name": name.strip(), "qualification": qualification, "interests": interests,
                "skills": skills, "favourite": favourite, "work_style": work_style,
                "learning": learning
            }
            st.session_state.results = None
            st.success("Assessment saved! Open Recommendations to view your career matches.")

elif page == "Recommendations":
    st.title("🤖 Your Career Recommendations")
    if "profile" not in st.session_state:
        st.warning("Please complete the Career Assessment first.")
        st.button("Go to assessment", on_click=lambda: st.session_state.update({"_unused": True}))
    else:
        p = st.session_state.profile
        st.write(f"Hello **{p['name']}**! Here are career paths that may suit your interests.")
        interest_map = {
            "Building websites": ["Web Developer", "UI/UX Designer"],
            "Programming and logic": ["Python Developer", "Software Developer"],
            "Artificial intelligence": ["AI / Machine Learning Associate", "Data Analyst"],
            "Data and numbers": ["Data Analyst", "Database Developer"],
            "Cybersecurity": ["Cybersecurity Analyst", "Network Administrator"],
            "Mobile apps": ["Mobile App Developer", "Software Developer"],
            "Design and creativity": ["UI/UX Designer", "Web Developer"],
            "Helping and teaching others": ["IT Support Specialist", "Technical Trainer"]
        }
        style_map = {
            "Writing code and building products": ["Python Developer", "Software Developer", "Web Developer", "Mobile App Developer"],
            "Finding patterns in data": ["Data Analyst", "AI / Machine Learning Associate", "Database Developer"],
            "Protecting systems and solving security problems": ["Cybersecurity Analyst", "Network Administrator"],
            "Designing useful and attractive experiences": ["UI/UX Designer", "Web Developer"],
            "Explaining technology and helping people": ["IT Support Specialist", "Technical Trainer"]
        }
        scores = {}
        for career in CAREERS:
            score = 0
            for interest in p["interests"]:
                if career["title"] in interest_map.get(interest, []):
                    score += 3
            if career["title"] in style_map.get(p["work_style"], []):
                score += 3
            overlap = set(p["skills"]) & set(career["related_skills"])
            score += min(len(overlap), 4)
            if p["favourite"] in career["subjects"]:
                score += 2
            scores[career["title"]] = score
        max_possible = 3 * len(p["interests"]) + 3 + 4 + 2
        ranked = sorted(CAREERS, key=lambda x: scores[x["title"]], reverse=True)
        rows = []
        for career in ranked:
            percent = round(min(98, scores[career["title"]] / max_possible * 100))
            rows.append({"Career": career["title"], "Match indicator": f"{percent}%",
                         "Score": percent, "Description": career["description"]})
        results_df = pd.DataFrame(rows)
        st.subheader("Top career matches")
        for career in ranked[:3]:
            percent = next(r["Score"] for r in rows if r["Career"] == career["title"])
            with st.container(border=True):
                left, right = st.columns([4, 1])
                left.subheader(career["title"])
                left.write(career["description"])
                right.metric("Match", f"{percent}%")
                st.progress(percent / 100)
                st.caption("Skills to develop: " + ", ".join(career["related_skills"]))
        st.subheader("Skill gap and learning roadmap")
        chosen = st.selectbox("Choose a career to explore", [c["title"] for c in ranked[:5]])
        selected = next(c for c in CAREERS if c["title"] == chosen)
        missing = [s for s in selected["related_skills"] if s not in p["skills"]]
        x, y = st.columns(2)
        with x:
            st.markdown("#### Skills you already have")
            present = [s for s in selected["related_skills"] if s in p["skills"]]
            st.write(", ".join(present) if present else "Build your foundation in the skills listed on the right.")
        with y:
            st.markdown("#### Skills to develop")
            st.write(", ".join(missing) if missing else "You already selected the key skills for this path.")
        st.markdown("#### Suggested 4-week starter roadmap")
        for week, task in enumerate(selected["roadmap"], start=1):
            st.markdown(f"**Week {week}:** {task}")
        st.download_button("⬇️ Download career results (CSV)",
            data=results_df.to_csv(index=False).encode("utf-8"),
            file_name="career_recommendations.csv", mime="text/csv")
        st.caption("How scores work: the application adds points for selected interests, preferred work style, related skills and favourite subject. Scores are indicative and should be combined with research and mentoring.")

else:
    st.title("ℹ️ About the Project")
    st.subheader("AI-Based Career Guidance System")
    st.write("This project is a student decision-support prototype. It uses a transparent, rule-based recommendation engine to compare a student's interests, skills, preferred work style and favourite subject with career profiles.")
    st.markdown("**Problem statement:** Students often find it difficult to connect their interests and current skills with possible technology careers.")
    st.markdown("**Objective:** Provide understandable career suggestions and beginner learning steps through a simple web interface.")
    st.markdown("**Modules:** Student assessment, career matching, match indicator, skill-gap analysis and learning roadmap.")
    st.markdown("**Future enhancements:** Train and evaluate a machine-learning model using a suitable, ethically collected dataset; add aptitude assessments; include verified course links; and support counsellor feedback.")
    st.warning("Academic note: This prototype does not use a trained machine-learning model. Its recommendation logic is rule-based, so describe it that way in your report and viva.")
