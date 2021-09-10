from werkzeug.wrappers import response
from app import app
from flask import make_response
app.config['JSON_AS_ASCII'] = False

def test_home():
    print("client test")
    client = app.test_client()
    response = client.get('/')
    
    assert response.status_code == 200 # 성공
    # assert '{"text":"굿모닝"}' in str(response.data)
    
    print(str(response.data))
  
if __name__ == '__main__':
    test_home()