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
        self.imu_pub1 = self.create_publisher(Imu, 'imu1', 10) # Creamos un publicador para los datos del sensor
        self.imu_pub2 = self.create_publisher(Imu, 'imu2', 10)
        # Imu es el tipo de mensaje, 'imu' es el nombre del tópico y 10 es el tamaño de la cola

    def publicar_datos(self):
        try: # Intentamos abrir el puerto serie
            self.wt_imu = serial.Serial(port = "/dev/ttyUSB0", baudrate = 9600, timeout=0.5)
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

            msg1 = Imu() # Creamos un mensaje de tipo Imu
            msg2 = Imu() # Creamos un mensaje de tipo Imu
            
            while rclpy.ok():
                try: # Intentamos leer los registros del sensor
                    # Lectura de registros
                    reg50 = self.master.execute(0x50, modbus_tk.defines.READ_HOLDING_REGISTERS, 52, 12)
                    reg51 = self.master.execute(0x51, modbus_tk.defines.READ_HOLDING_REGISTERS, 52, 12)

                except Exception as e: # Si no se logra leer los registros, se imprime un mensaje de error y se cierra el programa
                    self.get_logger().info('No se puede leer los registros.')
                    print(e)
                    time.sleep(0.1) 

                else: # Si se logra leer los registros, se publican los datos
                    # Conversión de registros a valores
                    v50 = [0]*12
                    for i in range(12):
                        if (reg50[i]>32767):
                            v50[i]=reg50[i]-65536
                        else:
                            v50[i]=reg50[i]

                    v51 = [0]*12
                    for i in range(12):
                        if (reg51[i]>32767):
                            v51[i]=reg51[i]-65536
                        else:
                            v51[i]=reg51[i]
                    


                    
                    # Aceleración lineal
                    aceleracion50 = [v50[i] / 32768.0 * 16 * 9.8 for i in range(0, 3)]
                    aceleracion51 = [v51[i] / 32768.0 * 16 * 9.8 for i in range(0, 3)]
                
                    # Velocidad angular
                    velocidadAngular50 = [v50[i] / 32768.0 * 2000 * math.pi / 180 for i in range(3, 6)]
                    velocidadAngular51 = [v51[i] / 32768.0 * 2000 * math.pi / 180 for i in range(3, 6)]

                    # Campo magnético
                    magnetometro50 = v50[6:9]
                    magnetometro51 = v51[6:9]

                    # Orientación
                    angulos_grados50 = [v50[i] / 32768.0 * 180 for i in range(9, 12)]
                    angulos_radianes50 = [angulos_grados50[i] * math.pi / 180 for i in range(3)]
                    qua50 = euler2quat(angulos_radianes50[0], angulos_radianes50[1], angulos_radianes50[2])
                    qua50 = [qua50[2], qua50[3], qua50[0], qua50[1]]

                    angulos_grados51 = [v51[i] / 32768.0 * 180 for i in range(9, 12)]
                    angulos_radianes51 = [angulos_grados51[i] * math.pi / 180 for i in range(3)]
                    qua51 = euler2quat(angulos_radianes51[0], angulos_radianes51[1], angulos_radianes51[2])
                    qua51 = [qua51[2], qua51[3], qua51[0], qua51[1]]


                    # Publicación de datos msg50

                    # Publicación de datos msg1

                    # Marca de tiempo
                    msg1.header.stamp = self.get_clock().now().to_msg()

                    # Identificador del marco de referencia
                    msg1.header.frame_id = "base_link"

                    msg1.linear_acceleration.x = aceleracion50[0]
                    msg1.linear_acceleration.y = aceleracion50[1]
                    msg1.linear_acceleration.z = aceleracion50[2]

                    msg1.angular_velocity.x = velocidadAngular50[0]
                    msg1.angular_velocity.y = velocidadAngular50[1]
                    msg1.angular_velocity.z = velocidadAngular50[2]

                    msg1.orientation.x = qua50[0]
                    msg1.orientation.y = qua50[1]
                    msg1.orientation.z = qua50[2]
                    msg1.orientation.w = qua50[3]

                    #msg1.orientation_covariance = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
                    #msg1.angular_velocity_covariance = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

                    # Publicación de datos msg2

                    # Marca de tiempo
                    msg2.header.stamp = self.get_clock().now().to_msg()

                    # Identificador del marco de referencia
                    msg2.header.frame_id = "base_link"

                    msg2.linear_acceleration.x = aceleracion51[0]
                    msg2.linear_acceleration.y = aceleracion51[1]
                    msg2.linear_acceleration.z = aceleracion51[2]

                    msg2.angular_velocity.x = velocidadAngular51[0]
                    msg2.angular_velocity.y = velocidadAngular51[1]
                    msg2.angular_velocity.z = velocidadAngular51[2]

                    msg2.orientation.x = qua51[0]
                    msg2.orientation.y = qua51[1]
                    msg2.orientation.z = qua51[2]
                    msg2.orientation.w = qua51[3]

                    #msg2.orientation_covariance = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
                    #msg2.angular_velocity_covariance = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

                    self.imu_pub1.publish(msg1)
                    self.imu_pub2.publish(msg2)

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
    
