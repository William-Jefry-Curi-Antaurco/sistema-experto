from __future__ import annotations

from sqlalchemy import text

from app import create_app
from models import (
    db,
    CategoriaFalla,
    Sintoma,
    Diagnostico,
    Recomendacion,
    Regla,
    CondicionRegla,
)


app = create_app()


CATEGORIAS = [
    {
        "clave": "falla_total_internet",
        "nombre": "Falla total de Internet",
        "descripcion": "Ningún equipo puede utilizar servicios externos.",
    },
    {
        "clave": "falla_wifi",
        "nombre": "Falla exclusiva de WiFi",
        "descripcion": "La red por cable funciona, pero la conexión inalámbrica no.",
    },
    {
        "clave": "falla_equipo",
        "nombre": "Falla en un solo equipo",
        "descripcion": "La incidencia se limita a un dispositivo.",
    },
    {
        "clave": "falla_general",
        "nombre": "Falla general",
        "descripcion": "Varios o todos los equipos presentan el problema.",
    },
    {
        "clave": "lentitud",
        "nombre": "Lentitud o congestión",
        "descripcion": "La red funciona, pero las respuestas son muy lentas.",
    },
    {
        "clave": "intermitencia",
        "nombre": "Intermitencia",
        "descripcion": "La conexión se pierde y vuelve repetidamente.",
    },
    {
        "clave": "dhcp",
        "nombre": "Asignación de configuración DHCP",
        "descripcion": "Los equipos no reciben automáticamente los datos necesarios para conectarse.",
    },
    {
        "clave": "dns",
        "nombre": "Resolución de nombres DNS",
        "descripcion": "La red parece activa, pero las páginas no pueden localizarse por su nombre.",
    },
    {
        "clave": "salida_red",
        "nombre": "Salida hacia otras redes",
        "descripcion": "Existe comunicación interna, pero no se puede llegar a Internet.",
    },
    {
        "clave": "conflicto_ip",
        "nombre": "Conflicto de dirección",
        "descripcion": "Dos equipos intentan utilizar la misma dirección IPv4.",
    },
    {
        "clave": "falla_fisica",
        "nombre": "Falla física",
        "descripcion": "Cable, conector, puerto, alimentación o adaptador presentan problemas.",
    },
]


