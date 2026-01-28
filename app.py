import streamlit as st
from groq import Groq

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Aviation Career Advisor",
    page_icon="✈️",
    layout="centered"
)

# ---------------- GROQ CLIENT ----------------
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ---------------- LANGUAGE SELECT ----------------
language = st.selectbox(
    "🌍 Select Language / اختر اللغة",
    ["English", "العربية"]
)

# ---------------- TEXT CONTENT ----------------
TEXT = {
    "English": {
        "title": "✈️ AI Aviation Career Advisor",
        "subtitle": "Explore your ideal career path in aviation using Artificial Intelligence",
        "age": "Your Age",
        "education": "Education Level",
        "country": "Preferred Country",
        "interest": "Aviation Interest",
        "button": "Generate My Career Path",
        "loading": "Analyzing your aviation future...",
        "result": "Career Recommendation"
    },
    "العربية": {
        "title": "✈️ مستشار المسار المهني في الطيران",
        "subtitle": "اكتشف مسارك المهني في مجال الطيران باستخدام الذكاء الاصطناعي",
        "age": "العمر",
        "education": "المستوى التعليمي",
        "country": "الدولة المفضلة",
        "interest": "مجال الاهتمام",
        "button": "إنشاء المسار المهني",
        "loading": "جاري تحليل مستقبلك في الطيران...",
        "result": "التوصية المهنية"
    }
}

T = TEXT[language]

# ---------------- UI ----------------
st.title(T["title"])
st.write(T["subtitle"])
st.divider()

age = st.number_input(T["age"], min_value=16, max_value=60, value=22)

education = st.selectbox(
    T["education"],
    ["High School", "Diploma", "Bachelor Degree", "Master Degree"]
)

country = st.selectbox(
    T["country"],
    ["Oman", "UAE", "Saudi Arabia", "Europe", "Other"]
)

interest = st.selectbox(
    T["interest"],
    [
        "Pilot",
        "Air Traffic Controller (ATC)",
        "Cabin Crew",
        "Aircraft Maintenance Engineer",
        "Aviation Management",
        "Flight Dispatcher"
    ]
)

# ---------------- PROMPT ----------------
def build_prompt():
    if language == "English":
        return f"""
You are an expert aviation career advisor.

User profile:
- Age: {age}
- Education: {education}
- Preferred country: {country}
- Area of interest: {interest}

Provide:
1. Recommended aviation career path
2. Required licenses or certifications
3. Estimated cost range
4. Required time to qualify
5. Recommended countries or academies
6. A short professional advice

Use clear bullet points and professional tone.
"""
    else:
        return f"""
أنت خبير في المسارات المهنية في مجال الطيران.

بيانات المستخدم:
- العمر: {age}
- المستوى التعليمي: {education}
- الدولة المفضلة: {country}
- مجال الاهتمام: {interest}

قدّم:
1. المسار المهني المناسب
2. التراخيص أو الشهادات المطلوبة
3. التكلفة التقريبية
4. المدة اللازمة للتأهيل
5. دول أو أكاديميات مقترحة
6. نصيحة مهنية قصيرة

استخدم نقاط واضحة وبأسلوب احترافي.
"""

# ---------------- ACTION ----------------
if st.button(T["button"]):
    with st.spinner(T["loading"]):
        try:
            completion = client.chat.completions.create(
                model="llama3-8b-8192",  # ✅ stable & fast
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional aviation career advisor."
                    },
                    {
                        "role": "user",
                        "content": build_prompt()
                    }
                ],
                temperature=0.6,
                max_tokens=700
            )

            result = completion.choices[0].message.content
            st.subheader(T["result"])
            st.markdown(result)

        except Exception as e:
            st.error("⚠️ Something went wrong. Please check API key or model availability.")
