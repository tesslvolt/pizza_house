const API = "http://localhost:8000/api";
let cart = [];

async function loadPizzas() {
    const res = await fetch(`${API}/pizzas`, {
        credentials: "include"
    });

    const pizzas = await res.json();
    const container = document.getElementById("pizza-list");
    container.innerHTML = "";

    pizzas.forEach(pizza => {
        const card = document.createElement("div");
        card.className = "pizza-card";
        card.innerHTML = `
            <div class="pizza-title">${pizza.name}</div>
            <div>${pizza.description || ""}</div>
        `;

        pizza.variants.forEach(v => {
            const variant = document.createElement("div");
            variant.className = "variant";
            variant.innerHTML = `
                <span>${v.size} — ${v.price} ₽</span>
                <button>Добавить</button>
            `;

            variant.querySelector("button").onclick = () => {
                cart.push({
                    pizza_variant_id: v.id,
                    quantity: 1
                });
                alert("Добавлено в заказ");
            };

            card.appendChild(variant);
        });

        container.appendChild(card);
    });
}

async function submitOrder() {
    if (cart.length === 0) {
        alert("Корзина пуста");
        return;
    }

    const body = {
        customer_name: document.getElementById("name").value,
        customer_phone: document.getElementById("phone").value,
        items: cart
    };

    await fetch(`${API}/orders`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        credentials: "include",   // 🔥
        body: JSON.stringify(body)
    });

    alert("Заказ отправлен 🍕");
    cart = [];
}

loadPizzas();