SINTOMAS = [
    # Síntomas generales
    {
        "codigo": "SIN_ACCESO_INTERNET",
        "categoria": "falla_total_internet",
        "nombre": "Sin acceso a Internet",
        "descripcion": "El usuario no puede abrir páginas o servicios externos.",
        "pregunta": "¿No puede abrir ninguna página o servicio de Internet?",
        "tipo_respuesta": "BOOLEANO",
        "orden": 10,
    },
    {
        "codigo": "FALLA_GENERAL",
        "categoria": "falla_general",
        "nombre": "Varios equipos afectados",
        "descripcion": "El problema afecta a varios equipos.",
        "pregunta": "¿Otros equipos también presentan el mismo problema?",
        "tipo_respuesta": "BOOLEANO",
        "orden": 20,
    },
    {
        "codigo": "TODOS_SIN_INTERNET",
        "categoria": "falla_general",
        "nombre": "Todos sin Internet",
        "descripcion": "Todos los usuarios están sin acceso a Internet.",
        "pregunta": "¿Todos los usuarios están sin Internet?",
        "tipo_respuesta": "BOOLEANO",
        "orden": 30,
    },
    {
        "codigo": "SOLO_UN_EQUIPO",
        "categoria": "falla_equipo",
        "nombre": "Solo un equipo afectado",
        "descripcion": "La incidencia se limita a un dispositivo.",
        "pregunta": "¿Solo su equipo presenta el problema?",
        "tipo_respuesta": "BOOLEANO",
        "orden": 40,
    },
    {
        "codigo": "OTROS_EQUIPOS_FUNCIONAN",
        "categoria": "falla_equipo",
        "nombre": "Otros equipos funcionan",
        "descripcion": "Los demás equipos navegan con normalidad.",
        "pregunta": "¿Los demás equipos pueden navegar normalmente?",
        "tipo_respuesta": "BOOLEANO",
        "orden": 50,
    },

    # Falla física y enlace
    {
        "codigo": "ICONO_RED_DESCONECTADO",
        "categoria": "falla_fisica",
        "nombre": "Ícono de red desconectado",
        "descripcion": "El sistema muestra una X, un globo o una advertencia.",
        "pregunta": "¿El ícono de red muestra una X, un globo o una advertencia?",
        "tipo_respuesta": "BOOLEANO",
        "orden": 60,
    },
    {
        "codigo": "CABLE_CONECTADO",
        "categoria": "falla_fisica",
        "nombre": "Cable conectado",
        "descripcion": "El cable se encuentra conectado en ambos extremos.",
        "pregunta": "¿El cable está conectado en ambos extremos?",
        "tipo_respuesta": "BOOLEANO",
        "orden": 70,
    },
    {
        "codigo": "LUZ_PUERTO_ENCENDIDA",
        "categoria": "falla_fisica",
        "nombre": "Luz del puerto encendida",
        "descripcion": "Existe actividad visible en el puerto de red.",
        "pregunta": "¿La luz cercana al puerto de red está encendida?",
        "tipo_respuesta": "BOOLEANO",
        "orden": 80,
    },
    {
        "codigo": "EQUIPO_DETECTA_RED",
        "categoria": "falla_fisica",
        "nombre": "Equipo detecta red",
        "descripcion": "El equipo detecta al menos una red disponible.",
        "pregunta": "¿El equipo detecta alguna red?",
        "tipo_respuesta": "BOOLEANO",
        "orden": 90,
    },
    {
        "codigo": "WIFI_ACTIVO",
        "categoria": "falla_fisica",
        "nombre": "WiFi activo",
        "descripcion": "El WiFi está encendido y el modo avión está desactivado.",
        "pregunta": "¿El WiFi está encendido y el modo avión desactivado?",
        "tipo_respuesta": "BOOLEANO",
        "orden": 100,
    },

    # Router y energía
    {
        "codigo": "ROUTER_ENCENDIDO",
        "categoria": "falla_general",
        "nombre": "Router encendido",
        "descripcion": "El router presenta luces encendidas.",
        "pregunta": "¿El router tiene alguna luz encendida?",
        "tipo_respuesta": "BOOLEANO",
        "orden": 110,
    },
    {
        "codigo": "CORTE_ENERGIA",
        "categoria": "falla_general",
        "nombre": "Corte de energía",
        "descripcion": "Se produjo un corte o problema eléctrico.",
        "pregunta": "¿Se produjo un corte de energía?",
        "tipo_respuesta": "BOOLEANO",
        "orden": 120,
    },
    {
        "codigo": "REGULADOR_APAGADO",
        "categoria": "falla_general",
        "nombre": "Regulador apagado",
        "descripcion": "El enchufe, UPS o regulador está apagado.",
        "pregunta": "¿El enchufe, UPS o regulador está apagado?",
        "tipo_respuesta": "BOOLEANO",
        "orden": 130,
    },
    {
        "codigo": "WAN_FALLA",
        "categoria": "salida_red",
        "nombre": "Luz WAN en falla",
        "descripcion": "La luz Internet o WAN está roja o apagada.",
        "pregunta": "¿La luz marcada Internet o WAN está roja o apagada?",
        "tipo_respuesta": "BOOLEANO",
        "orden": 140,
    },

    # LAN y salida
    {
        "codigo": "RECURSOS_INTERNOS_FUNCIONAN",
        "categoria": "salida_red",
        "nombre": "Recursos internos disponibles",
        "descripcion": "Impresoras, carpetas o sistemas internos siguen funcionando.",
        "pregunta": "¿Puede usar impresoras, carpetas o sistemas internos?",
        "tipo_respuesta": "BOOLEANO",
        "orden": 150,
    },
    {
        "codigo": "RED_LOCAL_VISIBLE",
        "categoria": "salida_red",
        "nombre": "Red local visible",
        "descripcion": "La red local o WiFi continúa visible.",
        "pregunta": "¿La red local o WiFi sigue apareciendo disponible?",
        "tipo_respuesta": "BOOLEANO",
        "orden": 160,
    },
    {
        "codigo": "SERVICIOS_INTERNOS_CAIDOS",
        "categoria": "falla_general",
        "nombre": "Servicios internos caídos",
        "descripcion": "También fallan servicios internos.",
        "pregunta": "¿También fallan impresoras, carpetas o sistemas internos?",
        "tipo_respuesta": "BOOLEANO",
        "orden": 170,
    },
    {
        "codigo": "CAIDA_SIMULTANEA",
        "categoria": "falla_general",
        "nombre": "Caída simultánea",
        "descripcion": "Todos perdieron conexión al mismo tiempo.",
        "pregunta": "¿Todos perdieron la conexión al mismo tiempo?",
        "tipo_respuesta": "BOOLEANO",
        "orden": 180,
    },

    # DHCP
    {
        "codigo": "CONECTADO_SIN_INTERNET",
        "categoria": "dhcp",
        "nombre": "Conectado sin Internet",
        "descripcion": "El equipo aparece conectado, pero sin Internet.",
        "pregunta": "¿El equipo aparece conectado, pero sin Internet?",
        "tipo_respuesta": "BOOLEANO",
        "orden": 190,
    },
    {
        "codigo": "RED_NO_IDENTIFICADA",
        "categoria": "dhcp",
        "nombre": "Red no identificada",
        "descripcion": "El sistema muestra el mensaje red no identificada.",
        "pregunta": "¿El sistema muestra el mensaje «red no identificada»?",
        "tipo_respuesta": "BOOLEANO",
        "orden": 200,
    },
    {
        "codigo": "VARIOS_CONFIG_INVALIDA",
        "categoria": "dhcp",
        "nombre": "Varios equipos sin configuración válida",
        "descripcion": "Varios equipos presentan el problema de configuración.",
        "pregunta": "¿Varios equipos muestran «sin Internet» o «red no identificada»?",
        "tipo_respuesta": "BOOLEANO",
        "orden": 210,
    },
    {
        "codigo": "IP_LINK_LOCAL",
        "categoria": "dhcp",
        "nombre": "Dirección 169.254 detectada",
        "descripcion": "El equipo tiene una dirección IPv4 169.254.x.x.",
        "pregunta": "¿Se comprobó que el equipo tiene una dirección que empieza con 169.254?",
        "tipo_respuesta": "BOOLEANO",
        "orden": 220,
    },
    {
        "codigo": "UN_EQUIPO_SIN_CONFIG",
        "categoria": "dhcp",
        "nombre": "Un equipo sin configuración automática",
        "descripcion": "Solo un equipo no recibe correctamente sus parámetros.",
        "pregunta": "¿Solo su equipo aparece conectado sin Internet o con red no identificada?",
        "tipo_respuesta": "BOOLEANO",
        "orden": 230,
    },
    {
        "codigo": "CAMBIO_AJUSTES_RED",
        "categoria": "dhcp",
        "nombre": "Cambios recientes de red",
        "descripcion": "El problema comenzó después de modificar ajustes.",
        "pregunta": "¿El problema comenzó después de cambiar ajustes de red?",
        "tipo_respuesta": "BOOLEANO",
        "orden": 240,
    },

    # WiFi
    {
        "codigo": "CABLE_FUNCIONA",
        "categoria": "falla_wifi",
        "nombre": "Internet por cable funciona",
        "descripcion": "La conexión cableada funciona correctamente.",
        "pregunta": "¿Por cable sí funciona Internet?",
        "tipo_respuesta": "BOOLEANO",
        "orden": 250,
    },
    {
        "codigo": "FALLA_SOLO_WIFI",
        "categoria": "falla_wifi",
        "nombre": "Falla solo por WiFi",
        "descripcion": "El problema ocurre únicamente por WiFi.",
        "pregunta": "¿El problema ocurre solamente por WiFi?",
        "tipo_respuesta": "BOOLEANO",
        "orden": 260,
    },
    {
        "codigo": "RED_WIFI_APARECE",
        "categoria": "falla_wifi",
        "nombre": "Red WiFi visible",
        "descripcion": "La red inalámbrica aparece en la lista.",
        "pregunta": "¿La red WiFi aparece en la lista de redes disponibles?",
        "tipo_respuesta": "BOOLEANO",
        "orden": 270,
    },
    {
        "codigo": "VARIOS_NO_CONECTAN_WIFI",
        "categoria": "falla_wifi",
        "nombre": "Varios dispositivos no conectan al WiFi",
        "descripcion": "Más de un dispositivo no puede conectarse.",
        "pregunta": "¿Varios dispositivos no pueden conectarse al mismo WiFi?",
        "tipo_respuesta": "BOOLEANO",
        "orden": 280,
    },
    {
        "codigo": "WIFI_LENTO_INESTABLE",
        "categoria": "falla_wifi",
        "nombre": "WiFi lento o inestable",
        "descripcion": "La conexión inalámbrica es lenta o se corta.",
        "pregunta": "¿El WiFi está lento o se corta con frecuencia?",
        "tipo_respuesta": "BOOLEANO",
        "orden": 290,
    },
    {
        "codigo": "SENAL_POCAS_BARRAS",
        "categoria": "falla_wifi",
        "nombre": "Señal débil",
        "descripcion": "La señal WiFi muestra pocas barras.",
        "pregunta": "¿La señal WiFi tiene pocas barras?",
        "tipo_respuesta": "BOOLEANO",
        "orden": 300,
    },
    {
        "codigo": "MEJORA_CERCA_AP",
        "categoria": "falla_wifi",
        "nombre": "Mejora cerca del punto de acceso",
        "descripcion": "La conexión mejora al acercarse al router o AP.",
        "pregunta": "¿La conexión mejora al acercarse al router o punto de acceso?",
        "tipo_respuesta": "BOOLEANO",
        "orden": 310,
    },
    {
        "codigo": "MUCHOS_USUARIOS_WIFI",
        "categoria": "falla_wifi",
        "nombre": "Muchos usuarios WiFi",
        "descripcion": "Hay muchas personas conectadas simultáneamente.",
        "pregunta": "¿Hay muchas personas conectadas al mismo WiFi?",
        "tipo_respuesta": "BOOLEANO",
        "orden": 320,
    },

    # Conflicto IPv4
    {
        "codigo": "MENSAJE_CONFLICTO_IP",
        "categoria": "conflicto_ip",
        "nombre": "Mensaje de conflicto IPv4",
        "descripcion": "El equipo muestra una alerta de dirección duplicada.",
        "pregunta": "¿Aparece un mensaje que menciona conflicto o dirección IP duplicada?",
        "tipo_respuesta": "BOOLEANO",
        "orden": 330,
    },
    {
        "codigo": "FALLA_AL_CONECTAR_OTRO",
        "categoria": "conflicto_ip",
        "nombre": "Falla cuando se conecta otro equipo",
        "descripcion": "La conexión falla cuando otro equipo entra a la red.",
        "pregunta": "¿La conexión falla cuando otro equipo se conecta?",
        "tipo_respuesta": "BOOLEANO",
        "orden": 340,
    },
    {
        "codigo": "IP_CONFIGURADA_MANUAL",
        "categoria": "conflicto_ip",
        "nombre": "Configuración IP manual",
        "descripcion": "Se configuraron valores de red manualmente.",
        "pregunta": "¿Se cambiaron direcciones o valores de red manualmente?",
        "tipo_respuesta": "BOOLEANO",
        "orden": 350,
    },

    # Lentitud y congestión
    {
        "codigo": "PAGINAS_LENTAS_PERO_ABREN",
        "categoria": "lentitud",
        "nombre": "Páginas lentas pero disponibles",
        "descripcion": "Las páginas tardan, pero finalmente abren.",
        "pregunta": "¿Las páginas tardan mucho, pero finalmente abren?",
        "tipo_respuesta": "BOOLEANO",
        "orden": 360,
    },
    {
        "codigo": "VARIOS_PERCIBEN_LENTITUD",
        "categoria": "lentitud",
        "nombre": "Lentitud general",
        "descripcion": "Varias personas perciben la lentitud.",
        "pregunta": "¿Varias personas perciben la misma lentitud?",
        "tipo_respuesta": "BOOLEANO",
        "orden": 370,
    },
    {
        "codigo": "OCURRE_HORARIO_ESPECIFICO",
        "categoria": "lentitud",
        "nombre": "Lentitud en horarios específicos",
        "descripcion": "La lentitud ocurre en momentos determinados.",
        "pregunta": "¿La lentitud ocurre en horarios específicos?",
        "tipo_respuesta": "BOOLEANO",
        "orden": 380,
    },
    {
        "codigo": "TRAFICO_INTENSIVO",
        "categoria": "lentitud",
        "nombre": "Tráfico intensivo",
        "descripcion": "Existen videollamadas, copias o descargas masivas.",
        "pregunta": "¿Hay videollamadas, copias o descargas masivas en ese momento?",
        "tipo_respuesta": "BOOLEANO",
        "orden": 390,
    },
    {
        "codigo": "MEJORA_CON_MENOS_USUARIOS",
        "categoria": "lentitud",
        "nombre": "Mejora con menor carga",
        "descripcion": "El rendimiento mejora cuando hay menos usuarios.",
        "pregunta": "¿La conexión mejora cuando hay menos usuarios?",
        "tipo_respuesta": "BOOLEANO",
        "orden": 400,
    },

    # Intermitencia
    {
        "codigo": "CONEXION_INTERMITENTE",
        "categoria": "intermitencia",
        "nombre": "Conexión intermitente",
        "descripcion": "La conexión se corta y regresa sola.",
        "pregunta": "¿La conexión se corta y regresa sola?",
        "tipo_respuesta": "BOOLEANO",
        "orden": 410,
    },
    {
        "codigo": "SENAL_CAMBIA",
        "categoria": "intermitencia",
        "nombre": "Señal variable",
        "descripcion": "La señal cambia constantemente.",
        "pregunta": "¿La señal cambia constantemente?",
        "tipo_respuesta": "BOOLEANO",
        "orden": 420,
    },
    {
        "codigo": "CABLE_FLOJO_DANADO",
        "categoria": "intermitencia",
        "nombre": "Cable flojo o deteriorado",
        "descripcion": "El cable presenta movimiento o deterioro.",
        "pregunta": "¿El cable está flojo o deteriorado?",
        "tipo_respuesta": "BOOLEANO",
        "orden": 430,
    },
    {
        "codigo": "PERDIDA_PAQUETES",
        "categoria": "intermitencia",
        "nombre": "Pérdida de paquetes",
        "descripcion": "Una prueba técnica confirma pérdida de paquetes.",
        "pregunta": "¿Se confirmó pérdida de paquetes durante una prueba técnica?",
        "tipo_respuesta": "BOOLEANO",
        "orden": 440,
    },

    # DNS
    {
        "codigo": "EQUIPO_CONECTADO",
        "categoria": "dns",
        "nombre": "Equipo conectado",
        "descripcion": "El equipo aparece conectado a la red.",
        "pregunta": "¿El equipo aparece conectado a la red?",
        "tipo_respuesta": "BOOLEANO",
        "orden": 450,
    },
    {
        "codigo": "IP_RESPONDE",
        "categoria": "dns",
        "nombre": "Conectividad por dirección IP",
        "descripcion": "Un recurso responde mediante su dirección IP.",
        "pregunta": "¿Puede acceder a algún recurso mediante su dirección IP?",
        "tipo_respuesta": "BOOLEANO",
        "orden": 460,
    },
    {
        "codigo": "NAVEGADOR_NO_ENCUENTRA_SERVIDOR",
        "categoria": "dns",
        "nombre": "Navegador no encuentra servidor",
        "descripcion": "El navegador no puede localizar el servidor.",
        "pregunta": "¿El navegador indica que no encuentra el servidor o la página?",
        "tipo_respuesta": "BOOLEANO",
        "orden": 470,
    },
    {
        "codigo": "FALLA_VARIAS_PAGINAS",
        "categoria": "dns",
        "nombre": "Falla en varias páginas",
        "descripcion": "El problema ocurre en varios nombres de dominio.",
        "pregunta": "¿El problema ocurre en varias páginas diferentes?",
        "tipo_respuesta": "BOOLEANO",
        "orden": 480,
    },
]


