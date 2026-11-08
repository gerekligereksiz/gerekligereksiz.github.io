// Build sonrası: public/**/*.html dosyalarına Content-Security-Policy <meta> etiketi ekler.
// GitHub Pages yanıt başlığı eklemeye izin vermediği için meta kullanılır
// (frame-ancestors, HSTS, COOP, XFO meta ile verilemez).
//
// Satır içi script'ler (JSON-LD hariç) sayfa başına sha256 ile izinlenir; 'unsafe-inline' yok.
// Hash'ler Hugo --minify çıktısından hesaplanır, bu yüzden betik hugo'dan SONRA çalışmalı.
// Satır içi <style> (css.html, 20 KB altı CSS) de aynı şekilde hash'lenir.
// Yeni dış kaynak (script, görsel, iframe, bağlantı) eklenirse aşağıdaki listeyi güncelle.
import { createHash } from "node:crypto";
import { readdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const root = process.argv[2] || "public";

const GA = {
  script: ["https://www.googletagmanager.com"],
  connect: [
    "https://*.google-analytics.com",
    "https://*.analytics.google.com",
    "https://*.googletagmanager.com",
  ],
  img: ["https://*.google-analytics.com", "https://*.googletagmanager.com"],
};

function policy(hashes, styleHashes) {
  return [
    "default-src 'self'",
    `script-src 'self' ${[...hashes].map((h) => `'sha256-${h}'`).join(" ")} ${GA.script.join(" ")}`.replace(/ +/g, " "),
    `connect-src 'self' ${GA.connect.join(" ")}`,
    `img-src 'self' data: ${GA.img.join(" ")}`,
    `style-src 'self' ${[...styleHashes].map((h) => `'sha256-${h}'`).join(" ")}`.replace(/ +/g, " ").trim(),
    "font-src 'self'",
    "manifest-src 'self'",
    "frame-src https://www.youtube-nocookie.com",
    "object-src 'none'",
    "base-uri 'self'",
    "form-action 'self'",
  ].join("; ");
}

function walk(dir, out = []) {
  for (const name of readdirSync(dir)) {
    const p = join(dir, name);
    if (statSync(p).isDirectory()) walk(p, out);
    else if (name.endsWith(".html")) out.push(p);
  }
  return out;
}

const STYLE_RE = /<style\b[^>]*>([\s\S]*?)<\/style>/gi;
const SCRIPT_RE = /<script\b([^>]*)>([\s\S]*?)<\/script>/gi;
const META_RE = /<meta[^>]+http-equiv=["']?Content-Security-Policy["']?[^>]*>/i;
const CHARSET_RE = /<meta\s+charset=[^>]*>/i;
const allHashes = new Set();
const allStyleHashes = new Set();
let pages = 0;
const errors = [];

for (const file of walk(root)) {
  let html = readFileSync(file, "utf8");
  const hashes = new Set();
  const styleHashes = new Set();
  for (const m of html.matchAll(STYLE_RE)) {
    if (m[1].trim()) styleHashes.add(createHash("sha256").update(m[1]).digest("base64"));
  }
  for (const m of html.matchAll(SCRIPT_RE)) {
    const attrs = m[1];
    if (/\bsrc\s*=/.test(attrs)) continue;
    if (/type\s*=\s*["']?application\/(ld\+)?json/i.test(attrs)) continue;
    if (!m[2].trim()) continue;
    hashes.add(createHash("sha256").update(m[2]).digest("base64"));
  }
  if (/\son[a-z]+\s*=\s*["']/i.test(html.replace(SCRIPT_RE, ""))) {
    errors.push(`${file}: satır içi event handler (onclick= vb.) CSP ile çalışmaz`);
  }
  if (/href\s*=\s*["']?javascript:/i.test(html)) errors.push(`${file}: javascript: bağlantısı`);

  const meta = `<meta http-equiv="Content-Security-Policy" content="${policy(hashes, styleHashes)}">`;
  html = html.replace(META_RE, "");
  if (!CHARSET_RE.test(html)) {
    errors.push(`${file}: <meta charset> bulunamadı`);
    continue;
  }
  html = html.replace(CHARSET_RE, (c) => c + meta);
  writeFileSync(file, html);
  hashes.forEach((h) => allHashes.add(h));
  styleHashes.forEach((h) => allStyleHashes.add(h));
  pages++;
}

if (errors.length) {
  console.error(errors.slice(0, 20).join("\n"));
  process.exit(1);
}
console.log(`CSP: ${pages} sayfa, ${allHashes.size} benzersiz script, ${allStyleHashes.size} benzersiz style hash'i`);
