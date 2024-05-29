# Emotion Analysis Package

This package provides tools for emotion detection using transformer-based models. It includes functionalities for preprocessing data, generating word clouds, visualizing statistics, and evaluating model performance.

## Installation

To install the package, you can use pip:

`pip install isgc`

## Usage

### Data Preprocessing

First, you need to preprocess your datasets. You can use the `upload_datasets` function to load your data. Here is the full testing code. For example:


```bash
from emotion_analysis.data_preprocessing import *
from emotion_analysis.tweets_embedding import *
from emotion_analysis.frnn import *
from emotion_analysis.bert_pcc_score_emotions import *
from emotion_analysis.roberta_pcc_score_emotions import *

anger_train, anger_dev, anger_data, anger_test = upload_datasets(
    "/home/ahsan-pmylsp/Desktop/frnn_emotion_detection-main/update/Frnn_Emotion/emotion_analysis/dataset/2018-EI-oc-En-anger-dev.txt",
    "/home/ahsan-pmylsp/Desktop/frnn_emotion_detection-main/update/Frnn_Emotion/emotion_analysis/dataset/EI-oc-En-anger-train.txt",
    "/home/ahsan-pmylsp/Desktop/frnn_emotion_detection-main/update/Frnn_Emotion/emotion_analysis/dataset/2018-EI-oc-En-anger-test.txt",
)

fear_train, fear_dev, fear_data, fear_test = upload_datasets(
    "/home/ahsan-pmylsp/Desktop/frnn_emotion_detection-main/update/Frnn_Emotion/emotion_analysis/dataset/EI-oc-En-fear-train.txt",
    "/home/ahsan-pmylsp/Desktop/frnn_emotion_detection-main/update/Frnn_Emotion/emotion_analysis/dataset/2018-EI-oc-En-fear-dev.txt",
    "/home/ahsan-pmylsp/Desktop/frnn_emotion_detection-main/update/Frnn_Emotion/emotion_analysis/dataset/2018-EI-oc-En-fear-test.txt",
)

joy_train, joy_dev, joy_data, joy_test = upload_datasets(
    "/home/ahsan-pmylsp/Desktop/frnn_emotion_detection-main/update/Frnn_Emotion/emotion_analysis/dataset/EI-oc-En-joy-train.txt",
    "/home/ahsan-pmylsp/Desktop/frnn_emotion_detection-main/update/Frnn_Emotion/emotion_analysis/dataset/2018-EI-oc-En-joy-dev.txt",
    "/home/ahsan-pmylsp/Desktop/frnn_emotion_detection-main/update/Frnn_Emotion/emotion_analysis/dataset/2018-EI-oc-En-joy-test.txt",
)

sad_train, sad_dev, sad_data, sad_test = upload_datasets(
    "/home/ahsan-pmylsp/Desktop/frnn_emotion_detection-main/update/Frnn_Emotion/emotion_analysis/dataset/EI-oc-En-sadness-train.txt",
    "/home/ahsan-pmylsp/Desktop/frnn_emotion_detection-main/update/Frnn_Emotion/emotion_analysis/dataset/2018-EI-oc-En-sadness-dev.txt",
    "/home/ahsan-pmylsp/Desktop/frnn_emotion_detection-main/update/Frnn_Emotion/emotion_analysis/dataset/2018-EI-oc-En-sadness-test.txt",
)


generate_wordclouds(anger_train, anger_dev, anger_data, anger_test, "Anger")
plot_statistics(anger_train, anger_dev, anger_data, anger_test, "Anger")
plot_additional_statistics(anger_train, anger_dev, anger_test, "Anger")
plot_top_n_words(anger_train, n=20, title="Top 20 Frequent Words in Anger Train Data")
plot_ngrams_frequency(
    anger_train, n=2, top_n=10, title="Bigram Frequency in Anger Train Data"
)
plot_ngrams_frequency(
    anger_train, n=3, top_n=10, title="Trigram Frequency in Anger Train Data"
)

generate_wordclouds(joy_train, joy_dev, joy_data, joy_test, "Joy")
plot_statistics(joy_train, joy_dev, joy_data, joy_test, "Joy")
plot_additional_statistics(joy_train, joy_dev, joy_test, "Joy")
plot_top_n_words(joy_train, n=20, title="Top 20 Frequent Words in Joy Train Data")
plot_ngrams_frequency(
    joy_train, n=2, top_n=10, title="Bigram Frequency in Joy Train Data"
)
plot_ngrams_frequency(
    joy_train, n=3, top_n=10, title="Trigram Frequency in Joy Train Data"
)

generate_wordclouds(sad_train, sad_dev, sad_data, sad_test, "Sadness")
plot_statistics(sad_train, sad_dev, sad_data, sad_test, "Sadness")
plot_additional_statistics(sad_train, sad_dev, sad_test, "Sadness")
plot_top_n_words(sad_train, n=20, title="Top 20 Frequent Words in Sadness Train Data")
plot_ngrams_frequency(
    sad_train, n=2, top_n=10, title="Bigram Frequency in Sadness Train Data"
)
plot_ngrams_frequency(
    sad_train, n=3, top_n=10, title="Trigram Frequency in Sadness Train Data"
)

generate_wordclouds(fear_train, fear_dev, fear_data, fear_test, "Fear")
plot_statistics(fear_train, fear_dev, fear_data, fear_test, "Fear")
plot_additional_statistics(fear_train, fear_dev, fear_test, "Fear")
plot_top_n_words(fear_train, n=20, title="Top 20 Frequent Words in Fear Train Data")
plot_ngrams_frequency(
    fear_train, n=2, top_n=10, title="Bigram Frequency in Fear Train Data"
)
plot_ngrams_frequency(
    fear_train, n=3, top_n=10, title="Trigram Frequency in Fear Train Data"
)


plot_dataset_statistics([anger_data, joy_data, sad_data, fear_data])

print("vector Bert")

anger_data["Vector_bert"] = anger_data["Tweet"].apply(get_vector_bert)
anger_test["Vector_bert"] = anger_test["Tweet"].apply(get_vector_bert)

joy_data["Vector_bert"] = joy_data["Tweet"].apply(get_vector_bert)
joy_test["Vector_bert"] = joy_test["Tweet"].apply(get_vector_bert)

sad_data["Vector_bert"] = sad_data["Tweet"].apply(get_vector_bert)
sad_test["Vector_bert"] = sad_test["Tweet"].apply(get_vector_bert)

fear_data["Vector_bert"] = fear_data["Tweet"].apply(get_vector_bert)
fear_test["Vector_bert"] = fear_test["Tweet"].apply(get_vector_bert)

print("1st done")

anger_data["Vector_bert_cl"] = anger_data["Cleaned_tweet"].apply(get_vector_bert)
anger_test["Vector_bert_cl"] = anger_test["Cleaned_tweet"].apply(get_vector_bert)

joy_data["Vector_bert_cl"] = joy_data["Cleaned_tweet"].apply(get_vector_bert)
joy_test["Vector_bert_cl"] = joy_test["Cleaned_tweet"].apply(get_vector_bert)

sad_data["Vector_bert_cl"] = sad_data["Cleaned_tweet"].apply(get_vector_bert)
sad_test["Vector_bert_cl"] = sad_test["Cleaned_tweet"].apply(get_vector_bert)

fear_data["Vector_bert_cl"] = fear_data["Cleaned_tweet"].apply(get_vector_bert)
fear_test["Vector_bert_cl"] = fear_test["Cleaned_tweet"].apply(get_vector_bert)

print("2nd done")

# BERT
# With raw tweets

anger_data["Vector_bert_cl_ws"] = anger_data["Cleaned_tweet_wt_stopwords"].apply(
    get_vector_bert
)
anger_test["Vector_bert_cl_ws"] = anger_test["Cleaned_tweet_wt_stopwords"].apply(
    get_vector_bert
)

joy_data["Vector_bert_cl_ws"] = joy_data["Cleaned_tweet_wt_stopwords"].apply(
    get_vector_bert
)
joy_test["Vector_bert_cl_ws"] = joy_test["Cleaned_tweet_wt_stopwords"].apply(
    get_vector_bert
)

sad_data["Vector_bert_cl_ws"] = sad_data["Cleaned_tweet_wt_stopwords"].apply(
    get_vector_bert
)
sad_test["Vector_bert_cl_ws"] = sad_test["Cleaned_tweet_wt_stopwords"].apply(
    get_vector_bert
)

fear_data["Vector_bert_cl_ws"] = fear_data["Cleaned_tweet_wt_stopwords"].apply(
    get_vector_bert
)
fear_test["Vector_bert_cl_ws"] = fear_test["Cleaned_tweet_wt_stopwords"].apply(
    get_vector_bert
)


anger_data["Vector_roberta"] = anger_data["Tweet"].apply(get_vector_roberta)
anger_test["Vector_roberta"] = anger_test["Tweet"].apply(get_vector_roberta)

joy_data["Vector_roberta"] = joy_data["Tweet"].apply(get_vector_roberta)
joy_test["Vector_roberta"] = joy_test["Tweet"].apply(get_vector_roberta)

sad_data["Vector_roberta"] = sad_data["Tweet"].apply(get_vector_roberta)
sad_test["Vector_roberta"] = sad_test["Tweet"].apply(get_vector_roberta)

fear_data["Vector_roberta"] = fear_data["Tweet"].apply(get_vector_roberta)
fear_test["Vector_roberta"] = fear_test["Tweet"].apply(get_vector_roberta)

print("1st done")

anger_data["Vector_roberta_cl"] = anger_data["Cleaned_tweet"].apply(get_vector_roberta)
anger_test["Vector_roberta_cl"] = anger_test["Cleaned_tweet"].apply(get_vector_roberta)

joy_data["Vector_roberta_cl"] = joy_data["Cleaned_tweet"].apply(get_vector_roberta)
joy_test["Vector_roberta_cl"] = joy_test["Cleaned_tweet"].apply(get_vector_roberta)

sad_data["Vector_roberta_cl"] = sad_data["Cleaned_tweet"].apply(get_vector_roberta)
sad_test["Vector_roberta_cl"] = sad_test["Cleaned_tweet"].apply(get_vector_roberta)

fear_data["Vector_roberta_cl"] = fear_data["Cleaned_tweet"].apply(get_vector_roberta)
fear_test["Vector_roberta_cl"] = fear_test["Cleaned_tweet"].apply(get_vector_roberta)

print("2nd done")

# roberta
# With raw tweets

anger_data["Vector_roberta_cl_ws"] = anger_data["Cleaned_tweet_wt_stopwords"].apply(
    get_vector_roberta
)
anger_test["Vector_roberta_cl_ws"] = anger_test["Cleaned_tweet_wt_stopwords"].apply(
    get_vector_roberta
)

joy_data["Vector_roberta_cl_ws"] = joy_data["Cleaned_tweet_wt_stopwords"].apply(
    get_vector_roberta
)
joy_test["Vector_roberta_cl_ws"] = joy_test["Cleaned_tweet_wt_stopwords"].apply(
    get_vector_roberta
)

sad_data["Vector_roberta_cl_ws"] = sad_data["Cleaned_tweet_wt_stopwords"].apply(
    get_vector_roberta
)
sad_test["Vector_roberta_cl_ws"] = sad_test["Cleaned_tweet_wt_stopwords"].apply(
    get_vector_roberta
)

fear_data["Vector_roberta_cl_ws"] = fear_data["Cleaned_tweet_wt_stopwords"].apply(
    get_vector_roberta
)
fear_test["Vector_roberta_cl_ws"] = fear_test["Cleaned_tweet_wt_stopwords"].apply(
    get_vector_roberta
)


anger_pcc_scores = cross_validation_ensemble_owa(
    anger_data.head(10),
    vector_names=["Vector_roberta_cl", "Vector_roberta", "Vector_roberta_cl_ws"],
    NNeighbours=[5, 5],
    lower=[1, 1],
    upper=[1, 1],
    alpha=0.5,
    cv=5,
)
print("anger_PCC Scores:", np.mean(anger_pcc_scores))

joy_pcc_scores = cross_validation_ensemble_owa(
    joy_data.head(10),
    vector_names=["Vector_roberta_cl", "Vector_roberta", "Vector_roberta_cl_ws"],
    NNeighbours=[5, 5],
    lower=[1, 1],
    upper=[1, 1],
    alpha=0.5,
    cv=5,
)
print("joy_PCC Scores:", np.mean(joy_pcc_scores))

fear_pcc_scores = cross_validation_ensemble_owa(
    fear_data.head(10),
    vector_names=["Vector_roberta_cl", "Vector_roberta", "Vector_roberta_cl_ws"],
    NNeighbours=[5, 5],
    lower=[1, 1],
    upper=[1, 1],
    alpha=0.5,
    cv=5,
)
print("fear_PCC Scores:", np.mean(fear_pcc_scores))

sad_pcc_scores = cross_validation_ensemble_owa(
    sad_data.head(10),
    vector_names=["Vector_roberta_cl", "Vector_roberta", "Vector_roberta_cl_ws"],
    NNeighbours=[5, 5],
    lower=[1, 1],
    upper=[1, 1],
    alpha=0.5,
    cv=5,
)
print("sad_PCC Scores:", np.mean(sad_pcc_scores))


anger_pcc_scores = np.mean(anger_pcc_scores)
joy_pcc_scores = np.mean(joy_pcc_scores)
fear_pcc_scores = np.mean(fear_pcc_scores)
sad_pcc_scores = np.mean(sad_pcc_scores)
avg_roberta_emotions_pcc = (
    anger_pcc_scores + joy_pcc_scores + fear_pcc_scores + sad_pcc_scores
) / 4
print("Final PCC Score roberta :", avg_roberta_emotions_pcc)


import os
import matplotlib.pyplot as plt

# Emotion labels
emotion_labels = ["Anger", "Joy", "Fear", "Sadness"]

# Vector types
vector_types = ["Vector_roberta_cl", "Vector_roberta", "Vector_roberta_cl_ws", "bb"]

# Mean PCC scores for each vector type
mean_pcc_scores = [
    np.mean(anger_pcc_scores),
    np.mean(joy_pcc_scores),
    np.mean(fear_pcc_scores),
    np.mean(sad_pcc_scores),
]

plt.figure(figsize=(10, 6))

bars = plt.bar(vector_types, mean_pcc_scores, color="skyblue")

plt.xlabel("Vector Type")
plt.ylabel("Mean PCC Score")
plt.title("Mean PCC Scores for Different Vector Types")
plt.xticks(rotation=45)
plt.grid(axis="y")

# Set the emotion labels as tick labels on the x-axis
plt.xticks(ticks=vector_types, labels=emotion_labels)

# Add value labels on top of each bar
for bar, score in zip(bars, mean_pcc_scores):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.01,
        round(score, 4),
        ha="center",
        va="bottom",
        fontweight="bold",
    )

# Create the directory if it doesn't exist
plots_dir = "plots/roberta_pcc_score"
os.makedirs(plots_dir, exist_ok=True)

# Save the figure
plt.savefig(os.path.join(plots_dir, "roberta_pcc_scores.png"))

print("roberta Base Vector Done!")


anger_pcc_scores = cross_validation_ensemble_owa(
    anger_data.head(10),
    vector_names=["Vector_bert_cl", "Vector_bert", "Vector_bert_cl_ws"],
    NNeighbours=[5, 5],
    lower=[1, 1],
    upper=[1, 1],
    alpha=0.5,
    cv=5,
)
print("anger_PCC Scores:", np.mean(anger_pcc_scores))

joy_pcc_scores = cross_validation_ensemble_owa(
    joy_data.head(10),
    vector_names=["Vector_bert_cl", "Vector_bert", "Vector_bert_cl_ws"],
    NNeighbours=[5, 5],
    lower=[1, 1],
    upper=[1, 1],
    alpha=0.5,
    cv=5,
)
print("joy_PCC Scores:", np.mean(joy_pcc_scores))

fear_pcc_scores = cross_validation_ensemble_owa(
    fear_data.head(10),
    vector_names=["Vector_bert_cl", "Vector_bert", "Vector_bert_cl_ws"],
    NNeighbours=[5, 5],
    lower=[1, 1],
    upper=[1, 1],
    alpha=0.5,
    cv=5,
)
print("fear_PCC Scores:", np.mean(fear_pcc_scores))

sad_pcc_scores = cross_validation_ensemble_owa(
    sad_data.head(10),
    vector_names=["Vector_bert_cl", "Vector_bert", "Vector_bert_cl_ws"],
    NNeighbours=[5, 5],
    lower=[1, 1],
    upper=[1, 1],
    alpha=0.5,
    cv=5,
)
print("sad_PCC Scores:", np.mean(sad_pcc_scores))


anger_pcc_scores = np.mean(anger_pcc_scores)
joy_pcc_scores = np.mean(joy_pcc_scores)
fear_pcc_scores = np.mean(fear_pcc_scores)
sad_pcc_scores = np.mean(sad_pcc_scores)
avg_bert_emotions_pcc = (
    anger_pcc_scores + joy_pcc_scores + fear_pcc_scores + sad_pcc_scores
) / 4
print("Final PCC Score Bert :", avg_bert_emotions_pcc)


import os
import matplotlib.pyplot as plt

# Emotion labels
emotion_labels = ["Anger", "Joy", "Fear", "Sadness"]

# Vector types
vector_types = ["Vector_bert_cl", "Vector_bert", "Vector_bert_cl_ws", "bb"]

# Mean PCC scores for each vector type
mean_pcc_scores = [
    np.mean(anger_pcc_scores),
    np.mean(joy_pcc_scores),
    np.mean(fear_pcc_scores),
    np.mean(sad_pcc_scores),
]

plt.figure(figsize=(10, 6))

bars = plt.bar(vector_types, mean_pcc_scores, color="skyblue")

plt.xlabel("Vector Type")
plt.ylabel("Mean PCC Score")
plt.title("Mean PCC Scores for Different Vector Types")
plt.xticks(rotation=45)
plt.grid(axis="y")

# Set the emotion labels as tick labels on the x-axis
plt.xticks(ticks=vector_types, labels=emotion_labels)

# Add value labels on top of each bar
for bar, score in zip(bars, mean_pcc_scores):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.01,
        round(score, 4),
        ha="center",
        va="bottom",
        fontweight="bold",
    )

# Create the directory if it doesn't exist
plots_dir = "plots/bert_pcc_score"
os.makedirs(plots_dir, exist_ok=True)

# Save the figure
plt.savefig(os.path.join(plots_dir, "bert_pcc_scores.png"))

print("Bert Base Vector Done!")


print(
    "Thanks For Your Patence. Code Run Succesfull Checkout Plot Folder to see Results!"
)

```

