// Sample admin credentials
const ADMIN_ID = 'admin';
const ADMIN_PASSWORD = '1234'; // Replace this with a secure password in production

// Daily sales variable (for demonstration purposes)
let dailySales = 0;

// Dummy list of products (initial data)
let products = [
    { id: 1, name: 'Beef Head Meat', price: 550 },
    { id: 2, name: 'Mutton Tehari Cut', price: 1040 }
];

// Admin login validation
function validateAdmin() {
    const adminId = document.getElementById('admin-id').value;
    const adminPassword = document.getElementById('admin-password').value;

    if (adminId === ADMIN_ID && adminPassword === ADMIN_PASSWORD) {
        // Show admin dashboard and hide login section
        document.getElementById('login-section').style.display = 'none';
        document.getElementById('admin-dashboard').style.display = 'block';
        displayProducts();
        updateSalesSummary();
    } else {
        alert('Invalid Admin ID or Password');
    }
}

// Display products in the list
function displayProducts() {
    const productList = document.getElementById('product-list');
    productList.innerHTML = ''; // Clear previous entries

    products.forEach((product) => {
        const li = document.createElement('li');
        li.textContent = `${product.name} - ৳${product.price}`;
        
        const removeButton = document.createElement('button');
        removeButton.textContent = 'Remove';
        removeButton.onclick = () => removeProduct(product.id);
        
        li.appendChild(removeButton);
        productList.appendChild(li);
    });
}

// Add a new product
function addProduct() {
    const productName = document.getElementById('product-name').value;
    const productPrice = parseFloat(document.getElementById('product-price').value);

    if (productName && !isNaN(productPrice)) {
        const newProduct = {
            id: Date.now(), // Unique ID based on timestamp
            name: productName,
            price: productPrice
        };
        
        products.push(newProduct);
        displayProducts();
        alert(`${productName} has been added.`);
        
        // Clear input fields
        document.getElementById('product-name').value = '';
        document.getElementById('product-price').value = '';
    } else {
        alert('Please enter valid product details');
    }
}

// Remove a product by ID
function removeProduct(productId) {
    products = products.filter(product => product.id !== productId);
    displayProducts();
    alert('Product removed successfully.');
}

// Update daily sales summary
function updateSalesSummary() {
    dailySales = products.reduce((total, product) => total + product.price, 0);
    document.getElementById('daily-sales').textContent = `Total Sales: ৳${dailySales}`;
}