(function () {
  "use strict";

  var STORAGE_KEY = "sphinx-hextra:theme";
  var root = document.documentElement;

  function apply(theme) {
    if (theme === "dark") {
      root.classList.add("dark");
    } else {
      root.classList.remove("dark");
    }
  }

  function resolveInitial() {
    try {
      var stored = localStorage.getItem(STORAGE_KEY);
      if (stored === "dark" || stored === "light") return stored;
    } catch (e) { /* ignore */ }
    if (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) {
      return "dark";
    }
    return "light";
  }

  apply(resolveInitial());

  document.addEventListener("DOMContentLoaded", function () {
    var btn = document.querySelector(".hx-theme-toggle");
    if (!btn) return;
    btn.addEventListener("click", function () {
      var next = root.classList.contains("dark") ? "light" : "dark";
      apply(next);
      try { localStorage.setItem(STORAGE_KEY, next); } catch (e) { /* ignore */ }
    });
  });
})();
