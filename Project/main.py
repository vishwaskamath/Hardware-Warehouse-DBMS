# import required inbuilt functions

from datetime import date
from flask import Flask, render_template, request, redirect, url_for, flash, json, session, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# config database connection
app.secret_key = "secret key"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'vis123'
app.config['MYSQL_DB'] = 'raika'
mysql = MySQL(app)


# index page
@app.route('/')
def index():
    # return index page / home page
    return render_template('index.html')


# adminlogin page
@app.route('/adminlogin')
def adminlogin():
    # return adminlogin page
    return render_template('auth/adminlogin.html')


# salesmanlogin page
#@app.route('/salesmanlogin')
#def salesmanlogin():
    # return adminlogin page
   # return render_template('auth/salesmanlogin.html')


# adminpanel page
@app.route('/adminpanel')
def adminpanel():
    # return adminpanel page
    return render_template('admin/adminpanel.html')


# salesmanpanel page
# @app.route('/salesmanpanel', methods=['GET', 'POST'])
# def salesmanpanel():
#
#     curcatname = mysql.connection.cursor()
#     curcatname.callproc('Getallproducts')
#     datacatname = curcatname.fetchall()
#     curcatname.close()
#     # return adminpanel page
#     return render_template('admin/salesmanpanel.html', categoryname=datacatname)


# addcategory page
@app.route('/addcategory', methods=['GET', 'POST'])
def addcategory():
    # fetch all the products from category and store it in data
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM category")
    data = cur.fetchall()
    cur.close()

    # post method of the form taking inputs and performing insert operation
    if request.method == "POST":
        # flash message
        flash("Category inserted Successfully")
        details = request.form
        cat_id = details['cat_id']
        name = details['cat_name']

        # mysql connection and insertion
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO category(cat_id, cat_name) VALUES (%s,%s)", [cat_id, name])
        mysql.connection.commit()
        cur.close()

        # redirect to same page
        return redirect(url_for('addcategory'))

    # return addcategory page by default and passing data to the html
    return render_template('admin/addcategory.html', category=data)


# category update page
@app.route('/category/update', methods=['POST', 'GET'])
def category_update():
    # post method of the form taking inputs and performing update operation
    if request.method == 'POST':
        id_data = request.form['cat_id']
        cat_name = request.form['cat_name']

        # mysql connection and updation
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE category
        SET cat_name=%s
        WHERE cat_id=%s
        """, (cat_name, id_data))

        # flash message
        flash("Category updated Successfully")

        mysql.connection.commit()

        # redirect to addcategory page
        return redirect(url_for('addcategory'))


# category delete page
@app.route('/category/delete/<string:id_data>', methods=['POST', 'GET'])
def category_delete(id_data):
    # flash message
    flash("Category deleted Successfully")

    # mysql connection and delete operation
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM category WHERE cat_id = %s', [id_data])
    mysql.connection.commit()

    # redirect to addcategory page
    return redirect(url_for('addcategory'))


# addproducts page
@app.route('/addproduct', methods=['GET', 'POST'])
def addproduct():
    # mysql connection and fetch all category data
    curcat = mysql.connection.cursor()
    curcat.execute("SELECT * FROM category")
    datacat = curcat.fetchall()
    curcat.close()

    # mysql connection and fetch all products data
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products")
    data = cur.fetchall()
    cur.close()

    # mysql connection and calling stored procedure getallproducts
    curcatname = mysql.connection.cursor()
    curcatname.callproc('Getallproducts')
    datacatname = curcatname.fetchall()
    curcatname.close()

    # post method to take form inputs and insert into products
    if request.method == "POST":
        # flash message
        flash("Product inserted Successfully")

        details = request.form
        prod_id = details['prod_id']
        name = details['prod_name']
        desc = details['prod_des']
        cost = details['prod_cost']
        quantity = details['prod_quantity']
        cat_id = details['cat_id']

        # mysql connection and insert operation on products
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO products(prod_id, prod_name, prod_des, prod_cost, prod_quantity, cat_id) VALUES (%s,%s,%s,"
            "%s,%s,%s)",
            [prod_id, name, desc, cost, quantity, cat_id])
        mysql.connection.commit()
        cur.close()

        # return same page
        return redirect(url_for('addproduct'))

    # return addproduct page by default, passing data to the html
    return render_template('admin/addproduct.html', product=data, category=datacat, categoryname=datacatname)


# product update page
@app.route('/product/update', methods=['POST', 'GET'])
def product_update():
    # post method of the form taking inputs and performing update operation
    if request.method == 'POST':
        details = request.form
        id_data = details['prod_id']
        name = details['prod_name']
        desc = details['prod_des']
        cost = details['prod_cost']
        quantity = details['prod_quantity']

        # mysql connection and updation
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE products
        SET prod_name=%s, prod_des=%s, prod_cost=%s, prod_quantity=%s
        WHERE prod_id=%s
        """, (name, desc, cost, quantity, id_data))

        # flash message
        flash("Product updated Successfully")
        mysql.connection.commit()

        # redirect to addproduct page
        return redirect(url_for('addproduct'))


