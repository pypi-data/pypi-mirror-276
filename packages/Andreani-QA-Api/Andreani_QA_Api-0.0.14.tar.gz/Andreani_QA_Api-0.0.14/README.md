#18/01/2024 
0.0.1
Se crea libreria

0.0.2

#Se actualiza la libreria, faltaba un self en la linea 226#
#cant_registros_db = Api.check_base_sqlserver(**self**, data['data_db']['server_name']#

0.0.3
se actualiza init, estaba mal configurado / from .Api import Api

0.0.4
Faltaba **self** en la linea 143 y 145

0.0.5
Error de tipeo en linea 143 y 145

0.0.6
Faltaba **self** en la linea 14

0.0.7
Actualización a funciones, reformateo del constructor

0.0.11
Se agrega función tear_down

0.0.12
Se mueve función tear_down a la clase Api

0.0.13
Se hereda Api en la clase RequestObj

0.0.14
Se agregan 2 funciones nuevas : set_new_value_json y delete_value_json