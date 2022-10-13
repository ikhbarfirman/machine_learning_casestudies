# TELCO CUSTOMERS CHURN PREDICTION!

Created by [Ikhbar Firman](https://github.com/ikhbarfirman)

[Model deployment URL](https://p2ml1-ikhbarfirman.herokuapp.com/)

<div align="center">
  <p>
    <a align="center">
      <img width="450" src="https://www.tibco.com/blog/wp-content/uploads/2013/04/telco-churn.jpg"></a>
  </p>
</div>  

## Problem Statement

Customers churn refers to the amount of customers of a given company that stop using products or services during a certain time frame. At this time Telecom companies face major challenge with customer churn, as customers switch to alternate provider due to various reasons like lower cost, multi (combo) service offerings, marketing promotions by competitors, etc. Identifying these potential customers early on who may voluntarily churn and providing them retention incentives in form of discounts & combo offers will help the organization to retain those customers and reduce revenue loss. 

## Objective
- Predict potential customers who may voluntarily churn

## Data Description
Dataset source: https://www.kaggle.com/datasets/blastchar/telco-customer-churn

- Data consists of 7043 customers who belong to various demographics (single; with dependents; senior citizen) and subscribe to different products offerings (internet service; phone line; streaming TV; streaming movies; online security) from a telecom company located in one of the US states.
- Independent variables: 17 Categorical and 3 Numerical
- Dependent Target variable: “Churn”

<div align="center">
<img src = "https://user-images.githubusercontent.com/108855393/195709754-27720e1b-9f13-42f3-9042-3ac47d93d3f6.png" width = 500\>
</div>

## Process
<div align="center">
<img src = "https://user-images.githubusercontent.com/108855393/195710083-a416a276-2d37-4623-9475-bbdcedba6ac5.png" width = 750\>
</div>

Dari dataset disini kita akan melakukan prediksi terhadap customer terkait kecenderungan customer akan berhenti berlangganan atau tidak. Untuk melakukan prediksi ini diterapkan model ANN sequential API dan functional API dimana kita membuat dua model yang berbeda baik pada sequential dan functional. Prioritas pada prediksi ini adalah meminimalisir jumlah customer yang terprediksi masih loyal sedangkan customer tersebut mempunyai niat untuk berhenti berlangganan, atau dengan kata lain kita ingin membuat jumlah false negative sekecil mungkin (dimana positive disini menandakan customer berhenti berlangganan churn = 'Yes'). Sehingga orientasi saat proses training model mengacu pada recall score, selain itu kita juga mengatur class weight dominan ke kelas 1 (churn = 'Yes') dikarenakan dataset tergolong imbalanced dimana proporsi jumlah customer yang masih loyal lebih banyak dibanding customer yang telah berhenti berlangganan. Konsekuens dari hal tersebut adalah penurunan terhadap precision ataupun jumlah false positive yang meningkat. Hal tersebut menurut saya pribadi tidak menjadi suatu masalah. Anggaplah customer yang terprediksi berhenti berlangganan akan diberlakukan berbagai promosi seperti discount ataupun berbagai benefit tambahan lainnya atau memperbaiki kualitas pelayanan. Customer dengan false positive, atau customer yang terprediksi berhenti berlangganan sedangkan sebenarnya tidak merupakan customer yang beruntung karena dikenakan benefit tersebut. Meskipun mungkin akan terjadi penurunan revenue karena semakin banyak customer yang diterapkan benefit tersesbut, namn secara jangka panjangnya kemungkinan besar perusahaan masih dapat mempertahankan banyak customer untuk tetap berlangganan.

## DEMO PROGRAM!
Please check this [URL model deployment](https://p2ml1-ikhbarfirman.herokuapp.com/) to run the model program
<div align="center">
<img src = "https://user-images.githubusercontent.com/108855393/195710479-107d3ce7-78db-4306-871a-f72fb601694e.png" width = 750\>
</div>
