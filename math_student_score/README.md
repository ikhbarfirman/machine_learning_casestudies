# USING MACHINE LEARNING TO PREDICT MATHEMATICS SCORES ON SECONDARY SCHOOL STUDENT

Created by [Ikhbar Firman](https://github.com/ikhbarfirman)

[Model deployment URL](https://ml2-mathscore-ikhbarfirman.herokuapp.com/)

<div align="center">
  <p>
    <a align="center">
      <img width="550" src="https://odinland.vn/wp-content/uploads/2020/06/29.06-portugal.jpg"></a>
  </p>
</div>  

## Problem Statement

Pendidikan merupakan salah satu faktor kunci untuk mencapai kemajuan ekonomi jangka panjang. Selama beberapa dekade terakhir (sebelum 2008), tingkat pendidikan Portugal menjadi lebih baik. Namun, berdasarkan statistik Portugal tetap masih tertinggal dibanding Eropa karena tingginya kegagalan siswa dan tingkat putus sekolah. Misalnya, pada tahun 2006 rate siswa meninggalkan sekolah dini di Portugal adalah 40% untuk usia 18 hingga 24 tahun, sedangkan rata-rata Uni Eropa nilainya hanya 15% (Eurostat 2007).

Secara khusus, kegagalan di pelajaran inti Matematika dan Bahasa Portugal (Bahasa asal) sangatlah serius, karena kedua pelajaran tersebut dapat memberikan pengetahuan dasar untuk keberhasilan dalam berbagai mata pelajaran lainnya, misalnya fisika atau sejarah (Cortez and Silva 2008).

Terdapat berbagai tindakan untuk mencegah hal tersebut, seperti menerapkan model pembelajaran yang cocok, pengaturan beban tugas ke siswa, mengubah cara pendekatan pada siswa atau pengadaan tambahan jam belajar. Namun tindakan tersebut harus dapat terlaksana terutama sebelum terlaksana ujian. Akan lebih baik apabila guru dapat memperkirakan atau memprediksi skor ujian siswa, untuk segera mengambil tindakan.

### Dapatkah kita memprediksi performa belajar siswa terutama pada pelajaran matematika ??

## Objective
- Pada studi kasus ini akan dilakukan prediksi nilai ujian siswa dari dua sekolah di Portugal yaitu Gabriel Pereira dan Mousinho da Silveira

## Data Description
Dataset source: https://archive.ics.uci.edu/ml/datasets/Student+Performance

Data set yang digunakan untuk pembuatan model prediksi ini adalah data siswa secondary education dari dua sekolah di Portugal yaitu Gabriel Pereira dan Mousinho da Silveira. Berbagai atribut data meliputi nilai ujian matematika, demographic, social dan berbagai informasi yang berkaitan dengan sekolah. Pengambilan data berdasarkan school reports dan kuisioner.

### Predictor Variable
Variables yang digunakan untuk memprediksi nilai ujian siswa: school, sex, age address, dll

### Target
Target variables disini merupakan nilai first period, second priod, dan final grade siswa dari sekolah Gabriel Pereira atau Mousinho da Silveira.
G1 - first period grade (numeric: from 0 to 20)

G2 - second period grade (numeric: from 0 to 20)

G3 - final grade (numeric: from 0 to 20, output target)

## Process
Pada pengerjaan ini akan menerapkan 4 model yang berbeda untuk memprediksi target output G1 dan G2, yaitu:

1. Linear Regression
2. Lasso dan Ridge Regression
3. XGB
4. SVR

Selanjutnya kita akan membuat model untuk predict G3 dengan memasukkan G1 dan G2 sebagai variables input dikarenakan G1 dan G2 mempunyai korelasi yang sangat kuat terhadap G3. Model yang digunakan disini adalah Linear Regression. Dan untuk finalisasinya kita akan memakai hasil predict G1 dan G2 (yang terbaik keempat model) untuk membuat predict G3.

Metrics yang digunakan disini adalah mean_absolute_error, dimana mean_absolute_error akan mencari mean dari absolute difference antara aktual dan prediksi output target.

Untuk informasi lebih detail dapat dilihat pada **h8dsft_Milestone2P1_ikhbar_firman.ipynb**.

## DEMO PROGRAM!
Please check this [URL model deployment](https://ml2-mathscore-ikhbarfirman.herokuapp.com/) to run the model program
<div align="center">
<img src = "https://user-images.githubusercontent.com/108855393/195716413-a0d5ecff-dc75-4e62-bad7-c445a0369b87.png" width = 750\>
</div>
