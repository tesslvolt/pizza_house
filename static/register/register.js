document.getElementById("register-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const errorBox = document.getElementById("error");
    errorBox.textContent = "";

    try {
        const response = await fetch("/api/auth/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.detail || "Ошибка регистрации");
        }

        alert("Регистрация успешна! Теперь можно войти.");
        window.location.href = "/static/login/login.html";

    } catch (err) {
        errorBox.textContent = err.message;
    }
});
