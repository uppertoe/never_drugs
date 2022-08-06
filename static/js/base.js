let navlinks = document.querySelectorAll('.nav-link');

navlinks.forEach((link) => {
    // Add a click event on each link
    link.addEventListener("click", () => {
      let currActive = document.querySelector(".active");
      currActive.classList.toggle("active");
      link.classList.toggle("active");
    });
  });