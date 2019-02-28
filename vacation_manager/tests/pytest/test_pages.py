def test_login_page(client):
        response = client.get("/login")
        assert response.status_code == 200

def test_admin_page(client):
        response = client.get("/admin/")
        assert response.status_code == 403