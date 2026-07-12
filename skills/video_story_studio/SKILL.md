# Video Story Studio

**Kab use karo:** Jab Boss kisi topic par video content maange — "X pe video banao", "Y minute ki video ke liye script/story banao", "voiceover aur video prompts banao", "faceless video content", "reel/short/YouTube video ke liye clips aur narration", "AI video (Sora/Veo/Runway/Kling) ke liye prompts banao". Yeh skill ek poora video package banati hai: research + full story + timed voiceover + scene-by-scene video-clip prompts — sab Desktop ke ek folder mein.

## Pehle 2 cheezein confirm karo (agar Boss ne nahi batayi)
1. **Topic** — kis cheez pe video hai.
2. **Duration** — video kitni lambi (seconds ya minutes). Yahi sab kuch decide karti hai.
3. (Optional) Tone/platform — YouTube long, Reel/Short, documentary, motivational, horror, etc. Na bataye to default: engaging + cinematic. Language: Boss jis mein baat kare (default English narration).

Duration na mile to **maang lo** — uske bina scene count aur word budget nikal hi nahi sakte.

## Step 1 — Desktop par short-naam ka folder banao
Topic se ek **chhota (1-3 shabd) naam** nikaalo aur Desktop par usi naam ka naya folder banao.
- "how black holes are formed" → `Black_Holes`
- "history of the Roman Empire" → `Roman_Empire`
- "10 tips to save money" → `Money_Tips`
Saari files isi folder ke **andar** banengi. Folder ka poora path yaad rakho (e.g. `Desktop\Black_Holes`) — subagents ko exact path dena zaroori hai.

## Step 2 — Duration se maths nikaalo (yeh sab ka base hai)
- **Voiceover words** ≈ duration(seconds) × **2.5** (≈150 words/min natural pace).
- **Number of scenes/clips** ≈ duration(seconds) ÷ **5** (AI video clips ~5s each), upar round karo. Zyada action ho to 4s, calm ho to 8s — beech mein adjust karo.
- Har scene ko ek narration line + ek video prompt milega, sab aapas mein match karein.

| Duration | ~Words (voiceover) | ~Scenes/clips |
|----------|--------------------|---------------|
| 30 sec   | ~75                | ~6            |
| 60 sec   | ~150               | ~12           |
| 3 min    | ~450               | ~36           |
| 5 min    | ~750               | ~60           |
| 10 min   | ~1500              | ~120          |

Bade video (5+ min / 40+ scenes) me scenes ko chunks me baanto (10-12 scenes per subagent) taaki har file complete aur detailed rahe — kabhi "baaki same" likh ke chhota mat karo.

## Step 3 — SERP se research karo (plain search only, koi document nahi)
Topic par **web/SERP search** se research karo — 6-10 solid, sahi facts, numbers, dates, aur 2-3 killer hook angles. Galat fact mat likho; jo confirm ho wahi use karo. Yeh research story ko accurate aur voiceover ko credible banati hai.

⚠️ **Bahut zaroori:** Research ke liye SIRF web/SERP **search** karo. `research_agent` ya koi bhi **document-banane wala tool** (Word/PDF/PPT/Excel/`.docx`) **bilkul mat** use karo — wo tool hamesha ek Word/PDF file bana deta hai, jo Boss ne nahi maangi ("jabardasti ke docs"). Yeh skill ka output SIRF plain `.txt` files hain. Research ka nateeja seedhe `research.txt` mein likho.

## Step 4 — Master structure LOCK karo (sabse important)
Voiceover aur video-prompts **same scenes** pe bane, isliye pehle ek numbered **scene list** fix karo — narrative order mein, hook se outro tak:
- **Hook (Scene 1):** pehle 3 second ka scroll-stopper — ek daring question, shocking fact, ya bold claim. Boring intro bilkul nahi.
- **Body (Scenes 2..N-1):** story/points logical flow mein, tension build karti hui, research ke facts ke saath.
- **Outro (last scene):** satisfying close + CTA ("subscribe/follow", ya thought-provoking last line).
Yeh locked scene list hi story.txt, voiceover aur prompts — teeno ka source of truth hai.

## Step 5 — 4 files banao (bhaari kaam SUBAGENTS se)
Boss ne kaha "subagents ke help se" — to writing subagents ko do. Subagent ke paas tumhaara **koi context nahi**, isliye har subagent ke task me yeh sab **poora likho:** exact folder path, topic, duration, word/scene budget, aur poori locked scene list. Ek do-chhoti file (research + story) khud likh sakti ho; do bhaari derived files (voiceover + video prompts) parallel subagents se — dono ko wahi scene list do.

