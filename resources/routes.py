import requests
from .resources import  UpdateUserInfo,ChangePassword,UpdatePassword

def initialize_routes(api):
     api.add_resource(UpdateUserInfo, '/api/updateuserinfo')
     api.add_resource(ChangePassword, '/api/changepassword')
     api.add_resource(UpdatePassword, '/api/updatePassword/<string:newPassword>')