# product delete page
@app.route('/product/delete/<string:id_data>', methods=['POST', 'GET'])
def product_delete(id_data):
    # flash message
    flash("Product deleted Successfully")

    # mysql connection and delete operation
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM products WHERE prod_id = %s', [id_data])
    mysql.connection.commit()

    # redirect to addproduct page
    return redirect(url_for('addproduct'))


# user login page
@app.route('/login', methods=['POST', 'GET'])
def login():
    return render_template('auth/login.html')


# user signup page
@app.route('/signup', methods=['POST', 'GET'])
def signupuser():
    # taking user input from post method and insert operation
    if request.method == 'POST':

        details = request.form
        email = details['cust_email']
        name = details['cust_name']
        phone = details['cust_number']
        street = details['cust_street']
        pincode = details['cust_pincode']
        state = details['cust_state']
        password = details['cust_password']

        # mysql connection
        cur = mysql.connection.cursor()
        cur1 = mysql.connection.cursor()

        # fetching details of customer if already registered via email
        cur.execute("""SELECT * FROM `customers` WHERE `cust_email` LIKE '{}' """.format(email))
        users = cur.fetchall()

        cur.execute("""SELECT cust_id FROM `customers` order by cust_id desc limit 1""")
        custid = cur.fetchall()
        if not custid:
            new_custid = 1
        else:
            new_custid = custid[0][0] + 1

        if len(users) > 0:
            # user email already in use
            flash('User email already registered! Kindly Login !')
            return render_template('auth/login.html')

        else:
            # insert into customer table
            cur.execute(
                "INSERT INTO customers(cust_id, cust_name, cust_phone, cust_email, cust_password, cust_street, "
                "cust_pincode, "
                "cust_state) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",
                [new_custid, name, phone, email, password, street, pincode, state])

            # insert into address table
            cur1.execute(
                "INSERT INTO customer_address(cust_id, cust_street, cust_pincode, "
                "cust_state) VALUES(%s, %s, %s, %s)",
                [new_custid, street, pincode, state])

            flash("Your account was created !, You may now proceed to login.")
            mysql.connection.commit()
            cur.close()
            cur1.close()

        # return to signupuser page
        return redirect(url_for('signupuser'))
    # return signup page
    return render_template('auth/signup.html')


# login user page
@app.route('/loginuser', methods=['POST'])
def loginuser():
    # email and password is fetched
    email = request.form.get('email')
    password = request.form.get('password')

    # check if password and email match the one in database
    cur = mysql.connection.cursor()
    cur.execute("""SELECT * FROM `customers` WHERE `cust_email` LIKE '{}' AND `cust_password` LIKE '{}'""".format(email,
                                                                                                                  password))
    users = cur.fetchall()
    if len(users) > 0:

        # user exists store email in session
        session['current_user'] = email
        return redirect(url_for('homepage'))

    else:

        # user wrong credentials check again
        flash('Wrong credentials!, if you are a new user please signup!')
        return render_template('auth/login.html')


# logout user pop session variable
@app.route('/logout')
def logout():
    session.pop('current_user', None)
    return redirect(url_for('login'))


# customer home page
@app.route('/customer/homepage', methods=['POST', 'GET'])
def homepage():
    # fetch customer email in session
    if 'current_user' in session:
        cr = session['current_user']

    # stored procedure to fetch the product details
    curcatname = mysql.connection.cursor()
    curcatname.callproc('Getallproducts')
    product_data = curcatname.fetchall()
    curcatname.close()

    #  return home page along with the passed data
    return render_template('customer/homepage.html', products=product_data, currentuser=cr)


