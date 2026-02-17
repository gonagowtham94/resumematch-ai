async function analyzeResume() {

    const resumeFile = document.getElementById("resumeFile").files[0];
    const jobDescription = document.getElementById("jobDescription").value;

    const matchScoreElement = document.getElementById("matchScore");
    const matchedSkillsElement = document.getElementById("matchedSkills");
    const recommendationElement = document.getElementById("recommendationText");
    const resultsSection = document.getElementById("resultsSection");

    // -----------------------
    // Validation
    // -----------------------

    if (!resumeFile) {
        alert("Please upload a resume file.");
        return;
    }

    if (!jobDescription.trim()) {
        alert("Please enter job description.");
        return;
    }

    // -----------------------
    // Loading UI
    // -----------------------

    matchScoreElement.innerText = "Analyzing...";
    matchedSkillsElement.innerText = "Extracting skills...";
    recommendationElement.innerText = "AI is evaluating profile...";

    // Smooth scroll to results
    resultsSection.scrollIntoView({ behavior: "smooth" });

    // Fake AI thinking delay (UX effect)
    await new Promise(resolve => setTimeout(resolve, 1500));

    // -----------------------
    // Prepare API Request
    // -----------------------

    const formData = new FormData();
    formData.append("resume", resumeFile);
    formData.append("job_description", jobDescription);

    try {

        const response = await fetch("/analyze", {
            method: "POST",
            body: formData
        });

        const result = await response.json();

        // -----------------------
        // Success Response
        // -----------------------

        if (result.status === "success") {

            // Save data for Insights page
            localStorage.setItem("matchScore", result.match_percentage);
            localStorage.setItem("matchedSkills", JSON.stringify(result.common_keywords));

            // Animate score
            animateScore(result.match_percentage);

            // Display matched keywords
            if (result.common_keywords.length > 0) {
                matchedSkillsElement.innerText =
                    result.common_keywords.join(", ");
            } else {
                matchedSkillsElement.innerText =
                    "No strong keyword matches found.";
            }

            // Recommendation logic
            const score = result.match_percentage;

            if (score >= 80) {
                recommendationElement.innerText =
                    "Strong candidate match. Recommended for technical interview round.";
            }
            else if (score >= 60) {
                recommendationElement.innerText =
                    "Moderate match. Candidate meets core requirements but needs improvement.";
            }
            else {
                recommendationElement.innerText =
                    "Low match score. Resume requires optimization for this role.";
            }

        } else {
            alert("Resume analysis failed.");
        }

    } catch (error) {

        console.error("Backend Error:", error);

        alert("Backend server is not responding. Please check Flask server.");
    }
}


// ---------------------------
// Animated Match Counter
// ---------------------------

function animateScore(targetScore) {

    const matchScoreElement = document.getElementById("matchScore");

    let currentScore = 0;

    const animation = setInterval(() => {

        if (currentScore >= targetScore) {
            clearInterval(animation);
            matchScoreElement.innerText = targetScore + "%";
        } else {
            currentScore++;
            matchScoreElement.innerText = currentScore + "%";
        }

    }, 15); // animation speed
}
