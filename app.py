from flask import Flask, abort, send_from_directory, redirect
import os

app = Flask(__name__)

STORAGE_PATH = 'files'

@app.route("/")
def index():
    return 'helo welcpome to put.nu'
    
@app.route("/<path>")
def fetch(path):
    if not os.path.isfile(os.path.join(STORAGE_PATH, path)):
        return resolve_link(path) #if not a file, try to resolve as shortened link

    return send_from_directory(STORAGE_PATH, path) 

def resolve_link(url): # link shortening
    shortened = {'zucc': 'https://facebook.com'} #use a real db for this
    if url in shortened:
        return redirect(shortened[url])
    abort(404)
        
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000)
