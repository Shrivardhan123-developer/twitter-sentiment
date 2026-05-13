import streamlit as st
import pickle
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import re

# ===== PAGE CONFIG =====
st.set_page_config(
    page_title="Twitter Sentiment Analyzer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== CUSTOM CSS =====
st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    [data-testid="stMainBlockContainer"] {
        padding-top: 2rem;
    }
    
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1a1f3a 100%);
        color: #e2e8f0;
    }
    
    /* Header styling */
    h1 {
        background: linear-gradient(135deg, #06b6d4, #fbbf24);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3rem !important;
        font-weight: 800 !important;
        margin-bottom: 1rem !important;
        letter-spacing: -1px;
    }
    
    h2 {
        color: #f1f5f9 !important;
        font-size: 1.8rem !important;
        margin-top: 1.5rem !important;
        margin-bottom: 1rem !important;
    }
    
    h3 {
        color: #cbd5e1 !important;
        font-size: 1.3rem !important;
    }
    
    /* Card styling */
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        color: #06b6d4 !important;
    }
    
    /* Text area styling */
    .stTextArea textarea {
        background-color: #1e293b !important;
        border: 2px solid #334155 !important;
        border-radius: 12px !important;
        color: #e2e8f0 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease;
    }
    
    .stTextArea textarea:focus {
        border-color: #06b6d4 !important;
        box-shadow: 0 0 0 3px rgba(6, 182, 212, 0.1) !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #06b6d4, #fbbf24) !important;
        color: #0f172a !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        padding: 0.75rem 2rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 10px 30px rgba(6, 182, 212, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 15px 40px rgba(6, 182, 212, 0.4) !important;
    }
    
    /* Container styling */
    [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.5rem;
        backdrop-filter: blur(10px);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.8);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        background: transparent;
        border: none;
        padding: 0;
    }
    
    /* Metric cards */
    [data-testid="stMetric"] {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 1.25rem;
        backdrop-filter: blur(10px);
    }
    
    /* Success/Error messages */
    .stSuccess {
        background-color: rgba(34, 197, 94, 0.1) !important;
        border-left: 4px solid #22c55e !important;
        border-radius: 8px !important;
    }
    
    .stError {
        background-color: rgba(239, 68, 68, 0.1) !important;
        border-left: 4px solid #ef4444 !important;
        border-radius: 8px !important;
    }
    
    .stWarning {
        background-color: rgba(251, 191, 36, 0.1) !important;
        border-left: 4px solid #fbbf24 !important;
        border-radius: 8px !important;
    }
    
    /* Sentiment badges */
    .sentiment-positive {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.2), rgba(34, 197, 94, 0.1));
        border: 2px solid #22c55e;
        color: #86efac;
        padding: 1rem;
        border-radius: 12px;
        font-weight: 700;
        font-size: 1.2rem;
        text-align: center;
    }
    
    .sentiment-negative {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.2), rgba(239, 68, 68, 0.1));
        border: 2px solid #ef4444;
        color: #fca5a5;
        padding: 1rem;
        border-radius: 12px;
        font-weight: 700;
        font-size: 1.2rem;
        text-align: center;
    }
    
    .sentiment-neutral {
        background: linear-gradient(135deg, rgba(94, 165, 198, 0.2), rgba(94, 165, 198, 0.1));
        border: 2px solid #5ea5c6;
        color: #7dd3fc;
        padding: 1rem;
        border-radius: 12px;
        font-weight: 700;
        font-size: 1.2rem;
        text-align: center;
    }
    
    /* Table styling */
    [data-testid="stTable"] {
        background: rgba(30, 41, 59, 0.6);
    }
    
    /* Divider */
    hr {
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin: 2rem 0;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(15, 23, 42, 0.5);
    }
    
    ::-webkit-scrollbar-thumb {
        background: #06b6d4;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #0891b2;
    }
