import tkinter as tk
from tkinter import messagebox, ttk
from typing import List
from datetime import datetime, timedelta
import random

# ===================== Uçuş Sınıfı =====================
class Ucus:
    def __init__(self, ucus_id: str, kalkis: str, varis: str, toplam_koltuk: int, rezerve_edilen_koltuk: int,
                 ucus_saati: str, gidis_tarihi: str, donus_tarihi: str, bilet_fiyati: float, ucus_sinifi: str):
        self.ucus_id = ucus_id
        self.kalkis = kalkis
        self.varis = varis
        self.toplam_koltuk = toplam_koltuk
        self.rezerve_edilen_koltuk = rezerve_edilen_koltuk
        self.ucus_saati = ucus_saati
        self.gidis_tarihi = gidis_tarihi
        self.donus_tarihi = donus_tarihi
        self.bilet_fiyati = bilet_fiyati
        self.ucus_sinifi = ucus_sinifi

    def mevcut_koltuk(self) -> int:
        return self.toplam_koltuk - self.rezerve_edilen_koltuk

    def koltuk_rezervasyonu_yap(self, kisi_sayisi: int) -> bool:
        if self.mevcut_koltuk() >= kisi_sayisi:
            self.rezerve_edilen_koltuk += kisi_sayisi
            return True
        return False

    def toplam_fiyat(self, kisi_sayisi: int, sigorta: bool = False, bagaj_kg: int = 0) -> float:
        toplam = self.bilet_fiyati * kisi_sayisi
        if sigorta:
            toplam += 100 * kisi_sayisi
        if bagaj_kg > 0:
            toplam += 50 * bagaj_kg
        return toplam

# ================= Rezervasyon Sınıfı =================
class Rezervasyon:
    def __init__(self, yolcu_adi: str, ucus_id: str, koltuk_numarasi: str, kisi_sayisi: int,
                 toplam_fiyat: float, sigorta: bool, bagaj_kg: int):
        self.yolcu_adi = yolcu_adi
        self.ucus_id = ucus_id
        self.koltuk_numarasi = koltuk_numarasi
        self.kisi_sayisi = kisi_sayisi
        self.toplam_fiyat = toplam_fiyat
        self.sigorta = sigorta
        self.bagaj_kg = bagaj_kg

# ================== Diğer Yardımcı Fonksiyonlar ===================
def rastgele_tarih(baslangic_tarihi: datetime, gun_araligi: int) -> str:
    rastgele_gun = random.randint(0, gun_araligi)
    tarih = baslangic_tarihi + timedelta(days=rastgele_gun)
    return tarih.strftime("%Y-%m-%d")

def rastgele_saat() -> str:
    saat = random.randint(0, 23)
    dakika = random.randint(0, 59)
    return f"{saat:02d}:{dakika:02d}"

def rastgele_ucus_id() -> str:
    return f"{random.choice(['TK', 'LH', 'AF', 'BA', 'KL'])}{random.randint(100, 999)}"

def rastgele_sinif() -> str:
    return random.choice(["Economy", "Business", "First Class"])

def rastgele_fiyat(sinif: str) -> float:
    if sinif == "Economy": return round(random.uniform(300, 1200), 2)
    elif sinif == "Business": return round(random.uniform(1000, 3000), 2)
    else: return round(random.uniform(2500, 6000), 2)

# ================== Uçuş Verileri ===================
sehirler = ["İstanbul", "Ankara", "İzmir", "Antalya", "Adana", "Bursa", "Trabzon", "Diyarbakır", "Eskişehir", "Konya",
    "Zonguldak", "Selanik", "Londra", "Paris", "Berlin", "Roma", "Amsterdam", "Brüksel", "Viyana", "Madrid",
    "Barselona", "Moskova", "New York", "Los Angeles", "Chicago", "Miami", "San Francisco", "Toronto", "Montreal",
    "Pekin", "Şanghay", "Tokyo", "Dubai", "Doha", "Singapur", "Bangkok", "Sidney", "Melbourne", "Cape Town",
    "Kahire", "Riyad", "Kuala Lumpur", "Stockholm", "Kopenhag", "Oslo", "Helsinki", "Zürih", "Cenevre", "Dublin",
    "Lizbon", "Atina", "Budapeşte"]

