# Sprint 9: Automatización de pruebas de la aplicación web para Urban Routes 🚕

Una suite de pruebas automatizadas End-to-End (E2E) robusta, mantenible y escalable desarrollada para la aplicación web **Urban Routes**. Este proyecto automatiza el flujo crítico del proceso de solicitud de viajes, implementando patrones de diseño estándar de la industria como el **Page Object Model (POM)**, estrategias de sincronización explícita e interceptación de red automatizada mediante el protocolo Chrome DevTools (CDP).
---

## 📌 Tabla de Contenidos
- [Descripción General y Cobertura Funcional](#-descripción-general-y-cobertura-funcional)
- [Arquitectura del Framework y Diseño Técnico](#-arquitectura-del-framework-y-diseño-técnico)
- [Estructura del Repositorio](#-estructura-del-repositorio)
- [Requisitos Previos del Sistema](#-requisitos-previos-del-sistema)
- [Dependencias del Framework](#-dependencias-del-framework)
- [Configuración e Instalación](#-configuración-e-instalación)
- [Actualización de Datos de Prueba Dinámicos](#-actualización-de-datos-de-prueba-dinámicos)
- [Ejecución de Pruebas y Guía de Comandos](#-ejecución-de-pruebas-y-guía-de-comandos)

---

## 📖 Descripción General y Cobertura Funcional

El objetivo principal de esta suite automatizada es realizar pruebas de regresión y validación en el flujo completo de pedidos de **Urban Routes**. La suite cubre escenarios de usuario de extremo a extremo, desde la entrada inicial de direcciones hasta la búsqueda activa del vehículo y la asignación del conductor.

### Escenarios Funcionales Automatizados:
1. **Selección de Ruta:** Configuración de las direcciones de origen ("Desde") y destino ("Hasta").
2. **Selección de Tarifa/Plan:** Selección del plan "Comfort" y verificación de los indicadores de estado activo en la interfaz.
3. **Autenticación Telefónica por SMS:** Solicitud de código de verificación e interceptación de registros de rendimiento para extraer y enviar el PIN automáticamente.
4. **Viculación de Método de Pago:** Adición de una tarjeta de crédito válida (Número de tarjeta + CVV) y vinculación al perfil.
5. **Comunicación con el Conductor:** Envío de instrucciones o comentarios personalizados para el conductor.
6. **Servicios Adicionales:** Solicitud de extras para el viaje, incluyendo mantas/pañuelos y múltiples unidades de helado.
7. **Envío del Pedido y Modal del Conductor:** Confirmación de la solicitud final del viaje y aserción de la visibilidad del modal de búsqueda de automóvil y del panel con información del conductor.

---

## 🏗️ Arquitectura del Framework y Diseño Técnico

Este framework utiliza principios de arquitectura limpia para maximizar la mantenibilidad, legibilidad y solidez de las pruebas:


```text
                                  +-----------------------+
                                  |     data.py / Env     |
                                  +-----------+-----------+
                                              |
                                              v
+-----------------------+         +-----------+-----------+         +-----------------------+
|  helpers.py (Utils &  | <-----> |   main.py (Test Suite)    | ------> |  pages.py (Page Object|
| Network Interceptors) |         |  Pytest / Assertions  |         |   Locators & Actions) |
+-----------------------+         +-----------------------+         +-----------+-----------+
                                                                                |
                                                                                v
                                                                    +-----------+-----------+
                                                                    |   Selenium WebDriver  |
                                                                    |     (Chrome Browser)  |
                                                                    +-----------------------+

📁 Estructura del Repositorio

qa-project-Urban-Routes-es/
│
├── pages.py            # Page Object Model que encapsula localizadores de UI e interacciones
├── main.py             # Suite de pruebas Pytest con casos de prueba E2E y aserciones
├── helpers.py          # Utilidades para interceptación de red y verificación de URL
├── data.py             # Constantes de datos de prueba (URLs, teléfonos, direcciones, tarjetas)
├── requirements.txt    # Declaración de dependencias del proyecto
└── README.md           # Documentación técnica y guía de ejecución

📋 Requisitos Previos del Sistema

Antes de configurar el proyecto localmente, asegúrate de que tu equipo cumpla con los siguientes requisitos:Entorno Python: Python 3.10+ (Probado y verificado en Python 3.13.5).   
Navegador: Google Chrome (Última versión estable)[cite: 5].WebDriver: Gestionado dinámicamente mediante Selenium Manager (incluido en Selenium 4+), eliminando la gestión manual de binarios chromedriver

📦 Dependencias del Framework

Plaintext
selenium>=4.0.0
pytest>=7.0.0

⚙️ Configuración e Instalación

Bash
git clone <repository_url>
cd qa-project-Urban-Routes-es


Instalar Dependencias

Bash
pip install --upgrade pip
pip install -r requirements.txt


🔄 Actualización de Datos de Prueba Dinámicos

# data.py
urban_routes_url = '[https://cnt-66de97dc-e75d-495d-8ca3-869c41abe993.containerhub.tripleten-services.com?lng=es](https://cnt-66de97dc-e75d-495d-8ca3-869c41abe993.containerhub.tripleten-services.com?lng=es)'
address_from = 'East 2nd Street, 601'
address_to = '1300 1st St'
phone_number = '+1 123 123 12 12'
card_number, card_code = '1234 5678 9100', '111'
message_for_driver = 'Muéstrame el camino al museo'


🧪 Ejecución de Pruebas y Guía de Comandos

Bash
pytest main.py

Bash
pytest -v -s main.py


