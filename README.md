# Sosyal Günlük Platformu

Modern ve sade tasarımlı sosyal günlük platformu. Kullanıcılar günlük yazılarını paylaşabilir, fotoğraflar ekleyebilir ve arkadaşlarının hikayelerini takip edebilir.

## Özellikler

### 🔐 Kullanıcı Yönetimi
- Kullanıcı kaydı ve girişi
- Profil yönetimi (biyografi, profil fotoğrafı)
- Takip sistemi (arkadaşları takip etme/takibi bırakma)

### 📝 Günlük Girişleri
- Metin tabanlı günlük yazıları
- Her günlük için en fazla 3 fotoğraf yükleme
- Gizlilik kontrolü: "Sadece Ben" / "Herkes"
- Günlük girişlerini silme

### 🏠 Ana Sayfa (Feed)
- Takip edilen kişilerin herkese açık günlüklerinin kronolojik akışı
- Sayfalama ile performanslı görüntüleme
- Fotoğraf galerisi ile modal görüntüleme

### 👤 Profil Sayfası
- Liste görünümü: Tüm günlük girişleri
- Takvim görünümü: Günlük girişleri tarihe göre gruplandırılmış
- Takipçi/takip edilen sayıları
- Kendi profilinde düzenleme ve silme seçenekleri

## Teknoloji Stack

- **Backend:** Django 4.2.7
- **Frontend:** Bootstrap 5.3, Font Awesome 6.0
- **Veritabanı:** SQLite (geliştirme için)
- **Medya Yönetimi:** Pillow
- **Stil:** Custom CSS ile modern tasarım

## Kurulum

### Gereksinimler
- Python 3.8+
- pip

### Adımlar

1. **Projeyi klonlayın:**
   ```bash
   git clone <repository-url>
   cd günlük
   ```

2. **Virtual environment oluşturun:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   # veya
   venv\Scripts\activate     # Windows
   ```

3. **Bağımlılıkları yükleyin:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Veritabanı migration'larını çalıştırın:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Superuser oluşturun:**
   ```bash
   python manage.py createsuperuser
   ```

6. **Development server'ı başlatın:**
   ```bash
   python manage.py runserver
   ```

7. **Tarayıcıda açın:**
   http://127.0.0.1:8000

## Kullanım

### İlk Kullanım
1. Ana sayfada "Hemen Başla" butonuna tıklayın
2. Kullanıcı kaydı oluşturun
3. Giriş yapın ve profilinizi düzenleyin
4. İlk günlük girişinizi oluşturun

### Günlük Oluşturma
1. "Yaz" butonuna tıklayın
2. Başlık (opsiyonel) ve içerik yazın
3. İsteğe bağlı olarak 1-3 fotoğraf ekleyin
4. Gizlilik ayarını seçin
5. "Günlüğü Kaydet" butonuna tıklayın

### Arkadaş Takibi
1. Başka kullanıcıların profillerine gidin
2. "Takip Et" butonuna tıklayın
3. Ana sayfada takip ettiğiniz kişilerin herkese açık günlüklerini görün

## Proje Yapısı

```
günlük/
├── diary/                  # Ana uygulama
│   ├── models.py          # Veritabanı modelleri
│   ├── views.py           # View fonksiyonları
│   ├── forms.py           # Django formları
│   ├── admin.py           # Admin panel konfigürasyonu
│   ├── urls.py            # URL yönlendirmeleri
│   └── templates/         # HTML şablonları
├── social_diary/          # Proje ayarları
│   ├── settings.py        # Django ayarları
│   └── urls.py            # Ana URL konfigürasyonu
├── static/                # Statik dosyalar
│   ├── css/style.css      # Custom CSS
│   └── js/main.js         # JavaScript
├── media/                 # Yüklenen medya dosyaları
├── requirements.txt       # Python bağımlılıkları
└── README.md             # Bu dosya
```

## Özellik Detayları

### Gizlilik Kontrolü
- **Sadece Ben:** Sadece günlük sahibi görebilir
- **Herkes:** Tüm kullanıcılar görebilir (ana sayfada görünür)

### Fotoğraf Yükleme
- Desteklenen formatlar: JPEG, PNG
- Maksimum 3 fotoğraf per günlük
- Otomatik boyutlandırma ve optimizasyon
- Modal ile büyük görüntüleme

### Responsive Tasarım
- Mobil uyumlu arayüz
- Bootstrap 5 grid sistemi
- Touch-friendly etkileşimler

## Güvenlik

- CSRF koruması
- Kullanıcı kimlik doğrulaması
- Medya dosyaları için güvenli yükleme
- XSS koruması

## Geliştirme

### Yeni Özellik Ekleme
1. Model değişiklikleri için `models.py` düzenleyin
2. Migration oluşturun: `python manage.py makemigrations`
3. Migration'ı uygulayın: `python manage.py migrate`
4. View ve template'leri güncelleyin

### Debug Modu
Development ortamında `DEBUG = True` ayarı aktiftir. Production'da `False` yapın.

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit edin (`git commit -m 'Add amazing feature'`)
4. Push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## İletişim

Herhangi bir sorunuz veya öneriniz için issue oluşturabilirsiniz.

---

**Not:** Bu platform eğitim amaçlı geliştirilmiştir. Production kullanımı için ek güvenlik önlemleri alınmalıdır.
