import pandas as pd
import re
from bs4 import BeautifulSoup
from emoji import demojize
from nltk.corpus import stopwords
import contractions
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
import os
from nltk import ngrams
import nltk

# Download NLTK data if not already downloaded
nltk.download("stopwords")
stop_words = set(stopwords.words("english"))
nltk.download("punkt")

print(
    "EXPAND CONTRACTION, REMOVE HTML TAGS, NON-ASCII, TWEET CLEANING, DATA PREPROCESSING START!"
)


def expand_contractions(text):
    """
    Expand contractions in the text.
    """
    return contractions.fix(text)


print("\n\n Expand Contraction Applying Process End!")


def remove_html_tags(text):
    """
    Remove HTML tags from the text.
    """
    return BeautifulSoup(text, "html.parser").get_text()


print("\n\n Removing HTML tags Applying Process End!")


def remove_non_ascii(text):
    """
    Remove non-ASCII characters from the text.
    """
    return re.sub(r"[^\x00-\x7F]+", "", text)


print("\n\n Removing NON-ASCII Applying Process End!")


def tweet_cleaning(tweet):
    """
    Perform general preprocessing of the tweet, including removing stop words.
    """
    tweet = tweet.replace("\\n", " ")

    tweet = expand_contractions(tweet)
    tweet = remove_html_tags(tweet)
    tweet = remove_non_ascii(tweet)
    tweet = re.sub(r"#|@[^\s]+|https?:\/\/.*[\r\n]*", "", tweet)
    tweet = re.sub(r"\d+", "", tweet)

    smilies = {
        ":)": "smiley",
        ":-)": "smiley",
        ":(": "sad",
        ":/": "skeptical",
        ":D": "laughing",
        ":o": "surprise",
        ":O": "surprise",
    }
    for smile, desc in smilies.items():
        tweet = tweet.replace(smile, desc)

    tweet = demojize(tweet).replace(":", "").replace("_", " ")

    tweet = re.sub(r"[^\w\s]", "", tweet.lower())
    tweet = re.sub(r"\s+", " ", tweet).strip()

    return tweet


print("\n\n Tweet Cleaning Applying Process End!")


def transform_data(file_name):
    """
    Transform the original dataset into a DataFrame suitable for further processing.
    """
    data = pd.read_csv(file_name, sep="\t")
    data["Cleaned_tweet"] = data["Tweet"].apply(tweet_cleaning)
    data["Cleaned_tweet_wt_stopwords"] = data["Cleaned_tweet"].apply(
        lambda x: " ".join([word for word in x.split() if word not in stop_words])
    )
    data["Class"] = data["Intensity Class"].str.split(":").str[0]
    data = data.drop(["Intensity Class", "Affect Dimension"], axis=1)
    return data


def upload_datasets(file_train, file_dev, file_test):
    """
    Compose emotion datasets in DataFrames for train, development, and test sets.
    """
    train_data = transform_data(file_train)
    dev_data = transform_data(file_dev)
    test_data = transform_data(file_test)
    combined_train_data = pd.concat([train_data, dev_data], ignore_index=True)
    return train_data, dev_data, combined_train_data, test_data


def namestr(obj, namespace):
    """
    This function returns the name of 'obj' variable
    Input: obj - any variable, namespace - the namespace setup, we used 'globals()'
    Output: string - the name of 'obj' variable
    """
    return [name for name in namespace if namespace[name] is obj]


def create_wordcloud(text, title=None):
    """
    Create and display a word cloud from the provided text.
    """
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(
        text
    )
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    if title:
        plt.title(title)


