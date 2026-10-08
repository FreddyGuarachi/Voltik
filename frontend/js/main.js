// Archivo principal: el único que carga el HTML.
// Maneja el login, el menú y qué sección se ve.
// Lo de cada sección está en su propio archivo dentro de views/.

import { downloadFile } from "./api.js";
import { login, logout } from "./auth.js";
import { getToken, getRole } from "./session.js";
import { showMessage, showError } from "./ui.js";
import { loadProducts } from "./views/products.js";
import { loadBrands } from "./views/brands.js";
import { loadSales } from "./views/sales.js";
import { loadRestock } from "./views/restock.js";
import { loadUsers } from "./views/users.js";

const loginForm = document.getElementById("login-form");
const usernameInput = document.getElementById("login-username");
const passwordInput = document.getElementById("login-password");
const nav = document.getElementById("main-nav");
const sections = document.querySelectorAll("section");

// Muestra solo la sección con ese id y oculta las demás.
function showSection(sectionId) {
  for (const section of sections) {
    section.hidden = section.id !== sectionId;
  }
  showMessage(""); // Borra el mensaje de la sección anterior
}

// Pasa del login a la aplicación.
function startApp() {
  nav.hidden = false;

  if (getRole() === "admin") {
    showSection("products-section");
    loadProducts();
  } else {
    // Al vendedor le ocultamos los botones de administrador.
    for (const button of document.querySelectorAll(".admin-only")) {
      button.hidden = true;
    }
    showSection("sales-section");
    loadSales();
  }
}

// ---------- Login ----------

loginForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  try {
    await login(usernameInput.value, passwordInput.value);
    loginForm.reset();
    startApp();
  } catch (error) {
    showError(error.message);
  }
});

// ---------- Menú ----------

document.getElementById("nav-products").addEventListener("click", () => {
  showSection("products-section");
  loadProducts();
});

document.getElementById("nav-brands").addEventListener("click", () => {
  showSection("brands-section");
  loadBrands();
});

document.getElementById("nav-sales").addEventListener("click", () => {
  showSection("sales-section");
  loadSales();
});

document.getElementById("nav-restock").addEventListener("click", () => {
  showSection("restock-section");
  loadRestock();
});

document.getElementById("nav-users").addEventListener("click", () => {
  showSection("users-section");
  loadUsers();
});

document.getElementById("export-button").addEventListener("click", async () => {
  try {
    await downloadFile("/product/export?format=csv", "stock.csv");
  } catch (error) {
    showError(error.message);
  }
});

document.getElementById("logout-button").addEventListener("click", logout);

// ---------- Inicio ----------

// Si ya hay sesión guardada (por ejemplo, al recargar), entramos directo.
if (getToken()) {
  startApp();
}
