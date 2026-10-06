from flask import Flask
from flask import jsonify
from werkzeug.routing import BaseConverter

app = Flask(__name__)  # Flask bắt buộc phải tìm thấy dòng này

class ListConverter(BaseConverter):
    regex = r"-?\d+(?:,-?\d+)*"

    def to_python(self, value):
        return [int(number) for number in value.split(",")]

    def to_url(self, values):
        return ",".join(super().to_url(value) for value in values)

app.url_map.converters["list"] = ListConverter

@app.route("/")
@app.route("/home")
@app.route("/index")
def home():
    return "Hello, Flask!"

@app.route("/chia-nhom")
def chia_nhom():
    so_bai = 12
    so_nhom = 0
    rs = f"Mỗi nhóm làm {so_bai / so_nhom} bài"
    return rs
@app.route("/user/<user_name>")
def user_profile(user_name):
    rs = f" xin chào bạn: {user_name}"
    return rs

@app.route("/square/<float:n>")
def square(n):
    return str(n ** 2)

@app.route("/sum/<list:numbers>")
def sum_numbers(numbers):
    return jsonify(numbers=numbers, sum=sum(numbers))

if __name__ == "__main__":
    app.run(debug=True, port=8000)