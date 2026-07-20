"use strict";

const PROBLEMAS_PRINCIPALES = [
    {
        id: "sin_internet",
        titulo: "No tengo Internet",
        descripcion: "No puede abrir páginas ni utilizar servicios externos.",
        icono: "🌐",
        codigos: [
            "SIN_ACCESO_INTERNET",
            "FALLA_GENERAL",
            "TODOS_SIN_INTERNET",
            "ROUTER_ENCENDIDO",
            "WAN_FALLA",
            "RECURSOS_INTERNOS_FUNCIONAN",
            "RED_LOCAL_VISIBLE",
            "CAIDA_SIMULTANEA",
            "SERVICIOS_INTERNOS_CAIDOS",
            "ICONO_RED_DESCONECTADO",
            "LUZ_PUERTO_ENCENDIDA"
        ]
    },
    {
        id: "wifi",
        titulo: "El WiFi no funciona",
        descripcion: "La conexión inalámbrica no aparece, no conecta o falla.",
        icono: "📶",
        codigos: [
            "CABLE_FUNCIONA",
            "FALLA_SOLO_WIFI",
            "RED_WIFI_APARECE",
            "VARIOS_NO_CONECTAN_WIFI",
            "WIFI_LENTO_INESTABLE",
            "SENAL_POCAS_BARRAS",
            "MEJORA_CERCA_AP",
            "MUCHOS_USUARIOS_WIFI",
            "WIFI_ACTIVO"
        ]
    },
    {
        id: "lentitud",
        titulo: "Internet está lento",
        descripcion: "Las páginas abren, pero tardan demasiado.",
        icono: "🐢",
        codigos: [
            "PAGINAS_LENTAS_PERO_ABREN",
            "VARIOS_PERCIBEN_LENTITUD",
            "OCURRE_HORARIO_ESPECIFICO",
            "TRAFICO_INTENSIVO",
            "MEJORA_CON_MENOS_USUARIOS",
            "WIFI_LENTO_INESTABLE",
            "MUCHOS_USUARIOS_WIFI"
        ]
    },
    {
        id: "intermitencia",
        titulo: "La conexión se corta",
        descripcion: "Internet desaparece y vuelve repetidamente.",
        icono: "⚡",
        codigos: [
            "CONEXION_INTERMITENTE",
            "SENAL_CAMBIA",
            "CABLE_FLOJO_DANADO",
            "PERDIDA_PAQUETES",
            "WIFI_LENTO_INESTABLE",
            "SENAL_POCAS_BARRAS"
        ]
    },
    {
        id: "un_equipo",
        titulo: "Solo falla un equipo",
        descripcion: "Los demás dispositivos funcionan con normalidad.",
        icono: "💻",
        codigos: [
            "SOLO_UN_EQUIPO",
            "OTROS_EQUIPOS_FUNCIONAN",
            "UN_EQUIPO_SIN_CONFIG",
            "CAMBIO_AJUSTES_RED",
            "EQUIPO_CONECTADO",
            "EQUIPO_DETECTA_RED",
            "WIFI_ACTIVO",
            "ICONO_RED_DESCONECTADO"
        ]
    },
    {
        id: "configuracion",
        titulo: "Aparece “sin Internet” o “red no identificada”",
        descripcion: "El equipo está conectado, pero no recibe una configuración válida.",
        icono: "⚙️",
        codigos: [
            "CONECTADO_SIN_INTERNET",
            "RED_NO_IDENTIFICADA",
            "VARIOS_CONFIG_INVALIDA",
            "IP_LINK_LOCAL",
            "UN_EQUIPO_SIN_CONFIG",
            "OTROS_EQUIPOS_FUNCIONAN",
            "CAMBIO_AJUSTES_RED"
        ]
    }
];

