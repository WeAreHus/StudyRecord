#coding:utf8
from models import Users
from werkzeug.security import check_password_hash

def validate(username, password1, password2=None):
    user = Users.query.filter(Users.username == username).first()
    if password2:
        if user:
            return 'username already exists'
        else:
            if len(username) < 4:
                return 'Username length is at least 4 characters'
            elif password1 != password2:
                return 'Two passwords are inconsistent'
            elif len(password1) < 6:
                return 'Password length at least 6 characters'
            else:
                return 'register successful'
    else:
        if user:
            if check_password_hash(user.password, password1):
                return 'login successful'
            else:
                return 'wrong password'
        else:
            return 'Username does not exist'

def validate_func(user, o_password, password1, password2):
    if user:
        if check_password_hash(user.password, o_password):
            if password1 != password2:
                return 'new passwords are different'
            elif len(password1) < 6:
                return 'new passwords length at least 6 characters'
            else:
                return 'change successful'
        else:
            return 'wrong password'

#控制上传文件的格式
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ['jpg', 'jpeg', 'png', 'gif']