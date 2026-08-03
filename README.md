# Ustozim Nurim — Kunlik bilim sinovi

Har kuni soat **20:00** da communityga bitta e'lon tashlanadi.
Tugma bosilganda viktorina sahifasi ochiladi — savollar u yerda birma-bir beriladi.

- **Savol bazasi:** 451 ta (300 IT + 151 fazilatli liderlik)
- **30 kun davomida hech bir savol takrorlanmaydi**
- Savollar soni haftama-hafta: 7 → 9 → 11 → 13 → 15

## Tarkibi

| Fayl | Vazifasi |
|------|----------|
| `index.html` | Viktorina sahifasi (GitHub Pages) |
| `bank.js` | Savollar bazasi |
| `post_daily_announcement.py` | Kunlik e'lonni yuboradi |
| `.github/workflows/daily-quiz.yml` | Har kuni 20:00 da ishga tushiradi |

## Sozlamalar

Repozitoriya → **Settings → Secrets and variables → Actions**

**Secrets:** `BOT_TOKEN`, `CHAT_ID`
**Variables:** `QUIZ_URL`, ixtiyoriy `TOPIC_ID`, `PIN`

## Savol qo'shish

`quiz_bank.json` ga qo'shing, keyin `bank.js` ni yangilang:

```bash
python3 -c "import json;d=json.load(open('quiz_bank.json'));open('bank.js','w').write('window.BANK='+json.dumps(d,ensure_ascii=False,separators=(',',':'))+';')"
```

Format: `{"q":"Savol?","o":["a","b","c"],"c":0,"t":"IT"}` — `c` to'g'ri javob indeksi (0 dan), `t` = `IT` yoki `Liderlik`.

> ⚠️ `WEEKLY_COUNTS`, `IT_SHARE`, `START_DATE` qiymatlari `index.html` va
> `post_daily_announcement.py` da **bir xil** bo'lishi shart.
