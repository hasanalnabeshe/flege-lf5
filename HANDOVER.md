# HANDOVER – Pflege LF 5 Lernseite

> هالملف بيتحدّث مع كل تغيير. آخر تحديث: **21.10.2026**
> القسم الأخير (سجل التغييرات) فيه كل شي صار بالترتيب.

---

## 1. شو الهدف من المشروع

موقع دراسة شخصي لـ Hasan (تدريب تمريض Pflegefachmann، مدرسة التمريض DRK بـ Saarlouis) لمادة **LF 5**:

- كل أوراق الدرس **منقولة حرفياً بالألماني**، ومع **ترجمة عربي وشرح** تحت كل سطر.
- زر فوق بيبدّل بين **DE + عربي** و **Nur Deutsch**. بوضع الألماني بس بيختفي كل النص العربي، والجداول والصور بتضل.
- كل الصور موجودة: صور أوراقه بخط إيده، رسمات التشريح، وكل شرائح عروض المجموعات.
- تصحيحات Claude على أوراقه موجودة بصناديق بنفسجية (Korrektur / تصحيح).
- لما Hasan يبعت أوراق جديدة، بتنضاف لنفس الموقع.

---

## 2. وين المشروع

| الشي | المكان |
|---|---|
| **المصدر الأساسي** | GitHub `hasanalnabeshe/flege-lf5`، branch `main` (اسم الـ repo فيه غلطة "flege" بدون P، بس هيك انعمل) |
| نسخة قديمة | GitHub `hasanalnabeshe/pflege`، branch `lf5-lernseite`. نفس المحتوى، **ما عاد هي الأساس**. الـ `main` هناك موقع Hasan القديم وما انلمس |
| الموقع على Vercel | Hasan بيعمل import لـ `flege-lf5`، والرابط المتوقع `flege-lf5.vercel.app`. **لسا ما تأكدنا من الرابط** |
| نسخة Claude (Artifact) | https://claude.ai/artifact/9yaDBa4Jz4HLbNFnMa935s (خاصة، بتتحدث مع كل تغيير) |

### بنية الملفات
```
content/            ← كل المحتوى (ملف لكل قسم، بيتقرأ بالترتيب حسب الرقم)
  01-behandlungspfad.txt   Übersicht + Behandlungspfad + Impulsfrage
  02-herr-m.txt            Herr M. – akutes Abdomen (Aufgaben 1–5)
  03-gruppen.txt           Gruppenarbeit-Auftrag + Gruppe 1 Cholezystektomie
  04-gruppen2.txt          Gruppe 2 Hüft-TEP + Gruppe 3 Frakturversorgung
  05-gruppen3.txt          Gruppe 4 Hernie + Gruppe 5 Appendektomie + Gruppe 6 Débridement
  06-nervensystem.txt      NS Grundlagen, Fälle, Lernaufgabe Schmerz
  07-zns.txt               Gehirn, Rückenmark, Häute, Liquor, PNS
  08-teamarbeit.txt        Ingos TB – Gruppenarbeit Lösung (Teams & Hierarchien)
template.html       ← التصميم + CSS + JS (القائمة، زر اللغة، dark mode، تكبير الصور)
build.py            ← بيحوّل content/*.txt + template.html إلى public/index.html
public/index.html   ← الصفحة النهائية (بتنبنى، لا تعدّلها باليد)
public/img/         ← كل الصور (jpg مضغوطة)
public/vercel.json  ← cleanUrls + cache للصور
HANDOVER.md         ← هالملف
```

---

## 3. القرارات المهمة

