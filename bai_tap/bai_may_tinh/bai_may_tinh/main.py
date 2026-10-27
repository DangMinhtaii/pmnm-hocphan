
from flask import Flask, render_template, request

app = Flask(__name__)


# TRANG CHU
@app.route("/")
def trang_chu():
    return render_template("index.html")


# BAI 1: MAY TINH CO BAN
@app.route("/may-tinh", methods=["GET", "POST"])
def may_tinh():
    ket_qua = None
    loi = None

    if request.method == "POST":
        try:
            so_a = float(request.form.get("so_a", ""))
            so_b = float(request.form.get("so_b", ""))
            phep_tinh = request.form.get("phep_tinh", "")

            if phep_tinh == "cong":
                ket_qua = so_a + so_b
            elif phep_tinh == "tru":
                ket_qua = so_a - so_b
            elif phep_tinh == "nhan":
                ket_qua = so_a * so_b
            elif phep_tinh == "chia":
                if so_b == 0:
                    loi = "Khong the chia cho 0!"
                else:
                    ket_qua = so_a / so_b
            else:
                loi = "Vui long chon phep tinh!"

        except ValueError:
            loi = "Vui long nhap so hop le!"

    return render_template(
        "calculator.html",
        ket_qua=ket_qua,
        loi=loi
    )


# BAI 2: TINH DIEM HOC PHAN
@app.route("/tinh-diem", methods=["GET", "POST"])
def tinh_diem():
    diem_trung_binh = None
    diem_chu = None
    ket_qua = None
    loi = None

    if request.method == "POST":
        try:
            diem_cc = float(request.form.get("diem_cc", ""))
            diem_gk = float(request.form.get("diem_gk", ""))
            diem_ck = float(request.form.get("diem_ck", ""))

            if not all(0 <= diem <= 10 for diem in
                       [diem_cc, diem_gk, diem_ck]):
                loi = "Diem phai tu 0 den 10!"
            else:
                diem_trung_binh = (
                    diem_cc * 0.1
                    + diem_gk * 0.3
                    + diem_ck * 0.6
                )

                if diem_ck < 1:
                    diem_chu = "F"
                    ket_qua = "Khong dat do diem cuoi ky duoi 1."
                elif diem_trung_binh >= 8.5:
                    diem_chu = "A"
                    ket_qua = "Xuat sac"
                elif diem_trung_binh >= 7:
                    diem_chu = "B"
                    ket_qua = "Kha"
                elif diem_trung_binh >= 5.5:
                    diem_chu = "C"
                    ket_qua = "Trung binh"
                elif diem_trung_binh >= 4:
                    diem_chu = "D"
                    ket_qua = "Dat"
                else:
                    diem_chu = "F"
                    ket_qua = "Khong dat"

        except ValueError:
            loi = "Vui long nhap day du diem hop le!"

    return render_template(
        "bai2.html",
        diem_trung_binh=diem_trung_binh,
        diem_chu=diem_chu,
        ket_qua=ket_qua,
        loi=loi
    )


# BAI 3: TINH CHI SO BMI
@app.route("/bmi", methods=["GET", "POST"])
def tinh_bmi():
    bmi = None
    phan_loai = None
    mau_ket_qua = None

    chieu_cao = ""
    can_nang = ""

    loi_chieu_cao = None
    loi_can_nang = None
    can_nang_chuan = None

    if request.method == "POST":
        chieu_cao = request.form.get("chieu_cao", "").strip()
        can_nang = request.form.get("can_nang", "").strip()

        # Kiem tra chieu cao
        try:
            chieu_cao_so = float(chieu_cao.replace(",", "."))

            if not 50 <= chieu_cao_so <= 250:
                loi_chieu_cao = "Gia tri phai tu 50 den 250 cm."

        except ValueError:
            chieu_cao_so = None
            loi_chieu_cao = "Loi: chieu cao phai la mot so."

        # Kiem tra can nang
        try:
            can_nang_so = float(can_nang.replace(",", "."))

            if not 10 <= can_nang_so <= 300:
                loi_can_nang = "Gia tri phai tu 10 den 300 kg."

        except ValueError:
            can_nang_so = None
            loi_can_nang = "Loi: can nang phai la mot so."

        # Tinh BMI neu du lieu hop le
        if loi_chieu_cao is None and loi_can_nang is None:
            chieu_cao_m = chieu_cao_so / 100

            bmi = round(
                can_nang_so / (chieu_cao_m ** 2),
                1
            )

            # Phan loai theo chuan nguoi chau A
            if bmi < 18.5:
                phan_loai = "Thieu can"
                mau_ket_qua = "vang"
            elif bmi < 23:
                phan_loai = "Binh thuong"
                mau_ket_qua = "xanh"
            elif bmi < 25:
                phan_loai = "Thua can"
                mau_ket_qua = "vang"
            else:
                phan_loai = "Beo phi"
                mau_ket_qua = "do"

            # Can nang tham khao voi BMI tu 18.5 den 22.9
            can_nang_min = 18.5 * (chieu_cao_m ** 2)
            can_nang_max = 22.9 * (chieu_cao_m ** 2)

            can_nang_chuan = (
                round(can_nang_min, 1),
                round(can_nang_max, 1)
            )

    return render_template(
        "bmi.html",
        bmi=bmi,
        phan_loai=phan_loai,
        mau_ket_qua=mau_ket_qua,
        chieu_cao=chieu_cao,
        can_nang=can_nang,
        loi_chieu_cao=loi_chieu_cao,
        loi_can_nang=loi_can_nang,
        can_nang_chuan=can_nang_chuan
    )


if __name__ == "__main__":
    app.run(debug=True)
