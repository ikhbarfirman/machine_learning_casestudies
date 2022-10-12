import streamlit as st
import requests
from time import sleep

st.markdown("""<h1 style='text-align: center;'>
    🎼SPOTIFY MUSIC RECOMMENDATION</h1>""",unsafe_allow_html=True)
st.subheader('👈🏽 Input Artists and song title')
st.write('Tap left corner to input for phone browsers ')

with st.expander("See explanation"):
    st.write("""
        This recommendation music system created from spotify music dataset that contains music from year 1921 until 2020.
        It's not quite a large dataset, so there's a possibility you won't get the results from artists and titles you entered.
        Make sure you typed the artist and song title correctly and recommendation search takes about 5 seconds (depends with your connection).
        I just want to share my work to you all and i'm open to any advice and question related to my project thank you.
        
        For more detailed information: https://github.com/ikhbarfirman
    """)
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Spotify_icon.svg/1982px-Spotify_icon.svg.png",width = 100)   

with st.sidebar:
    art_1 = st.text_input('First Artist',value="bts").lower()
    song_1 = st.text_input('Song',value="dynamite").lower()

    with st.spinner("Loading..."):
        sleep(5)
        st.success("Done!")

# inference
URL = "https://backend-spotify-rec.herokuapp.com/predict"
param = {'0': [{'name':song_1,'artist':art_1}]}

def write_rec_song(song_info):
    song_ = song_info['name'].title()
    art_ = song_info['artists'][0].title()
    year_ = song_info['year']
    id_link = 'https://open.spotify.com/track/'+song['id']
    text = art_ + ' - ' + song_ + f' ({year_})'
    return st.markdown(f'[{text}]({id_link})')

def display_rec_art(artist,url,image_link,width):
    out1 = artist.title()
    out2 = f'<img src = "{image_link}" width = "{width}"/>'
    return st.markdown(f"""
    [{out1}]({url})

    [{out2}]({url})
     """,unsafe_allow_html= True)

r = requests.post(URL, json=param)

if r.status_code == 200:
    rec_song, rec_art = r.json()
    st.header('Recommended Songs for You 🎧')
    for song in rec_song:
        write_rec_song(song)

    st.header('Recommended Artist for You 🎶')   
    for artist_info in rec_art:
        artist_ = artist_info['artist'].title()
        artist_url = artist_info['url'] 
        artist_image = artist_info['image']
        display_rec_art(artist_,artist_url,artist_image,100)
        
else:
    st.title("Sorry no results found 😖")
