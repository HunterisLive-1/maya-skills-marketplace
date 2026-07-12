# Video Story Studio

**Kab use karo:** Jab Boss kisi topic par video content maange — "X pe video banao", "Y minute ki video ke liye script/story banao", "voiceover aur scene prompts banao", "faceless video content", "reel/short/YouTube video ke liye clips aur narration", "AI video (Sora/Veo/Runway/Kling) ke liye prompts banao". Yeh skill ek strong story ko scene-by-scene todkar Desktop ke ek folder mein **4 plain `.txt` files** deti hai — script, scene prompts, aur do voiceover files.

## Pehle yeh confirm karo (jo Boss ne na bataya ho)
1. **Topic** — kis cheez pe video hai.
2. **Duration** — video kitni lambi (seconds/minutes). Yahi scene count decide karti hai.
3. **Voiceover ki LANGUAGE** — narration kis bhaasha mein ho (Bengali, Hindi, Urdu, English…). **Yeh zaroor poochho ya Boss ke ishaare se pakdo** — voiceover isi language mein likhni hai. Scene prompts hamesha **English** mein.
4. (Optional) Genre/tone/platform — horror, motivational, documentary, reel/short vs long. Na bataye to engaging + cinematic default.

Duration ya language na mile to **maang lo** — inke bina sahi output ban hi nahi sakta.

## Step 1 — Desktop par short-naam ka folder banao
Topic se ek **chhota (1-3 shabd) naam** nikaalo aur Desktop par usi naam ka naya folder banao ("the well that whispered after fajr" → `Whispering_Well`). Saari files isi folder ke **andar** banengi. Folder ka poora path yaad rakho (e.g. `Desktop\Whispering_Well`) — subagents ko exact path dena zaroori hai.

## Step 2 — Duration se scene count nikaalo
- **Scenes ≈ duration(seconds) ÷ 5** (har AI video clip ~5s), upar round karo. Har scene = **ek narration line + ek scene prompt**.

| Duration | ~Scenes |
|----------|---------|
| 30 sec   | ~6      |
| 60 sec   | ~12     |
| 2.5 min  | ~30     |
| 5 min    | ~60     |
| 10 min   | ~120    |

Bade video (40+ scenes) ko chunks me baanto (10-12 scenes per subagent) taaki har scene detailed rahe — kabhi "baaki same"/"repeat" mat likho, jitne scenes required utne poore.

## Step 3 — Research (SIRF jab topic factual ho)
Agar topic real/factual hai (history, science, real event) to **web/SERP search** se 5-8 verified facts nikaalo taaki story sahi rahe. ⚠️ **Research ke liye `research_agent` ya koi document-banane wala tool (Word/PDF/`.docx`) BILKUL mat use karo** — wo bekaar ka doc bana deta hai jo Boss ne maanga hi nahi. Sirf `search_web`. Fiction/horror/story topic ho to research skip — seedhe creative story likho. **Koi research.txt file mat banao** — output sirf niche wali 4 files hain.

## Step 4 — Scene list LOCK karo (sab ka source of truth)
Ek numbered **scene list** fix karo, narrative order mein, jisme har scene ki (a) narration aur (b) visual dono clear hon:
- **Scene 1 = HOOK:** pehla scene aisa ho jo turant pakad le — ek eerie image ya bold line. Boring intro nahi.
- **Beech ke scenes:** kahani ko step-by-step build karo, tension badhao, har scene ek aage badhta beat.
- **Aakhri scene = OUTRO:** satisfying/haunting close ya twist. Kabhi adhoora mat chhodo.
Yahi ek locked list se teeno files banengi taaki sab **perfectly sync** rahein (scene 5 ka prompt = scene 5 ki narration).

