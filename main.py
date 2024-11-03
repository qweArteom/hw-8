from flask import Flask, render_template, redirect, url_for, request, flash
from models import db, MenuItem
from forms import MenuItemForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizzeria.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'supersecretkey'

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    menu_items = MenuItem.query.all()
    return render_template('menu.html', menu_items=menu_items)


@app.route('/')
def index():
    menu_items = MenuItem.query.all()
    return render_template('index.html', menu_items=menu_items)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    form = MenuItemForm()
    if form.validate_on_submit():
        new_item = MenuItem(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data
        )
        db.session.add(new_item)
        db.session.commit()
        flash('Страву додано до меню', 'success')
        return redirect(url_for('admin'))
    menu_items = MenuItem.query.all()
    return render_template('admin.html', form=form, menu_items=menu_items)


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_item(id):
    item = MenuItem.query.get_or_404(id)
    form = MenuItemForm(obj=item)
    if form.validate_on_submit():
        item.name = form.name.data
        item.description = form.description.data
        item.price = form.price.data
        db.session.commit()
        flash('Страву оновлено', 'success')
        return redirect(url_for('admin'))
    return render_template('admin.html', form=form, menu_items=MenuItem.query.all(), edit_item=item)


@app.route('/delete/<int:id>', methods=['POST'])
def delete_item(id):
    item = MenuItem.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Страву видалено', 'warning')
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)