ucuslar: List[Ucus] = []
baslangic_tarihi = datetime(2025, 6, 1)

for _ in range(100):
    kalkis = random.choice(sehirler)
    varis = random.choice([s for s in sehirler if s != kalkis])
    gidis_tarihi = rastgele_tarih(baslangic_tarihi, 60)
    donus_tarihi = (datetime.strptime(gidis_tarihi, "%Y-%m-%d") + timedelta(days=random.randint(2, 30))).strftime("%Y-%m-%d")
    ucuslar.append(Ucus(
        ucus_id=rastgele_ucus_id(), kalkis=kalkis, varis=varis,
        toplam_koltuk=random.randint(80, 250),
        rezerve_edilen_koltuk=random.randint(0, 70),
        ucus_saati=rastgele_saat(), gidis_tarihi=gidis_tarihi,
        donus_tarihi=donus_tarihi,
        bilet_fiyati=rastgele_fiyat(rastgele_sinif()), ucus_sinifi=rastgele_sinif()
    ))

rezervasyonlar: List[Rezervasyon] = []
# Tkinter GUI için Uçuşları listeleme
def ucuslari_listele_gui():
    ucus_listesi.delete(0, tk.END)
    for ucus in ucuslar:
        ucus_listesi.insert(tk.END, f"{ucus.ucus_id} | {ucus.kalkis} - {ucus.varis} | {ucus.gidis_tarihi} - {ucus.donus_tarihi} | {ucus.ucus_saati} | {ucus.mevcut_koltuk()} boş koltuk | ₺{ucus.bilet_fiyati} | {ucus.ucus_sinifi}")

# Örnek bir Tkinter penceresi (isteğe bağlı)
if __name__ == "__main__":
    pencere = tk.Tk()
    pencere.title("Uçuş Listesi")

    ucus_listesi = tk.Listbox(pencere, width=100)
    ucus_listesi.pack(pady=10)

    ucuslari_listele_gui()

    pencere.mainloop()# Rezervasyon yapma işlemi
def ucus_rezervasyonu_gui():
    ucus_id = ucus_id_girdi.get()
    yolcu_adi = ad_soyad_girdi.get()
    koltuk_numarasi = koltuk_numarasi_girdi.get()
    kisi_sayisi_str = kisi_sayisi_spinbox.get()
    try:
        kisi_sayisi = int(kisi_sayisi_str)
    except ValueError:
        messagebox.showerror("Hata", "Geçersiz kişi sayısı.")
        return
    sigorta = sigorta_var.get()
    bagaj_kg_str = bagaj_kg_spinbox.get()
    try:
        bagaj_kg = int(bagaj_kg_str)
    except ValueError:
        messagebox.showerror("Hata", "Geçersiz bagaj kilogramı.")
        return

    if not ucus_id or not yolcu_adi or not koltuk_numarasi or kisi_sayisi <= 0:
        messagebox.showerror("Hata", "Lütfen tüm alanları doğru şekilde doldurun.")
        return

    ucus = next((u for u in ucuslar if u.ucus_id == ucus_id), None)
    if not ucus:
        messagebox.showerror("Hata", "Geçersiz uçuş ID'si.")
        return

    if ucus.mevcut_koltuk() < kisi_sayisi:
        messagebox.showerror("Hata", "Yeterli boş koltuk bulunmamaktadır.")
        return

    if ucus.koltuk_rezervasyonu_yap(kisi_sayisi):
        toplam_fiyat = ucus.toplam_fiyat(kisi_sayisi, sigorta, bagaj_kg)
        rezervasyon = Rezervasyon(yolcu_adi, ucus_id, koltuk_numarasi, kisi_sayisi, toplam_fiyat, sigorta, bagaj_kg)
        rezervasyonlar.append(rezervasyon)
        messagebox.showinfo("Başarılı", f"{yolcu_adi} için {kisi_sayisi} kişilik rezervasyon başarıyla yapıldı. Toplam Tutar: ₺{toplam_fiyat}")
        ucuslari_listele_gui()
    else:
        messagebox.showerror("Hata", "Koltuk rezerve edilemedi.")

