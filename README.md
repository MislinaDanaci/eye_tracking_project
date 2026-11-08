# Cognitive Load & Gaze-Tracking Analytics Tool

Bu proje, akademik metin okuma süreçlerindeki bilişsel yükü ve odaklanma performansını ölçmek amacıyla geliştirilmiş, donanım bağımsız bir göz takibi (eye-tracking) aracıdır.

Proje, okuyucunun ekrandaki etkileşimini MediaPipe ve OpenCV kütüphaneleri aracılığıyla gerçek zamanlı olarak izler. Ekranı dörde bölen basit bir okuma arayüzü yerine, sistemin odak noktası metin üzerindeki göz hareketlerinin verisel analizidir. NLTK (Natural Language Toolkit) kullanılarak bölümlendirilen metinler üzerinde okuyucunun hangi bölüme ne kadar süre odaklandığı ölçülür.

Amacımız, pahalı donanımlara ihtiyaç duymadan standart web kameraları ile erişilebilir bir odak analizi altyapısı sunmaktır.

## Temel Özellikler

* **Gerçek Zamanlı Göz Takibi:** MediaPipe Face Mesh algoritması ile kullanıcının göz bebeği koordinatları hassas bir şekilde tespit edilir.
* **Donanım Bağımsız Çalışma:** Özel bir eye-tracking cihazına gerek duymadan standart dizüstü veya masaüstü bilgisayar kameraları ile çalışır.
* **Bölgesel Odak Analizi:** Ekran mantıksal quadrantlara bölünür ve kullanıcının bakış yönüne göre anlık odaklanma alanı tespit edilir.
* **NLTK Tabanlı Metin Yapılandırma:** Girdi olarak alınan akademik metinler, NLTK kütüphanesi ile yapısal bütünlüğü korunarak analiz için hazır hale getirilir.
* **Düşük Sistem Gereksinimi:** API bağımlılığı olmadan, yerel makinede (offline) çalışacak şekilde optimize edilmiştir.

## Kullanılan Teknolojiler

* **Python 3.11:** Çekirdek programlama dili.
* **OpenCV (cv2):** Görüntü işleme, kamera yakalama ve görsel arayüz oluşturma.
* **MediaPipe:** Yüz ve göz işaretçilerinin (landmarks) biyometrik tespiti.
* **NLTK:** Metin ayrıştırma ve dil işleme.
* **Tkinter:** Kullanıcıdan metin girdisi almak için hafif arayüz tasarımı.

## Kurulum ve Çalıştırma

Projenin bağımlılıklarını izole bir ortamda kurmanız önerilir.

1. Depoyu bilgisayarınıza klonlayın:
   `git clone https://github.com/kullaniciadi/proje-adi.git`

2. Proje dizinine gidin:
   `cd proje-adi`

3. Gerekli kütüphaneleri yükleyin:
   `pip install opencv-python mediapipe nltk`

4. Uygulamayı başlatın:
   `python proje_dosyasi.py` 

## Geliştirme Yol Haritası

Mevcut sürüm temel bir prototip olup aşağıdaki geliştirmeler planlanmaktadır:

* Odaklanma sürelerinin milisaniye cinsinden loglanması ve veri analizi için CSV formatında dışa aktarılması.
* Göz kırpma hızına (blink rate) bağlı olarak "Bilişsel Yorgunluk" (Cognitive Fatigue) tahmini yapan algoritmaların entegrasyonu.
* Okuma hızını (WPM - Words Per Minute) ölçen dinamik metin kaydırma mekanizması.

## Akademik Özgün Değer

Bu çalışma, donanım tabanlı göz takibi sistemlerinin yüksek maliyetine karşı yazılım tabanlı, açık kaynaklı bir alternatif sunmaktadır. Biyometrik verilerin metin analizi ile birleştirilmesi, uzaktan eğitim sistemlerinde ve akademik araştırmalarda öğrencilerin odaklanma sürelerinin ölçümlenmesi için erişilebilir bir veri sağlama potansiyeli taşır.
