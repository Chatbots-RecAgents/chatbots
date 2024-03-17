from sklearn.metrics.pairwise import cosine_similarity

def get_similar_profiles(profile_index, df):
    # Making our data set have numerical values
    features = df.drop(columns=['name'])
    
    # Calculate the cosine similarity matrix
    similarity_matrix = cosine_similarity(features)
    
    profile_similarities = similarity_matrix[profile_index]
    
    # Get the indices of the profiles with the highest similarity scores
    # Exclude the first one as it will be the profile itself with a score of 1
    similar_indices = profile_similarities.argsort()[-6:][::-1][1:]
    
    return df['name'].iloc[similar_indices]