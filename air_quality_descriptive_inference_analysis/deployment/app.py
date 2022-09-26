import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats


data = pd.read_csv('air_quality_annual_summary.csv')
data['mean']= np.abs(data['mean'])

pollutants = ['Ozone','PM2.5 - Local Conditions','PM10 Total 0-10um STP','Carbon monoxide','Sulfur dioxide','Nitrogen dioxide (NO2)']
weather_param = [param for param in data['parameter_name'].unique() if param not  in pollutants]

c = []
for par in data['parameter_name'].unique():
    df = data[(data['parameter_name'] == par)][['mean','year']].groupby('year').mean()
    df.rename(columns={'mean':par},inplace=True)
    c = c + [df]

df_parameter_year = pd.concat(c, axis = 1)

page = st.sidebar.selectbox('Topics', ['Introduction','Kadar Polutan di Berbagai Tahun', 'Korelasi Polutan dan Cuaca','Polutan tiap Negara Bagian', 'Air Quality','Rural vs Urban'])

if page == 'Introduction':
  st.title('Analisa Kualitas Udara pada Negara Bagian Amerika Serikat')
  st.markdown('''
<div>
<center><img src = 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Air_Pollution-Causes%26Effects.svg/1052px-Air_Pollution-Causes%26Effects.svg.png' width="700"/> </center></div>
''', unsafe_allow_html= True)
  st.markdown('''Kementerian Lingkungan Hidup Amerika Serikat ingin membuat regulasi mengenai emisi industri dan kendaraan bermotor yang kini sangat merusak kualitas udara di negara tersebut. 
  Namun untuk membuat regulasi tersebut, harus diketahui kondisi kualitas udara saat ini di berbagai negara bagian agar mudah menentukan negara bagian mana saja yang harus diterapkan regulasi tersebut terlebih dahulu

Untuk memantau kondisi kualitas udara yang dihirup manusia, Badan Perlindungan Lingkungan Amerika Serikat (EPA) membuat sebuah ukuran yang disebut Indeks Kualitas Udara atau **Air Quality Index (AQI)** 
yang menggambarkan konsentrasi polusi udara di satu daerah.

<div>
<center><img src="https://www.epa.gov/sites/default/files/2019-07/aqitableforcourse.png" width="500"/>
</center></div>''', unsafe_allow_html=True)
  

elif page == 'Kadar Polutan di Berbagai Tahun':
    st.title('Polutan US pada Tahun 2011-2021')
    agree = st.checkbox('Tampilkan grafik semua polutan')
    if agree:
        fig, ax = plt.subplots(ncols=2,nrows=3,figsize = (14,14))
        pollutants_arr = np.array([pollutants]).reshape(3,2)
        for rows in range(3):
            for cols in range(2):
                ax[rows,cols].plot(data[data['parameter_name'] == pollutants_arr[rows,cols]][['year','mean']].groupby('year').mean(),c = ((np.cos(rows))**2,(np.sin(cols))**2,(np.cos(cols))**2))
                ax[rows,cols].set_xlabel('Year')
                ax[rows,cols].set_ylabel('Average')
                ax[rows,cols].legend([pollutants_arr[rows,cols]])
        st.pyplot(fig)
    
    pollutant = st.selectbox('Pilih jenis polutan: ',options=pollutants)
    k = pollutants.index(pollutant)
    fig, ax = plt.subplots()
    plt.plot(data[data['parameter_name'] == pollutant][['year','mean']].groupby('year').mean(), c = (0.2*k, (k+1)/15, (k+3)/10))
    plt.xlabel('Year')
    plt.ylabel('Average')
    plt.legend([pollutant])
    st.pyplot(fig)

    st.markdown('''Dapat dilihat kadar tiap polutan mengalami 
      penurunan dalam tiap tahunnya, terutama pada **PM10** yang mengalami penurunan drastis dari tahun 2018 
      ke tahun 2019 dan **CO** dari tahun 2013 ke tahun 2014, yang sebelumnya mengalami kenaikan yang cukup drastis. 
      Apabila kita perhatikan setelah tahun 2019, trends tiap polutan cenderung mulai agak naik, meskipun kenaikan tidak drastis 
      namun hal tersebut mulai harus kita waspadai.''')

