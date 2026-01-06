/* =========================
   UTILITY
========================= */
async function sendForm(form, url) {
    const data = Object.fromEntries(new FormData(form));

    const res = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    return res;
}

/* =========================
   LOGIN
========================= */
const loginForm = document.getElementById("loginForm");

if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const data = Object.fromEntries(new FormData(loginForm));

        const res = await fetch("/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        const result = await res.json();

        if (res.ok && result.redirect) {
            window.location.href = result.redirect;
        } else {
            alert("Credenziali errate");
        }
    });
}

/* =========================
   REGISTRAZIONE
========================= */
const registerForm = document.getElementById("registerForm");

if (registerForm) {
    registerForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const res = await sendForm(registerForm, "/register");

        if (res.ok) {
            alert("Registrazione completata");
            window.location.href = "/login";
        } else {
            alert("Errore durante la registrazione");
        }
    });
}

/* =========================
   NUOVO POST + IA
========================= */
const postForm = document.getElementById("postForm");

if (postForm) {
    postForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const submitBtn = postForm.querySelector("button");
        submitBtn.disabled = true;

        const data = Object.fromEntries(new FormData(postForm));

        const res = await fetch("/posts", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        const result = await res.json();
        submitBtn.disabled = false;

        if (!res.ok) {
            alert("Errore creazione post");
            return;
        }

        // ❌ BLOCCATO DALL'IA → POPUP
        if (result.stato === "bloccato") {
            openAppelloPopup(result.post_id);
        }
        // ✅ PUBBLICATO → FEED
        else {
            window.location.href = "/feed";
        }
    });
}

/* =========================
   POPUP APPELLO
========================= */
function openAppelloPopup(postId) {
    const popup = document.getElementById("appelloPopup");
    const form = document.getElementById("appelloForm");

    if (!popup || !form) {
        console.error("Popup o form appello non trovati");
        return;
    }

    form.action = "/fact_checker/appelli/create/" + postId;

    popup.style.display = "block";
}
function closePopup() {
    const popup = document.getElementById("appelloPopup");
    if (popup) popup.style.display = "none";
}
/* =========================
   POPUP SEGNALAZIONE
========================= */
function openSegnalaPopup(postId) {
    const popup = document.getElementById("segnalaPopup");
    const form = document.getElementById("segnalaForm");

    if (!popup || !form) {
        console.error("Popup segnalazione non trovato");
        return;
    }

    form.action = "/segnala/" + postId;
    popup.style.display = "block";
}

function closeSegnalaPopup() {
    const popup = document.getElementById("segnalaPopup");
    if (popup) popup.style.display = "none";
}