## FRNN OWA Weights and PCC Score Calculation

Our package implements the FRNN algorithm with OWA weights for evaluating model performance. Here's a brief overview of how the PCC scores are calculated:

1. **FRNN Algorithm:** The FRNN algorithm is used to predict emotion labels based on the nearest neighbors in the feature space.

2. **OWA Weights:** OWA weights are applied to the nearest neighbors' emotion labels to compute a weighted average. These weights are determined based on the degree of importance assigned to each neighbor.

3. **PCC Score Calculation:** After predicting emotion labels for the test data using the FRNN algorithm, the Pearson Correlation Coefficient (PCC) is calculated to measure the correlation between the predicted and true emotion labels. A higher PCC score indicates better model performance.

For detailed implementation and usage examples, please refer to the documentation and codebase.


## Benefits

### Easy-to-Use

Our package offers a user-friendly interface with simple function calls, making it accessible for both beginners and experienced users.

### Transformer-Based Models

We leverage state-of-the-art transformer-based models for emotion detection, ensuring high accuracy and robust performance.

### Comprehensive Functionality

From data preprocessing to model evaluation, our package provides a wide range of functionalities to streamline the entire process of emotion analysis.

### Visualization Tools

With built-in visualization tools such as word clouds and statistical plots, users can gain insights into their data and model performance at a glance.

### Modular and Extensible

Our package is designed with modularity in mind, allowing users to easily extend its functionality or integrate it into existing workflows.

### Active Development and Support

We are committed to continuously improving our package and providing prompt support to our users through GitHub issues and pull requests.

### Open Source and Free

Our package is open source and freely available under the MIT License, allowing users to use, modify, and distribute it without any restrictions.


## Contact

For any inquiries, feedback, or support requests, please feel free to reach out:

- **Ahsan Tariq**
  - **Email:** ahsantariq0724@email.com
  - **GitHub:** [ahsantariq7](https://github.com/ahsantariq7)
