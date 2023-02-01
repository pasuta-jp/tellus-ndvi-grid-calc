#Tellus JupiterからNDVIの画像生成に使われているCOMNDVI_ASNARO1という変数をcsvで保存してください。
#ex:np.savetxt('NDVI_nerima.csv', COMNDVI_ASNARO1, delimiter=',', fmt='%12.8f')
#上記csvを作業ディレクトリに配置したら準備完了です。

#import dotenv
import os, json, requests, math
import numpy as np
#import cv2
from skimage import io, color, img_as_ubyte, filters, transform
from io import BytesIO
from PIL import Image
import matplotlib.pyplot as plt

#バイナリのNDVIを何分の１のデータ量にするか先に決める
value1=10 #緯度
value2=10 #経度

# 緯度の最小値
max_lat = 35.775869
# 経度の最小値
min_lon = 139.563481
# 緯度の最大値
min_lat = 35.713590
# 経度の最大値
max_lon = 139.672142

#CSV読み込み
COMNDVI_ASNARO1=np.loadtxt('NDVI_nerima.csv',delimiter=",")

#緯度経度の差異
delta_lon=max_lon-min_lon
delta_lat=max_lat-min_lat
#NDVIの要素数を出力
NDVI_num=COMNDVI_ASNARO1.shape
#NDVIの値間の緯度経度を算出
lon_plot=delta_lon/NDVI_num[1]
lat_plot=delta_lat/NDVI_num[0]
print(NDVI_num[0])
print(NDVI_num[1])

#４点のNDVIの値から平均値を算出し配列に格納
x=0
y=0
avr_NDVI=np.zeros((int(NDVI_num[0]/value1),int(NDVI_num[1]/value2)))
for i in range(1,NDVI_num[0]):
    if i % value1 ==0:
        print("iの値は:",i)
        x=x+1
        y=0
        for j in range(1,NDVI_num[1]):
            if j % value2 ==0:
                print("jの値は:",j)
                y=y+1
                print('x,yの値は',x,y)
                if np.isnan(COMNDVI_ASNARO1[i-1,j-1]) or np.isnan(COMNDVI_ASNARO1[i-1,j]) or np.isnan(COMNDVI_ASNARO1[i,j-1]) or np.isnan(COMNDVI_ASNARO1[i,j]):
                #if COMNDVI_ASNARO1[i-1,j-1]=='nan' or COMNDVI_ASNARO1[i-1,j]=='nan' or COMNDVI_ASNARO1[i,j-1]=='nan' or COMNDVI_ASNARO1[i,j]=='nan':
                    avr_NDVI[x-1,y-1]=0
                else:
                    avr_NDVI[x-1,y-1]=np.average([COMNDVI_ASNARO1[i-1,j-1],COMNDVI_ASNARO1[i-1,j],COMNDVI_ASNARO1[i,j-1],COMNDVI_ASNARO1[i,j]])
    print(avr_NDVI.shape)

#avr_NDVI=np.zeros((NDVI_num[0],NDVI_num[1]))
#for i in range(1,NDVI_num[0]):
#        for j in range(1,NDVI_num[1]):
#            if np.isnan(COMNDVI_ASNARO1[i-1,j-1]) or np.isnan(COMNDVI_ASNARO1[i-1,j]) or np.isnan(COMNDVI_ASNARO1[i,j-1]) or np.isnan(COMNDVI_ASNARO1[i,j]):
#            #if COMNDVI_ASNARO1[i-1,j-1]=='nan' or COMNDVI_ASNARO1[i-1,j]=='nan' or COMNDVI_ASNARO1[i,j-1]=='nan' or COMNDVI_ASNARO1[i,j]=='nan':
#                avr_NDVI[i-1,j-1]=0
#            else:
#                avr_NDVI[i-1,j-1]=np.average([COMNDVI_ASNARO1[i-1,j-1],COMNDVI_ASNARO1[i-1,j],COMNDVI_ASNARO1[i,j-1],COMNDVI_ASNARO1[i,j]])
#print(avr_NDVI.shape)

#NDVIの平均値に対応する緯度経度の四角形を配列に格納
#[[min_lon, min_lat, max_lon, max_lat],[min_lon, min_lat, max_lon, max_lat],***]
coordinate_data=np.zeros((avr_NDVI.shape[0],avr_NDVI.shape[1],4))
for i in range(1,avr_NDVI.shape[0]):
    for j in range(1,avr_NDVI.shape[1]):
        coordinate_data[i-1,j-1]=[min_lon+lon_plot*(j-1)*value2, max_lat-lat_plot*i*value1,min_lon+lon_plot*j*value2,max_lat-lat_plot*(i-1)*value1]
print(coordinate_data.shape)

#４隅の緯度経度とそのグリッドのNDVIをペアにしてリスト化
#[[NDVI,min_lon, min_lat, max_lon, max_lat],***]
NDVI_fin_data=np.zeros((avr_NDVI.shape[0],avr_NDVI.shape[1],5))
print(NDVI_fin_data.shape)
for i in range(1,avr_NDVI.shape[0]):
    for j in range(1,avr_NDVI.shape[1]):
        row = [avr_NDVI[i-1][j-1],coordinate_data[i-1][j-1][0],coordinate_data[i-1][j-1][1],coordinate_data[i-1][j-1][2],coordinate_data[i-1][j-1][3]]
        NDVI_fin_data[i-1][j-1]=row
print(NDVI_fin_data.shape)

from cmath import isnan
for i in range(NDVI_fin_data.shape[0]):
    for j in range(NDVI_fin_data.shape[1]):
        if np.isnan(NDVI_fin_data[i][j][0]):
            NDVI_fin_data[i][j][0]=0

#2次元配列に変換
result = [] 
for row1 in NDVI_fin_data:
    for row2 in row1:
        if row2[0]!=0:
            result.append(row2)

#CSVで保存
np.savetxt('NDVI_grid_nerima_50_4.csv', result, delimiter=',', fmt='%12.8f')