const AYUDAS = {
    CABLE_FUNCIONA:
        "Conecte temporalmente el equipo al router con un cable de red e intente abrir una página conocida.",
    ROUTER_ENCENDIDO:
        "Observe el router. Debe tener al menos una luz encendida. No desconecte cables desconocidos.",
    WAN_FALLA:
        "Busque una luz llamada Internet o WAN. Indique si está roja o apagada.",
    IP_LINK_LOCAL:
        "En Windows, abra Símbolo del sistema y ejecute ipconfig. Revise si la dirección comienza con 169.254.",
    LUZ_PUERTO_ENCENDIDA:
        "Observe el puerto donde está conectado el cable. Normalmente debe haber una luz encendida o parpadeando.",
    RED_WIFI_APARECE:
        "Abra la lista de redes WiFi disponibles y busque el nombre habitual de su red.",
    MEJORA_CERCA_AP:
        "Acérquese al router o punto de acceso y compruebe si la señal o velocidad mejora.",
    PERDIDA_PAQUETES:
        "Esta comprobación suele realizarla personal técnico mediante una prueba de ping continua.",
    IP_RESPONDE:
        "Esta comprobación puede requerir apoyo técnico. Puede elegir “No puedo comprobarlo”."
};

const estado = {
    idConsulta: null,
    modo: "basico",
    categorias: [],
    sintomas: [],
    respuestas: new Map(),
    problemaSeleccionado: null,
    preguntasBasicas: [],
    indiceBasico: 0
};

const elementos = {
    alerta: document.querySelector("#alerta"),
    panelInicio: document.querySelector("#panel-inicio"),
    panelSeleccionProblema: document.querySelector("#panel-seleccion-problema"),
    panelPreguntasBasico: document.querySelector("#panel-preguntas-basico"),
    panelTecnico: document.querySelector("#panel-tecnico"),
    panelCarga: document.querySelector("#panel-carga"),
    formConsulta: document.querySelector("#form-consulta"),
    btnModoBasico: document.querySelector("#btn-modo-basico"),
    btnModoTecnico: document.querySelector("#btn-modo-tecnico"),
    problemasPrincipales: document.querySelector("#problemas-principales"),
    tituloProblemaSeleccionado: document.querySelector("#titulo-problema-seleccionado"),
    descripcionProblemaSeleccionado: document.querySelector("#descripcion-problema-seleccionado"),
    contadorBasico: document.querySelector("#contador-basico"),
    barraProgresoBasico: document.querySelector("#barra-progreso-basico"),
    categoriaBasico: document.querySelector("#categoria-basico"),
    preguntaBasico: document.querySelector("#pregunta-basico"),
    ayudaBasico: document.querySelector("#ayuda-basico"),
    detalleAyuda: document.querySelector("#detalle-ayuda"),
    textoAyudaComprobacion: document.querySelector("#texto-ayuda-comprobacion"),
    botonesBasicos: document.querySelectorAll("[data-respuesta-basica]"),
    btnAnteriorBasico: document.querySelector("#btn-anterior-basico"),
    btnVolverProblemas: document.querySelector("#btn-volver-problemas"),
    btnEvaluarBasico: document.querySelector("#btn-evaluar-basico"),
    contadorTecnico: document.querySelector("#contador-tecnico"),
    buscarSintoma: document.querySelector("#buscar-sintoma"),
    filtroCategoria: document.querySelector("#filtro-categoria"),
    listaSintomas: document.querySelector("#lista-sintomas"),
    btnLimpiar: document.querySelector("#btn-limpiar"),
    btnEvaluarTecnico: document.querySelector("#btn-evaluar-tecnico")
};

function mostrarAlerta(mensaje, tipo = "error") {
    elementos.alerta.textContent = mensaje;
    elementos.alerta.className = `alert ${tipo}`;
    window.scrollTo({ top: 0, behavior: "smooth" });
}

function ocultarAlerta() {
    elementos.alerta.textContent = "";
    elementos.alerta.className = "alert hidden";
}

async function apiRequest(url, opciones = {}) {
    const respuesta = await fetch(url, {
        headers: {
            "Content-Type": "application/json",
            ...(opciones.headers || {})
        },
        ...opciones
    });

    let contenido = {};

    try {
        contenido = await respuesta.json();
    } catch {
        contenido = {};
    }

    if (!respuesta.ok) {
        const error = new Error(
            contenido.detalle ||
            contenido.mensaje ||
            `Error HTTP ${respuesta.status}`
        );

        error.status = respuesta.status;
        error.contenido = contenido;

        throw error;
    }

    return contenido;
}

