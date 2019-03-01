import json

def login(client, email, password):
    return client.post('/login', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)


def test_set_get_date_ajax(client, simple_user):
    client.post('/logout')
    rv = login(client, simple_user.email, simple_user.password)

    # Test date insertation
    data = dict(date='2019-03-01',operation='insert')
    client.post('/set_date_ajax', data=json.dumps(data),content_type='application/json')
    dates = client.post('/get_date_ajax')
    assert json.loads(dates.data)[-1]['avaliable_day'] == data['date'] + "T00:00:00+00:00"

    # Test date deletation
    data['operation'] = 'delete'
    client.post('/set_date_ajax', data=json.dumps(data),content_type='application/json')
    dates = client.post('/get_date_ajax')
    assert json.loads(dates.data)[-1]['avaliable_day'] != data['date'] + "T00:00:00+00:00"

# def test_set_get_date_vacation_ajax(client, simple_user):

#     rv = login(client, simple_user.email, simple_user.password)
#     # Test date insertation
#     data = dict(date='2019-03-01',operation='insert')
#     client.post('/set_date_ajax', data=json.dumps(data),content_type='application/json')
#     dates = client.post('/get_date_ajax')
#     assert json.loads(dates.data)[-1]['avaliable_day'] == data['date'] + "T00:00:00+00:00"

#     # Test date deletation
#     data['operation'] = 'delete'
#     client.post('/set_date_ajax', data=json.dumps(data),content_type='application/json')
#     dates = client.post('/get_date_ajax')
#     assert json.loads(dates.data)[-1]['avaliable_day'] != data['date'] + "T00:00:00+00:00"