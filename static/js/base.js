// Toggle navigation .active
let navlinks = document.querySelectorAll('.nav-link');

navlinks.forEach((link) => {
    // Add a click event on each link
    link.addEventListener("click", () => {
      let currActive = document.querySelector(".active");
      if (currActive) {
        currActive.classList.toggle("active");
      }
      link.classList.toggle("active");
    });
  });

  // Enable popovers
  const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
  const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl), {
    container: 'body'
  })