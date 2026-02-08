document.addEventListener("DOMContentLoaded", async () => {
    const container = document.getElementById("pizza-container");

    try {
        const res = await fetch("/api/pizzas", {
            credentials: "include"
        });

        const pizzas = await res.json();

        pizzas.forEach(pizza => {
            const card = document.createElement("div");
            card.className = "pizza-card";
            card.innerHTML = `
                <h3>${pizza.name}</h3>
                <p>${pizza.description || ""}</p>
                <button>В корзину</button>
            `;
            container.appendChild(card);
        });

    } catch (err) {
        container.innerHTML = "<p>Не удалось загрузить пиццы 😔</p>";
        console.error(err);
    }

    document.getElementById("login-btn").addEventListener("click", () => {
        window.location.href = "/static/login/login.html";
    });
});
