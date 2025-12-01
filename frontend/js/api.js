// API Helper Functions
async function api(endpoint, method = "GET", body = null) {
  const options = {
    method,
    headers: { "Content-Type": "application/json" },
  };

  if (body) {
    options.body = JSON.stringify(body);
  }

  try {
    const response = await fetch(`${CONFIG.API_BASE_URL}${endpoint}`, options);

    // Update connection status
    updateApiStatus(true);

    if (!response.ok) {
      throw new Error(`API Error: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Fetch error:", error);
    updateApiStatus(false);
    return null;
  }
}

function updateApiStatus(isConnected) {
  const statusEl = document.getElementById("api-status");
  if (statusEl) {
    if (isConnected) {
      statusEl.innerHTML =
        '<span class="text-green-600 font-medium">Connected</span>';
    } else {
      statusEl.innerHTML =
        '<span class="text-red-500">Connection Failed</span>';
    }
  }
}
