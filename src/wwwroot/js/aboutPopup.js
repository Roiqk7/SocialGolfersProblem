// Toggle About popup visibility
const aboutLink = document.getElementById("about-link");
const aboutPopup = document.getElementById("info-about-popup");

aboutLink.addEventListener("click", (e) => {
	e.preventDefault();
	aboutPopup.classList.toggle("active");
});
