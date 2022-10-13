# Spotify Music Recommendation 

Created by [Ikhbar Firman](https://github.com/ikhbarfirman)

[Model deployment URL](https://recommendation-music-ikh.herokuapp.com/)
<div align="center">
  <p>
    <a align="center">
      <img width="150" src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Spotify_icon.svg/1982px-Spotify_icon.svg.png""></a>
  </p>
</div>

## About
                                                                                                                                  
Untuk recommendation system yang saya gunakan disini adalah content-based music recommendation system, dimana:

1. Dari input artist dan judul lagu, akan dilakukan filter genres yang sesuai dengan genres artist
2. Mencari distance dari vector 'audio features' input terhadap lagu-lagu di data_df yang genre-nya sesuai.
3. Menampilkan rekomendasi lagu dengan n distance terkecil serta rekomendasi artist dari kesesuaian genre input artist.

Untuk lebih jelasnya dapat dilihat pada notebook **recommendation_spotify.ipynb**                               

### How to USE ??
Please check this [Model deployment URL](https://recommendation-music-ikh.herokuapp.com/) to run the model program
- Silahkan input nama artist dan judul lagu di bagian sidebar sebelah kiri atau tap ujung kiri pada phone browser.
<div align="center">
  <p>
    <a align="center">
      <img width="750" src="https://github.com/ikhbarfirman/machine_learning_casestudies/blob/main/recommendation_spotify_ikh/assets/tutorial.png"></a>
  </p>
</div>                                                                                                                                    
- Durasi pencarian rekomendasi lagu dan artist sekitar 5-8 detik (tergantung koneksi). Kemudian akan keluar hasil rekomendasi artist dan lagu.
<div align="center">
  <p>
    <a align="center">
      <img width="750" src="https://github.com/ikhbarfirman/machine_learning_casestudies/blob/main/recommendation_spotify_ikh/assets/tutorial2.png"></a>
  </p>
</div>

- Pastikan anda memasukkan nama artist dan judul yang sesuai, tidak masalah mengenai huruf besar maupun kecil pada input.                                               
                                                                                                                                                   
- Dataset yang digunakan di model ini tidaklah besar, jadi terdapat kemunngkinan anda tidak menemukan artist dan lagu yang kurang sesuai.                                                                                         
- Klik hasil rekomendasi lagu maupun artist untuk mengunjungi halaman spotify dan langsung mendengarkannya.                                                          

# References
- https://github.com/gabrielfas/songs-clustering-recommendations
- https://www.kaggle.com/code/vatsalmavani/music-recommendation-system-using-spotify-dataset
