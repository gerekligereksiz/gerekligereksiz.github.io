---
title: "ElixirOffice beta — Microsoft Office alışkanlığına hedeflenen açık kaynak ofis paketi"
slug: "elixiroffice"
description: "Euro-Office/ONLYOFFICE bileşenleri üzerine kurulu, çevrimdışı çalışan ve arayüzü Microsoft Office'e benzeyen açık kaynak ofis paketi. Beta ne kadar güvenilir?"
date: 2026-10-18T09:00:00+03:00
lastmod: 2026-10-18T09:00:00+03:00
draft: false
categories: ["Uygulama İncelemesi"]
tags: ["ofis-paketi", "linux", "windows", "macos", "acik-kaynak", "agpl"]
platforms: ["Linux", "Windows", "macOS"]
developers: ["leag1234"]
version: "0.2.0-beta"
license: "AGPL-3.0"
website: "https://github.com/leag1234/elixiroffice"
download_url: "https://github.com/leag1234/elixiroffice/releases/tag/v0.2.0"
issue_number: 42
---

{{< bulten-inceleme
    platform="Linux (AppImage/DEB), Windows x64, macOS (yalnızca Apple Silicon)"
    lisans="AGPL-3.0"
    kod="github.com/leag1234/elixiroffice|https://github.com/leag1234/elixiroffice"
    kime="Belgelerini çevrimdışı, hesap açmadan düzenlemek isteyen ve beta olmanın getirdiği riski kabul eden Linux/Windows kullanıcıları."
    durum="Beta"
    kaynak="Beta 2|https://github.com/leag1234/elixiroffice/releases/tag/v0.1.0-beta.2; 0.2.0|https://github.com/leag1234/elixiroffice/releases/tag/v0.2.0; It’s FOSS|https://itsfoss.com/news/elixiroffice-euro-office-fork/" >}}

{{< bulten-giris >}}
13 Ekim'de masaüstü beta 2, 15 Ekim'de PDF desteği ve parola korumalı dosya desteği getiren 0.2.0 yayımlandı; Euro-Office/ONLYOFFICE bileşenleri üzerine kurulu ve arayüzü Microsoft Office'e benzetilmiş.
{{< /bulten-giris >}}

{{< bulten-artilar >}}
- Tamamen yerel ve çevrimdışı çalışıyor; hesap ve sunucu gerektirmiyor.
- DOCX/XLSX/PPTX ile ODT/ODS/ODP uyumu var.
- 0.2.0 ile PDF açma/arama/annotasyon, parola korumalı dosyalar ve 39 dilde şablon geldi.
- AI varsayılan olarak kapalı; telemetri yok iddiası var.
{{< /bulten-artilar >}}

{{< bulten-eksiler >}}
- Beta olduğu için üretim belgeleri açısından riskli.
- Eşzamanlı düzenleme, sürüm geçmişi, mektup birleştirme, eklenti/makro ve dijital imza yok.
- Kodun büyük ölçüde LLM ajanlarıyla üretilmesi güven ve denetim sorusu doğuruyor; imzalı kurulum paketi bulunmuyor.
{{< /bulten-eksiler >}}
{{< /bulten-inceleme >}}
