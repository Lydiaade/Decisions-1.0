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

main_name = "" # Username
reasoning = "" # Reasoning for use of website

# Link -- Decide 2 (options list)
# User name and reasoning
@app.route("/decide2", methods=["POST"])
def Decide2():
    main_name = request.form["name"]
    reasoning = request.form["reason"]
    return render_template('Decide2.html', name=request.form["name"])

options_dict = {} #options list
options_list = []

# Link -- Decide 3 (variables list)
# Options List
@app.route("/decide3", methods=["POST"])
def Decide3():
    for name in request.form.values():
        options_list.append(name)
        options_dict[name] = 0
    return render_template('Decide3.html')

variables_dict = {} # Variables list
variables_list = []

# Link -- Decide 4 (prioritising factors)
# Variables List
@app.route("/decide4", methods=["POST"])
def Decide4():
    for name in request.form.values():
        variables_dict[name] = 0
        variables_list.append(name)
    for option in options_dict.keys():
            options_dict[option] = {variable:0 for variable in variables_list}
    return render_template('Decide4.html', variable1=variables_list[0], variable2=variables_list[1], variable3=variables_list[2])

# Link -- Rank Order 1 (ranking 1st variable)
# Prioritising factors
@app.route("/rankorder1", methods=["POST"])
def Rankorder1():
    print(options_dict)
    for variable, value in request.form.items():
        variables_dict[variable] = int(value)
    return render_template('Ranking.html', variable1=variables_list[0], variable2=variables_list[1], variable3=variables_list[2],
    option1=options_list[0], option2=options_list[1], option3=options_list[2])

result = []

# NEW RANKING PAGE FOR DECISIONS
# Link -- Final outcome
# Ranking third option based on all variable
@app.route("/finaldecision", methods=["POST"])
def ranking():
    for key, value in request.form.items():
        opt_var = key.split(",")
        options_dict[opt_var[0]][variables_list[int(opt_var[1])]] = int(value)

    for opt in options_list:
        total = 0
        for var in variables_list:
            total += options_dict[opt][var]*variables_dict[var]
        result.append((opt,total))

    decision = sorted(result, key=itemgetter(1), reverse=True)

    return render_template('FINAL.html', decision, reasoning, main_name)




















# option1_ranks=[] # Ranking in order for first variable
# results_for_all_options=[] # All options final result

# # Link -- Rank Order 2 (ranking 2nd variable)
# # Ranking first option based on all variable
# @app.route("/rankorder2", methods=["POST"])
# def Rankorder2():
#     form_data = request.form
#     print(form_data["opt1rank1"])
#     print(form_data["opt1rank2"])
#     print(form_data["opt1rank3"])
#     option1_ranks.append(form_data["opt1rank1"])
#     option1_ranks.append(form_data["opt1rank2"])
#     option1_ranks.append(form_data["opt1rank3"])
#     print(option1_ranks)
#     result1= (4-float(main_ranks_list[0]))*float(option1_ranks[0]) + (4-float(main_ranks_list[1]))*float(option1_ranks[1]) + (4-float(main_ranks_list[2]))*float(option1_ranks[2])
#     print(result1)
#     results_for_all_options.append(result1)
#     print(results_for_all_options)
#     return render_template('RankOrdering2.html', variable1=variables_dict[0], variable2=variables_dict[1], variable3=variables_dict[2], option2=options_dict[1])


# option2_ranks=[] # Ranking in order for second variable

# # Link -- Rank Order 3 (ranking 3rd variable)
# # Ranking second option based on all variable
# @app.route("/rankorder3", methods=["POST"])
# def Rankorder3():
#     form_data = request.form
#     print(form_data["opt2rank1"])
#     print(form_data["opt2rank2"])
#     print(form_data["opt2rank3"])
#     option2_ranks.append(form_data["opt2rank1"])
#     option2_ranks.append(form_data["opt2rank2"])
#     option2_ranks.append(form_data["opt2rank3"])
#     print(option2_ranks)
#     result2= (4-float(main_ranks_list[0]))*float(option2_ranks[0]) + (4-float(main_ranks_list[1]))*float(option2_ranks[1]) + (4-float(main_ranks_list[2]))*float(option2_ranks[2])
#     print(result2)
#     results_for_all_options.append(result2)
#     print(results_for_all_options)
#     return render_template('RankOrdering3.html', variable1=variables_dict[0], variable2=variables_dict[1], variable3=variables_dict[2], option3=options_dict[2])

# option3_ranks=[]

