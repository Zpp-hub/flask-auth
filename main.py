from flask import Flask
import router

app = Flask(__name__)
router.register(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(3060), threaded=False, debug=True)
