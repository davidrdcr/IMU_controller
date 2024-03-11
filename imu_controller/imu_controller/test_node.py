#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import serial
from modbus_tk import modbus_rtu
import modbus_tk
import math
import time
from transforms3d.euler import euler2quat
from sensor_msgs.msg import Imu
from vesc_msgs.msg import VescStateStamped
from std_msgs.msg import Float64

class Prueba(Node):

    def __init__(self):
        super().__init__('prueba')
        self.velocidad_motor = 0
        self.velocidad_sensor_motor =0
        self.pose_subscriber_ = self.create_subscription(VescStateStamped, '/sensors/core', self.leer_valor, 10)
        self.pose_subscriber_ = self.create_subscription(Imu, 'imu', self.pose_callback, 10)
        self.publicador_ = self.create_publisher(Float64, '/commands/motor/speed', 10)
        self.timer_ = self.create_timer(0.1, self.enviar_velocidad)

    def leer_valor(self, msg: VescStateStamped):
        self.velocidad_sensor_motor = msg.state.speed
        
    def pose_callback(self, msg: Imu):
        print('********************************************************')
        print('Velocidad del motor según el sensor: ', self.velocidad_sensor_motor)
        qua = [0]*4
        qua[0] = msg.orientation.x 
        qua[1] = msg.orientation.y 
        qua[2] = msg.orientation.z 
        qua[3] = msg.orientation.w
        qua = [qua[2], qua[3], qua[0], qua[1]]

        # roll = math.atan2(2*(qua[3]*qua[0]+qua[1]*qua[2]),1-2*(qua[0]**2+qua[1]**2))
        # roll = math.degrees(roll)
        # yaw = math.atan2(2*(qua[3]*qua[2]+qua[0]*qua[1]),1-2*(qua[1]**2+qua[2]**2))
        # yaw = math.degrees(yaw)
        pitch = math.asin(2*(qua[3]*qua[1]-qua[2]*qua[0]))
        pitch = math.degrees(pitch)
        
        kp = 1
        velocidad_maxima = 3000
        valor_sensor_imu = round(pitch)
        
        valor_sensor_imu = (((valor_sensor_imu + 90)/180)*6000)-3000
        
        print('Valor del sensor seleccionado según el IMU: ', valor_sensor_imu)
        error = valor_sensor_imu - self.velocidad_sensor_motor
        delta_velocidad = kp * error

        self.velocidad_motor = self.velocidad_sensor_motor + delta_velocidad

        if self.velocidad_motor > velocidad_maxima:
            self.velocidad_motor = velocidad_maxima
        elif self.velocidad_motor < -velocidad_maxima:
            self.velocidad_motor = -velocidad_maxima

        print('Velocidad del motor controlada: ', self.velocidad_motor)


    def enviar_velocidad(self):
        msg = Float64()
        msg.data = float(self.velocidad_motor)
        self.publicador_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    prueba = Prueba()
    rclpy.spin(prueba)
    rclpy.shutdown()