from flask import *
from flask_bootstrap import Bootstrap
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb://neil1:neil1234@ds113853.mlab.com:13853/neilantony2710login?retryWrites=false"
app.config['SECRET_KEY'] = 'onestopshop'

Bootstrap(app)
mongo = PyMongo(app)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/cart')
def cart():
    print(session['cart'])
    y = []
    t = 0
    for z in session['cart']:
        x = mongo.db.itemInfo.find_one({'_id': ObjectId(z)})
        x['itemnum'] = session['cart'][z]
        x['subtotal'] = int(x['itemnum']) * int(x['price'])
        t = t + x['subtotal']
        y.append(x)

    return render_template('cart.html', y=y, total=t)


@app.route('/clearcart')
def clearcart():
    session["cart"] = ''
    return redirect('/cart')


@app.route('/shop', methods=['GET', 'POST'])
def shop():
    if request.method == 'GET':
        y = mongo.db.itemInfo.find()

        return render_template('shop.html', y=y)
    else:
        print(request.form)
        session['cart'] = request.form
        return redirect('/cart')


@app.route('/addProduct', methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template('add.html')
    if request.method == 'POST':
        y = {}
        # for x in request.form:
        #     y[x] = request.form[x].encode('ascii','ignore')
        print(request.form)
        y['title'] = request.form['title']
        y['description'] = request.form['description']
        y['price'] = request.form['price']
        y['unit'] = request.form['unit']
        y['ql'] = request.form['ql']
        y['img'] = request.form['img']
        mongo.db.itemInfo.insert_one(y)

        return redirect('/addProduct')


if __name__ == '__main__':
    app.run(debug=True)
