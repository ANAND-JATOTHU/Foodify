document.addEventListener("DOMContentLoaded", () => {
  // Load navbar and footer from shared HTML files
  fetch("shared/navbar.html")
    .then(response => response.text())
    .then(data => document.querySelector("header").innerHTML = data);

  fetch("shared/footer.html")
    .then(response => response.text())
    .then(data => document.querySelector("footer").innerHTML = data);
});
