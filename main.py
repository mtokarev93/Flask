from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

from cloudipsp import Api, Checkout

app = Flask(__name__) #создание объекта на основе класса Flask. Можем отслеживать те функции, которые будут отслеживать переходы на разные URL адреса.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#Чтобы отследить главную страницу, нам необходимо создать декоратор
@app.route('/')
def index():
    items = Item.query.order_by(Item.price).all()
    return render_template('index.html', data=items )


# ORM - Object-relational model
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    
# item = Item(id=....)
# item.save() => 'INSERT INTO items .....'
    # query = 'SELECT * ....'
    # db.execute(query)
    #text = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return self.title

@app.route('/about')
def about():
    return render_template('about.html')

# GET /item/4 => { Холодильник, белый, 100 000 ₽}
# GET /item/4/buying

@app.route('/item/<int:id>/purchase')
def item_buy(id):
    item = Item.query.get(id)
    api = Api(merchant_id=1396424,
              secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "RUB",
        "amount": str(item.price) + "00"
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)

# https://google.ru/products
# REST API

# POST site.ru/item
# GET site.ru/item/3

# site.ru/item
# Это handler (обработчик)
# POST | GET /item

# POST /item 
# body:
# title=Tovar&price=100

# GET site.ru/
# @app.route('/') => "<html><head></head><.....></html>"

# Введите название: Товар
# Введите цену: 20 000
# => POST /item
# BODY
# title=Товар&price=20000

# => request.form = {
#     'title': 'Товар',
#     'price': '20000',
# }


# a = dict()
# 'Vasya' => +7985...
# 'Petya' => +7999...
# Petya?
# a['Petya']

@app.route('/item', methods=['POST', 'GET'])
def create():
    if request.method == "POST":
        title = request.form['title']
        price = request.form['price']

        item = Item(title=title, price=price)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return "Получилась ошибка"
    else:
        return render_template('create.html')

if __name__ == "__main__":
    app.run(debug=True)