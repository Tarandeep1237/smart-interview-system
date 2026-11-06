let interview = null;

let currentQuestionIndex = 0;

let currentQuestionId = null;


document.addEventListener("DOMContentLoaded", () => {

    startInterview();

});


async function startInterview() {

    const loadingSection =
        document.getElementById("loading-section");

    const interviewSection =
        document.getElementById("interview-section");

    const statusMessage =
        document.getElementById("status-message");


    /*
     * First read the interview configuration
     * directly from the URL.
     */
    const urlParams =
        new URLSearchParams(window.location.search);


    let domain =
        urlParams.get("domain");

    let difficulty =
        urlParams.get("difficulty");


    /*
     * If the URL does not contain the values,
     * use localStorage as a fallback.
     */
    if (!domain) {

        domain =
            localStorage.getItem(
                "interview_domain"
            );

    }


    if (!difficulty) {

        difficulty =
            localStorage.getItem(
                "interview_difficulty"
            );

    }


    /*
     * If no interview configuration exists,
     * send the user back to setup.
     */
    if (!domain || !difficulty) {

        window.location.replace(
            "/interview/setup"
        );

        return;
    }


    /*
     * Keep the configuration available while
     * the interview is running.
     */
    localStorage.setItem(
        "interview_domain",
        domain
    );

    localStorage.setItem(
        "interview_difficulty",
        difficulty
    );


    try {

        statusMessage.textContent =
            "Generating your personalized interview questions...";


        const response =
            await fetch(
                "/api/interview/start",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        domain: domain,
                        difficulty: difficulty
                    })
                }
            );


        const data =
            await response.json();


        if (!response.ok || !data.success) {

            throw new Error(
                data.message ||
                "Failed to start interview."
            );
        }


        interview =
            data.interview;


        loadingSection.style.display =
            "none";


        interviewSection.style.display =
            "block";


        document.getElementById(
            "interview-info"
        ).textContent =
            `${interview.domain} | ${interview.difficulty}`;


        showQuestion();


    } catch (error) {

        loadingSection.innerHTML = `
            <div class="card">
                <h2>Unable to Start Interview</h2>
                <p>${error.message}</p>

                <a href="/interview/setup">
                    <button type="button">
                        Back to Interview Setup
                    </button>
                </a>
            </div>
        `;

        statusMessage.textContent = "";

    }

}


function showQuestion() {

    const question =
        interview.questions[
            currentQuestionIndex
        ];


    currentQuestionId =
        interview.question_ids[
            currentQuestionIndex
        ];


    document.getElementById(
        "question-number"
    ).textContent =
        `Question ${
            currentQuestionIndex + 1
        } of ${
            interview.questions.length
        }`;


    document.getElementById(
        "question-text"
    ).textContent =
        question;


    document.getElementById(
        "answer"
    ).value = "";


    document.getElementById(
        "status-message"
    ).textContent = "";


    document.getElementById(
        "submit-answer-btn"
    ).disabled = false;

}


document.getElementById(
    "submit-answer-btn"
).addEventListener(
    "click",
    submitAnswer
);


async function submitAnswer() {

    const answerElement =
        document.getElementById(
            "answer"
        );


    const submitButton =
        document.getElementById(
            "submit-answer-btn"
        );


    const statusMessage =
        document.getElementById(
            "status-message"
        );


    const answer =
        answerElement.value.trim();


    if (!answer) {

        statusMessage.textContent =
            "Please enter your answer.";

        return;
    }


    submitButton.disabled =
        true;


    statusMessage.textContent =
        "Evaluating your answer...";


    try {

        const response =
            await fetch(
                "/api/interview/answer",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        question_id:
                            currentQuestionId,

                        answer:
                            answer
                    })
                }
            );


        const data =
            await response.json();


        if (!response.ok || !data.success) {

            throw new Error(
                data.message ||
                "Failed to submit answer."
            );
        }


        displayEvaluation(
            data.evaluation
        );


    } catch (error) {

        statusMessage.textContent =
            error.message;

        submitButton.disabled =
            false;

    }

}