⚠️ **Har subagent task me yeh line zaroor daalo:** "Output SIRF plain `.txt` file(s) hon — `write_file` se likho. `research_agent`, `create_document`, ya koi bhi Word/PDF/PPT/`.docx` banane wala tool bilkul mat use karo." Warna subagent apne aap document bana deta hai (jo Boss ne nahi maangi). Yeh skill sirf `.txt` deti hai.

Banane wali files (sab folder ke andar, `.txt`):

**1. `research.txt`** — topic, 6-10 verified facts (bullets), hook angles, sources, tone/platform note.

**2. `story.txt`** — poori story, ek continuous engaging narrative:
```
TITLE: <catchy title>
DURATION: <e.g. 60s>  |  PLATFORM/TONE: <...>

HOOK (0:00–0:03):
<3-second scroll-stopper>

STORY:
<poora flowing narrative, hook se build karta hua, research ke facts ke saath>

OUTRO:
<satisfying close + CTA / punchy last line>
```

**3. `voiceover_script.txt`** — record-ready narration, scene ke hisaab se timed:
```
=== VOICEOVER SCRIPT — <Title> (<duration>) ===
Total words: <~N>  |  Pace: ~150 wpm

[Scene 1 | 0:00–0:05]  (HOOK)
Narration: "<exact words to speak — scene ki length me fit>"
Delivery: <tone/pace note, e.g. punchy, mysterious, slow>

[Scene 2 | 0:05–0:10]
Narration: "..."
Delivery: ...
... (har scene ke liye) ...

--- FULL CONTINUOUS SCRIPT (one-take recording) ---
<saari narration lines joined, natural flow me>
```
Har scene ki narration us scene ki **seconds × 2.5** words ke aas-paas rakho — na zyada, na kam.

**4. `video_prompts.txt`** — har scene ke liye ek **detailed AI-video-generation prompt** (Sora/Veo/Runway/Kling style), voiceover line se match karta hua:
```
=== VIDEO CLIP PROMPTS — <Title> ===
Aspect ratio: <9:16 short / 16:9 long>  |  Style: <cinematic/anime/realistic/...>

[Scene 1 | ~5s]  (matches VO Scene 1)
Prompt: <subject + action + setting + camera movement (dolly/pan/aerial) + lighting + mood + color palette + film style>. Highly detailed, <aspect ratio>, cinematic.
Negative: <text, watermark, distorted, low-res>

[Scene 2 | ~5s]
Prompt: ...
... (har scene ke liye, jitne required hain utne — no shortcuts) ...
```
Har prompt self-contained aur bharpoor detail wala ho — koi model bhi bina extra context ke clip bana sake.

## Step 6 — Report karo
Sab ban jaaye to Boss ko chhoti Hinglish line me batao: folder ka naam, kitne scenes/clips bane, aur files ready hain. Subagents background me hon to bolo "ban rahi hai, ho jaate hi batati hoon" — result aa jaayega tab confirm karo.

## Example
Boss: *"Titanic ke doobне pe 60 second ki YouTube short banao."*
→ Folder `Desktop\Titanic`. Maths: ~150 words, ~12 scenes. SERP se Titanic facts (date 1912, iceberg, ~1500 died, band bajta raha). Scene list lock: Hook "What if the 'unsinkable' ship's last night was a warning we ignored?" → 10 body scenes (departure, iceberg warning ignored, collision, chaos, lifeboats, band, sinking, cold water, dawn, aftermath) → Outro "Some legends are built to remind us: pride sinks ships. Follow for more." Phir research.txt + story.txt khud; voiceover_script.txt aur video_prompts.txt do parallel subagents se (dono ko yahi 12-scene list + path diya).

## Kya NAHI karna
- **Koi Word/PDF/PPT/`.docx` document mat banao** — na khud, na subagent se. `research_agent` aur document-builder tools se door raho. Is skill ka output SIRF 4 plain `.txt` files hain. Extra "docs" = bug.
- Duration ke bina scenes/words guess mat karo — pehle poochho.
- Desktop ka folder mat bhoolo; files kahin aur mat banao — sab short-naam folder ke andar.
- Voiceover aur video prompts ke scenes alag mat hone do — dono locked scene list se.
- Prompts ya narration ko "…same pattern repeat" ya "baaki khud kar lena" likh ke chhota mat karo — jitne scenes required hain, utne poore likho.
- Hook ko boring mat banao (koi "Hello guys, aaj hum baat karenge…" nahi). Outro kabhi mat chhodo.
- Subagent ko aधूra task mat do — exact path, scene list, budget sab likho, warna wo galat jagah/galat cheez bana dega.
- Facts galat mat likho — jo SERP se confirm ho wahi.
