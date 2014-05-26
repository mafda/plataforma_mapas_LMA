clc
clear all
close all

gps_ideal = load('gps_ideal.txt');
size(gps_ideal);

gps_lowcost = load('gps_lowcost.txt');
[longitud,~]=size(gps_lowcost)

position_vision_system = load('position_vision_system.txt');
size(position_vision_system)

velocity = load('velocity.txt');
v_carro=(velocity(:,1).^2+velocity(:,2).^2).^(1/2);
size(v_carro)

compass = load('compass.txt');
size(compass)

%filtro de kalman extendido (EKF)

%matriz ruido del modelo del vehiculo Wx,Wy,Wz "ideal"
Q=eye(3,3);
Q(1,1)=0.01;
Q(2,2)=0.01;
Q(3,3)=0.001;

%cuando tengo mediciones de gps y compas
%matriz de desviacion estandar da cada sensor
R1=eye(3,3);
R1(1,1)=3.12;
R1(2,2)=3.12;
R1(3,3)=0.001;
%matriz de mediciones z,vector estados
H1=[1 0 0;0 1 0;0 0 1];

%cuando tengo las mediciones de gps compas y vision
%matriz de desviacion estandar da cada sensor
R2=eye(5,5);
R2(1,1)=R1(1,1);
R2(2,2)=R1(2,2);
R2(3,3)=R1(3,3);
R2(4,4)=0.1;
R2(5,5)=0.1;
%matriz de mediciones z,vector estados
H2=[1 0 0;0 1 0;0 0 1;1 0 0;0 1 0];


%condiciones iniciales de mi carro
%x,y,theta
%xe=[0;0;1.195];
xe=[0;0;compass(1)];
%direcion del carro
delta=0; 
%matriz de incertidumbre (incerteza) covarianza
P=eye(3);
X=zeros(longitud,3);
%tiempo
T=0.1;
%distancia ruedas carro
L=2.5;

%calculos fase de prediccion 
for k=1:longitud
    %velocidad del carro
    V=v_carro(k);
    
    % es la estimacion por el modelo variables de estado x,y,theta
    xe(1)=xe(1)+T*V*cos(xe(3));
    xe(2)=xe(2)+T*V*sin(xe(3));
    xe(3)=xe(3)+T*V*tan(delta)/L;
    %linealizar el modelo (sistema no lineal)
    %matriz estado de transicion
    F=[1 0 -T*V*sin(xe(3))
       0 1  T*V*cos(xe(3))
       0 0      1         ];
   %matriz de incertidumbre (incerteza) covarianza 
    P = F*P*F' + Q;
    
  % encontrar la correcion por las medidas
  % si no tengo datos de vision
  if(isnan(position_vision_system(k,1)))
      %matriz de mediciones z,vector estados
      H=H1;
      %matriz de desviacion estandar da cada sensor
      R=R1;
      %vector de medidas
      z=[gps_lowcost(k,1)
         gps_lowcost(k,2)
         compass(k)];
  
  %si tengo todos los datos    
  else
      %matriz de mediciones z,vector estados
      H=H2;
      %matriz de desviacion estandar da cada sensor
      R=R2;
      %vector de medidas
      z=[gps_lowcost(k,1)
         gps_lowcost(k,2)
          compass(k)
          position_vision_system(k,1)
          position_vision_system(k,2)];
  end
      
    %calculos fase de correcion  
    S = H * P * H' + R;
    %ganancia kalman
    K =  (P * H')/S;
    %estimado
    xe = xe + K * (z - H*xe);
    %matriz de incertidumbre (incerteza) covarianza
    P = (eye(3) - K * H) * P;
    X(k,:)=xe';
    
end

plot(gps_ideal(:,1),gps_ideal(:,2))
hold on
plot(position_vision_system(:,1),position_vision_system(:,2),'*g')
plot(gps_lowcost(:,1),gps_lowcost(:,2),'*r')
%kalman
plot(X(:,1),X(:,2),'-*black')
