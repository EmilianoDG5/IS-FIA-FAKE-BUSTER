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


const registerForm = document.getElementById("registerForm");
if (registerForm) {
    registerForm.addEventListener("submit", async e => {
        e.preventDefault();
        const res = await sendForm(registerForm, "/register");
        alert(res.ok ? "Registrazione OK" : "Errore registrazione");
    });
}const postForm = document.getElementById("postForm");

if (postForm) {
    postForm.addEventListener("submit", async e => {
        e.preventDefault();

        const submitBtn = postForm.querySelector("button[type='submit']");
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

        if (result.stato === "bloccato") {
            openAppelloPopup(result.post_id); 
        } else {
            window.location.href = "/feed";
        }
    });
}




function openAppelloPopup(postId) {
    const form = document.getElementById("appelloForm");
    form.action = "/appello/" + postId;

    document.getElementById("appelloPopup").style.display = "block";
}

function closePopup() {
    document.getElementById("appelloPopup").style.display = "none";

    const postForm = document.getElementById("postForm");
    if (postForm) {
        const submitBtn = postForm.querySelector("button[type='submit']");
        submitBtn.disabled = false;
    }
}
