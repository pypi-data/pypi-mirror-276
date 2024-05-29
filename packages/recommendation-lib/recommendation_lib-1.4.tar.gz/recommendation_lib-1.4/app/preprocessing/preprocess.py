from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

class Preprocessor:
    def __init__(self, cols, numerical_cols):
        self.cols = cols
        self.numerical_cols = numerical_cols

    def map_categorical(self, df):
        df_selected = df[self.cols]
        
        def map_own_type(x):
            mapping = {'root': 0, 'user': 1}
            return mapping.get(x, x)

        def map_os(x):
            mapping = {'Windows': 0, 'Linux': 1, 'Solaris': 2, 'Android': 3, 'FreeBSD': 4, 'OpenBSD': 5, 'Other': 6}
            return mapping.get(x, x)

        def map_difficulty(x):
            mapping = {'Very Easy': 0, 'Easy': 1, 'Medium': 2, 'Hard': 3, 'Insane': 4}
            return mapping.get(x, x)

        def map_variety(x):
            mapping = {"offensive": 0, "defensive": 1}
            return mapping.get(x, x)

        df_selected['own_type'] = df_selected['own_type'].map(map_own_type)
        df_selected['os'] = df_selected['os'].map(map_os)
        df_selected['difficulty'] = df_selected['difficulty'].map(map_difficulty)
        df_selected['variety'] = df_selected['variety'].map(map_variety)
        return df_selected

    def normalize_numerical_features(self, df):
        """
        Normalize numerical features in a DataFrame using Min-Max scaling.

        Args:
            df (DataFrame): Input DataFrame.

        Returns:
            normalized_df (DataFrame): DataFrame with normalized numerical features.
        """
        scaler = MinMaxScaler()
        df[self.numerical_cols] = scaler.fit_transform(df[self.numerical_cols])
        df = df.loc[:, ~df.columns.duplicated()]
        return df

    def train_test_val_split(self, data, test_size=0.2, validation_size=0.25, random_state=42):
        """
        Perform train-test-validation split on the merged DataFrame.

        Args:
            data (DataFrame): Pandas DataFrame containing the merged data.
            test_size (float): Proportion of the dataset to include in the test split.
            validation_size (float): Proportion of the dataset to include in the validation split.
            random_state (int or None): Seed used by the random number generator.

        Returns:
            train_df (DataFrame): Pandas DataFrame containing the training data.
            test_df (DataFrame): Pandas DataFrame containing the testing data.
            val_df (DataFrame): Pandas DataFrame containing the validation data.
        """
        # Perform train-test-validation split
        train_df, test_validation_df = train_test_split(data, test_size=test_size, random_state=random_state)
        test_df, val_df = train_test_split(test_validation_df, test_size=validation_size / (1 - test_size),
                                           random_state=random_state)

        return train_df, test_df, val_df