# Rezervasyonları gösterme fonksiyonu
def rezervasyonlari_goster():
    rezervasyonlar_ekran = tk.Toplevel(root)
    rezervasyonlar_ekran.title("Yapılan Rezervasyonlar")
    rezervasyonlar_ekran.geometry("800x400")

    tree = ttk.Treeview(rezervasyonlar_ekran, columns=("Yolcu Adı", "Uçuş ID", "Koltuk", "Kişi Sayısı", "Toplam Fiyat", "Sigorta", "Bagaj (kg)"), show='headings')

    tree.heading("Yolcu Adı", text="Yolcu Adı")
    tree.heading("Uçuş ID", text="Uçuş ID")
    tree.heading("Koltuk", text="Koltuk")
    tree.heading("Kişi Sayısı", text="Kişi Sayısı")
    tree.heading("Toplam Fiyat", text="Toplam Fiyat")
    tree.heading("Sigorta", text="Sigorta")
    tree.heading("Bagaj (kg)", text="Bagaj (kg)")

    for rezervasyon in rezervasyonlar:
        tree.insert("", tk.END, values=(rezervasyon.yolcu_adi, rezervasyon.ucus_id, rezervasyon.koltuk_numarasi, rezervasyon.kisi_sayisi, f"₺{rezervasyon.toplam_fiyat}", "Evet" if rezervasyon.sigorta else "Hayır", rezervasyon.bagaj_kg))

    tree.pack(expand=True, fill='both', padx=10, pady=10)

