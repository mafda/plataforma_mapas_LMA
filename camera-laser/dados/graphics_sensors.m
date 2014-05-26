clc
clear all
close all

gps_ideal = load('gps_ideal.txt');
size(gps_ideal)
plot(gps_ideal(:,1),gps_ideal(:,2))
hold on

gps_lowcost = load('gps_lowcost.txt');
size(gps_lowcost)
plot(gps_lowcost(:,1),gps_lowcost(:,2),'*r')

position_vision_system = load('position_vision_system.txt');
size(position_vision_system)
plot(position_vision_system(:,1),position_vision_system(:,2),'*g')

%velocity = load('velocity.txt');
%v_carro=(velocity(:,1).^2+velocity(:,2).^2).^(1/2);
%figure, plot(sqrt(velocity(:,1).^2 + velocity(:,2).^2),'g')
