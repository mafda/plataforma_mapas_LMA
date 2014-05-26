#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32MultiArray
from sensor_msgs.msg import NavSatFix
from transformations import *
import psycopg2

#ponto de referencia 0,0 do mundo,  lat,long PontoA
Lat_o = -22.8189685 
Lon_o = -47.0647617

#posicao em metros do gps_ideal
Xgps_ideal = 0
Ygps_ideal = 0

#posicao em metros do gps_lowcost
Xgps_low = 0
Ygps_low = 0

#posicao medida pelo sistema de visao
Xcar_m = 0
Ycar_m = 0
Available_data = 0

#velocidade do veiculo
Vx = 0
Vy = 0
Vz = 0

#angulo do veiculo
Theta_car = 0

#guardar os dados em arquivos texto
file_gps_ideal = open('dados/gps_ideal.txt','w')
file_gps_lowcost = open('dados/gps_lowcost.txt','w')
file_velocity = open('dados/velocity.txt','w')
file_position_vision_system = open('dados/position_vision_system.txt','w')
file_compass = open('dados/compass.txt','w')

#funcao que chama os dados do GPS ideal, latitude e longitude do veiculo
def callbackGPS_ideal_gps(data):
    global Xgps_ideal, Ygps_ideal
    #faco a transformada de lat,long a um ponto em metros x,y
    Xgps_ideal, Ygps_ideal, z = lla2flat((data.latitude,data.longitude,data.altitude),(Lat_o,Lon_o),0,0)
    

#funcao que chama os dados do GPS low cost, latitude e longitude do veiculo
def callbackGPS_lowcost(data):
    global Xgps_low, Ygps_low
    #faco a transformada de lat,long a um ponto em metros x,y
    Xgps_low, Ygps_low, z = lla2flat((data.latitude,data.longitude,data.altitude),(Lat_o,Lon_o),0,0)
    

#funcao que chama vilma_position_vision_system para obter a posicao do veiculo baseada no sistema de visao
def callbackVisionSystem(data):
    global Xcar_m,Ycar_m,Available_data
    Xcar_m = data.data[0] #posicao medida do veiculo em x
    Ycar_m = data.data[1] #posicao medida do veiculo em y
    Available_data = data.data[2] #dado valido


#funcao que chama vilma_velocity para obter a velocidade linear do veiculo
def callbackVelocity(data):
    global Vx, Vy, Vz
    Vx = data.data[0]  #velocidade veiculo x
    Vy = data.data[1]  #velocidade veiculo y
    Vz = data.data[2]  #velocidade veiculo z  


#funcao que chama compass para obter o angulo de direcao do veiculo
def callbackCompass(data):
    global Theta_car
    Theta_car = data.data[2]  #yaw veiculo
    
    
if __name__ == '__main__':
    #node name
    rospy.init_node('vilma_all_sensors', anonymous=True)

    #node suscribers
    rospy.Subscriber("ideal_gps", NavSatFix, callbackGPS_ideal_gps)
    rospy.Subscriber("lowcost_gps", NavSatFix, callbackGPS_lowcost)
    rospy.Subscriber("vilma_vision_position", Float32MultiArray, callbackVisionSystem)
    rospy.Subscriber("vilma_linear_velocity", Float32MultiArray, callbackVelocity)
    rospy.Subscriber("compass_yaw", Float32MultiArray, callbackCompass)
    
    #publish node
    pub = rospy.Publisher('vilma_sensors_data', Float32MultiArray)

    r = rospy.Rate(5)
    while not rospy.is_shutdown():
        
        print Xgps_ideal, Ygps_ideal, Xgps_low, Ygps_low, Xcar_m, Ycar_m, Vx, Vy, Theta_car

        file_gps_ideal.write ("%s\t%s\n" % (Xgps_ideal, Ygps_ideal)) #guarda os dados em arquivo texto
        file_gps_lowcost.write ("%s\t%s\n" % (Xgps_low,Ygps_low)) #guarda os dados em arquivo texto
        
        if(Available_data == 0):
            file_position_vision_system.write ("NaN\tNaN\n") #guarda os dados em arquivo texto
        else:
            file_position_vision_system.write ("%s\t%s\n" % (Xcar_m,Ycar_m)) #guarda os dados em arquivo texto

        file_velocity.write ("%s\t%s\n" % (Vx, Vy)) #guarda os dados em arquivo texto
        file_compass.write ("%s\n" % (Theta_car)) #guarda os dados em arquivo texto

        array = Float32MultiArray()
        array.data = [Xgps_ideal, Ygps_ideal, Xgps_low, Ygps_low, Xcar_m, Ycar_m, Vx, Vy, Theta_car]
        pub.publish(array) 

        r.sleep()
