from sklearn.metrics.pairwise import cosine_similarity
from load_data import get_dataset, encode_dataset

def get_similar_profiles(profile_index, path):
    # Load and encode dataset
    df = get_dataset(path)
    df = encode_dataset(df)

    # Making our data set have numerical values
    features = df.drop(columns=['name'])
    
    # Calculate the cosine similarity matrix
    similarity_matrix = cosine_similarity(features)
    
    profile_index = len(df) - 1  # Index of the last response in the DataFrame
    profile_similarities = similarity_matrix[profile_index]
    
    # Get the indices of the profiles with the highest similarity scores
    # Exclude the first one as it will be the profile itself with a score of 1
    similar_indices = profile_similarities.argsort()[-6:][::-1][1:]
    
    #return df['name'].iloc[similar_indices]
    similar_profiles = df['name'].iloc[similar_indices].tolist()
    return f"Based on your interests, you might enjoy interacting with profiles: {', '.join(similar_profiles)}."

#To make it run
# Load and encode dataset
#df = get_dataset('/Users/marianareyes/Documents/GitHub/chatbots/chatbot/data.csv')

#df = encode_dataset(df)
    
# Get similar profiles for the first profile in the DataFrame
#similar_profiles = get_similar_profiles(0, df)
#print(similar_profiles)