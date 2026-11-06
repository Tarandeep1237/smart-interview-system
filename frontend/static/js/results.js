document.addEventListener("DOMContentLoaded", () => {
    loadResults();
});


async function loadResults() {

    const loadingSection =
        document.getElementById("loading-section");

    const noResultsSection =
        document.getElementById("no-results-section");

    const resultsSection =
        document.getElementById("results-section");


    try {

        const response =
            await fetch("/api/results");


        const data =
            await response.json();


        if (!response.ok || !data.success) {

            throw new Error(
                data.message ||
                "Unable to load interview results."
            );
        }


        displayResults(data.data);


        loadingSection.style.display =
            "none";

        resultsSection.style.display =
            "block";


    } catch (error) {

        loadingSection.style.display =
            "none";

        noResultsSection.style.display =
            "block";


        document.getElementById(
            "no-results-message"
        ).textContent =
            error.message;

    }

}


function displayResults(data) {

    const interview =
        data.interview;

    const results =
        data.results;

    const report =
        data.report;


    document.getElementById(
        "result-domain"
    ).textContent =
        interview.domain;


    document.getElementById(
        "result-difficulty"
    ).textContent =
        interview.difficulty;


    document.getElementById(
        "result-status"
    ).textContent =
        interview.status;


    const evaluatedResults =
        results.filter(
            result =>
                result.overall_score !== null
        );


    if (evaluatedResults.length === 0) {

        document.getElementById(
            "overall-score"
        ).textContent =
            "Not available";


        document.getElementById(
            "question-results"
        ).textContent =
            "No evaluated answers are available yet.";


        document.getElementById(
            "performance-summary"
        ).textContent =
            "Complete an interview to generate your performance report.";


        document.getElementById(
            "improvement-summary"
        ).textContent =
            "No improvement areas are available yet.";


        document.getElementById(
            "recommendation-summary"
        ).textContent =
            "No recommendations are available yet.";


        return;
    }


    if (
        report &&
        report.overall_score !== null
    ) {

        document.getElementById(
            "overall-score"
        ).textContent =
            `${Number(
                report.overall_score
            ).toFixed(2)}/100`;

    } else {

        document.getElementById(
            "overall-score"
        ).textContent =
            "Not available";

    }


    displayQuestionResults(results);

    displayPerformanceSummary(
        evaluatedResults
    );

    displayImprovementSummary(
        evaluatedResults
    );

    displayRecommendation(
        report
    );

}


function displayQuestionResults(results) {

    const container =
        document.getElementById(
            "question-results"
        );


    container.innerHTML =
        "";


    results.forEach(
        (result, index) => {

            const questionCard =
                document.createElement("div");


            questionCard.className =
                "dashboard-card result-question-card";


            const questionTitle =
                document.createElement("h3");


            questionTitle.textContent =
                `Question ${index + 1}`;


            questionCard.appendChild(
                questionTitle
            );


            addExpandableText(
                questionCard,
                result.question_text,
                230,
                "Question"
            );


            if (
                result.overall_score === null
            ) {

                const pendingMessage =
                    document.createElement("p");


                pendingMessage.className =
                    "result-pending";


                pendingMessage.textContent =
                    "This question has not been evaluated yet.";


                questionCard.appendChild(
                    pendingMessage
                );


                container.appendChild(
                    questionCard
                );


                return;
            }


            addScore(
                questionCard,
                "Relevance",
                result.relevance_score
            );


            addScore(
                questionCard,
                "Correctness",
                result.correctness_score
            );


            addScore(
                questionCard,
                "Completeness",
                result.completeness_score
            );


            addScore(
                questionCard,
                "Technical Accuracy",
                result.technical_accuracy_score
            );


            addScore(
                questionCard,
                "Overall Score",
                result.overall_score
            );


            addExpandableText(
                questionCard,
                result.feedback,
                260,
                "Feedback"
            );


            addExpandableText(
                questionCard,
                result.strengths,
                220,
                "Strengths"
            );


            addExpandableText(
                questionCard,
                result.areas_for_improvement,
                220,
                "Areas for Improvement"
            );


            container.appendChild(
                questionCard
            );

        }
    );

}


function addScore(
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


    const formattedScore =
        score !== null &&
        score !== undefined
            ? `${score}/100`
            : "Not available";


    paragraph.appendChild(
        document.createTextNode(
            formattedScore
        )
    );


    container.appendChild(
        paragraph
    );

}


