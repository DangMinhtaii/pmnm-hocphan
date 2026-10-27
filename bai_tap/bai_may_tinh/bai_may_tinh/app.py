
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def calculator():
    a = ""
    b = ""
    op = "+"
    errors = {"a": "", "b": "", "op": ""}
    result = None
    a_num = None
    b_num = None

    if request.method == "POST":
        a = request.form.get("a", "").strip()
        b = request.form.get("b", "").strip()
        op = request.form.get("op", "")

        try:
            a_num = float(a.replace(",", ""))
          
        except ValueError:
            errors["a"] = "Vui lòng nhập một số."

        try:
            b_num = float(b.replace(",", ""))
        except ValueError:
            errors["b"] = "Vui lòng nhập một số."

      
        if op not in ["+", "-", "*", "/"]:
            errors["op"] = "Phép toán không hợp lệ."

      
        if op == "/" and b_num == 0 and not errors["b"]:
            errors["b"] = "Không thể chia cho 0."

       
        if not any(errors.values()):
            if op == "+":
                result = a_num + b_num
            elif op == "-":
                result = a_num - b_num
            elif op == "*":
                result = a_num * b_num
            elif op == "/":
                result = a_num / b_num

    return render_template(
        "calculator.html",
        a=a,
        b=b,
        op=op,
        errors=errors,
        result=result,
        a_num=a_num,
        b_num=b_num
    )


if __name__ == "__main__":
    app.run(debug=True)
