// Vista de Ventas: registrar una venta y ver el resumen diario.

import { apiRequest, getAllItems } from "../api.js";
import { showMessage, showError, createRow, createOption } from "../ui.js";

const form = document.getElementById("sale-form");
const productSelect = document.getElementById("sale-product");
const quantityInput = document.getElementById("sale-quantity");
const tableBody = document.getElementById("sale-summary");

// Llena el <select> con los productos activos y dibuja el resumen.
export async function loadSales() {
  try {
    const products = await getAllItems("/product/");

    productSelect.textContent = "";
    for (const product of products) {
      if (product.is_active) {
        const text = `${product.sku} - ${product.brand.name} (stock: ${product.stock})`;
        productSelect.append(createOption(product.id, text));
      }
    }

    const summary = await apiRequest("/sale/summary");

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

  const sale = {
    product_id: productSelect.value,
    quantity: Number(quantityInput.value),
  };

  try {
    await apiRequest("/sale/", "POST", sale);
    showMessage("Venta registrada");
    form.reset();
    loadSales(); // Recarga: el stock y el resumen cambiaron
  } catch (error) {
    showError(error.message);
  }
});
