function nav(sectionId) {
  const contentArea = document.getElementById("main-content-area");

  if (!TEMPLATES[sectionId]) {
    console.error("Template not found for:", sectionId);
    return;
  }

  contentArea.innerHTML = TEMPLATES[sectionId];

  document.querySelectorAll(".nav-item").forEach((el) => {
    el.classList.remove("bg-slate-900", "text-white");
    el.classList.add("text-slate-600", "hover:bg-slate-50");
  });

  const btn = document.getElementById(`btn-${sectionId}`);
  if (btn) {
    btn.classList.remove("text-slate-600", "hover:bg-slate-50");
    btn.classList.add("bg-slate-900", "text-white");
  }

  const title =
    sectionId.charAt(0).toUpperCase() + sectionId.slice(1).replace("-", " ");
  const titleEl = document.getElementById("page-title");
  if (titleEl) titleEl.innerText = title;

  window.location.hash = sectionId;

  loadSectionData(sectionId);
}

// Load data based on section (sama seperti sebelumnya)
function loadSectionData(sectionId) {
  switch (sectionId) {
    case "menu":
      fetchMenus();
      break;
    case "customers":
      fetchCustomers();
      break;
    case "tables":
      fetchTables();
      break;
    case "reservations":
      fetchReservations();
      break;
    case "dashboard":
      fetchReports();
      break;
    case "orders":
      fetchMenus();
      loadReservationOptions();
      break;
  }
}