DIAGNOSTICOS = [
    {
        "codigo": "D-001",
        "categoria": "falla_fisica",
        "nombre": "Posible falla física de conexión",
        "descripcion": "Cable desconectado o dañado, puerto inactivo, conector defectuoso o adaptador deshabilitado.",
        "nivel_severidad": "MEDIO",
        "requiere_escalamiento": True,
    },
    {
        "codigo": "D-002",
        "categoria": "falla_general",
        "nombre": "Router apagado o sin alimentación",
        "descripcion": "Router apagado, desconectado de la corriente o con falla de alimentación.",
        "nivel_severidad": "ALTO",
        "requiere_escalamiento": True,
    },
    {
        "codigo": "D-003",
        "categoria": "salida_red",
        "nombre": "Problema en el router o en la salida de la red",
        "descripcion": "Falla del enlace WAN, configuración de salida incorrecta o router bloqueado.",
        "nivel_severidad": "ALTO",
        "requiere_escalamiento": True,
    },
    {
        "codigo": "D-004",
        "categoria": "dhcp",
        "nombre": "Falla general del servicio DHCP",
        "descripcion": "Servidor DHCP no disponible, rango agotado, relay defectuoso o comunicación bloqueada.",
        "nivel_severidad": "ALTO",
        "requiere_escalamiento": True,
    },
    {
        "codigo": "D-005",
        "categoria": "falla_wifi",
        "nombre": "Falla exclusiva del WiFi",
        "descripcion": "Falla del punto de acceso, radio apagada, SSID no emitido o configuración inalámbrica incorrecta.",
        "nivel_severidad": "MEDIO",
        "requiere_escalamiento": True,
    },
    {
        "codigo": "D-006",
        "categoria": "falla_wifi",
        "nombre": "Interferencia, baja cobertura o saturación inalámbrica",
        "descripcion": "Cobertura insuficiente, interferencia, canal congestionado o exceso de clientes.",
        "nivel_severidad": "MEDIO",
        "requiere_escalamiento": True,
    },
    {
        "codigo": "D-007",
        "categoria": "falla_equipo",
        "nombre": "Problema local en un solo equipo",
        "descripcion": "Adaptador, configuración, controlador, firewall, cable local o software del dispositivo.",
        "nivel_severidad": "MEDIO",
        "requiere_escalamiento": False,
    },
    {
        "codigo": "D-008",
        "categoria": "conflicto_ip",
        "nombre": "Conflicto de dirección entre equipos",
        "descripcion": "Dirección IPv4 duplicada por configuración manual, error de DHCP o reserva incorrecta.",
        "nivel_severidad": "MEDIO",
        "requiere_escalamiento": True,
    },
    {
        "codigo": "D-009",
        "categoria": "salida_red",
        "nombre": "Posible falla del proveedor o del router principal",
        "descripcion": "Interrupción del proveedor, interfaz WAN caída, autenticación o ruta de salida incorrecta.",
        "nivel_severidad": "ALTO",
        "requiere_escalamiento": True,
    },
    {
        "codigo": "D-010",
        "categoria": "falla_general",
        "nombre": "Interrupción simultánea de toda la red",
        "descripcion": "Corte eléctrico, switch principal apagado, router central caído o enlace troncal desconectado.",
        "nivel_severidad": "CRITICO",
        "requiere_escalamiento": True,
    },
    {
        "codigo": "D-011",
        "categoria": "lentitud",
        "nombre": "Congestión o saturación de la red",
        "descripcion": "Saturación de enlace, colas, tráfico excesivo o capacidad insuficiente.",
        "nivel_severidad": "MEDIO",
        "requiere_escalamiento": True,
    },
    {
        "codigo": "D-012",
        "categoria": "intermitencia",
        "nombre": "Conexión intermitente con pérdida de comunicación",
        "descripcion": "Cable defectuoso, señal WiFi inestable, interferencia, errores de puerto o congestión severa.",
        "nivel_severidad": "MEDIO",
        "requiere_escalamiento": True,
    },
    {
        "codigo": "D-013",
        "categoria": "falla_fisica",
        "nombre": "Cable desconectado, adaptador o puerto sin enlace",
        "descripcion": "Falla local de acceso físico o lógico al medio.",
        "nivel_severidad": "MEDIO",
        "requiere_escalamiento": False,
    },
    {
        "codigo": "D-014",
        "categoria": "dns",
        "nombre": "Problema del servicio DNS",
        "descripcion": "Servidor DNS no disponible, configuración incorrecta, caché dañada o bloqueo de consultas.",
        "nivel_severidad": "MEDIO",
        "requiere_escalamiento": True,
    },
    {
        "codigo": "D-015",
        "categoria": "dhcp",
        "nombre": "Un equipo no recibe configuración automática",
        "descripcion": "Cliente DHCP detenido, adaptador con error, configuración manual incorrecta o concesión dañada.",
        "nivel_severidad": "MEDIO",
        "requiere_escalamiento": False,
    },
    {
        "codigo": "D-016",
        "categoria": "salida_red",
        "nombre": "Conectividad interna sin acceso a Internet",
        "descripcion": "Gateway incorrecto, ruta de salida ausente, NAT defectuoso o enlace WAN caído.",
        "nivel_severidad": "ALTO",
        "requiere_escalamiento": True,
    },
]


