
# Instalación

1. Dentro de la carpeta **src** de su espacio de trabajo clone el paquete.
	
	    git clone https://github.com/davidrdcr/imu_controller.git
	    
4. Con el terminal abierto en el espacio de trabajo, compila el paquete.

		 colcon build
		
5. Configure las variables de entorno.

		echo "source ~/robot_ws/install/setup.sh" >> ~/.bashrc
		source ~/.bashrc
	
7. Instale el pip

		sudo apt install python3-pip
		
8. Agrega el directorio al PATH

		`export PATH=$PATH:/home/NOMBREDEUSUARIO/.local/bin`

9. Instale las dependencias.

	    pip install pyserial modbus_tk transforms3d
		
10. Verifique en qué puerto se encuntra el dispositivo.

		ls /dev/ttyUSB* 
	    
11. Otorgue permisos al puerto.

		sudo chmod 777 /dev/ttyUSB0
 
12. Ejecute el paquete.

		ros2 run imu_controller imu_node

13. También se puede ejecutar desde el launch file

		ros2 launch imu_controller _imu_launch.py

16. Los datos se pueden ver haciéndole eco al tópico.

		ros2 topic echo /imu1
		ros2 topic echo /imu2


## Para visualizar en Rviz

1. De no tener instalado rviz2

		sudo apt-get install ros-<DISTRO>-imu-tools
		
2. Instalar

		sudo apt-get install ros-<DISTO>-imu-tools

3. Ejecutar

		ros2 launch imu_controller _imu_rviz_launch.py

