// Vista de Productos: listar, crear, editar y eliminar.

import { apiRequest, getAllItems } from "../api.js";
import {
  showMessage,
  showError,
  createRow,
  createButton,
  createOption,
  formatBoolean,
} from "../ui.js";

const form = document.getElementById("product-form");
const skuInput = document.getElementById("product-sku");
const brandSelect = document.getElementById("product-brand");
const stockInput = document.getElementById("product-stock");
const ahInput = document.getElementById("product-ah");
const ccaInput = document.getElementById("product-cca");
const voltageInput = document.getElementById("product-voltage");
const activeInput = document.getElementById("product-active");
const cancelButton = document.getElementById("product-cancel");
const tableBody = document.getElementById("products-table");

// id del producto que se está editando. null = se está creando uno nuevo.
let editingId = null;

// Carga las marcas en el <select> y dibuja la tabla de productos.
export async function loadProducts() {
  try {
    const brands = await getAllItems("/brand/");

    brandSelect.textContent = ""; // Borra las opciones anteriores
    for (const brand of brands) {
      brandSelect.append(createOption(brand.id, brand.name));
    }

    const products = await getAllItems("/product/");

    tableBody.textContent = "";

    for (const product of products) {
      const row = createRow([
        product.sku,
        product.brand.name,
        product.stock,
        product.capacity_ah,
        product.capacity_cca,
        product.voltage,
        formatBoolean(product.is_active),
      ]);

      const actions = document.createElement("td");
      actions.append(createButton("Editar", () => startEdit(product)));
      actions.append(createButton("Eliminar", () => deleteProduct(product)));
      row.append(actions);

      tableBody.append(row);
    }
  } catch (error) {
    showError(error.message);
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  // .value siempre es texto: Number() lo convierte a número.
  const product = {
    sku: skuInput.value,
    brand_id: brandSelect.value,
    stock: Number(stockInput.value),
    capacity_ah: Number(ahInput.value),
    capacity_cca: Number(ccaInput.value),
    voltage: Number(voltageInput.value),
    is_active: activeInput.checked,
  };

  try {
    if (editingId === null) {
      await apiRequest("/product/", "POST", product);
      showMessage("Producto creado");
    } else {
      await apiRequest(`/product/${editingId}`, "PUT", product);
      showMessage("Producto actualizado");
    }
    resetForm();
    loadProducts();
  } catch (error) {
    showError(error.message);
  }
});

cancelButton.addEventListener("click", resetForm);

function startEdit(product) {
  editingId = product.id;
  skuInput.value = product.sku;
  brandSelect.value = product.brand_id;
  stockInput.value = product.stock;
  ahInput.value = product.capacity_ah;
  ccaInput.value = product.capacity_cca;
  voltageInput.value = product.voltage;
  activeInput.checked = product.is_active;
}

async function deleteProduct(product) {
  if (!confirm(`¿Eliminar el producto "${product.sku}"?`)) {
    return;
  }

  try {
    await apiRequest(`/product/${product.id}`, "DELETE");
    showMessage("Producto eliminado");
    loadProducts();
  } catch (error) {
    showError(error.message);
  }
}

function resetForm() {
  form.reset();
  editingId = null;
}
