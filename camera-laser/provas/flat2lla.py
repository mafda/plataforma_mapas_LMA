#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

#posicao lat, long, alt, inicial PontoA = [-22.8189685 -47.0647617]
Lat_o = -22.8189685 
Lon_o = -47.0647617
Alt_o = 0

#posicao en radianes
Lat_r = Lat_o * math.pi / 180
Lon_r = Lon_o * math.pi / 180
Alt_r = Alt_o * math.pi / 180

#ponto em metros 
Xp = 65
Yp = 164 * (-1)
Zp = 0

#Direcao angular do eixo x-Terra plana
psio = 0

#Altura de referência a partir da superfície da Terra 
href = 0

#raio equador terra metros
R =  6378137

#achatamento da terra metros
f = 0.003352813 #0,005079304

dNorth = math.cos(psio)*Xp - math.sin(psio)*Yp
dEast  = math.sin(psio)*Xp + math.cos(psio)*Yp
Alt_p = -Zp - href

ff = 2*f-f*f
sinLat = math.sin(Lat_r)
Rn = R / (math.sqrt(1-(ff*sinLat*sinLat)))
Rm = Rn * ( (1-ff) / (1-(ff*sinLat*sinLat) ) )

dLat = dNorth * math.atan2(1,Rm)
dLon = dEast * math.atan2(1,Rn * math.cos(Lat_r))

Lat_p = (dLat * 180 / math.pi) + Lat_o
Lon_p = (dLon * 180 / math.pi) + Lon_o

print Lat_p, Lon_p, Alt_p
