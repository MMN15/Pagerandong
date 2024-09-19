from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def load_products():
    try:
        with open('products.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_products(products):
    with open('products.json', 'w') as file:
        json.dump(products, file, indent=4)

@app.route('/')
def index():
    products = load_products()
    return render_template('index.html', products=products)

@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        
        # Handle image upload
        image = request.files['image']
        if image:
            image_filename = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            image.save(image_filename)
            image_url = f"/static/images/{image.filename}"
        else:
            image_url = ""

        new_product = {
            'name': name,
            'price': price,
            'description': description,
            'image_url': image_url
        }

        products = load_products()
        products.append(new_product)
        save_products(products)
        return redirect(url_for('index'))

    return render_template('add_product.html')

@app.route('/delete/<product_name>', methods=['POST'])
def delete_product(product_name):
    products = load_products()
    products = [product for product in products if product['name'] != product_name]
    save_products(products)
    return redirect(url_for('index'))

@app.route('/products')
def products():
    products = load_products()
    return render_template('products.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)
