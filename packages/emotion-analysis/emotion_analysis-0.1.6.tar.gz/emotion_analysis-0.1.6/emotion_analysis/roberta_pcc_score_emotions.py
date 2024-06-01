from .frnn import *

print("roberta Vector Process Start")


vector_names = ["Vector_roberta"]
NNeighbours = [
    5,
]  # Number of neighbors to consider
lower = [1] * (NNeighbours[0] // 2)
upper = [1] * (NNeighbours[0] - len(lower))
alpha = 0.5  # Example value for alpha


from sklearn.model_selection import KFold
from scipy.stats import pearsonr


def cross_validation_ensemble_owa(
    data, vector_names, NNeighbours, lower, upper, alpha, cv=5
):
    # Function to calculate PCC score
    def calculate_pcc_score(data_vectors, test_vectors):
        pcc_scores = []
        for data_vector, test_vector in zip(data_vectors, test_vectors):
            if isinstance(data_vector, float) or isinstance(test_vector, float):
                # Skip float values
                continue
            # Convert to numpy arrays if not already
            data_vector = np.array(data_vector)
            test_vector = np.array(test_vector)
            if len(data_vector) == 0 or len(test_vector) == 0:
                # Skip empty vectors
                continue
            pcc_score, _ = pearsonr(data_vector, test_vector)
            pcc_scores.append(pcc_score)
        return pcc_scores

    # Prepare data for cross-validation
    X = data[vector_names]
    y = data["Class"]

    # Initialize lists to store PCC scores
    mean_pcc_scores = []

    # Perform cross-validation
    kf = KFold(n_splits=cv, shuffle=True, random_state=42)
    for train_index, test_index in kf.split(X):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]

        # Calculate PCC scores for each emotion category and vector type
        pcc_scores = []
        for vector_name in vector_names:
            pcc_scores_vector = calculate_pcc_score(
                X_train[vector_name], X_test[vector_name]
            )
            pcc_scores.append(np.mean(pcc_scores_vector))

        mean_pcc_scores.append(pcc_scores)

    # Calculate mean PCC scores for each emotion category and vector type
    mean_pcc_scores = np.mean(mean_pcc_scores, axis=0)

    return mean_pcc_scores
