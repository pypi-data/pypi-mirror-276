import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.metrics.pairwise import cosine_similarity

class ContentRecommender:
    def __init__(self, df_encoded):
        self.df_encoded = df_encoded

    def build_user_profile(self, user_id):
        user_data_encoded = self.df_encoded[self.df_encoded['user_uuid'] == user_id]
        user_profile = user_data_encoded.drop(columns=['user_uuid', 'content_name', 'description']).mean()
        return user_profile

    def calculate_similarity(self, user_profile):
        item_profiles = self.df_encoded.drop(columns=['user_uuid', 'content_name', 'description'])
        imputer = KNNImputer(n_neighbors=3)
        df_imputed = pd.DataFrame(imputer.fit_transform(item_profiles), columns=item_profiles.columns)
        similarities = cosine_similarity(user_profile.values.reshape(1, -1), df_imputed)
        return similarities.flatten()

    def recommend_content(self, user_id, top_n=5):
        user_profile = self.build_user_profile(user_id)
        similarities = self.calculate_similarity(user_profile)

        self.df_encoded['similarity'] = similarities
        user_content = self.df_encoded[self.df_encoded['user_uuid'] == user_id]['content_name']

        recommendations = self.df_encoded[~self.df_encoded['content_name'].isin(user_content)]
        recommendations = recommendations.sort_values(by='similarity', ascending=False)

        return recommendations['content_name'].drop_duplicates().head(top_n).values