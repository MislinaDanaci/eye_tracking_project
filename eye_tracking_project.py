import tkinter as tk
import cv2
import mediapipe as mp
import nltk
import textwrap

# NLTK paketlerini güvenli şekilde indirme (İnternet sorunu yaşanırsa çökmemesi için)
try:
    nltk.download('punkt', quiet=True)
except:
    pass

alinan_makale = ""
bolunmus_metinler = []

# --- 1. NLTK METİN ANALİZİ (YAPAY ZEKA ALTERNATİFİ) ---
def turkce_karakter_temizle(metin):
    # OpenCV ekrana yazı yazarken Türkçe harfleri bozar, bunu önlüyoruz.
    return metin.translate(str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU"))

def metni_analiz_et_ve_bol(metin):
    metin = turkce_karakter_temizle(metin)
    
    # NLTK ile metni cümle cümle ayır (NLTK hata verirse standart yolla ayır)
    try:
        from nltk.tokenize import sent_tokenize
        cumleler = sent_tokenize(metin)
    except:
        cumleler = metin.split(". ")
        
    # Boş veya çok kısa olanları filtrele
    cumleler = [c.strip() for c in cumleler if len(c) > 15]
    
    # Metin çok kısaysa boşlukları doldur
    if len(cumleler) < 4:
        cumleler += ["Metin baska cumle icermiyor."] * (4 - len(cumleler))
        
    # Metnin akışına göre kronolojik olarak 4 temsilci cümle seç (Giriş, Orta, Orta-Son, Son)
    bolum1 = "1. GIRIS: " + cumleler[0]
    bolum2 = "2. LITERATUR: " + cumleler[len(cumleler) // 3]
    bolum3 = "3. METOD: " + cumleler[(len(cumleler) * 2) // 3]
    bolum4 = "4. SONUC: " + cumleler[-1]
    
    return [bolum1, bolum2, bolum3, bolum4]

# --- 2. KULLANICI ARAYÜZÜ (GİRDİ ALMA) ---
def metni_al_ve_basla():
    global alinan_makale, bolunmus_metinler
    alinan_makale = text_kutusu.get("1.0", tk.END).strip()
    
    if len(alinan_makale) > 50:
        print("NLTK metni analiz ediyor...")
        bolunmus_metinler = metni_analiz_et_ve_bol(alinan_makale)
        print("Analiz bitti! Kamera motoru baslatiliyor...")
        pencere.destroy() # Arayüzü kapat, kameraya geç
    else:
        print("Lütfen daha uzun bir akademik metin girin!")

pencere = tk.Tk()
pencere.title("NLTK Tabanlı Akıllı Okuma Asistanı")
pencere.geometry("500x400")

tk.Label(pencere, text="Lütfen akademik makaleyi aşağıya yapıştırın:", font=("Arial", 12)).pack(pady=10)
text_kutusu = tk.Text(pencere, height=15, width=55, font=("Arial", 10))
text_kutusu.pack(pady=10)
tk.Button(pencere, text="NLTK Analizini Başlat", bg="green", fg="white", font=("Arial", 12, "bold"), command=metni_al_ve_basla).pack(pady=10)

pencere.mainloop()


# --- 3. GÖZ TAKİBİ VE DİNAMİK EKRAN (OPENCV) ---
if len(bolunmus_metinler) == 4:
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)
    cap = cv2.VideoCapture(0)

    # Ekrana uzun cümleleri sığdırmak için yardımcı fonksiyon (Yazıları alt satıra atar)
    def yaziyi_ekrana_sigdir(img, metin, x, y, max_karakter=45):
        satirlar = textwrap.wrap(metin, width=max_karakter)
        for i, satir in enumerate(satirlar):
            cv2.putText(img, satir, (x, y + (i * 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue

        image = cv2.flip(image, 1)
        h, w, _ = image.shape
        
        # Ekranı bölen rehber çizgiler
        cv2.line(image, (w//2, 0), (w//2, h), (100, 100, 100), 2)
        cv2.line(image, (0, h//2), (w, h//2), (100, 100, 100), 2)

        # NLTK'nın böldüğü 4 cümleyi 4 farklı kareye (odaya) yazdırıyoruz
        yaziyi_ekrana_sigdir(image, bolunmus_metinler[0], 10, 30)                # Sol Üst
        yaziyi_ekrana_sigdir(image, bolunmus_metinler[1], w//2 + 10, 30)         # Sağ Üst
        yaziyi_ekrana_sigdir(image, bolunmus_metinler[2], 10, h//2 + 30)         # Sol Alt
        yaziyi_ekrana_sigdir(image, bolunmus_metinler[3], w//2 + 10, h//2 + 30)  # Sağ Alt

        # Göz ve Yüz Takibi
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(image_rgb)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                left_eye_x = int(face_landmarks.landmark[473].x * w)
                left_eye_y = int(face_landmarks.landmark[473].y * h)
                right_eye_x = int(face_landmarks.landmark[468].x * w)
                right_eye_y = int(face_landmarks.landmark[468].y * h)
                
                cv2.circle(image, (left_eye_x, left_eye_y), 4, (0, 255, 0), -1)
                cv2.circle(image, (right_eye_x, right_eye_y), 4, (0, 255, 0), -1)

                avg_x = (left_eye_x + right_eye_x) // 2
                avg_y = (left_eye_y + right_eye_y) // 2

                # Göz bebeği hangi koordinatta ise sadece o bölgeye "-> OKUNUYOR" yaz
                if avg_x < w//2 and avg_y < h//2:
                    cv2.putText(image, "-> OKUNUYOR", (10, h//2 - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                elif avg_x >= w//2 and avg_y < h//2:
                    cv2.putText(image, "-> OKUNUYOR", (w//2 + 10, h//2 - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                elif avg_x < w//2 and avg_y >= h//2:
                    cv2.putText(image, "-> OKUNUYOR", (10, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                else:
                    cv2.putText(image, "-> OKUNUYOR", (w//2 + 10, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        cv2.imshow('NLTK ve Goz Takibi Akademik Arayuzu', image)

        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
