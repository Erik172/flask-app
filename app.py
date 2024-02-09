from api import app as api_app

if __name__ == '__main__':
    api_app.run(debug=True, host='localhost', port=5000)