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
from geojson import MultiPolygon, Feature, FeatureCollection

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
#[[lon,lat] [lon lat]]
avr_NDVI=np.zeros((NDVI_num[0],NDVI_num[1]))
for i in range(1,NDVI_num[0]):
    for j in range(1,NDVI_num[1]):
        if np.isnan(COMNDVI_ASNARO1[i-1,j-1]) or np.isnan(COMNDVI_ASNARO1[i-1,j]) or np.isnan(COMNDVI_ASNARO1[i,j-1]) or np.isnan(COMNDVI_ASNARO1[i,j]):
        #if COMNDVI_ASNARO1[i-1,j-1]=='nan' or COMNDVI_ASNARO1[i-1,j]=='nan' or COMNDVI_ASNARO1[i,j-1]=='nan' or COMNDVI_ASNARO1[i,j]=='nan':
            avr_NDVI[i-1,j-1]=0
        else:
            avr_NDVI[i-1,j-1]=np.average([COMNDVI_ASNARO1[i-1,j-1],COMNDVI_ASNARO1[i-1,j],COMNDVI_ASNARO1[i,j-1],COMNDVI_ASNARO1[i,j]])
print(avr_NDVI.shape)

#NDVIの平均値に対応する緯度経度の四角形を配列に格納
#[[min_lon, min_lat, max_lon, max_lat],[min_lon, min_lat, max_lon, max_lat],***]
coordinate_data=np.zeros((avr_NDVI.shape[0],avr_NDVI.shape[1],4))
result=[]
for i in range(1,avr_NDVI.shape[0]):
    for j in range(1,avr_NDVI.shape[1]):
        #coordinate_data[i-1,j-1]=[min_lon+lon_plot*(j-1), max_lat-lat_plot*i,min_lon+lon_plot*j,max_lat-lat_plot*(i-1)]
        my_polygon = MultiPolygon([[[[float(min_lon+lon_plot*(j-1)), float(max_lat-lat_plot*i)],[float(min_lon+lon_plot*(j-1)), float(max_lat-lat_plot*(i-1)),float(min_lon+lon_plot*j), float(max_lat-lat_plot*(i-1))],[float(min_lon+lon_plot*j), float(max_lat-lat_plot*i)],[float(min_lon+lon_plot*(j-1)), float(max_lat-lat_plot*i)]]]])
       #my_polygon = MultiPolygon([[[[float(LON_1), float(LAT_1)],[float(LON_1), float(LAT_2)],[float(LON_2), float(LAT_2)],[float(LON_2), float(LAT_1)],[float(LON_1), float(LAT_1)]]]])
        my_feature = Feature(geometry=my_polygon, properties={"NDVI": float(avr_NDVI[i-1,j-1])})
        result.append(my_feature)
        my_feature_collection = FeatureCollection(result)
print(coordinate_data.shape)
#path='C:\Users\Akama\Desktop\Engineering\Python\PJ\Tokyo City Cup'
fname = f'NDVI_Nerima_grid_2.json'
file=open(fname,'w')
file.write(str(my_feature_collection))
file.close
print(fname, 'としてGeoJsonファイルの保存完了')