# Gerekli Gereksiz

Hugo ile geliştirilen çok içerikli Türkçe portal: uygulama kataloğu, haber/blog, haftalık bülten, Türk sporcu başarıları ve baraj doluluk verileri.

Stil: **Tailwind CSS v4** — Hugo'nun yerleşik `css.TailwindCSS` fonksiyonu ile derlenir.

## Gereksinimler

| Araç | Not |
|---|---|
| [Hugo](https://gohugo.io/installation/) | **Extended**, v0.169.0 (CI ile aynı) — `make version` ile kontrol et |
| [Node.js](https://nodejs.org/) | v24 (CI ile aynı, Tailwind CLI npm ile kurulur) |
| npm | Node ile birlikte gelir |

## Kurulum

```bash
npm install    # Tailwind CSS v4 CLI (node_modules yoksa make build da otomatik kurar)
```

## Geliştirme

```bash
make serve     # Geliştirme sunucusu (taslaklar dahil) → http://localhost:1313
```

- Şablon, CSS veya içerik değişikliğinde tarayıcı otomatik yeniler.
- Geliştirme modunda CSS minify'sız servis edilir (`/css/main.css`).
- Tailwind sınıfı eklediğin herhangi bir şablon kaydedildiğinde CSS anında yeniden derlenir.

## Yayına Alma

Site, `gerekligereksiz/gerekligereksiz.github.io` deposundan GitHub Pages'e yayınlanır. Bu klasörün içeriği o deponun **köküne** kopyalanır (Hugo proje kökü = depo kökü).

```bash
make build     # yerel derleme → public/ (üretimde CSS minify + fingerprint)
```

Başarıda `OK`, hatada son 20 satır yazdırır. Build'de deprecation uyarısı çıkarsa düzeltme yap.

### Otomatik deploy

`.github/workflows/deploy.yml` `main` dalına yapılan her push'ta çalışır:

1. Hugo **extended v0.169.0** + Node **v24** kurulur, `npm ci` çalışır.
2. `hugo --gc --minify --baseURL <Pages adresi>` ile derlenir.
3. `public/` artifact olarak yüklenir ve `actions/deploy-pages` ile yayınlanır.

`baseURL` workflow'da `actions/configure-pages` çıktısından alınır; yani depo Pages ayarında hangi adres tanımlıysa o kullanılır. `hugo.yaml`'daki `baseURL` üretim adresidir, yerel build'ler onu kullanır.

| Durum | Yayın adresi |
|---|---|
| Şu an (geçici) | `https://gerekligereksiz.github.io/` |
| Domain transferi bitince | `https://gerekli-gereksiz.com/` |

**Domain geçişi:** Cloudflare transferi tamamlanınca depo ayarlarından custom domain'i `gerekli-gereksiz.com` yapmak yeterli. Workflow ve `hugo.yaml` değişmez; `baseURL` Pages ayarından otomatik gelir. `hugo.yaml` zaten üretim adresini taşıdığı için yerel build'ler de doğru kalır.

> Not: Workflow yalnızca hedef depoda çalışır. Bu klasör bir monorepo alt dizinindeyken GitHub iç içe `.github` klasörünü yok sayar.

## Komutlar

| Komut | Ne yapar |
|---|---|
| `make build` | Derler, `public/` klasörüne yazar |
| `make serve` | Geliştirme sunucusu |
| `make new section=<bolum> slug=<slug>` | Yeni içerik dosyası oluşturur |
| `make search` | Build + Pagefind arama indeksi |
| `make version` | Hugo sürümünü gösterir |
| `make clean` | `public/` ve `resources/_gen` siler |

## Tailwind Nasıl Çalışıyor?

1. `hugo.yaml`'da `build.buildStats.enable: true` → Hugo, şablonlarda kullanılan sınıfları `hugo_stats.json` dosyasına yazar.
2. `assets/css/main.css` içindeki `@source "hugo_stats.json"` sayesinde Tailwind **yalnızca kullanılan** sınıfları derler.
3. `layouts/_partials/css.html` içindeki `css.TailwindCSS` sonucu üretimi minify eder ve fingerprint (SRI) ekler.

Konfigürasyon değişikliğinde `hugo_stats.json` ve `resources/_gen` eski kalabilir; sorun yaşarsan:

```bash
make clean && make build
```

Yeni utility sınıfı eklemek için config dosyası gerekmez — şablonlarda kullanman yeterli. Tema renkleri/spacing gibi ayarlar `assets/css/main.css` içinde CSS-first olarak tanımlanır (`@theme` bloğu).

## Klasör Yapısı

```
content/{uygulamalar,yazilar,bulten,sporcular,baraj}/  # içerik
data/baraj/            # otomatik güncellenen veri akışları
layouts/               # şablonlar (_partials/ içinde parçalar)
assets/                # işlenecek css/js/görseller (assets/css/main.css)
scripts/               # veri çekme scriptleri
.github/workflows/     # zamanlanmış işler ve deploy
hugo.yaml              # Hugo + Tailwind yapılandırması
Makefile               # tüm komutlar burada
```

## Kurallar

- İçerik Türkçe; dosya/klasör adları ASCII slug (ş, ğ, ı, ö, ü, ç yok).
- API anahtarlarını repoya yazma; ortam değişkeni veya GitHub Secrets kullan.
- Ajan kuralları için bkz. [AGENTS.md](AGENTS.md).
