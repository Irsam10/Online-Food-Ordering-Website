import pymysql
import datetime

class DBHandler:

    #CONSTRUCTOR
    def __init__(self,host, username, password, db):
        self.host = host
        self.username = username
        self.password = password
        self.db = db
        self.connection = pymysql.connect(host= self.host, user= self.username, password= self.password, database= self.db)

    #DESTRUCTOR
    def __del__(self):
        if self.connection != None:
            self.connection.close()

    #==========================HELPER FUNCTIONS====================================
    def usernameOccupied(self,name):
        cur = None
        try:
            cur = self.connection.cursor()
            query= "SELECT * FROM users where user_name=%s"
            cur.execute(query,name)
            data= cur.fetchone()
            if data is None:
                return False
            else:
                return True
        except Exception as err:
            print(err)
        finally:
            cur.close()

    def userEmailOccupied(self,email):
        cur = None
        try:
            cur = self.connection.cursor()
            query= "SELECT * FROM users where user_email=%s"
            cur.execute(query, email)
            data= cur.fetchone()
            if data is None:
                return False
            else:
                return True
        except Exception as err:
            print(err)
        finally:
            cur.close()

    def nonExistent(self,args):
        cur = None
        try:
            cur = self.connection.cursor()
            query = "SELECT * FROM users where user_name=%s and user_pwd=%s"
            cur.execute(query, args)
            data = cur.fetchone()
            if data is None:
                return True
            else:
                return False
        except Exception as err:
            print(err)
        finally:
            cur.close()

    def productAlreadyAdded(self,name):
        cur = None
        try:
            cur = self.connection.cursor()
            query = "SELECT * FROM products where product_name=%s"
            cur.execute(query, name)
            data = cur.fetchone()
            if data is None:
                return False
            else:
                return True
        except Exception as err:
            print(err)
        finally:
            cur.close()

    def productNonExistent(self,args):
        cur = None
        try:
            cur = self.connection.cursor()
            query = "SELECT * FROM products where product_name=%s"
            cur.execute(query, args)
            data = cur.fetchone()
            if data is None:
                return True
            else:
                return False
        except Exception as err:
            print(err)
        finally:
            cur.close()

    def doesOrderExists(self,id):
        cur = None
        try:
            cur = self.connection.cursor()
            query = "SELECT * FROM orders where order_id=%s"
            cur.execute(query, id)
            data = cur.fetchone()
            if data is None:
                return False
            else:
                return True
        except Exception as err:
            print(err)
        finally:
            cur.close()

    def doesProductExists(self,id):
        cur = None
        try:
            cur = self.connection.cursor()
            query = "SELECT * FROM products where product_id=%s"
            cur.execute(query, id)
            data = cur.fetchone()
            if data is None:
                return False
            else:
                return True
        except Exception as err:
            print(err)
        finally:
            cur.close()

    def doesOrderProductExists(self,orderID,productID):
        cur = None
        try:
            cur = self.connection.cursor()
            query = "SELECT * FROM order_product where order_id=%s and product_id=%s"
            args=(orderID,productID)
            cur.execute(query, args)
            data = cur.fetchone()
            if data is None:
                return False
            else:
                return True
        except Exception as err:
            print(err)
        finally:
            cur.close()

    def doesPaymentExists(self,id):
        cur = None
        try:
            cur = self.connection.cursor()
            query = "SELECT * FROM payment where payment_id=%s"
            cur.execute(query, id)
            data = cur.fetchone()
            if data is None:
                return False
            else:
                return True
        except Exception as err:
            print(err)
        finally:
            cur.close()


    #======================================MAIN FUNCTIONS====================================
    def logIn(self,args):
        cur = None
        try:
            cur = self.connection.cursor()

            query = "select * from users where user_name=%s and user_pwd=%s"
            cur.execute(query, args)
            data= cur.fetchone()
            return data

        except Exception as err:
            print(err)
        finally:
            cur.close()

    def signUP(self, args):
        cur = None
        try:
            cur = self.connection.cursor()
            isOccupied = self.usernameOccupied(args[0])
            if isOccupied == True:
                print("Username is already in use")
                cur.close()
                return False

            query= "INSERT INTO users(user_name,user_email,user_pwd,contact, address) VALUES(%s,%s,%s,%s,%s)"
            cur.execute(query, args)
            self.connection.commit()
            print("User Added")
        except Exception as err:
            print(err)
        finally:
            cur.close()
            return True

    def deleteUser(self,args):
        cur = None
        try:
            cur = self.connection.cursor()
            nonExistence = self.nonExistent(args)
            if nonExistence == True:
                print("User you are trying to delete doesn't exist")
                cur.close()
                return False

            query1= "SELECT user_id FROM users where user_name=%s and user_pwd=%s"
            cur.execute(query1,args)
            id= cur.fetchone()

            query2 = "DELETE FROM users where user_id=%s"
            cur.execute(query2,id)

            self.connection.commit()
            print("User Deleted")
        except Exception as err:
            print(err)
        finally:
            cur.close()
            return True

    def addProduct(self,args):
        cur = None
        isAlreadyAdded = self.productAlreadyAdded(args[0])
        if isAlreadyAdded == True:
            print("Product is already added with this name")
            return False

        try:
            cur = self.connection.cursor()
            query = "INSERT INTO products(product_name,product_details,price,category_type) VALUES(%s,%s,%s,%s)"
            cur.execute(query, args)
            self.connection.commit()
            print("Product Added")
        except Exception as err:
            print(err)
        finally:
            cur.close()
            return True

    def deleteProduct(self,args):
        cur = None
        try:
            cur = self.connection.cursor()
            nonExistence = self.productNonExistent(args)
            if nonExistence == True:
                print("Product you are trying to delete doesn't exist")
                cur.close()
                return False

            query1 = "SELECT product_id FROM products where product_name=%s"
            cur.execute(query1, args)
            id = cur.fetchone()

            query2 = "DELETE FROM products where product_id=%s"
            cur.execute(query2, id)

            self.connection.commit()
            print("Product Deleted")
        except Exception as err:
            print(err)
        finally:
            cur.close()
            return True

    def addOrder(self,args):
        cur = None
        try:
            cur = self.connection.cursor()
            query = "INSERT INTO orders(user_id,date,order_status) VALUES(%s,%s,%s)"
            cur.execute(query, args)
            self.connection.commit()
            print("Order Added")
        except Exception as err:
            print(err)
        finally:
            cur.close()

    def deleteOrder(self,args):
        cur = None
        try:
            cur = self.connection.cursor()
            existence = self.doesOrderExists(args[0])
            if existence == False:
                print("Order you are trying to delete doesn't exist")
                cur.close()
                return False

            query2 = "DELETE FROM orders where order_id=%s"
            cur.execute(query2, args)

            self.connection.commit()
            print("Order Deleted")
        except Exception as err:
            print(err)
        finally:
            cur.close()
            return True

    def updateOrderStatus(self,args):
        cur = None
        try:
            cur = self.connection.cursor()
            existence = self.doesOrderExists(args[0])
            if existence == False:
                print("Order you are trying to update doesn't exist")
                cur.close()
                return False

            query2 = "UPDATE orders SET order_status=%s where order_id=%s"
            arguments=(args[1],args[0])
            cur.execute(query2, arguments)

            self.connection.commit()
            print("Order status updated")
        except Exception as err:
            print(err)
        finally:
            cur.close()
            return True

    def addOrderProduct(self,args):
        cur = None
        try:
            cur = self.connection.cursor()
            existence = self.doesOrderExists(args[0])
            if existence == False:
                print("OrderID you are trying to add doesn't exist")
                cur.close()
                return False

            existence1 = self.doesProductExists(args[1])
            if existence1 == False:
                print("ProductID you are trying to add doesn't exist")
                cur.close()
                return False

            existence2 = self.doesOrderProductExists(args[0],args[1])
            if existence2 == True:
                print("Entry you are trying to add with given productId and orderID already exists")
                cur.close()
                return False

            query2 = "INSERT INTO order_product(order_id,product_id,quantity) VALUES(%s, %s, %s)"
            cur.execute(query2, args)

            self.connection.commit()
            print("OrderProduct Added")
        except Exception as err:
            print(err)
        finally:
            cur.close()
            return True

    def deleteOrderProduct(self,args):
        cur = None
        try:
            cur = self.connection.cursor()
            existence = self.doesOrderProductExists(args[0],args[1])
            if existence is False:
                print("Entry you are trying to delete with given product and order ID doesn't exist")
                cur.close()
                return False

            query="DELETE FROM order_product WHERE order_id=%s and product_id=%s"
            cur.execute(query,args)
            self.connection.commit()
            print("Order_Product Deleted")
        except Exception as err:
            print(err)
        finally:
            cur.close()

    def addPayment(self,args):
        cur = None
        try:
            cur = self.connection.cursor()
            existence = self.doesOrderExists(args[0])
            if existence == False:
                print("OrderID you are trying to add doesn't exist")
                cur.close()
                return False

            query2 = "INSERT INTO payment(order_id,date,amount,payment_method) VALUES(%s, %s, %s, %s)"
            cur.execute(query2, args)

            self.connection.commit()
            print("Payment Added")
        except Exception as err:
            print(err)
        finally:
            cur.close()
            return True

    def deletePayment(self,id):
        cur = None
        try:
            cur = self.connection.cursor()
            existence = self.doesPaymentExists(id)
            if existence == False:
                print("Payment you are trying to delete doesn't exist")
                cur.close()
                return False

            query2 = "DELETE FROM payment where payment_id=%s"
            cur.execute(query2, id)

            self.connection.commit()
            print("payment Deleted")
        except Exception as err:
            print(err)
        finally:
            cur.close()
            return True

    def updateProfile(self,args):
        cur = None
        try:
            cur = self.connection.cursor()
            query = "UPDATE users SET user_name=%s,user_email=%s,contact=%s,address=%s where user_id=%s"
            cur.execute(query,args)
            self.connection.commit()
        except Exception as err:
            print(err)
        finally:
            cur.close()

    def addChef(self,args):
        cur=None
        try:
            cur = self.connection.cursor()
            query = "INSERT into chefs(chef_name,chef_rank) values(%s,%s)"
            cur.execute(query,args)
            self.connection.commit()
        except Exception as err:
            print(err)
        finally:
            cur.close()

    def getAllProducts(self):
        cur = None
        data = None
        try:
            cur = self.connection.cursor()
            query = "select * from Products"
            cur.execute(query)
            data = cur.fetchall()
        except Exception as err:
            print(err)
        finally:
            cur.close()
            return data

    def getProductsFromCertainType(self,type):
        cur = None
        data=None
        try:
            cur = self.connection.cursor()
            query = "select * from Products where category_type=%s or category_type='appetizer' or category_type='dessert'"
            cur.execute(query, type)
            data = cur.fetchall()
        except Exception as err:
            print(err)
        finally:
            cur.close()
            return data

    def getProduct(self,type):
        cur = None
        try:
            cur = self.connection.cursor()
            query="select * from Products where category_type=%s"
            cur.execute(query,type)
            data = cur.fetchall()
        except Exception as err:
            print(err)
        finally:
            cur.close()
            return data

    def getProductByName(self,name):
        cur = None
        data= None
        try:
            cur = self.connection.cursor()
            query = "select * from Products where product_name=%s"
            cur.execute(query, name)
            data = cur.fetchone()
        except Exception as err:
            print(err)
        finally:
            cur.close()
            return data

    def getProductIDByName(self,name):
        cur = None
        data= None
        try:
            cur = self.connection.cursor()
            query = "select product_id from Products where product_name=%s"
            cur.execute(query, name)
            data = cur.fetchone()
        except Exception as err:
            print(err)
        finally:
            cur.close()
            return data

    def getUserInfo(self,name):
        cur=None
        data = None
        try:
            cur= self.connection.cursor()
            query="select * from Users where user_name=%s"
            cur.execute(query,name)
            data=cur.fetchone()
        except Exception as err:
            print(err)
        finally:
            cur.close()
            return data

    def getUserId(self,name):
        cur = None
        data=None
        try:
            cur = self.connection.cursor()
            query = "select user_id from Users where user_name=%s"
            cur.execute(query, name)
            data = cur.fetchone()
        except Exception as err:
            print(err)
        finally:
            cur.close()
            return data

    def getLastAddedOrderID(self):
        cur = None
        data = None
        try:
            cur = self.connection.cursor()
            query = "select LAST_INSERT_ID() from orders";
            cur.execute(query)
            data = cur.fetchone()
        except Exception as err:
            print(err)
        finally:
            cur.close()
            return data

    def getUserPasswordByName(self,name):
        cur = None
        data = None
        try:
            cur = self.connection.cursor()
            query = "select user_pwd from Users where user_name=%s"
            cur.execute(query, name)
            data = cur.fetchone()
        except Exception as err:
            print(err)
        finally:
            cur.close()
            return data

    def changeUserPassword(self,name,pwd):
        cur = None
        data = None
        try:
            cur = self.connection.cursor()
            query = "UPDATE users set user_pwd=%s where user_name=%s"
            args=(pwd,name)
            cur.execute(query, args)
            self.connection.commit()
        except Exception as err:
            print(err)
        finally:
            cur.close()

    def getOrderIDForAUser(self,userID):
        cur = None
        data = None
        try:
            cur = self.connection.cursor()
            query = "select order_id from orders where user_id=%s"
            cur.execute(query, userID)
            data = cur.fetchall()
        except Exception as err:
            print(err)
        finally:
            cur.close()
            return data

    def getPaymentInfoByOrderID(self,orderID):
        cur = None
        data = None
        try:
            cur = self.connection.cursor()
            if self.doesOrderExists(orderID) == True:
                query = "select * from payment where order_id=%s"
                cur.execute(query, orderID)
                data = cur.fetchone()
            else:
                print("Payment with this orderID doesn't exist")
        except Exception as err:
            print(err)
        finally:
            cur.close()
            return data
    def getOrderStatusByOrderId(self,orderID):
        cur = None
        data = None
        try:
            cur = self.connection.cursor()
            if self.doesOrderExists(orderID) == True:
                query = "select order_status from orders where order_id=%s"
                cur.execute(query, orderID)
                data = cur.fetchone()
            else:
                print("Payment with this orderID doesn't exist")
        except Exception as err:
            print(err)
        finally:
            cur.close()
            return data
    def getChefs(self):
        cur = None
        data = None
        try:
            cur = self.connection.cursor()
            query = "select * from chefs"
            cur.execute(query)
            data = cur.fetchall()
        except Exception as err:
            print(err)
        finally:
            cur.close()
            return data
