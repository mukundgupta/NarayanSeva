from flask import Flask, render_template, request
import main
import addDonorData

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
@app.route('/submit',  methods=['POST', 'GET'])
def submit():
    # getting details from html form
    if request.method == 'POST':
        name = request.form.get("d_name")
        email = request.form.get("email")
        num = request.form.get("number")
        address = request.form.get("Address")
        addDonorData.add_donor_data([name, num, email,address])
        print("added")
    return render_template('submit.html')
@app.route('/acceptor_form')
def acceptor_form():
    return render_template('acceptor_form.html')
if __name__ == '__main__':
    app.run(debug=True)

