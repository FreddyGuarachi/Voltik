// Funciones para hablar con el backend.

import { getToken, clearSession } from "./session.js";

export const API_URL = "http://127.0.0.1:8000";

// Hace un pedido al backend (con el token) y devuelve la respuesta como objeto.
//   path:   ruta del endpoint, por ejemplo "/brand/"
//   method: "GET", "POST", "PUT" o "DELETE"
//   body:   datos a enviar (opcional). Se mandan como JSON.
export async function apiRequest(path, method = "GET", body = null) {
  const options = {
    method: method,
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${getToken()}`,
    },
  };

  if (body !== null) {
    options.body = JSON.stringify(body); // Objeto de JS → texto JSON
  }

  const response = await fetch(API_URL + path, options);

  // 401 = el token venció: borramos la sesión y recargamos (vuelve al login).
  if (response.status === 401) {
    clearSession();
    location.reload();
  }

  // 204 = respuesta sin contenido (por ejemplo, al eliminar).
  if (response.status === 204) {
    return null;
  }

  const data = await response.json();

  // Si el backend respondió con error, lo "lanzamos" para que lo
  // atrape el catch de quien llamó a esta función.
  if (!response.ok) {
    throw new Error(getErrorMessage(data));
  }

  return data;
}

// Los listados del backend devuelven como máximo 50 items por pedido.
// Esta función pide de a 50 (usando skip) hasta tener todos.
export async function getAllItems(path) {
  let items = [];
  let total = 1; // Valor inicial para que el while entre la primera vez

  while (items.length < total) {
    const data = await apiRequest(`${path}?skip=${items.length}&limit=50`);
    items = items.concat(data.items); // Suma los nuevos a la lista
    total = data.total;
  }

  return items;
}

// Descarga un archivo de un endpoint que pide token.
// Un link <a href> no puede mandar el token, por eso lo pedimos con fetch.
export async function downloadFile(path, fileName) {
  const response = await fetch(API_URL + path, {
    headers: { Authorization: `Bearer ${getToken()}` },
  });

  if (!response.ok) {
    throw new Error("No se pudo descargar el archivo");
  }

  const blob = await response.blob(); // El contenido del archivo
  const url = URL.createObjectURL(blob); // Una dirección temporal hacia ese contenido

  // Creamos un link invisible que apunta al archivo y le hacemos clic.
  const link = document.createElement("a");
  link.href = url;
  link.download = fileName; // Nombre con el que se guarda
  link.click();

  URL.revokeObjectURL(url); // Liberamos la dirección temporal
}

// FastAPI manda el error en "detail". Normalmente es un texto, pero en los
// errores de validación (422) es una lista: en ese caso mostramos el primero.
function getErrorMessage(data) {
  if (typeof data.detail === "string") {
    return data.detail;
  }
  return data.detail[0].msg;
}