REGLAS = [
    {
        "codigo": "R-001",
        "diagnostico": "D-001",
        "nombre": "Posible falla física de conexión",
        "descripcion": "Detecta una pérdida básica de comunicación antes de analizar servicios superiores.",
        "operador_logico": "AND",
        "prioridad": 95,
        "factor_confianza": 0.85,
        "fuente": "Documento del proyecto, entrevista, Tanenbaum, Stallings, Cisco y RFC 792.",
        "condiciones": [
            ("SIN_ACCESO_INTERNET", "=", "SI", 1.0),
            ("ICONO_RED_DESCONECTADO", "=", "SI", 1.0),
            ("LUZ_PUERTO_ENCENDIDA", "=", "NO", 1.0),
        ],
    },
    {
        "codigo": "R-002",
        "diagnostico": "D-002",
        "nombre": "Router apagado o sin alimentación",
        "descripcion": "Reconoce una caída general cuando el router no muestra actividad.",
        "operador_logico": "AND",
        "prioridad": 100,
        "factor_confianza": 0.95,
        "fuente": "Documento del proyecto, entrevista, Tanenbaum y Stallings.",
        "condiciones": [
            ("FALLA_GENERAL", "=", "SI", 1.0),
            ("ROUTER_ENCENDIDO", "=", "NO", 1.2),
        ],
    },
    {
        "codigo": "R-003",
        "diagnostico": "D-003",
        "nombre": "Problema en el router o en la salida de la red",
        "descripcion": "Distingue una falla de salida cuando nadie puede navegar y el router está encendido.",
        "operador_logico": "AND",
        "prioridad": 88,
        "factor_confianza": 0.85,
        "fuente": "Documento, entrevista, Kurose y Ross, Cisco y RFC 792.",
        "condiciones": [
            ("TODOS_SIN_INTERNET", "=", "SI", 1.0),
            ("ROUTER_ENCENDIDO", "=", "SI", 1.0),
            ("WAN_FALLA", "=", "SI", 1.2),
        ],
    },
    {
        "codigo": "R-004",
        "diagnostico": "D-004",
        "nombre": "Falla general del servicio DHCP",
        "descripcion": "Detecta que varios equipos no reciben configuración automática válida.",
        "operador_logico": "AND",
        "prioridad": 90,
        "factor_confianza": 0.92,
        "fuente": "Documento, entrevista, RFC 2131, RFC 3927 y Microsoft Learn.",
        "condiciones": [
            ("VARIOS_CONFIG_INVALIDA", "=", "SI", 1.0),
            ("IP_LINK_LOCAL", "=", "SI", 1.3),
        ],
    },
    {
        "codigo": "R-005",
        "diagnostico": "D-005",
        "nombre": "Falla exclusiva del WiFi",
        "descripcion": "Separa una falla inalámbrica de una falla general de Internet.",
        "operador_logico": "AND",
        "prioridad": 85,
        "factor_confianza": 0.92,
        "fuente": "Documento, entrevista, Tanenbaum y documentación Cisco Wireless.",
        "condiciones": [
            ("CABLE_FUNCIONA", "=", "SI", 1.2),
            ("FALLA_SOLO_WIFI", "=", "SI", 1.0),
            ("VARIOS_NO_CONECTAN_WIFI", "=", "SI", 1.0),
        ],
    },
    {
        "codigo": "R-006",
        "diagnostico": "D-006",
        "nombre": "Interferencia, baja cobertura o saturación inalámbrica",
        "descripcion": "Orienta el diagnóstico cuando el WiFi mejora al acercarse al punto de acceso.",
        "operador_logico": "AND",
        "prioridad": 72,
        "factor_confianza": 0.75,
        "fuente": "Documento, entrevista, Tanenbaum y Cisco Wireless.",
        "condiciones": [
            ("CABLE_FUNCIONA", "=", "SI", 1.0),
            ("WIFI_LENTO_INESTABLE", "=", "SI", 1.0),
            ("MEJORA_CERCA_AP", "=", "SI", 1.2),
        ],
    },
    {
        "codigo": "R-007",
        "diagnostico": "D-007",
        "nombre": "Problema local en un solo equipo",
        "descripcion": "Determina que la infraestructura general funciona y la causa es local.",
        "operador_logico": "AND",
        "prioridad": 75,
        "factor_confianza": 0.80,
        "fuente": "Documento, entrevista, Kurose y Ross, y Cisco.",
        "condiciones": [
            ("SOLO_UN_EQUIPO", "=", "SI", 1.0),
            ("OTROS_EQUIPOS_FUNCIONAN", "=", "SI", 1.2),
        ],
    },
    {
        "codigo": "R-008",
        "diagnostico": "D-008",
        "nombre": "Conflicto de dirección entre equipos",
        "descripcion": "Detecta que dos dispositivos intentan utilizar la misma dirección IPv4.",
        "operador_logico": "OR",
        "prioridad": 92,
        "factor_confianza": 0.95,
        "fuente": "Documento, entrevista, RFC 5227 y RFC 826.",
        "condiciones": [
            ("MENSAJE_CONFLICTO_IP", "=", "SI", 1.5),
            ("FALLA_AL_CONECTAR_OTRO", "=", "SI", 1.0),
        ],
    },
    {
        "codigo": "R-009",
        "diagnostico": "D-009",
        "nombre": "Posible falla del proveedor o del router principal",
        "descripcion": "Genera una hipótesis general cuando todos pierden Internet y la LAN sigue disponible.",
        "operador_logico": "AND",
        "prioridad": 86,
        "factor_confianza": 0.78,
        "fuente": "Documento, entrevista, Kurose y Ross, Cisco y RFC 792.",
        "condiciones": [
            ("TODOS_SIN_INTERNET", "=", "SI", 1.0),
            ("RED_LOCAL_VISIBLE", "=", "SI", 1.0),
            ("WAN_FALLA", "=", "SI", 1.1),
        ],
    },
    {
        "codigo": "R-010",
        "diagnostico": "D-010",
        "nombre": "Interrupción simultánea de toda la red",
        "descripcion": "Reconoce una caída simultánea de servicios internos y externos.",
        "operador_logico": "AND",
        "prioridad": 99,
        "factor_confianza": 0.90,
        "fuente": "Documento, entrevista, Tanenbaum y Stallings.",
        "condiciones": [
            ("CAIDA_SIMULTANEA", "=", "SI", 1.2),
            ("SERVICIOS_INTERNOS_CAIDOS", "=", "SI", 1.2),
            ("TODOS_SIN_INTERNET", "=", "SI", 1.0),
        ],
    },
    {
        "codigo": "R-011",
        "diagnostico": "D-011",
        "nombre": "Congestión o saturación de la red",
        "descripcion": "Relaciona la lentitud con periodos de alta demanda.",
        "operador_logico": "AND",
        "prioridad": 65,
        "factor_confianza": 0.72,
        "fuente": "Documento, entrevista, Kurose y Ross, y Stallings.",
        "condiciones": [
            ("PAGINAS_LENTAS_PERO_ABREN", "=", "SI", 1.0),
            ("VARIOS_PERCIBEN_LENTITUD", "=", "SI", 1.0),
            ("TRAFICO_INTENSIVO", "=", "SI", 1.0),
        ],
    },
    {
        "codigo": "R-012",
        "diagnostico": "D-012",
        "nombre": "Conexión intermitente con pérdida de comunicación",
        "descripcion": "Orienta la búsqueda cuando la conexión se corta y regresa repetidamente.",
        "operador_logico": "AND",
        "prioridad": 70,
        "factor_confianza": 0.75,
        "fuente": "Documento, entrevista, Kurose y Ross, Stallings y Cisco.",
        "condiciones": [
            ("CONEXION_INTERMITENTE", "=", "SI", 1.0),
            ("PERDIDA_PAQUETES", "=", "SI", 1.2),
        ],
    },
    {
        "codigo": "R-013",
        "diagnostico": "D-013",
        "nombre": "Cable desconectado, adaptador o puerto sin enlace",
        "descripcion": "Detecta que un equipo no puede conectarse al primer punto de red.",
        "operador_logico": "AND",
        "prioridad": 96,
        "factor_confianza": 0.90,
        "fuente": "Documento, entrevista, Tanenbaum y Stallings.",
        "condiciones": [
            ("EQUIPO_DETECTA_RED", "=", "NO", 1.0),
            ("LUZ_PUERTO_ENCENDIDA", "=", "NO", 1.2),
        ],
    },
    {
        "codigo": "R-014",
        "diagnostico": "D-014",
        "nombre": "Problema del servicio DNS",
        "descripcion": "Identifica conectividad básica disponible con falla de resolución de nombres.",
        "operador_logico": "AND",
        "prioridad": 82,
        "factor_confianza": 0.90,
        "fuente": "Documento, entrevista, RFC 1034, RFC 1035 y Kurose y Ross.",
        "condiciones": [
            ("EQUIPO_CONECTADO", "=", "SI", 1.0),
            ("IP_RESPONDE", "=", "SI", 1.2),
            ("NAVEGADOR_NO_ENCUENTRA_SERVIDOR", "=", "SI", 1.0),
        ],
    },
    {
        "codigo": "R-015",
        "diagnostico": "D-015",
        "nombre": "Un equipo no recibe configuración automática",
        "descripcion": "Distingue una falla DHCP local de una falla general del servicio.",
        "operador_logico": "AND",
        "prioridad": 78,
        "factor_confianza": 0.82,
        "fuente": "Documento, entrevista, RFC 2131, Microsoft Learn y Kurose y Ross.",
        "condiciones": [
            ("UN_EQUIPO_SIN_CONFIG", "=", "SI", 1.1),
            ("OTROS_EQUIPOS_FUNCIONAN", "=", "SI", 1.1),
        ],
    },
    {
        "codigo": "R-016",
        "diagnostico": "D-016",
        "nombre": "Conectividad interna sin acceso a Internet",
        "descripcion": "Identifica comunicación LAN disponible sin alcance hacia redes externas.",
        "operador_logico": "AND",
        "prioridad": 84,
        "factor_confianza": 0.85,
        "fuente": "Documento, entrevista, Kurose y Ross, Cisco y RFC 792.",
        "condiciones": [
            ("RECURSOS_INTERNOS_FUNCIONAN", "=", "SI", 1.2),
            ("SIN_ACCESO_INTERNET", "=", "SI", 1.0),
        ],
    },
]


