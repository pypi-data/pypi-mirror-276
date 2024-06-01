"""TargetGradients: Compute Feature Space to Target Gradients"""

import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler


# Target Gradients Class
class TargetGradients:

    def __init__(self):
        """Initialize the TargetGradients object"""
        self.scalar = StandardScaler()
        self.knn = KNeighborsRegressor(n_neighbors=2, algorithm="ball_tree", metric="euclidean")
        self.df = None

    def compute(
        self,
        input_df: pd.DataFrame,
        features: list,
        target_column: str,
        min_target_distance=0.1,
    ):
        """TargetGradients: Compute Feature Space to Target Gradients

        Args:
             input_df: Pandas DataFrame
             features: List of feature column names
             target_column: Name of the target column
             min_target_distance: Minimum target distance (default: 0.1)
        """

        # Make a copy of the DataFrame
        self.df = input_df.copy()

        # Check for expected columns
        for column in [target_column] + features:
            if column not in self.df.columns:
                print(f"DataFrame does not have required {column} Column!")
                return

        # Check for NaNs in the features and log the percentage
        for feature in features:
            nan_count = self.df[feature].isna().sum()
            if nan_count > 0:
                print(f"Feature '{feature}' has {nan_count} NaNs ({nan_count / len(input_df) * 100:.2f}%).")

        # Impute NaNs with the mean value for each feature
        imputer = SimpleImputer(strategy="mean")
        self.df[features] = imputer.fit_transform(self.df[features])

        # Standardize the features
        X = self.scalar.fit_transform(self.df[features])
        y = self.df[target_column]

        # Fit the KNN model
        self.knn.fit(X, y)

        # Initialize new columns
        self.df["feature_diff"] = float("nan")
        self.df["target_diff"] = float("nan")
        self.df["target_gradient"] = float("nan")

        # Compute the gradients
        for index, row in enumerate(X):
            # Find the nearest neighbors
            distances, indices = self.knn.kneighbors([row], n_neighbors=2)

            # Find the index of the nearest neighbor that is not the observation itself
            nn_index = indices[0][0] if indices[0][0] != index else indices[0][1]

            # Compute the difference in feature space and target space
            feature_diff = distances[0][0] if indices[0][0] != index else distances[0][1]
            target_diff = abs(y[index] - y[nn_index])

            # Calculate the target gradient, handling division by zero
            if feature_diff == 0 and target_diff < min_target_distance:
                target_gradient = 0
            else:
                target_gradient = float("inf") if feature_diff == 0 else target_diff / feature_diff

            # Update the DataFrame
            self.df.at[index, "feature_diff"] = feature_diff
            self.df.at[index, "target_diff"] = target_diff
            self.df.at[index, "target_gradient"] = target_gradient

        return self.df


# Test the TargetGradients Class
def test():
    """Test for the Feature Spider Class"""
    # Set some pandas options
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 1000)

    # Make some fake data
    data = {
        "ID": [
            "id_0",
            "id_1",
            "id_2",
            "id_3",
            "id_4",
            "id_5",
            "id_6",
            "id_7",
            "id_8",
            "id_9",
        ],
        "feat1": [1.0, 1.0, 1.1, 3.0, 4.0, 1.0, 1.0, 1.1, 3.0, 4.0],
        "feat2": [1.0, 1.0, 1.1, 3.0, 4.0, 1.0, 1.0, 1.1, 3.0, 4.0],
        "feat3": [0.1, 0.2, 0.2, 1.6, 2.5, 0.1, 0.3, 0.2, 1.6, 2.5],
        "price": [31, 60, 62, 40, 20, 35, 61, 60, 40, 20],
    }
    data_df = pd.DataFrame(data)

    # Create the class and run the computation
    gradients = TargetGradients()
    data_df = gradients.compute(
        data_df,
        features=["feat1", "feat2", "feat3"],
        target_column="price",
        min_target_distance=1,
    )

    # Print the results
    print(data_df)

    # Plot the results
    # import matplotlib.pyplot as plt

    # Filter out infinity and NaN values
    # finite_gradients = data_df[data_df["target_gradient"].apply(np.isfinite)]
    # finite_gradients.plot.hist(y="target_gradient", bins=20, alpha=0.5)
    # plt.show()


if __name__ == "__main__":
    test()
