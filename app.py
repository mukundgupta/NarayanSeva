from flask import Flask, render_template
import main

app = Flask(__name__)

@app.route('/')
def home():
    
    return render_template("index.html")

@app.route('/page')
def map_page():
    c,directions = main.main()
    return render_template("page.html",solution=c,directions=directions)

@app.route('/donor_form')
def donor_form():
    return render_template('donor_form.html')


if __name__ == '__main__':
    app.run(debug=True)

