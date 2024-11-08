                                                                                                                                                                                                            # Collaborative Filtering Recommendation System
## Outline
## Import Modules
## Import the Dataset
## Explore the Dataset
## Create an Interaction Matrix
## Explore the Interaction Matrix
## Create a Similarity Matrix
## Provide Recommendations
## View the Provided Recommendations
## Create Wrapper Function

## Import Modules
import pandas as pd
import numpy as np
import sklearn
from sklearn.metrics.pairwise import cosine_similarity 

## Import the Dataset
# Load the rating data into a DataFrame
column_names = ['User_ID','User_Names','Movie_ID','Rating','Timestamp']
movies_df = pd.read_csv('Movie_data.csv', sep = ',', names = column_names)

# Load the move information in a DataFrame
movies_title_df = pd.read_csv("Movie_Id_Titles.csv")
movies_title_df.rename(columns = {'item_id': 'Movie_ID', 'title':'Movie_Title'}, inplace = True)

# Merge the DataFrames
movies_df = pd.merge(movies_df, movies_title_df, on = 'Movie_ID')
# View the DataFrame
print(movies_df.head())

## Explore the Dataset
print(f"\n Size of the movie_df dataset is {movies_df.shape}")
# display statistical summary of dataset
movies_df.describe()
# find minimum ratings per user 
movies_df.groupby('User_ID')['Rating'].count().sort_values(ascending = True).head()
# find and store the number of unique users and movies
n_users = movies_df.User_ID.unique().shape[0]
n_movies = movies_df.Movie_ID.unique().shape[0]
print(str(n_users)+ ' users')
print( str(n_movies)+ ' movies')
  
## Create an Interaction Matrix
ratings = np.zeros((n_users, n_movies))

for row in movies_df.itertuples():
    ratings[row[1], row[3]-1] = row[4]

print(ratings)

## Explore the Interaction Matrix
# calculate the sparsity of the interaction matrix
# .shape = (n,m) n is num of row, m is num of column
sparsity = float(len(ratings.nonzero()[0]))
sparsity /= (ratings.shape[0] * ratings.shape[1])
sparsity *= 100
print(sparsity)
  
## Create a Similarity Matrix
# to find the similarity among users
rating_cosine_similarity = cosine_similarity(ratings)
print(rating_cosine_similarity)

## Provide Recommendations
# the system can recommend movies to the users according to thier taste
# a function that receives a user's ID, then give movie recommendations to the user
    # find the k most similar users. assume k=10. 
    # find the average rating of the movies rated by these k users
    # find the top 10 rated movies
def movie_recommender(user_item_m, X_user, user, k=10, top_n=10):
    # get the location of the actual user in the user-item matrix
    # use it to index the user similarity matrix
    user_similarities = X_user[user]
    
    # obtain the indices of the top k most similar users
    most_similar_users = user_item_m.index[user_similarities.argpartition(-k)[-k:]]
    
    # obtain the mean ratings of those users for all movies
    rec_movies = user_item_m.loc[most_similar_users].mean(0).sort_values(ascending = False)
    
    # discard already seen movies
    m_seen_movies = user_item_m.loc[user].gt(0)
    seen_movies = m_seen_movies.index[m_seen_movies].tolist()
    rec_movies = rec_movies.drop(seen_movies).head(top_n)
    
    #return recommendations
    rec_movies_a = rec_movies.index.to_frame().reset_index(drop = True)
    rec_movies_a.rename(columns = {rec_movies_a.columns[0]: 'Movie_ID'}, inplace = True)
    return rec_movies_a

## View the Provided Recommendations
# convert the training matrix to a dataframe expected by the function
ratings_df = pd.DataFrame(ratings)
print(ratings_df)
# call the function
user_ID = 12
movie_recommender(ratings_df, rating_cosine_similarity, user_ID)

## Create Wrapper Function
def movie_recommender_run(user_Name):
  # get ID from Name
  user_ID = movies_df.loc[movies_df['User_Names']== user_Name].User_ID.values[0]
  
  #call the function
  temp = movie_recommender(ratings_df, rating_cosine_similarity, user_ID)
  
  # join with the movie_title_df to get the new movie titles
  top_k_rec = temp.merge(movies_title_df, how= 'inner')
  return top_k_rec
