#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

#raio equador terra metros
R =  6378137

#achatamento da terra metros
f = 0.003352813 #0,005079304

#funcao transformada ponto de referencia detectado em coordenada x,y [m] com o mundo 0,0
def rotation(theta, delta, R):

    a1 = math.cos(theta) 
    a2 = math.sin(theta)
    a3 = delta[0]
    a4 = R[0]
    b3 = delta[1]
    b4 = R[1]

    Xr_o = a1 * a3 + (-a2 * b3) + a4
    Yr_o = a2 * a3 + a1 * b3 + b4

    return Xr_o, Yr_o

#funcao para converter de um ponto em metros a lat, long
def flat2lla(P,llo,psio,href):

    #ponto em metros que preciso converter
    Xp = P[0]
    Yp = -1 * P[1]
    Zp = P[2]

    #ponto lat, long de referencia 0,0
    Lat_o = llo[0]
    Lon_o = llo[1]

    #ponto lat, long de referencia em radianes
    Lat_r = Lat_o * math.pi / 180
    Lon_r = Lon_o * math.pi / 180
    
    #equacoes da transformacao
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
    
    return Lat_p, Lon_p, Alt_p

#funcao para converter de um ponto em lat, long ao um ponto em metros
def lla2flat(lla,llo,psio,href):

    #ponto em lat, long que preciso converter
    Lat_p = lla[0]
    Lon_p = lla[1]
    Alt_p = lla[2]

    #ponto lat, long de referencia 0,0
    Lat_o = llo[0]
    Lon_o = llo[1]

    #ponto lat, long de referencia 0,0 em radianes llo
    Lat_r = Lat_o * math.pi / 180
    Lon_r = Lon_o * math.pi / 180

    #equacoes
    dLat = Lat_p - Lat_o
    dLon = Lon_p - Lon_o

    ff = 2*f-f*f
    sinLat = math.sin(Lat_r)
    Rn = R/math.sqrt(1-(ff*sinLat*sinLat))
    Rm = Rn*( (1-ff)/(1-(ff*sinLat*sinLat)))

    dNorth = (dLat * math.pi / 180) / math.atan2(1,Rm)
    dEast = (dLon * math.pi / 180) / math.atan2(1,Rn*math.cos(Lat_r))

    Xp = math.cos(psio)*dNorth + math.sin(psio)*dEast
    Yp = -math.sin(psio)*dNorth + math.cos(psio)*dEast
    Zp = -Alt_p - href

    return Xp,-Yp,Zp