function displayEvaluation(evaluation) {

    document.getElementById(
        "interview-section"
    ).style.display =
        "none";


    const resultSection =
        document.getElementById(
            "result-section"
        );


    const evaluationContent =
        document.getElementById(
            "evaluation-content"
        );


    evaluationContent.innerHTML =
        "";


    addEvaluationScore(
        evaluationContent,
        "Relevance",
        evaluation.relevance_score
    );


    addEvaluationScore(
        evaluationContent,
        "Correctness",
        evaluation.correctness_score
    );


    addEvaluationScore(
        evaluationContent,
        "Completeness",
        evaluation.completeness_score
    );


    addEvaluationScore(
        evaluationContent,
        "Technical Accuracy",
        evaluation.technical_accuracy_score
    );


    addEvaluationScore(
        evaluationContent,
        "Overall Score",
        evaluation.overall_score
    );


    addEvaluationText(
        evaluationContent,
        "Feedback",
        evaluation.feedback
    );


    addEvaluationText(
        evaluationContent,
        "Strengths",
        evaluation.strengths
    );


    addEvaluationText(
        evaluationContent,
        "Areas for Improvement",
        evaluation.areas_for_improvement
    );


    resultSection.style.display =
        "block";


    const nextButton =
        document.getElementById(
            "next-question-btn"
        );


    nextButton.textContent =
        currentQuestionIndex ===
        interview.questions.length - 1
            ? "Finish Interview"
            : "Next Question";

}


function addEvaluationScore(
    container,
    label,
    score
) {

    const paragraph =
        document.createElement("p");


    const strong =
        document.createElement("strong");


    strong.textContent =
        `${label}: `;


    paragraph.appendChild(
        strong
    );


    paragraph.appendChild(
        document.createTextNode(
            `${score}/100`
        )
    );


    container.appendChild(
        paragraph
    );

}


function addEvaluationText(
    container,
    heading,
    text
) {

    if (!text) {
        return;
    }


    const title =
        document.createElement("h3");


    title.textContent =
        heading;


    container.appendChild(
        title
    );


    const paragraph =
        document.createElement("p");


    paragraph.textContent =
        text;


    container.appendChild(
        paragraph
    );

}


document.getElementById(
    "next-question-btn"
).addEventListener(
    "click",
    nextQuestion
);


async function nextQuestion() {

    if (
        currentQuestionIndex ===
        interview.questions.length - 1
    ) {

        await finishInterview();

        return;
    }


    currentQuestionIndex++;


    document.getElementById(
        "result-section"
    ).style.display =
        "none";


    document.getElementById(
        "interview-section"
    ).style.display =
        "block";


    showQuestion();

}


async function finishInterview() {

    const nextButton =
        document.getElementById(
            "next-question-btn"
        );


    nextButton.disabled =
        true;


    nextButton.textContent =
        "Completing Interview...";


    try {

        const response =
            await fetch(
                "/api/interview/complete",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        interview_id:
                            interview.interview_id
                    })
                }
            );


        const data =
            await response.json();


        if (!response.ok || !data.success) {

            throw new Error(
                data.message ||
                "Failed to complete interview."
            );
        }


        /*
         * Clear the setup values only after
         * the interview has been completed.
         */
        localStorage.removeItem(
            "interview_domain"
        );

        localStorage.removeItem(
            "interview_difficulty"
        );


        window.location.replace(
            "/results"
        );


    } catch (error) {

        nextButton.disabled =
            false;


        nextButton.textContent =
            "Finish Interview";


        const errorMessage =
            document.createElement("p");


        errorMessage.textContent =
            error.message;


        document.getElementById(
            "evaluation-content"
        ).appendChild(
            errorMessage
        );

    }

}