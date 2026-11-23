// Logo Animation
document.querySelectorAll(".logo").forEach(function (logo) {
    logo.addEventListener("mouseout", function () {
        logo.classList.add("logoHoverRemoved");
    });
});
