// Vista de Reposiciones: registrar una reposición y ver el resumen diario.

import { apiRequest, getAllItems } from "../api.js";
import { showMessage, showError, createRow, createOption } from "../ui.js";

const form = document.getElementById("restock-form");
const productSelect = document.getElementById("restock-product");
const quantityInput = document.getElementById("restock-quantity");
const tableBody = document.getElementById("restock-summary");

// Llena el <select> con los productos activos y dibuja el resumen.
export async function loadRestock() {
  try {
    const products = await getAllItems("/product/");

    productSelect.textContent = "";
    for (const product of products) {
      if (product.is_active) {
        const text = `${product.sku} - ${product.brand.name} (stock: ${product.stock})`;
        productSelect.append(createOption(product.id, text));
      }
    }

    const summary = await apiRequest("/restock/summary");

    tableBody.textContent = "";
    for (const item of summary) {
      const row = createRow([
        item.date,
        item.product_sku,
        item.brand_name,
        item.total_quantity,
      ]);
      tableBody.append(row);
    }
  } catch (error) {
    showError(error.message);
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const restock = {
    product_id: productSelect.value,
    quantity: Number(quantityInput.value),
  };

  try {
    await apiRequest("/restock/", "POST", restock);
    showMessage("Reposición registrada");
    form.reset();
    loadRestock(); // Recarga: el stock y el resumen cambiaron
  } catch (error) {
    showError(error.message);
  }
});
