from flask import Flask, render_template, request
import requests

app = Flask("DecideApp")

@app.route("/")
def Homepage():
    return render_template("Home.html")

@app.route('/Decide', methods=['GET', 'POST'])
def Decide():
    if request.method == 'POST':
        return redirect(url_for('Homepage'))
    return render_template('Decide.html')

@app.route('/Home', methods=['GET', 'POST'])
def Home():
    if request.method == 'POST':
        return redirect(url_for('Decide'))
    return render_template('Home.html')

@app.route("/contact", methods=["POST"])
def Contact():
    form_data = request.form
    print form_data["email"]
    send_simple_message(form_data["email"])
    return render_template('Contact.html')

def send_simple_message(email):
    return requests.post(
        "https://api.mailgun.net/v3/sandboxa9ce70879809408aa3386c574ebdf5e6.mailgun.org/messages",
        auth=("api", "d470b0501ac7d51991d94c5c43b52951-059e099e-c9fa3bca"),
        data={"from": "Decisions 1.0<mailgun@sandboxa9ce70879809408aa3386c574ebdf5e6.mailgun.org>",
              "to": [email],
              "subject": "Contact Response",
              "text": "Thank for your expressed interest. We will definetely take your opinions on board when improving Decisions 1.0. In order to register your query please email <insert email> with your issue and will take it from there. Once again, thank you for your expressed interest and have a lovely day."})

@app.route("/decide2", methods=["POST"])
def Decide2():
    form_data = request.form
    main_name = form_data["name"]
    print form_data["name"]
    return render_template('Decide2.html', name=request.form["name"])

options_list()
print options_list

@app.route("/decide3", methods=["POST"])
def Decide3():
    form_data = request.form
    print form_data["option1"]
    print form_data["option2"]
    print form_data["option3"]
    options_list.append(form_data["option1"])
    options_list.append(form_data["option2"])
    options_list.append(form_data["option3"])
    print options_list
    return render_template('Decide3.html')




@app.route("/decide4.1", methods=["POST"])
def Decide41():
    form_data = request.form
    print form_data["variable1"]
    print form_data["variable2"]
    print form_data["variable3"]
    print form_data["option1"]
    return render_template('Decide4.html', variable1=request.form["variable1"], variable2=request.form["variable2"], variable3=request.form["variable3"], option1=request.form["option1"])


app.run(debug=True)
