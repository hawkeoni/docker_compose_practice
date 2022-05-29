# OpenWeb Test Task
Test task for OpenWeb.

## Launch
To launch:
1. Download [classifier.pkl](https://drive.google.com/file/d/1YDIzoUq0pnXmR0ybFnZbbB-qodS3B1tc/view?usp=sharing) and move it to `./static/classifier.pkl`. Download [static.json](https://drive.google.com/file/d/10vbUnZpvBnJXzDMv9cw7YILi4_qpyNaW/view?usp=sharing) and move it to `./static/static.json`.

2. Launch docker:
```bash
docker compose build
docker compose up
```
We will be using default .env file for development from this repo. This is a dev version, files with real secrets should never be commited to a repo.

3. Fake twitter client should be availiable in your browser at [localhost](http://localhost). Dashboard is available on port 8080 and ground truth updater on 8081.

Enjoy your life-feed on Fake Twitter!

## Overview
### Database
A simple postgresql database. I chose postgresql because it's simple and it's better than sqlite, which does not work well with multiple writing connections.

I originally had a dbutils package which contained all the commands for the database interaction, but there was no way to pass it to all the services - I had to make another repo for it, so I cut it into pieces and simply provided only the required functions for the services.

I also considered using SQLAlchemy ORM, but using raw `execute` was just faster for prototyping.

## Fake Twitter
A simple TCP server, which provides access in a Streaming-API pattern. I made this service as a placeholder, as I could not use [tweepy](https://github.com/tweepy/tweepy), because I did not manage to get a Twitter API token to use.

It uses randomness to generate countries, followers, etc and uses real twitter dumps to produce texts.

## Client
A simple client built upon streamlit. Uses sockets to read fake twitter feed from a Streaming API. It sends the data to the classifier and then renders it for the user.

Everything is done server-side, in real applications this would be done via websockets or other technologies working on client-side.

## Dashboard
A small dashboard built on streamlit. Every minute it updates the activity graph & builds a confusion matrix for labeled tweets.

There are a lot of things to monitor, like the percentage of political tweets, different regions, etc but due to time constraints and demonstration purposes this part was left ascetic.

## Classifier
A simple API which serves a linear regression model and writes the results to the database.

## Ground Truth Updater
A simple streamlit UI to update tweet class with ground_truth labels. True labels are stored in the database. They are also used in the dashboard for the generation of confusion matrix

# Data
Data used for training was taken from https://www.kaggle.com/datasets/kaushiksuresh147/political-tweets?resource=download - tweets considered political
https://www.kaggle.com/datasets/kazanova/sentiment140 - tweets from sentiment analysis corpus.

Originally I wanted to scrape twitter API and check for words, but not all political tweets are political, here are some fun examples:

```
Stranger: Where are you from? You: Moscow, Russia. Stranger: Hello comrade Stranger: Give my regards to Putin  ? ??? ????? Omegle 

Going to Jon Corzine's campaign kick off with Joe Biden tomorrow  SO excited

Excited about seeing World Press Photo exhibition when it comes to the United Nations this July! 
```
Unfortunately, the datasets I used were nonetheless connected in the same manner.