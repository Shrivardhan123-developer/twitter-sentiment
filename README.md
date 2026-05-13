# 🎯 Twitter Sentiment Analyzer

A professional, feature-rich Streamlit application for real-time Twitter sentiment analysis using machine learning.

![Streamlit](https://img.shields.io/badge/Streamlit-1.40.0-FF4B4B?style=flat-square&logo=streamlit)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-F7931E?style=flat-square)

---

## ✨ Features

✅ **Real-time Sentiment Analysis**
- Analyze any tweet or text instantly
- Support for multiple languages (English)
- Advanced text preprocessing

✅ **Confidence Scores**
- View detailed confidence metrics
- Visual confidence distribution charts
- Track prediction certainty

✅ **Analytics Dashboard**
- Historical analysis tracking
- Sentiment distribution statistics
- Confidence trends visualization
- Recent analyses history

✅ **Beautiful UI**
- Modern, gradient-based design
- Responsive layout
- Interactive visualizations with Plotly
- Smooth animations and transitions
- Dark theme optimized for eyes

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or Download** the project
```bash
# If using git
git clone <your-repo-url>
cd twitter-sentiment-analyzer

# Or simply download and extract the files
```

2. **Create Virtual Environment** (Optional but Recommended)
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Place Model Files**
Make sure these files are in the same directory as `app.py`:
```
├── app.py
├── model.pkl
├── vectorizer.pkl
└── requirements.txt
```

5. **Run the Application**
```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

---

## 📊 How to Use

### 1. **Analyze Tab** 🎯
- Paste your tweet or text in the text area
- Click "🚀 Analyze Sentiment" button
- View instant sentiment analysis with:
  - Sentiment label (Positive/Negative/Neutral)
  - Confidence percentage
  - Confidence score visualization

### 2. **Analytics Tab** 📈
- View historical statistics
- See sentiment distribution (pie chart)
- Track confidence trends
- Browse recent analyses
- Clear analysis history if needed

### 3. **About Tab** ⚙️
- Learn about the application
- Understand sentiment categories
- Get tips for best results
- View technology stack

---

## 🎨 Sentiment Categories

| Sentiment | Emoji | Description |
|-----------|-------|-------------|
| **Positive** | 😊 | Happy, satisfied, supportive, loving tweets |
| **Negative** | 😞 | Angry, dissatisfied, critical, hateful tweets |
| **Neutral** | 😐 | Informational, factual, question tweets |

---

## 🔧 Technical Details

### Model Architecture
- **Vectorizer**: TF-IDF (Term Frequency-Inverse Document Frequency)
- **Algorithm**: Trained ML classifier (Logistic Regression/SVM)
- **Output**: Multi-class classification (3 categories)

### Text Preprocessing
The app automatically:
1. Removes URLs and web links
2. Removes @ mentions and # symbols
3. Cleans special characters
4. Converts to lowercase
5. Removes extra whitespace
6. Handles edge cases

### Confidence Scores
- Returns probability for each sentiment class
- Displayed as percentage (0-100%)
- Helps assess model certainty

---

## 📁 Project Structure

```
twitter-sentiment-analyzer/
│
├── app.py                  # Main Streamlit application
├── model.pkl              # Pre-trained sentiment model
├── vectorizer.pkl         # TF-IDF vectorizer
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

---

## 💻 Requirements

```
streamlit==1.40.0
pandas==2.2.0
numpy==1.24.3
scikit-learn==1.5.0
plotly==5.22.0
```

---

## 🎯 Tips for Best Results

1. **Use Natural Language**
   - ✅ Good: "This product is amazing!"
   - ❌ Avoid: "AMAZINGGGG!!!!!!"

2. **Longer Context**
   - Multi-sentence inputs work better
   - More context = better accuracy

3. **Watch for Sarcasm**
   - Sarcasm might be misclassified
   - Irony can confuse the model

4. **Clean Input**
   - Excessive emojis may affect results
   - URLs are automatically removed

5. **Multiple Analyses**
   - Analyze similar tweets to see patterns
   - Use analytics tab to track trends

---

## 🐛 Troubleshooting

### "Model files not found!"
- Ensure `model.pkl` and `vectorizer.pkl` are in the same directory as `app.py`
- Check file names are exactly correct (case-sensitive)

### "ModuleNotFoundError"
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Verify you're using the correct Python environment

### App runs slowly
- First load takes time to load models (cached after that)
- Try refreshing the page
- Ensure sufficient system resources

### Inaccurate results
- Model trained on Twitter data, works best with tweet format
- Check text preprocessing in code
- Consider retraining with more diverse data

---

## 📈 Performance Metrics

- **Model Accuracy**: [Insert your model's accuracy]
- **Average Response Time**: < 1 second
- **Max Text Length**: No strict limit (preprocessed automatically)
- **Concurrent Users**: Supports multiple simultaneous sessions

---

## 🤝 Contributing

Found a bug? Have suggestions? Feel free to:
1. Report issues
2. Suggest new features
3. Improve documentation
4. Enhance UI/UX

---

## 📄 License

This project is provided as-is for educational and commercial use.

---

## 👨‍💻 About the Developer

**Shrivardhan Tyagi**
- 🎓 B.Tech Computer Science
- 📊 Data Science Enthusiast

📧 **Contact**: shrivardhan@gmail.com

---

## 🌐 Live Demo

[Coming Soon - Will be hosted on Streamlit Cloud]

---

## 📚 Learn More

- [Streamlit Documentation](https://docs.streamlit.io)
- [Scikit-learn Guide](https://scikit-learn.org)
- [Plotly Documentation](https://plotly.com/python)
- [NLP Best Practices](https://github.com/microsoft/nlp)

---

**Made with ❤️ using Streamlit & Machine Learning**

Last Updated: 2026# twitter-sentiment
