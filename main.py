
import re
from flask import Flask, render_template, request
from fuzzy_beasiswa import FuzzyBeasiswa

app = Flask(__name__)
sistem = FuzzyBeasiswa()


def rupiah(x):
    return "{:,.0f}".format(x).replace(",", ".")


app.jinja_env.filters["rupiah"] = rupiah




# =========================================
# DATA PENGUJIAN
# =========================================

data_uji = [
    (2.00, 500000),
    (2.50, 500000),
    (2.75, 500000),
    (3.00, 500000),
    (3.25, 500000),
    (3.50, 500000),
    (4.00, 500000),
    (3.00, 1000000),
    (3.00, 2500000),
    (3.25, 2500000),
    (3.50, 2500000),
    (4.00, 5000000),
    (3.50, 500000),
    (3.50, 1000000),
    (3.50, 2000000),
    (3.50, 2500000),
    (3.50, 3000000),
    (3.50, 4000000),
    (3.50, 5000000),
    (3.50, 6000000)
]

# Menghitung skor dan status secara otomatis
hasil_pengujian = []

for no, (ipk, gaji) in enumerate(data_uji, start=1):
    hasil_uji = sistem.hitung(ipk, gaji)

    hasil_pengujian.append({
        "no": no,
        "ipk": ipk,
        "gaji": gaji,
        "skor": hasil_uji["Z"],
        "status": hasil_uji["keterangan"]
    })


@app.route("/", methods=["GET", "POST"])
def index():
    hasil = None
    error = None
    ipk_text = ""
    gaji_text = ""

    if request.method == "POST":
        ipk_text = request.form.get("ipk", "").strip()
        gaji_text = request.form.get("gaji", "").strip()

        try:
            ipk = float(ipk_text.replace(",", "."))

            angka = re.sub(r"[^\d]", "", gaji_text)

            if angka == "":
                raise ValueError

            gaji = int(angka)

            if not (0 <= ipk <= 4):
                error = "IPK harus di antara 0 sampai 4."

            elif gaji < 0:
                error = "Penghasilan tidak boleh negatif."

            else:
                hasil = sistem.hitung(ipk, gaji)

        except ValueError:
            error = "Masukkan IPK dan penghasilan orang tua dengan angka yang benar."

    return render_template(
        "index.html",
        hasil=hasil,
        error=error,
        ipk_text=ipk_text,
        gaji_text=gaji_text,
        hasil_pengujian=hasil_pengujian
    )


if __name__ == "__main__":
    app.run(debug=True)