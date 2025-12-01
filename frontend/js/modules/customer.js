async function fetchCustomers() {
  const data = await api("/customers");
  if (data) {
    setState("customers", data);
    renderCustomerTable();
  }
}

function openCreateCustomer() {
  document.getElementById("cust-edit-id").value = "";
  document.getElementById("new-cust-name").value = "";
  document.getElementById("new-cust-phone").value = "";
  document.getElementById("cust-modal-title").innerText = "Add New Customer";
  openModal("customer-modal");
}

function openEditCustomer(id) {
  const customers = getState("customers");
  const item = customers.find((c) => c.id === id);
  if (!item) return;

  document.getElementById("cust-edit-id").value = item.id;
  document.getElementById("new-cust-name").value = item.name;
  document.getElementById("new-cust-phone").value = item.phone;
  document.getElementById("cust-modal-title").innerText = "Edit Customer";
  openModal("customer-modal");
}

async function saveCustomer() {
  const id = document.getElementById("cust-edit-id").value;
  const name = document.getElementById("new-cust-name").value;
  const phone = document.getElementById("new-cust-phone").value;

  if (!validateFields(name, phone)) {
    return showError("Fill all fields");
  }

  let res;
  if (id) {
    res = await api(`/customers/${id}`, "PUT", { name, phone });
  } else {
    res = await api("/customers", "POST", { name, phone });
  }

  if (res) {
    closeModal("customer-modal");
    fetchCustomers();
    showSuccess(id ? "Customer updated!" : "Customer created!");
  }
}

async function deleteCustomer(id) {
  if (confirmAction("Delete this customer?")) {
    const res = await api(`/customers/${id}`, "DELETE");
    if (res !== null) {
      fetchCustomers();
      showSuccess("Customer deleted!");
    }
  }
}

function renderCustomerTable() {
  const customers = getState("customers");
  const tbody = document.getElementById("customer-table-body");

  if (!tbody) return;

  tbody.innerHTML = customers
    .map(
      (c) => `
        <tr class="hover:bg-slate-50">
          <td class="px-6 py-4 font-medium text-slate-900">${c.name}</td>
          <td class="px-6 py-4 text-slate-500">${c.phone}</td>
          <td class="px-6 py-4 text-right">
            <button onclick="openEditCustomer('${c.id}')" class="text-blue-500 hover:text-blue-700 bg-blue-50 p-2 rounded-md mr-1">
              <i class="fa-solid fa-pen"></i>
            </button>
            <button onclick="deleteCustomer('${c.id}')" class="text-red-500 hover:text-red-700 bg-red-50 p-2 rounded-md">
              <i class="fa-solid fa-trash"></i>
            </button>
          </td>
        </tr>
      `
    )
    .join("");
}