RECOMENDACIONES = {
    "D-001": [
        ("Usuario: revisar conexión", "Reconecte el cable en ambos extremos y compruebe que el WiFi esté encendido.", None),
        ("Usuario: reiniciar equipo", "Reinicie el equipo una sola vez y vuelva a comprobar la conexión.", None),
        ("Técnico: revisar enlace", "Pruebe otro cable y puerto, revise el adaptador y realice ping al gateway.", "ping <puerta_de_enlace>"),
    ],
    "D-002": [
        ("Usuario: verificar energía", "Compruebe visualmente el cable de energía, el regulador y la toma eléctrica.", None),
        ("Usuario: no cambiar adaptador", "No utilice adaptadores de corriente no autorizados.", None),
        ("Técnico: revisar alimentación", "Revise adaptador, UPS, eventos eléctricos y sustituya el equipo solo tras confirmar la falla.", None),
    ],
    "D-003": [
        ("Usuario: observar luces", "Revise las luces del router sin modificar cables desconocidos.", None),
        ("Usuario: consultar mantenimiento", "Consulte si existe mantenimiento anunciado y no restablezca el router de fábrica.", None),
        ("Técnico: verificar WAN", "Compruebe interfaz WAN, gateway, rutas y estado del enlace con el proveedor.", "tracert 8.8.8.8"),
    ],
    "D-004": [
        ("Usuario: reconectar red", "Desconecte y vuelva a conectar la red; reinicie el dispositivo.", None),
        ("Usuario: no configurar IP manual", "No introduzca direcciones IP manuales sin indicación técnica.", None),
        ("Técnico: revisar DHCP", "Compruebe servidor, pool, concesiones, relay, VLAN, filtros y registros.", "ipconfig /renew"),
    ],
    "D-005": [
        ("Usuario: reiniciar WiFi", "Apague y encienda el WiFi del dispositivo y compruebe el modo avión.", None),
        ("Usuario: probar otro equipo", "Pruebe la red desde un segundo dispositivo.", None),
        ("Técnico: revisar AP", "Revise alimentación, SSID, radio, seguridad, VLAN y controladora.", None),
    ],
    "D-006": [
        ("Usuario: acercarse al AP", "Acérquese temporalmente al punto de acceso y pruebe desde otra ubicación.", None),
        ("Usuario: reducir consumo", "Cierre descargas innecesarias y evite obstáculos físicos grandes.", None),
        ("Técnico: medir radiofrecuencia", "Mida RSSI, SNR, uso de canal, reintentos y densidad de usuarios.", None),
    ],
    "D-007": [
        ("Usuario: revisión básica", "Reinicie el equipo, revise WiFi, modo avión y cable.", None),
        ("Usuario: probar otra aplicación", "Pruebe otra página o aplicación sin modificar opciones avanzadas.", None),
        ("Técnico: revisar cliente", "Revise adaptador, controlador, TCP/IP, firewall, proxy y software de seguridad.", "ipconfig /all"),
    ],
    "D-008": [
        ("Usuario: reconectar", "Reinicie el equipo y vuelva a conectarlo.", None),
        ("Usuario: no copiar configuración", "No copie direcciones ni configuraciones de otro dispositivo.", None),
        ("Técnico: corregir conflicto", "Revise ARP, reservas, exclusiones y configuraciones estáticas; renueve DHCP.", "arp -a"),
    ],
    "D-009": [
        ("Usuario: revisar avisos", "Compruebe las luces y consulte avisos del proveedor o del área de TI.", None),
        ("Usuario: registrar hora", "Registre la hora de inicio y evite reinicios repetidos.", None),
        ("Técnico: verificar proveedor", "Revise interfaz WAN, siguiente salto, traceroute y monitoreo del proveedor.", "tracert 8.8.8.8"),
    ],
    "D-010": [
        ("Usuario: confirmar energía", "Confirme si existe energía y observe las luces sin manipular cableado central.", None),
        ("Usuario: informar alcance", "Informe qué servicios dejaron de funcionar y a qué hora.", None),
        ("Técnico: continuidad", "Revise UPS, switches, router, troncales y aplique el procedimiento de recuperación.", None),
    ],
    "D-011": [
        ("Usuario: reducir tráfico", "Cierre descargas o transmisiones innecesarias.", None),
        ("Usuario: registrar horario", "Registre el horario y las aplicaciones afectadas.", None),
        ("Técnico: analizar capacidad", "Mida utilización, latencia, pérdida, colas y throughput; evalúe QoS o ampliación.", None),
    ],
    "D-012": [
        ("Usuario: identificar medio", "Indique si utiliza cable o WiFi y registre la frecuencia de los cortes.", None),
        ("Usuario: cambiar ubicación", "Si usa WiFi, pruebe otra ubicación sin mover continuamente el cable.", None),
        ("Técnico: pruebas sostenidas", "Realice pruebas por tramos, revise errores de interfaz y mida RF.", "ping -t <destino>"),
    ],
    "D-013": [
        ("Usuario: activar interfaz", "Active el WiFi, desactive el modo avión y reconecte el cable.", None),
        ("Usuario: reiniciar equipo", "Reinicie el equipo sin abrir físicamente el dispositivo.", None),
        ("Técnico: revisar puerto", "Habilite el adaptador, revise controlador, cable, puerto, velocidad y dúplex.", None),
    ],
    "D-014": [
        ("Usuario: reiniciar navegador", "Cierre y vuelva a abrir el navegador; pruebe otra página conocida.", None),
        ("Usuario: no cambiar DNS", "Reinicie o reconecte el equipo, pero no cambie servidores DNS sin autorización.", None),
        ("Técnico: comprobar DNS", "Compare resolución con nslookup, revise servidores, caché, firewall y reenviadores.", "nslookup example.com"),
    ],
    "D-015": [
        ("Usuario: reconectar WiFi", "Olvide la red WiFi, vuelva a conectarse y reinicie el dispositivo.", None),
        ("Usuario: no configurar manual", "No introduzca valores manualmente e informe que otros equipos sí funcionan.", None),
        ("Técnico: revisar DHCP local", "Revise servicio cliente DHCP, adaptador, concesión, filtros y autenticación.", "ipconfig /release && ipconfig /renew"),
    ],
    "D-016": [
        ("Usuario: confirmar servicios internos", "Confirme qué recursos internos funcionan y si otros usuarios están afectados.", None),
        ("Usuario: revisar router", "Observe las luces del router sin modificar su configuración.", None),
        ("Técnico: revisar salida", "Compruebe gateway, rutas, NAT, enlace WAN y políticas de firewall.", "tracert 8.8.8.8"),
    ],
}



