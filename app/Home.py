from flask import Flask, render_template, request, redirect, url_for
import requests
from operator import itemgetter

from app.api.adapter.mailing_adapter import mailing_message

app = Flask("DecideApp")


@app.route("/")
def homepage():
    return render_template("Home.html")


# Link -- Decide (input name and reasoning)
@app.route('/decide', methods=['GET', 'POST'])
def decide():
    if request.method == 'POST':
        return redirect(url_for('Homepage'))
    return render_template('Decide.html')


# Link -- How it works
@app.route('/howitworks', methods=['GET', 'POST'])
def how_it_works():
    if request.method == 'POST':
        return redirect(url_for('app'))
    return render_template('HowItWorks.html')


# Link -- app page
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        return redirect(url_for('Decide'))
    return render_template('Home.html')


# Link -- contact detail completion section
# once email has been included also initiates sending email
@app.route("/contact", methods=["POST"])
def contact():
    form_data = request.form
    print(form_data["email"])
    _send_simple_message(form_data["email"])
    return render_template('Contact.html')


# Sends email to whomever completes form
def _send_simple_message(email: str):
    return requests.post(mailing_message(email))


name = ""  # Username
reason = ""  # Reasoning for use of website
options_dict = {}  # options list
options_list = []
variables_dict = {}  # Variables list
variables_list = []
result = []


# Link -- Decide 2 (options list)
# Username and reasoning
@app.route("/decide2", methods=["POST"])
def decide_2():
    name = request.form["name"].title()
    reason = request.form["reason"].lower()
    return render_template('Decide2.html', name=name)


# Link -- Decide 3 (variables list)
# Options List
@app.route("/decide3", methods=["POST"])
def decide_3():
    for option in request.form.values():
        options_list.append(option)
        options_dict[option] = 0
    return render_template('Decide3.html')


# Link -- Decide 4 (prioritising factors)
# Variables List
@app.route("/decide4", methods=["POST"])
def decide_4():
    for value in request.form.values():
        variables_dict[value] = 0
        variables_list.append(value)
    for key in options_dict.keys():
        options_dict[key] = {variable: 0 for variable in variables_list}
    print(variables_list)
    return render_template('Decide4.html', variable=variables_list)


# Link -- Rank Order 1 (ranking 1st variable)
# Prioritising factors
@app.route("/rankorder1", methods=["POST"])
def rank_order_1():
    print(variables_list)
    print(options_dict)
    for variable, value in request.form.items():
        variables_dict[variable] = int(value)
    return render_template('Ranking.html', variable=variables_list, option=options_list)


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
            total += options_dict[opt][var] * variables_dict[var]
        result.append((opt, total))

    decision = sorted(result, key=itemgetter(1), reverse=True)

    return render_template('FINAL.html', choice=decision, name=name, reason=reason)


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


if __name__ == "__main__":
    app.run(debug=True)
