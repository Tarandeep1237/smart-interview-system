document.addEventListener("DOMContentLoaded", () => {

    hideResumeSections();


    const form =
        document.getElementById("resumeForm");


    if (!form) {

        console.error(
            "Resume form not found."
        );

        return;
    }


    form.addEventListener(
        "submit",
        uploadResume
    );

});


function hideResumeSections() {

    const resumeSection =
        document.getElementById(
            "resume-section"
        );

    const skillsSection =
        document.getElementById(
            "skills-section"
        );


    if (resumeSection) {

        resumeSection.style.display =
            "none";

    }


    if (skillsSection) {

        skillsSection.style.display =
            "none";

    }

}


function showResumeSections() {

    const resumeSection =
        document.getElementById(
            "resume-section"
        );

    const skillsSection =
        document.getElementById(
            "skills-section"
        );


    if (resumeSection) {

        resumeSection.style.display =
            "block";

    }


    if (skillsSection) {

        skillsSection.style.display =
            "block";

    }

}


async function loadResume() {

    const resumeDetails =
        document.getElementById(
            "resume-details"
        );

    const skillsContainer =
        document.getElementById(
            "skills-container"
        );


    try {

        const response =
            await fetch(
                "/api/resume"
            );


        const data =
            await response.json();


        if (!response.ok || !data.success) {

            throw new Error(
                data.message ||
                "Unable to load resume."
            );

        }


        displayResume(
            data.resume
        );


        displaySkills(
            data.skills
        );


        showResumeSections();


    } catch (error) {

        resumeDetails.innerHTML = `
            <p>
                ${error.message}
            </p>
        `;

    }

}


async function uploadResume(event) {

    event.preventDefault();


    const fileInput =
        document.getElementById(
            "resume"
        );

    const messageElement =
        document.getElementById(
            "resume-message"
        );

    const uploadButton =
        document.getElementById(
            "upload-resume-btn"
        );


    messageElement.textContent = "";


    if (
        !fileInput.files ||
        fileInput.files.length === 0
    ) {

        messageElement.textContent =
            "Please select a resume.";

        return;
    }


    const file =
        fileInput.files[0];


    const allowedExtensions =
        [".pdf", ".docx"];


    const fileName =
        file.name.toLowerCase();


    const isValidFile =
        allowedExtensions.some(
            extension =>
                fileName.endsWith(
                    extension
                )
        );


    if (!isValidFile) {

        messageElement.textContent =
            "Please upload a PDF or DOCX file.";

        return;
    }


    const formData =
        new FormData();


    formData.append(
        "resume",
        file
    );


    uploadButton.disabled =
        true;

    uploadButton.textContent =
        "Uploading...";


    try {

        const response =
            await fetch(
                "/api/resume/upload",
                {
                    method: "POST",
                    body: formData
                }
            );


        const data =
            await response.json();


        if (!response.ok || !data.success) {

            throw new Error(
                data.message ||
                "Resume upload failed."
            );

        }


        messageElement.textContent =
            "Resume uploaded successfully.";


        fileInput.value = "";


        await loadResume();


    } catch (error) {

        messageElement.textContent =
            error.message;


    } finally {

        uploadButton.disabled =
            false;

        uploadButton.textContent =
            "Upload Resume";

    }

}


function displayResume(resume) {

    const container =
        document.getElementById(
            "resume-details"
        );


    if (!resume) {

        container.innerHTML = `
            <p>
                No resume uploaded yet.
            </p>
        `;

        return;
    }


    container.innerHTML = "";


    const fileName =
        document.createElement("p");


    const fileNameLabel =
        document.createElement("strong");


    fileNameLabel.textContent =
        "File: ";


    fileName.appendChild(
        fileNameLabel
    );


    fileName.appendChild(
        document.createTextNode(
            resume.file_name || "Resume"
        )
    );


    container.appendChild(
        fileName
    );


    if (resume.uploaded_at) {

        const uploadedAt =
            document.createElement("p");


        const uploadedLabel =
            document.createElement("strong");


        uploadedLabel.textContent =
            "Uploaded: ";


        uploadedAt.appendChild(
            uploadedLabel
        );


        uploadedAt.appendChild(
            document.createTextNode(
                resume.uploaded_at
            )
        );


        container.appendChild(
            uploadedAt
        );

    }

}


function displaySkills(skills) {

    const container =
        document.getElementById(
            "skills-container"
        );


    container.innerHTML = "";


    if (
        !skills ||
        skills.length === 0
    ) {

        container.innerHTML = `
            <p>
                No technical skills were extracted
                from the resume.
            </p>
        `;

        return;
    }


    const list =
        document.createElement("ul");


    skills.forEach(
        skill => {

            const item =
                document.createElement("li");


            item.textContent =
                skill;


            list.appendChild(
                item
            );

        }
    );


    container.appendChild(
        list
    );

}