TABLAS_REQUERIDAS = {
    "categorias_falla",
    "sintomas",
    "diagnosticos",
    "recomendaciones",
    "reglas",
    "condiciones_regla",
}


def obtener_definicion_columna(tabla: str, columna: str):
    return db.session.execute(
        text(
            """
            SELECT DATA_TYPE, COLUMN_TYPE, CHARACTER_MAXIMUM_LENGTH, IS_NULLABLE
            FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = :tabla
              AND COLUMN_NAME = :columna
            """
        ),
        {"tabla": tabla, "columna": columna},
    ).mappings().first()


def obtener_valores_enum(column_type: str | None) -> set[str]:
    if not column_type or not column_type.lower().startswith("enum("):
        return set()

    contenido = column_type[5:-1]
    valores = []
    actual = []
    dentro_comillas = False
    escape = False

    for caracter in contenido:
        if escape:
            actual.append(caracter)
            escape = False
            continue

        if caracter == "\\":
            escape = True
            continue

        if caracter == "'":
            dentro_comillas = not dentro_comillas
            if not dentro_comillas:
                valores.append("".join(actual))
                actual = []
            continue

        if dentro_comillas:
            actual.append(caracter)

    return set(valores)


def validar_estructura_bd():
    tablas_existentes = {
        fila["TABLE_NAME"]
        for fila in db.session.execute(
            text(
                """
                SELECT TABLE_NAME
                FROM information_schema.TABLES
                WHERE TABLE_SCHEMA = DATABASE()
                """
            )
        ).mappings()
    }

    faltantes = TABLAS_REQUERIDAS - tablas_existentes
    if faltantes:
        raise RuntimeError(
            "Faltan tablas requeridas en la base de datos: "
            + ", ".join(sorted(faltantes))
        )

    # Validar longitud del código de síntomas.
    columna_codigo = obtener_definicion_columna("sintomas", "codigo")
    if columna_codigo is None:
        raise RuntimeError("No existe la columna sintomas.codigo.")

    longitud_codigo = columna_codigo["CHARACTER_MAXIMUM_LENGTH"]
    longitud_necesaria = max(len(item["codigo"]) for item in SINTOMAS)

    if longitud_codigo is not None and longitud_codigo < longitud_necesaria:
        raise RuntimeError(
            "La columna sintomas.codigo es demasiado corta. "
            f"Longitud actual: {longitud_codigo}; "
            f"longitud mínima necesaria: {longitud_necesaria}. "
            "Ejecute: ALTER TABLE sintomas MODIFY codigo VARCHAR(60) NOT NULL;"
        )

    # Validar severidades reales.
    columna_severidad = obtener_definicion_columna(
        "diagnosticos",
        "nivel_severidad",
    )
    if columna_severidad is None:
        raise RuntimeError(
            "No existe la columna diagnosticos.nivel_severidad."
        )

    valores_bd = obtener_valores_enum(columna_severidad["COLUMN_TYPE"])
    valores_seed = {
        item["nivel_severidad"]
        for item in DIAGNOSTICOS
    }

    if valores_bd and not valores_seed.issubset(valores_bd):
        raise RuntimeError(
            "Los niveles de severidad del seed no coinciden con la BD. "
            f"BD: {sorted(valores_bd)}; seed: {sorted(valores_seed)}."
        )

    # Validar tipo de respuesta.
    columna_tipo_respuesta = obtener_definicion_columna(
        "sintomas",
        "tipo_respuesta",
    )
    if columna_tipo_respuesta is None:
        raise RuntimeError(
            "No existe la columna sintomas.tipo_respuesta."
        )

    tipos_bd = obtener_valores_enum(
        columna_tipo_respuesta["COLUMN_TYPE"]
    )
    tipos_seed = {
        item["tipo_respuesta"]
        for item in SINTOMAS
    }

    if tipos_bd and not tipos_seed.issubset(tipos_bd):
        raise RuntimeError(
            "Los tipos de respuesta del seed no coinciden con la BD. "
            f"BD: {sorted(tipos_bd)}; seed: {sorted(tipos_seed)}."
        )

    # Validar operador lógico.
    columna_operador_logico = obtener_definicion_columna(
        "reglas",
        "operador_logico",
    )
    if columna_operador_logico is None:
        raise RuntimeError(
            "No existe la columna reglas.operador_logico."
        )

    operadores_bd = obtener_valores_enum(
        columna_operador_logico["COLUMN_TYPE"]
    )
    operadores_seed = {
        item["operador_logico"]
        for item in REGLAS
    }

    if operadores_bd and not operadores_seed.issubset(operadores_bd):
        raise RuntimeError(
            "Los operadores lógicos del seed no coinciden con la BD. "
            f"BD: {sorted(operadores_bd)}; seed: {sorted(operadores_seed)}."
        )

    # Validar operador de comparación.
    columna_operador_comparacion = obtener_definicion_columna(
        "condiciones_regla",
        "operador_comparacion",
    )
    if columna_operador_comparacion is None:
        raise RuntimeError(
            "No existe la columna condiciones_regla.operador_comparacion."
        )

    comparadores_bd = obtener_valores_enum(
        columna_operador_comparacion["COLUMN_TYPE"]
    )
    comparadores_seed = {
        condicion[1]
        for regla in REGLAS
        for condicion in regla["condiciones"]
    }

    if comparadores_bd and not comparadores_seed.issubset(comparadores_bd):
        raise RuntimeError(
            "Los operadores de comparación del seed no coinciden con la BD. "
            f"BD: {sorted(comparadores_bd)}; "
            f"seed: {sorted(comparadores_seed)}."
        )

    print("Estructura de la base de datos validada correctamente.")

