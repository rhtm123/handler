from main import app, socketio

if __name__ == "__main__":
    # app.run(host='0.0.0.0')
	socketio.run(app,host='0.0.0.0',port=5000)