# Uçuş arama fonksiyonu (basit bir örnek)
def ucus_ara():
    kalkis = kalkis_girdi.get().strip().lower()
    varis = varis_girdi.get().strip().lower()
    tarih_str = gidis_tarihi_girdi.get().strip()

    try:
        aranan_tarih = datetime.strptime(tarih_str, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Hata", "Lütfen geçerli bir gidiş tarihi giriniz. (Format: YYYY-AA-GG)")
        return

    sonuclar = []
    for ucus in ucuslar:
        try:
            ucus_tarihi = datetime.strptime(ucus.gidis_tarihi, "%Y-%m-%d")
            tarih_farki = abs((ucus_tarihi - aranan_tarih).days)
            if (
                kalkis in ucus.kalkis.lower()
                and varis in ucus.varis.lower()
                and tarih_farki <= 1  # ±1 gün esneklik
            ):
                sonuclar.append(ucus)
        except Exception as e:
            continue

    ucus_listesi.delete(0, tk.END)
    if sonuclar:
        for ucus in sonuclar:
            ucus_listesi.insert(tk.END, f"{ucus.ucus_id} | {ucus.kalkis} - {ucus.varis} | {ucus.gidis_tarihi} - {ucus.donus_tarihi} | {ucus.ucus_saati} | {ucus.mevcut_koltuk()} boş koltuk | ₺{ucus.bilet_fiyati} bilet fiyatı | {ucus.ucus_sinifi}")
    else:
        ucus_listesi.insert(tk.END, "Aradığınız kritere ±1 gün içinde uygun uçuş bulunamadı.")

# Menü tasarımına yönelik değişkenler ve fonksiyonlar
def tek_yon_sec():
    donus_tarihi_label.grid_forget()
    donus_tarihi_girdi.grid_forget()

def gidis_donus_sec():
    donus_tarihi_label.grid(row=3, column=1, sticky="ew", padx=5, pady=5)
    donus_tarihi_girdi.grid(row=3, column=2, sticky="ew", padx=5, pady=5)

def coklu_yon_sec():
    messagebox.showinfo("Bilgi", "Çoklu yön seçeneği henüz desteklenmemektedir.")

# Tkinter arayüzü
root = tk.Tk()
root.title("Uçuş Rezervasyon Sistemi")
root.geometry("800x900")
root.configure(bg="#f0f0f0") # Daha açık bir arka plan

# Fontlar ve Renkler
ana_font = ("Segoe UI", 10)
baslik_font = ("Segoe UI", 12, "bold")
ana_renk = "#0079d6" # THY mavisine yakın
acik_renk = "#e3f2fd"
vurgu_renk = "#ff9800" # Turuncu tonları

# Logo (isteğe bağlı, bir resim dosyası gerektirir)
# try:
#     logo_img = Image.open("thy_logo.png")
#     logo_img = logo_img.resize((150, 50), Image.Resampling.LANCZOS)
#     logo_photo = ImageTk.PhotoImage(logo_img)
#     logo_label = tk.Label(root, image=logo_photo, bg=root["bg"])
#     logo_label.pack(pady=10)
# except FileNotFoundError:
#     logo_label = tk.Label(root, text="Türk Hava Yolları", font=("Segoe UI", 16, "bold"), bg=root["bg"], fg=ana_renk)
#     logo_label.pack(pady=10)

# Menü Butonları Çerçevesi
menu_frame = tk.Frame(root, bg=root["bg"])
menu_frame.pack(pady=10)

tek_yon_button = tk.Button(menu_frame, text="Tek Yön", command=tek_yon_sec, bg=acik_renk, fg=ana_renk, font=ana_font, bd=2, relief=tk.RAISED)
tek_yon_button.pack(side=tk.LEFT, padx=5)

gidis_donus_button = tk.Button(menu_frame, text="Gidiş-Dönüş", command=gidis_donus_sec, bg=acik_renk, fg=ana_renk, font=ana_font, bd=2, relief=tk.RAISED)
gidis_donus_button.pack(side=tk.LEFT, padx=5)

coklu_yon_button = tk.Button(menu_frame, text="Çoklu Uçuş", command=coklu_yon_sec, bg=acik_renk, fg=ana_renk, font=ana_font, bd=2, relief=tk.RAISED)
coklu_yon_button.pack(side=tk.LEFT, padx=5)

# Arama Kriterleri Çerçevesi
arama_frame = tk.LabelFrame(root, text="Uçuş Ara", font=baslik_font, bg=root["bg"], padx=10, pady=10)
arama_frame.pack(pady=10, padx=20, fill="x")

tk.Label(arama_frame, text="Kalkış:", font=ana_font, bg=root["bg"]).grid(row=0, column=0, sticky="w", padx=5, pady=5)
kalkis_girdi = tk.Entry(arama_frame, font=ana_font)
kalkis_girdi.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

tk.Label(arama_frame, text="Varış:", font=ana_font, bg=root["bg"]).grid(row=1, column=0, sticky="w", padx=5, pady=5)
varis_girdi = tk.Entry(arama_frame, font=ana_font)
varis_girdi.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

tk.Label(arama_frame, text="Gidiş Tarihi (YYYY-AA-GG):", font=ana_font, bg=root["bg"]).grid(row=2, column=0, sticky="w", padx=5, pady=5)
gidis_tarihi_girdi = tk.Entry(arama_frame, font=ana_font)
gidis_tarihi_girdi.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

donus_tarihi_label = tk.Label(arama_frame, text="Dönüş Tarihi (YYYY-AA-GG):", font=ana_font, bg=root["bg"])
donus_tarihi_girdi = tk.Entry(arama_frame, font=ana_font)

ucus_ara_button = tk.Button(arama_frame, text="Uçuş Ara", command=ucus_ara, bg=ana_renk, fg="white", font=baslik_font, bd=2, relief=tk.RAISED)
ucus_ara_button.grid(row=4, column=0, columnspan=2, pady=10, sticky="ew")

arama_frame.columnconfigure(1, weight=1)
                            # Uçuşlar Listesi Çerçevesi
ucus_listesi_frame = tk.LabelFrame(root, text="Mevcut Uçuşlar", font=baslik_font, bg=root["bg"], padx=10, pady=10)
ucus_listesi_frame.pack(pady=10, padx=20, fill="both", expand=True)

ucus_listesi = tk.Listbox(ucus_listesi_frame, width=100, height=10, font=ana_font)
ucus_listesi.pack(fill="both", expand=True)

# Rezervasyon Yapma Çerçevesi
rezervasyon_frame = tk.LabelFrame(root, text="Rezervasyon Yap", font=baslik_font, bg=root["bg"], padx=10, pady=10)
rezervasyon_frame.pack(pady=10, padx=20, fill="x")

tk.Label(rezervasyon_frame, text="Ad Soyad:", font=ana_font, bg=root["bg"]).grid(row=0, column=0, sticky="w", padx=5, pady=5)
ad_soyad_girdi = tk.Entry(rezervasyon_frame, font=ana_font)
ad_soyad_girdi.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

tk.Label(rezervasyon_frame, text="Uçuş ID:", font=ana_font, bg=root["bg"]).grid(row=1, column=0, sticky="w", padx=5, pady=5)
ucus_id_girdi = tk.Entry(rezervasyon_frame, font=ana_font)
ucus_id_girdi.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

tk.Label(rezervasyon_frame, text="Koltuk Numarası:", font=ana_font, bg=root["bg"]).grid(row=2, column=0, sticky="w", padx=5, pady=5)
koltuk_numarasi_girdi = tk.Entry(rezervasyon_frame, font=ana_font)
koltuk_numarasi_girdi.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

tk.Label(rezervasyon_frame, text="Kişi Sayısı:", font=ana_font, bg=root["bg"]).grid(row=3, column=0, sticky="w", padx=5, pady=5)
kisi_sayisi_spinbox = tk.Spinbox(rezervasyon_frame, from_=1, to=10, font=ana_font)
kisi_sayisi_spinbox.grid(row=3, column=1, sticky="ew", padx=5, pady=5)

tk.Label(rezervasyon_frame, text="Bagaj Kilogramı:", font=ana_font, bg=root["bg"]).grid(row=4, column=0, sticky="w", padx=5, pady=5)
bagaj_kg_spinbox = tk.Spinbox(rezervasyon_frame, from_=0, to=50, font=ana_font)
bagaj_kg_spinbox.grid(row=4, column=1, sticky="ew", padx=5, pady=5)

sigorta_var = tk.BooleanVar()
sigorta_check = tk.Checkbutton(rezervasyon_frame, text="Seyahat Sigortası Ekle", variable=sigorta_var, font=ana_font, bg=root["bg"])
sigorta_check.grid(row=5, column=0, columnspan=2, sticky="w", padx=5, pady=5)

rezervasyon_buton = tk.Button(rezervasyon_frame, text="Rezervasyonu Tamamla", command=ucus_rezervasyonu_gui, bg=vurgu_renk, fg="white", font=baslik_font, bd=2, relief=tk.RAISED)
rezervasyon_buton.grid(row=6, column=0, columnspan=2, pady=10, sticky="ew")

rezervasyon_frame.columnconfigure(1, weight=1) # Entry widget'larının genişlemesi için

# Rezervasyonları Göster Butonu
rezervasyonlar_buton = tk.Button(root, text="Rezervasyonları Görüntüle", command=rezervasyonlari_goster, bg="#66bb6a", fg="white", font=baslik_font, bd=2, relief=tk.RAISED)
rezervasyonlar_buton.pack(pady=10, padx=20, fill="x")

# Başlangıçta sadece gidiş-dönüş alanlarını göster
tek_yon_sec()
gidis_donus_sec() # Varsayılan olarak gidiş-dönüş seçili olabilir

# Uçuşları listele ve göster
ucuslari_listele_gui()

root.mainloop()