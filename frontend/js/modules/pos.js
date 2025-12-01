// Add item to cart
function addToCart(id, name, price) {
  const cart = getCart();
  const existing = cart.find((c) => c.id === id);

  if (existing) {
    existing.qty++;
  } else {
    cart.push({ id, name, price, qty: 1 });
  }

  setCart(cart);
  renderCart();
}

// Remove item from cart
function removeFromCart(index) {
  const cart = getCart();
  cart.splice(index, 1);
  setCart(cart);
  renderCart();
}

// Render cart UI
function renderCart() {
  const cart = getCart();
  const container = document.getElementById("cart-items");
  const totalEl = document.getElementById("cart-total");

  if (!container || !totalEl) return;

  if (cart.length === 0) {
    container.innerHTML = `
      <div class="flex flex-col items-center text-slate-300 mt-10">
        <i class="fa-solid fa-basket-shopping text-4xl mb-2"></i>
        <span class="text-sm">No items selected</span>
      </div>
    `;
    totalEl.innerText = "Rp 0";
    return;
  }

  let total = 0;
  container.innerHTML = cart
    .map((item, idx) => {
      const itemTotal = item.price * item.qty;
      total += itemTotal;

      return `
        <div class="flex justify-between items-center bg-slate-50 p-3 rounded-lg border border-slate-100">
          <div>
            <p class="text-sm font-semibold text-slate-900">${item.name}</p>
            <p class="text-xs text-slate-500">${formatCurrency(item.price)} x ${
        item.qty
      }</p>
          </div>
          <div class="flex items-center gap-2">
            <p class="text-sm font-bold text-slate-900">${formatCurrency(
              itemTotal
            )}</p>
            <button onclick="removeFromCart(${idx})" class="text-slate-400 hover:text-red-500 ml-1">
              <i class="fa-solid fa-xmark"></i>
            </button>
          </div>
        </div>
      `;
    })
    .join("");

  totalEl.innerText = formatCurrency(total);
}

// Process checkout/payment
async function processCheckout() {
  const resId = document.getElementById("reservation-select")?.value;
  const cart = getCart();

  if (!resId) {
    return showWarning("Please SELECT A RESERVATION first!");
  }

  if (cart.length === 0) {
    return showWarning("Cart is empty");
  }

  // Create order
  const orderRes = await api("/orders", "POST", {
    reservation_id: resId,
  });

  if (orderRes && orderRes.id) {
    // Add order items
    for (const item of cart) {
      await api(`/orders/${orderRes.id}/items`, "POST", {
        menu_id: item.id,
        quantity: item.qty,
      });
    }

    showSuccess("Order Placed Successfully!");

    // Clear cart and reset
    clearCart();
    renderCart();

    const select = document.getElementById("reservation-select");
    if (select) {
      select.value = "";
    }

    // Refresh dashboard data
    fetchReports();
  }
}