elif page == 'Korelasi Polutan dan Cuaca':
    st.title('Korelasi Polutan dan Cuaca')
    st.markdown('''Cuaca dapat memiliki dampak yang signifikan terhadap kualitas udara karena 
    berbagai aspek cuaca mempengaruhi jumlah ozon dan partikulat yang ada di area tertentu.
    Berbagai informasi cuaca yang menjadi pembahasan disini adalah
    **Barometric pressure, Outdoor Temperature, Wind Direction - Resultant, Wind Speed - Resultant, Relative Humidity,
    Dew Point**. Korelasi informasi cuaca dan polutan udara dapat ditampilkan pada gambar berikut.''')
    cor = df_parameter_year.corr().iloc[[0,1,3,5,6,10],[2,4,7,8,9,11]]
    cor_col = cor.columns.tolist()
    cor_row = cor.index.tolist()
    fig, ax = plt.subplots()
    sns.set(rc={'figure.figsize':(8,6)})
    sns.heatmap(cor) #Plot nilai korelasi tersebut
    st.pyplot(fig)
    
    st.markdown('''*Note: Warna semakin terang menunjukkan semakin besar korelasi positif, sedangkan 
    warna semakin gelap menunjukkan semakin besar korelasi negatif.*.''')
    st.write('Untuk lebih jelasnya, data polutan dan informasi cuaca dapat ditampilkan dengan grafik berikut')

    i = st.selectbox('Polutan', options= cor.index)
    j = st.select_slider('Parameter cuaca', options= cor.columns)
    fig= sns.jointplot(data=df_parameter_year, x=j, y=i, kind="reg")
    st.markdown(f'Correlation: {round(cor.iloc[cor_row.index(i),cor_col.index(j)],2)}')
    st.pyplot(fig)
    
    co_2012_2014 = df_parameter_year.iloc[1:4,[3,4,7]]
    co_2012_2014
    st.markdown('''Pada tahun 2012 ke 2013, Outdoor Temperature meningkat, 
      Wind Direction mengalami penurunan, dan Carbon monoxide mengalami peningkatan.
     Pada tahun 2013 ke 2014 terjadi sebaliknya Outdoor Temperature turun, 
     Wind Direction mengalami kenaikan, dan Carbon monoxide mengalami penurunan. 
     Nilai korelasi tiap parameter tersebut dapat membantu kita meninjau perilaku polutan dan info cuaca.''')

elif page == 'Polutan tiap Negara Bagian':
  st.title('Polutan tiap Negara Bagian')
  state_list = data['state_name'].unique().tolist()
  agree = st.checkbox('Tampilkan data untuk seluruh tahun (2017-2021)')

  if agree:
    stack_row = []
    for year in range(2017,2022):
        df_poll_maxmin = pd.DataFrame([],index = [4*[year],['State MAX','MAX Value','State MIN','MIN Value']])
        for pollutant in pollutants:
            data_year = data[(data['parameter_name'] == pollutant) & (data['year'] == year)]
            maks_poll = data_year.iloc[np.argmax(data_year['mean'])][['state_name','mean']].tolist()
            min_poll = data_year.iloc[np.argmin(data_year['mean'])][['state_name','mean']].tolist()
            df_poll_maxmin[pollutant] = maks_poll +min_poll
        stack_row = stack_row + [df_poll_maxmin]
    df_poll = pd.concat(stack_row, axis=0).transpose()
    df_poll

  
  stack_row = []
  year = st.select_slider('Pilih tahun data yang ingin ditampilkan ', options= [k for k in range(2017,2022)])
  df_poll_maxmin = pd.DataFrame([],index = [4*[year],['State MAX','MAX Value','State MIN','MIN Value']])
  for pollutant in pollutants:
    data_year = data[(data['parameter_name'] == pollutant) & (data['year'] == year)]
    maks_poll = data_year.iloc[np.argmax(data_year['mean'])][['state_name','mean']].tolist()
    min_poll = data_year.iloc[np.argmin(data_year['mean'])][['state_name','mean']].tolist()
    df_poll_maxmin[pollutant] = maks_poll +min_poll
  stack_row = stack_row + [df_poll_maxmin]
  df_poll = pd.concat(stack_row, axis=0).transpose()
  df_poll

  st.markdown("""Dari tabel di atas, tampak jelas bahwa dalam 5 tahun terakhir:
1. **Wyoming** selalu memiliki kadar **NO2** terkecil 
2. **Puerto Rico** selalu memiliki kadar **Ozone** terkecil
3. **California** cukup sering memiliki kadar **PM2.5** terbesar
4. **Colorado** selalu memiliki kadar **NO2** terbesar
5. **Missouri** menempati kadar **SO2** tertinggi dalam 3 tahun terakhir
6. **Country Of Mexico** cukup sering memiliki kadar **PM10** terbesar. """)