- **موقع ثابت 100%**: ما في Supabase، ما في قاعدة بيانات، ما في تسجيل دخول، ما في backend. ما في حاجة لهيك، والمحتوى نص وصور بس.
- **ما في build على Vercel**: الصفحة بتنبنى محلياً بـ `python3 build.py`، و`public/` بينرفع جاهز مع الـ commit. إعدادات Vercel: Framework **Other**، Build Command فاضي، Output Directory **`public`**.
- **ما في GitHub Actions** ولا أي workflow، فما في أي مشكلة billing بالـ Actions بهالمشروع.
- **صيغة المحتوى** (بـ `content/*.txt`). كل سطر: `ألماني | عربي`.
  - `@page id | اسم DE | اسم AR | مجموعة DE / مجموعة AR` ← صفحة جديدة بالقائمة
  - `# ` / `## ` / `### ` ← عناوين (h2/h3/h4)
  - `p: ` فقرة · `- ` نقطة · `1. ` قائمة مرقمة · سطر بادئ بمسافة ← نقطة فرعية
  - `q: ` سؤال (صندوق) · `note:` ملاحظة · `tip:` تذكّر (أخضر) · `warn:` انتبه (أحمر) · `fix:` تصحيح (بنفسجي)
  - `th: خلية ;; خلية` رأس جدول · `tr: خلية ;; خلية` صف (كل خلية ممكن تكون `DE | AR`)
  - `img: اسم-الصورة | تعليق DE | تعليق AR` (بدون .jpg، من public/img)
  - `gallery: بادئة | عنوان DE | عنوان AR` ← معرض لكل الصور اللي اسمها بيبلش بالبادئة
  - `cards:` ← بطاقات كل الصفحات (بصفحة البداية)
  - `**غامق**` و `*مائل*` مدعومين
- **أسماء الصور**:
  - `herrm-*` أوراق Herr M.
  - `bp-seiteN` ورقة Behandlungspfad
  - `impuls-seiteN` شرائح المعلمة
  - `gN-folieNN` شرائح المجموعة N
  - `ns-seiteNN` صفحات دفتر Nervensystem
  - `ns-*` رسمات الجهاز العصبي
  - `zns-*` صور الدماغ والنخاع
  - `ingo-*` شريحة حل Ingos TB
- **الترجمة**: الألماني منقول متل الورقة بالضبط ("ما تغير شي"). والعربي فصحى بسيطة، مع شروحات بالعامية الشامية/الفلسطينية متل ما بيحكي Hasan.
- **الأخطاء بأوراق Hasan** ما بتنصلح جوّا النص الأصلي. بيضل النص متل ما هو، وبينحط تحته صندوق `fix:` فيه التصحيح.
- **الخطوط**: IBM Plex Sans + IBM Plex Sans Arabic + Fraunces (من Google Fonts).

---

## 3b. مواضيع الامتحان (من اللوح، 21.10.2026)

1. **Ingos TB** – Merksatz zur Gruppenarbeit: Wie gehen Auszubildende mit der Arbeit in diversen Teams / Berufsgruppen und mit Hierarchien um? ← ✅ موجود (صفحة `team`، من شريحة "Gruppenarbeit Lösung")
2. **Chirurgische Behandlungspfade** – Was ist ein Behandlungspfad? Welche Rolle spielen die PFK im Behandlungspfad → zentraler Aspekt ← ✅ موجود
3. **ZNS** – Einteilung (Tafelbild insb.); Reiz-Reaktions-Kette = Grundprinzip ↔ Reflex; worauf können Veränderungen im ZNS Einfluss nehmen; Beschreibung NZ (Nervenzelle); Bestandteile des Gehirns; Rückenmark; Hirn- + RM-Häute ← ✅ موجود
4. **Expertenstandard** ← **مش بالموقع بعد** (غالباً DNQP Expertenstandard Schmerzmanagement)
5. **Schmerzmanagement – Pflege bei Schmerzen**: Rolle der Pflege, Schmerzassessment, Schmerzen bei Kindern, Begleitsymptome, Schmerzprävention, Schmerztherapie ← **جزئياً** (بس Lernaufgabe Schmerz)

## 4. شو خلص

