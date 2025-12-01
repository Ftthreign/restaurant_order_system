const TEMPLATES = {
  dashboard: `
    <section id="dashboard" class="space-y-6 fade-in">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-slate-500">Total Revenue</p>
            <h3 class="text-2xl font-bold text-slate-900 mt-2" id="dash-total-sales">Rp 0</h3>
          </div>
          <div class="h-12 w-12 bg-green-50 rounded-full flex items-center justify-center text-green-600">
            <i class="fa-solid fa-coins text-xl"></i>
          </div>
        </div>

        <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-slate-500">Total Transactions</p>
            <h3 class="text-2xl font-bold text-slate-900 mt-2" id="dash-total-orders">0</h3>
          </div>
          <div class="h-12 w-12 bg-blue-50 rounded-full flex items-center justify-center text-blue-600">
            <i class="fa-solid fa-receipt text-xl"></i>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
          <h3 class="font-bold text-lg mb-4 text-slate-800">Recent Transactions</h3>
          <div class="relative h-72 w-full">
            <canvas id="salesChart"></canvas>
          </div>
        </div>

        <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
          <h3 class="font-bold text-lg mb-4 text-slate-800">Menu Price Analysis</h3>
          <div class="relative h-72 w-full flex justify-center">
            <canvas id="itemsChart"></canvas>
          </div>
        </div>
      </div>
    </section>
  `,
  orders: `
    <section id="orders" class="h-full flex flex-col fade-in">
      <div class="flex flex-col md:flex-row gap-4 h-full pb-2">
        <div class="flex-1 overflow-y-auto pr-1">
          <div id="pos-grid" class="grid grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4"></div>
        </div>
        <div class="w-full md:w-80 lg:w-96 bg-white rounded-xl border border-slate-200 shadow-sm flex flex-col flex-shrink-0 h-[50vh] md:h-full">
          <div class="p-4 border-b border-slate-100 bg-slate-50 rounded-t-xl">
            <h3 class="font-semibold text-slate-900">Current Order</h3>
            <div class="mt-3 flex gap-2">
              <select id="reservation-select" class="w-full border border-slate-300 p-2 rounded text-sm bg-white outline-none">
                  <option value="">-- No Reservation --</option>
              </select>
              <button onclick="loadReservationOptions()" class="bg-white border px-2 rounded hover:bg-slate-50"><i class="fa-solid fa-sync text-xs"></i></button>
            </div>
          </div>
          <div class="flex-1 overflow-y-auto p-4 space-y-3" id="cart-items">
            <div class="text-center text-slate-400 mt-10 text-sm">Cart is empty</div>
          </div>
          <div class="p-4 border-t border-slate-100 bg-slate-50 rounded-b-xl">
            <div class="flex justify-between mb-4 text-lg font-bold text-slate-900">
              <span>Total</span><span id="cart-total">Rp 0</span>
            </div>
            <button onclick="processCheckout()" class="w-full py-3 bg-slate-900 hover:bg-slate-800 text-white font-bold rounded-lg shadow-lg active:scale-95 transition-all">
              Process Payment
            </button>
          </div>
        </div>
      </div>
    </section>
  `,

  reservations: `
    <section id="reservations" class="space-y-6 fade-in">
      <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <h3 class="font-bold text-lg">Reservation List</h3>
        <button onclick="openCreateReservation()" class="bg-slate-900 text-white px-4 py-2 rounded-lg text-sm shadow-sm hover:bg-slate-800 w-full md:w-auto">
          <i class="fa-solid fa-plus mr-2"></i> New Reservation
        </button>
      </div>
      <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-x-auto">
        <table class="w-full text-sm text-left min-w-[600px]">
          <thead class="bg-slate-50 text-xs text-slate-500 uppercase border-b">
            <tr>
              <th class="px-6 py-3">Date/Time</th>
              <th class="px-6 py-3">Customer</th>
              <th class="px-6 py-3">Table</th>
              <th class="px-6 py-3 text-right">Action</th>
            </tr>
          </thead>
          <tbody id="reservation-table-body" class="divide-y divide-slate-100"></tbody>
        </table>
      </div>
    </section>
  `,

  menu: `
    <section id="menu" class="space-y-6 fade-in">
      <div class="flex justify-between items-center">
        <h3 class="font-bold text-lg">Menu Items</h3>
        <button onclick="openCreateMenu()" class="bg-slate-900 text-white px-4 py-2 rounded-lg text-sm shadow-sm hover:bg-slate-800">
          <i class="fa-solid fa-plus mr-2"></i> Add Menu
        </button>
      </div>
      <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        <table class="w-full text-sm text-left">
          <thead class="bg-slate-50 text-xs text-slate-500 uppercase border-b">
            <tr>
              <th class="px-6 py-3">Name</th>
              <th class="px-6 py-3">Price</th>
              <th class="px-6 py-3 text-right">Action</th>
            </tr>
          </thead>
          <tbody id="menu-table-body" class="divide-y divide-slate-100"></tbody>
        </table>
      </div>
    </section>
  `,

  customers: `
    <section id="customers" class="space-y-6 fade-in">
      <div class="flex justify-between items-center">
        <h3 class="font-bold text-lg">Customer Database</h3>
        <button onclick="openCreateCustomer()" class="bg-slate-900 text-white px-4 py-2 rounded-lg text-sm shadow-sm hover:bg-slate-800">
          <i class="fa-solid fa-plus mr-2"></i> Add Customer
        </button>
      </div>
      <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        <table class="w-full text-sm text-left">
          <thead class="bg-slate-50 text-xs text-slate-500 uppercase border-b">
            <tr>
              <th class="px-6 py-3">Name</th>
              <th class="px-6 py-3">Phone</th>
              <th class="px-6 py-3 text-right">Action</th>
            </tr>
          </thead>
          <tbody id="customer-table-body" class="divide-y divide-slate-100"></tbody>
        </table>
      </div>
    </section>
  `,

  tables: `
    <section id="tables" class="space-y-6 fade-in">
      <div class="flex justify-between items-center">
        <h3 class="font-bold text-lg">Table Layout</h3>
        <button onclick="openCreateTable()" class="bg-slate-900 text-white px-4 py-2 rounded-lg text-sm shadow-sm hover:bg-slate-800">
          <i class="fa-solid fa-plus mr-2"></i> Add Table
        </button>
      </div>
      <div id="tables-grid" class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-6"></div>
    </section>
  `,
};
