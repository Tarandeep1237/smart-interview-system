document.addEventListener("DOMContentLoaded", () => {

    const form =
        document.getElementById("registerForm");


    if (!form) {

        console.error(
            "Registration form not found."
        );

        return;
    }


    form.addEventListener(
        "submit",
        registerUser
    );

});


async function registerUser(event) {

    event.preventDefault();


    const nameElement =
        document.getElementById("name");

    const emailElement =
        document.getElementById("email");

    const passwordElement =
        document.getElementById("password");

    const confirmPasswordElement =
        document.getElementById(
            "confirm_password"
        );

    const messageElement =
        document.getElementById(
            "register-message"
        );

    const registerButton =
        document.getElementById(
            "register-btn"
        );


    const name =
        nameElement.value.trim();

    const email =
        emailElement.value.trim();

    const password =
        passwordElement.value;

    const confirmPassword =
        confirmPasswordElement.value;


    messageElement.textContent = "";


    if (!name) {

        messageElement.textContent =
            "Please enter your full name.";

        nameElement.focus();

        return;
    }


    if (!email) {

        messageElement.textContent =
            "Please enter your email.";

        emailElement.focus();

        return;
    }


    if (!password) {

        messageElement.textContent =
            "Please enter a password.";

        passwordElement.focus();

        return;
    }


    if (password.length < 6) {

        messageElement.textContent =
            "Password must be at least 6 characters.";

        passwordElement.focus();

        return;
    }


    if (password !== confirmPassword) {

        messageElement.textContent =
            "Passwords do not match.";

        confirmPasswordElement.focus();

        return;
    }


    registerButton.disabled =
        true;

    registerButton.textContent =
        "Creating Account...";


    try {

        const response =
            await fetch(
                "/api/register",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        name: name,
                        email: email,
                        password: password
                    })
                }
            );


        const data =
            await response.json();


        if (!response.ok || !data.success) {

            throw new Error(
                data.message ||
                "Registration failed."
            );

        }


        messageElement.textContent =
            "Registration successful. Redirecting to dashboard...";


        window.location.href =
            "/dashboard";


    } catch (error) {

        messageElement.textContent =
            error.message;

        registerButton.disabled =
            false;

        registerButton.textContent =
            "Create Account";

    }

}