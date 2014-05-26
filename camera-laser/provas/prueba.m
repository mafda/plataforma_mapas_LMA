clc
clear all
close all

Lat_o = convang(-22.8189685, 'deg','rad');
Lon_o = convang(-47.0647617, 'deg','rad');
Alt_o = convang(0, 'deg','rad');

Xp = 65;
Yp = -164;
Zp = 0;

psio = convang(0, 'deg','rad');

href = 0;

%R =  6378137 f = 0.003352813

f = 1/196.877360;
R = 3397000;

dNorth = cos(psio)*Xp - sin(psio)*Yp;
dEast  = sin(psio)*Xp + cos(psio)*Yp;

Rn = R / sqrt(1-(2*f-f*f) *(Lat_o) * (Lat_o));
Rm = Rn * ((1-(2*f-f*f)) / (1-(2*f-f*f) * sin(Lat_o) * sin(Lat_o)));

dLat = dNorth * atan2(1,Rm);
dLon = dEast * atan2(1,Rn * cos(Lat_o));

dLon = convang(dLon,'rad','deg');
dLon = convang(dLon,'rad','deg');

Lat_p = dLat + Lat_o
Lon_p = dLon + Lon_o
Alt_p = -Zp - href
