
(venv) C:\Users\Luke_Lenovo\Documents\GitHub\3200_sqlalchemy_prettyprint_tutorials\create_one_to_many_relationship>python
Python 3.7.1 (v3.7.1:260ec2c36a, Oct 20 2018, 14:05:16) [MSC v.1915 32 bit (Intel)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> from application import db
>>> db.create_all()
>>> from application import Member, Order
>>> mem = Member(username='Susan')
>>> ord = Order(price=99)
>>> mem.orders.append(ord)
>>> db.session.add(mem)
>>> db.session.commit()
>>> mem.orders[0].price
99
>>> ord.member_id
1
>>> mem.orders
[<Order 1>]

