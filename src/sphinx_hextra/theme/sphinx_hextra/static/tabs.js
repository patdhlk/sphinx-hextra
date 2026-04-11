(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", function () {
    var containers = document.querySelectorAll("[data-hx-tabs]");
    containers.forEach(function (container) {
      var labels = container.querySelectorAll(".hx-tabs__label");
      var panels = container.querySelectorAll(".hx-tabs__panel");
      labels.forEach(function (label, idx) {
        label.addEventListener("click", function () {
          labels.forEach(function (l) { l.classList.remove("hx-tabs__label--active"); });
          panels.forEach(function (p) { p.classList.remove("hx-tabs__panel--active"); });
          label.classList.add("hx-tabs__label--active");
          if (panels[idx]) panels[idx].classList.add("hx-tabs__panel--active");
        });
      });
    });
  });
})();
