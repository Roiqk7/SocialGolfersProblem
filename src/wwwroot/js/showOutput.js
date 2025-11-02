// Show the schedule output section when the Solve button is clicked
const solveButton = document.getElementById("solve-button");
const outputSection = document.getElementById("output-section");

solveButton.addEventListener("click", () => {
	outputSection.style.display = "block";
});
