from flask import Flask, render_template, request
import requests

app = Flask("DecideApp")

@app.route("/")
def homepage():
    return render_template("Home.html")

#Link between html page 1 and page 2
@app.route('/Decide', methods=['GET', 'POST'])
def Decide():
    if request.method == 'POST':
        # do stuff when the form is submitted
        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('homepage'))
    # show the form, it wasn't submitted
    return render_template('Decide.html')

@app.route("/signup", methods=["POST"])
def sign_up():
    form_data = request.form
    print form_data["email"]
    send_simple_message(form_data["email"])
    return "We'll get back to you soon."

def send_simple_message(email):
    return requests.post(
        "https://api.mailgun.net/v3/sandboxa9ce70879809408aa3386c574ebdf5e6.mailgun.org/messages",
        auth=("api", "d470b0501ac7d51991d94c5c43b52951-059e099e-c9fa3bca"),
        data={"from": "Welcome trial<mailgun@sandboxa9ce70879809408aa3386c574ebdf5e6.mailgun.org>",
              "to": [email],
              "subject": "Hello",
              "text": "Thanks for joining the team you will soon be able to hear more from blogs in the upcoming weeks."})

app.run(debug=True)
