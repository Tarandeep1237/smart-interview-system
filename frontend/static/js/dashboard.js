document.addEventListener("DOMContentLoaded", () => {
    loadDashboard();
});


async function loadDashboard() {

    const loadingSection =
        document.getElementById("dashboard-loading");

    const dashboardContent =
        document.getElementById("dashboard-content");

    const errorSection =
        document.getElementById("dashboard-error");


    try {

        const response =
            await fetch("/api/dashboard");


        const data =
            await response.json();


        if (!response.ok || !data.success) {

            throw new Error(
                data.message ||
                "Unable to load dashboard."
            );
        }


        displayDashboard(data.data);


        loadingSection.style.display = "none";

        dashboardContent.style.display = "block";


    } catch (error) {

        loadingSection.style.display = "none";

        errorSection.style.display = "block";


        document.getElementById(
            "dashboard-error-message"
        ).textContent =
            error.message;
    }
}


function displayDashboard(data) {

    const user =
        data.user;

    const profile =
        data.profile;

    const resume =
        data.resume;

    const latestInterview =
        data.latest_interview;


    document.getElementById(
        "candidate-name"
    ).textContent =
        user.name;


    document.getElementById(
        "candidate-name-detail"
    ).textContent =
        user.name;


    document.getElementById(
        "candidate-email"
    ).textContent =
        user.email;


    document.getElementById(
        "target-role"
    ).textContent =
        profile && profile.target_role
            ? profile.target_role
            : "Not provided";


    displayProfileStatus(
        profile
    );


    displayResumeStatus(
        resume
    );


    displayLatestInterview(
        latestInterview
    );
}


function displayProfileStatus(profile) {

    const element =
        document.getElementById(
            "profile-status"
        );


    if (!profile) {

        element.textContent =
            "Profile not completed yet.";

        return;
    }


    const hasBasicInformation =
        profile.phone ||
        profile.education ||
        profile.target_role;


    if (hasBasicInformation) {

        element.textContent =
            "Profile information is available.";

    } else {

        element.textContent =
            "Complete your profile.";
    }
}


function displayResumeStatus(resume) {

    const element =
        document.getElementById(
            "resume-status"
        );


    if (!resume) {

        element.textContent =
            "No resume uploaded yet.";

        return;
    }


    element.textContent =
        `Uploaded: ${resume.file_name}`;
}


function displayLatestInterview(interview) {

    const noInterviewMessage =
        document.getElementById(
            "no-interview-message"
        );


    const latestInterviewSection =
        document.getElementById(
            "latest-interview"
        );


    if (!interview) {

        noInterviewMessage.style.display =
            "block";

        latestInterviewSection.style.display =
            "none";

        return;
    }


    noInterviewMessage.style.display =
        "none";


    latestInterviewSection.style.display =
        "block";


    document.getElementById(
        "latest-domain"
    ).textContent =
        interview.domain;


    document.getElementById(
        "latest-difficulty"
    ).textContent =
        interview.difficulty;


    document.getElementById(
        "latest-status"
    ).textContent =
        interview.status;


    if (
        interview.overall_score !== null
    ) {

        document.getElementById(
            "latest-score"
        ).textContent =
            `${Number(
                interview.overall_score
            ).toFixed(2)}/100`;

    } else {

        document.getElementById(
            "latest-score"
        ).textContent =
            "Not available";
    }
}