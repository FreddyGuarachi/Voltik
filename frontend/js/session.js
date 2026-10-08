// Guarda, lee y borra los datos de la sesión (token y rol) en el navegador.

export function saveSession(token, role) {
  localStorage.setItem("token", token);
  localStorage.setItem("role", role);
}

export function getToken() {
  return localStorage.getItem("token");
}

export function getRole() {
  return localStorage.getItem("role");
}

export function clearSession() {
  localStorage.removeItem("token");
  localStorage.removeItem("role");
}
