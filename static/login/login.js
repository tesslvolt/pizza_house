async function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const errorBox = document.getElementById("error");

    errorBox.textContent = "";

    if (!username || !password) {
        errorBox.textContent = "Введите логин и пароль";
        return;
    }

    try {
        const response = await fetch("/api/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            credentials: "include",
            body: JSON.stringify({ email: username, password: password })
        });

        if (!response.ok) {
            throw new Error("Неверный логин или пароль");
        }

        const data = await response.json();

        if (data.is_admin) {
            window.location.href = "/static/admin/admin.html";
        } else {
            window.location.href = "/static/guest/guest.html";
        }

    } catch (error) {
        errorBox.textContent = error.message;
    }
}
