document.addEventListener("DOMContentLoaded", () => {
  console.log("Restaurant System v" + CONFIG.APP_VERSION + " initialized");
  const hash = window.location.hash.substring(1);

  if (hash && TEMPLATES[hash]) {
    nav(hash);
  } else {
    nav("dashboard"); // Default
  }
});

window.addEventListener("hashchange", () => {
  const hash = window.location.hash.substring(1);
  if (hash && TEMPLATES[hash]) {
    nav(hash);
  }
});

window.addEventListener("error", (event) => {
  console.error("Application error:", event.error);
});