function cambiarModo(modo) {
    estado.modo = modo;

    elementos.btnModoBasico.classList.toggle("active", modo === "basico");
    elementos.btnModoTecnico.classList.toggle("active", modo === "tecnico");

    if (!estado.idConsulta) {
        return;
    }

    ocultarPanelesTrabajo();

    if (modo === "basico") {
        if (estado.problemaSeleccionado) {
            elementos.panelPreguntasBasico.classList.remove("hidden");
            renderizarPreguntaBasica();
        } else {
            elementos.panelSeleccionProblema.classList.remove("hidden");
        }
    } else {
        elementos.panelTecnico.classList.remove("hidden");
        renderizarSintomasTecnicos();
    }
}

function ocultarPanelesTrabajo() {
    elementos.panelSeleccionProblema.classList.add("hidden");
    elementos.panelPreguntasBasico.classList.add("hidden");
    elementos.panelTecnico.classList.add("hidden");
    elementos.panelCarga.classList.add("hidden");
}

async function iniciarConsulta(evento) {
    evento.preventDefault();
    ocultarAlerta();

    const datosFormulario = new FormData(elementos.formConsulta);
    const nombreUsuario = String(datosFormulario.get("nombre_usuario") || "").trim();
    const descripcionProblema = String(
        datosFormulario.get("descripcion_problema") || ""
    ).trim();

    if (!nombreUsuario) {
        mostrarAlerta("Ingrese el nombre del usuario.");
        return;
    }

    const boton = elementos.formConsulta.querySelector("button[type='submit']");
    boton.disabled = true;
    boton.textContent = "Cargando información...";

    try {
        const consultaResponse = await apiRequest("/api/consultas", {
            method: "POST",
            body: JSON.stringify({
                nombre_usuario: nombreUsuario,
                descripcion_problema: descripcionProblema || "Consulta guiada"
            })
        });

        estado.idConsulta = consultaResponse.datos.id_consulta;

        const [categoriasResponse, sintomasResponse] = await Promise.all([
            apiRequest("/api/catalogos/categorias"),
            apiRequest("/api/catalogos/sintomas")
        ]);

        estado.categorias = Array.isArray(categoriasResponse.datos)
            ? categoriasResponse.datos
            : [];

        estado.sintomas = Array.isArray(sintomasResponse.datos)
            ? sintomasResponse.datos
            : [];

        if (!estado.sintomas.length) {
            throw new Error("No existen síntomas activos en la base de conocimiento.");
        }

        cargarOpcionesCategorias();
        renderizarProblemasPrincipales();

        elementos.panelInicio.classList.add("hidden");
        cambiarModo(estado.modo);
    } catch (error) {
        mostrarAlerta(error.message);
    } finally {
        boton.disabled = false;
        boton.textContent = "Iniciar diagnóstico";
    }
}

function renderizarProblemasPrincipales() {
    elementos.problemasPrincipales.innerHTML = "";

    PROBLEMAS_PRINCIPALES.forEach((problema) => {
        const boton = document.createElement("button");
        boton.type = "button";
        boton.className = "problem-card";
        boton.innerHTML = `
            <span class="problem-icon">${problema.icono}</span>
            <div>
                <h3>${escaparHtml(problema.titulo)}</h3>
                <p>${escaparHtml(problema.descripcion)}</p>
            </div>
            <span class="problem-arrow">→</span>
        `;
        boton.addEventListener("click", () => seleccionarProblema(problema));
        elementos.problemasPrincipales.appendChild(boton);
    });
}

function seleccionarProblema(problema) {
    estado.problemaSeleccionado = problema;
    estado.indiceBasico = 0;

    estado.preguntasBasicas = problema.codigos
        .map((codigo) => estado.sintomas.find((sintoma) => sintoma.codigo === codigo))
        .filter(Boolean);

    if (!estado.preguntasBasicas.length) {
        mostrarAlerta("No se encontraron síntomas relacionados con esta opción.");
        return;
    }

    elementos.tituloProblemaSeleccionado.textContent = problema.titulo;
    elementos.descripcionProblemaSeleccionado.textContent = problema.descripcion;

    elementos.panelSeleccionProblema.classList.add("hidden");
    elementos.panelPreguntasBasico.classList.remove("hidden");
    renderizarPreguntaBasica();
}

