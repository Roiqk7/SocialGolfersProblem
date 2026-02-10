// Show the schedule output section when the Solve button is clicked
const solveButton = document.getElementById("solve-button");
const outputSection = document.getElementById("output-section");
const scheduleTable = document.getElementById("schedule-table");

solveButton.addEventListener("click", async () => {
	// Gather inputs
	const N = parseInt(document.getElementById("players").value);
	const G = parseInt(document.getElementById("groups").value);
	const S = parseInt(document.getElementById("group-size").value);
	const R = parseInt(document.getElementById("rounds").value);
	const T = parseInt(document.getElementById("pairing").value);

    // Basic validation
    if (isNaN(N) || isNaN(G) || isNaN(S) || isNaN(R) || isNaN(T)) {
        alert("Please fill in all fields with valid numbers.");
        return;
    }

	// Show loading state
	solveButton.disabled = true;
	solveButton.textContent = "Generating...";
	outputSection.style.display = "none";
	scheduleTable.innerHTML = "";

	try {
		const response = await fetch('/api/solve', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ N, G, S, R, T })
		});

		if (!response.ok) {
            const errorText = await response.text();
            let errorMessage = `Server error: ${response.status}`;
            try {
                const errorJson = JSON.parse(errorText);
                if (errorJson.detail) {
                    errorMessage += ` - ${errorJson.detail}`;
                }
            } catch (e) {
                errorMessage += ` - ${errorText}`;
            }
			throw new Error(errorMessage);
		}

		const data = await response.json();
        const schedule = data.schedule;

        if (schedule === "UNSAT") {
            scheduleTable.innerHTML = "<p class='error-message'>No solution exists for these parameters.</p>";
        } else {
            // Parse schedule CSV-like string: "Player1,Player2;Player3,Player4\nPlayer1,Player3;Player2,Player4"
            // Rounds are separated by newline, groups by semicolon, players by comma
            let html = "<table>";
            const rounds = schedule.split('\n');
            rounds.forEach((round, roundIndex) => {
                html += `<tr><th colspan="${G}">Round ${roundIndex + 1}</th></tr><tr>`;
                const groups = round.split(';');
                groups.forEach((group, groupIndex) => {
                    const players = group.split(',').join(', ');
                    html += `<td><strong>Group ${groupIndex + 1}:</strong><br>${players}</td>`;
                });
                html += "</tr>";
            });
            html += "</table>";
            scheduleTable.innerHTML = html;
        }
        outputSection.style.display = "block";

	} catch (error) {
		console.error("Error:", error);
		alert("An error occurred: " + error.message);
	} finally {
		solveButton.disabled = false;
		solveButton.textContent = "Generate Schedule";
	}
});
