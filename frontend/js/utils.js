// Modal Management
function openModal(id) {
  const modal = document.getElementById(id);
  if (modal) {
    modal.classList.remove("hidden");
  }
}

function closeModal(id) {
  const modal = document.getElementById(id);
  if (modal) {
    modal.classList.add("hidden");
  }
}

// Number Formatting
function formatCurrency(amount) {
  return `Rp ${amount.toLocaleString()}`;
}

// Date Formatting
function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toLocaleDateString("id-ID");
}

function formatTime(timeString) {
  if (!timeString) return "";
  return timeString.substring(0, 5); // HH:MM
}

// Validation
function validateFields(...fields) {
  return fields.every((field) => field && field.trim() !== "");
}

// Alert Helpers
function showAlert(message, type = "info") {
  alert(message);
}

function showSuccess(message) {
  showAlert(`✅ ${message}`);
}

function showError(message) {
  showAlert(`⚠️ ${message}`);
}

function showWarning(message) {
  showAlert(`⚠️ ${message}`);
}

// Confirmation Dialog
function confirmAction(message) {
  return confirm(message);
}

function showError(message) {
  const toast = document.getElementById("error-toast");
  toast.innerText = message;

  toast.classList.remove("hidden");

  // hide after 3s
  setTimeout(() => {
    toast.classList.add("hidden");
  }, 3000);
}
