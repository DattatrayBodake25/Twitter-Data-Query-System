# Import Flask modules for building the web application
from flask import Flask, request, jsonify

# Import pandas for data manipulation and analysis
import pandas as pd

# Import numpy for numerical operations
import numpy as np

# Import TextBlob for sentiment analysis
from textblob import TextBlob 

# Import regular expressions for text processing
import re  

# Initialize a new Flask application
app = Flask(__name__) 

# Load the TSV file containing Twitter data
df = pd.read_csv('correct_twitter_201904.tsv', sep='\t') 

# Debugging: Print the columns in the DataFrame to verify the structure of the data
# This ensures we are working with the correct columns
print("Columns in DataFrame:", df.columns)  

# Check if 'created_at' column exists, then convert it to datetime format
if 'created_at' in df.columns:
    df['created_at'] = pd.to_datetime(df['created_at'], utc=True)  # Convert 'created_at' to UTC datetime
    df['hour'] = df['created_at'].dt.hour  # Extract the hour from 'created_at' for time-based analysis
else:
    raise KeyError("The 'created_at' column is missing from the DataFrame.")  # Raise an error if the column is missing

# Function to handle different numpy types (integers, floats, arrays) and convert them to native Python types
def convert_numpy_types(obj):
    if isinstance(obj, np.integer):  # If the object is a numpy integer
        return int(obj)  # Convert to Python int
    elif isinstance(obj, np.floating):  # If the object is a numpy float
        return float(obj)  # Convert to Python float
    elif isinstance(obj, np.ndarray):  # If it's a numpy array
        return obj.tolist()  # Convert to a Python list
    else:
        return obj  # Otherwise, return the object as-is

# Function to perform sentiment analysis on a given text using TextBlob
def analyze_sentiment(text):
    analysis = TextBlob(text)  # Create a TextBlob object for sentiment analysis
    if analysis.sentiment.polarity > 0:  # If polarity is positive
        return 'positive'  # Return 'positive'
    elif analysis.sentiment.polarity < 0:  # If polarity is negative
        return 'negative'  # Return 'negative'
    else:  # If polarity is neutral
        return 'neutral'  # Return 'neutral'

# Function to extract hashtags from a given text
def extract_hashtags(text):
    return re.findall(r'#\w+', text)  # Use regular expressions to find all hashtags in the text

# Route for the home page
@app.route('/')
def home():
    # Return a simple welcome message
    return "Welcome to the Twitter Data API!"

# Route to handle search queries for tweets
@app.route('/search', methods=['GET'])
def search_tweets():
    term = request.args.get('term', '')  # Get the search term from the request's query parameters
    if term:  # Proceed if a search term is provided
        # Filter the DataFrame to find tweets containing the search term (case insensitive)
        filtered_data = df[df['text'].str.contains(term, case=False, na=False)].reset_index()

        # Calculate insights from the filtered data
        tweets_per_day = filtered_data['created_at'].dt.date.value_counts().to_dict()  # Count tweets per day
        unique_users = filtered_data['author_id'].nunique()  # Count unique users
        average_likes = filtered_data['like_count'].mean()  # Calculate average likes per tweet
        place_ids = filtered_data['place_id'].dropna().unique().tolist()  # Get unique place IDs
        tweets_per_hour = filtered_data['hour'].value_counts().to_dict()  # Count tweets per hour
        most_tweets_user = filtered_data['author_id'].value_counts().idxmax()  # User with the most tweets
        most_tweets_count = filtered_data['author_id'].value_counts().max()  # Count of tweets by that user

        # Perform sentiment analysis on the filtered tweets
        sentiments = filtered_data['text'].apply(analyze_sentiment)  # Analyze sentiment for each tweet
        sentiment_counts = sentiments.value_counts().to_dict()  # Count positive, negative, neutral sentiments

        # Perform hashtag analysis to find the top hashtags # Top 5 hashtags
        hashtags = filtered_data['text'].apply(extract_hashtags).explode().value_counts().head(5).to_dict()

        # Get the top 5 most active users
        # Count of tweets by top users
        top_users = filtered_data['author_id'].value_counts().head(5).to_dict()

        # Analyze tweet sources (e.g., iPhone, Web, etc.)
        # Count of tweets from different sources
        sources = filtered_data['source'].value_counts().to_dict()  

        # Prepare the response dictionary with all calculated insights
        response = {
            'tweets_per_day': {str(k): int(v) for k, v in tweets_per_day.items()},  # Convert date to string for JSON
            'unique_users': convert_numpy_types(unique_users),  # Convert numpy types to Python native types
            'average_likes': convert_numpy_types(average_likes),  # Same for average likes
            'place_ids': place_ids,  # List of unique place IDs
            'tweets_per_hour': {str(k): int(v) for k, v in tweets_per_hour.items()},  # Convert hours to string
            'most_tweets_user': str(most_tweets_user),  # Convert user ID to string
            'tweet_count': int(most_tweets_count),  # Number of tweets by the most active user
            'sentiment_counts': sentiment_counts,  # Sentiment analysis results
            'top_hashtags': hashtags,  # Top 5 hashtags
            'top_active_users': top_users,  # Top 5 most active users
            'tweet_sources': sources  # Count of tweets from different sources
        }
        return jsonify(response), 200  # Return the response as JSON with status code 200 (OK)
    else:
        return jsonify({'error': 'No search term provided'}), 400  # Return error if no search term is provided

# Main block to run the Flask application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Start the Flask app on the specified host and port
