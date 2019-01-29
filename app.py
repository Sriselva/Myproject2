from flask import Flask,request,make_response
app = Flask(__name__)

@app.route('/set')
def setcookie():
    response=make_response("i have created cookies")
    response.set_cookie("mynewcookie","selvakumar")
    return response

@app.route('/getting')
def getcookie():
    cookiess=request.cookies.get("mynewcookie")
    return "my new cookie is"+cookiess+"is created"



if __name__ == '__main__':
   app.run(debug = True)