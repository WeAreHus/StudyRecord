#coding:utf8
from models import Users
from werkzeug.security import check_password_hash

# 登录与注册的判断条件，返回提示
def validate(username, password1, password2=None):
    user = Users.query.filter(Users.username == username).first()
    # 当有password2对应的实参传入时,表明是注册操作
    if password2:
        if user:
            return 'username already exists'
        else:
            # 用户名长度不能小于4
            if len(username) < 4:
                return 'Username length is at least 4 characters'
            # 两次输入的密码要相等
            elif password1 != password2:
                return 'Two passwords are inconsistent'
            # 密码的长度不能小于6
            elif len(password1) < 6:
                return 'Password length at least 6 characters'
            else:
                return 'register successful'
    else:
        if user:
            # 使用check_password_hash()方法判断登录时的密码是否与数据库保存的hash加密后的密码匹配
            if check_password_hash(user.password, password1):
                return 'login successful'
            else:
                return 'wrong password'
        else:
            return 'Username does not exist'

# 更改密码时的判断条件
def validate_func(user, o_password, password1, password2):
    if user:
        if check_password_hash(user.password, o_password):
            if password1 != password2:
                return 'new passwords are not the same'
            elif len(password1) < 6:
                return 'new passwords length at least 6 characters'
            else:
                return 'change successful'
        else:
            return 'wrong password'

#控制上传文件的格式,仅可使用jpg,jpeg,png,gif文件
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ['jpg', 'jpeg', 'png', 'gif']