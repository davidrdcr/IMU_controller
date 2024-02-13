#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import serial
from modbus_tk import modbus_rtu
import modbus_tk
import math
import time
from transforms3d.euler import euler2quat


class ImuNode(Node):

    def __init__(self):
        super().__init__('imu_node')
        self.get_logger().info('Se inició el ImuNode.')
        self.wt_imu = serial.Serial(port = "/dev/ttyUSB0", baudrate = 9600, timeout=0.5)

        if self.wt_imu.isOpen():
            self.get_logger().info('Puerto abierto.')
        else:
            self.wt_imu.open()
            self.get_logger().info('Puerto abierto.')  

        self.master = modbus_rtu.RtuMaster(self.wt_imu)
        self.master.set_timeout(1)
        self.master.set_verbose(True)
        
        while True:
            reg = self.master.execute(80, modbus_tk.defines.READ_HOLDING_REGISTERS, 61, 3)
            v = [0]*3

            for i in range(3):
                if (reg[i]>32767):
                    v[i]=reg[i]-65536
                else:
                    v[i]=reg[i]

            angulos_grados = [v[i] / 32768.0 * 180 for i in range(0, 3)]
            self.get_logger().info('Ángulo: ' + str(angulos_grados))

            
        

def main(args=None):
    rclpy.init(args=args) # Inicializamos las comunicaciones de ROS
    node = ImuNode() # Creamos un objeto de la clase ImuNode
    rclpy.spin(node) # Mantenemos el nodo en ejecución
    rclpy.shutdown() # Cerramos las comunicaciones de ROS

if __name__ == '__main__':
    main()



    #node.destroy_node()
