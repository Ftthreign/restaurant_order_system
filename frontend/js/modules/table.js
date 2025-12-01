// Table Management Module

// Fetch all tables
async function fetchTables() {
  const data = await api("/tables");
  if (data) {
    setState("tables", data);
    renderTableGrid();
  }
}

// Open modal for creating new table
function openCreateTable() {
  document.getElementById("table-edit-id").value = "";
  document.getElementById("new-table-num").value = "";
  document.getElementById("new-table-cap").value = "";
  document.getElementById("table-modal-title").innerText = "Add New Table";
  openModal("table-modal");
}

// Open modal for editing existing table
function openEditTable(id) {
  const tables = getState("tables");
  const item = tables.find((t) => t.id === id);
  if (!item) return;

  document.getElementById("table-edit-id").value = item.id;
  document.getElementById("new-table-num").value = item.table_number;
  document.getElementById("new-table-cap").value = item.capacity;
  document.getElementById("table-modal-title").innerText = "Edit Table";
  openModal("table-modal");
}

// Save table (create or update)
async function saveTable() {
  const id = document.getElementById("table-edit-id").value;
  const numStr = document.getElementById("new-table-num").value;
  const capStr = document.getElementById("new-table-cap").value;

  if (!validateFields(numStr, capStr)) {
    return showError("Fill all fields");
  }

  const num = parseInt(numStr);
  const cap = parseInt(capStr);

  let res;
  if (id) {
    res = await api(`/tables/${id}`, "PUT", {
      table_number: num,
      capacity: cap,
    });
  } else {
    res = await api("/tables", "POST", {
      table_number: num,
      capacity: cap,
    });
  }

  if (res) {
    closeModal("table-modal");
    fetchTables();
    showSuccess(id ? "Table updated!" : "Table created!");
  }
}

// Delete table
async function deleteTable(id) {
  if (confirmAction("Delete this table?")) {
    const res = await api(`/tables/${id}`, "DELETE");
    if (res !== null) {
      fetchTables();
      showSuccess("Table deleted!");
    }
  }
}

// Render table grid
function renderTableGrid() {
  const tables = getState("tables");
  const grid = document.getElementById("tables-grid");

  if (!grid) return;

  grid.innerHTML = tables
    .map(
      (t) => `
        <div class="aspect-square bg-white border border-slate-200 rounded-xl flex flex-col items-center justify-center relative group hover:border-slate-900 transition-colors">
          <div class="absolute top-2 right-2 hidden group-hover:flex gap-1">
            <button onclick="openEditTable('${t.id}')" class="text-blue-400 hover:text-blue-600">
              <i class="fa-solid fa-pen"></i>
            </button>
            <button onclick="deleteTable('${t.id}')" class="text-slate-300 hover:text-red-500">
              <i class="fa-solid fa-trash"></i>
            </button>
          </div>
          <div class="w-16 h-16 bg-slate-50 rounded-full border border-slate-100 flex items-center justify-center mb-2 text-slate-800 font-bold text-xl">
            ${t.table_number}
          </div>
          <span class="text-xs text-slate-500 font-medium">${t.capacity} Seats</span>
        </div>
      `
    )
    .join("");
}