#handler= DBHandler("localhost","root","sony10","foodorderonline")
#args=("abcd","abcd")
#handler.deleteUser(args)
#args=("abcd","abcd@gmail.com","abcd","1234","1234 st. 1234")
#handler.signUP(args)
#args=("TIRAMISU","Creamy Mascarpone, Espresso-soaked Ladyfingers and Cacao powder","9","dessert")
#handler.addProduct(args)
#args=("abcD")
#handler.deleteProduct(args)

#dateNow= datetime.datetime.now()
#args=("1",dateNow,"pending")
#handler.addOrder(args)

#handler.deleteOrder("1")

#args=("1","completed")
#handler.updateOrderStatus(args)

#args=("2","1","5")
#handler.addOrderProduct(args)


#args=("2","1")
#handler.deleteOrderProduct(args)

#dateNow= datetime.datetime.now()
#args=("2",dateNow,"2500","cash")
#handler.addPayment(args)

#handler.deletePayment("1")

#handler= DBHandler("localhost","root","sony10","foodorderonline")
#print(handler.getProduct("appetizer"))
# handler= DBHandler("localhost","root","sony10","foodorderonline")
# arg=("Anthony Bourdain","Executive Chef")
# handler.addChef(arg)
# handler= DBHandler("localhost","root","sony10","foodorderonline")
# data= handler.getProductsFromCertainType("lunch")
# print(data)

