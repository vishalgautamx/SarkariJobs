const menuBtn = document.getElementById("menuToggle");
const navMenu = document.getElementById("navMenu");

menuBtn.addEventListener("click", () => {

    menuBtn.classList.toggle("active");

    navMenu.classList.toggle("active");

});

