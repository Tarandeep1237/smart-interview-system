document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("interviewSetupForm");

    if (!form) {
        console.error("Interview setup form not found.");
        return;
    }

    form.addEventListener("submit", startInterview);

});


function startInterview(event) {

    event.preventDefault();

    const domainElement =
        document.getElementById("domain");

    const difficultyElement =
        document.getElementById("difficulty");

    const messageElement =
        document.getElementById("setup-message");


    const domain =
        domainElement.value.trim();

    const difficulty =
        difficultyElement.value.trim();


    messageElement.textContent = "";


    if (!domain) {

        messageElement.textContent =
            "Please select an interview domain.";

        domainElement.focus();

        return;
    }


    if (!difficulty) {

        messageElement.textContent =
            "Please select the interview difficulty.";

        difficultyElement.focus();

        return;
    }


    /*
     * Store the selected interview configuration.
     */
    localStorage.setItem(
        "interview_domain",
        domain
    );

    localStorage.setItem(
        "interview_difficulty",
        difficulty
    );


    /*
     * Pass the configuration directly to the
     * interview page as well.
     *
     * This prevents the setup page from appearing
     * again because of a missing localStorage value.
     */
    const interviewUrl =
        "/interview" +
        "?domain=" +
        encodeURIComponent(domain) +
        "&difficulty=" +
        encodeURIComponent(difficulty);


    window.location.href =
        interviewUrl;

}