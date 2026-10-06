from flask import Flask, jsonify, request, abort, redirect, make_response
from markupsafe import escape

app = Flask(__name__)

STUDENTS = {
    "23T1020001": {
        "name": "Nguyễn Văn An",
        "lop": "K47A",
        "scores": {
            "PHNMHM": 8.5,
            "CSDL": 7.0,
            "MMT": 9.0
        },
    },

    "23T1020002": {
        "name": "Trần Thị Bình",
        "lop": "K47A",
        "scores": {
            "PHNMHM": 6.0,
            "CSDL": 5.5,
            "MMT": 7.0
        },
    },

    "23T1020003": {
        "name": "Lê Hoàng Cường",
        "lop": "K47B",
        "scores": {
            "PHNMHM": 9.5,
            "CSDL": 9.0
        },
    },

    "23T1020004": {
        "name": "Phạm Minh Dũng",
        "lop": "K47B",
        "scores": {
            "PHNMHM": 4.0,
            "CSDL": 3.5,
            "MMT": 5.0
        },
    },

    "23T1020005": {
        "name": "Hoàng Thu Hà",
        "lop": "K47A",
        "scores": {},
    },

    "23T1020006": {
        "name": "Võ Quốc Khánh",
        "lop": "K47C",
        "scores": {
            "PHNMHM": 7.5,
            "MMT": 8.0
        },
    },
}



def tinh_diem_tb(scores):
    if not scores:
        return None

    return sum(scores.values()) / len(scores)


def xep_loai(diem_tb):
    if diem_tb is None:
        return "-"

    if diem_tb >= 8.0:
        return "Giỏi"
    elif diem_tb >= 6.5:
        return "Khá"
    elif diem_tb >= 5.0:
        return "Trung bình"
    else:
        return "Yếu"



# CÂU 1 


@app.route("/")
def home():
    tong_so_sinh_vien = len(STUDENTS)

    cac_lop = set()

    for sinh_vien in STUDENTS.values():
        cac_lop.add(sinh_vien["lop"])

    so_lop = len(cac_lop)

    return f"""
    <h1>Quản lý sinh viên</h1>

    <p>Tổng số sinh viên: {tong_so_sinh_vien}</p>
    <p>Số lớp: {so_lop}</p>

    <p>
        <a href="/students">Danh sách sinh viên</a>
    </p>

    <p>
        <a href="/api/students">API sinh viên</a>
    </p>

    <p>
        <a href="/search">Tìm kiếm sinh viên</a>
    </p>
    """


# CÂU 2 - DANH SÁCH SINH VIÊN


@app.route("/students")
def students():
    lop_can_loc = request.args.get("lop")

    # Lấy danh sách lớp tự động từ dữ liệu
    cac_lop = set()

    for sinh_vien in STUDENTS.values():
        cac_lop.add(sinh_vien["lop"])

    # Tạo thanh lọc lớp
    thanh_loc = '<a href="/students">Tất cả</a>'

    for lop in sorted(cac_lop):
        thanh_loc += f' | <a href="/students?lop={lop}">{lop}</a>'

    # Tạo bảng
    bang = """
    <table border="1">
        <tr>
            <th>MSSV</th>
            <th>Họ tên</th>
            <th>Lớp</th>
            <th>Điểm TB</th>
            <th>Xếp loại</th>
        </tr>
    """

    so_ket_qua = 0

    for ma_sv, sinh_vien in STUDENTS.items():

        # Lọc theo lớp, không phân biệt hoa thường
        if lop_can_loc:
            if sinh_vien["lop"].lower() != lop_can_loc.lower():
                continue

        so_ket_qua += 1

        diem_tb = tinh_diem_tb(sinh_vien["scores"])
        xep_loai_sv = xep_loai(diem_tb)

        diem_hien_thi = (
            "-" if diem_tb is None else f"{diem_tb:.2f}"
        )

        bang += f"""
        <tr>
            <td>
                <a href="/students/{ma_sv}">{ma_sv}</a>
            </td>

            <td>{sinh_vien["name"]}</td>

            <td>{sinh_vien["lop"]}</td>

            <td>{diem_hien_thi}</td>

            <td>{xep_loai_sv}</td>
        </tr>
        """

    # Không có kết quả
    if so_ket_qua == 0:
        bang = "<p>Không có sinh viên phù hợp.</p>"
    else:
        bang += "</table>"

    return f"""
    <h1>Danh sách sinh viên</h1>

    <p>
        Tổng số sinh viên: {len(STUDENTS)}
    </p>

    <p>
        {thanh_loc}
    </p>

    {bang}
    """



# CÂU 3 - CHI TIẾT SINH VIÊN