- [x] **Behandlungspfad**: النص كامل، أهداف، مثال akutes Abdomen، جدول Hüft-TEP، وصور الورقة الأصلية
- [x] **Impulsfrage & Rolle der Pflege**: شرائح المعلمة (Print2) مع جدول دور التمريض
- [x] **Herr M. – akutes Abdomen**: Aufgaben 1–5 كاملة مع الجداول، صور حلول Hasan، تصحيحات وإضافات
- [x] **Gruppenarbeit**: الطلب، وجدول المواضيع، وصورة الورقة
- [x] **Gruppe 1–6**: كل مجموعة صفحة لحالها، مع ترجمة كاملة ومعرض لكل الشرائح (Gruppe 3 ورقة، مش عرض)
- [x] **Nervensystem LF 5.3**: Frau Müller، Aufbau/Funktion، Reflex، Weg des Reizes، Was kann ausfallen، PNS-Schäden
- [x] **Fälle**: Herr Schneider، Frau Weber، Herr Müller، مع ملاحظات Hasan وجدول تصحيح إملائي
- [x] **Lernaufgabe Schmerz**: تعاريف الخلية العصبية، رسمة الخلية الأصلية، طريق الألم
- [x] **ZNS – Gehirn**: الأجزاء ①–⑩ مع صورة الدماغ المرقمة
- [x] **ZNS – Rückenmark / Häute / Liquor / PNS**: كل الصور اتبدلت بنسخ واضحة بعتها Hasan (Wirbel، Wirbelsäule، Rückenmark-Querschnitt، Häute، Liquor)
- [x] **Ingos TB – Teams & Hierarchien** (موضوع الامتحان 1): شريحة "Gruppenarbeit Lösung" حرفياً مع ترجمة، صورة الشريحة، تصحيحين (`fix:`)، وجملة حفظ مقترحة (معلّمة إنها من Claude)
- [x] الموقع مرفوع على GitHub (`flege-lf5` main)
- [x] الموقع شغال على الموبايل (جرّبناه 390px) وبالـ dark mode

## 5. شو باقي

- [ ] **التأكد من Vercel**: Hasan لازم يعمل Import لـ `flege-lf5` (Other / Output `public`) ويبعت الرابط. بعدها نكتب الرابط هون.
- [ ] **الـ repo `flege-lf5` لازم يصير Private**. هو هلأ Public وفيه خط إيد Hasan، صور أوراقه، وأسماء زملائه على الشرائح.
- [ ] **تقرير إذا لازم نحذف branch `lf5-lernseite`** من `pflege` (صار نسخة مكررة).
- [ ] **مواضيع الامتحان الناقصة**: Expertenstandard، Schmerzmanagement كامل – بانتظار أوراق Hasan
- [ ] **مواضيع جديدة**: كل ما يبعت Hasan أوراق جديدة، بتنضاف (صفحة جديدة أو ملف `08-....txt`).
- [ ] اختياري: One Minute Wonder لكل مجموعة، وأسئلة مراجعة / Quiz.

---

## 6. مشاكل معروفة

| المشكلة | التفاصيل | الحل / الحالة |
|---|---|---|
| **Vercel MCP ما بيقدر يعمل مشروع** | `create_project` و `create_deployment` بيرجعوا 403 "You don't have permission to create a project". حساب Vercel الموصول بـ Claude (team `hasanalnabeshe`) ما فيه غير مشروع `losheimer-kebab` | Hasan بيعمل الـ Import من dashboard Vercel بنفسه |
| **مشروع Vercel تبع Hasan مش ظاهر لـ Claude** | Hasan فتح نسخة على `…alnabeshe.vercel.app` (بحساب أو scope تاني)، و Claude ما بيشوفها بالـ MCP | بعد Import `flege-lf5` كل push بيعمل deploy لحاله، فما في حاجة يشوفها Claude |
| **GitHub: Claude ما بيقدر يعمل repo** | `POST user/repos` ممنوع بالـ session (403) | Hasan بيعمل الـ repo، و Claude بيعمل push |
| **رسالة git غريبة وقت الـ push** | `fatal: expected 'acknowledgments'` بتطلع، بس الـ push بينجح (اتأكدنا بـ `git ls-remote`) | تجاهلها، بس دايماً تأكد بـ `ls-remote` |
| **صور الـ scans باهتة** | ملفات PDF الأصلية صور موبايل لأوراق مطبوعة (~200ppi) | الصور المهمة اتبدلت بنسخ نظيفة. أي صورة باهتة تانية: Hasan بيبعت نسخة أوضح |
| **الجهاز (remote device) مش متصل** | `device_bash` بيرجع "not connected to the bridge" | مش مهم لهالمشروع |
| **GitHub Actions / billing** | ما في Actions بهالمشروع، فما في مشكلة billing | — |