# add to cart route for creating order
@app.route('/addtocart/<string:data>', methods=['POST', 'GET'])
def customer_addtocart(data):
    cur = mysql.connection.cursor()

    email = data
    today = date.today()
    datenow = today.strftime("%Y/%m/%d")

    # fetching cust_id from the email stored and passed in the form of session data
    cur.execute("SELECT cust_id from customers WHERE `cust_email` LIKE '{}' ".format(email))
    custo_id = cur.fetchall()

    cur.execute("""SELECT ord_id FROM `orders` order by ord_id desc limit 1""")
    ordid = cur.fetchall()
    if not ordid:
        new_ordid = 1
    else:
        new_ordid = ordid[0][0] + 1

    #  insert into order table
    cur.execute("INSERT INTO orders(ord_id, ord_date,cust_id) VALUES(%s, %s, %s)", [new_ordid, datenow, custo_id])
    mysql.connection.commit()

    cur.execute("""SELECT status_id FROM `statuses` order by status_id desc limit 1""")
    statusid = cur.fetchall()
    if not statusid:
        new_statusid = 1
    else:
        new_statusid = statusid[0][0] + 1

    # inserting into status table of the particular order
    cur.execute("INSERT INTO statuses(status_id, ord_id) VALUES(%s, %s)", [new_statusid, new_ordid])

    mysql.connection.commit()
    return '', 204


# add to cart route for inserting ordered_items of the order
@app.route('/addtocart', methods=['POST', 'GET'])
def addtocart():
    # fetch order id in order to insert into the cart table
    cur = mysql.connection.cursor()
    cur.execute("SELECT ord_id from orders ORDER BY ord_id desc limit 1")
    order_id = cur.fetchall()

    if request.method == 'POST':

        # fetch the json data
        req = request.get_json()

        jsonData = json.dumps(req)
        jsonData = json.loads(jsonData)

        # for each item in the cart
        for cartid, qty, cost in zip(jsonData['cartid'], jsonData['cartquantity'], jsonData['cartcost']):

            cur.execute("""SELECT ord_id FROM `ordered_items` order by item_id desc limit 1""")
            orditemid = cur.fetchall()
            if not orditemid:
                new_orditemid = 1
            else:
                new_orditemid = orditemid[0][0] + 1

            #  calculate total cost of each product
            totalcost = float(cost) * float(qty)
            totalcost = round(totalcost)

            # insert into orderded_items table
            cur.execute(
                "INSERT INTO ordered_items(item_id, ord_id, prod_id, prod_cost, item_quantity, total_cost) VALUES(%s, %s, %s, %s, %s, %s)",
                [new_orditemid, order_id, cartid, cost, qty, totalcost])

        mysql.connection.commit()
        return jsonify({'status': 'success'})


#  view order page
@app.route('/vieworder', methods=['POST', 'GET'])
def vieworder():
    # mysql connection and fetch and display orders details
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM orders")
    orderdata = cur.fetchall()
    cur.close()

    # mysql connection and fetching ordered_items details
    cura = mysql.connection.cursor()
    cura.execute("SELECT i.*  FROM orders o, ordered_items i WHERE o.ord_id = i.ord_id ORDER BY i.ord_id")
    orderitemdata = cura.fetchall()
    cura.close()

    return render_template('admin/vieworders.html', vieworder=orderdata, viewitem=orderitemdata)


#  view status page
@app.route('/viewstatus', methods=['POST', 'GET'])
def viewstatus():
    # mysql connection and fetching status details
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM statuses")
    orderdata = cur.fetchall()
    cur.close()

    return render_template('admin/viewstatuses.html', viewstatus=orderdata)


# view statuses page
@app.route('/status/update', methods=['POST', 'GET'])
def status_update():
    # form details to update status details
    if request.method == 'POST':
        status_id = request.form['status_id']
        del_status = request.form['del_status']
        payment_status = request.form['payment_status']

        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE statuses
        SET del_status = %s, payment_status = %s
        WHERE status_id=%s
        """, (del_status, payment_status, status_id))

        mysql.connection.commit()
        return redirect(url_for('viewstatus'))


# view salesdata page
@app.route('/viewinventory', methods=['POST', 'GET'])
def viewinventory():
    # mysql connection and fetching sales details
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT p.prod_id, p.prod_name, SUM(item_quantity) FROM products p, ordered_items o WHERE p.prod_id = "
        "o.prod_id GROUP BY prod_id")
    orderdata = cur.fetchall()
    cur.close()

    return render_template('admin/viewsalesdata.html', productsales=orderdata)


# run main function
if __name__ == "__main__":
    app.run(debug=True)
