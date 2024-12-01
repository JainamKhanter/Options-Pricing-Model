from flask import Flask, render_template
import random

app = Flask(__name__)

@app.route('/')
def index():
    print(random.randint(0,5))
    return render_template('topsj.html')


if __name__ == '__main__':
    app.run(debug=True)