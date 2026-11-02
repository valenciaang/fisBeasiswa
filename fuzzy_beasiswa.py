class Variabel:
    def __init__(self, nama, min, max, rendah, tinggi):
        self.nama = nama
        self.min = min
        self.max = max
        self.rendah_params = rendah  
        self.tinggi_params = tinggi  

    def linier_naik(self, x, params):
        a, b = params
        if x <= a:
            return 0
        if x >= b:
            return 1
        return (x - a) / (b - a)

    def linier_turun(self, x, params):
        a, b = params
        if x <= a:
            return 1
        if x >= b:
            return 0
        return (b - x) / (b - a)

    def rendah(self, x):
        return self.linier_turun(x, self.rendah_params)

    def tinggi(self, x):
        return self.linier_naik(x, self.tinggi_params)

    def fuzzy(self, x):
        return {
            "RENDAH": self.rendah(x),
            "TINGGI": self.tinggi(x)
        }


class Rule:
    def __init__(self, nomor, labelIPK, labelPenghasilan, labelSkorKelayakan):
        self.nomor = nomor
        self.labelIPK = labelIPK
        self.labelPenghasilan = labelPenghasilan
        self.labelSkorKelayakan = labelSkorKelayakan

    def hitung(self, ipk, penghasilan):
        mu_ipk = ipk[self.labelIPK]
        mu_gaji = penghasilan[self.labelPenghasilan]

        # Operator OR = MAX
        alpha = min(mu_ipk, mu_gaji)

        # Konsekuen monoton (Tsukamoto): skor naik 0 -> 100
        if self.labelSkorKelayakan == "LAYAK":
            z = 100 * alpha
        else:
            z = 100 * (1 - alpha)

        return {
            "nomor": self.nomor,
            "labelIPK": self.labelIPK,
            "labelPenghasilan": self.labelPenghasilan,
            "labelSkor": self.labelSkorKelayakan,
            "mu_ipk": mu_ipk,
            "mu_gaji": mu_gaji,
            "alpha": alpha,
            "z": z
        }


class FuzzyBeasiswa:
    IPK_MIN = 3.0
    GAJI_MAX = 5000000

    def __init__(self):
        # IPK: hanya "TINGGI" yang dipakai (linier naik 3.0 -> 4.0)
        self.ipk = Variabel(
            "IPK", 3.0, 4.0,
            rendah=(3.0, 4.0),
            tinggi=(3.0, 4.0)
        )

        # Penghasilan: "RENDAH" = tidak mampu (linier turun 500rb -> 5jt)
        self.gaji = Variabel(
            "Penghasilan Orang Tua", 500000, 5000000,
            rendah=(500000, 5000000),
            tinggi=(500000, 5000000)
        )

        # JIKA IPK tinggi ATAU penghasilan rendah (tidak mampu) MAKA layak
        self.rules = [
            Rule(1, "TINGGI", "RENDAH", "LAYAK"),
            Rule(2, "TINGGI", "TINGGI", "TIDAK_LAYAK"),
            Rule(3, "RENDAH", "RENDAH", "LAYAK"),
            Rule(4, "RENDAH", "TINGGI", "TIDAK_LAYAK"),
        ]

    def keterangan(self, Z):
        return "Layak" if Z >= 50 else "Tidak Layak"

    def hitung(self, ipk, gaji):
        mu_ipk = self.ipk.fuzzy(ipk)
        mu_gaji = self.gaji.fuzzy(gaji)

        # Gerbang tolak
        if ipk < self.IPK_MIN or gaji >= self.GAJI_MAX:
            alasan = "IPK < 3.0" if ipk < self.IPK_MIN else "Penghasilan >= 5jt"
            return {
                "ipk": ipk,
                "gaji": gaji,
                "mu_ipk": {k: round(v, 4) for k, v in mu_ipk.items()},
                "mu_gaji": {k: round(v, 4) for k, v in mu_gaji.items()},
                "rules": [],
                "total_alpha": 0,
                "total_alpha_z": 0,
                "Z": 0,
                "keterangan": f"Tidak Layak ({alasan})"
            }

        hasil_rules = []
        total_alpha = 0
        total_alpha_z = 0

        for r in self.rules:
            hasil = r.hitung(mu_ipk, mu_gaji)
            hasil_rules.append(hasil)
            total_alpha += hasil["alpha"]
            total_alpha_z += hasil["alpha"] * hasil["z"]

        # Defuzzifikasi weighted average
        Z = round(total_alpha_z / total_alpha, 2) if total_alpha > 0 else 0

        return {
            "ipk": ipk,
            "gaji": gaji,
            "mu_ipk": {k: round(v, 4) for k, v in mu_ipk.items()},
            "mu_gaji": {k: round(v, 4) for k, v in mu_gaji.items()},
            "rules": hasil_rules,
            "total_alpha": round(total_alpha, 4),
            "total_alpha_z": round(total_alpha_z, 2),
            "Z": Z,
            "keterangan": self.keterangan(Z)
        }


if __name__ == "__main__":
    data = [
        (2.00, 500000), (2.50, 500000), (2.75, 500000), (3.00, 500000),
        (3.25, 500000), (3.50, 500000), (4.00, 500000), (3.00, 1000000),
        (3.00, 2500000), (3.25, 2500000), (3.50, 2500000), (4.00, 5000000),
        (3.50, 500000), (3.50, 1000000), (3.50, 2000000), (3.50, 2500000),
        (3.50, 3000000), (3.50, 4000000),
    ]

    f = FuzzyBeasiswa()
    for i, (ipk, gaji) in enumerate(data, 1):
        h = f.hitung(ipk, gaji)
        # print(f"{i:>2} | IPK {ipk:.2f} | Rp {gaji:>9,} | Skor {h['Z']:>6} | {h['keterangan']}")