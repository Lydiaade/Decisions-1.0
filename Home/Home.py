from flask import Flask, render_template, request, redirect, url_for
import requests
from operator import itemgetter

app = Flask("DecideApp")

@app.route("/")
def Homepage():
    return render_template("Home.html")

# Link -- Decide (input name and reasoning)
@app.route('/Decide', methods=['GET', 'POST'])
def Decide():
    if request.method == 'POST':
        return redirect(url_for('Homepage'))
    return render_template('Decide.html')


# Link -- How it works
@app.route('/Howitworks', methods=['GET', 'POST'])
def Howitworks():
    if request.method == 'POST':
        return redirect(url_for('Home'))
    return render_template('HowItWorks.html')

# Link -- Home page
@app.route('/Home', methods=['GET', 'POST'])
def Home():
    if request.method == 'POST':
        return redirect(url_for('Decide'))
    return render_template('Home.html')

# Link -- contact detail completion section
# once email has been included also initiates sending email
@app.route("/contact", methods=["POST"])
def Contact():
    form_data = request.form
    print(form_data["email"])
    send_simple_message(form_data["email"])
    return render_template('Contact.html')

# Sends email to whomever completes form
def send_simple_message(email):
    return requests.post(
        "https://api.mailgun.net/v3/sandboxa9ce70879809408aa3386c574ebdf5e6.mailgun.org/messages",
        auth=("api", "d470b0501ac7d51991d94c5c43b52951-059e099e-c9fa3bca"),
        data={"from": "Decisions 1.0<mailgun@sandboxa9ce70879809408aa3386c574ebdf5e6.mailgun.org>",
              "to": [email],
              "subject": "Contact Response",
              "text": "Thank for your expressed interest. We will definetely take your opinions on board when improving Decisions 1.0. In order to register your query please email <insert email> with your issue and will take it from there. Once again, thank you for your expressed interest and have a lovely day."})

name = "" # Username
reason = "" # Reasoning for use of website
options_dict = {} #options list
options_list = []
variables_dict = {} # Variables list
variables_list = []
result = []

# Link -- Decide 2 (options list)
# User name and reasoning
@app.route("/decide2", methods=["POST"])
def Decide2():
    name = request.form["name"].title()
    reason = request.form["reason"].lower()
    return render_template('Decide2.html', name=request.form["name"])

# Link -- Decide 3 (variables list)
# Options List
@app.route("/decide3", methods=["POST"])
def Decide3():
    for option in request.form.values():
        options_list.append(option)
        options_dict[option] = 0
    return render_template('Decide3.html')

# Link -- Decide 4 (prioritising factors)
# Variables List
@app.route("/decide4", methods=["POST"])
def Decide4():
    for name in request.form.values():
        variables_dict[name] = 0
        variables_list.append(name)
    for option in options_dict.keys():
            options_dict[option] = {variable:0 for variable in variables_list}
    print(variables_list)
    return render_template('Decide4.html', variable = variables_list)

# Link -- Rank Order 1 (ranking 1st variable)
# Prioritising factors
@app.route("/rankorder1", methods=["POST"])
def Rankorder1():
    print(variables_list)
    print(options_dict)
    for variable, value in request.form.items():
        variables_dict[variable] = int(value)
    return render_template('Ranking.html', variable = variables_list, option = options_list)

# NEW RANKING PAGE FOR DECISIONS
# Link -- Final outcome
# Ranking third option based on all variable
@app.route("/finaldecision", methods=["POST"])
def ranking():
    for key, value in request.form.items():
        opt_var = key.split(",")
        print(opt_var)
        options_dict[opt_var[0]][variables_list[int(opt_var[1])]] = int(value)

    for opt in options_list:
        total = 0
        for var in variables_list:
            total += options_dict[opt][var]*variables_dict[var]
        result.append((opt,total))

    decision = sorted(result, key=itemgetter(1), reverse=True)

    return render_template('FINAL.html', choice = decision, name = name, reason = reason)

# Clearing out the lists to calculate new decision
@app.route("/restart", methods=["POST"])
def restart():
    del name
    del reason
    options_dict.clear()
    options_list.clear()
    variables_dict.clear()
    variables_list.clear()
    result.clear()
    return render_template('Decide.html')

app.run(debug=True)