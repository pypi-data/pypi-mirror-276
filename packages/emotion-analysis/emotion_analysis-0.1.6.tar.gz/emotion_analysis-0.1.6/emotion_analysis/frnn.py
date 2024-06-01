import numpy as np
from scipy.spatial.distance import pdist
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedKFold
import pandas as pd

print("FRNN OWA WEIGHTS Classification And PCC SCORE CALCULATION IMPORT START!")


class CosineKNN:
    """
    K-Nearest Neighbors search with cosine similarity
    """

    def __init__(self, n_neighbors):
        self.n_neighbors = n_neighbors
        self.nbrs = None
        self.scaler = StandardScaler()

    def fit(self, X):
        X_scaled = self.scaler.fit_transform(X)
        self.nbrs = NearestNeighbors(n_neighbors=self.n_neighbors, metric="cosine")
        self.nbrs.fit(X_scaled)
        return self

    def kneighbors(self, X):
        X_scaled = self.scaler.transform(X)
        return self.nbrs.kneighbors(X_scaled)


def frnn_owa_method(train_data, y, test_data, vector_name, NNeighbours, lower, upper):
    def create_X(data, vector_name):
        indexes = list(data.index)
        vector_size = len(data[vector_name][indexes[0]])
        X = np.zeros((len(data), vector_size))
        for k in range(len(indexes)):
            X[k] = data[vector_name][indexes[k]]
        return X

    X_train = create_X(train_data, vector_name)
    X_test = create_X(test_data, vector_name)

    nn_search = CosineKNN(NNeighbours)
    nn_search.fit(X_train)

    distances, indices = nn_search.kneighbors(X_test)

    conf_scores = np.zeros((len(X_test), len(np.unique(y))))
    for i in range(len(X_test)):
        for j in range(NNeighbours):
            neighbor_idx = indices[i][j]
            neighbor_label = y.iloc[neighbor_idx]
            weight = (
                lower[j] if j < (NNeighbours // 2) else upper[j - (NNeighbours // 2)]
            )
            conf_scores[i][neighbor_label] += weight * (1 - distances[i][j])

    conf_scores = conf_scores / np.linalg.norm(conf_scores, axis=1, keepdims=True)
    y_pred = np.argmax(conf_scores, axis=1)

    return conf_scores, y_pred


def weights_sum_test(conf_scores, alpha):
    conf_scores_T = conf_scores.T
    rescaled_scores = [
        (score - 0.5) / alpha for scores in conf_scores_T for score in scores
    ]
    rescaled_sum = [
        sum(rescaled_scores[i : i + len(conf_scores_T)])
        for i in range(0, len(rescaled_scores), len(conf_scores_T))
    ]
    softmax_scores = np.exp(rescaled_sum) / np.sum(np.exp(rescaled_sum), axis=0)
    return softmax_scores


def test_ensemble_confscores(
    train_data, y, test_data, vector_names, NNeighbours, lower, upper, alpha
):
    conf_scores_all = np.zeros((len(vector_names), len(test_data), len(np.unique(y))))
    for j in range(len(vector_names)):
        conf_scores_all[j] = frnn_owa_method(
            train_data, y, test_data, vector_names[j], NNeighbours[j], lower, upper
        )[0]

    rescaled_conf_scores = np.array(
        [
            weights_sum_test(conf_scores_all[:, k, :], alpha)
            for k in range(len(conf_scores_all[0]))
        ]
    )
    y_pred_res = [
        np.argmax(np.average(scores, axis=0, weights=rescaled_conf_scores[i]))
        for i, scores in enumerate(rescaled_conf_scores)
    ]
    return y_pred_res


def test_ensemble_labels(
    train_data, y, test_data, vector_names, NNeighbours, lower, upper
):
    y_pred_ensemble = []
    for i in range(len(test_data)):
        label_counts = {}
        for vector_name in vector_names:
            _, predicted_label = frnn_owa_method(
                train_data,
                y,
                test_data.iloc[[i]],
                vector_name,
                NNeighbours[0],
                lower,
                upper,
            )
            predicted_label = predicted_label[0]
            if predicted_label not in label_counts:
                label_counts[predicted_label] = 0
            label_counts[predicted_label] += 1
        y_pred_ensemble.append(max(label_counts, key=label_counts.get))
    return y_pred_ensemble


def preprocess_data(data, vector_names):
    for vector_name in vector_names:
        data[vector_name] = data[vector_name].apply(
            lambda x: np.nan_to_num(x, nan=np.mean(x))
        )
    return data


def cross_validation_ensemble_owa(
    X_train,
    y_train,
    X_test,
    y_test,
    vector_names,
    NNeighbours,
    lower,
    upper,
    alpha,
    cv=5,
):
    X_train = preprocess_data(X_train.copy(), vector_names)
    X_test = preprocess_data(X_test.copy(), vector_names)

    skf = StratifiedKFold(n_splits=cv, shuffle=True, random_state=42)

    scores = []
    for train_index, test_index in skf.split(X_train, y_train):
        X_train_fold, X_test_fold = X_train.iloc[train_index], X_train.iloc[test_index]
        y_train_fold, y_test_fold = y_train.iloc[train_index], y_train.iloc[test_index]

        y_pred_ensemble = test_ensemble_labels(
            X_train_fold,
            y_train_fold,
            X_test_fold,
            vector_names,
            NNeighbours,
            lower,
            upper,
        )
        accuracy = np.mean(y_test_fold == y_pred_ensemble)
        scores.append(accuracy)

    return np.mean(scores), np.std(scores)


print("FRNN OWA WEIGHTS Classification And PCC SCORE CALCULATION IMPORT SUCCESSFULL!")
