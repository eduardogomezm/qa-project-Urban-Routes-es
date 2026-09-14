# Obtiene el código telefónico. No lo modifique.
# El archivo no debe sufrir ninguna modificación.

def retrieve_phone_code(driver) -> str:
    """Este código obtiene el número de confirmación telefónica y lo devuelve como una cadena de texto.
Úselo cuando la aplicación esté esperando el código de confirmación, para así pasarlo a sus pruebas.
El código de confirmación telefónica solo puede obtenerse después de haber sido solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No phone confirmation code found.\n"
                            "Please use retrieve_phone_code only after the code was requested in your application.")
        return code


# Comprueba si Routes está en funcionamiento. No modificar.
def is_url_reachable(url):
    """Comprueba si se puede acceder a la URL. Pasa la URL de Urban Routes como parámetro.
Si es accesible, devuelve True; de ​​lo contrario, devuelve False."""

    import ssl
    import urllib.request

    try:
        ssl_ctx = ssl.create_default_context()
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl.CERT_NONE

        with urllib.request.urlopen(url, context=ssl_ctx) as response:
            # print("Response Status Code:", response.status) #con fines de depuración
            if response.status == 200:
                return True
            else:
                return False
    except Exception as e:
        print(e)

    return False