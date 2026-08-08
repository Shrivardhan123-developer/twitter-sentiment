import streamlit as st
import pickle
import numpy as np
import time

# Page config
st.set_page_config(
    page_title="Tweet Sentiment Analyzer",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load model and vectorizer
@st.cache_resource
def load_models():
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("vectorizer.pkl", "rb") as f:
        vectorizer = pickle.load(f)
    return model, vectorizer

model, vectorizer = load_models()

# Custom CSS for stunning animated UI
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap');

* {
    font-family: 'Poppins', sans-serif;
    color: #ffffff !important;
}

/* Animated background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
    background-size: 400% 400%;
    animation: gradient 15s ease infinite;
    color: #ffffff !important;
}

/* Overlay for better text contrast */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.2);
    pointer-events: none;
    z-index: -1;
}

@keyframes gradient {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Floating animation */
@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-20px); }
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
}

@keyframes slideInRight {
    from {
        opacity: 0;
        transform: translateX(100px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

/* Title styling with glow */
.neon-title {
    text-align: center;
    font-size: 56px;
    font-weight: 800;
    background: linear-gradient(90deg, #ff006e, #8338ec, #3a86ff, #06ffa5);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 10px;
    animation: float 3s ease-in-out infinite;
    text-shadow: 0 0 30px rgba(255, 0, 110, 0.5);
}

.neon-subtitle {
    text-align: center;
    font-size: 18px;
    color: #ffffff;
    margin-bottom: 30px;
    font-weight: 500;
    animation: slideInRight 1s ease-out;
    text-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
}

/* Input card */
.input-card {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border: 2px solid rgba(255, 255, 255, 0.2);
    border-radius: 20px;
    padding: 25px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    animation: slideInRight 0.8s ease-out;
}

.input-label {
    font-size: 18px;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 12px;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
}

/* Result boxes with animation */
.positive-box {
    background: linear-gradient(135deg, #34d399, #10b981);
    border-radius: 20px;
    padding: 30px;
    text-align: center;
    box-shadow: 0 10px 40px rgba(52, 211, 153, 0.4);
    animation: slideInRight 0.6s ease-out;
    border: none;
    color: white;
}

.negative-box {
    background: linear-gradient(135deg, #ff6b6b, #ff5252);
    border-radius: 20px;
    padding: 30px;
    text-align: center;
    box-shadow: 0 10px 40px rgba(255, 107, 107, 0.4);
    animation: slideInRight 0.6s ease-out;
    border: none;
    color: white;
}

.result-title {
    font-size: 32px;
    font-weight: 800;
    margin-bottom: 15px;
    animation: pulse 2s ease-in-out infinite;
}

.result-confidence {
    font-size: 24px;
    font-weight: 700;
    margin-top: 15px;
}

/* Input area */
.stTextArea textarea {
    background: rgba(0, 0, 0, 0.6) !important;
    border: 2px solid rgba(255, 255, 255, 0.4) !important;
    border-radius: 15px !important;
    color: white !important;
    font-size: 16px !important;
    transition: all 0.3s !important;
}

.stTextArea textarea::placeholder {
    color: rgba(255, 255, 255, 0.7) !important;
}

.stTextArea textarea:focus {
    border-color: rgba(255, 255, 255, 0.8) !important;
    box-shadow: 0 0 30px rgba(255, 255, 255, 0.3) !important;
    background: rgba(0, 0, 0, 0.7) !important;
}

/* Button styling */
.stButton button {
    background: linear-gradient(90deg, #ff006e, #8338ec) !important;
    color: white !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 15px !important;
    padding: 15px 50px !important;
    font-size: 18px !important;
    transition: all 0.3s !important;
    box-shadow: 0 8px 20px rgba(255, 0, 110, 0.3) !important;
}

.stButton button:hover {
    transform: scale(1.08);
    box-shadow: 0 12px 35px rgba(255, 0, 110, 0.6) !important;
}

.stButton button:active {
    transform: scale(0.98);
}

/* Metrics styling */
.stMetric {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 15px;
    padding: 20px;
    border: 1px solid rgba(255, 255, 255, 0.2);
}

/* Info box */
.info-box {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border-left: 5px solid #06ffa5;
    padding: 20px;
    border-radius: 10px;
    color: #ffffff;
    animation: slideInRight 1.2s ease-out;
    text-shadow: 0 1px 3px rgba(0, 0, 0, 0.5);
}

/* Progress bar */
.stProgress > div > div > div {
    background: linear-gradient(90deg, #06ffa5, #3a86ff) !important;
}

/* Expander */
.streamlit-expanderHeader {
    background: rgba(255, 255, 255, 0.1) !important;
    color: white !important;
    font-weight: 700 !important;
}

/* Divider */
hr {
    border-color: rgba(255, 255, 255, 0.2) !important;
}

/* All headings */
h1, h2, h3, h4, h5, h6 {
    color: #ffffff !important;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5) !important;
}

/* All paragraphs and text */
p, span, div, li, a {
    color: #ffffff !important;
}

/* Warning/Info text */
.stWarning, .stInfo, .stSuccess {
    color: #ffffff !important;
}

/* Expander text - improved */
.streamlit-expanderHeader {
    color: #ffffff !important;
    text-shadow: 0 1px 3px rgba(0, 0, 0, 0.5) !important;
    font-weight: 700 !important;
}

</style>
""", unsafe_allow_html=True)

# Header with animation
st.markdown("<h1 class='neon-title'>🎭 ✨ Tweet Sentiment Analyzer ✨ 🎭</h1>", unsafe_allow_html=True)
st.markdown("<p class='neon-subtitle'>🚀 Analyze tweets with AI-powered predictions in real-time 🚀</p>", unsafe_allow_html=True)

# Create layout with columns
col1, col2 = st.columns([2, 1], gap="medium")

with col1:
    st.markdown("<div class='input-card'>", unsafe_allow_html=True)
    st.markdown("<div class='input-label'>📝 Enter Your Tweet</div>", unsafe_allow_html=True)
    tweet_text = st.text_area("", height=150, placeholder="✨ Type a tweet here... ✨", label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='info-box'>", unsafe_allow_html=True)
    st.markdown("<h4>ℹ️ About This AI</h4>", unsafe_allow_html=True)
    st.markdown("""
    🧠 Trained on **1.6M tweets**
    
    ⚡ Real-time analysis
    
    📊 Confidence scores
    
    🎯 High accuracy
    """)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# Analyze button
col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
with col_btn2:
    if st.button("🚀 ANALYZE SENTIMENT 🚀", use_container_width=True):
        if tweet_text.strip() == "":
            st.warning("⚠️ Please enter some text to analyze")
        else:
            # Animated loading
            with st.spinner("🔮 Analyzing sentiment..."):
                time.sleep(0.5)
                vec = vectorizer.transform([tweet_text])
                pred = model.predict(vec)[0]
                confidence = model.predict_proba(vec)[0]
            
            # Get detailed emotion based on confidence levels
            def get_detailed_emotion(prediction, conf_neg, conf_pos):
                """
                Map confidence scores to 50+ moods with emojis and messages
                """
                # Very strong emotions (>0.95)
                if prediction == 1 and conf_pos > 0.95:
                    moods = [
                        ("😍 OBSESSED", "LOVE IT! 💕", "#ff006e", "You're absolutely loving this!"),
                        ("🤩 AMAZED", "Incredible! 🌟", "#ff1493", "This is mind-blowing!"),
                        ("🚀 AMBITIOUS", "Go conquer! 💪", "#ff6b9d", "You're ready to take over!"),
                        ("😎 CONFIDENT", "Unstoppable vibes! ⚡", "#ff007f", "Pure self-assurance!"),
                        ("🎉 EXCITED", "Thrilled! 🎊", "#ff4757", "Maximum enthusiasm!"),
                    ]
                    return moods[int(conf_pos * 10) % len(moods)], conf_pos * 100
                
                # Strong positive emotions (0.75-0.95)
                elif prediction == 1 and conf_pos > 0.75:
                    moods = [
                        ("😄 HAPPY", "Amazing vibes! 🌟", "#34d399", "Life is good!"),
                        ("😊 HOPEFUL", "Bright future! ✨", "#10b981", "Things are looking up!"),
                        ("🙌 GRATEFUL", "Thankful! 🙏", "#059669", "Blessed vibes!"),
                        ("💪 MOTIVATED", "Let's go! 🔥", "#047857", "Ready for anything!"),
                        ("😃 CHEERFUL", "Smiling inside! 😊", "#0d9488", "Spreading joy!"),
                        ("✨ ROMANTIC", "Love in the air! 💕", "#14b8a6", "Feeling special!"),
                        ("🌈 HOPEFUL", "Everything's possible! 💫", "#06b6d4", "Optimistic energy!"),
                        ("🎊 PLAYFUL", "Having fun! 🎉", "#0891b2", "Life's a party!"),
                        ("😎 PROUD", "Own it! 👑", "#06b6d4", "You're the best!"),
                        ("🚀 ENERGETIC", "Full of energy! ⚡", "#0ea5e9", "Unstoppable force!"),
                        ("💖 AFFECTIONATE", "So much love! 💗", "#38bdf8", "Spreading warmth!"),
                        ("🌟 BLESSED", "Grateful vibes! 🙏", "#7dd3fc", "Feeling fortunate!"),
                    ]
                    return moods[int(conf_pos * 12) % len(moods)], conf_pos * 100
                
                # Moderate positive (0.60-0.75)
                elif prediction == 1 and conf_pos > 0.60:
                    moods = [
                        ("🙂 POSITIVE", "Good tweet! 👍", "#3b82f6", "Decent vibes!"),
                        ("😌 CHILL", "Relaxed mood! 😎", "#0ea5e9", "Going with the flow!"),
                        ("🎵 CREATIVE", "Expressing yourself! 🎨", "#06b6d4", "Inner artist speaking!"),
                        ("🧘 PEACEFUL", "Zen vibes! ☮️", "#0891b2", "Inner calm!"),
                        ("👋 FRIENDLY", "Good company! 🤝", "#06b6d4", "Welcoming energy!"),
                        ("😏 FLIRTY", "Playful teasing! 😉", "#0284c7", "Charming vibes!"),
                        ("💭 THOUGHTFUL", "Deep thinking... 🤔", "#0369a1", "Reflective mood!"),
                        ("🎭 FUNNY", "Making people laugh! 😂", "#06b6d4", "Comedy mode on!"),
                        ("🌱 GROWING", "Getting better! 📈", "#0d9488", "Moving forward!"),
                        ("🕉️ SPIRITUAL", "Connected vibes! ✨", "#06b6d4", "Inner peace!"),
                    ]
                    return moods[int(conf_pos * 10) % len(moods)], conf_pos * 100
                
                # Very strong negative (>0.95)
                elif prediction == 0 and conf_neg > 0.95:
                    moods = [
                        ("😡 FURIOUS", "Yikes! Very angry 🔥", "#dc2626", "Rage mode activated!"),
                        ("💔 HEARTBROKEN", "Devastating! 😭", "#991b1b", "Deep pain!"),
                        ("😢 DEVASTATED", "Completely crushed 😞", "#b91c1c", "Rock bottom!"),
                        ("🖤 DARK", "Very dark energy ⚫", "#7f1d1d", "Deep darkness!"),
                    ]
                    return moods[int(conf_neg * 4) % len(moods)], conf_neg * 100
                
                # Strong negative (0.75-0.95)
                elif prediction == 0 and conf_neg > 0.75:
                    moods = [
                        ("😞 SAD", "Quite negative 😢", "#ff6b6b", "Heavy feelings!"),
                        ("😤 ANGRY", "Frustrated energy 😠", "#ff5252", "Built-up tension!"),
                        ("😭 DEPRESSED", "Deep sadness 💔", "#f87171", "Everything feels heavy!"),
                        ("😔 LONELY", "Isolated vibes 🥺", "#fca5a5", "Seeking connection!"),
                        ("🚫 FEARFUL", "Anxious energy 😰", "#fecaca", "Worried thoughts!"),
                        ("💔 HEARTBROKEN", "Love lost 💘", "#fb7185", "Shattered inside!"),
                        ("😡 SAVAGE", "Sharp tone! ⚔️", "#f43f5e", "Cutting remarks!"),
                        ("🖤 COLD", "Emotionless... ❄️", "#ec4899", "Distant vibes!"),
                        ("😒 ATTITUDE", "Attitude heavy! 💢", "#f72585", "Confrontational!"),
                    ]
                    return moods[int(conf_neg * 9) % len(moods)], conf_neg * 100
                
                # Moderate negative (0.60-0.75)
                elif prediction == 0 and conf_neg > 0.60:
                    moods = [
                        ("😕 NEGATIVE", "Not great vibes... 😞", "#f97316", "Challenging mood!"),
                        ("😑 MOODY", "Unpredictable vibes 🎭", "#fb923c", "Complex feelings!"),
                        ("😒 SARCASTIC", "Thick sarcasm here 😏", "#fdba74", "Witty but sharp!"),
                        ("🥱 LAZY", "Low energy 😴", "#fed7aa", "Just tired..."),
                        ("😕 CONFUSED", "Mixed signals 🤔", "#fbbf24", "Not sure what to feel!"),
                        ("😞 BROKEN", "Acting okay... 💔", "#f59e0b", "Hiding pain inside!"),
                        ("🌙 TIRED", "Exhausted... 😴", "#f97316", "Running on empty!"),
                        ("😒 SARCASM", "Sharp wit! 🔪", "#fb923c", "Sarcasm overload!"),
                        ("🤨 SKEPTICAL", "Doubting... 🤔", "#fdba74", "Not convinced!"),
                        ("😕 JEALOUS", "Green-eyed monster 👀", "#fcd34d", "Envious feelings!"),
                        ("🌪️ MISCHIEVOUS", "Trouble brewing! 😈", "#fbbf24", "Up to something!"),
                        ("😴 BORED", "So tedious... 😐", "#f59e0b", "Yawn inducing!"),
                    ]
                    return moods[int(conf_neg * 12) % len(moods)], conf_neg * 100
                
                # Neutral zone (close to 0.5)
                else:
                    moods = [
                        ("🤔 NEUTRAL", "Could go either way...", "#8b5cf6", "Balanced perspective!"),
                        ("🧐 OVERTHINKING", "Too many thoughts... 🤯", "#a78bfa", "Mind spinning!"),
                        ("🎭 DRAMATIC", "Over the top! 🎬", "#c4b5fd", "Making a scene!"),
                        ("😲 SHOCKED", "Surprising! 😮", "#ddd6fe", "Caught off guard!"),
                        ("🔮 CURIOUS", "Intrigued... 🤨", "#ede9fe", "What's next?"),
                        ("💭 NOSTALGIC", "Missing the past... 🎞️", "#f3e8ff", "Lost in memories!"),
                        ("😐 QUIET", "Silent observer 🤐", "#e9d5ff", "Watching and listening!"),
                        ("❄️ COLD", "Emotionless... 🚫", "#f5f3ff", "Detached vibes!"),
                        ("😵 LOST", "Going nowhere 🛣️", "#dbeafe", "Searching for direction!"),
                        ("🤓 PRODUCTIVE", "Getting things done! 📋", "#93c5fd", "In the zone!"),
                        ("🎪 FUNNY", "Hilarious moments! 😂", "#60a5fa", "Making us laugh!"),
                        ("💎 BOLD", "Standing strong! 💪", "#3b82f6", "Taking a stand!"),
                        ("🌀 MOODY", "Mood swinging... 🎢", "#1d4ed8", "Unpredictable day!"),
                        ("🎯 AMBITIOUS", "Big dreams! 🚀", "#1e40af", "Aiming high!"),
                    ]
                    return moods[int((conf_pos + conf_neg) * 14) % len(moods)], max(conf_pos, conf_neg) * 100
            
            emotion_data, score = get_detailed_emotion(pred, confidence[0], confidence[1])
            emotion, message = emotion_data[0], emotion_data[1]
            gradient = emotion_data[2]
            description = emotion_data[3]
            
            # Display result with animation
            st.markdown("---")
            
            st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, {gradient}, {gradient}cc);
                border-radius: 20px;
                padding: 30px;
                text-align: center;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
                animation: slideInRight 0.6s ease-out;
                border: none;
                color: white;
            '>
                <div style='font-size: 32px; font-weight: 800; margin-bottom: 15px; animation: pulse 2s ease-in-out infinite;'>
                    {emotion}
                </div>
                <div style='font-size: 16px; margin-top: 10px;'>
                    {message}
                </div>
                <div style='font-size: 14px; margin-top: 8px; opacity: 0.95;'>
                    💭 {description}
                </div>
                <div style='font-size: 24px; font-weight: 700; margin-top: 15px;'>
                    Confidence: {score:.1f}% 💯
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Emotion breakdown with progress bars
            st.markdown("### 📊 Emotion Analysis")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("😔 Negative Score", f"{confidence[0]*100:.1f}%")
                st.progress(confidence[0], text="Negativity Level")
            with col2:
                st.metric("😊 Positive Score", f"{confidence[1]*100:.1f}%")
                st.progress(confidence[1], text="Positivity Level")
            
            # Detailed emotion insights
            st.markdown("### 🎯 Detailed Insights")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div style='
                    background: rgba(255, 107, 107, 0.2);
                    padding: 15px;
                    border-radius: 10px;
                    border-left: 4px solid #ff6b6b;
                    text-align: center;
                >
                    <div style='font-size: 24px;'>😔</div>
                    <div style='font-weight: 700; margin-top: 10px;'>Negativity</div>
                    <div style='font-size: 18px; font-weight: 600; color: #ff6b6b; margin-top: 8px;'>{confidence[0]*100:.0f}%</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                neutrality = 1 - abs(confidence[1] - 0.5) * 2
                st.markdown(f"""
                <div style='
                    background: rgba(139, 92, 246, 0.2);
                    padding: 15px;
                    border-radius: 10px;
                    border-left: 4px solid #8b5cf6;
                    text-align: center;
                >
                    <div style='font-size: 24px;'>🤔</div>
                    <div style='font-weight: 700; margin-top: 10px;'>Neutrality</div>
                    <div style='font-size: 18px; font-weight: 600; color: #8b5cf6; margin-top: 8px;'>{max(0, (1 - abs(confidence[1] - 0.5) * 2)) * 100:.0f}%</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div style='
                    background: rgba(52, 211, 153, 0.2);
                    padding: 15px;
                    border-radius: 10px;
                    border-left: 4px solid #34d399;
                    text-align: center;
                >
                    <div style='font-size: 24px;'>😊</div>
                    <div style='font-weight: 700; margin-top: 10px;'>Positivity</div>
                    <div style='font-size: 18px; font-weight: 600; color: #34d399; margin-top: 8px;'>{confidence[1]*100:.0f}%</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Tweet preview
            st.markdown("---")
            with st.expander("📌 Your Tweet Preview", expanded=True):
                st.markdown(f"""
                <div style='
                    background: rgba(255, 255, 255, 0.1);
                    padding: 15px;
                    border-radius: 10px;
                    border-left: 5px solid #06ffa5;
                    color: white;
                    font-size: 16px;
                '>
                {tweet_text}
                </div>
                """, unsafe_allow_html=True)
            
            # Footer
            st.markdown("---")
            st.markdown("""
            <div style='text-align: center; color: #ffffff; font-size: 12px;'>
            💡 Try analyzing different tweets to see how the AI responds!
            </div>
            """, unsafe_allow_html=True)