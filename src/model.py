import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn import tree, metrics
from typing import Tuple, List, Dict, Optional


class Model:
    """Model object handles data and logic updates separate from the dashboard view"""

    round_digits = 2

    def __init__(self, data_csv: str) -> None:
        """
        Prepare data on instance initialization, uses data frames for easy processing

        Parameters
        ----------
        data_csv
            string with file name of where to load data

        Returns
        ------
        None
        """
        self.data, self.values, self.features = self.load_data(data_csv)
        self.summary = self.summarize_data(self.data)
        self.features_list = list(self.features.columns)
        self.algos = ["Linear Regression", "Decision Tree", "Random Forest"]
        self.model = None

    def load_data(self, data_csv: str) -> pd.DataFrame:
        """
        Load a dataframe from a CSV file and prepare/clean it.

        Parameters
        ----------
        data_csv
            string with file name of where to load data

        Returns
        ------
        pd.DataFrame
            the data after being modified by the preparation pipeline
        """
        # Read the data file
        df = pd.read_csv(data_csv)
        return self.prepare_data(df)

    def prepare_data(
        self, dataframe: pd.DataFrame
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Prepare the raw data to remove outliers, fill missing values etc.
        Also add features to the dataframe computed from raw data and split target value column from features

        Parameters
        ----------
        dataframe
            raw dataframe before processing

        Returns
        ------
        Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]
            Full cleaned dataframe, the single column of target values, the features without the values as a frame
        """
        # Check required columns are present
        required_columns = [
            "total_bedrooms",
            "total_rooms",
            "households",
            "total_bedrooms",
            "population",
            "median_house_value",
        ]
        if not set(required_columns).issubset(dataframe.columns):
            raise Exception(
                "Missing Required Column(s)!",
                set(required_columns).difference(dataframe.columns),
            )

        # Fix Missing Values
        median_beds = dataframe["total_bedrooms"].median()
        dataframe["total_bedrooms"].fillna(median_beds, inplace=True)

        # Add Features
        dataframe["rooms_per_household"] = (
            dataframe["total_rooms"] / dataframe["households"]
        )
        dataframe["bedrooms_per_room"] = (
            dataframe["total_bedrooms"] / dataframe["total_rooms"]
        )
        dataframe["population_per_household"] = (
            dataframe["population"] / dataframe["households"]
        )

        # Separate the target values (outputs) from the features (inputs)
        target_values = dataframe.median_house_value
        features_df = dataframe.drop("median_house_value", axis=1)

        return dataframe, target_values, features_df

    def summarize_data(self, dataframe: pd.DataFrame) -> Dict[str, List[float]]:
        """
        Using aggregation methods, group the data by house age for display in a stacked bar chart

        Parameters
        ----------
        dataframe
            datafrome table to summarize

        Returns
        ------
        Dict[str, List[float]]
            With keys for "young", "medium", "old" groups, list of the average house prices by distance to ocean
        """

        # Check that required columns exist
        if not set(["housing_median_age", "ocean_proximity"]).issubset(
            dataframe.columns
        ):
            return {"young": [], "medium": [], "old": []}

        # Aggregate and average
        young = (
            dataframe.where(dataframe["housing_median_age"] < 15.0)
            .groupby("ocean_proximity")
            .mean()
            .round(self.round_digits)
        )
        medium = (
            dataframe.where(
                (dataframe["housing_median_age"] < 30.0)
                & (dataframe["housing_median_age"] >= 15.0)
            )
            .groupby("ocean_proximity")
            .mean()
            .round(self.round_digits)
        )
        old = (
            dataframe.where(dataframe["housing_median_age"] >= 30.0)
            .groupby("ocean_proximity")
            .mean()
            .round(self.round_digits)
        )

        return {
            "young": young["median_house_value"].tolist(),
            "medium": medium["median_house_value"].tolist(),
            "old": old["median_house_value"].tolist(),
        }

    def fit_model(
        self,
        algorithm: str,
        features_include: List[str],
        random_state: Optional[int] = None,
    ) -> Tuple[pd.DataFrame, pd.DataFrame, float]:
        """
        Create a predictive model based off of algorithm choice and list of features to use

        Parameters
        ----------
        algorithm
            name of the algorithm to use in fitting
        features_include
            list of the features (frame columns) which should be inputs
        random_state
            random state passed to RandomForest training. Use non-None values to get reproducible training outcome

        Returns
        ------
        Tuple[pd.DataFrame, pd.DataFrame, float]
            Single column df of the real values, the single column df of model predictions, r2 metric of accuracy
        """

        # Restrict data frame to the selected features
        features_subset = self.features[features_include]

        # One-Hot Encode categorical column (if present)
        features_encoded = pd.get_dummies(features_subset)

        # Create a model object for the selected algorithm
        if algorithm == "Linear Regression":
            self.model = LinearRegression()
        elif algorithm == "Decision Tree":
            self.model = tree.DecisionTreeRegressor(max_depth=12, max_leaf_nodes=30)
        else:
            self.model = RandomForestRegressor(random_state=random_state)

        # Fit the selected model and make predictions
        self.model.fit(features_encoded, self.values)
        predictions = self.model.predict(features_encoded)
        r2 = metrics.r2_score(predictions, self.values)

        return self.values, predictions, r2
