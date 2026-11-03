---
title: "Strata 1.0 — klavye odaklı Linux dosya yöneticisi"
slug: "strata"
description: "Rust ve GTK4 ile yazılmış, Miller kolonlu ve klavye ağırlıklı bir Linux dosya yöneticisi. 1.0 sürümü ne sunuyor, kime uygun?"
date: 2026-10-18T09:00:00+03:00
lastmod: 2026-10-18T09:00:00+03:00
draft: false
categories: ["Uygulama İncelemesi"]
tags: ["linux", "dosya-yoneticisi", "rust", "gtk4", "acik-kaynak"]
platforms: ["Linux"]
developers: ["lgse"]
version: "1.0"
license: "MIT"
website: "https://github.com/lgse/strata"
download_url: "https://github.com/lgse/strata/releases/tag/v1.0.0"
issue_number: 42
---

{{< bulten-inceleme
    platform="Linux (glibc; x86_64 ve aarch64), Arch/Omarchy öncelikli"
    lisans="MIT (GitHub deposu ve LICENSE dosyası); proje sitesinin altbilgisi ise GPL-3.0-or-later diyor — lisans tutarsızlığı giderilmeli"
    kod="github.com/lgse/strata|https://github.com/lgse/strata"
    kime="Klavye ağırlıklı dosya gezinmeyi seven, Arch/Omarchy tarafında çalışan ve hafif bir yerel dosya yöneticisi arayan Linux kullanıcıları."
    degerlendirme="Terminal alışkanlığı olan Linux kullanıcıları için hızlı ve hafif bir alternatif; ancak 1.0 etiketi olgunluk anlamına gelmiyor, günlük sürücü olarak kullanmadan önce yedek ve test önerilir."
    durum="1.0"
    kaynak="Sürüm notları|https://github.com/lgse/strata/releases/tag/v1.0.0; It’s FOSS|https://itsfoss.com/news/strata-file-manager/" >}}

{{< bulten-artilar >}}
- Rust + GTK4 ile yazılmış yerel uygulama; Miller kolonları, sekmeler, klasör başına hatırlanan sıralama/ikon boyutu ve Space ile zengin önizleme sunuyor.
- SMB/SFTP/GIO/GVfs desteği, arşiv oluşturma/çıkarma, özel aksiyonlar, TOML tema editörü ve 12 dil var.
- Önizlemeler Bubblewrap ile izole ediliyor ve hata durumunda kapalı davranıyor (fail-closed); 100 bin dosyalık testte en düşük tepe belleği kullandığı iddia ediliyor.
{{< /bulten-artilar >}}

{{< bulten-eksiler >}}
- Yalnızca Linux'ta çalışıyor; proje yaklaşık 45 günlük ve çok genç.
- Dosya içeriğinde arama, bağımsız split pane ve gömülü terminal yok.
- Lisans bilgisindeki çelişki kurumsal kullanım öncesi netleştirilmeli.
{{< /bulten-eksiler >}}
{{< /bulten-inceleme >}}
