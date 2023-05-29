from flask import Flask,render_template,request,redirect,session,jsonify,url_for
from flask_restful import Api,Resource
from resources import routes
from DBHandler import DBHandler
import re,random,json,datetime,ast

app = Flask(__name__)
TEMPLATES_AUTO_RELOAD = True
app.secret_key = "secretkey"
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
cartData=[]
api=Api(app)
routes.initialize_routes(api)
jsdata = None

def getCategoryTypeByTime():
    now = datetime.datetime.now()
    today7am = now.replace(hour=7,minute=0,second=0,microsecond=0)
    today12pm = now.replace(hour=12,minute=0,second=0,microsecond=0)
    today5pm = now.replace(hour=17, minute=0,second=0,microsecond=0)
    if now>today7am and now<today12pm:
        return "breakfast"
    elif now>today12pm and now<today5pm:
        return "lunch"
    else:
        return "dinner"

def validateSingUp(name,email,pwd,contact,address):
    if name=="":
        error = "One or more fields are empty"
        return error
    if name.strip() == "" or pwd=="" or contact=="" or address=="":
        error="One or more fields are empty"
        return error
    if (re.fullmatch(regex,email)) is None:
        error="Invalid Email"
        return error
    if " " in pwd:
        error = "Password can't contain whitespaces"
        return error
    if len(pwd)<8:
        error = "Length of password can't be less than 8"
        return error
    handler= DBHandler("localhost","root","sony10","foodorderonline")
    if handler.usernameOccupied(name) == True:
        error = "Username already taken, choose another username"
        return error
    if handler.userEmailOccupied(email) == True:
        error = "This Email is already in use by another user"
        return error

    return None

def getRandomProducts():
    handler = DBHandler("localhost", "root", "sony10", "foodorderonline")
    data = []

    while len(data) < 5:
        category = getCategoryTypeByTime()
        allDishes = handler.getProductsFromCertainType(category)
        temp = random.choice(allDishes)

        existCount = 0
        count = 0
        if len(data) >= 1:
            for i in data:
                if temp[0] == i[0]:
                    existCount = existCount + 1

        if existCount == 0:
            data.append(temp)

    return data


def evaluateOrder(jsdata):

    handler = DBHandler("localhost", "root", "sony10", "foodorderonline")
    count = jsdata["totalElements"]

    amount = jsdata["totalAmount"]
    if int(amount)>0:
        userid = handler.getUserId(session["nm"])
        date = datetime.datetime.now()
        orderStatus = "pending"
        args0 = (userid, date, orderStatus)
        try:
            handler.addOrder(args0)
        except Exception as err:
            print(err)


        orderId = handler.getLastAddedOrderID()
        args1 = (orderId, date, amount, jsdata["paymentMethod"])

        try:
            handler.addPayment(args1)
        except Exception as err:
            print(err)

        for i in range(0, count):
            name = jsdata["name" + str(i)]
            productID = handler.getProductIDByName(name)
            quantity = jsdata["quantity" + str(i)]
            args2 = (orderId, productID, quantity)
            try:
                handler.addOrderProduct(args2)
            except Exception as err:
                print(err)
@app.route('/')
def onStart():  # put application's code here
    return render_template("login.html")

@app.route('/dologin' , methods=["GET","POST"])
def dologin():
    if session.get("nm") and session.get("pwd"):
        data = getRandomProducts()
        return render_template("home.html", data=data)

    if request.method == "POST":
        pwd = request.form["pwd"]
        nm = request.form["fname"]
    elif request.method == "GET":
        pwd = request.args.get("pwd")
        nm = request.args.get("fname")


    if nm is None or pwd is None:
        return render_template("login.html", error="One or more fields are empty")
    if nm.strip() == "":
        return render_template("login.html", error= "One or more fields are empty")
    session["nm"] = nm
    session["pwd"] = pwd

    handler = DBHandler("localhost","root", "sony10", "foodorderonline")
    args=(nm,pwd)
    data = handler.logIn(args)
    if data is None:
        return render_template("login.html",error="Invalid credentials")
    else:
        data= getRandomProducts()
        return render_template("home.html",data=data)

@app.route('/logout', methods=["GET","POST"])
def logout():
    if session.get("nm") and session.get("pwd"):
        session.pop("nm")
        session.pop("pwd")
    return redirect("/")