</style>
""", unsafe_allow_html=True)

# ===== LOAD MODELS =====
@st.cache_resource
def load_models():
    """Load pre-trained model and vectorizer"""
    try:
        with open('model.pkl', 'rb') as f:
            model = pickle.load(f)
        with open('vectorizer.pkl', 'rb') as f:
            vectorizer = pickle.load(f)
        return model, vectorizer
    except FileNotFoundError:
        st.error("❌ Model files not found! Make sure 'model.pkl' and 'vectorizer.pkl' are in the same directory.")
        st.stop()

# ===== INITIALIZE SESSION STATE =====
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []

# ===== UTILITY FUNCTIONS =====
def preprocess_text(text):
    """Clean and preprocess text"""
    # Remove URLs
    text = re.sub(r'http\S+|www\S+', '', text)
    # Remove mentions and hashtags symbols
    text = re.sub(r'[@#]', '', text)
    # Remove special characters but keep spaces
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Convert to lowercase
    text = text.lower()
    # Remove extra spaces
    text = ' '.join(text.split())
    return text

def get_sentiment_label(prediction):
    """Convert prediction to sentiment label"""
    if prediction == 0:
        return "Negative", "😞", "#ef4444"
    elif prediction == 1:
        return "Neutral", "😐", "#5ea5c6"
    else:
        return "Positive", "😊", "#22c55e"

def get_sentiment_emoji(sentiment):
    """Get emoji based on sentiment"""
    emojis = {
        "Positive": "😊",
        "Negative": "😞",
        "Neutral": "😐"
    }
    return emojis.get(sentiment, "❓")

def analyze_sentiment(text, model, vectorizer):
    """Analyze sentiment of given text"""
    try:
        # Preprocess
        cleaned_text = preprocess_text(text)
        if not cleaned_text:
            return None, "Error: Text is empty after processing"
        
        # Vectorize
        vectorized = vectorizer.transform([cleaned_text])
        
        # Predict
        prediction = model.predict(vectorized)[0]
        confidence = model.predict_proba(vectorized)[0]
        
        sentiment, emoji, color = get_sentiment_label(prediction)
        
        return {
            'sentiment': sentiment,
            'emoji': emoji,
            'color': color,
            'confidence': max(confidence) * 100,
            'all_confidences': {
                'Negative': confidence[0] * 100,
                'Neutral': confidence[1] * 100,
                'Positive': confidence[2] * 100
            }
        }, None
    except Exception as e:
        return None, f"Error: {str(e)}"

# ===== LOAD MODELS =====
model, vectorizer = load_models()

# ===== HEADER =====
col1, col2 = st.columns([4, 1])
with col1:
    st.markdown("# 🎯 Twitter Sentiment Analyzer")
    st.markdown("*Advanced NLP-powered sentiment analysis for real-time tweet insights*")
with col2:
    st.markdown("")
    st.markdown("")
    if st.button("🔄 Refresh", use_container_width=True):
        st.rerun()

st.divider()

# ===== MAIN CONTENT =====
tab1, tab2, tab3 = st.tabs(["📊 Analyzer", "📈 Analytics", "⚙️ About"])

# ===== TAB 1: ANALYZER =====
with tab1:
    col1, col2 = st.columns([2, 1], gap="large")
    
    with col1:
        st.markdown("### Enter Tweet Text")
        tweet_text = st.text_area(
            label="Paste your tweet or text here:",
            placeholder="e.g., 'I absolutely love this product! Best purchase ever!' 💯",
            height=150,
            label_visibility="collapsed"
        )
        
        # Analyze button
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            analyze_button = st.button("🚀 Analyze Sentiment", use_container_width=True)
        with col_btn2:
            clear_button = st.button("🗑️ Clear Text", use_container_width=True)
        
        if clear_button:
            st.rerun()
        
        # Analysis result
        if analyze_button:
            if not tweet_text.strip():
                st.error("⚠️ Please enter some text to analyze!")
            else:
                with st.spinner("🔍 Analyzing sentiment..."):
                    result, error = analyze_sentiment(tweet_text, model, vectorizer)
                    
                    if error:
                        st.error(error)
                    else:
                        # Store in history
                        st.session_state.analysis_history.insert(0, {
                            'text': tweet_text[:100],
                            'sentiment': result['sentiment'],
                            'confidence': result['confidence'],
                            'timestamp': datetime.now()
                        })
                        
                        # Display result
                        st.markdown("---")
                        st.markdown("### 📋 Analysis Result")
                        
                        # Sentiment badge
                        sentiment_class = f"sentiment-{result['sentiment'].lower()}"
                        st.markdown(f"""
                        <div class="{sentiment_class}">
                            {result['emoji']} {result['sentiment'].upper()} 
                            <br>
                            <small>Confidence: {result['confidence']:.1f}%</small>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown("---")
    
    with col2:
        st.markdown("### 📊 Confidence Scores")
        if analyze_button and result:
            # Create confidence chart
            conf_data = pd.DataFrame({
                'Sentiment': list(result['all_confidences'].keys()),
                'Confidence': list(result['all_confidences'].values())
            })
            
            fig = go.Figure(data=[
                go.Bar(
                    x=conf_data['Sentiment'],
                    y=conf_data['Confidence'],
                    marker=dict(
                        color=['#ef4444', '#5ea5c6', '#22c55e'],
                        opacity=0.8
                    ),
                    text=conf_data['Confidence'].round(1),
                    textposition='outside',
                    texttemplate='%{text:.1f}%',
                    hovertemplate='<b>%{x}</b><br>Confidence: %{y:.2f}%<extra></extra>'
                )
            ])
            
            fig.update_layout(
                height=300,
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e2e8f0'),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', range=[0, 100]),
                margin=dict(l=0, r=0, t=0, b=0)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("💡 Analyze a tweet to see confidence scores")

