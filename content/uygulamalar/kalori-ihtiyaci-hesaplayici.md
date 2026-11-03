---
title: "Kalori ihtiyacı hesaplayıcı"
slug: "kalori-ihtiyaci-hesaplayici"
description: "Cinsiyet, yaş, boy, kilo ve hareket seviyesine göre günlük kalori ihtiyacınızı ve makro dağılımınızı hesaplayın."
date: 2026-10-22T10:00:00+03:00
lastmod: 2026-10-22T10:00:00+03:00
draft: false
categories: ["Sağlık & Fitness"]
tags: ["kalori", "beslenme", "fitness", "hesaplayici"]
platforms: ["Web"]
developers: ["Gerekli Gereksiz"]
version: ""
license: "Ücretsiz"
website: ""
download_url: ""
icon: ""
featured: false
layout: kalori-ihtiyaci-hesaplayici
---

## Hesaplama yöntemi ve formüller

Bu hesaplayıcıda **Mifflin-St Jeor** denklemi kullanılır.

### Bazal Metabolizma Hızı (BMR)
- Erkek: `BMR = 10 × kilo (kg) + 6,25 × boy (cm) - 5 × yaş + 5`
- Kadın: `BMR = 10 × kilo (kg) + 6,25 × boy (cm) - 5 × yaş - 161`

### Toplam Günlük Enerji Harcaması (TDEE)
`TDEE = BMR × Aktivite Çarpanı`

| Aktivite Seviyesi | Çarpan |
|---|---|
| Sedanter (hareket etmiyorum / çok az) | 1,2 |
| Az hareketli (hafif aktif / haftada 1-3 gün egzersiz) | 1,375 |
| Orta derece hareketli (aktif / haftada 3-5 gün egzersiz) | 1,55 |
| Çok hareketli (çok aktif / haftada 6-7 gün egzersiz) | 1,725 |
| Aşırı hareketli (profesyonel sporcu / atlet seviyesi) | 1,9 |

### Hedefe Göre Günlük Kalori
| Hedef | Ayarlama |
|---|---|
| Zayıflamak, yağ yakmak | TDEE - 400 kcal |
| Kilo almak (kas kütlesini arttırma, clean bulking) | TDEE + 250 kcal |
| Hızlı kilo almak (yağ oranınız artabilir, dirty bulking) | TDEE + 500 kcal |
| Kilomu korumak | TDEE |

*(Hesaplanan hedef kalori 1200 kcal'in altına düşerse 1200 kcal olarak sınırlandırılır.)*

### Makro Dağılımı
- **Protein:** `kilo (kg) × 1,8 g` (7,2 kcal/g)
- **Yağ:** `kilo (kg) × 0,9 g` (9 kcal/g)
- **Karbonhidrat:** Kalan kalori `(hedef kcal - protein kcal - yağ kcal)` ÷ 4 g (4 kcal/g)
