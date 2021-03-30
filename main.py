from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

students = [
    {
        "first_name": "Riju",
        "last_name": "Krishnamurthy",
        "age": 21,
        "gender": "female",
        "mobile": "7858183325"
    },
    {
        "first_name": "Priya",
        "last_name": "Krishnamurthy",
        "age": 50,
        "gender": "female",
        "mobile": "9840792111"
    },
    {
        "first_name": "Anantharajan",
        "last_name": "Krishnamurthy",
        "age": 56,
        "gender": "male",
        "mobile": "9840792225"
    },
    {
        "first_name": "Juhi",
        "last_name": "Krishnamurthy",
        "age": 26,
        "gender": "female",
        "mobile": "4304694896"
    },
]


def is_exist_student(mobile):
    return any(student['mobile'] == mobile for student in students)


def get_by_mobile(s_list, mobile):
    return next(x for x in s_list if x['mobile'] == mobile)


def update_student_info(mobile, req):
    for s in students:
        if s['mobile'] == mobile:
            for key in req.json.keys():
                if key != 'mobile':
                    if key == 'age':
                        s[key] = int(req.json.get(key))
                    else:
                        s[key] = req.json.get(key)


# GET method
@app.route("/students")
def get_students():
    return render_template("students.html", data=students)


# GET method using Query Strings
@app.route("/student")
def get_a_student():
    mobile = request.args.get("mobile")
    return jsonify(get_by_mobile(students, mobile))


# Path parameters
@app.route("/student/<mobile>")
def get_student(mobile):
    return jsonify(get_by_mobile(students, mobile))


# POST method using Postman
@app.route("/student/<mobile>", methods=['POST'])
def create_student(mobile):
    # using form-data
    # print(request.form['first_name'], request.form['last_name'], request.form["age"], request.form["gender"])

    # using json
    # print(request.json['first_name'], request.json['last_name'], request.json["age"], request.json["gender"])

    if not is_exist_student(mobile):
        students.append({
            "first_name": request.json['first_name'],
            "last_name": request.json['last_name'],
            "age": int(request.json["age"]),
            "gender": request.json["gender"],
            "mobile": mobile
        })
        return f"Created Student record for {mobile}"
    else:
        return f"ERROR: Student with {mobile} already exists"


# PUT method using Postman
@app.route("/student/<mobile>", methods=['PUT'])
def update_student(mobile):
    if is_exist_student(mobile):
        update_student_info(mobile, request)
        return f"Updated Student record for {mobile}"
    else:
        return f"ERROR: Student with {mobile} does not exist"


# DELETE method using Postman
@app.route("/student/<mobile>", methods=['DELETE'])
def delete_student(mobile):
    if is_exist_student(mobile):
        for i, d in enumerate(students):
            if d['mobile'] == mobile:
                del students[i]
                return f"Deleted Student record for {mobile}"
    return f"ERROR: Student with {mobile} does not exist"


if __name__ == "__main__":
    app.run(debug=True)
