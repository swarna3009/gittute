from flask import Flask,request,render_template,jsonify
from datetime import datetime
from dotenv import load_dotenv
import os
import pymongo
import json

load_dotenv()
MONGO_URI =os.getenv('MONGO_URI')
client = pymongo.MongoClient(MONGO_URI)

db = client.dummy

collection = db['dummy-collection']
todo = db['todo_items']
app= Flask(__name__)
@app.route("/")
def home():
    return render_template('todo.html')

@app.route('/api')
def name():
    with open("data.json","r") as file:
        data=json.load(file)
    return jsonify(data)
@app.route('/submit',methods=['POST'])
def submit():
    form_data = dict(request.form)
    collection.insert_one(form_data)
    
    print(form_data)
    return 'Data submitted sucessfuly'


@app.route('/submittodoitem',methods=["POST"])
def submit_todo_item():
    item_name=request.form.get("itemName")
    item_desc=request.form.get("itemDesc")
    if not item_name or item_desc:
        return jsonify({'error':'item name and description required'})
    todo_item={
        'itemName':item_name,
        'itemDesc':item_desc
    }
    todo.insert_one(todo_item)
    return jsonify({'message':'item added sucessfully'})
    


    
if __name__ == "__main__":
    app.run(debug=True)
    
    
    