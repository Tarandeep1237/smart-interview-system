document.addEventListener("DOMContentLoaded", () => {

    const form =
        document.getElementById("loginForm");


    if (!form) {

        console.error(
            "Login form not found."
        );

        return;
    }


    form.addEventListener(
        "submit",
        loginUser
    );

});


async function loginUser(event) {

    event.preventDefault();


    const emailElement =
        document.getElementById("email");

    const passwordElement =
        document.getElementById("password");

    const messageElement =
        document.getElementById(
            "login-message"
        );

    const loginButton =
        document.getElementById(
            "login-btn"
        );


    const email =
        emailElement.value.trim();

    const password =
        passwordElement.value;


    messageElement.textContent = "";


    if (!email) {

        messageElement.textContent =
            "Please enter your email.";

        emailElement.focus();

        return;
    }


    if (!password) {

        messageElement.textContent =
            "Please enter your password.";

        passwordElement.focus();

        return;
    }


    loginButton.disabled = true;

    loginButton.textContent =
        "Logging in...";


    try {

        const response =
            await fetch(
                "/api/login",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
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
                "Login failed."
            );

        }


        messageElement.textContent =
            "Login successful. Redirecting...";


        window.location.href =
            "/dashboard";


    } catch (error) {

        messageElement.textContent =
            error.message;

        loginButton.disabled =
            false;

        loginButton.textContent =
            "Login";

    }

}