# yaniyo-extension

### Desteklenen Argümanlar:

- `--discount_range` (str, varsayılan: `""`):
  İndirim aralığı belirler. Örneğin:
  - `"10-20"`: %10 ile %20 arasında indirimli ürünler
  - `"10-"`: %10 ve üzeri indirim
  - `"-20"`: %20 ve altı indirim
- `--price_range` (str, varsayılan: `""`):
  Ürün fiyat aralığı belirler. Örneğin:

  - `"400-2000"`: ₺400 ile ₺2000 arasındaki ürünler
  - `"400-"`: ₺400 ve üzeri ürünler
  - `"-2000"`: ₺2000 ve altı ürünler

- `--interval` (int, varsayılan: `60`):
  Sayfayı kontrol etmek için kaç saniye bekleyeceğinizi belirler.

- `--url` (str, varsayılan: `"tum-firsatlar"`):
  Kontrol edilecek Yaniyo sayfasının son kısmını belirtir. Örneğin:
  - `"tum-firsatlar"` → `https://yaniyo.com/tum-firsatlar`

Eğer belirtilen sayfa bulunamazsa, script otomatik olarak duracaktır.

Klavyeden bir tuşa basılırsa script otomatik olarak duracaktır.
