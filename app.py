from flask import Flask, render_template, request, redirect, flash, session, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
# from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meatbangladbms.sqlite'
app.config['SECRET_KEY']='b8d1532b75e9bc33973341fd'
app.config["SESSION_PARMANENT"]=False
app.config["SESSION_FILE"]='filesystem'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
# Hardcoded admin credentials
ADMIN_CREDENTIALS = {"username": "admin", "password": "123"}

# In-memory storage for products and sales (replace with a database in production)
products = {
    "chicken": [],
    "beef": [],
    "mutton": [],
    "fish": [],
}
sales = []
# login_manager = LoginManager(app)
# login_manager.login_view = 'user_login'

# user class
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    remarks = db.Column(db.String(255), nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'User: {self.username}'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
with app.app_context():
    db.create_all()

# # User loader function
# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

# home index
@app.route('/')
def home():
    return render_template('admin/index.html', title='Meat Bangla')

# register
@app.route('/user/sign-up/', methods=['POST', 'GET'])
def user_signup():
    if request.method == 'POST':
        username=request.form.get('username')
        name=request.form.get('name')
        age=request.form.get('age')
        gender=request.form.get('gender')
        email=request.form.get('email')
        phone=request.form.get('phone')
        address=request.form.get('address')
        remarks=request.form.get('remarks')
        password=request.form.get('password')

        if not all([username, name, age, gender, email, phone, address, password]):
            flash("All the fields except 'remarks' are required.")
            return redirect(url_for('user_signup'))
        else:
            if User.query.filter_by(username=username).first():
                flash("Username already exists. Use a different username.")
                return redirect(url_for('user_signup'))
            password_hash = bcrypt.generate_password_hash(password, 10).decode('utf-8')
            try:
                user = User(username=username, name=name, age=int(age), gender=gender, email=email, phone=phone, address=address, remarks=remarks, password_hash=password_hash)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('user_dashboard', username=user.username, msg="Account created successfully"))
            except Exception as e:
                db.session.rollback()
                flash("An error occurred while creating your account.")
                print(f"Error: {e}")
                return redirect(url_for('user_signup'))

    return render_template('user/signup.html', title='Signup')

# login
# @app.route('/admin-login/', methods=['POST', 'GET'])
# def admin_login():
    
#     return render_template('admin/admin.html', title='Login')

# login
@app.route('/user/login/', methods=['POST', 'GET'])
def user_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not all([username, password]):
            flash("All the fields are required.")
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            # login_user(user)
            return redirect(url_for('user_dashboard'))
        else:
            flash("Username or password don't match. Please try again.")
    msg = request.args.get('msg')
    if msg:
        flash(msg, 'warning')
    return render_template('user/login.html', title="Login")

@app.route('/logout')
# @login_required
def user_logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('home'))

@app.route('/user/dashboard')
def user_dashboard():
    if 'user_id' not in session:
        flash("Please login to access this page.")
        return redirect(url_for('user_login'))
    else:
        username = session.get('username')
        flash("Logged in successfully!")
        return render_template('user/dashboard.html', username=username, title="User Dashboard")

@app.route('/chicken')
def chicken():
    return render_template('chicken.html', title="Chicken")

@app.route('/mutton')
def mutton():
    return render_template('mutton.html', title="Mutton")

# @app.route('/beef')
# def beef():
#     return render_template('beef.html', title="Beef")

@app.route('/fish')
def fish():
    return render_template('fish.html', title="Fish")

# @app.route('/cart')
# def cart():
#     return render_template('cart.html', title="Cart")


# Initialize session data
@app.before_request
def initialize_cart():
    if "cart" not in session:
        session["cart"] = []

# Route to display beef products
@app.route("/beef")
def beef():
    return render_template("beef.html")

# Add to Cart Route
@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    product = request.json
    cart = session.get("cart", [])
    
    # Check if the product is already in the cart
    for item in cart:
        if item["id"] == product["id"]:
            item["quantity"] += 1
            session["cart"] = cart
            return jsonify({"success": True})
    
    # Add new product
    cart.append(product)
    session["cart"] = cart
    return jsonify({"success": True})

