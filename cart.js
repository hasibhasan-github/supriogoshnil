const products = document.querySelectorAll(".product-card");
const cartElement = document.getElementById("cart");

let cart = JSON.parse(localStorage.getItem("cart")) || [];

function displayCart() {
  let total_amount = 0;
  const cartAmount = document.createElement("div");
  cartAmount.innerHTML = "";
  cartElement.innerHTML = "";
  if (cart.length === 0) {
    cartElement.innerHTML = "<p>Your cart is empty.</p>";
    return;
  }
  cart.forEach((item, index) => {
    const cartItem = document.createElement("div");
    cartItem.classList.add("cart-item");
    cartItem.innerHTML = `
            <span>${item.name} - ${item.price} Taka x ${item.quantity}</span>
            <button onclick="removeFromCart(${index})">Remove</button>
        `;
    total_amount += item.price * item.quantity;
    cartElement.appendChild(cartItem);
  });
  if (total_amount > 2000) {
    total_discount = 100 * Math.floor(total_amount / 2000);
    total_amount = total_amount - total_discount;
    cartAmount.innerHTML = `<p>Total Amount (After ${total_discount} Taka Discount): ${total_amount} Taka</p>`;
  } else {
    cartAmount.innerHTML = `<p>Total Amount: ${total_amount} Taka</p>`;
  }
  cartElement.appendChild(cartAmount);
}

function addToCart(product) {
  const existingItem = cart.find((item) => item.id === product.id);
  if (existingItem) {
    existingItem.quantity += 1; // Increment quantity if item exists
  } else {
    cart.push({ ...product, quantity: 1 });
  }
  localStorage.setItem("cart", JSON.stringify(cart)); // Save to local storage
  alert("Added to cart!");
  displayCart();
}

function removeFromCart(index) {
  cart.splice(index, 1); // Remove item
  localStorage.setItem("cart", JSON.stringify(cart)); // Update local storage
  displayCart();
}

products.forEach((product) => {
  product.querySelector(".add-to-cart").addEventListener("click", () => {
    const productData = {
      id: product.dataset.id,
      name: product.dataset.name,
      price: parseFloat(product.dataset.price),
    };
    addToCart(productData);
  });
});

displayCart();
