# Instalación
1. Cree un espacio de trabajo en **~/**

	   mkdir ~/robot_ws
2. Cree una carpeta **src** dentro de su espacio de trabajo.

	    mkdir ~/robot_ws/src

3. Clonar el archivo de github dentro de la carpeta **src**
	
	    cd ~/robot_ws/src && git clone https://github.com/davidrdcr/IMU_controller.git
	    
4. Con el terminal abierto en el espacio de trabajo, compila el paquete.

		 cd ~/robot_ws/ && colcon build
		
5. Configure las variables de entorno.

		echo "source ~/robot_ws/install/setup.sh" >> ~/.bashrc
		source ~/.bashrc

6. Otorgue permiso a los archivos de python.

		cd ~/robot_ws/src/imu_controller/imu_controller
		sudo chmod 777 *.py
	
7. Instale el pip

		sudo apt install python3-pip
		
8. Agrega el directorio al PATH

		`export PATH=$PATH:/home/NOMBREDEUSUARIO/.local/bin`

8. Instale las dependencias.

	    pip install pyserial
	    pip install modbus_tk
	    pip install transforms3d
		
9. Verifique en qué puerto se encuntra el dispositivo.

		ls /dev/ttyUSB* 
	    
10. Otorgue permisos al puerto.

		sudo chmod 777 /dev/ttyUSB0
 

11. Ejecute el paquete.

		ros2 run imu_controller imu_node

12. Los datos se pueden ver haciéndole eco al tópico.

		ros2 topic echo /imu
