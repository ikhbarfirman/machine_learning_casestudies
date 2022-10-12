from flask import Flask,jsonify,request
import ast
from random import sample
import pickle
import pandas as pd
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from collections import defaultdict
from scipy.spatial.distance import cdist

#init app
app = Flask(__name__)

def open_scaler(path):
    with open(path,"rb") as modelfile:
        scaler = pickle.load(modelfile)
    return scaler

scaler = open_scaler('scaler.pkl')
feat = ['year','popularity' ,'acousticness', 'danceability', 'energy', 
           'instrumentalness', 'key','liveness','loudness', 'mode', 'speechiness',
           'tempo', 'valence']
data_df = pd.read_csv('data_ready.csv')

def string_list(x):
    return ast.literal_eval(x)

data_df['artists'] = data_df.artists.apply(lambda x: x.lower())
data_df['genres'] = data_df.genres.apply(lambda x: x.lower())
data_df['name'] = data_df.name.apply(lambda x: x.lower())

data_df['artists'] = data_df.artists.apply(string_list)
data_df['genres'] = data_df.genres.apply(string_list)

scaled_data = scaler.transform(data_df[feat])

# Load scaler
with open("id_secret.txt", "r") as f:
    content = f.read()
id_secret = ast.literal_eval(content)

# Setup Spotipy
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=id_secret['id'],
                                                           client_secret=id_secret['secret']))

def find_song(name, artist):
    song_data = defaultdict()
    results = sp.search(q= 'track: {} artist: {}'.format(name,artist), limit=1)
    if results['tracks']['items'] == []:
        return None

    results = results['tracks']['items'][0]
    artist_ = sp.artist(results["artists"][0]["external_urls"]["spotify"])
    
    track_id = results['id']
    audio_features = sp.audio_features(track_id)[0]

    song_data['name'] = [name]
    song_data['artist'] = [artist]
    song_data['year'] = [int(results['album']['release_date'][:3])]
    song_data['genres'] =[artist_['genres']]
    song_data['explicit'] = [int(results['explicit'])]
    song_data['duration_ms'] = [results['duration_ms']]
    song_data['popularity'] = [results['popularity']]

    for key, value in audio_features.items():
        song_data[key] = value

    return pd.DataFrame(song_data)

def get_index_genres(artist,genre): # Define function to get index artist in data_df and genre for that artist
    index = []
    artist_rec = []
    genre = set(genre)
    for i in range(len(data_df)):
        g_data = set(data_df.genres.iloc[i])
        if len(genre.intersection(g_data)) >= 0.5*len(genre): 
            index.append(i)
            art_rec = data_df.artists.iloc[i]
            artist_rec.extend(art_rec)
    artist_rec = set(artist_rec)
    if artist in artist_rec: artist_rec.remove(artist)                    
    return list(set(index)), list(artist_rec)

def get_vector_genre(song_list):
    
    song_vectors = []
    art_genres = []
    
    for song in song_list:
        song_data = find_song(song['name'],song['artist'])
        if song_data is None:
            print('Warning: {} does not exist in Spotify or in database'.format(song['name']))
            continue
        art_genre = song_data[['artist','genres']]
        song_vector = song_data[feat].values
        song_vectors.append(song_vector)
        art_genres.append(art_genre)  
    
    song_matrix = np.array(list(song_vectors))
    genres_matrix = np.array(list(art_genres))
    return song_matrix.reshape(1,-1), np.squeeze(genres_matrix)


def flatten_dict_list(dict_list):
    
    flattened_dict = defaultdict()
    for key in dict_list[0].keys():
        flattened_dict[key] = []
    
    for dictionary in dict_list:
        for key, value in dictionary.items():
            flattened_dict[key].append(value)
            
    return flattened_dict

def get_url_image(artist_list):
    res = []
    for art in artist_list:
        get_info = sp.search(q= f'artist: {art}', limit=1)
        link = get_info['tracks']['items'][0]['artists'][0]['external_urls']['spotify']
        link_img = get_info['tracks']['items'][0]['album']['images'][1]['url']
        res.append({'artist':art,'url':link, 'image':link_img})
    return res        


def recommend_songs(song_list, data, n_songs=3):
    
    metadata_cols = ['name', 'year', 'artists', 'id']
    song_dict = flatten_dict_list(song_list)
    song_matrix,genre_art = get_vector_genre(song_list)
    scaled_data = scaler.transform(data[feat])
    scaled_song_matrix = scaler.transform(song_matrix)
    indek,art_rec = get_index_genres(genre_art[0],genre_art[1])
    
    indeks = []

    distances = cdist(scaled_song_matrix, scaled_data[indek,:], 'cityblock')
    indeks = list(np.argsort(distances)[:, :n_songs][0])
    loc_ = data[feat].iloc[indek].iloc[indeks].index

    if n_songs <= len(art_rec):
        art_rec_show = sample(art_rec,n_songs)
    else:
        art_rec_show = art_rec

    rec_songs = data.loc[loc_]
    rec_songs = rec_songs[~rec_songs['name'].isin(song_dict['name'])]
    return  rec_songs[metadata_cols].to_dict(orient='records'), get_url_image(art_rec_show)


@app.route("/")
def home():
    return "<h1> Berhasil <h1>"

@app.route("/predict", methods=['POST'])

def result():
    args = request.json
    new_data = args['0']
    rec_song,rec_art = recommend_songs(new_data, data_df,3)   
    response = jsonify(rec_song,rec_art)
    return response

#app.run(debug=True)    