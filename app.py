import streamlit as st
import pandas as pd
import pickle

st.title("Los Angeles Günlük Suç Sayısı Tahmini :police_car:")
model=pickle.load(open('suc_model.pkl','rb'))
son=pickle.load(open('suc_son.pkl','rb'))

gun_sayisi=st.number_input('Kaç gün sonrasına kadar tahmin edilsin?',1,60,7)
if st.button('Tahmin et'):
    gecmis=list(son['son_degerler'])
    tarih=son['son_tarih']
    sonuc=[]
    for i in range(int(gun_sayisi)):
        tarih=tarih+pd.Timedelta(days=1)
        x=pd.DataFrame([[gecmis[-1],gecmis[-7],gecmis[-14],sum(gecmis[-7:])/7,tarih.dayofweek,tarih.month]],
                       columns=['lag1','lag7','lag14','ort7','haftanin_gunu','ay'])
        t=float(model.predict(x)[0])
        gecmis.append(t)
        sonuc.append({'tarih':tarih.strftime('%Y-%m-%d'),'tahmini_suc_sayisi':round(t)})
    sonuc=pd.DataFrame(sonuc)
    st.line_chart(sonuc.set_index('tarih'))
    st.write(sonuc)
