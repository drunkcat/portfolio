function updateSearchLanguage() {
  const input = document.querySelector(".md-search__input");
  if (!input) return;
  const polish = /\/pl(?:\/|$)/.test(window.location.pathname);
  input.placeholder = polish ? "Szukaj" : "Search";
  input.setAttribute("aria-label", input.placeholder);
}

function updatePortfolioUi() {
  updateSearchLanguage();
}

document.addEventListener("DOMContentLoaded", updatePortfolioUi);
window.addEventListener("load", updatePortfolioUi);
if (typeof document$ !== "undefined") document$.subscribe(updatePortfolioUi);
