from flask import Flask
app = Flask(__name__)
# define a starting point or "root"
@app.route('/')

def hello_world():

    return 'Hello world'

@app.route('/test')

def hello():

    return 'hello'
    
