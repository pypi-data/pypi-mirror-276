
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