# Cart Page
@app.route("/cart", methods=["GET"])
def cart():
    cart = session.get("cart", [])
    subtotal = sum(item["price"] * item["quantity"] for item in cart)
    discount = 0

    # Apply a discount if subtotal exceeds 3000
    if subtotal > 3000:
        discount = subtotal * 0.1  # 10% discount

    delivery_location = session.get("delivery_location", "inside")  # Default to inside Dhaka
    delivery_charge = 60 if delivery_location == "inside" else 120

    total = subtotal - discount + delivery_charge

    return render_template(
        "cart.html",
        cart=cart,
        subtotal=subtotal,
        discount=discount,
        delivery_charge=delivery_charge,
        total=total,
    )


# Place Order
@app.route("/place_order", methods=["POST"])
def place_order():
    data = request.json
    payment_method = data.get("paymentMethod")
    delivery_address = data.get("deliveryAddress")

    if not delivery_address:
        return jsonify({"success": False, "message": "Delivery address is required."})

    # Process the order (e.g., save to database, reduce stock, etc.)
    # Simulating order placement here:
    try:
        order_id = save_order_to_db(session["cart"], payment_method, delivery_address)

        # Clear the cart after placing the order
        session["cart"] = []

        return jsonify ({"success": True, "message": f"Order placed successfully!  Order ID: {order_id}"})
    except Exception as e:
        return jsonify({"success": False, "message": "Failed to place order. Please try again."})

def save_order_to_db(cart, payment_method, delivery_address):
    # Simulated database save
    order_id = generate_order_id()  # Replace with actual DB logic
    print(f"Order saved: {order_id}, Cart: {cart}, Payment: {payment_method}, Address: {delivery_address}")
    return order_id

def generate_order_id():
    from datetime import datetime
    return f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}"




## update cart  code
@app.route("/update_cart", methods=["POST"])
def update_cart():
    data = request.json
    product_id = data.get("id")
    action = data.get("action")

    cart = session.get("cart", [])
    updated_cart_item = None

    for item in cart:
        if item["id"] == product_id:
            if action == "increment":
                item["quantity"] += 1
            elif action == "decrement":
                item["quantity"] = max(0, item["quantity"] - 1)
            elif action == "remove":
                cart.remove(item)
            updated_cart_item = item
            break

    session["cart"] = cart

    # Recalculate totals
    subtotal = sum(i["price"] * i["quantity"] for i in cart)
    discount = subtotal * 0.04 if subtotal > 1000 else 0
    delivery_location = session.get("delivery_location", "inside")
    delivery_charge = 60 if delivery_location == "inside" else 120
    total = subtotal - discount + delivery_charge

    return jsonify({
        "success": True,
        "subtotal": subtotal,
        "discount": discount,
        "delivery_charge": delivery_charge,
        "total": total,
        "updated_cart": updated_cart_item,
    })


# admin login from chatgpt
# Admin Login Page
@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == ADMIN_CREDENTIALS["username"] and password == ADMIN_CREDENTIALS["password"]:
            session["admin"] = True
            return redirect(url_for("admin_dashboard"))
        else:
            return render_template("user/admin_login.html", error="Invalid Passwod")
    return render_template("user/admin_login.html")

# Admin Dashboard
@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    total_sales = sum(sale["total"] for sale in sales)
    return render_template("user/admin_dashboard.html", products=products, total_sales=total_sales)

# Add Product
@app.route('/admin/add_product', methods=['POST'])
def add_product():
    data = request.json
    category = data.get('category')
    name = data.get('name')
    price = data.get('price')
    image = data.get('image')

    if category in products:
        products[category].append({'name': name, 'price': price, 'image': image})
        return jsonify({'message': 'Product added successfully!'})
    return jsonify({'message': 'Invalid category'}), 400

@app.route('/get_products/<category>', methods=['GET'])
def get_products_by_category(category):
    if category in products:
        return jsonify(products[category])
    return jsonify({"error": "Invalid category"}), 400

# Remove Product
@app.route("/admin/remove_product", methods=["POST"])
def remove_product():
    if not session.get("admin"):
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    data = request.json
    category = data.get("category")
    name = data.get("name")
    if category in products:
        products[category] = [p for p in products[category] if p["name"] != name]
        return jsonify({"success": True, "message": "Product removed successfully"})
    return jsonify({"success": False, "message": "Invalid category"}), 400

# Logout Admin
@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect(url_for("admin_login"))








@app.route('/about')
def about_us():
    return render_template('about_us.html', title="About")

if __name__ == '__main__':
    app.run(debug=True)