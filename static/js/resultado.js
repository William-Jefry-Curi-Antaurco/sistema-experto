"use strict";

const elementos = {
    alerta: document.querySelector("#alerta"),
    carga: document.querySelector("#resultado-carga"),
    contenido: document.querySelector("#resultado-contenido"),
    diagnosticoPrincipal: document.querySelector("#diagnostico-principal"),
    descripcionPrincipal: document.querySelector("#descripcion-principal"),
    confianzaPrincipal: document.querySelector("#confianza-principal"),
    explicacionPrincipal: document.querySelector("#explicacion-principal"),
    nivelSeveridad: document.querySelector("#nivel-severidad"),
    textoEscalamiento: document.querySelector("#texto-escalamiento"),
    listaRecomendaciones: document.querySelector("#lista-recomendaciones"),
    listaResultados: document.querySelector("#lista-resultados"),
};

function mostrarError(mensaje) {
    elementos.alerta.textContent = mensaje;
    elementos.alerta.className = "alert error";
}

async function apiRequest(url) {
    const respuesta = await fetch(url);
    let contenido = {};

    try {
        contenido = await respuesta.json();
    } catch {
        contenido = {};
    }

    if (!respuesta.ok) {
        throw new Error(
            contenido.mensaje ||
            contenido.detalle ||
            `Error HTTP ${respuesta.status}`
        );
    }

    return contenido;
}

function escaparHtml(valor) {
    const elemento = document.createElement("div");
    elemento.textContent = String(valor ?? "");
    return elemento.innerHTML;
}

function renderizarRecomendaciones(recomendaciones) {
    elementos.listaRecomendaciones.innerHTML = "";

    if (!Array.isArray(recomendaciones) || recomendaciones.length === 0) {
        elementos.listaRecomendaciones.innerHTML = `
            <p class="empty-copy">
                No existen recomendaciones registradas.
            </p>
        `;
        return;
    }

    recomendaciones.forEach((recomendacion, indice) => {
        const articulo = document.createElement("article");
        articulo.className = "recommendation-item";

        const comando = recomendacion.comando_sugerido
            ? `
                <code>${escaparHtml(recomendacion.comando_sugerido)}</code>
            `
            : "";

        articulo.innerHTML = `
            <span class="recommendation-number">${indice + 1}</span>
            <div>
                <h3>${escaparHtml(recomendacion.titulo)}</h3>
                <p>${escaparHtml(recomendacion.descripcion)}</p>
                ${comando}
            </div>
        `;

        elementos.listaRecomendaciones.appendChild(articulo);
    });
}

function renderizarResultados(resultados, idPrincipal) {
    elementos.listaResultados.innerHTML = "";

    const secundarios = resultados.filter(
        (resultado) =>
            resultado.id_diagnostico !== idPrincipal
    );

    if (secundarios.length === 0) {
        elementos.listaResultados.innerHTML = `
            <p class="empty-copy">
                No se identificaron hipótesis adicionales con evidencia suficiente.
            </p>
        `;
        return;
    }

    secundarios.forEach((resultado) => {
        const diagnostico = resultado.diagnostico || {};
        const articulo = document.createElement("article");
        articulo.className = "diagnosis-item";

        articulo.innerHTML = `
            <div>
                <span class="diagnosis-code">
                    ${escaparHtml(diagnostico.codigo || "Diagnóstico")}
                </span>
                <h3>${escaparHtml(diagnostico.nombre || "Sin nombre")}</h3>
                <p>${escaparHtml(diagnostico.descripcion || "")}</p>
            </div>

            <strong class="diagnosis-confidence">
                ${Number(resultado.porcentaje_confianza || 0).toFixed(1)}%
            </strong>
        `;

        elementos.listaResultados.appendChild(articulo);
    });
}

async function cargarResultado() {
    const idConsulta = Number(window.ID_CONSULTA);

    if (!Number.isInteger(idConsulta) || idConsulta <= 0) {
        mostrarError("El identificador de la consulta no es válido.");
        elementos.carga.classList.add("hidden");
        return;
    }

    try {
        const [principalResponse, resultadosResponse] = await Promise.all([
            apiRequest(
                `/api/diagnosticos/consultas/${idConsulta}/principal`
            ),
            apiRequest(
                `/api/diagnosticos/consultas/${idConsulta}/resultados`
            ),
        ]);

        const principal = principalResponse.datos;
        const diagnostico = principal.diagnostico || {};
        const confianza = Number(
            principal.porcentaje_confianza || 0
        );

        elementos.diagnosticoPrincipal.textContent =
            diagnostico.nombre || "Diagnóstico no disponible";
        elementos.descripcionPrincipal.textContent =
            diagnostico.descripcion || "";
        elementos.confianzaPrincipal.textContent =
            `${confianza.toFixed(1)}%`;
        elementos.explicacionPrincipal.textContent =
            principal.explicacion ||
            "No se registró una explicación para este resultado.";

        const severidad = diagnostico.nivel_severidad || "MEDIO";
        elementos.nivelSeveridad.textContent = severidad;
        elementos.nivelSeveridad.dataset.level = severidad;

        elementos.textoEscalamiento.textContent =
            diagnostico.requiere_escalamiento
                ? "Se recomienda escalar la incidencia a personal técnico."
                : "Las primeras verificaciones pueden ser realizadas por el usuario.";

        renderizarRecomendaciones(principal.recomendaciones);
        renderizarResultados(
            resultadosResponse.datos || [],
            principal.id_diagnostico
        );

        elementos.carga.classList.add("hidden");
        elementos.contenido.classList.remove("hidden");
    } catch (error) {
        elementos.carga.classList.add("hidden");
        mostrarError(error.message);
    }
}

document.addEventListener("DOMContentLoaded", cargarResultado);
