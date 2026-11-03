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
    IPK_MIN, IPK_MAX = 2.0, 4.0
    GAJI_MIN, GAJI_MAX = 500000, 5000000
    SKOR_MIN, SKOR_MAX = 0, 100

    if ipk < IPK_MIN:
        return {
            "Z": 0, 
            "keterangan": f"Tidak Layak (IPK < {IPK_MIN})"
        }
    
    if gaji >= GAJI_MAX:
        return {
            "Z": 0, 
            "keterangan": "Tidak Layak (Penghasilan >= 5.000.000)"
        }

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

    if total_alpha > 0:
        skor_z = total_alpha_z / total_alpha
        skor_z = round(skor_z, 2)
    else:
        skor_z = 0

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