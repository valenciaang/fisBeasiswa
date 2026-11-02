def fuzzifikasi(nilai, min, max):
    # Linier Turun
    if nilai <= min:
        mu_rendah = 1.0
    elif nilai >= max:
        mu_rendah = 0.0
    else:
        mu_rendah = (max - nilai) / (max - min)

    # Linier Naik
    if nilai <= min:
        mu_tinggi = 0.0
    elif nilai >= max:
        mu_tinggi = 1.0
    else:
        mu_tinggi = (nilai - min) / (max - min)

    return {
        "RENDAH": round(mu_rendah, 4),
        "TINGGI": round(mu_tinggi, 4)
    }

def hitung_z(alpha, jenis_output, z_min, z_max):
    if jenis_output == "LAYAK":
        return z_min + (alpha * (z_max - z_min))
    else:
        return z_max - (alpha * (z_max - z_min))

def hitung_beasiswa(ipk, gaji):
    IPK_MIN, IPK_MAX = 3.0, 4.0
    GAJI_MIN, GAJI_MAX = 500000, 5000000
    SKOR_MIN, SKOR_MAX = 0, 100

    if ipk < IPK_MIN:
        return {"Z": 0, "keterangan": f"Tidak Layak (IPK < {IPK_MIN})"}
    
    if gaji >= GAJI_MAX:
        return {"Z": 0, "keterangan": f"Tidak Layak (Penghasilan >= {GAJI_MAX:,})"}

    mu_ipk = fuzzifikasi(ipk, IPK_MIN, IPK_MAX)
    mu_gaji = fuzzifikasi(gaji, GAJI_MIN, GAJI_MAX)

    a1 = min(mu_ipk["TINGGI"], mu_gaji["RENDAH"])
    z1 = hitung_z(a1, "LAYAK", SKOR_MIN, SKOR_MAX)

    a2 = min(mu_ipk["TINGGI"], mu_gaji["TINGGI"])
    z2 = hitung_z(a2, "TIDAK_LAYAK", SKOR_MIN, SKOR_MAX)

    a3 = min(mu_ipk["RENDAH"], mu_gaji["RENDAH"])
    z3 = hitung_z(a3, "LAYAK", SKOR_MIN, SKOR_MAX)

    a4 = min(mu_ipk["RENDAH"], mu_gaji["TINGGI"])
    z4 = hitung_z(a4, "TIDAK_LAYAK", SKOR_MIN, SKOR_MAX)

    total_alpha = a1 + a2 + a3 + a4
    total_alpha_z = (a1 * z1) + (a2 * z2) + (a3 * z3) + (a4 * z4)

    skor_z = round(total_alpha_z / total_alpha, 2) if total_alpha > 0 else 0

    if 50 <= skor_z <= 100:
        status = "Layak"
    else:
        status = "Tidak Layak"

    return {
        "Z": skor_z,
        "keterangan": status,
        "mu_ipk": mu_ipk,
        "mu_gaji": mu_gaji
    }


# class Variabel:
#     def __init__(self, nama, min, max, rendah, tinggi):
#         self.nama = nama
#         self.min = min
#         self.max = max
#         self.rendah_params = rendah  
#         self.tinggi_params = tinggi  

#     def linier_naik(self, x, params):
#         a, b = params
#         if x <= a:
#             return 0
#         if x >= b:
#             return 1
#         return (x - a) / (b - a)

#     def linier_turun(self, x, params):
#         a, b = params
#         if x <= a:
#             return 1
#         if x >= b:
#             return 0
#         return (b - x) / (b - a)

#     def rendah(self, x):
#         return self.linier_turun(x, self.rendah_params)

#     def tinggi(self, x):
#         return self.linier_naik(x, self.tinggi_params)

#     def fuzzy(self, x):
#         return {
#             "RENDAH": self.rendah(x),
#             "TINGGI": self.tinggi(x)
#         }


# class Rule:
#     def __init__(self, nomor, labelIPK, labelPenghasilan, labelSkorKelayakan):
#         self.nomor = nomor
#         self.labelIPK = labelIPK
#         self.labelPenghasilan = labelPenghasilan
#         self.labelSkorKelayakan = labelSkorKelayakan

#     def hitung(self, ipk, penghasilan):
#         mu_ipk = ipk[self.labelIPK]
#         mu_gaji = penghasilan[self.labelPenghasilan]

#         alpha = min(mu_ipk, mu_gaji)

#         if self.labelSkorKelayakan == "LAYAK":
#             z = 0 + alpha * (100 - 0)    
#         else:
#             z = 100 - alpha * (100 - 0)  

