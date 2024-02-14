# Instalación
1. Cree un espacio de trabajo en **~/**

	   mkdir ~/robot_ws
2. Cree una carpeta **src** dentro de su espacio de trabajo.

	    mkdir ~/robot_ws/src

3. Clonar el archivo de github dentro de la carpeta **src**
	
	    git clone https://github.com/davidrdcr/IMU_controller.git
	    
4. Con el terminal abierto en la carpeta **src**, compila el paquete.

		colcon build
		
5. Configure las variables de entorno.

		echo "source ~/robot_ws/install/setup.sh" >> ~/.bashrc
		source ~/.bashrc

6. Otorgue permiso a los archivos de python.

		cd ~/robot_ws/src/imu_controller/imu_controller
		sudo chmod 777 *.py
	
7. Instale las dependencias.

	    pip install pyserial
	    pip install modbus_tk
	    pip install transforms3d
		
8. Verifique en qué puerto se encuntra el dispositivo.

		ls /dev/ttyUSB* 
	    
9. Otorgue permisos al puerto.

		sudo chmod 777 /dev/ttyUSB0
 

10. Ejecute el paquete.

		ros2 run imu_controller imu_node

11. Los datos se pueden ver haciéndole eco al tópico.

		ros2 topic echo /imu		