function renderizarPreguntaBasica() {
    const pregunta = estado.preguntasBasicas[estado.indiceBasico];

    if (!pregunta) {
        mostrarAlerta("No se pudo cargar la pregunta.");
        return;
    }

    elementos.categoriaBasico.textContent = obtenerNombreCategoria(
        pregunta.id_categoria
    );
    elementos.preguntaBasico.textContent = pregunta.pregunta;
    elementos.ayudaBasico.textContent =
        pregunta.descripcion || "Seleccione la respuesta que mejor corresponda.";

    const ayuda = AYUDAS[pregunta.codigo];
    elementos.detalleAyuda.classList.toggle("hidden", !ayuda);
    elementos.textoAyudaComprobacion.textContent = ayuda || "";
    elementos.detalleAyuda.open = false;

    const total = estado.preguntasBasicas.length;
    const respondidas = estado.preguntasBasicas.filter((item) =>
        estado.respuestas.has(item.id_sintoma)
    ).length;
    const avance = Math.round(((estado.indiceBasico + 1) / total) * 100);

    elementos.contadorBasico.textContent = `${respondidas}/${total}`;
    elementos.barraProgresoBasico.style.width = `${avance}%`;
    elementos.btnAnteriorBasico.disabled = estado.indiceBasico === 0;

    elementos.botonesBasicos.forEach((boton) => {
        const seleccionada =
            estado.respuestas.get(pregunta.id_sintoma) === boton.dataset.respuestaBasica;
        boton.classList.toggle("selected", seleccionada);
    });

    const ultima = estado.indiceBasico === total - 1;
    elementos.btnEvaluarBasico.classList.toggle(
        "hidden",
        !ultima || !estado.respuestas.has(pregunta.id_sintoma)
    );
}

async function seleccionarRespuestaBasica(evento) {
    const pregunta = estado.preguntasBasicas[estado.indiceBasico];
    const valor = evento.currentTarget.dataset.respuestaBasica;

    if (!pregunta) {
        return;
    }

    elementos.botonesBasicos.forEach((boton) => {
        boton.disabled = true;
    });

    try {
        await guardarRespuesta(pregunta.id_sintoma, valor);

        if (estado.indiceBasico < estado.preguntasBasicas.length - 1) {
            estado.indiceBasico += 1;
            renderizarPreguntaBasica();
        } else {
            renderizarPreguntaBasica();
        }
    } catch (error) {
        mostrarAlerta(error.message);
    } finally {
        elementos.botonesBasicos.forEach((boton) => {
            boton.disabled = false;
        });
    }
}

async function guardarRespuesta(idSintoma, valor) {
    await apiRequest(`/api/consultas/${estado.idConsulta}/respuestas`, {
        method: "POST",
        body: JSON.stringify({
            id_sintoma: idSintoma,
            valor_respuesta: valor
        })
    });

    estado.respuestas.set(idSintoma, valor);
    actualizarContadores();
}

function irAnteriorBasico() {
    if (estado.indiceBasico > 0) {
        estado.indiceBasico -= 1;
        renderizarPreguntaBasica();
    }
}

function volverAProblemas() {
    elementos.panelPreguntasBasico.classList.add("hidden");
    elementos.panelSeleccionProblema.classList.remove("hidden");
}

function cargarOpcionesCategorias() {
    elementos.filtroCategoria.innerHTML =
        '<option value="">Todas las categorías</option>';

    estado.categorias.forEach((categoria) => {
        const opcion = document.createElement("option");
        opcion.value = String(categoria.id_categoria);
        opcion.textContent = categoria.nombre;
        elementos.filtroCategoria.appendChild(opcion);
    });
}

function obtenerNombreCategoria(idCategoria) {
    const categoria = estado.categorias.find(
        (item) => Number(item.id_categoria) === Number(idCategoria)
    );

    return categoria ? categoria.nombre : "Sin categoría";
}

