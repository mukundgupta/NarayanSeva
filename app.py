from flask import Flask, render_template, request
import main
import addAcceptorData
import addDonorData
import csv

app = Flask(__name__)

@app.route('/')
def home():
    
    return render_template("index.html")

@app.route('/page')
def map_page():
    c,directions,names,allocations = main.main()
    
    return render_template("page.html",solution=c,directions=directions,names=names,allocations=allocations)

@app.route('/volunteer_form')
def volunteer_form():
    
    return render_template('volunteer_form.html')


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
@app.route('/submit-a',  methods=['POST', 'GET'])
def submit_a():
    # getting details from html form
    if request.method == 'POST':
        name = request.form.get("d_name")
        email = request.form.get("email")
        num = request.form.get("number")
        address = request.form.get("Address")
        req = request.form.get("req")
        addAcceptorData.add_acceptor_data([name, num, email,address,req])
        print("added")
    return render_template('submit-a.html')



@app.route('/food_form')
def food_form():
    donors = []
    with open('static/donorData.csv',"r") as file:
        reader = csv.reader(file)
        next(reader)
        try:
            for row in reader:
                donors.append(row[1])
        except:
            pass

    
    return render_template('food_form.html',donors=donors)




if __name__ == '__main__':
    app.run(debug=True)

