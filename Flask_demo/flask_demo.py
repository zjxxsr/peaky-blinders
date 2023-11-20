from flask import Flask
from flask import request
from flask import jsonify

app=Flask(__name__)

@app.route("/zjx",methods=["POST"])
def answer():
    flask_dict=request.get_json(force=True)
    print(flask_dict)
    print(type(flask_dict))
    flask_list=[]
    for i in flask_dict:
        flask_list.extend(i)
        print(i)
        print("3")
        print(flask_list)

        return flask_list

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000)