def get_or_create(modelo, defaults=None, **filtros):
    instancia = modelo.query.filter_by(**filtros).first()
    if instancia is not None:
        return instancia, False

    valores = dict(filtros)
    if defaults:
        valores.update(defaults)

    instancia = modelo(**valores)
    db.session.add(instancia)
    db.session.flush()
    return instancia, True


def cargar_categorias():
    categorias = {}

    for dato in CATEGORIAS:
        categoria, _ = get_or_create(
            CategoriaFalla,
            nombre=dato["nombre"],
            defaults={
                "descripcion": dato["descripcion"],
                "estado": True,
            },
        )

        categoria.descripcion = dato["descripcion"]
        categoria.estado = True
        categorias[dato["clave"]] = categoria

    return categorias


def cargar_sintomas(categorias):
    sintomas = {}

    for dato in SINTOMAS:
        sintoma, _ = get_or_create(
            Sintoma,
            codigo=dato["codigo"],
            defaults={
                "id_categoria": categorias[dato["categoria"]].id_categoria,
                "nombre": dato["nombre"],
                "descripcion": dato["descripcion"],
                "pregunta": dato["pregunta"],
                "tipo_respuesta": dato["tipo_respuesta"],
                "unidad_medida": None,
                "orden": dato["orden"],
                "estado": True,
            },
        )

        sintoma.id_categoria = categorias[dato["categoria"]].id_categoria
        sintoma.nombre = dato["nombre"]
        sintoma.descripcion = dato["descripcion"]
        sintoma.pregunta = dato["pregunta"]
        sintoma.tipo_respuesta = dato["tipo_respuesta"]
        sintoma.orden = dato["orden"]
        sintoma.estado = True
        sintomas[dato["codigo"]] = sintoma

    return sintomas