function obtenerSintomasFiltrados() {
    const texto = elementos.buscarSintoma.value.trim().toLowerCase();
    const categoria = elementos.filtroCategoria.value;

    return estado.sintomas.filter((sintoma) => {
        const coincideCategoria =
            !categoria ||
            Number(sintoma.id_categoria) === Number(categoria);

        const contenido = [
            sintoma.codigo,
            sintoma.nombre,
            sintoma.descripcion,
            sintoma.pregunta
        ]
            .filter(Boolean)
            .join(" ")
            .toLowerCase();

        return coincideCategoria && (!texto || contenido.includes(texto));
    });
}

function renderizarSintomasTecnicos() {
    elementos.listaSintomas.innerHTML = "";

    const sintomas = obtenerSintomasFiltrados();

    if (!sintomas.length) {
        elementos.listaSintomas.innerHTML = `
            <section class="card empty-state">
                <h3>No se encontraron síntomas</h3>
                <p>Modifique el texto de búsqueda o la categoría.</p>
            </section>
        `;
        return;
    }

    const grupos = sintomas.reduce((acumulado, sintoma) => {
        const clave = String(sintoma.id_categoria);
        acumulado[clave] ??= [];
        acumulado[clave].push(sintoma);
        return acumulado;
    }, {});

    Object.entries(grupos).forEach(([idCategoria, items]) => {
        const seccion = document.createElement("section");
        seccion.className = "symptom-group card";
        seccion.innerHTML = `
            <header class="symptom-group-header">
                <div>
                    <span class="header-label">Categoría</span>
                    <h3>${escaparHtml(obtenerNombreCategoria(idCategoria))}</h3>
                </div>
                <span class="symptom-count">${items.length} síntomas</span>
            </header>
            <div class="symptom-list"></div>
        `;

        const lista = seccion.querySelector(".symptom-list");

        items.forEach((sintoma) => {
            lista.appendChild(crearTarjetaTecnica(sintoma));
        });

        elementos.listaSintomas.appendChild(seccion);
    });
}

function crearTarjetaTecnica(sintoma) {
    const seleccionada = estado.respuestas.get(sintoma.id_sintoma);
    const articulo = document.createElement("article");
    articulo.className = "symptom-card";

    articulo.innerHTML = `
        <div class="symptom-information">
            <span class="symptom-code">${escaparHtml(sintoma.codigo)}</span>
            <h4>${escaparHtml(sintoma.pregunta)}</h4>
            <p>${escaparHtml(sintoma.descripcion || sintoma.nombre || "")}</p>
        </div>

        <div class="tri-state-control">
            ${crearBotonTecnico(sintoma.id_sintoma, "SI", "Sí", seleccionada)}
            ${crearBotonTecnico(sintoma.id_sintoma, "NO", "No", seleccionada)}
            ${crearBotonTecnico(sintoma.id_sintoma, "NO_SE", "No sé", seleccionada)}
        </div>
    `;

    articulo.querySelectorAll("[data-respuesta-tecnica]").forEach((boton) => {
        boton.addEventListener("click", seleccionarRespuestaTecnica);
    });

    return articulo;
}

function crearBotonTecnico(idSintoma, valor, etiqueta, seleccionada) {
    return `
        <button
            type="button"
            class="state-button ${seleccionada === valor ? "selected" : ""}"
            data-id-sintoma="${idSintoma}"
            data-respuesta-tecnica="${valor}"
        >
            ${etiqueta}
        </button>
    `;
}

async function seleccionarRespuestaTecnica(evento) {
    const boton = evento.currentTarget;
    const idSintoma = Number(boton.dataset.idSintoma);
    const valor = boton.dataset.respuestaTecnica;
    const tarjeta = boton.closest(".symptom-card");

    tarjeta.querySelectorAll("button").forEach((item) => {
        item.disabled = true;
    });

    try {
        await guardarRespuesta(idSintoma, valor);

        tarjeta.querySelectorAll("[data-respuesta-tecnica]").forEach((item) => {
            item.classList.toggle(
                "selected",
                item.dataset.respuestaTecnica === valor
            );
        });
    } catch (error) {
        mostrarAlerta(error.message);
    } finally {
        tarjeta.querySelectorAll("button").forEach((item) => {
            item.disabled = false;
        });
    }
}