### أخطاء بالمحتوى الأصلي (موثقة بالموقع كـ `fix:`)
- Herr M., Aufgabe 2: "Koliken → Extrauteringravidität" ← الصح: Gallen-/Nierenkolik
- Herr M., Aufgabe 5: "SBR A" ← SBAR
- Gruppe 2: شريحة "Besonderheiten" بتوصف DEP مش TEP
- Gruppe 3: Konservativ تحت Operation؛ ناقص: فك الجبس عند Kompartmentsyndrom، Fettembolie، Gipskontrolle، Antibiotika/Tetanus بالكسر المفتوح
- Gruppe 5: "Urin: Elektrolyte & Gerinnung" ← هدول فحوصات دم
- Nervensystem: "Lähmung" عند العصب الحسي ← الصح Taubheit؛ "Vorderes Übertragungsgehirn" ← Hinterhorn
- Ingos TB (Folie): "Verlegunge" ← Verlegung؛ "Ärzten" بالقائمة ← Ärzte
- Hypophyse: Oxytocin مش "Glückshormon" (هو Bindungshormon، وبيتصنع بالـ Hypothalamus)

---

## 7. أول خطوة لازم تنعمل

1. **Hasan**: بـ Vercel ← **Add New → Project** ← `flege-lf5` ← Framework **Other**، Output Directory **`public`** ← **Deploy**. ابعت الرابط.
2. **Hasan**: خلي `flege-lf5` **Private** (Settings → Danger Zone → Change visibility).
3. **Claude**: بعد ما يوصل الرابط، اكتبه بالقسم 2 هون.

### كيف تعمل تحديث (لأي جلسة جاية)
```bash
git clone https://github.com/hasanalnabeshe/flege-lf5 && cd flege-lf5
# عدّل content/*.txt أو حط صور بـ public/img/
python3 build.py              # بيبني public/index.html
git add -A && git commit -m "..." && git push origin main
# حدّث HANDOVER.md (سجل التغييرات + شو خلص/شو باقي) بنفس الـ commit
```

---

## 8. سجل التغييرات

- **20.10.2026**: ترجمة Behandlungspfad والملف الثاني (Impulsfrage). حل Herr M. مع تصحيحات. ترجمة 6 مجموعات وملاحظات Gruppe 3. ترجمة Nervensystem + ZNS.
- **20.10.2026**: بناء الموقع: 16 صفحة، DE+AR / Nur DE، 118 صورة. انرفع على `pflege` branch `lf5-lernseite` وعلى Claude Artifact.
- **20.10.2026**: محاولة Vercel MCP فشلت (403). Hasan عمل نسخة بنفسه (`…alnabeshe.vercel.app`).
- **20.10.2026**: صور ZNS انقصت من جديد من الـ scan الأصلي. صورة الخلية العصبية اتبدلت بورقة العمل الأصلية (رسمة Hasan مع كتابته).
- **20.10.2026**: Hasan بعت صور واضحة، اتبدلت: Wirbel، Wirbelsäule، Rückenmark-Querschnitt، Hirn-/Rückenmarkshäute، Liquorräume.
- **21.10.2026**: Hasan عمل repo `flege-lf5`، والموقع انرفع على `main`. صار هو المصدر الأساسي. انعمل HANDOVER.md و CLAUDE.md.
- **21.10.2026**: Hasan بعت صورة اللوح بمواضيع الامتحان (5 مواضيع) – انضافت بالقسم 3b.
- **21.10.2026**: Hasan بعت صورة شريحة "Gruppenarbeit Lösung" (جواب موضوع الامتحان 1، Ingos TB). انضافت صفحة جديدة `content/08-teamarbeit.txt` + صورة `ingo-loesung.jpg`. الموقع صار 17 صفحة.
