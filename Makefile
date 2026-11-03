.PHONY: build serve new version search clean

# Çıktıyı kısa tutar: başarıda tek satır, hatada son 20 satır.
build:
	@[ -d node_modules ] || npm install >/dev/null 2>&1
	@out=$$(hugo --gc --minify 2>&1); rc=$$?; \
	if [ $$rc -ne 0 ]; then echo "$$out" | tail -n 20; exit $$rc; fi; \
	echo OK; echo "$$out" | grep -iE 'warn|deprecat' | head -n 10 || true

serve:
	hugo server -D

# Kullanım: make new section=uygulamalar slug=uygulama-adi
new:
	@test -n "$(section)" -a -n "$(slug)" || { echo "kullanim: make new section=<bolum> slug=<slug>"; exit 1; }
	@hugo new content $(section)/$(slug).md

version:
	@hugo version

# Build sonrası arama indeksi (Pagefind)
search: build
	@npx --yes pagefind --site public 2>&1 | tail -n 5

clean:
	@rm -rf public resources/_gen

# Görsel kırpma: make crop file=assets/images/foo.png top=10 bottom=5 left=0 right=0
crop:
	@test -n "$(file)" || { echo "kullanim: make crop file=<dosya> [top=<n>] [bottom=<n>] [left=<n>] [right=<n>]"; exit 1; }
	@python3 scripts/crop.py "$(file)" $(if $(top),--top $(top),) $(if $(bottom),--bottom $(bottom),) $(if $(left),--left $(left),) $(if $(right),--right $(right),)
