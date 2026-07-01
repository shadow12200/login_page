//javascript

async function transmit() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const response = await fetch("/login", {
        method: "POST",
        credentials: "include",        // <-- Important
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ username, password })
    });

    if (response.ok) {
        window.location.href = "/protected";
    } else {
        alert("Invalid username or password");
    }
}

const usernameInput = document.getElementById("username");
const passwordInput = document.getElementById("password");
const submitButton = document.getElementById("submit"); 


function check_status() {
    const usernameValue = usernameInput.value;
    const passwordValue = passwordInput.value;
    if (usernameValue.trim() !== "" && passwordValue.trim() !== "") {
        submitButton.disabled = false;
    } else {
        submitButton.disabled = true;
    }
}

usernameInput.addEventListener("input", check_status);
passwordInput.addEventListener("input", check_status);




check_status(); // Initial check to set the button state on page load