elif page == 'Air Quality':
  st.title('Kualitas Udara US Tahun 2021')
  st.markdown('''Penilaian kualitas udara biasanya dilakukan dengan berdasarkan **Air quality index (AQI)** dengan ketentuan U.S. 
  Environmental Protection Agency (EPA). Untuk melihat nilai AQI tiap polutan di berbagai negara bagian silahkan
  pilih jenis polutan dibawah berikut.
  
  <center><img src="https://www.epa.gov.tw/File/C8314F72F3092ECE?s=l" width="700"/></center>''', unsafe_allow_html=True)
  

  filter_poll = []
  for i in range(len(data)):
      if data['parameter_name'].iloc[i] in pollutants:
          filter_poll.append(True)
      else: filter_poll.append(False)
  data_pollutant = data[filter_poll]
  data_pollutant_2021 = data_pollutant[data_pollutant['year'] == 2021].groupby(['state_name','parameter_name']).mean()
  
  # O3
  state_o3_list = []
  aqi_o3_list = []
  status_o3_list = []
  for i,j in (data_pollutant_2021.index):
      if j == 'Ozone':
          o3 = data_pollutant_2021.loc[i,j]['mean']
          if o3 <= 0.054:
              aqi_o3 = ((50-0)/(0.054-0))*(o3-0) + 0
              state_o3_list.append(i)
              aqi_o3_list.append(aqi_o3)
              status_o3_list.append('Good')
          elif o3 <= 0.070:
              aqi_o3 = ((100-51)/(0.070-0.055))*(o3-0.055) + 51
              state_o3_list.append(i)
              aqi_o3_list.append(aqi_o3)
              status_o3_list.append('Moderate')
          elif o3 <= 0.085:
              aqi_o3 = ((150-101)/(0.085-0.071))*(o3-0.071) + 101
              state_o3_list.append(i)
              aqi_o3_list.append(aqi_o3)
              status_o3_list.append('Unhealthy for sensitive groups')
          elif o3 <= 0.105:
              aqi_o3 = ((200-151)/(0.105-0.086))*(o3-0.086) + 151
              state_o3_list.append(i)
              aqi_o3_list.append(aqi_o3)
              status_o3_list.append('Unhealthy')
          elif o3 <= 0.200:
              aqi_o3 = ((300-201)/(0.200-0.106))*(o3-0.106) + 201
              state_o3_list.append(i)
              aqi_o3_list.append(aqi_o3)
              status_o3_list.append('Very unhealthy')
          else: print('Apabila O3 lebih besar dari 0.2 harus diperhitungakm dengan pengukuran 1-hour O3 concentrations')
  df_aqi_o3 = pd.DataFrame({'state_name':state_o3_list, 'AQI':aqi_o3_list, 'status':status_o3_list})
  df_aqi_o3.sort_values('AQI', inplace=True)
  
  #CO
  state_co_list = []
  aqi_co_list = []
  status_co_list = []
  for i,j in (data_pollutant_2021.index):
      if j == 'Carbon monoxide':
          co = data_pollutant_2021.loc[i,j]['mean']
          if co <= 4.4:
              aqi_co = ((50-0)/(4.4-0))*(co-0) + 0
              state_co_list.append(i)
              aqi_co_list.append(aqi_co)
              status_co_list.append('Good')
          elif co <= 9.4:
              aqi_co = ((100-51)/(9.4-4.5))*(co-4.5) + 51
              state_co_list.append(i)
              aqi_co_list.append(aqi_co)
              status_co_list.append('Moderate')
          elif co <= 12.4:
              aqi_co = ((150-101)/(12.4-9.5))*(co-9.5) + 101
              state_co_list.append(i)
              aqi_co_list.append(aqi_co)
              status_co_list.append('Unhealthy for sensitive groups')
          elif co <= 15.4:
              aqi_co = ((200-151)/(15.4-12.5))*(co-12.5) + 151
              state_co_list.append(i)
              aqi_co_list.append(aqi_co)
              status_co_list.append('Unhealthy')
          elif co <= 30.4:
              aqi_co = ((300-201)/(30.4-15.5))*(co-0.106) + 201
              state_co_list.append(i)
              aqi_co_list.append(aqi_co)
              status_co_list.append('Very unhealthy')
          elif co <= 40.4:
              aqi_co = ((400-301)/(40.4-30.5))*(co-0.106) + 301
              state_co_list.append(i)
              aqi_co_list.append(aqi_co)
              status_co_list.append('Hazardous I')
          else:
              aqi_co = ((500-401)/(50.4-40.5))*(co-0.106) + 401
              state_co_list.append(i)
              aqi_co_list.append(aqi_co)
              status_co_list.append('Hazardous II')
  df_aqi_co = pd.DataFrame({'state_name':state_co_list, 'AQI':aqi_co_list, 'status':status_co_list})
  df_aqi_co.sort_values('AQI',inplace=True)  
  # SO2
  state_so2_list = []
  aqi_so2_list = []
  status_so2_list = []
  for i,j in (data_pollutant_2021.index):
      if j == 'Sulfur dioxide':
          so2 = data_pollutant_2021.loc[i,j]['mean']
          if so2 <= 35:
              aqi_so2 = ((50-0)/(35-0))*(so2-0) + 0
              state_so2_list.append(i)
              aqi_so2_list.append(aqi_so2)
              status_so2_list.append('Good')
          elif so2 <= 75:
              aqi_so2 = ((100-51)/(75-36))*(so2-36) + 51
              state_so2_list.append(i)
              aqi_so2_list.append(aqi_so2)
              status_so2_list.append('Moderate')
          elif so2 <= 185:
              aqi_so2 = ((150-101)/(185-76))*(so2-9.5) + 101
              state_so2_list.append(i)
              aqi_so2_list.append(aqi_so2)
              status_so2_list.append('Unhealthy for sensitive groups')
          elif so2 <= 304:
              aqi_so2 = ((200-151)/(304-186))*(so2-12.5) + 151
              state_so2_list.append(i)
              aqi_so2_list.append(aqi_so2)
              status_so2_list.append('Unhealthy')
          elif so2 <= 604:
              aqi_so2 = ((300-201)/(604-305))*(so2-0.106) + 201
              state_so2_list.append(i)
              aqi_so2_list.append(aqi_so2)
              status_so2_list.append('Very unhealthy')
          elif so2 <= 804:
              aqi_so2 = ((400-301)/(804-605))*(so2-0.106) + 301
              state_so2_list.append(i)
              aqi_so2_list.append(aqi_so2)
              status_so2_list.append('Hazardous I')
          else:
              aqi_so2 = ((500-401)/(1004-805))*(so2-0.106) + 401
              state_so2_list.append(i)
              aqi_so2_list.append(aqi_so2)
              status_so2_list.append('Hazardous II')
  df_aqi_so2 = pd.DataFrame({'state_name':state_so2_list, 'AQI':aqi_so2_list, 'status':status_so2_list})
  df_aqi_so2.sort_values('AQI', inplace=True)

  # NO2
  state_no2_list = []
  aqi_no2_list = []
  status_no2_list = []
  for i,j in (data_pollutant_2021.index):
      if j == 'Nitrogen dioxide (NO2)':
          no2 = data_pollutant_2021.loc[i,j]['mean']
          if no2 <= 53:
              aqi_no2 = ((50-0)/(53-0))*(no2-0) + 0
              state_no2_list.append(i)
              aqi_no2_list.append(aqi_no2)
              status_no2_list.append('Good')
          elif no2 <= 100:
              aqi_no2 = ((100-51)/(100-54))*(no2-36) + 51
              state_no2_list.append(i)
              aqi_no2_list.append(aqi_no2)
              status_no2_list.append('Moderate')
          elif no2 <= 360:
              aqi_no2 = ((150-101)/(360-101))*(no2-9.5) + 101
              state_no2_list.append(i)
              aqi_no2_list.append(aqi_no2)
              status_no2_list.append('Unhealthy for sensitive groups')
          elif no2 <= 649:
              aqi_no2 = ((200-151)/(649-361))*(no2-12.5) + 151
              state_no2_list.append(i)
              aqi_no2_list.append(aqi_no2)
              status_no2_list.append('Unhealthy')
          elif no2 <= 1249:
              aqi_no2 = ((300-201)/(1249-650))*(no2-0.106) + 201
              state_no2_list.append(i)
              aqi_no2_list.append(aqi_no2)
              status_no2_list.append('Very unhealthy')
          elif no2 <= 1649:
              aqi_no2 = ((400-301)/(1649-1250))*(no2-0.106) + 301
              state_no2_list.append(i)
              aqi_no2_list.append(aqi_no2)
              status_no2_list.append('Hazardous I')
          else:
              aqi_no2 = ((500-401)/(2049-1650))*(no2-0.106) + 401
              state_no2_list.append(i)
              aqi_no2_list.append(aqi_no2)
              status_no2_list.append('Hazardous II')
  
  df_aqi_no2 = pd.DataFrame({'state_name':state_no2_list, 'AQI':aqi_no2_list, 'status':status_no2_list})
  df_aqi_no2.sort_values('AQI',inplace=True)
  
  #PM2.5
  state_pm25_list = []
  aqi_pm25_list = []
  status_pm25_list = []
  for i,j in (data_pollutant_2021.index):
      if j == 'PM2.5 - Local Conditions':
          pm25 = data_pollutant_2021.loc[i,j]['mean']
          if pm25 <= 15.4:
              aqi_pm25 = ((50-0)/(15.4-0))*(pm25-0) + 0
              state_pm25_list.append(i)
              aqi_pm25_list.append(aqi_pm25)
              status_pm25_list.append('Good')
          elif pm25 <= 35.4:
              aqi_pm25 = ((100-51)/(35.4-15.4))*(pm25-36) + 51
              state_pm25_list.append(i)
              aqi_pm25_list.append(aqi_pm25)
              status_pm25_list.append('Moderate')
          elif pm25 <= 54.4:
              aqi_pm25 = ((150-101)/(54.4-35.5))*(pm25-9.5) + 101
              state_pm25_list.append(i)
              aqi_pm25_list.append(aqi_pm25)
              status_pm25_list.append('Unhealthy for sensitive groups')
          elif pm25 <= 150.4:
              aqi_pm25 = ((200-151)/(150.4-54.5))*(pm25-12.5) + 151
              state_pm25_list.append(i)
              aqi_pm25_list.append(aqi_pm25)
              status_pm25_list.append('Unhealthy')
          elif pm25 <= 250.4:
              aqi_pm25 = ((300-201)/(250.4-150.5))*(pm25-0.106) + 201
              state_pm25_list.append(i)
              aqi_pm25_list.append(aqi_pm25)
              status_pm25_list.append('Very unhealthy')
          elif pm25 <= 350.4:
              aqi_pm25 = ((400-301)/(350.4-250.5))*(pm25-0.106) + 301
              state_pm25_list.append(i)
              aqi_pm25_list.append(aqi_pm25)
              status_pm25_list.append('Hazardous I')
          else:
              aqi_pm25 = ((500-401)/(500.4-350.5))*(pm25-0.106) + 401
              state_pm25_list.append(i)
              aqi_pm25_list.append(aqi_pm25)
              status_pm25_list.append('Hazardous II')
  df_aqi_pm25 = pd.DataFrame({'state_name':state_pm25_list, 'AQI':aqi_pm25_list, 'status':status_pm25_list})
  df_aqi_pm25.sort_values('AQI',inplace=True)

  #PM10
  state_pm10_list = []
  aqi_pm10_list = []
  status_pm10_list = []
  for i,j in (data_pollutant_2021.index):
      if j == 'PM10 Total 0-10um STP':
          pm10 = data_pollutant_2021.loc[i,j]['mean']
          if pm10 <= 54:
              aqi_pm10 = ((50-0)/(54-0))*(pm10-0) + 0
              state_pm10_list.append(i)
              aqi_pm10_list.append(aqi_pm10)
              status_pm10_list.append('Good')
          elif pm10 <= 125:
              aqi_pm10 = ((100-51)/(125-55))*(pm10-36) + 51
              state_pm10_list.append(i)
              aqi_pm10_list.append(aqi_pm10)
              status_pm10_list.append('Moderate')
          elif pm10 <= 254:
              aqi_pm10 = ((150-101)/(254-126))*(pm10-9.5) + 101
              state_pm10_list.append(i)
              aqi_pm10_list.append(aqi_pm10)
              status_pm10_list.append('Unhealthy for sensitive groups')
          elif pm10 <= 354:
              aqi_pm10 = ((200-151)/(354-255))*(pm10-12.5) + 151
              state_pm10_list.append(i)
              aqi_pm10_list.append(aqi_pm10)
              status_pm10_list.append('Unhealthy')
          elif pm10 <= 424:
              aqi_pm10 = ((300-201)/(424-355))*(pm10-0.106) + 201
              state_pm10_list.append(i)
              aqi_pm10_list.append(aqi_pm10)
              status_pm10_list.append('Very unhealthy')
          elif pm10 <= 504:
              aqi_pm10 = ((400-301)/(504-425))*(pm10-0.106) + 301
              state_pm10_list.append(i)
              aqi_pm10_list.append(aqi_pm10)
              status_pm10_list.append('Hazardous I')
          else:
              aqi_pm10 = ((500-401)/(604-505))*(pm10-0.106) + 401
              state_pm10_list.append(i)
              aqi_pm10_list.append(aqi_pm10)
              status_pm10_list.append('Hazardous II')
  df_aqi_pm10 = pd.DataFrame({'state_name':state_pm10_list, 'AQI':aqi_pm10_list, 'status':status_pm10_list})
  df_aqi_pm10.sort_values('AQI', inplace=True)


  st.header('AQI Setiap Polutan')
  poll_df = {'Carbon monoxide':df_aqi_co,'Nitrogin dioxide':df_aqi_no2, 'Ozone':df_aqi_o3,
  'Sulfur dioxide':df_aqi_so2,'PM10':df_aqi_pm10,'PM2.5':df_aqi_pm25}
  pp = ['Carbon monoxide','Nitrogin dioxide','Ozone','Sulfur dioxide','PM10','PM2.5']
  #list_pol_df = [df_aqi_co,df_aqi_no2,df_aqi_o3,df_aqi_so2,df_aqi_pm10,df_aqi_pm25]
  pol = st.selectbox('Pilih jenis polutan', options = pp)
  fig, ax = plt.subplots()
  sns.set(rc={'figure.figsize':(15,8)})
  sns.barplot(x='state_name',y='AQI',data= poll_df[pol])
  plt.xticks(rotation=90)
  plt.xlabel('State')
  plt.ylabel('AQI')
  plt.title('AQI 2021')
  st.pyplot(fig)
  plt.show()

  df_mergeaqi = pd.merge(df_aqi_co, df_aqi_no2, how='outer', on='state_name').merge(df_aqi_o3, how='outer',on='state_name').merge(df_aqi_so2,how='outer',on='state_name').merge(df_aqi_pm10,how='outer',on='state_name').merge(df_aqi_pm25, how='outer',on='state_name')
  df_mergeaqi.columns = ['state_name', 'CO_AQI', 'status_x', 'NO2_AQI', 'status_y', 'O3_AQI',
       'status_x', 'SO2_AQI', 'status_y', 'PM10_AQI', 'status_x', 'PM25_AQI',
       'status_y']
  df_mergeaqi = df_mergeaqi[['state_name','CO_AQI','NO2_AQI','O3_AQI','SO2_AQI','PM10_AQI','PM25_AQI']]
  df_mergeaqi.dropna(inplace=True)
  df_mergeaqi['Total_AQI'] = df_mergeaqi.mean(axis = 1) 
  df_mergeaqi.sort_values('Total_AQI')

  st.header('Total AQI Keseluruhan')
  st.markdown('Nilai total AQI disini didapat dengan mencari rata-rata dari AQI semua polutan.')
  agree = st.checkbox('Tampilkan data Total AQI')

  if agree:
    df_mergeaqi
  
  fig, ax = plt.subplots()
  sns.histplot(df_mergeaqi['Total_AQI'], kde=True)
  plt.axvline(df_mergeaqi['Total_AQI'].mean(), linewidth = 3, linestyle='dashed',color = 'red', label='mean')
  plt.axvline(df_mergeaqi['Total_AQI'].median(), linewidth = 3, linestyle='dashed',color = 'green',label='median')
  plt.title('AQI US 2021')
  plt.xlabel('Total AQI')
  plt.legend()
  st.pyplot(fig)

  statistik = st.checkbox('Tampilkan statistik data')
  
  if statistik:
    st.write(f'Mean: {round(df_mergeaqi["Total_AQI"].mean(),2)}')
    st.write(f'Median: {round(df_mergeaqi["Total_AQI"].median(),2)}')
    st.write(f'Standard deviation: {round(df_mergeaqi["Total_AQI"].std(),2)}')
    st.write(f'Skewness: {round(df_mergeaqi["Total_AQI"].skew(),2)}')
  
  st.markdown('''Berdasarkan data, dapat kita lihat **Total AQI** terbesar adalah **Nevada**, 
  sedangkan **Total AQI** terkecil adalah **Hawaii**. 
  Ada beberapa negara bagian (tidak tertampil di data) yang juga patut diperhitungkan seperti **Puerto Rico** yang memiliki AQI masing-masing polutan yang cukup kecil,
   serta **Idaho** yang memiliki AQI masing-masing polutan yang cukup besar. Namun apabila kita perhatikan nilai AQI ozone dan PM lebih tinggi dari nilai AQI polutan yang lain.
   Walaupun secara keseluruhan AQI negara bagian US masuk dalam kategori *GOOD* namun pemerintah perlu waspada akan polutan PM dan Ozone. ''')


