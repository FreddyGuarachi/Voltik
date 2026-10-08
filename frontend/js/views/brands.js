// Vista de Marcas: listar, crear, editar y eliminar.

import { apiRequest, getAllItems } from "../api.js";
import {
  showMessage,
  showError,
  createRow,
  createButton,
  formatBoolean,
} from "../ui.js";

const form = document.getElementById("brand-form");
const nameInput = document.getElementById("brand-name");
const originInput = document.getElementById("brand-origin");
const providerInput = document.getElementById("brand-provider");
const activeInput = document.getElementById("brand-active");
const cancelButton = document.getElementById("brand-cancel");
const tableBody = document.getElementById("brands-table");

// id de la marca que se está editando. null = se está creando una nueva.
let editingId = null;

// Pide las marcas al backend y dibuja la tabla.
export async function loadBrands() {
  try {
    const brands = await getAllItems("/brand/");

    tableBody.textContent = ""; // Vacía la tabla antes de llenarla

    for (const brand of brands) {
      const row = createRow([
        brand.name,
        brand.origin,
        brand.provider,
        formatBoolean(brand.is_active),
      ]);

      const actions = document.createElement("td");
      actions.append(createButton("Editar", () => startEdit(brand)));
      actions.append(createButton("Eliminar", () => deleteBrand(brand)));
      row.append(actions);

      tableBody.append(row);
    }
  } catch (error) {
    showError(error.message);
  }
}

// Guardar: crea o edita según editingId.
form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const brand = {
    name: nameInput.value,
    origin: originInput.value,
    provider: providerInput.value,
    is_active: activeInput.checked,
  };

  try {
    if (editingId === null) {
      await apiRequest("/brand/", "POST", brand);
      showMessage("Marca creada");
    } else {
      await apiRequest(`/brand/${editingId}`, "PUT", brand);
      showMessage("Marca actualizada");
    }
    resetForm();
    loadBrands();
  } catch (error) {
    showError(error.message);
  }
});

cancelButton.addEventListener("click", resetForm);

// Pasa los datos de la marca al formulario para editarla.
function startEdit(brand) {
  editingId = brand.id;
  nameInput.value = brand.name;
  originInput.value = brand.origin;
  providerInput.value = brand.provider;
  activeInput.checked = brand.is_active;
}

async function deleteBrand(brand) {
  // confirm() muestra un cuadro Aceptar/Cancelar y devuelve true o false.
  if (!confirm(`¿Eliminar la marca "${brand.name}"?`)) {
    return;
  }

  try {
    await apiRequest(`/brand/${brand.id}`, "DELETE");
    showMessage("Marca eliminada");
    loadBrands();
  } catch (error) {
    showError(error.message);
  }
}

// Vacía el formulario y vuelve al modo "crear".
function resetForm() {
  form.reset();
  editingId = null;
}
