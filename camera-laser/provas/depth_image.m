clc
clear all
close all

x = load('velodyne_x.txt');
y = load('velodyne_y.txt');
z = load('velodyne_z.txt');

size(x)
size(y)
size(z)

figure, plot3(x,y,z,'.')

d = sqrt(x.^2 + y.^2 + z.^2);
size(d)

figure, imagesc(d);