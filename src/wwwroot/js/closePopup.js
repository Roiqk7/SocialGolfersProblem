// Close About popup with "×" button
const closeAboutBtn = document.getElementById("close-about-popup");

closeAboutBtn.addEventListener("click", () => {
	aboutPopup.classList.remove("active");
});
