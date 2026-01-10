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
let currentPostId = null;

function openSegnalaPopup(postId) {
    currentPostId = postId;
    document.getElementById("segnalaPopup").style.display = "block";
}

function closeSegnalaPopup() {
    document.getElementById("segnalaPopup").style.display = "none";
}

document.getElementById("segnalaForm")?.addEventListener("submit", async (e) => {
    e.preventDefault();

    const motivo = e.target.motivo.value;

    const res = await fetch(`/segnala/${currentPostId}`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({ motivo })
    });

    const data = await res.json();

    if (!res.ok) {
        alert(data.error); 
        return;
    }
    closeSegnalaPopup();
});


/* =========================*/
document.getElementById("registerForm")?.addEventListener("submit", async (e) => {
    e.preventDefault();

    const form = e.target;
    const errorMsg = document.getElementById("errorMsg");

    const data = {
        username: form.username.value,
        email: form.email.value,
        password: form.password.value
    };

    const res = await fetch("/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    const result = await res.json();

    if (!res.ok) {
        errorMsg.innerText = result.error;
        errorMsg.style.display = "block";
        return;
    }

    // successo
    window.location.href = "/login";
});