function actualizarContadores() {
    elementos.contadorTecnico.textContent = String(estado.respuestas.size);

    if (estado.preguntasBasicas.length) {
        const respondidas = estado.preguntasBasicas.filter((item) =>
            estado.respuestas.has(item.id_sintoma)
        ).length;
        elementos.contadorBasico.textContent =
            `${respondidas}/${estado.preguntasBasicas.length}`;
    }
}

function limpiarRespuestasVisuales() {
    estado.respuestas.clear();
    renderizarSintomasTecnicos();
    actualizarContadores();
}

async function evaluarConsulta() {
    ocultarAlerta();

    if (!estado.idConsulta) {
        mostrarAlerta("No existe una consulta activa.");
        return;
    }

    if (!estado.respuestas.size) {
        mostrarAlerta(
            "Responda al menos una pregunta antes de continuar."
        );
        return;
    }

    const botonesEvaluar = [
        elementos.btnEvaluarBasico,
        elementos.btnEvaluarTecnico
    ].filter(Boolean);

    botonesEvaluar.forEach((boton) => {
        boton.disabled = true;
    });

    ocultarPanelesTrabajo();
    elementos.panelCarga.classList.remove("hidden");

    try {
        const evaluacion = await apiRequest(
            `/api/diagnosticos/consultas/${estado.idConsulta}/evaluar`,
            {
                method: "POST",
                body: JSON.stringify({})
            }
        );

        console.log(
            "Resultado completo del motor:",
            evaluacion
        );

        const datosEvaluacion = evaluacion?.datos || {};

        const cantidadReglasActivadas = Number(
            datosEvaluacion.cantidad_reglas_activadas || 0
        );

        const resultados = Array.isArray(
            datosEvaluacion.resultados
        )
            ? datosEvaluacion.resultados
            : [];

        if (
            cantidadReglasActivadas === 0 ||
            resultados.length === 0
        ) {
            throw new Error(
                "Ninguna regla de diagnóstico coincidió con las respuestas. " +
                "Responda más preguntas relacionadas con el problema y vuelva a intentarlo."
            );
        }

        const principal = await apiRequest(
            `/api/diagnosticos/consultas/${estado.idConsulta}/principal`,
            {
                method: "GET"
            }
        );

        if (!principal?.datos) {
            throw new Error(
                "No se encontró un diagnóstico principal."
            );
        }

        window.location.href =
            `/resultado/${estado.idConsulta}`;

    } catch (error) {
        console.error(
            "Error al generar diagnóstico:",
            error
        );

        elementos.panelCarga.classList.add("hidden");

        if (estado.modo === "basico") {
            elementos.panelPreguntasBasico.classList.remove(
                "hidden"
            );
        } else {
            elementos.panelTecnico.classList.remove(
                "hidden"
            );
        }

        mostrarAlerta(
            error.message ||
            "No se pudo ejecutar el motor de inferencia."
        );

    } finally {
        botonesEvaluar.forEach((boton) => {
            boton.disabled = false;
        });
    }
}

function escaparHtml(valor) {
    const elemento = document.createElement("div");
    elemento.textContent = String(valor ?? "");
    return elemento.innerHTML;
}

elementos.formConsulta.addEventListener("submit", iniciarConsulta);
elementos.btnModoBasico.addEventListener("click", () => cambiarModo("basico"));
elementos.btnModoTecnico.addEventListener("click", () => cambiarModo("tecnico"));
elementos.botonesBasicos.forEach((boton) => {
    boton.addEventListener("click", seleccionarRespuestaBasica);
});
elementos.btnAnteriorBasico.addEventListener("click", irAnteriorBasico);
elementos.btnVolverProblemas.addEventListener("click", volverAProblemas);
elementos.btnEvaluarBasico.addEventListener("click", evaluarConsulta);

elementos.buscarSintoma.addEventListener("input", renderizarSintomasTecnicos);
elementos.filtroCategoria.addEventListener("change", renderizarSintomasTecnicos);
elementos.btnLimpiar.addEventListener("click", limpiarRespuestasVisuales);
elementos.btnEvaluarTecnico.addEventListener("click", evaluarConsulta);
