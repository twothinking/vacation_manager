from vacation_manager.models import User
 

def test_admin_user(admin_user):

    user = User(email='admin_user@gmail.com', password='admin_pass')
    assert admin_user.email == user.email
    assert admin_user.password == user.password