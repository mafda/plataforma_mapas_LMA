#!/usr/bin/env python
# -*- coding: utf-8 -*-

from transformations import *
import psycopg2

if __name__ == '__main__':
    #posicao lat, long, alt, inicial PontoA = [-22.8189685 -47.0647617] (llo)
    Lat_o = -22.8189685 
    Lon_o = -47.0647617
    
    # #ponto em metros (p)
    # Xp = 65
    # Yp = 164
    # Zp = 0
    
    # #Direcao angular do eixo x-Terra plana
    # psio = 0
    
    # #Altura de referência a partir da superfície da Terra 
    # href = 0

    # lat,lon,h = flat2lla((Xp,Yp,Zp),(Lat_o,Lon_o),psio,href)

    # print lat,lon
    
    # x,y,z = lla2flat((lat,lon,h),(Lat_o,Lon_o),psio,href)

    # print x,y,z

    #informacoes que publica os nodos camera detection e position euler    

    Xcar_o =  27.6133365631
    Ycar_o = 70.9453277588
    theta = 1.18994903564

    Xcam_car = 1.2 
    Ycam_car = 0.0
    Xr_cam = 5.65881347656 
    Yr_cam = -1.98187768459

    #calcula a transformada, encontra o ponto R em metros
    Xr_o,Yr_o = rotation(theta, (Xcam_car + Xr_cam, Ycam_car + Yr_cam), (Xcar_o,Ycar_o))
    print Xr_o,Yr_o

    #converte o ponto metros em uma coordenada em lat, long
    lat,lon,h = flat2lla((Xr_o,Yr_o,0),(Lat_o,Lon_o),0,0)
    print lat,lon

    #conexao com DB 
    conexion = psycopg2.connect(dbname='gis')
    cur = conexion.cursor()

    d_max = 1000

    point = str(lon) + " " + str(lat)
    
    #procurar o primeiro ponto mais perto lat, long
    search = "SELECT ST_AsText(ST_Transform(position,4326)), type, info, ST_Distance(ST_Transform(ST_GeomFromText('POINT(" + point + ")',4326),900913), position) FROM info_vilma WHERE ST_Distance(ST_Transform(ST_GeomFromText('POINT(" + point + ")',4326),900913), position) < " + str(d_max) + " ORDER BY ST_Distance(ST_Transform(ST_GeomFromText('POINT(" + point + ")',4326),900913), position) LIMIT 1"
    #print search

    cur.execute(search)

    p = cur.fetchall()

    conexion.commit()
    conexion.close()
    P = p[0][0]

    P =  P.split('(')[1].split(')')[0].split()
    lat_star = float(P[1])
    lon_star = float(P[0])

    

    #mostra o ponto
    print lat_star, lon_star

    #converte o ponto lat, lon em um ponto em metros 
    Xr_star,Yr_star,Zr_star = lla2flat((lat_star,lon_star,0),(Lat_o,Lon_o),0,0)
    print Xr_star, Yr_star

   
    #calcula a transformada, encontra o ponto do veiculo medida
    Xcar_m,Ycar_m = rotation(theta, (- Xcam_car - Xr_cam, - Ycam_car - Yr_cam), (Xr_star, Yr_star))
    print Xcar_m,Ycar_m