def cargar_diagnosticos(categorias):
    diagnosticos = {}

    for dato in DIAGNOSTICOS:
        diagnostico, _ = get_or_create(
            Diagnostico,
            codigo=dato["codigo"],
            defaults={
                "id_categoria": categorias[dato["categoria"]].id_categoria,
                "nombre": dato["nombre"],
                "descripcion": dato["descripcion"],
                "nivel_severidad": dato["nivel_severidad"],
                "requiere_escalamiento": dato["requiere_escalamiento"],
                "estado": True,
            },
        )

        diagnostico.id_categoria = categorias[dato["categoria"]].id_categoria
        diagnostico.nombre = dato["nombre"]
        diagnostico.descripcion = dato["descripcion"]
        diagnostico.nivel_severidad = dato["nivel_severidad"]
        diagnostico.requiere_escalamiento = dato["requiere_escalamiento"]
        diagnostico.estado = True
        diagnosticos[dato["codigo"]] = diagnostico

    return diagnosticos


def cargar_reglas(diagnosticos, sintomas):
    for dato in REGLAS:
        regla, _ = get_or_create(
            Regla,
            codigo=dato["codigo"],
            defaults={
                "id_diagnostico": diagnosticos[dato["diagnostico"]].id_diagnostico,
                "nombre": dato["nombre"],
                "descripcion": dato["descripcion"],
                "operador_logico": dato["operador_logico"],
                "prioridad": dato["prioridad"],
                "factor_confianza": dato["factor_confianza"],
                "fuente": dato["fuente"],
                "estado": True,
            },
        )

        regla.id_diagnostico = diagnosticos[dato["diagnostico"]].id_diagnostico
        regla.nombre = dato["nombre"]
        regla.descripcion = dato["descripcion"]
        regla.operador_logico = dato["operador_logico"]
        regla.prioridad = dato["prioridad"]
        regla.factor_confianza = dato["factor_confianza"]
        regla.fuente = dato["fuente"]
        regla.estado = True

        # Reemplaza las condiciones para mantener el seed sincronizado.
        CondicionRegla.query.filter_by(id_regla=regla.id_regla).delete(
            synchronize_session=False
        )
        db.session.flush()

        for codigo_sintoma, operador, valor, peso in dato["condiciones"]:
            db.session.add(
                CondicionRegla(
                    id_regla=regla.id_regla,
                    id_sintoma=sintomas[codigo_sintoma].id_sintoma,
                    operador_comparacion=operador,
                    valor_esperado=valor,
                    peso=peso,
                )
            )


def cargar_recomendaciones(diagnosticos):
    for codigo_diagnostico, recomendaciones in RECOMENDACIONES.items():
        diagnostico = diagnosticos[codigo_diagnostico]

        Recomendacion.query.filter_by(
            id_diagnostico=diagnostico.id_diagnostico
        ).delete(synchronize_session=False)

        for orden, (titulo, descripcion, comando) in enumerate(
            recomendaciones,
            start=1,
        ):
            db.session.add(
                Recomendacion(
                    id_diagnostico=diagnostico.id_diagnostico,
                    titulo=titulo,
                    descripcion=descripcion,
                    comando_sugerido=comando,
                    orden=orden,
                    estado=True,
                )
            )


def mostrar_resumen():
    print("\nResumen cargado:")
    print(f"  Categorías:       {CategoriaFalla.query.count()}")
    print(f"  Síntomas:         {Sintoma.query.count()}")
    print(f"  Diagnósticos:     {Diagnostico.query.count()}")
    print(f"  Reglas:           {Regla.query.count()}")
    print(f"  Condiciones:      {CondicionRegla.query.count()}")
    print(f"  Recomendaciones:  {Recomendacion.query.count()}")


def ejecutar_seed():
    with app.app_context():
        try:
            base_actual = db.session.execute(
                text("SELECT DATABASE()")
            ).scalar()

            print(f"Base de datos utilizada: {base_actual}")

            validar_estructura_bd()

            categorias = cargar_categorias()
            sintomas = cargar_sintomas(categorias)
            diagnosticos = cargar_diagnosticos(categorias)
            cargar_reglas(diagnosticos, sintomas)
            cargar_recomendaciones(diagnosticos)

            db.session.commit()

            print("Base de conocimiento cargada correctamente.")
            mostrar_resumen()

        except Exception as error:
            db.session.rollback()

            print("\nNo se pudo cargar la base de conocimiento.")
            print(f"Tipo: {type(error).__name__}")
            print(f"Detalle: {error}")

            raise


if __name__ == "__main__":
    ejecutar_seed()
