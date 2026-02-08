const pizzaContainer = document.getElementById("pizza-container");
const pizzaSelect = document.getElementById("pizza-select");
const errorBox = document.getElementById("error");


async function fetchPizzas() {
    pizzaContainer.innerHTML = "";
    pizzaSelect.innerHTML = "";

    const res = await fetch("/api/admin/pizzas", {
        credentials: "include"
    });

    if (!res.ok) {
        errorBox.textContent = "Ошибка при загрузке пицц";
        return;
    }

    const pizzas = await res.json();

    pizzas.forEach(pizza => {
        const card = document.createElement("div");
        card.className = "pizza-card";

        card.innerHTML = `
            ${pizza.image_url ? `<img src="${pizza.image_url}" class="pizza-img">` : ""}
            <strong>${pizza.name}</strong>
            <p>${pizza.description || ""}</p>

            <div class="variants">
                ${pizza.variants.map(v =>
                    `<div class="variant">${v.size} — $${v.price}</div>`
                ).join("")}
            </div>

            <button class="delete" onclick="deletePizza(${pizza.id})">Удалить</button>
        `;

        pizzaContainer.appendChild(card);

        const option = document.createElement("option");
        option.value = pizza.id;
        option.textContent = pizza.name;
        pizzaSelect.appendChild(option);
    });
}

async function addPizza() {
    const name = document.getElementById("pizza-name").value;
    const desc = document.getElementById("pizza-desc").value;
    const imageInput = document.getElementById("pizza-image");

    if (!name) {
        errorBox.textContent = "Введите название пиццы";
        return;
    }

    const formData = new FormData();
    formData.append("name", name);
    if (desc) formData.append("description", desc);
    if (imageInput.files.length > 0) {
        formData.append("image", imageInput.files[0]);
    }

    const res = await fetch("/api/admin/pizzas", {
        method: "POST",
        body: formData,
        credentials: "include"
    });

    if (!res.ok) {
        errorBox.textContent = "Ошибка при добавлении пиццы";
        return;
    }

    document.getElementById("pizza-name").value = "";
    document.getElementById("pizza-desc").value = "";
    imageInput.value = "";
    errorBox.textContent = "";

    await fetchPizzas();
}

async function addVariant() {
    const pizza_id = pizzaSelect.value;
    const size = document.getElementById("variant-size").value;
    const price = parseFloat(document.getElementById("variant-price").value);

    if (!pizza_id || !size || isNaN(price)) {
        errorBox.textContent = "Заполните все поля для варианта";
        return;
    }

    const res = await fetch("/api/admin/pizza-variants", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ pizza_id, size, price }),
        credentials: "include"
    });

    if (!res.ok) {
        errorBox.textContent = "Ошибка при добавлении варианта";
        return;
    }

    document.getElementById("variant-size").value = "";
    document.getElementById("variant-price").value = "";
    errorBox.textContent = "";

    await fetchPizzas();
}

async function deletePizza(id) {
    const res = await fetch(`/api/admin/pizzas/${id}`, {
        method: "DELETE",
        credentials: "include"
    });

    if (!res.ok) {
        errorBox.textContent = "Ошибка при удалении пиццы";
        return;
    }

    await fetchPizzas();
}


document.getElementById("add-pizza-btn").addEventListener("click", addPizza);
document.getElementById("add-variant-btn").addEventListener("click", addVariant);

fetchPizzas();