function addExpandableText(
    container,
    text,
    characterLimit,
    heading
) {

    if (!text) {
        return;
    }


    const wrapper =
        document.createElement("div");


    wrapper.className =
        "expandable-section";


    if (heading) {

        const title =
            document.createElement("h4");


        title.textContent =
            heading;


        wrapper.appendChild(
            title
        );

    }


    const content =
        document.createElement("p");


    content.className =
        "expandable-content";


    const fullText =
        String(text).trim();


    if (
        fullText.length <=
        characterLimit
    ) {

        content.textContent =
            fullText;


        wrapper.appendChild(
            content
        );


        container.appendChild(
            wrapper
        );


        return;
    }


    const previewText =
        createPreview(
            fullText,
            characterLimit
        );


    content.textContent =
        previewText;


    wrapper.appendChild(
        content
    );


    const readMoreButton =
        document.createElement("button");


    readMoreButton.type =
        "button";


    readMoreButton.className =
        "read-more-btn";


    readMoreButton.textContent =
        "Read more";


    let expanded = false;


    readMoreButton.addEventListener(
        "click",
        () => {

            expanded =
                !expanded;


            if (expanded) {

                content.textContent =
                    fullText;

                readMoreButton.textContent =
                    "Read less";

            } else {

                content.textContent =
                    previewText;

                readMoreButton.textContent =
                    "Read more";

            }

        }
    );


    wrapper.appendChild(
        readMoreButton
    );


    container.appendChild(
        wrapper
    );

}


function createPreview(
    text,
    characterLimit
) {

    let preview =
        text.substring(
            0,
            characterLimit
        );


    const lastSpace =
        preview.lastIndexOf(" ");


    if (
        lastSpace >
        characterLimit * 0.70
    ) {

        preview =
            preview.substring(
                0,
                lastSpace
            );

    }


    return `${preview.trim()}...`;

}


function displayPerformanceSummary(
    results
) {

    const container =
        document.getElementById(
            "performance-summary"
        );


    container.innerHTML =
        "";


    const feedbackHeading =
        document.createElement("h3");


    feedbackHeading.textContent =
        "AI Feedback";


    container.appendChild(
        feedbackHeading
    );


    results.forEach(
        (result, index) => {

            if (!result.feedback) {
                return;
            }


            const wrapper =
                document.createElement("div");


            wrapper.className =
                "summary-item";


            const label =
                document.createElement("strong");


            label.textContent =
                `Question ${index + 1}`;


            wrapper.appendChild(
                label
            );


            addExpandableText(
                wrapper,
                result.feedback,
                220,
                ""
            );


            container.appendChild(
                wrapper
            );

        }
    );


    const strengthsHeading =
        document.createElement("h3");


    strengthsHeading.textContent =
        "Strengths";


    container.appendChild(
        strengthsHeading
    );


    results.forEach(
        (result, index) => {

            if (!result.strengths) {
                return;
            }


            const wrapper =
                document.createElement("div");


            wrapper.className =
                "summary-item";


            const label =
                document.createElement("strong");


            label.textContent =
                `Question ${index + 1}`;


            wrapper.appendChild(
                label
            );


            addExpandableText(
                wrapper,
                result.strengths,
                220,
                ""
            );


            container.appendChild(
                wrapper
            );

        }
    );

}


function displayImprovementSummary(
    results
) {

    const container =
        document.getElementById(
            "improvement-summary"
        );


    container.innerHTML =
        "";


    results.forEach(
        (result, index) => {

            if (
                !result.areas_for_improvement
            ) {
                return;
            }


            const wrapper =
                document.createElement("div");


            wrapper.className =
                "summary-item";


            const label =
                document.createElement("strong");


            label.textContent =
                `Question ${index + 1}`;


            wrapper.appendChild(
                label
            );


            addExpandableText(
                wrapper,
                result.areas_for_improvement,
                220,
                ""
            );


            container.appendChild(
                wrapper
            );

        }
    );

}


function displayRecommendation(
    report
) {

    const container =
        document.getElementById(
            "recommendation-summary"
        );


    container.innerHTML =
        "";


    if (
        !report ||
        !report.recommendations
    ) {

        container.textContent =
            "No recommendations are available yet.";

        return;
    }


    addExpandableText(
        container,
        report.recommendations,
        260,
        ""
    );

}