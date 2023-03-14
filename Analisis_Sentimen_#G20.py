#!/usr/bin/env python
# coding: utf-8

# Pertama mari kita ambil data yang kita butuhkan dari media sosial twitter.

# In[88]:


import tweepy
import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

consumer_key = "2YZxNuPd3OJWAEw46LD77xptz"
consumer_secret = "VFRJg6MigfPOL8HPgTNuGKtdifH6WZwA8SpjxDOcE4BdnWonK5"
access_token = "1220348258834206721-EddBeeOhuruHOOBbnNfuCwcEfFoyui"
access_token_secret = "ilBvOh3tYKS5Pud8LHypRguFHpfo0EAUzOFOsm1KY0kdJ"


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


# Untuk melakukan pencarian tweet kita akan mengunakan kode `api.search_tweets` kita juga akan menggunakan cursor disini. Sebelumnya kita akan menentukan kata kunci pencarian kita dan tanggal mulai diambilnya tweet. Untuk saat ini mari kita cari kata kunci “G20” dan “2022-11-15”

# In[89]:


search_words = "G20"
date_since = "2022-11-15"
new_search = search_words + " -filter:retweets"

tweets = tweepy.Cursor(api.search_tweets,
        q=new_search,
        lang="id",
        since_id=date_since).items(10)


# *Ket: `filter` disini digunakan untuk melakukan pengecualian pada konten Retweet.
# `q` merupakan query/kata kunci yang dipakai
# `lang` merupakan bahasa pencarian
# `items` digunakan untuk melakukan pembatasan hasil pencarian*

# Karena tweet nanti akan berupa list maka kita akan melakukan loop untuk mengambil masing-masing data. Dalam loop ini kita akan langsung melakukan pembersihan data dari kata/karakter seperti @, link, dsb.

# In[90]:


items = []
for tweet in tweets:
    items.append (' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet.text).split()))
hasil = pd.DataFrame(data=items, columns=['tweet'])


# Data tweet sudah kita dapatkan maka mari sekarang kita lakukan evaluasi dan analisis nilai positif dan negatif semua kalimat yang telah kita ambil. Pertama kita buka file list kata positif dan negatif yang kita punya lalu untuk setiap kalimat yang kita miliki kita akan menghitung terdapat berapa kata positif dan negatif.

# In[91]:


pos_list= open("kata_positif.txt","r")
pos_kata = pos_list.readlines()
neg_list= open("kata_negatif.txt","r")
neg_kata = neg_list.readlines()  

sentiments = [] #Membuat sebuah list menyimpan nilai sentiment

#membuat list kata-kata negasi
list_anti = ['tidak','lawan','anti', 'belum', 'belom', 'tdk', 'jangan', 'gak', 'enggak', 'bukan', 'sulit', 'tak', 'sblm']

#fungsi menghitung sentiment setiap tweet
for item in items:
    print(item.strip())
    tweets = item.strip().split() #tokenization
    # print(tweets)
    
    count_p = 0 #nilai positif
    count_n = 0 #nilai negatif
    
    for tweet in tweets:
        for kata_pos in pos_kata:
            if kata_pos.strip().lower() == tweet.lower():
                #items.index(item)-1 digunakan untuk mencari nilai index sebelum index positifnya
                #aku menyukai bola
                if items[items.index(item)-1] in list_anti:
                    print(items[items.index(item)-1], kata_pos, ['negatif'])
                    count_n += 1
                else:
                    print(kata_pos, ['positif'])
                    count_p += 1
        for kata_neg in neg_kata:
            if kata_neg.strip().lower() == tweet.lower():
                if items[items.index(item)-1] in list_anti:
                    print(items[items.index(item)-1], kata_neg, ['positif'])
                    count_p += 1
                else:
                    print(kata_neg, ['negatif'])
                    count_n += 1
    
    print ("positif: "+str(count_p))
    print ("negatif: "+str(count_n))


# Sekarang mari kita hitung evaluasi dari sentimen kita dengan persamaan berikut
# 
# Total Nilai = Nilai Positif - Nilai Negatif
# Total Nilai > 0, maka sentimen positif
# Total Nilai < 0, maka sentimen negatif
# Total Nilai = 0, maka sentimen netral
# 
# Hasil perhitungan kita masukkan ke dalam dataframe pandas agar lebih mudah untuk memanipulasi dan melihat. Lalu kita coba cari nilai rata-rata dan standar deviasinya.

# In[92]:


sentiments = [] #Membuat sebuah list menyimpan nilai sentiment

#membuat list kata-kata negasi
list_anti = ['tidak','lawan','anti', 'belum', 'belom', 'tdk', 'jangan', 'gak', 'enggak', 'bukan', 'sulit', 'tak', 'sblm']

#fungsi menghitung sentiment setiap tweet
for item in items:
    print(item.strip())
    tweets = item.strip().split() #tokenization
    # print(tweets)
    
    count_p = 0 #nilai positif
    count_n = 0 #nilai negatif
    
    for tweet in tweets:
        for kata_pos in pos_kata:
            if kata_pos.strip().lower() == tweet.lower():
                #items.index(item)-1 digunakan untuk mencari nilai index sebelum index positifnya
                #aku menyukai bola
                if items[items.index(item)-1] in list_anti:
                    print(items[items.index(item)-1], kata_pos, ['negatif'])
                    count_n += 1
                else:
                    print(kata_pos, ['positif'])
                    count_p += 1
        for kata_neg in neg_kata:
            if kata_neg.strip().lower() == tweet.lower():
                if items[items.index(item)-1] in list_anti:
                    print(items[items.index(item)-1], kata_neg, ['positif'])
                    count_p += 1
                else:
                    print(kata_neg, ['negatif'])
                    count_n += 1
    
    print ("positif: "+str(count_p))
    print ("negatif: "+str(count_n))
    sentiments.append(count_p - count_n)


# Mencetak hasil dari sentimen

# In[93]:


print(sentiments)


# Kita lakukan plot terhadap data

# In[94]:


labels, counts = np.unique(sentiments, return_counts=True)
plt.bar(labels, counts, align='center')
plt.gca().set_xticks(labels)
plt.show()


# Artinya bahwa untuk jumlah tweet 10 buah Sentimen masyarakat twitter berada ke arah positif dibandingkan ke arah negatif untuk bahasan G20. Dari sini kita tahu bahwa dengan database kata yang baik dan jumlah data mentah yang mumpuni akan membuat analisis sentimen menjadi alat yang cukup kuat untuk melihat kecenderungan pasar. Analisis lebih lanjut dari data juga akan menguatkan kesimpulan yang didapat dari proses analisis sentimen.
