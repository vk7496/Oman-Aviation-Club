import streamlit as st
from groq import Groq

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="AI Aviation Career Advisor",
    page_icon="✈️",
    layout="centered"
)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ---------------- LANGUAGE ----------------
language = st.selectbox(
    "🌍 Select Language / اختر اللغة",
    ["English", "العربية"]
)

# ---------------- TEXTS ----------------
TEXT = {
    "English": {
        "title": "✈️ AI Aviation Career Advisor",
        "subtitle": "Discover your ideal career path in aviation using Artificial Intelligence",
        "age": "Your Age",
        "education": "Education Level",
        "country": "Preferred Country",
        "interest": "Aviation Interest",
        "button": "Generate My Career Path",
        "loading": "Analyzing your aviation future...",
    },
    "العربية": {
        "title": "✈️ مستشار المسار المهني في الطيران بالذكاء الاصطناعي",
        "subtitle": "اكتشف مستقبلك المهني في مجال الطيران باستخدام الذكاء الاصطناعي",
        "age": "العمر",
        "education": "المستوى التعليمي",
        "country": "الدولة المفضلة",
        "interest": "مجال الاهتمام",
        "button": "إنشاء المسار المهني",
        "loading": "جاري تحليل مستقبلك في الطيران...",
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
def generate_prompt():
    if language == "English":
        return f"""
You are an aviation career expert.

User details:
Age: {age}
Education: {education}
Preferred country: {country}
Interest: {interest}

Provide:
1. Recommended career path
2. Required licenses/certifications
3. Estimated cost range
4. Time required
5. Recommended countries or academies
6. Short professional advice

Use clear bullet points.
"""
    else:
        return f"""
أنت خبير في المسارات المهنية في مجال الطيران.

بيانات المستخدم:
العمر: {age}
المستوى التعليمي: {education}
الدولة المفضلة: {country}
مجال الاهتمام: {interest}

قدّم:
1. المسار المهني المقترح
2. التراخيص والشهادات المطلوبة
3. التكلفة التقريبية
4. المدة الزمنية
5. دول أو أكاديميات مقترحة
6. نصيحة مهنية قصيرة

استخدم نقاط واضحة وبأسلوب احترافي.
"""

# ---------------- ACTION ----------------
if st.button(T["button"]):
    with st.spinner(T["loading"]):
        completion = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional aviation career advisor."
                },
                {
                    "role": "user",
                    "content": generate_prompt()
                }
            ],
            temperature=0.6,
            max_tokens=700
        )

        result = completion.choices[0].message.content
        st.success("✅ Result")
        st.markdown(result)