# # Link -- Final outcome
# # Ranking third option based on all variable
# @app.route("/finaldecision", methods=["POST"])
# def finaldecision():
#     form_data = request.form
#     print(form_data["opt3rank1"])
#     print(form_data["opt3rank2"])
#     print(form_data["opt3rank3"])
#     option3_ranks.append(form_data["opt3rank1"])
#     option3_ranks.append(form_data["opt3rank2"])
#     option3_ranks.append(form_data["opt3rank3"])
#     print(option3_ranks)
#     result3= (4-float(main_ranks_list[0]))*float(option3_ranks[0]) + (4-float(main_ranks_list[1]))*float(option3_ranks[1]) + (4-float(main_ranks_list[2]))*float(option3_ranks[2])
#     print(result3)
#     results_for_all_options.append(result3)
#     print(results_for_all_options)
#     final_conclusion1()
#     final_conclusion2()
#     final_conclusion3()
#     print(ordered_final_list)
#     print(corr_ordered_final_list)
#     return render_template('FINAL.html', name=main_name[0], reason=reasoning[0], option1=ordered_final_list[0], option1point=corr_ordered_final_list[0], option2=ordered_final_list[1], option2point=corr_ordered_final_list[1], option3=ordered_final_list[2], option3point=corr_ordered_final_list[2] )
















ordered_final_list=[]
corr_ordered_final_list=[]

# def final_conclusion1():
#     if (results_for_all_options[0]>results_for_all_options[1] and results_for_all_options[0]>results_for_all_options[2]):
#         ordered_final_list.append(options_dict[0])
#         corr_ordered_final_list.append(results_for_all_options[0])
#         print("Winner is ",options_dict[0],", with ",results_for_all_options[0],)
#         print(ordered_final_list)
#     elif (results_for_all_options[1]>results_for_all_options[0] and results_for_all_options[1]>results_for_all_options[2]):
#         ordered_final_list.append(options_dict[1])
#         corr_ordered_final_list.append(results_for_all_options[1])
#         print("Winner is ",options_dict[1],", with ",results_for_all_options[1],)
#         print(ordered_final_list)
#     else:
#         ordered_final_list.append(options_dict[2])
#         corr_ordered_final_list.append(results_for_all_options[2])
#         print("Winner is ",options_dict[2],", with ",results_for_all_options[2],)
#         print(ordered_final_list)

# def final_conclusion2():
#     if ((results_for_all_options[0]>results_for_all_options[1] and results_for_all_options[0]<results_for_all_options[2]) or (results_for_all_options[0]<results_for_all_options[1] and results_for_all_options[0]>results_for_all_options[2])):
#         ordered_final_list.append(options_dict[0])
#         corr_ordered_final_list.append(results_for_all_options[0])
#         print("Second is ",options_dict[0],", with ",results_for_all_options[0],)
#         print(ordered_final_list)
#     elif ((results_for_all_options[1]>results_for_all_options[0] and results_for_all_options[1]<results_for_all_options[2]) or (results_for_all_options[1]<results_for_all_options[0] and results_for_all_options[1]>results_for_all_options[2])):
#         ordered_final_list.append(options_dict[1])
#         corr_ordered_final_list.append(results_for_all_options[1])
#         print("Second is ",options_dict[1],", with ",results_for_all_options[1],)
#         print(ordered_final_list)
#     else:
#         ordered_final_list.append(options_dict[2])
#         corr_ordered_final_list.append(results_for_all_options[2])
#         print("Second is ",options_dict[2],", with ",results_for_all_options[2],)
#         print(ordered_final_list)

# def final_conclusion3():
#     if (results_for_all_options[0]<results_for_all_options[1] and results_for_all_options[0]<results_for_all_options[2]):
#         ordered_final_list.append(options_dict[0])
#         corr_ordered_final_list.append(results_for_all_options[0])
#         print("Last is ",options_dict[0],", with ",results_for_all_options[0],)
#         print(ordered_final_list)
#     elif (results_for_all_options[1]<results_for_all_options[0] and results_for_all_options[1]<results_for_all_options[2]):
#         ordered_final_list.append(options_dict[1])
#         corr_ordered_final_list.append(results_for_all_options[1])
#         print("Last is ",options_dict[1],", with ",results_for_all_options[1],)
#         print(ordered_final_list)
#     else:
#         ordered_final_list.append(options_dict[2])
#         corr_ordered_final_list.append(results_for_all_options[2])
#         print("Last is ",options_dict[2],", with ",results_for_all_options[2],)
#         print(ordered_final_list)


# Clearing out the lists to calculate new decision
@app.route("/restart", methods=["POST"])
def restart():
    del main_name[:]
    print(main_name)
    del reasoning[:]
    print(reasoning)
    del options_dict[:]
    print(options_dict)
    del variables_dict[:]
    print(variables_dict)
    del main_ranks_list[:]
    print(main_ranks_list)
    del option1_ranks[:]
    print(option1_ranks)
    del results_for_all_options[:]
    print(results_for_all_options)
    del option2_ranks[:]
    print(option2_ranks)
    del option3_ranks[:]
    print(option3_ranks)
    del ordered_final_list[:]
    print(ordered_final_list)
    del corr_ordered_final_list[:]
    print(corr_ordered_final_list)
    return render_template('Decide.html')



app.run(debug=True)
