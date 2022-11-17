# Twitter-sentiment-classification

## Table of contents
* [General info](#general-info)
* [In a nutshell](#in-a-nutshell)
* [Technologies](#technologies)
* [Setup](#setup)

## General info
Twitter sentiment analysis using machine learning and natural language processing is a process of extracting information from twitter data and turning it into meaningful insights. This can be used to understand how people feel about a particular topic, product, or brand.

Twitter data is unstructured and contains a lot of noise. This makes it difficult to analyze using traditional methods. Machine learning and natural language processing can be used to overcome these challenges.

Machine learning algorithms can be used to automatically classify tweets as positive, negative, or neutral. Natural language processing can be used to extract features from the tweets such as the sentiment of the words used.

This information can be used to understand how people feel about a particular topic. It can also be used to track the sentiment of a brand over time.

## In a nutshell
We start by creating our machine learning model. The model is built using a pre-trained sentence embeddings based on feed-forward Neural-Net Language Models with pre-built OOV and trained on Google News 7B corpus (7 billion words). Then we add two dense layers of 16 neurons each and an output layer with one neuron and sigmoid activation function. The model takes a batch of sentences in a 1-D tensor of strings as input and encodes each one as a single 50-dimensional vector, then it computes the probability of a positive sentiment. 
 

## Technologies
Project is created with:
* Lorem version: 12.3
* Ipsum version: 2.33
* Ament library version: 999
	
## Setup
To run this project, install it locally using npm:

```
$ cd ../lorem
$ npm install
$ npm start
```