@app.route('/signup' , methods=["GET","POST"])
def showSignUp():
    return render_template("signUp.html")


@app.route('/dosignup' , methods=["GET","POST"])
def doSignUp():
    if request.method == "POST":
        pwd = request.form["pwd"]
        nm = request.form["fname"]
        email = request.form["email"]
        contact = request.form["contact"]
        address = request.form["address"]

    else:
        pwd = request.args.get("pwd")
        nm = request.args.get("fname")
        email = request.args.get("email")
        contact = request.args.get("contact")
        address = request.args.get("address")

    err = validateSingUp(nm,email,pwd,contact,address)
    if err is not None:
        return render_template("signUp.html",error=err)

    handler = DBHandler("localhost","root", "sony10", "foodorderonline")
    args=(nm,email,pwd,contact,address)
    check = handler.signUP(args)
    if check == True:
        session["nm"]=nm
        session["pwd"]= pwd
        data= getRandomProducts()
        #return render_template("home.html",data=data)
        return redirect("/dologin")
    else:
        return render_template("signUp.html", error= "An Unexpected error occured")

# @app.route('/showhome',methods=["GET","POST"])
# def showHome():
#     return render_template("home.html")

@app.route('/showabout',methods=["GET","POST"])
def showAbout():
    return render_template("about.html")

@app.route('/showappetizers' , methods= ["GET","POST"])
def showAppetizers():
    if session.get("nm") and session.get("pwd"):
        handler= DBHandler("localhost","root","sony10","foodorderonline")
        data = handler.getProduct('appetizer')
        return render_template("appetizers.html",data=data, count=len(data))
    else:
        return render_template("login.html", error="One or more fields are empty")

@app.route('/showbreakfast', methods=["GET","POST"])
def showBreakfast():
    if session.get("nm") and session.get("pwd"):
        if getCategoryTypeByTime()== 'breakfast':
            handler = DBHandler("localhost", "root", "sony10", "foodorderonline")
            data = handler.getProduct('breakfast')
            return render_template("breakfast.html",data=data, count=len(data))
        else:
            return render_template('our-special-dishes.html',message="Wait for breakfast time")
    else:
        return render_template("login.html", error="One or more fields are empty")

@app.route('/showlunch', methods=["GET","POST"])
def showLunch():
    if session.get("nm") and session.get("pwd"):
        if getCategoryTypeByTime() == 'lunch':
            handler = DBHandler("localhost", "root", "sony10", "foodorderonline")
            data = handler.getProduct('lunch')
            return render_template("lunch.html",data=data, count=len(data))
        else:
            return render_template('our-special-dishes.html',message="Wait for lunch time")
    else:
        return render_template("login.html", error="One or more fields are empty")

@app.route('/showdinner', methods=["GET","POST"])
def showDinner():
    if session.get("nm") and session.get("pwd"):
        if getCategoryTypeByTime() == 'dinner':
            handler = DBHandler("localhost", "root", "sony10", "foodorderonline")
            data = handler.getProduct('dinner')
            print(data)
            return render_template("dinner.html", data=data, count=len(data))
        else:
            return render_template('our-special-dishes.html', message="Wait for dinner time")
    else:
        return render_template("login.html", error="One or more fields are empty")

@app.route('/showdesserts', methods=["GET","POST"])
def showDesserts():
    if session.get("nm") and session.get("pwd"):
        handler = DBHandler("localhost", "root", "sony10", "foodorderonline")
        data = handler.getProduct('dessert')
        return render_template("desserts.html",data=data, count=len(data))
    else:
        return render_template("login.html", error="One or more fields are empty")

@app.route('/addtocart', methods=["GET","POST"])
def addToCart():
    if session.get("nm") and session.get("pwd"):
        handler=DBHandler("localhost","root","sony10","foodorderonline")
        jsdata= request.form.get('javascript_data')
        data= handler.getProductByName(jsdata)
        flag = False
        count= len(cartData)
        for i in range(0, count):
            if data[0] == cartData[i][0]:
                flag = True

        if flag==True:
            return redirect(request.referrer)

        cartData.append(data)
        print(cartData)
        return redirect(request.referrer)
    else:
        return render_template("login.html", error="One or more fields are empty")

