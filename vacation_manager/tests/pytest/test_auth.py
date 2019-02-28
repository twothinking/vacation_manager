def login(client, email, password):
    return client.post('/login', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)

def logout(client):
    return client.get('/logout', follow_redirects=True)

def test_create_admin_user_and_login_then_logout(client, admin_user):
    rv = login(client, admin_user.email, admin_user.password)
    assert b'fullcalendar' in rv.data

    rv = client.get('/admin/')
    assert rv.status_code == 200

    rv = logout(client)
    assert b'fullcalendar' not in rv.data

def test_create_simple_user_and_login_then_logout(client, simple_user):
    rv = login(client, simple_user.email, simple_user.password)
    assert b'fullcalendar' in rv.data

    rv = client.get('/admin/')
    assert rv.status_code == 403

    rv = logout(client)
    assert b'fullcalendar' not in rv.data