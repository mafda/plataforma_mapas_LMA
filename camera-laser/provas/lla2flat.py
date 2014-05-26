#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

#ponto de referenca lat, lon (ponto novo) lla
Lat_p = -22.8183797
Lon_p = -47.0663663
Alt_p = 0

#posicao lat, long, alt, inicial PontoA = [-22.8189685 -47.0647617]; llo
Lat_o = -22.8189685 
Lon_o = -47.0647617
Alt_o = 0

#posicao en radianes llo
Lat_r = Lat_o * math.pi / 180
Lon_r = Lon_o * math.pi / 180
Alt_r = Alt_o * math.pi / 180

#Direcao angular do eixo x-Terra plana
psio = 0

#Altura de referência a partir da superfície da Terra 
href = 0

#raio equador terra metros
R =  6378137

#achatamento da terra metros
f = 0.003352813 #0,005079304

dLat = Lat_p - Lat_o
dLon = Lon_p - Lon_o

ff = 2*f-f*f
sinLat = math.sin(Lat_r)
Rn = R/math.sqrt(1-(ff*sinLat*sinLat))
Rm = Rn*( (1-ff)/(1-(ff*sinLat*sinLat)))

dNorth = (dLat * math.pi / 180) / math.atan2(1,Rm)
dEast = (dLon * math.pi / 180) / math.atan2(1,Rn*math.cos(Lat_r))

Lat_n = math.cos(psio)*dNorth + math.sin(psio)*dEast
Lon_n = -math.sin(psio)*dNorth + math.cos(psio)*dEast
Alt_n = -Alt_p - href

print Lat_n, Lon_n, Alt_n