## Step 5 — 4 files banao (bhaari kaam SUBAGENTS se, sirf `.txt`)
Boss ne kaha "subagents ke help se" — writing subagents ko do. Subagent ke paas **koi context nahi**, isliye har subagent ke task me **poora likho:** exact folder path, topic, language, poori locked scene list (numbered, narration + visual dono), aur yeh line: **"Output SIRF plain `.txt` file `write_file` se likho — `research_agent` / Word / PDF / `.docx` koi document tool mat use karo."** Warna subagent bina maange doc bana dega.

Banane wali **4 files** (sab folder ke andar) — format bilkul isi tarah:

**1. `script.txt`** — master file. Title + numbered scenes; har scene mein narration (target language) + scene prompt (English):
```
Title: <catchy title>

1.
<Language> Voiceover: <scene 1 ki narration, target language me — hook>
Scene Prompt: <detailed English visual: subject + action + setting + camera move + lighting + mood + style, cinematic, ultra realistic, 4k>

2.
<Language> Voiceover: <scene 2 narration>
Scene Prompt: <detailed English prompt>
... (har scene ke liye, scene N tak) ...
```

**2. `video scene prompt.txt`** — sirf scene prompts, **ek line me ek prompt**, na number na label (AI video tool me seedha paste karne ke liye):
```
<scene 1 ka full English prompt>
<scene 2 ka full English prompt>
... (har scene, ek line) ...
```

**3. `voiceover_prompts.txt`** — Title + numbered voiceover lines (target language), script.txt se hu-ba-hu match:
```
Title: <title> - <Language> Voiceovers

1.
<scene 1 narration>

2.
<scene 2 narration>
... (blank line se alag, har scene) ...
```

**4. `voiceover_scene.txt`** — sirf voiceover, **ek line me ek scene**, na number na title — ek smooth, polished continuous narration (TTS/recording ready), scene order mein:
```
<scene 1 narration, thoda smooth kiya hua>
<scene 2 narration>
... (har scene ek line) ...
```

Teeno voiceover jagah (script.txt, voiceover_prompts.txt, voiceover_scene.txt) ki narration **same target language** me ho aur same scene order follow kare. Scene prompts har jagah **English** me.

## Step 6 — Report karo
Sab ban jaaye to Boss ko chhoti Hinglish line me batao: folder naam, kitne scenes bane, 4 files ready. Subagents background me hon to bolo "ban rahi hai, ho jaate hi batati hoon".

## Example
Boss: *"Fajr ke baad ek haunted kuen pe 2.5 min ki Bengali horror video banao."*
→ Folder `Desktop\Whispering_Well`. ~30 scenes. Fiction hai to research skip. Scene 1 hook: village Fajr ke baad silent, ek fisfisahat. 30 scenes tak kahani build (kuan khulta hai, aawaz, ifrit, imam, seal band). Aakhri scene outro: seal pe andar se geeli ungliyon ke nishaan. Phir 4 files — script.txt (Bengali Voiceover + English Scene Prompt per scene), video scene prompt.txt (30 English prompts, ek line each), voiceover_prompts.txt (numbered Bengali), voiceover_scene.txt (30 Bengali lines, smooth) — sab subagents se, sirf `.txt`.

## Kya NAHI karna
- **Koi Word/PDF/PPT/`.docx` mat banao** — na khud na subagent se. `research_agent` aur doc-builders se door. Output SIRF 4 plain `.txt` files. Extra "docs" = bug. Koi research.txt bhi nahi.
- Voiceover ki language guess mat karo — poochho. English me mat likho agar Boss ne doosri language maangi.
- Duration ke bina scene count guess mat karo — pehle poochho.
- Scenes ko file-to-file mismatch mat hone do — ek locked scene list se teeno files.
- "…same repeat" / "baaki khud kar lena" likh ke chhota mat karo — jitne scenes required, utne poore likho.
- Scene 1 (hook) boring mat banao; aakhri scene (outro) kabhi mat chhodo.
- Subagent ko adhoora task mat do — exact path, language, poori scene list, aur "sirf .txt, koi doc nahi" — sab likho.
