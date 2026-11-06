document.addEventListener("DOMContentLoaded", () => {

    loadProfile();


    const form =
        document.getElementById("profileForm");


    if (!form) {

        console.error(
            "Profile form not found."
        );

        return;
    }


    form.addEventListener(
        "submit",
        saveProfile
    );

});


async function loadProfile() {

    const messageElement =
        document.getElementById(
            "profile-message"
        );


    try {

        const response =
            await fetch(
                "/api/profile"
            );


        const data =
            await response.json();


        if (!response.ok || !data.success) {

            if (response.status === 404) {

                return;
            }


            throw new Error(
                data.message ||
                "Unable to load profile."
            );

        }


        const profile =
            data.profile;


        if (!profile) {
            return;
        }


        document.getElementById(
            "phone"
        ).value =
            profile.phone || "";


        document.getElementById(
            "education"
        ).value =
            profile.education || "";


        document.getElementById(
            "target_role"
        ).value =
            profile.target_role || "";


    } catch (error) {

        messageElement.textContent =
            error.message;

    }

}


async function saveProfile(event) {

    event.preventDefault();


    const phone =
        document.getElementById(
            "phone"
        ).value.trim();


    const education =
        document.getElementById(
            "education"
        ).value.trim();


    const targetRole =
        document.getElementById(
            "target_role"
        ).value.trim();


    const messageElement =
        document.getElementById(
            "profile-message"
        );


    const saveButton =
        document.getElementById(
            "save-profile-btn"
        );


    messageElement.textContent = "";


    saveButton.disabled =
        true;


    saveButton.textContent =
        "Saving...";


    try {

        const response =
            await fetch(
                "/api/profile",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        phone: phone,
                        education: education,
                        target_role: targetRole
                    })
                }
            );


        const data =
            await response.json();


        if (!response.ok || !data.success) {

            throw new Error(
                data.message ||
                "Unable to save profile."
            );

        }


        messageElement.textContent =
            "Profile saved successfully.";


    } catch (error) {

        messageElement.textContent =
            error.message;


    } finally {

        saveButton.disabled =
            false;

        saveButton.textContent =
            "Save Profile";

    }

}