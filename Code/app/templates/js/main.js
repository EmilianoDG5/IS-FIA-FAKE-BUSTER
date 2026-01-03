async function sendForm(form, url) {
    const data = Object.fromEntries(new FormData(form));

    const res = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    return res;
}

const loginForm = document.getElementById("loginForm");
if (loginForm) {
    loginForm.addEventListener("submit", async e => {
        e.preventDefault();
        const res = await sendForm(loginForm, "/login");
        alert(res.ok ? "Login OK" : "Errore login");
    });
}

const registerForm = document.getElementById("registerForm");
if (registerForm) {
    registerForm.addEventListener("submit", async e => {
        e.preventDefault();
        const res = await sendForm(registerForm, "/register");
        alert(res.ok ? "Registrazione OK" : "Errore registrazione");
    });
}
