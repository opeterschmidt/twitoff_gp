import numpy as np
from sklearn.linear_model import LogisticRegression
from .models import User
from .twitter import vectorize_tweet

def predict_user(user0_username, user1_username, hypo_tweet_text):
    """Predict the tweeter from text"""

    # query for users from DB
    user0 = User.query.filter(User.username == user0_username).one()
    user1 = User.query.filter(User.username == user1_username).one()

    # get word embeddings from user's tweets
    user0_vects = np.array([tweet.vect for tweet in user0.tweets])
    user1_vects = np.array([tweet.vect for tweet in user1.tweets])

    # combine their vectorizations into a big X matrix
    X = np.vstack([user0_vects, user1_vects])

    # create some 0s and 1s to generate a y vector
    # 0s at top (first), 1s at bottom (second)
    y = np.concatenate([np.zeros(len(user0.tweets)), 
                        np.ones(len(user1.tweets))])

    # train our logistic regression
    log_reg = LogisticRegression()
    log_reg.fit(X, y)

    # get word embedding for hypo tweeet
    # make sure ebedding is 2D
    hypo_tweet_vect = np.array([vectorize_tweet(hypo_tweet_text)])

    # generate a prediciton
    prediction = log_reg.predict(hypo_tweet_vect)

    # prediciton gets returned as array, here we grab 
    # just the integer from inside the array
    return prediction[0]
    