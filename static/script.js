document.addEventListener("DOMContentLoaded", () => {
    // Form validation
    const form = document.querySelector("form");
    if (form) {
        form.addEventListener("submit", (e) => {
            const age = document.querySelector("input[name='age']").value;
            const secondaryConcerns = document.querySelectorAll("input[name='secondary_concerns']:checked");
            const errorDivs = document.querySelectorAll(".error");

            // Clear previous errors
            errorDivs.forEach(div => div.style.display = "none");

            let hasError = false;

            // Age validation
            if (age <= 0 || age > 120) {
                document.getElementById("age-error").style.display = "block";
                hasError = true;
            }

            // Exactly one secondary concern validation
            if (secondaryConcerns.length === 0) {
                document.getElementById("concerns-error").style.display = "block";
                hasError = true;
            }

            if (hasError) {
                e.preventDefault();
            }
        });
    }

    // Results fade-in
    const results = document.querySelector(".results-container");
    if (results) {
        setTimeout(() => {
            results.classList.add("visible");
        }, 100);
    }

    // Smooth scroll for back button
    const backBtn = document.querySelector(".back-btn");
    if (backBtn) {
        backBtn.addEventListener("click", (e) => {
            e.preventDefault();
            window.location.href = "/";
        });
    }
});