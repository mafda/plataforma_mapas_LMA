clc
clear all
close all

format long
%posicao inicial (0,0) GPS PontoA
PontoA = [-22.8189685 -47.0647617];

%novo ponto em lat,long (100,0)
sinalpare_ll = flat2lla([50.9547 -138.3253 0], PontoA, 0, 0)

format short
%posicao sinal_pare em metros
sinalpare_mt = lla2flat([-22.8178672 -47.0678393 0], PontoA, 0, 0) 

format long
lla = flat2lla([sinalpare_mt], PontoA, 0, 0);
