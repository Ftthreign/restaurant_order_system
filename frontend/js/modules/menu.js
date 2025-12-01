// Fetch all menus
async function fetchMenus() {
  const data = await api("/menus");
  if (data) {
    setState("menus", data);
    renderMenuTable();
    renderPosGrid();
  }
}

// Open modal for creating new menu
function openCreateMenu() {
  document.getElementById("menu-edit-id").value = "";
  document.getElementById("new-menu-name").value = "";
  document.getElementById("new-menu-price").value = "";
  document.getElementById("menu-modal-title").innerText = "Add New Menu";
  openModal("menu-modal");
}

// Open modal for editing existing menu
function openEditMenu(id) {
  const menus = getState("menus");
  const item = menus.find((m) => m.id === id);
  if (!item) return;

  document.getElementById("menu-edit-id").value = item.id;
  document.getElementById("new-menu-name").value = item.name;
  document.getElementById("new-menu-price").value = item.price;
  document.getElementById("menu-modal-title").innerText = "Edit Menu";
  openModal("menu-modal");
}

// Save menu (create or update)
async function saveMenu() {
  const id = document.getElementById("menu-edit-id").value;
  const name = document.getElementById("new-menu-name").value;
  const priceStr = document.getElementById("new-menu-price").value;
  const price = parseInt(priceStr);

  if (!validateFields(name, priceStr)) {
    return showError("Fill all fields");
  }

  let res;
  if (id) {
    // Update existing menu
    res = await api(`/menus/${id}`, "PUT", { name, price });
  } else {
    // Create new menu
    res = await api("/menus", "POST", { name, price });
  }

  if (res) {
    closeModal("menu-modal");
    fetchMenus();
    showSuccess(id ? "Menu updated!" : "Menu created!");
  }
}

// Delete menu
async function deleteMenu(id) {
  if (confirmAction("Delete this menu item?")) {
    const res = await api(`/menus/${id}`, "DELETE");
    if (res !== null) {
      fetchMenus();
      showSuccess("Menu deleted!");
    }
  }
}

// Render menu table
function renderMenuTable() {
  const menus = getState("menus");
  const tbody = document.getElementById("menu-table-body");

  if (!tbody) return;

  tbody.innerHTML = menus
    .map(
      (item) => `
        <tr class="hover:bg-slate-50">
          <td class="px-6 py-4 font-medium text-slate-900">${item.name}</td>
          <td class="px-6 py-4">${formatCurrency(item.price)}</td>
          <td class="px-6 py-4 text-right">
            <button onclick="openEditMenu('${
              item.id
            }')" class="text-blue-500 hover:text-blue-700 bg-blue-50 p-2 rounded-md mr-1">
              <i class="fa-solid fa-pen"></i>
            </button>
            <button onclick="deleteMenu('${
              item.id
            }')" class="text-red-500 hover:text-red-700 bg-red-50 p-2 rounded-md">
              <i class="fa-solid fa-trash"></i>
            </button>
          </td>
        </tr>
      `
    )
    .join("");
}

function renderPosGrid() {
  const menus = getState("menus");
  const grid = document.getElementById("pos-grid");

  if (!grid) return;

  grid.innerHTML = menus
    .map(
      (item) => `
        <div onclick="addToCart('${item.id}', '${item.name}', ${item.price})" 
             class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm cursor-pointer hover:border-slate-900 transition-all group">
          <div class="h-20 bg-slate-50 rounded-lg mb-3 flex items-center justify-center text-slate-300 group-hover:bg-slate-100 group-hover:text-slate-500">
            <i class="fa-solid fa-utensils text-2xl"></i>
          </div>
          <h4 class="font-semibold text-slate-900 text-sm">${item.name}</h4>
          <p class="text-slate-500 text-xs mt-1">${formatCurrency(
            item.price
          )}</p>
        </div>
      `
    )
    .join("");
}
