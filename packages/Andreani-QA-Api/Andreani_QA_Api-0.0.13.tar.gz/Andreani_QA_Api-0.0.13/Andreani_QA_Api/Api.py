import json
import unittest

import allure
import requests
from Andreani_QA_Functions.Functions import Functions
from Andreani_QA_parameters.Parameters import Parameters
import pprint


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


class RequestObj(Api):
    def __init__(self, response):
        super().__init__()
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

    def validate_response_by_scheme(self):
        """
            :param json_schema: La estructura deseada a analizar en formato json.
        """
        json_obtenido = self.response.json()
        #load_json_file = json.dumps(json_obtenido)
        pprint.pprint(json_obtenido)
        html_to_attach = self.construir_html_comparativo(json_obtenido, Functions.data_cache['RESPONSE ESPERADO'])
        try:
            with open("prueba.html", "w") as file_write:
                file_write.write(html_to_attach)
            file_write.close()
            allure.attach(html_to_attach, "Comparativa", allure.attachment_type.HTML)
        except Exception as e:
            print(f"Ah ocurrido un error al comparar los json: {e}")

    @staticmethod
    def construir_html_comparativo(received_json, expected_json):
        html_head_styles = r"""<head>
                                    <meta charset="UTF-8">
                                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                                    <style>
                                        /* Estilos CSS */
                                        .json-block {
                                            background-color: #f4f4f4;
                                            padding: 0.5rem;
                                            margin: 0rem 0rem 0.5rem 0rem;
                                            overflow: scroll;
                                            font-family: monospace;
                                            height: 25vh;
                                        }

                                        .isGood {
                                            border-left: 0.5rem solid;
                                            border-left-color: #279E70;
                                        }

                                        .isError {
                                            border-left: 0.5rem solid;
                                            border-left-color: #D71920 !important;
                                        }

                                        .isWarning {
                                            border-left: 0.5rem solid;
                                            border-left-color: #FFD700;
                                        }

                                        .ref {
                                            border-left: 0.5rem solid;
                                            border-left-color: #4E63D7;
                                        }

                                        .title {
                                            font-family: Arial, Helvetica, sans-serif;
                                            font-size: 18px;
                                            margin: 1rem 0rem 1rem 0rem;
                                            color: #616161;
                                        }

                                        .code {
                                            border-radius: 5px;
                                            padding: 1rem;
                                            margin: 1rem;
                                            background-color: #E7E9EB;
                                        }

                                        .line {
                                            display: inline-block;
                                            padding-top: 0.25rem;
                                            padding-bottom: 0.25rem;
                                        }

                                        .different-key {
                                            cursor: pointer;
                                            opacity: 0.5;
                                            border: 1px solid black;
                                            border-radius: 5px;
                                        }

                                        .different-value {
                                            cursor: pointer;
                                            border-color: #D71920;
                                            border-style: dashed;
                                        }

                                        .different-others {
                                            cursor: pointer;
                                            border-color: #FFD700;
                                            border-style: dashed;
                                        }

                                        .key {
                                            color: blue;
                                        }

                                        .string {
                                            color: green;
                                        }

                                        .number {
                                            color: purple;
                                        }

                                        .boolean {
                                            color: #FF00FF;
                                        }

                                        .null {
                                            color: gray;
                                        }

                                        span {
                                            margin-bottom: 5rem;
                                            /* Ajusta el valor según lo que necesites */
                                        }

                                        .warning {
                                            background: #f4f4f4;
                                            display: block;
                                            padding: 0.5rem 0rem 0rem 0.5rem;
                                            margin: 0rem;
                                            font-family: Arial, Helvetica, sans-serif;
                                        }
                                    </style>
                                </head>"""
        html_body = """<body>
                        <div class="code">
                            <div class="title">
                                <span>Estructura esperada</span>
                            </div>
                            <div class="json-block isGood" style="white-space: pre-wrap;">
                                <div id="expected-json"></div>
                            </div>
                        </div>
                        <div class="code">
                            <div class="title">
                                <span>Estructura obtenida</span>
                            </div>
                            <div><span class="warning isGood" id="message">
                            </div>
                            <div class="json-block isGood" id="receivedJson" style="white-space: pre-wrap;">
                                <div id="received-json"></div>
                            </div>
                        </div>
                        <div class="code">
                            <div class="title"><span>Referencias de errores</span></div>
                            <div class="json-block ref" style="overflow: auto !important; height: auto;">
                                <div class="line">
                                    <span class="different-key key" title="Esta clave y valor no se encuentran presente.">"Keyword"</span>
                                    <span>: Indica que la clave debería existir en la estructura obtenida.</span>
                                </div><br>
                                <div class="line">
                                    <span class="different-key key" title="Esta clave y valor no se encuentran presente.">"..."</span>
                                    <span>: Indica que se perdieron valores esperados.</span>
                                </div><br>
                                <div class="line">
                                    <span class="different-others key" title="Esta clave no existe en el json esperado.">"Keyword"</span>
                                    <span>: Indica que se obtuvo una clave no esperada.</span>
                                </div><br>
                                <div class="line">
                                    <span class="different-value string" title="El tipo de valor no es el esperado.">"value"</span>
                                    <span>: Indica que el tipo de valor no coincide con el esperado para la clave recuperada.</span>
                                </div>
                            </div>
                        </div>
                    </body>"""
        script_json = f"""<script>
                    var receivedJson = {received_json};
                    var expectedJson = {expected_json};
                    </script>"""
        scripts = r"""<script>
                    // Función para dar formato y resaltar las diferencias entre dos JSON
                    function formatAndHighlightJson(expected, received) {
                        // Convertir los JSON en objetos para comparar las claves y los valores
                        var expectedObj = JSON.parse(JSON.stringify(expected));
                        var receivedObj = JSON.parse(JSON.stringify(received));
                        if (Array.isArray(expectedObj) && Array.isArray(receivedObj)) {
                            if (expectedObj.length !== receivedObj.length) {
                                if (!document.getElementById("receivedJson").classList.contains("isError")) {
                                    document.getElementById("receivedJson").classList.add("isWarning");
                                    document.getElementById("message").innerHTML = "<b>Atención: </b>Se han encontrado diferencias en la cantidad de objetos. Se sugiere revisar manualmente.</span></div>";
                                    document.getElementById("message").classList.add("isWarning");
                                }
                                console.log("hay diferencias");
                            }
                        }

                        for (var key in receivedObj) {
                            if (!expectedObj.hasOwnProperty(key)) {
                                if (!/~~/.test(key)) {
                                    if (isNaN(Number(key))) {
                                        receivedObj["--" + key + "--"] = receivedObj[key]; // "Esta clave no existe en el json esperado."
                                        delete receivedObj[key];
                                    }
                                    if (!document.getElementById("receivedJson").classList.contains("isError")) {
                                        document.getElementById("receivedJson").classList.add("isWarning");
                                    }
                                }
                            } else {
                                console.log(key);
                            }
                        }

                        // Iterar sobre las claves del JSON esperado
                        for (var key in expectedObj) {
                            if (Array.isArray(expectedObj[key]) && Array.isArray(receivedObj[key])) {
                                if (expectedObj[key].length !== receivedObj[key].length) {
                                    if (!document.getElementById("receivedJson").classList.contains("isError")) {
                                        document.getElementById("receivedJson").classList.add("isWarning");
                                        document.getElementById("message").innerHTML = "<b>Atención: </b>Se han encontrado diferencias en la cantidad de objetos. Se sugiere revisar manualmente.</span></div>";
                                        document.getElementById("message").classList.add("isWarning");
                                    }
                                }
                            }
                            if (expectedObj.hasOwnProperty(key)) {
                                // Si la clave no está presente en el JSON recibido, agregarla con un valor especial
                                if (!receivedObj.hasOwnProperty(key)) {
                                    receivedObj["~~" + key + "~~"] = "~~" + key + "~~";
                                    document.getElementById("receivedJson").classList.add("isError");
                                    document.getElementById("message").classList.add("isError");
                                }

                                // Si el tipo de valor es diferente, colorearlo en rojo
                                else if (typeof expectedObj[key] !== typeof receivedObj[key]) {
                                    eT = "E" + typeof receivedObj[key];
                                    console.log(eT)
                                    receivedObj[key] = "#" + eT + "#" + receivedObj[key];
                                    document.getElementById("receivedJson").classList.add("isError");
                                    document.getElementById("message").classList.add("isError");
                                }

                                // Si el valor es un objeto, continuar recursivamente para resaltar sus claves y valores
                                else if (typeof expectedObj[key] === 'object') {
                                    receivedObj[key] = formatAndHighlightJson(expectedObj[key], receivedObj[key]);
                                }
                            }
                        }

                        return receivedObj;
                    }

                    // Función para resaltar la sintaxis JSON
                    function syntaxHighlight(json) {
                        json = JSON.stringify(json, undefined, 4);
                        json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/\n/g, '<br>'); // Reemplazar saltos de línea con <br>
                        return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
                            var cls = 'number';
                            if (/^"/.test(match)) {
                                if (/:$/.test(match)) {
                                    cls = 'key';
                                    if (/~~/.test(match)) {
                                        match = match.replace(/\~{2}/g, '');
                                        return '<div class="line"><span class="different-key ' + cls + '" title="Esta clave y valor no se encuentran presente.">' + match + '</span></div>';
                                    }
                                    if (/--/.test(match)) {
                                        match = match.replace(/\-{2}/g, '');
                                        return '<div class="line"><span class="different-others key" title="Esta clave no existe en el json esperado.">' + match + '</span></div>';
                                    }
                                } else {
                                    cls = 'string';
                                }
                            } else if (/true|false/.test(match)) {
                                cls = 'boolean';
                            } else if (/null/.test(match)) {
                                cls = 'null';
                            }
                            if (match.includes("~~")) {
                                match = match.replace(/\~{2}/g, '');
                                return '<div class="line"><span class="different-key ' + cls + '" title="Esta clave y valor no se encuentran presente.">...</span></div>';
                            }
                            if (match.includes("#Enumber#")) {
                                match = match.replace(/#Enumber#|"|"/g, '');
                                //cls = 'number'
                                return '<div class="line"><span class="different-value number" title="El tipo de valor no es el esperado.">' + match + '</span></div>';
                            }
                            if (match.includes("#Eobject#")) {
                                match = match.replace(/#Eobject#|"|"/g, '');
                                //cls = 'null'
                                return '<div class="line"><span class="different-value null" title="El tipo de valor no es el esperado.">' + match + '</span></div>';
                            }
                            if (match.includes("#Eboolean#")) {
                                match = match.replace(/#Eboolean#|"|"/g, '');
                                //cls = 'boolean'
                                return '<div class="line"><span class="different-value boolean" title="El tipo de valor no es el esperado.">' + match + '</span></div>';
                            }
                            if (match.includes("#Estring#")) {
                                match = match.replace(/#Estring#|"|"/g, '');
                                //cls = 'string'
                                return '<div class="line"><span class="different-value string" title="El tipo de valor no es el esperado. '+cls +'">"' + match + '"</span></div>';
                            }
                            return '</div><span class="' + cls + '">' + match + '</span>';
                        });
                    }
                    // Mostrar JSON esperado
                    document.getElementById("expected-json").innerHTML = syntaxHighlight(expectedJson, null, 4);

                    // Mostrar las claves resaltadas y las diferencias de tipo de valor en rojo en el JSON obtenido
                    var receivedHighlighted = formatAndHighlightJson(expectedJson, receivedJson);
                    document.getElementById("received-json").innerHTML = syntaxHighlight(receivedHighlighted);
                </script>
        """
        return html_head_styles + html_body + script_json + scripts

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
