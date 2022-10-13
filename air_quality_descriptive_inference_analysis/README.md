# Analisa Kualitas Udara pada Negara Bagian Amerika Serikat

Created by [Ikhbar Firman](https://github.com/ikhbarfirman)

[Model deployment URL](https://frontend-ikhbarp2ml2.herokuapp.com/)

<div align="center">
  <p>
    <a align="center">
      <img width="550" src="https://camo.githubusercontent.com/45ee38bc4f423575c307dd3e769a97276ef2c02fa6c8c809b847351860f09da4/68747470733a2f2f75706c6f61642e77696b696d656469612e6f72672f77696b6970656469612f636f6d6d6f6e732f7468756d622f312f31342f4169725f506f6c6c7574696f6e2d436175736573253236456666656374732e7376672f3130353270782d4169725f506f6c6c7574696f6e2d436175736573253236456666656374732e7376672e706e67"></a>
  </p>
</div>  

## Problem Statement

Kementerian Lingkungan Hidup Amerika Serikat ingin membuat regulasi mengenai emisi industri dan kendaraan bermotor yang kini sangat merusak kualitas udara di negara tersebut. Namun untuk membuat regulasi tersebut, harus diketahui kondisi kualitas udara saat ini di berbagai negara bagian agar mudah menentukan negara bagian mana saja yang harus diterapkan regulasi tersebut terlebih dahulu.

Untuk memantau kondisi kualitas udara yang dihirup manusia, Badan Perlindungan Lingkungan Amerika Serikat (EPA) membuat sebuah ukuran yang disebut Indeks Kualitas Udara atau **Air Quality Index (AQI)** yang menggambarkan konsentrasi polusi udara di satu daerah. Bagi masyarakat umum, AQI dapat berperan sebagai tanda peringatan akan polusi udara yang ikut terhirup sehari-hari. Dengan begitu, kita dapat melakukan langkah mitigasi dan pencegahan. Bagaimanapun, polusi udara yang terakumulasi dalam tubuh dapat berbahaya jika di biarkan dalam jangka panjang

## Objective
1. Mengetahui perubahan kadar tiap pollutant di berbagai tahun
2. Mengetahui hubungan parameter cuaca dengan kadar pollutant
3. Mengetahui negara bagian manakah yang cenderung memiliki kadar pollutant yang besar di berbagai tahun
4. Mengetahui kualitas udara tiap berbagai negara bagian dengan kriteria AQI pada tahun 2021
5. Mengetahui keadaan kualitas udara Amerika Serikat secara keseluruhan pada tahun 2021
6. Mengetahui terdapat pengaruh signifikan antara daerah perkotaan dengan pedesaan.

## Data Description
Data yang digunakan disini didapat dari database 'epa_historical_air_quality' menggunakan bigquery-public-data pada Google Cloud Big Query dengan kriteria sebagai berikut:

- Berisi kolom dengan informasi state name, county name, year, pollutants, units of meassure, annual average pollutant concentatrion, annual average first max pollutant concetration value.
- Parameter Occurrence Code (POC) adalah 1.
- Dari tahun 2011 hingga 2021.

## Data Visualization
Please check this [Dashboard](https://frontend-ikhbarp2ml2.herokuapp.com/)
<div align="center">
<img src = "https://user-images.githubusercontent.com/108855393/195713621-308ab0c1-3d8c-4093-9d4d-c71491d25bfa.png" width = 750\>
</div>

## References
- https://www.idntimes.com/health/fitness/alfonsus-adi-putra-2/memahami-indeks-kualitas-udara-atau-air-quality-index?page=all
- https://www.kcur.org/news/2022-01-31/the-air-in-rural-areas-may-be-just-as-toxic-as-the-pollution-in-cities
- https://www.epa.gov/
- https://www.airnow.gov/sites/default/files/2020-05/aqi-technical-assistance-document-sept2018.pdf