#         return {
#             "nomor": self.nomor,
#             "labelIPK": self.labelIPK,
#             "labelPenghasilan": self.labelPenghasilan,
#             "labelSkor": self.labelSkorKelayakan,
#             "mu_ipk": mu_ipk,
#             "mu_gaji": mu_gaji,
#             "alpha": alpha,
#             "z": z
#         }


# class FuzzyBeasiswa:
#     IPK_MIN = 3.0
#     GAJI_MAX = 5000000

#     def __init__(self):
#         self.ipk = Variabel(
#             "IPK", 3.0, 4.0,
#             rendah=(3.0, 4.0),
#             tinggi=(3.0, 4.0)
#         )

#         self.gaji = Variabel(
#             "Penghasilan Orang Tua", 500000, 5000000,
#             rendah=(500000, 5000000),
#             tinggi=(500000, 5000000)
#         )

#         self.rules = [
#             Rule(1, "TINGGI", "RENDAH", "LAYAK"),
#             Rule(2, "TINGGI", "TINGGI", "TIDAK_LAYAK"),
#             Rule(3, "RENDAH", "RENDAH", "LAYAK"),
#             Rule(4, "RENDAH", "TINGGI", "TIDAK_LAYAK"),
#         ]

#     def keterangan(self, Z):
#         if Z >= 50:
#             return "Layak"
#         else:
#             return "Tidak Layak"

#     def hitung(self, ipk, gaji):
#         mu_ipk = self.ipk.fuzzy(ipk)
#         mu_gaji = self.gaji.fuzzy(gaji)

#         if ipk < self.IPK_MIN or gaji >= self.GAJI_MAX:
#             if ipk < self.IPK_MIN:
#                 alasan = "IPK < 3.0"
#             else:
#                 alasan = "Penghasilan >= 5jt"
#             return {
#                 "ipk": ipk,
#                 "gaji": gaji,
#                 "mu_ipk": {
#                     "RENDAH": round(mu_ipk["RENDAH"], 4),
#                     "TINGGI": round(mu_ipk["TINGGI"], 4)
#                 },
#                 "mu_gaji": {
#                     "RENDAH": round(mu_gaji["RENDAH"], 4),
#                     "TINGGI": round(mu_gaji["TINGGI"], 4)
#                 },
#                 "rules": [],
#                 "total_alpha": 0,
#                 "total_alpha_z": 0,
#                 "Z": 0,
#                 "keterangan": f"Tidak Layak ({alasan})"
#             }

#         hasil_rules = []
#         total_alpha = 0
#         total_alpha_z = 0

#         for r in self.rules:
#             hasil = r.hitung(mu_ipk, mu_gaji)
#             hasil_rules.append(hasil)
#             total_alpha += hasil["alpha"]
#             total_alpha_z += hasil["alpha"] * hasil["z"]

#         if total_alpha > 0:
#             Z = round(total_alpha_z / total_alpha, 2)
#         else:
#             Z = 0

#         return {
#             "ipk": ipk,
#             "gaji": gaji,
#             "mu_ipk": {
#                 "RENDAH": round(mu_ipk["RENDAH"], 4),
#                 "TINGGI": round(mu_ipk["TINGGI"], 4)
#             },
#             "mu_gaji": {
#                 "RENDAH": round(mu_gaji["RENDAH"], 4),
#                 "TINGGI": round(mu_gaji["TINGGI"], 4)
#             },
#             "rules": hasil_rules,
#             "total_alpha": round(total_alpha, 4),
#             "total_alpha_z": round(total_alpha_z, 2),
#             "Z": Z,
#             "keterangan": self.keterangan(Z)
#         }


# if __name__ == "__main__":
#     data = [
#         (2.00, 500000), (2.50, 500000), (2.75, 500000), (3.00, 500000),
#         (3.25, 500000), (3.50, 500000), (4.00, 500000), (3.00, 1000000),
#         (3.00, 2500000), (3.25, 2500000), (3.50, 2500000), (4.00, 5000000),
#         (3.50, 500000), (3.50, 1000000), (3.50, 2000000), (3.50, 2500000),
#         (3.50, 3000000), (3.50, 4000000),
#     ]

#     f = FuzzyBeasiswa()
#     for i, (ipk, gaji) in enumerate(data, 1):
#         h = f.hitung(ipk, gaji)
#         print(f"{i:>2} | IPK {ipk:.2f} | Rp {gaji:>9,} | Skor {h['Z']:>6} | {h['keterangan']}")