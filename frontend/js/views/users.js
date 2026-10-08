// Vista de Usuarios: listar, crear, editar y eliminar.

import { apiRequest, getAllItems } from "../api.js";
import {
  showMessage,
  showError,
  createRow,
  createButton,
  formatBoolean,
} from "../ui.js";

const form = document.getElementById("user-form");
const nameInput = document.getElementById("user-name");
const passwordInput = document.getElementById("user-password");
const roleSelect = document.getElementById("user-role");
const activeInput = document.getElementById("user-active");
const cancelButton = document.getElementById("user-cancel");
const tableBody = document.getElementById("users-table");

// id del usuario que se está editando. null = se está creando uno nuevo.
let editingId = null;

export async function loadUsers() {
  try {
    const users = await getAllItems("/user/");

    tableBody.textContent = "";

    for (const user of users) {
      const row = createRow([
        user.user_name,
        user.role,
        formatBoolean(user.is_active),
      ]);

      const actions = document.createElement("td");
      actions.append(createButton("Editar", () => startEdit(user)));
      actions.append(createButton("Eliminar", () => deleteUser(user)));
      row.append(actions);

      tableBody.append(row);
    }
  } catch (error) {
    showError(error.message);
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const user = {
    user_name: nameInput.value,
    role: roleSelect.value,
    is_active: activeInput.checked,
  };

  // Al editar, si la contraseña queda vacía no se envía
  // y el backend mantiene la que ya tenía.
  if (passwordInput.value !== "") {
    user.password = passwordInput.value;
  }

  try {
    if (editingId === null) {
      await apiRequest("/user/", "POST", user);
      showMessage("Usuario creado");
    } else {
      await apiRequest(`/user/${editingId}`, "PUT", user);
      showMessage("Usuario actualizado");
    }
    resetForm();
    loadUsers();
  } catch (error) {
    showError(error.message);
  }
});

cancelButton.addEventListener("click", resetForm);

function startEdit(user) {
  editingId = user.id;
  nameInput.value = user.user_name;
  roleSelect.value = user.role;
  activeInput.checked = user.is_active;

  // La contraseña no viene del backend: al editar el campo es opcional.
  passwordInput.value = "";
  passwordInput.required = false;
}

async function deleteUser(user) {
  if (!confirm(`¿Eliminar el usuario "${user.user_name}"?`)) {
    return;
  }

  try {
    await apiRequest(`/user/${user.id}`, "DELETE");
    showMessage("Usuario eliminado");
    loadUsers();
  } catch (error) {
    showError(error.message);
  }
}

// Vuelve al modo "crear": ahí la contraseña sí es obligatoria.
function resetForm() {
  form.reset();
  editingId = null;
  passwordInput.required = true;
}
