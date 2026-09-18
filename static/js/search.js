document.addEventListener("DOMContentLoaded", function () {

    const searchBox = document.getElementById("searchBox");
    const searchToggle = document.getElementById("searchToggle");
    const searchInput = document.getElementById("searchInput");
    const suggestionsBox = document.getElementById("searchSuggestions");

    // Search open / close
    searchToggle.addEventListener("click", function () {

        searchBox.classList.toggle("active");

        if (searchBox.classList.contains("active")) {
            searchInput.focus();
        } else {
            searchInput.value = "";
            suggestionsBox.innerHTML = "";
            suggestionsBox.style.display = "none";
        }

    });

    // Live suggestions
    searchInput.addEventListener("input", function () {

        const query = this.value.trim();

        if (query.length < 1) {
            suggestionsBox.innerHTML = "";
            suggestionsBox.style.display = "none";
            return;
        }

        fetch("/search-suggestions/?q=" + encodeURIComponent(query))
            .then(response => response.json())
            .then(data => {

                suggestionsBox.innerHTML = "";

                if (data.length === 0) {

                    suggestionsBox.innerHTML =
                        '<div class="no-result">No jobs found</div>';

                } else {

                    data.forEach(post => {

                        const item = document.createElement("a");

                        // IMPORTANT: Actual post URL
                        item.href = "/post/" + post.slug + "/";

                        item.textContent = post.title;

                        suggestionsBox.appendChild(item);

                    });

                }

                suggestionsBox.style.display = "block";

            })
            .catch(error => {
                console.error("Search Error:", error);
            });

    });

});