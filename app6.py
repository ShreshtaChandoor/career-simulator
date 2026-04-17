import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="Career Simulator Pro", layout="centered")

# Title
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🚀 Career Decision Simulator Pro</h1>", unsafe_allow_html=True)
st.write("Answer a few questions and discover careers that fit *YOU*")

# -----------------------------
# 🎯 SECTION 1: PERSONALITY MCQs
# -----------------------------

st.header("🧠 Tell us about yourself")

interest = st.radio(
    "What interests you the most?",
    ["Technology 💻", "Business 💼", "Creativity 🎨", "Helping People ❤️", "Government & Law ⚖️"]
)

work_style = st.radio(
    "Preferred work style?",
    ["Structured & Stable", "Flexible & Dynamic", "Creative & Free", "Leadership & Decision-making"]
)

risk_pref = st.slider("Risk Tolerance (low = safe career)", 1, 10)

salary_weight = st.slider("Salary Importance 💰", 1, 10)
demand_weight = st.slider("Job Demand Importance 📈", 1, 10)

# -----------------------------
# 📊 SECTION 2: CAREER DATA
# -----------------------------

data = {
    "Career": [
        "Software Engineer", "Data Scientist", "Cybersecurity Analyst",
        "Doctor", "Nurse", "Psychologist",
        "IAS Officer", "Lawyer", "Judge",
        "Entrepreneur", "Investment Banker", "CA",
        "Graphic Designer", "Animator", "Content Creator",
        "Teacher", "Professor", "Researcher"
    ],
    
    "Category": [
        "Technology", "Technology", "Technology",
        "Healthcare", "Healthcare", "Healthcare",
        "Government", "Government", "Government",
        "Business", "Business", "Business",
        "Creative", "Creative", "Creative",
        "Education", "Education", "Education"
    ],

    "Salary": [9, 9, 8, 8, 6, 7, 7, 8, 9, 10, 10, 9, 6, 7, 8, 6, 7, 8],
    "Demand": [9, 9, 8, 8, 7, 7, 8, 7, 6, 8, 7, 8, 7, 6, 9, 8, 7, 8],
    "Risk":   [3, 4, 4, 5, 3, 4, 2, 4, 3, 9, 7, 6, 6, 7, 8, 2, 3, 4]
}

df = pd.DataFrame(data)

# -----------------------------
# 🧠 SECTION 3: SCORING LOGIC
# -----------------------------

def match_score(row):
    score = 0

    # Interest mapping
    if interest == "Technology 💻" and row["Category"] == "Technology":
        score += 20
    elif interest == "Business 💼" and row["Category"] == "Business":
        score += 20
    elif interest == "Creativity 🎨" and row["Category"] == "Creative":
        score += 20
    elif interest == "Helping People ❤️" and row["Category"] in ["Healthcare", "Education"]:
        score += 20
    elif interest == "Government & Law ⚖️" and row["Category"] == "Government":
        score += 20

    # Work style mapping
    if work_style == "Structured & Stable" and row["Risk"] <= 4:
        score += 10
    elif work_style == "Flexible & Dynamic" and row["Risk"] >= 5:
        score += 10
    elif work_style == "Creative & Free" and row["Category"] == "Creative":
        score += 10
    elif work_style == "Leadership & Decision-making" and row["Category"] in ["Business", "Government"]:
        score += 10

    return score

df["MatchScore"] = df.apply(match_score, axis=1)

# Final Score
df["Final Score"] = (
    (df["Salary"] * salary_weight) +
    (df["Demand"] * demand_weight) -
    (df["Risk"] * risk_pref) +
    df["MatchScore"]
)

# -----------------------------
# 📊 SECTION 4: RESULTS
# -----------------------------

st.header("📊 Career Results")

st.dataframe(df.sort_values(by="Final Score", ascending=False))

best = df.loc[df["Final Score"].idxmax()]

st.success(f"🎯 Best Career for You: {best['Career']}")

# -----------------------------
# 📈 SECTION 5: VISUALIZATION
# -----------------------------

st.header("📈 Career Score Visualization")

fig, ax = plt.subplots()
ax.barh(df["Career"], df["Final Score"])
ax.set_xlabel("Score")
ax.set_title("Career Ranking")

st.pyplot(fig)

# -----------------------------
# 💡 SECTION 6: FUN INSIGHT
# -----------------------------

st.info(f"""
✨ Based on your answers:
- You prefer **{interest}**
- Your style is **{work_style}**
- Risk tolerance: **{risk_pref}/10**

This is why **{best['Career']}** suits you best!
""")