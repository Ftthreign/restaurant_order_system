let reservations = [];

async function fetchReservations() {
  const data = await api("/reservations");
  if (data) {
    reservations = data;
    renderReservationTable();
  }
}

async function populateReservationDropdowns() {
  const custSelect = document.getElementById("res-cust-id");
  const tableSelect = document.getElementById("res-table-id");

  if (!custSelect || !tableSelect) return;

  // Tampilkan state loading
  custSelect.innerHTML = '<option value="">Loading...</option>';
  tableSelect.innerHTML = '<option value="">Loading...</option>';

  try {
    const [customersData, tablesData] = await Promise.all([
      api("/customers"),
      api("/tables"),
    ]);

    if (customersData) {
      custSelect.innerHTML = '<option value="">-- Select Customer --</option>';
      customersData.forEach((c) => {
        const opt = document.createElement("option");
        opt.value = c.id;
        opt.text = `${c.name} (${c.phone})`;
        custSelect.appendChild(opt);
      });
    }

    if (tablesData) {
      tableSelect.innerHTML = '<option value="">-- Select Table --</option>';
      tablesData.forEach((t) => {
        const opt = document.createElement("option");
        opt.value = t.id;
        opt.text = `Table ${t.table_number} (Cap: ${t.capacity})`;
        tableSelect.appendChild(opt);
      });
    }
  } catch (error) {
    console.error("Failed to load dropdowns", error);
    custSelect.innerHTML = '<option value="">Error loading data</option>';
    tableSelect.innerHTML = '<option value="">Error loading data</option>';
  }
}

async function openCreateReservation() {
  // Reset Form
  document.getElementById("res-edit-id").value = "";
  document.getElementById("res-date").value = "";
  document.getElementById("res-time").value = "";
  document.getElementById("res-modal-title").innerText = "New Reservation";
  openModal("reservation-modal");
  await populateReservationDropdowns();
}

async function openEditReservation(id) {
  const item = reservations.find((r) => r.id === id);
  if (!item) return;

  document.getElementById("res-edit-id").value = item.id;
  document.getElementById("res-date").value = item.date;
  document.getElementById("res-time").value = item.time; // Format HH:MM:SS
  document.getElementById("res-modal-title").innerText = "Edit Reservation";

  openModal("reservation-modal");

  await populateReservationDropdowns();

  if (item.customer && item.customer.id) {
    document.getElementById("res-cust-id").value = item.customer.id;
  }

  if (item.table && item.table.id) {
    document.getElementById("res-table-id").value = item.table.id;
  }
}

// 5. Save reservation (Create or Update)
async function saveReservation() {
  const id = document.getElementById("res-edit-id").value;

  // Ambil value dari <select> (ini akan berisi UUID)
  const custId = document.getElementById("res-cust-id").value;
  const tableId = document.getElementById("res-table-id").value;

  const date = document.getElementById("res-date").value;
  let time = document.getElementById("res-time").value;

  if (!custId || !tableId || !date || !time) {
    return alert("Please fill all fields");
  }

  if (time.length === 5) {
    time += ":00";
  }

  const payload = {
    customer_id: custId,
    table_id: tableId,
    date,
    time,
  };

  let res;
  if (id) {
    res = await api(`/reservations/${id}`, "PUT", payload);
  } else {
    res = await api("/reservations", "POST", payload);
  }

  if (res) {
    closeModal("reservation-modal");
    fetchReservations();
  }
}

async function deleteReservation(id) {
  if (confirm("Cancel this reservation?")) {
    await api(`/reservations/${id}`, "DELETE");
    fetchReservations();
  }
}

function renderReservationTable() {
  const tbody = document.getElementById("reservation-table-body");
  if (!tbody) return;

  tbody.innerHTML = reservations
    .map(
      (r) => `
        <tr class="hover:bg-slate-50">
          <td class="px-6 py-4">
            <div class="font-medium text-slate-900">${r.date}</div>
            <div class="text-xs text-slate-500">${r.time}</div>
          </td>
          <td class="px-6 py-4 font-medium">
            ${r.customer ? r.customer.name : "Unknown"}
          </td>
          <td class="px-6 py-4">
            <span class="bg-slate-100 text-slate-700 px-2 py-1 rounded text-xs font-bold">
              Table ${r.table ? r.table.table_number : "?"}
            </span>
          </td>
          <td class="px-6 py-4 text-right">
            <button onclick="openEditReservation('${
              r.id
            }')" class="text-blue-500 hover:text-blue-700 bg-blue-50 p-2 rounded-md mr-1">
              <i class="fa-solid fa-pen"></i>
            </button>
            <button onclick="deleteReservation('${
              r.id
            }')" class="text-red-500 hover:text-red-700 bg-red-50 p-2 rounded-md">
              <i class="fa-solid fa-trash"></i>
            </button>
          </td>
        </tr>
      `
    )
    .join("");
}

async function loadReservationOptions() {
  const select = document.getElementById("reservation-select");
  if (!select) return;

  select.innerHTML = "<option>Loading...</option>";

  const data = await api("/reservations");
  if (!data || data.length === 0) {
    select.innerHTML = '<option value="">-- No Reservations Found --</option>';
    return;
  }

  select.innerHTML = '<option value="">-- Select Customer / Table --</option>';

  data.forEach((res) => {
    const cust = res.customer ? res.customer.name : "Unknown";
    const table = res.table ? res.table.table_number : "?";
    const time = res.time ? res.time.toString().substring(0, 5) : "";

    const option = document.createElement("option");
    option.value = res.id;
    option.text = `Table ${table} • ${cust} (${time})`;
    select.appendChild(option);
  });
}
