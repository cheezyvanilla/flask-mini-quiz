// static/js/login.js

document.getElementById("loginForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent form from submitting the traditional way
    
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;
    let errorMessage = document.getElementById("error-message");

    // Basic validation
    if (!username || !password) {
        errorMessage.textContent = "Both fields are required!";
        return;
    }

    // Prepare the data to send
    let data = {
        username: username,
        password: password
    };

    // Send data to the Flask API (adjust API route if needed)
    fetch('/api/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            errorMessage.textContent = data.error;
        } else {
            window.location.href = '/dashboard';  // Redirect to dashboard or another page
        }
    })
    .catch(error => {
        errorMessage.textContent = "An error occurred. Please try again.";
    });
});
