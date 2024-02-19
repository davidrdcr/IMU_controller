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

class ImuNode(Node):

    def __init__(self):
        super().__init__('imu_node') # Inicializamos el nodo
        self.get_logger().info('Se inició el ImuNode.')
        self.timer = self.create_timer(0.1, self.publicar_datos) # Creamos un temporizador para publicar los datos
        self.imu_pub = self.create_publisher(Imu, 'imu', 10) # Creamos un publicador para los datos del sensor

    def publicar_datos(self):
        try: # Intentamos abrir el puerto serie
            self.wt_imu = serial.Serial(port = "/dev/ttyUSB1", baudrate = 9600, timeout=0.5)
            if self.wt_imu.isOpen(): # Si el puerto se abre, se imprime un mensaje de éxito
                self.get_logger().info('Puerto abierto.')
            else:
                self.wt_imu.open() # Si el puerto no se abre, se intenta abrir
                self.get_logger().info('Puerto abierto.')

        except Exception as e: # Si no se puede abrir el puerto, se imprime un mensaje de error y se cierra el programa
            self.get_logger().info('Error al abrir el puerto. No está disponible el puerto /dev/ttyUSB0.')
            print(e)
            exit()
            
        else: # Si se logra abrir el puerto, se inicializa el maestro Modbus
            self.master = modbus_rtu.RtuMaster(self.wt_imu)
            self.master.set_timeout(1)
            self.master.set_verbose(True)

            msg = Imu() # Creamos un mensaje de tipo Imu
            
            while rclpy.ok():
                try: # Intentamos leer los registros del sensor
                    # Lectura de registros
                    reg = self.master.execute(81, modbus_tk.defines.READ_HOLDING_REGISTERS, 52, 12)

                except Exception as e: # Si no se logra leer los registros, se imprime un mensaje de error y se cierra el programa
                    self.get_logger().info('No se puede leer los registros.')
                    print(e)
                    time.sleep(0.1) 

                else: # Si se logra leer los registros, se publican los datos
                    # Conversión de registros a valores
                    v = [0]*12
                    for i in range(12):
                        if (reg[i]>32767):
                            v[i]=reg[i]-65536
                        else:
                            v[i]=reg[i]
                    

                    # Marca de tiempo
                    msg.header.stamp = self.get_clock().now().to_msg()

                    # Identificador del marco de referencia
                    msg.header.frame_id = "base_link"
                    
                    # Aceleración lineal
                    aceleracion = [v[i] / 32768.0 * 16 * 9.8 for i in range(0, 3)]
                
                    # Velocidad angular
                    velocidadAngular = [v[i] / 32768.0 * 2000 * math.pi / 180 for i in range(3, 6)]
                
                    # Campo magnético
                    magnetometro = v[6:9]

                    # Orientación
                    angulos_grados = [v[i] / 32768.0 * 180 for i in range(9, 12)]
                    angulos_radianes = [angulos_grados[i] * math.pi / 180 for i in range(3)]
                    qua = euler2quat(angulos_radianes[0], angulos_radianes[1], angulos_radianes[2])
                    qua = [qua[2], qua[3], qua[0], qua[1]]
    
                    # Publicación de datos
                    msg.linear_acceleration.x = aceleracion[0]
                    msg.linear_acceleration.y = aceleracion[1]
                    msg.linear_acceleration.z = aceleracion[2]
                    
                    msg.angular_velocity.x = velocidadAngular[0]
                    msg.angular_velocity.y = velocidadAngular[1]
                    msg.angular_velocity.z = velocidadAngular[2]

                    msg.orientation.x = qua[0]
                    msg.orientation.y = qua[1]
                    msg.orientation.z = qua[2]
                    msg.orientation.w = qua[3]
                    
                    msg.orientation_covariance = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
                    msg.angular_velocity_covariance = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
                    self.imu_pub.publish(msg)

def main(args=None):
    rclpy.init(args=args) # Inicializamos las comunicaciones de ROS
    node = ImuNode() # Creamos un objeto de la clase ImuNode
    try: # Intentamos mantener el nodo en ejecución
        rclpy.spin(node) 
    except KeyboardInterrupt: # Si se presiona Ctrl+C, se cierra el nodo
        pass
    rclpy.shutdown() # Cerramos las comunicaciones de ROS

if __name__ == '__main__':
    main()
    