elif page == 'Rural vs Urban':
  st.title('URBAN vs RURAL')
  st.markdown(r'''
  Dalam mencari perbedaan pollutant tahun 2021 pada urban area dengan rural area, 
  akan diambil data polutan dari sebagian negara bagian masing-masing. Rural $X_1$ sampel: Mississippi, Vermont, Montana,Wyoming, dan Maine.
  Urban $X_2$ sampel: California, Texas, New Jersey, Nevada, dan Florida. 
   
  Kemudian dilakukan uji hipotesis yang dilakukan adalah **Two Samples Independent Two Tailed Hypothesis testing** dengan significance level pada pengujian ini sebesar 0.05, dan kriteria pengambilan keputusan adalah:
- Accept $H_0$ apabila *p-value* $>0.05$
- Reject $H_0$ apabila *p-value* $<0.05$

Hipotesis dalam kasus disini adalah:

$H_0:\mu_1=\mu_2$

$H_1:\mu_1 \neq \mu_2$''')
  st.markdown('''Data sampel rural memiliki mean 4.37, sedangkan mean urban sampel adalah 6.07. 
    Distribusi selisih kedua nilai sampel atau $X_1-X_2$ tersebut dapat ditampilkan pada grafik berikut.''')

  filter_poll = []
  for i in range(len(data)):
    if data['parameter_name'].iloc[i] in pollutants:
      filter_poll.append(True)
    else: filter_poll.append(False)
  data_pollutant = data[filter_poll]
  data_pollutant_2021 = data_pollutant[data_pollutant['year'] == 2021].groupby(['state_name','parameter_name']).mean()
  filter_urban2021 = ((data_pollutant['state_name'] == 'California') |(data_pollutant['state_name'] == 'Texas') |(data_pollutant['state_name'] == 'New Jersey') |(data_pollutant['state_name'] == 'Florida')|(data_pollutant['state_name'] == 'Nevada')) & (data_pollutant['year'] == 2021)
  data_urban2021 = data_pollutant[filter_urban2021][['state_name','parameter_name','mean']]
  filter_rural2021 = ((data_pollutant['state_name'] == 'Mississippi') |(data_pollutant['state_name'] == 'Vermont') |(data_pollutant['state_name'] == 'Montana') |(data_pollutant['state_name'] == 'Maine')|(data_pollutant['state_name'] == 'Wyoming')) & (data_pollutant['year'] == 2021)
  data_rural2021 = data_pollutant[filter_rural2021][['state_name','parameter_name','mean']]

  mean_rural2021 = data_rural2021['mean'].mean()
  std_rural2021 = data_rural2021['mean'].std()
  var_rural2021 = data_rural2021['mean'].var()
  mean_urban2021 = data_urban2021['mean'].mean()
  std_urban2021 = data_urban2021['mean'].std()
  var_urban2021 = data_urban2021['mean'].var()
  t_stat, p_val = stats.ttest_ind(data_rural2021['mean'],data_urban2021['mean'])
  tampil_rural = st.checkbox('Tampilkan Data Rural')
  if tampil_rural:
    data_rural2021
  tampil_urban = st.checkbox('Tampilkan Data Urban')
  if tampil_urban:
    data_urban2021
  tampil_p_tvalue = st.checkbox('Tampilkan p-value dan t-stat')
  if tampil_p_tvalue:
    st.write(f'p-value: {round(p_val,3)}')
    st.write(f't-stat: {round(t_stat,3)}')
  def se(n1,n2,var1,var2):
    se= np.sqrt((((n1-1)*var1+(n2-1)*var2)/(n1+n2-2))*((1/n1)+(1/n2)))
    return se

  se12 = se(len(data_rural2021),len(data_urban2021),var_rural2021,var_urban2021)
  
  rv = stats.t(len(data_rural2021)+len(data_urban2021)-2,loc=0,scale = se12)
  xx = np.linspace(rv.ppf(0.0001), rv.ppf(0.9999), 100)
  yy = rv.pdf(xx)
  plt.figure(figsize=(8,5))
  fig,ax = plt.subplots()
  plt.plot(xx,yy)
  #sns.distplot(data_rural2021['mean'], label='Rural population', color='blue', hist=False)
  #sns.distplot(data_urban2021['mean'], label='Urban population', color='red',hist=False)
  #plt.axvline(mean_rural2021, color='green', linewidth=2, label='Rural (Mean)', linestyle='dashed')
  #plt.axvline(mean_urban2021, color='orange', linewidth=2, label='Urban (Mean)',linestyle='dashed')
  plt.axvline(rv.ppf(0.025), color = 'orange', label='Reject boundary')
  plt.axvline(rv.ppf(0.975), color = 'orange')
  plt.axvline(t_stat, color = 'red',linestyle='dashed', label = 't-stat')
  plt.xlabel('t-score')
  plt.title('X1-X2 Distribution')
  plt.legend()
  st.pyplot(fig)

  st.markdown('''Karena nilai *P-value* 0.038 yang mana lebih kecil dari 0.05, atau nilai *t-stat* -2.07 yang mana berada
   di reject area, maka kesimpulan reject $H_0$. 
  Sehingga dapat dinyatakan **terdapat pengaruh yang cukup signifikan antara pollutant di area rural state dengan area urban**. 
  Apabila melihat dari mean kedua data tersebut, 
  kita juga dapat menyimpulkan bahwa terjadi kadar polutan di daerah urban lebih besar dari daerah rural.''')
  






