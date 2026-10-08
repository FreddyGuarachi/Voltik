// Funciones chicas para mostrar cosas en pantalla. Las usan todas las vistas.
// Usamos siempre textContent (y no innerHTML): así ningún dato que venga
// del backend puede meter HTML en la página.

const statusMessage = document.getElementById("status-message");

export function showMessage(text) {
    statusMessage.textContent = text;
    statusMessage.className = "success";
}

export function showError(text) {
    statusMessage.textContent = text;
    statusMessage.className = "error";
}

// Crea una fila <tr> con una celda <td> por cada valor de la lista.
export function createRow(values) {
    const row = document.createElement("tr");

    for (const value of values) {
        const cell = document.createElement("td");
        cell.textContent = value;
        row.append(cell);
    }

    return row;
}

// Crea un botón que ejecuta la función onClick al hacerle clic.
export function createButton(text, onClick) {
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = text;
    button.addEventListener("click", onClick);
    return button;
}

// Crea una opción para un <select>.
export function createOption(value, text) {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = text;
    return option;
}

export function formatBoolean(value) {
    if (value) {
        return "Sí";
    }
    return "No";
}
