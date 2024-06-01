from emotion_analysis.data_preprocessing import *


anger_train, anger_dev, anger_data, anger_test = upload_datasets(
    "/home/ahsan-pmylsp/Desktop/Text Emotion Analysis Thesis Paper/emotion_analysis/dataset/EI-oc-En-anger-train.txt",
    "dataset/2018-EI-oc-En-anger-dev.txt",
    "dataset/2018-EI-oc-En-anger-test.txt",
)

fear_train, fear_dev, fear_data, fear_test = upload_datasets(
    "dataset/EI-oc-En-fear-train.txt",
    "dataset/2018-EI-oc-En-fear-dev.txt",
    "dataset/2018-EI-oc-En-fear-test.txt",
)

joy_train, joy_dev, joy_data, joy_test = upload_datasets(
    "dataset/EI-oc-En-joy-train.txt",
    "dataset/2018-EI-oc-En-joy-dev.txt",
    "dataset/2018-EI-oc-En-joy-test.txt",
)

sad_train, sad_dev, sad_data, sad_test = upload_datasets(
    "dataset/EI-oc-En-sadness-train.txt",
    "dataset/2018-EI-oc-En-sadness-dev.txt",
    "dataset/2018-EI-oc-En-sadness-test.txt",
)


# Printing shapes of all datasets
print("anger_train shape:", anger_train.shape)
print("anger_dev shape:", anger_dev.shape)
print("anger_data shape:", anger_data.shape)
print("anger_test shape:", anger_test.shape)
print("fear_train shape:", fear_train.shape)
print("fear_dev shape:", fear_dev.shape)
print("fear_data shape:", fear_data.shape)
print("fear_test shape:", fear_test.shape)
print("joy_train shape:", joy_train.shape)
print("joy_dev shape:", joy_dev.shape)
print("joy_data shape:", joy_data.shape)
print("joy_test shape:", joy_test.shape)
print("sad_train shape:", sad_train.shape)
print("sad_dev shape:", sad_dev.shape)
print("sad_data shape:", sad_data.shape)
print("sad_test shape:", sad_test.shape)