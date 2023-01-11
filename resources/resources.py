from flask import request, Response, jsonify,session
from flask_restful import Resource
from DBHandler import DBHandler

class UpdateUserInfo(Resource):
    def get(self):
        pass

    def post(self):
        data=request.get_json()
        print(data)
        name= data["name"]
        email = data["email"]
        contact = data["contact"]
        address = data["address"]
        handler= DBHandler("localhost","root","sony10","foodorderonline")
        userID= handler.getUserId(session["nm"])
        args = (name, email, contact, address,userID)
        try:
            handler.updateProfile(args)
        except Exception as err:
            print(err)

class ChangePassword(Resource):
    def get(self):
        handler=DBHandler("localhost","root","sony10","foodorderonline")
        password = handler.getUserPasswordByName(session["nm"])
        print(password[0])
        return password[0]


class UpdatePassword(Resource):
    def post(self,newPassword):
        print(newPassword)
        handler = DBHandler("localhost", "root", "sony10", "foodorderonline")
        handler.changeUserPassword(session["nm"],newPassword)

