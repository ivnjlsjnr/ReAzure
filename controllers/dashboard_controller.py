from models.dashboard_model import get_quote, analyze_recent_moods

MOOD_KEYWORDS = {
    "Sad": "Pain", "Ecstatic": "Happiness", "Excited": "Dreams",
    "Bored": "Time", "Tired": "Work", "Happy": "Happiness",
    "Calm": "Freedom", "Stressed": "Anxiety", "Worried": "Fear"
}

SUPPORTED_MOODS = [
    "Anger", "Attitude", "Beauty", "Cool", "Courage", "Dating", "Failure", "Faith", "Family", "Fear", "Funny", "Good",
    "Great", "Happiness", "Health", "Imagination", "Inspirational", "Jealousy", "Learning", "Love", "Patience", "Peace",
    "Poetry", "Positive", "Power", "Relationship", "Respect", "Romantic", "Sad", "Smile", "Strength", "Success",
    "Sympathy", "Thankful", "Truth", "Wisdom", "Favorite", "Motivational", "Life", "Morning"
]

MOOD_RECOMMENDATIONS = {
    "Sad": ["Take a short walk", "Call a friend", "Listen to calming music"],
    "Ecstatic": ["Celebrate your wins", "Write what made you feel this way"],
    "Excited": ["Plan your next step", "Capture the moment"],
    "Bored": ["Try a new hobby", "Watch something inspiring"],
    "Tired": ["Rest your eyes", "Take a nap", "Drink water"],
    "Happy": ["Capture it in a journal", "Smile at someone"],
    "Calm": ["Enjoy the moment", "Try meditation"],
    "Stressed": ["Do deep breathing", "Write your thoughts"],
    "Worried": ["List what's controllable", "Talk to someone"]
}

def fetch_quote_by_mood(mood_label):
    keyword = MOOD_KEYWORDS.get(mood_label)
    quote, source = get_quote(keyword)
    return quote, source or "none", keyword or "random"

def fetch_recommendations(mood_label):
    return MOOD_RECOMMENDATIONS.get(mood_label, ["Take care of yourself"])

def get_recent_rating_feedback(user_id: int):
    return analyze_recent_moods(user_id)
