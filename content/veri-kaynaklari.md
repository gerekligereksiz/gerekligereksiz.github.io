---
title: "Veri Kaynakları"
description: "Portalda otomatik güncellenen verilerin kaynağı, güncellenme sıklığı ve doğrulama kuralları."
date: 2026-10-21T12:00:00+03:00
---

Bu portaldeki bazı veriler elle değil, otomatik olarak güncellenir. Hangi verinin nereden geldiğini ve ne sıklıkla yenilendiğini buradan takip edebilirsiniz.

## Baraj doluluk verileri

Türkiye'deki barajların doluluk oranları, ilgili kurumun açıkladığı verilerden alınır.

| | |
|---|---|
| **Kaynak** | *TODO: kaynak — resmî kurum adı ve açık veri adresi belirlenip yazılmalıdır.* |
| **Güncellenme** | Günde 1 kez, otomatik |
| **Kapsam** | İstanbul, Ankara, İzmir, Bursa |
| **Son güncelleme** | Her baraj sayfasında ayrıca gösterilir |

*TODO: kaynak — veri akışı henüz devrede değildir. `scripts/` ve `.github/workflows/update-data.yml` eklendiğinde bu tablo kesinleştirilmelidir.*

### Veri kalitesi kuralları

Otomatik veri çekmenin en büyük riski, kaynağındaki geçici bir sorunun siteye yanlış veri olarak yansımasıdır. Bunu önlemek için şu kurallar uygulanır:

**Hata durumunda eski veri korunur.** Çekme başarısız olursa, veri boş gelirse ya da bir oran 0-100 aralığının dışında çıkarsa, mevcut veri dosyası **ezilmez**. Sayfa son bilinen doğru değeri göstermeye devam eder.

**Anormal sapma işaretlenir.** Bir önceki değere göre tek günde 15 puandan fazla değişim varsa, bu durum şüpheli sayılır ve otomatik olarak yayımlanmaz.

**Kaynak ve zaman her zaman görünür.** Her veri kaydı, hangi kurumdan geldiğini ve tam olarak ne zaman güncellendiğini taşır. Sayfada ikisi de gösterilir.

**Kaynağa yük olunmaz.** İstekler arasında bekleme uygulanır, tanımlayıcı bir `User-Agent` gönderilir ve günde 1-2 isteğin ötesine geçilmez.

**Var olan veri uydurulmaz.** Kaynağı gösterilemeyen bir değer yayımlanmaz.

## Elle hazırlanan veriler

Aşağıdaki içerikler otomatik değil, elle hazırlanır:

- **Sporcu ve takım maç haberleri** — her kayıt tek bir maçı ya da turnuvayı anlatır ve en az bir kaynak bağlantısı taşır. Kaynağı belirtilemeyen skor, istatistik veya tarih yazılmaz; bilinmeyen alan boş bırakılır. Takım bilgisi sporcu profilinde değil, yalnızca maç kaydında tutulur.
- **Uygulama kataloğu** — uygulamalar denenip elle eklenir.
- **Yazılar ve bülten** — elle yazılır.

## Veriyle ilgili bir sorun görürseniz

Bir verinin yanlış olduğunu düşünüyorsanız [Bize Ulaşın](/bize-ulasin/) sayfasından bildirebilirsiniz. Otomatik çekilen verilerde hata varsa, düzeltilmesi gereken yer kaynağın kendisidir.

## İlgili sayfalar

- [Gizlilik Politikası](/gizlilik-politikasi/)
- [Kullanım Şartları](/kullanim-sartlari/)