@app.route('/showcart',methods=["GET","POST"])
def showCart():
    #data= json.dumps(cartData)
    #print(data)
    if session.get("nm") and session.get("pwd"):
        count= len(cartData)
        return render_template("orderConfirmation.html",data=cartData,count=count)
    else:
        return render_template("login.html", error="One or more fields are empty")


@app.route('/paymentmethod',methods=["GET","POST"])
def paymentMethod():
    if session.get("nm") and session.get("pwd"):
        data = request.form.get('javascript_data')
        jsdata = json.loads(data)
        print(jsdata)
        print(type(jsdata))
        if jsdata["paymentMethod"] == "card":
            return jsonify({'redirect': url_for("showCardPage", data=jsdata)})
        else:
            if jsdata is not None:
                 evaluateOrder(jsdata)
            return jsonify({'redirect': url_for("ordersuccessful")})
    else:
        return render_template("login.html", error="One or more fields are empty")


@app.route('/showCardPage/<data>',methods=["GET","POST"])
def showCardPage(data):
    if session.get("nm") and session.get("pwd"):
        return render_template("cardPayment.html",data=data)
    else:
        return render_template("login.html", error="One or more fields are empty")

@app.route('/addorderviacard', methods=["GET","POST"])
def addOrderViaCard():
    if session.get("nm") and session.get("pwd"):
        data = request.form.get('javascript_data')
        print(data)
        jsdata = json.loads(data)
        print(jsdata)
        print(type(jsdata))

        if jsdata is not None:
            evaluateOrder(jsdata)
        return jsonify({'redirect': url_for("ordersuccessful")})
    else:
        return render_template("login.html", error="One or more fields are empty")

@app.route('/ordersuccessful', methods=["GET","POST"])
def ordersuccessful():
    cartData.clear()
    return render_template("orderSuccessful.html")

@app.route('/showupdateprofile', methods=["GET","POST"])
def showupdateProfile():
    if session.get("nm") and session.get("pwd"):
        handler = DBHandler("localhost", "root", "sony10", "foodorderonline")
        userInfo = handler.getUserInfo(session["nm"])
        print(userInfo)
        return render_template("updateProfile.html",data=userInfo)
    else:
        return render_template("login.html", error="One or more fields are empty")

@app.route('/showchangepassword', methods=["GET","POST"])
def showchangePassword():
    if session.get("nm") and session.get("pwd"):
        handler=DBHandler("localhost","root","sony10","foodorderonline")
        password =handler.getUserPasswordByName(session["nm"])
        return render_template("changePassword.html",password=password)
    else:
        return render_template("login.html", error="One or more fields are empty")

@app.route('/showteam')
def showTeam():
    if session.get("nm") and session.get("pwd"):
        handler= DBHandler("localhost","root","sony10","foodorderonline")
        data =handler.getChefs()
        print(data)
        return render_template("team.html",data=data, count= len(data))
    else:
        return render_template("login.html", error="One or more fields are empty")

@app.route('/showorderhistory')
def showOrderHistory():
    if session.get("nm") and session.get("pwd"):
        handler = DBHandler("localhost", "root", "sony10", "foodorderonline")
        paymentInfo=[]
        selectedDataPending=[]
        selectedDataCompleted=[]
        orderIDs= None
        if session["nm"]:
            userID = handler.getUserId(session["nm"])
            if userID:
                orderIDs = handler.getOrderIDForAUser(userID)
                for i in orderIDs:
                    data= handler.getPaymentInfoByOrderID(i)
                    paymentInfo.append(data)
            else:
                print("User id doesn't exist")

        for i in range(0,len(paymentInfo)):
            tempData=[]
            tempData.append(paymentInfo[i][3])
            tempData.append(paymentInfo[i][2])
            tempData.append(paymentInfo[i][1])
            orderStatus = handler.getOrderStatusByOrderId(paymentInfo[i][3])
            if orderStatus[0] == "completed":
                selectedDataCompleted.append(tempData)
            elif orderStatus[0] == "pending":
                selectedDataPending.append(tempData)

        print(selectedDataPending)
        print(selectedDataCompleted)
        pendingCount= len(selectedDataPending)
        completedCount= len(selectedDataCompleted)

        return render_template("orderHistory.html", dataPending=selectedDataPending,dataCompleted=selectedDataCompleted,pendingCount=pendingCount,completedCount=completedCount)
    else:
        return render_template("login.html", error="One or more fields are empty")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

#{"paymentMethod":"cash on delivery"}
