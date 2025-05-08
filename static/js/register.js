document.getElementById("registerForm").addEventListener("submit", async function (e) {
    e.preventDefault();
    const errorDiv = document.getElementById("error");

    const payload = {
        username: document.getElementById("username").value.trim(),
        nickname: document.getElementById("nickname").value.trim(),
        password: document.getElementById("password").value,
        confirm_password: document.getElementById("confirmPassword").value
    };

    const res = await fetch("/api/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });

    const data = await res.json();
    errorDiv.style.color = res.ok ? "green" : "red";
    errorDiv.textContent = data.message || data.error;
});