plot_dir = "plots"
emotions = ["Anger", "Joy", "Sadness", "Fear"]
for emotion in emotions:
    folder_path = os.path.join(plot_dir, emotion)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def save_plot(plt, filename, folder, subfolder):
    folder_path = os.path.join(plot_dir, folder, subfolder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    filepath = os.path.join(folder_path, filename)
    plt.savefig(filepath)
    plt.close()


def generate_wordclouds(train_data, dev_data, combined_train_data, test_data, emotion):
    """
    Generate and save word clouds for the train, dev, combined train, and test datasets.
    """
    for data, name in zip(
        [train_data, dev_data, combined_train_data, test_data],
        ["Train", "Dev", "Combined_Train", "Test"],
    ):
        create_wordcloud(
            " ".join(data["Cleaned_tweet"]), title=f"{emotion} {name} Data Word Cloud"
        )
        save_plot(
            plt,
            f"{emotion.lower()}_{name.lower()}_wordcloud.png",
            emotion,
            name.lower(),
        )


def plot_statistics(train_data, dev_data, combined_train_data, test_data, emotion):
    """
    Plot advanced statistics including word counts and save the plots.
    """
    datasets = [
        ("Train", train_data),
        ("Dev", dev_data),
        ("Combined Train", combined_train_data),
        ("Test", test_data),
    ]
    for name, data in datasets:
        plt.figure(figsize=(10, 5))
        sns.histplot(
            data["Cleaned_tweet"].apply(lambda x: len(x.split())), bins=30, kde=True
        )
        plt.title(f"{emotion} - Word Count Distribution - {name}")
        plt.xlabel("Word Count")
        plt.ylabel("Frequency")
        save_plot(
            plt,
            f"{emotion.lower()}_{name.lower()}_wordcount_distribution.png",
            emotion,
            name.lower(),
        )

    plt.figure(figsize=(10, 5))
    sns.countplot(data=train_data, x="Class")
    plt.title(f"{emotion} - Class Distribution - Train")
    plt.xlabel("Class")
    plt.ylabel("Frequency")
    save_plot(plt, f"{emotion.lower()}_train_class_distribution.png", emotion, "train")


def plot_additional_statistics(train_data, dev_data, test_data, emotion):
    """
    Plot additional statistics and save the plots.
    """
    plt.figure(figsize=(10, 5))
    sns.histplot(
        train_data["Cleaned_tweet"].apply(len),
        bins=30,
        kde=True,
        color="skyblue",
        label="Train",
    )
    sns.histplot(
        dev_data["Cleaned_tweet"].apply(len),
        bins=30,
        kde=True,
        color="orange",
        label="Dev",
    )
    sns.histplot(
        test_data["Cleaned_tweet"].apply(len),
        bins=30,
        kde=True,
        color="green",
        label="Test",
    )
    plt.title(f"{emotion} - Tweet Length Distribution")
    plt.xlabel("Tweet Length")
    plt.ylabel("Frequency")
    plt.legend()
    save_plot(
        plt, f"{emotion.lower()}_tweet_length_distribution.png", emotion, "additional"
    )

    plt.figure(figsize=(10, 5))
    sns.histplot(
        train_data["Cleaned_tweet_wt_stopwords"].apply(len),
        bins=30,
        kde=True,
        color="skyblue",
        label="Train",
    )
    sns.histplot(
        dev_data["Cleaned_tweet_wt_stopwords"].apply(len),
        bins=30,
        kde=True,
        color="orange",
        label="Dev",
    )
    sns.histplot(
        test_data["Cleaned_tweet_wt_stopwords"].apply(len),
        bins=30,
        kde=True,
        color="green",
        label="Test",
    )
    plt.title(f"{emotion} - Cleaned Tweet Length Distribution without Stopwords")
    plt.xlabel("Cleaned Tweet Length")
    plt.ylabel("Frequency")
    plt.legend()
    save_plot(
        plt,
        f"{emotion.lower()}_cleaned_tweet_length_distribution_without_stopwords.png",
        emotion,
        "additional",
    )


def plot_top_n_words(data, n=10, title=None):
    """
    Plot the top N most frequent words in the dataset.
    """
    word_freq = pd.Series(" ".join(data["Cleaned_tweet"]).split()).value_counts()[:n]
    plt.figure(figsize=(10, 5))
    sns.barplot(
        x=word_freq.values,
        y=word_freq.index,
        hue=word_freq.index,
        legend=False,
        palette="viridis",
    )
    plt.title(title)
    plt.xlabel("Frequency")
    plt.ylabel("Words")
    plt.gca().invert_yaxis()
    save_plot(
        plt,
        f"{title.lower().replace(' ', '_')}_top_{n}_words.png",
        "top_n_words",
        "top_words",
    )


def plot_ngrams_frequency(data, n=2, top_n=10, title=None, emotion=None):
    """
    Plot the frequency of n-grams (bi-grams or tri-grams) in the dataset.
    """
    tokenized_tweets = data["Cleaned_tweet"].apply(lambda x: x.split())
    ngrams_list = [ngrams(tokens, n) for tokens in tokenized_tweets]
    ngrams_flat = [item for sublist in ngrams_list for item in sublist]
    ngrams_freq = pd.Series(ngrams_flat).value_counts()[:top_n]

    plt.figure(figsize=(10, 5))
    sns.barplot(
        x=ngrams_freq.values,
        y=[" ".join(ngram) for ngram in ngrams_freq.index],
        hue=ngrams_freq.index,
        legend=False,
        palette="viridis",
    )
    plt.title(title)
    plt.xlabel("Frequency")
    plt.ylabel(f"{n}-grams")
    plt.gca().invert_yaxis()
    save_plot(
        plt,
        f"{title.lower().replace(' ', '_')}_top_{n}_words.png",
        folder="top_n_words",
        subfolder="top_words",
    )


def calculate_statistics(dataset):
    """
    Calculate imbalance ratio, characteristics, and other useful information for the dataset.
    """
    print("Characteristics of ", namestr(dataset, globals())[0])
    print("Number of instances: ", len(dataset))

    class_sizes = [
        len(dataset[dataset["Class"] == i]) for i in sorted(dataset["Class"].unique())
    ]
    min_size_other_than_zero = min(size for size in class_sizes if size > 0)

    print("Size of the smallest class (excluding class 0): ", min_size_other_than_zero)

    if min_size_other_than_zero > 0:
        imbalance_ratio = round(max(class_sizes) / min_size_other_than_zero, 2)
        print("Imbalance Ratio (IR): ", imbalance_ratio)
    else:
        print(
            "Imbalance Ratio (IR): N/A (Some classes other than 0 have zero instances)"
        )

    print("\n")


def plot_characteristics_and_ir(datasets):
    """
    Plot characteristics and imbalance ratio (IR) for each emotion dataset.
    """
    plt.figure(figsize=(10, 6))
    dataset_names = [namestr(dataset, globals())[0] for dataset in datasets]
    ir_values = [calculate_imbalance_ratio(dataset) for dataset in datasets]

    plt.bar(dataset_names, ir_values, color="skyblue")
    plt.title("Imbalance Ratio (IR) for Different Emotion Datasets")
    plt.xlabel("Dataset")
    plt.ylabel("Imbalance Ratio (IR)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    for i, ir in enumerate(ir_values):
        plt.text(i, ir, str(ir), ha="center", va="bottom")

    plt.savefig("imbalance_ratios_plot.png")
    plt.show()


def calculate_imbalance_ratio(dataset):
    """
    Calculate imbalance ratio (IR) for the dataset.
    """
    class_sizes = [
        len(dataset[dataset["Class"] == i]) for i in sorted(dataset["Class"].unique())
    ]
    min_size_other_than_zero = min(size for size in class_sizes if size > 0)
    if min_size_other_than_zero > 0:
        imbalance_ratio = round(max(class_sizes) / min_size_other_than_zero, 2)
        return imbalance_ratio
    else:
        return None


def plot_dataset_statistics(datasets):
    """
    Plot various statistics for each emotion dataset.
    """
    plt.figure(figsize=(12, 8))

    num_instances = []
    smallest_class_size = []
    imbalance_ratios = []

    for dataset in datasets:
        num_instances.append(len(dataset))
        class_sizes = [
            len(dataset[dataset["Class"] == i])
            for i in sorted(dataset["Class"].unique())
        ]
        min_size_other_than_zero = min(size for size in class_sizes if size > 0)
        if min_size_other_than_zero > 0:
            imbalance_ratio = round(max(class_sizes) / min_size_other_than_zero, 2)
        else:
            imbalance_ratio = None

        smallest_class_size.append(min_size_other_than_zero)
        imbalance_ratios.append(imbalance_ratio)

    plt.subplot(3, 1, 1)
    plt.bar(range(len(datasets)), num_instances, color="skyblue")
    plt.title("Number of Instances in Each Emotion Dataset")
    plt.ylabel("Number of Instances")
    plt.xticks(range(len(datasets)), ["Anger", "Joy", "Sadness", "Fear"])

    plt.subplot(3, 1, 2)
    plt.bar(range(len(datasets)), smallest_class_size, color="orange")
    plt.title("Size of the Smallest Class (Excluding Class 0) in Each Emotion Dataset")
    plt.ylabel("Smallest Class Size")
    plt.xticks(range(len(datasets)), ["Anger", "Joy", "Sadness", "Fear"])

    plt.subplot(3, 1, 3)
    plt.bar(range(len(datasets)), imbalance_ratios, color="green")
    plt.title("Imbalance Ratio (IR) for Each Emotion Dataset")
    plt.ylabel("Imbalance Ratio (IR)")
    plt.xticks(range(len(datasets)), ["Anger", "Joy", "Sadness", "Fear"])

    plt.tight_layout()

    plots_dir = "plots/statistic"
    os.makedirs(plots_dir, exist_ok=True)
    plt.savefig(os.path.join(plots_dir, "dataset_statistics_plot.png"))


print("DATASET STATISTICS PLOT SAVE!")
