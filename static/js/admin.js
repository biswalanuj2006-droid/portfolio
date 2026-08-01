/* ============================================================
   Admin panel - JavaScript
   ============================================================ */
(() => {
  "use strict";

  const $ = (sel) => document.querySelector(sel);
  const $$ = (sel) => Array.from(document.querySelectorAll(sel));

  /* ---------- Sidebar toggle ---------- */
  const burger = $("#adminBurger");
  const sidebar = $("#adminSidebar");
  if (burger && sidebar) {
    burger.addEventListener("click", () => sidebar.classList.toggle("open"));
  }

  /* ---------- Delete confirmation ---------- */
  $$(".delete-form").forEach((form) => {
    form.addEventListener("submit", (e) => {
      const msg = form.dataset.confirm || "Delete this entry?";
      if (!window.confirm(msg)) e.preventDefault();
    });
  });

  /* ---------- File/image preview in forms ---------- */
  $$('input[type="file"]').forEach((input) => {
    input.addEventListener("change", () => {
      const preview = document.getElementById(`preview-${input.name}`);
      if (!preview || !input.files || !input.files[0]) return;
      const reader = new FileReader();
      reader.onload = (e) => {
        preview.src = e.target.result;
        preview.style.display = "block";
      };
      reader.readAsDataURL(input.files[0]);
    });
  });

  /* ---------- Dashboard charts (Chart.js) ---------- */
  const chartData = (id) => {
    const el = document.getElementById(id);
    if (!el) return null;
    try { return JSON.parse(el.textContent); } catch (err) { return null; }
  };
  const gridColor = "rgba(147,160,196,0.12)";
  const textColor = "#93a0c4";
  const brand = getComputedStyle(document.documentElement).getPropertyValue("--brand-primary").trim() || "#6c5ce7";
  const accent = getComputedStyle(document.documentElement).getPropertyValue("--brand-accent").trim() || "#00d4ff";

  if (window.Chart) {
    const visitors = chartData("visitorsData");
    if (visitors && document.getElementById("chartVisitors")) {
      new Chart(document.getElementById("chartVisitors"), {
        type: "line",
        data: {
          labels: visitors.labels,
          datasets: [{
            label: "Visitors",
            data: visitors.values,
            borderColor: accent,
            backgroundColor: "rgba(0,212,255,0.12)",
            fill: true,
            tension: 0.4,
            pointBackgroundColor: accent,
          }],
        },
        options: {
          responsive: true,
          plugins: { legend: { display: false } },
          scales: {
            x: { ticks: { color: textColor }, grid: { color: gridColor } },
            y: { beginAtZero: true, ticks: { color: textColor }, grid: { color: gridColor } },
          },
        },
      });
    }

    const projects = chartData("projectsData");
    if (projects && document.getElementById("chartProjects")) {
      new Chart(document.getElementById("chartProjects"), {
        type: "doughnut",
        data: {
          labels: projects.labels,
          datasets: [{
            data: projects.values,
            backgroundColor: [brand, accent, "#f39c12", "#e84393", "#00b894", "#636e72"],
            borderWidth: 0,
          }],
        },
        options: { responsive: true, plugins: { legend: { labels: { color: textColor } } } },
      });
    }

    const skills = chartData("skillsData");
    if (skills && document.getElementById("chartSkills")) {
      new Chart(document.getElementById("chartSkills"), {
        type: "bar",
        data: {
          labels: skills.labels,
          datasets: [{
            label: "Skills",
            data: skills.values,
            backgroundColor: brand,
            borderRadius: 8,
          }],
        },
        options: {
          responsive: true,
          plugins: { legend: { display: false } },
          scales: {
            x: { ticks: { color: textColor }, grid: { display: false } },
            y: { beginAtZero: true, ticks: { color: textColor }, grid: { color: gridColor } },
          },
        },
      });
    }
  }
})();