# ===== TAB 2: ANALYTICS =====
with tab2:
    if st.session_state.analysis_history:
        st.markdown("### 📈 Analysis History & Statistics")
        
        # Convert history to DataFrame
        history_df = pd.DataFrame(st.session_state.analysis_history)
        
        # Stats
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total = len(history_df)
            st.metric("📊 Total Analyses", total)
        
        with col2:
            positive = len(history_df[history_df['sentiment'] == 'Positive'])
            st.metric("😊 Positive", positive)
        
        with col3:
            negative = len(history_df[history_df['sentiment'] == 'Negative'])
            st.metric("😞 Negative", negative)
        
        with col4:
            neutral = len(history_df[history_df['sentiment'] == 'Neutral'])
            st.metric("😐 Neutral", neutral)
        
        st.divider()
        
        # Sentiment distribution pie chart
        sentiment_counts = history_df['sentiment'].value_counts()
        colors = {'Positive': '#22c55e', 'Negative': '#ef4444', 'Neutral': '#5ea5c6'}
        color_list = [colors[s] for s in sentiment_counts.index]
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=sentiment_counts.index,
            values=sentiment_counts.values,
            marker=dict(colors=color_list),
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>',
            textposition='inside',
            textinfo='label+percent'
        )])
        
        fig_pie.update_layout(
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0'),
            margin=dict(l=0, r=0, t=0, b=0)
        )
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("##### Sentiment Distribution")
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            st.markdown("##### Confidence Trends")
            avg_confidence = history_df['confidence'].rolling(window=min(5, len(history_df))).mean()
            
            fig_trend = go.Figure()
            fig_trend.add_trace(go.Scatter(
                y=history_df['confidence'],
                mode='lines+markers',
                name='Confidence',
                line=dict(color='#06b6d4', width=2),
                marker=dict(size=6),
                fill='tozeroy',
                fillcolor='rgba(6, 182, 212, 0.1)',
                hovertemplate='Confidence: %{y:.1f}%<extra></extra>'
            ))
            
            fig_trend.update_layout(
                height=400,
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e2e8f0'),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', range=[0, 100]),
                margin=dict(l=0, r=0, t=0, b=0)
            )
            
            st.plotly_chart(fig_trend, use_container_width=True)
        
        st.divider()
        
        # Recent analyses table
        st.markdown("### 📋 Recent Analyses")
        display_df = history_df[['text', 'sentiment', 'confidence']].copy()
        display_df['confidence'] = display_df['confidence'].round(1).astype(str) + '%'
        display_df.columns = ['Tweet Preview', 'Sentiment', 'Confidence']
        
        st.dataframe(
            display_df.head(10),
            use_container_width=True,
            hide_index=True,
            height=400
        )
        
        # Clear history button
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.analysis_history = []
            st.rerun()
    else:
        st.info("💡 No analyses yet. Start analyzing tweets in the 'Analyzer' tab to see statistics!")

# ===== TAB 3: ABOUT =====
with tab3:
    st.markdown("### 📖 About This Application")
    
    st.markdown("""
    #### 🎯 Features
    - **Real-time Sentiment Analysis**: Analyze tweets instantly
    - **Confidence Scores**: See how confident the model is
    - **Analytics Dashboard**: Track sentiment trends over time
    - **Beautiful UI**: Modern, responsive design
    
    #### 🔧 Technology Stack
    - **Machine Learning**: Scikit-learn
    - **NLP**: Text vectorization & preprocessing
    - **Framework**: Streamlit
    - **Visualization**: Plotly
    
    #### 📊 Sentiment Categories
    - **😊 Positive**: Happy, satisfied, supportive tweets
    - **😞 Negative**: Angry, dissatisfied, critical tweets
    - **😐 Neutral**: Informational, factual tweets
    
    #### 💡 How It Works
    1. You input a tweet or text
    2. The app preprocesses the text (cleaning, tokenization)
    3. Text is vectorized using TF-IDF
    4. Machine learning model predicts sentiment
    5. Results with confidence scores are displayed
    
    #### ⚙️ Tips for Best Results
    - Use natural language (avoid too many emojis)
    - Longer texts provide better context
    - Sarcasm might be misclassified
    - Multiple sentences work well
    """)
    
    st.divider()
    
    st.markdown("### 📧 Contact & Support")
    col1, col2 = st.columns(2)
    with col1:
        st.info("👨‍💻 **Developer**: Sachin Ranjan")
    with col2:
        st.info("📧 **Email**: sranjan2219@gmail.com")
    
    st.markdown("""
    ---
    **Made with ❤️ using Streamlit**
    """)