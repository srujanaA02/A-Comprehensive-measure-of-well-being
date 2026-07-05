document.addEventListener("DOMContentLoaded", function() {
    
    // --- Theme (Dark/Light Mode) Control ---
    const themeToggleBtn = document.getElementById("theme-toggle");
    const themeToggleIcon = document.getElementById("theme-toggle-icon");
    const htmlElement = document.documentElement;

    // Load saved theme preference
    const savedTheme = localStorage.getItem("theme") || "light";
    htmlElement.setAttribute("data-bs-theme", savedTheme);
    updateThemeIcon(savedTheme);

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener("click", function() {
            const currentTheme = htmlElement.getAttribute("data-bs-theme");
            const newTheme = currentTheme === "dark" ? "light" : "dark";
            
            htmlElement.setAttribute("data-bs-theme", newTheme);
            localStorage.setItem("theme", newTheme);
            updateThemeIcon(newTheme);
        });
    }

    function updateThemeIcon(theme) {
        if (!themeToggleIcon) return;
        if (theme === "dark") {
            themeToggleIcon.className = "fa-solid fa-sun";
            themeToggleBtn.setAttribute("title", "Toggle Light Mode");
        } else {
            themeToggleIcon.className = "fa-solid fa-moon";
            themeToggleBtn.setAttribute("title", "Toggle Dark Mode");
        }
    }

    // --- Sidebar Responsiveness for Mobile ---
    const sidebarToggleMobile = document.getElementById("sidebar-toggle-mobile");
    const sidebar = document.getElementById("sidebar");
    
    if (sidebarToggleMobile && sidebar) {
        sidebarToggleMobile.addEventListener("click", function() {
            sidebar.classList.toggle("d-none");
            sidebar.classList.toggle("d-block");
            sidebar.classList.toggle("mobile-sidebar");
        });
    }

    // --- Input Sync Controls (Sliders vs Inputs) ---
    const leInput = document.getElementById("life_expectancy");
    const leRange = document.getElementById("life_expectancy_range");
    const leLabel = document.getElementById("le-val-label");

    const gniInput = document.getElementById("gni_per_capita");
    const gniRange = document.getElementById("gni_per_capita_range");
    const gniLabel = document.getElementById("gni-val-label");

    if (leInput && leRange) {
        // Sync Input -> Slider
        leInput.addEventListener("input", function() {
            const val = parseFloat(leInput.value);
            if (!isNaN(val) && val >= 20 && val <= 100) {
                leRange.value = val;
                leLabel.textContent = val.toFixed(1) + " Years";
            }
        });
        // Sync Slider -> Input
        leRange.addEventListener("input", function() {
            const val = parseFloat(leRange.value);
            leInput.value = val.toFixed(1);
            leLabel.textContent = val.toFixed(1) + " Years";
        });
    }

    if (gniInput && gniRange) {
        // Sync Input -> Slider
        gniInput.addEventListener("input", function() {
            const val = parseInt(gniInput.value);
            if (!isNaN(val) && val >= 100 && val <= 100000) {
                gniRange.value = val;
                gniLabel.textContent = "$" + val.toLocaleString() + " PPP";
            }
        });
        // Sync Slider -> Input
        gniRange.addEventListener("input", function() {
            const val = parseInt(gniRange.value);
            gniInput.value = val;
            gniLabel.textContent = "$" + val.toLocaleString() + " PPP";
        });
    }

    // --- Country Selection Auto-Fill ---
    const countrySelect = document.getElementById("country");
    if (countrySelect) {
        countrySelect.addEventListener("change", function() {
            const countryName = countrySelect.value;
            if (countryName && countryName !== "Custom Country") {
                // Fetch country details from backend
                fetch(`/api/country/${encodeURIComponent(countryName)}`)
                    .then(response => {
                        if (!response.ok) throw new Error("Country not found");
                        return response.json();
                    })
                    .then(data => {
                        if (data.success) {
                            if (leInput) {
                                leInput.value = data.life_expectancy.toFixed(1);
                                if (leRange) leRange.value = data.life_expectancy;
                                if (leLabel) leLabel.textContent = data.life_expectancy.toFixed(1) + " Years";
                            }
                            if (document.getElementById("expected_years_schooling")) {
                                document.getElementById("expected_years_schooling").value = data.expected_years_schooling.toFixed(1);
                            }
                            if (document.getElementById("mean_years_schooling")) {
                                document.getElementById("mean_years_schooling").value = data.mean_years_schooling.toFixed(1);
                            }
                            if (gniInput) {
                                gniInput.value = Math.round(data.gni_per_capita);
                                if (gniRange) gniRange.value = data.gni_per_capita;
                                if (gniLabel) gniLabel.textContent = "$" + Math.round(data.gni_per_capita).toLocaleString() + " PPP";
                            }
                        }
                    })
                    .catch(err => console.log("Country prefill error:", err));
            }
        });
    }

    // --- Form validation & Loading spinner trigger ---
    const hdiForm = document.getElementById("hdi-form");
    const loadingSpinner = document.getElementById("loading-spinner");
    
    if (hdiForm) {
        hdiForm.addEventListener("submit", function(event) {
            if (!hdiForm.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                hdiForm.classList.add("was-validated");
            } else {
                // Form is valid, show spinner overlay
                if (loadingSpinner) {
                    loadingSpinner.classList.remove("d-none");
                }
            }
        });
    }

    // Reset button control
    const btnReset = document.getElementById("btn-reset");
    if (btnReset && hdiForm) {
        btnReset.addEventListener("click", function() {
            hdiForm.reset();
            hdiForm.classList.remove("was-validated");
            if (leLabel) leLabel.textContent = "70.0 Years";
            if (gniLabel) gniLabel.textContent = "$15,000 PPP";
        });
    }

    // --- Prediction History Table Loader ---
    const historyTbody = document.getElementById("history-tbody");
    
    function loadHistoryTable() {
        if (!historyTbody) return;
        
        const history = JSON.parse(localStorage.getItem("hdi_history")) || [];
        
        if (history.length === 0) {
            historyTbody.innerHTML = `
                <tr>
                    <td colspan="9" class="text-center py-4 text-muted">
                        <i class="fa-solid fa-inbox fs-4 mb-2 d-block"></i>
                        No predictions made yet. Input metrics in the form above to trigger predictions.
                    </td>
                </tr>
            `;
            return;
        }

        let rowsHtml = "";
        history.forEach((item, index) => {
            rowsHtml += `
                <tr>
                    <td class="text-nowrap">${item.timestamp}</td>
                    <td class="fw-bold text-dark-emphasis">${item.country}</td>
                    <td class="text-center">${item.life_expectancy.toFixed(1)}</td>
                    <td class="text-center">${item.expected_years_schooling.toFixed(1)}</td>
                    <td class="text-center">${item.mean_years_schooling.toFixed(1)}</td>
                    <td class="text-end">$${Math.round(item.gni_per_capita).toLocaleString()}</td>
                    <td class="text-end fw-bold text-teal">${item.predicted_hdi.toFixed(3)}</td>
                    <td class="text-center">
                        <span class="badge bg-${item.category_color} text-nowrap">${item.category}</span>
                    </td>
                    <td>
                        <button class="btn btn-sm btn-outline-danger btn-delete-history" data-index="${index}">
                            <i class="fa-solid fa-trash-can"></i>
                        </button>
                    </td>
                </tr>
            `;
        });
        
        historyTbody.innerHTML = rowsHtml;

        // Register Delete item events
        const deleteButtons = document.querySelectorAll(".btn-delete-history");
        deleteButtons.forEach(btn => {
            btn.addEventListener("click", function() {
                const idx = parseInt(this.getAttribute("data-index"));
                deleteHistoryItem(idx);
            });
        });
    }

    function deleteHistoryItem(index) {
        let history = JSON.parse(localStorage.getItem("hdi_history")) || [];
        history.splice(index, 1);
        localStorage.setItem("hdi_history", JSON.stringify(history));
        loadHistoryTable();
    }

    // Clear History Button
    const btnClearHistory = document.getElementById("btn-clear-history");
    if (btnClearHistory) {
        btnClearHistory.addEventListener("click", function() {
            if (confirm("Are you sure you want to clear your prediction history?")) {
                localStorage.removeItem("hdi_history");
                loadHistoryTable();
            }
        });
    }

    // Export History CSV Button
    const btnExportCsv = document.getElementById("btn-export-csv");
    if (btnExportCsv) {
        btnExportCsv.addEventListener("click", function() {
            const history = JSON.parse(localStorage.getItem("hdi_history")) || [];
            if (history.length === 0) {
                alert("No history records available to export.");
                return;
            }

            // CSV headers
            let csvContent = "data:text/csv;charset=utf-8,";
            csvContent += "Timestamp,Country,Life Expectancy,Expected Education,Mean Education,GNI Per Capita,Predicted HDI,Category\n";

            // Add lines
            history.forEach(item => {
                const row = [
                    `"${item.timestamp}"`,
                    `"${item.country}"`,
                    item.life_expectancy,
                    item.expected_years_schooling,
                    item.mean_years_schooling,
                    item.gni_per_capita,
                    item.predicted_hdi,
                    `"${item.category}"`
                ].join(",");
                csvContent += row + "\n";
            });

            // Trigger download
            const encodedUri = encodeURI(csvContent);
            const downloadAnchor = document.createElement("a");
            downloadAnchor.setAttribute("href", encodedUri);
            downloadAnchor.setAttribute("download", "HDI_Prediction_History.csv");
            document.body.appendChild(downloadAnchor);
            downloadAnchor.click();
            downloadAnchor.remove();
        });
    }

    // Initial load
    loadHistoryTable();
});
