import json
from jsondiff import diff
from jsonschema import validate
import unittest
import jsonschema

import allure
from Andreani_QA_Functions.Functions import Functions
from Andreani_QA_parameters.Parameters import Parameters


class Api(Functions, Parameters):
    def get_response(self, response):
        return RequestObj(response)

    def tear_down(self):

        """
            Description:
                Finaliza la ejecución cerrando el Web Driver.
        """
        try:
            if Selenium.data_cache not in ([], {}):
                Functions.create_grid_by_sources(self.data_cache, "Datos del cache")
                print("====================Inicio Cache===================")
                pprint.pprint(Selenium.data_cache)
                print("=====================Fin Cache=====================")
            Functions.LoggingFeature(f"AGUARDANDO: Se cerrará el web driver.").send_log()
        except Exception as e:
            Functions.exception_logger(e)
        finally:
            Functions.LoggingFeature(f"REALIZADO: Finaliza la ejecución.").send_log()


class RequestObj(unittest.TestCase):
    def __init__(self, response):
        self.response = response
        self.lista_diferencias = []
        unittest.TestCase.assertIsNotNone(self.response, "El response es None")

    def response_time(self):
        """
            :return: Retorna el tiempo resultante (Segundos) desde el inicio del request hasta su respuesta.
        """
        elapsed_time = round(self.response.elapsed.total_seconds(), 2)
        Functions.create_grid_by_sources({'Esta request demoró': {elapsed_time}}, "Time Elapsed")
        return elapsed_time

    def validate_status_code(self, estado_deseado: int) -> bool:
        Functions.create_grid_by_sources({f'Estatus Code Deseado': f'{estado_deseado}',
                                          f'Estadus Code Obtenido': f'{self.response.status_code}'},
                                         "Información Importante")
        unittest.TestCase.assertEqual(unittest.TestCase(), str(estado_deseado), str(self.response.status_code),
                                      f"El status code no es el deseado, se esperaba {estado_deseado}, "
                                      f"pero se obtuvo: {self.response.status_code}")
        print(f"El status code es el deseado: {estado_deseado}")

    def validate_request_body(self, estructura_deseada) -> dict:
        try:
            json_respuesta = self.response.json()
        except ValueError:
            self.skipTest("No se puede obtener un Json válido de la repuesta.")
            return {"Error": "La respuesta no es un JSON válido."}

        if type(json_respuesta) != type(estructura_deseada):
            self.skipTest(f"El tipo de respuesta [{type(json_respuesta)}],"
                          f" no coincide con la deseada. [{type(estructura_deseada)}]")

        allure.attach(json.dumps(estructura_deseada, indent=2), "JSON esperado", allure.attachment_type.JSON)
        allure.attach(json.dumps(json_respuesta, indent=2), "JSON obtenido", allure.attachment_type.JSON)
        unittest.TestCase.assertEqual(unittest.TestCase(), json_respuesta, estructura_deseada,
                                      "El contenido de la respuesta no coincide con la estructura deseada.")
        Functions.create_grid_by_sources({' ': 'La respuesta tiene la estructura deseada.'}, "Resultado")
        return {"obtained_json": json_respuesta, "expected_json": estructura_deseada}

    def validate_response_structure(self, estructura_deseada):
        """

        :param estructura_deseada: La estructura deseada en formato json.
        :return: Retorna True si es identica, o False (marcando sus diferencias) cuando no coinciden.
        """

        json_respuesta = self.response.json()

        # de esta forma, muestra las diferencias encontradas en el obtenido
        resultado_obtenido = diff(estructura_deseada, json_respuesta)

        # de esta forma, muestra las diferencias encontradas en el esperado
        resultado_esperado = diff(json_respuesta, estructura_deseada)
        if len(resultado_obtenido) > 0 or len(resultado_esperado) > 0:
            # Si existen diferencias lo aviso
            Functions.create_grid_by_sources(
                {f'Resultado de la comparación': f'La estructura de los Json comparados NO coincide'},
                "Información Importante")
            allure.attach(json.dumps(estructura_deseada, sort_keys=True, indent=2), "JSON esperado",
                          allure.attachment_type.JSON)
            allure.attach(json.dumps(json_respuesta, sort_keys=True, indent=2), "JSON obtenido",
                          allure.attachment_type.JSON)
            print(f"La Estructura de los Json NO conciden.")
        else:
            Functions.create_grid_by_sources(
                {f'Resultado de la comparación': f'La estructura de los Json comparados coincide'},
                "Información Importante")
            allure.attach(json.dumps(estructura_deseada, sort_keys=True, indent=2), "JSON esperado",
                          allure.attachment_type.JSON)
            allure.attach(json.dumps(json_respuesta, sort_keys=True, indent=2), "JSON obtenido",
                          allure.attachment_type.JSON)
            print(f"La Estructura de los Json conciden.")

    def validate_response_by_scheme(self):
        """
            :param json_schema: La estructura deseada a analizar en formato json.
        """

        json_respuesta = self.response.json()
        scheme = self.generate_schema(Functions.data_cache['RESPONSE ESPERADO'])
        try:
            validate(instance=json_respuesta, schema=scheme)
            Functions.create_grid_by_sources(
                {f'Resultado de la comparación': f'Los tipos de datos dentro de la '
                                                 f'estructura de los Json comparados coincide'},
                "Información Importante")
            print(f"Los Json conciden.")
        except jsonschema.ValidationError as val_e:
            data = {val_e.path[0]: val_e.instance}
            allure.attach(json.dumps(data, sort_keys=True, indent=2), f'Dado que los Json no coinciden, se detectaron las sig. diferencias:',
                          allure.attachment_type.JSON)
            print(f"Los Json NO conciden.")

        except jsonschema.SchemaError as sch_e:
            data = {sch_e.path[0]: sch_e.instance}
            allure.attach(json.dumps(data, sort_keys=True, indent=2), "Dado que los Json no coinciden, se detectaron las sig. diferencias:",
                          allure.attachment_type.JSON)
            print(f"Los Json NO conciden.")

    def generate_schema(self, data):
        schema = {"type": "object", "properties": {}}

        for key, value in data.items():
            value_type = type(value).__name__
            if value_type == "str":
                schema["properties"][key] = {"type": "string"}
            elif value_type == "int":
                schema["properties"][key] = {"type": "integer"}
            elif value_type == "float":
                schema["properties"][key] = {"type": "number"}
            elif value_type == "bool":
                schema["properties"][key] = {"type": "boolean"}
            elif value_type == "list":
                schema["properties"][key] = {"type": "array"}
            elif value_type == "dict":
                schema["properties"][key] = {"type": "object"}

        return schema

    ###########################################   BASES DE DATOS  ######################################################
    def set_timeout_base_sql_server(self, time_seconds):

        """
            Description:
                Configura el value de timeout (segundos) configurado para las conexiones a bases sqlServer.
            Args:
                time_seconds: Valor (int) que representa una cantidad en segundos.
        """

        Functions.set_timeout_base_sql_server(Functions(), time_seconds)

    def get_timeout_base_sql_server(self):

        """
            Description:
                Devuelve el value de timeout configurado para la conexion a bases sqlServer.
            Return:
                Devuelve el value de timeout (segundos) configurado para la conexion a bases sqlServer.
        """

        return Functions.get_timeout_base_sql_server(Functions())

    def establish_connection_sqlserver(self, db_name):

        """
            Description:
                Realiza conexión a una base de datos sqlServer.
            Args:
                db_name: nombre de la base
            Return:
                Devuelve una variable con la conexion a la base de datos sqlServer.
        """

        return Functions.establish_connection_sqlserver(Functions(), db_name)

    def check_base_sqlserver(self, db_name, query):

        """
            Description:
                Realiza conexión y consulta a base de datos con la libreria pyodbc. El metodo incluye la
                desconexión.
            Args:
                db_name: Nombre de la data base.
                query: Consulta Query.
            Returns:
                <class 'pyodbc.Row'>: Retorna un class 'pyodbc.Row' si la consulta y la conexión es exitosa. De lo
                contrario imprime por consola "Se produjo un error en la base de datos."
        """

        return Functions.check_base_sqlserver(Functions(), db_name, query)

    def execute_sp_base_sqlserver(self, db_name, query, parameters: tuple):

        """
            Description:
                Realiza conexión y consulta a base de datos con la libreria pyodbc. El metodo incluye la
                desconexión.
            Args:
                db_name (str): Nombre de la base.
                query (str): Consulta Query.
                parameters (tuple): Tupla con parametros para el sp.
            Returns:
                Lista con los resultados.
        """

        return Functions.execute_sp_base_sqlserver(Functions(), db_name, query, parameters)

    def get_list_base_sqlserver(self, db_name, query):
        """
            Description:
                Realiza conexión y consulta a base de datos con la libreria pyodbc. El metodo incluye la
                desconexión.
            Args:
                db_name (str): Nombre de la base.
                query (str): Consulta Query.
            Returns:
                Lista con los resultados.
        """

        return Functions.get_list_base_sqlserver(Functions(), db_name, query)

    def delete_reg_base_sqlserver(self, db_name, query):

        """
            Description:
                Elimina un registro de la base de datos. El método incluye la desconexión.
            Args:
                db_name: Nombre de la base.
                query: Consulta Query.
            Returns:
                Imprime por consola "Ocurrió un error en la base".
        """

        Functions.delete_reg_base_sqlserver(Functions(), db_name, query)

    def insert_reg_base_sqlserver(self, db_name, query):

        """
            Description:
                Inserta un registro de la base de datos. El método incluye la desconexión.
            Args:
                db_name: Nombre de la base.
                query: Consulta Query.
            Returns:
                Imprime por consola "Ocurrió un error en la base".
        """

        Functions.insert_row_base_sqlserver(Functions(), db_name, query)

    """def update_reg_base_sqlserver(self, db_name, query):
        Functions.update_row_base_sqlserver(Functions(), db_name, query)"""

    def establish_connection_oracle(self, db_name):

        """
            Description:
                Realiza conexión a una base de datos sqlServer.
            Args:
                db_name: nombre de la base
            Return:
                Devuelve una variable con la conexion a la base de datos sqlServer.
        """

        return Functions.establish_connection_oracle_db(Functions(), db_name)

    def check_base_oracle(self, db_name, query):

        """
            Description:
                Realiza conexión y consulta a base de datos con la libreria xOracle. El metodo incluye la
                desconexión.
            Args:
                db_name: Nombre de la data base.
                query: Consulta Query.
            Returns:
                <class 'pyodbc.Row'>: Retorna un class 'pyodbc.Row' si la consulta y la conexión es exitosa. De lo
                contrario imprime por consola "Se produjo un error en la base de datos."
        """
        return Functions.check_base_oracle_db(Functions(), db_name, query)

    def tear_down(self):

        """
            Description:
                Finaliza la ejecución cerrando el Web Driver.
        """
        try:
            if Selenium.data_cache not in ([], {}):
                Functions.create_grid_by_sources(self.data_cache, "Datos del cache")
                print("====================Inicio Cache===================")
                pprint.pprint(Selenium.data_cache)
                print("=====================Fin Cache=====================")
            Functions.LoggingFeature(f"AGUARDANDO: Se cerrará el web driver.").send_log()

        except Exception as e:
            Functions.exception_logger(e)

        finally:
            Functions.LoggingFeature(f"REALIZADO: Finaliza la ejecución.").send_log()
