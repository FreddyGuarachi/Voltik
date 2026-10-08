// Iniciar y cerrar sesión.

import { API_URL } from "./api.js";
import { saveSession, clearSession } from "./session.js";

export async function login(username, password) {
  // /auth/login espera form-urlencoded (no JSON), por eso usamos
  // URLSearchParams en vez de apiRequest.
  const formData = new URLSearchParams();
  formData.append("username", username);
  formData.append("password", password);

  const response = await fetch(`${API_URL}/auth/login`, {
    method: "POST",
    body: formData,
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail);
  }

  saveSession(data.access_token, data.role);
}

export function logout() {
  clearSession();
  location.reload(); // Sin sesión, la página arranca en el login
}