@app.route("/students/<mssv>")
def student_detail(mssv):

    # Kiểm tra MSSV
    if mssv not in STUDENTS:
        abort(
            404,
            description=f"Không có sinh viên với MSSV = {mssv}."
        )

    sinh_vien = STUDENTS[mssv]

    # Tính điểm
    diem_tb = tinh_diem_tb(sinh_vien["scores"])
    xep_loai_sv = xep_loai(diem_tb)

    # Tạo bảng điểm
    bang_diem = """
    <table border="1">
        <tr>
            <th>Học phần</th>
            <th>Điểm</th>
        </tr>
    """

    for hoc_phan, diem in sinh_vien["scores"].items():
        bang_diem += f"""
        <tr>
            <td>{hoc_phan}</td>
            <td>{diem}</td>
        </tr>
        """

    if sinh_vien["scores"]:
        bang_diem += "</table>"
    else:
        bang_diem = "<p>Không có điểm.</p>"

    diem_tb_hien_thi = (
        "-" if diem_tb is None else f"{diem_tb:.2f}"
    )

    return f"""
    <h1>Chi tiết sinh viên</h1>

    <p>
        Họ tên: {sinh_vien["name"]}
    </p>

    <p>
        MSSV: {mssv}
    </p>

    <p>
        Lớp:
        <a href="/students?lop={sinh_vien["lop"]}">
            {sinh_vien["lop"]}
        </a>
    </p>

    <p>
        Điểm TB: {diem_tb_hien_thi}
    </p>

    <p>
        Xếp loại: {xep_loai_sv}
    </p>

    <h2>Bảng điểm</h2>

    {bang_diem}

    <p>
        <a href="/students/{mssv}/export">
            Tải bảng điểm (CSV)
        </a>
    </p>

    <p>
        Link rút gọn:
        <a href="/sv/{mssv}">
            /sv/{mssv}
        </a>
    </p>
    """


# CÂU 4 - REDIRECT 301


@app.route("/sv/<mssv>")
def old_student(mssv):
    return redirect(
        f"/students/{mssv}",
        code=301
    )



# CÂU 5 - XUẤT BẢNG ĐIỂM CSV


@app.route("/students/<mssv>/export")
def export_student_csv(mssv):

    # Kiểm tra MSSV
    if mssv not in STUDENTS:
        abort(
            404,
            description=f"Không có sinh viên với MSSV = {mssv}."
        )

    sinh_vien = STUDENTS[mssv]

    # Tạo nội dung CSV
    noi_dung_csv = "hoc_phan,diem\n"

    for hoc_phan, diem in sinh_vien["scores"].items():
        noi_dung_csv += f"{hoc_phan},{diem}\n"

    # Tạo response để tải file
    response = make_response(noi_dung_csv)

    response.headers["Content-Type"] = (
        "text/csv; charset=utf-8"
    )

    response.headers["Content-Disposition"] = (
        f"attachment; filename=diem_{mssv}.csv"
    )

    return response



# CÂU 6 - TÌM KIẾM AN TOÀN


@app.route("/search")
def search_students():

    # Lấy từ khóa
    tu_khoa = request.args.get("q", "")

    # Chuyển thành chữ thường để tìm kiếm
    tu_khoa_tim_kiem = tu_khoa.lower()

    ket_qua = []

    # Tìm theo Họ tên hoặc MSSV
    for mssv, sinh_vien in STUDENTS.items():

        ten = sinh_vien["name"].lower()

        if (
            tu_khoa_tim_kiem in ten
            or tu_khoa_tim_kiem in mssv.lower()
        ):
            ket_qua.append(
                (mssv, sinh_vien)
            )

    # Escape từ khóa để chống XSS
    tu_khoa_an_toan = escape(tu_khoa)

    # Tạo danh sách kết quả
    danh_sach = ""

    for mssv, sinh_vien in ket_qua:

        danh_sach += f"""
        <li>
            <a href="/students/{mssv}">
                {escape(mssv)}
            </a>

            - {escape(sinh_vien["name"])}

            - {escape(sinh_vien["lop"])}
        </li>
        """

    if not ket_qua:
        danh_sach = (
            "<p>Không tìm thấy sinh viên phù hợp.</p>"
        )

    return f"""
    <h1>Tìm kiếm sinh viên</h1>

    <form method="GET" action="/search">

        <input
            type="text"
            name="q"
            value="{tu_khoa_an_toan}"
            placeholder="Nhập họ tên hoặc MSSV"
        >

        <button type="submit">
            Tìm kiếm
        </button>

    </form>

    <h2>
        Tìm thấy {len(ket_qua)}
        kết quả cho '{tu_khoa_an_toan}'
    </h2>

    <ul>
        {danh_sach}
    </ul>
    """


@app.route("/api/students")
def api_students():
    return jsonify(STUDENTS)



if __name__ == "__main__":
    app.run(
        debug=True,
        port=8000
    )