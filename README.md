# Twitter-Data-Query-System

## Overview
The Twitter Data Query System is a Flask-based web application designed to analyze and query Twitter data from a TSV file. Users can perform searches, retrieve insights, and perform sentiment analysis on tweets.

## Features
- Search for tweets containing specific terms.
- Retrieve insights such as tweet counts per day, unique users, average likes, and more.
- Perform sentiment analysis on tweets.
- Extract hashtags and analyze tweet sources.

## Prerequisites
- Python 3.6 or higher
- Pip (Python package installer)
- Docker (optional, for containerized deployment)

## Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/DattatrayBodake25/Twitter-Data-Query-System.git
cd Twitter-Data-Query-System
```

## Step 2: Install Dependencies
Make sure you have the required Python packages. You can install them using pip. The dependencies are listed in the requirements.txt file.

pip install -r requirements.txt

Step 3: (Optional) Run with Docker
If you prefer to run the application using Docker, ensure you have Docker installed, and then run:

docker-compose up

This will build the Docker container as specified in the Dockerfile and start the Flask application.

Running the Application
To run the application locally, execute:

python app.py

This will start the Flask server, and you can access the application at http://127.0.0.1:5000.

Using the API
Home Page
Visit http://127.0.0.1:5000/ to see a welcome message.

Search Endpoint
You can search for tweets by sending a GET request to the /search endpoint with a query parameter for the search term.

Example:

curl "http://127.0.0.1:5000/search?term=your_search_term"

Replace your_search_term with the term you want to search for.

Response Format
The response will be in JSON format and includes:

tweets_per_day: Count of tweets per day.
unique_users: Number of unique users.
average_likes: Average likes per tweet.
place_ids: List of unique place IDs.
tweets_per_hour: Count of tweets per hour.
most_tweets_user: User ID of the most active user.
tweet_count: Number of tweets by the most active user.
sentiment_counts: Counts of positive, negative, and neutral sentiments.
top_hashtags: Top 5 hashtags.
top_active_users: Top 5 most active users.
tweet_sources: Count of tweets from different sources.
Important Design Choices
Flask Framework: The Flask framework was chosen for its simplicity and flexibility, making it easy to create RESTful APIs.

Data Handling with Pandas: The application uses pandas for efficient data manipulation and analysis, enabling quick filtering and calculations on the dataset.

Sentiment Analysis with TextBlob: TextBlob is used for sentiment analysis due to its simplicity and effectiveness, allowing the application to classify tweets as positive, negative, or neutral.

Regular Expressions for Hashtags: Regular expressions are used to extract hashtags from tweets, providing an efficient way to find patterns in text data.

JSON Responses: The API returns data in JSON format, which is widely used for data interchange and easily consumable by clients.

Conclusion
You now have a fully functional Twitter Data Query System that allows you to analyze tweets and extract meaningful insights. Feel free to explore and modify the code as per your requirements.
