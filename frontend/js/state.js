// Global State Management
const STATE = {
  cart: [],
  menus: [],
  customers: [],
  tables: [],
  reservations: [],
};

// State Getters
const getState = (key) => STATE[key];

// State Setters
const setState = (key, value) => {
  STATE[key] = value;
};

// Cart Management
const getCart = () => STATE.cart;
const setCart = (cart) => {
  STATE.cart = cart;
};
const clearCart = () => {
  STATE.cart = [];
};
