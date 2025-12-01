async function api(endpoint, method = "GET", body = null) {
  const options = {
    method,
    headers: {
      Accept: "application/json",
      ...(body ? { "Content-Type": "application/json" } : {}),
    },
    body: body ? JSON.stringify(body) : undefined,
  };

  try {
    const response = await fetch(`${CONFIG.API_BASE_URL}${endpoint}`, options);

    updateApiStatus(true);

    const text = await response.text();
    let data;

    try {
      data = text ? JSON.parse(text) : null;
    } catch {
      data = text;
    }

    if (!response.ok) {
      const message =
        data?.detail || response.statusText || "Unknown API Error";
      throw new Error(message);
    }

    return data;
  } catch (error) {
    console.error("Fetch error:", error);
    updateApiStatus(false);
    throw error;
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
