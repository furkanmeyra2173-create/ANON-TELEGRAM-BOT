const LANGUAGES = {
  tr: { name: "🇹🇷 Türkçe", choose: "🌍 Lütfen dilini seç:", welcome: "👑 ANON H4X'e hoş geldin!", menu: "Ana menü", ai: "🤖 Yapay zekâ", premium: "💎 Premium", wallet: "💰 Cüzdan", help: "ℹ️ Yardım", language: "🌍 Dil değiştir", aiIntro: "🤖 ANON H4X AI hazır! Bana soru sorabilir veya kod yazdırabilirsin.\n\nÇıkmak için /exit, sohbeti sıfırlamak için /reset yaz.", thinking: "⏳ Düşünüyorum..." },
  ku: { name: "☀️ Kurdî", choose: "🌍 Ji kerema xwe zimanê xwe hilbijêre:", welcome: "👑 Bi xêr hatî ANON H4X!", menu: "Menuya sereke", ai: "🤖 Alîkarê AI", premium: "💎 Premium", wallet: "💰 Cuzdan", help: "ℹ️ Alîkarî", language: "🌍 Ziman biguherîne", aiIntro: "🤖 ANON H4X AI amade ye! Dikare pirsan bipirsî an kodê bixwazî. Ji bo derketinê /exit, ji bo paqijkirina sohbetê /reset binivîse.", thinking: "⏳ Ez difikirim..." },
  en: { name: "🇬🇧 English", choose: "🌍 Please choose your language:", welcome: "👑 Welcome to ANON H4X!", menu: "Main menu", ai: "🤖 AI assistant", premium: "💎 Premium", wallet: "💰 Wallet", help: "ℹ️ Help", language: "🌍 Change language", aiIntro: "🤖 ANON H4X AI is ready! Ask questions or request code.\n\nUse /exit to leave AI mode or /reset to clear this chat.", thinking: "⏳ Thinking..." },
  ar: { name: "🇸🇦 العربية", choose: "🌍 يرجى اختيار لغتك:", welcome: "👑 أهلاً بك في ANON H4X!", menu: "القائمة الرئيسية", ai: "🤖 مساعد الذكاء الاصطناعي", premium: "💎 بريميوم", wallet: "💰 المحفظة", help: "ℹ️ المساعدة", language: "🌍 تغيير اللغة", aiIntro: "🤖 مساعد ANON H4X جاهز! أرسل سؤالك أو اطلب كتابة كود. /exit للخروج و /reset لمسح المحادثة.", thinking: "⏳ جارٍ التفكير..." },
  fr: { name: "🇫🇷 Français", choose: "🌍 Veuillez choisir votre langue :", welcome: "👑 Bienvenue sur ANON H4X !", menu: "Menu principal", ai: "🤖 Assistant IA", premium: "💎 Premium", wallet: "💰 Portefeuille", help: "ℹ️ Aide", language: "🌍 Changer de langue", aiIntro: "🤖 ANON H4X AI est prêt ! Posez une question ou demandez du code. /exit pour quitter, /reset pour effacer la discussion.", thinking: "⏳ Réflexion..." },
  de: { name: "🇩🇪 Deutsch", choose: "🌍 Bitte wähle deine Sprache:", welcome: "👑 Willkommen bei ANON H4X!", menu: "Hauptmenü", ai: "🤖 KI-Assistent", premium: "💎 Premium", wallet: "💰 Wallet", help: "ℹ️ Hilfe", language: "🌍 Sprache ändern", aiIntro: "🤖 ANON H4X AI ist bereit! Stelle Fragen oder fordere Code an. /exit beendet den KI-Modus, /reset löscht den Chat.", thinking: "⏳ Ich denke nach..." },
  hi: { name: "🇮🇳 हिन्दी", choose: "🌍 कृपया अपनी भाषा चुनें:", welcome: "👑 ANON H4X में आपका स्वागत है!", menu: "मुख्य मेनू", ai: "🤖 एआई सहायक", premium: "💎 प्रीमियम", wallet: "💰 वॉलेट", help: "ℹ️ सहायता", language: "🌍 भाषा बदलें", aiIntro: "🤖 ANON H4X AI तैयार है! सवाल पूछें या कोड लिखवाएँ। बाहर निकलने के लिए /exit और चैट साफ़ करने के लिए /reset लिखें।", thinking: "⏳ सोच रहा हूँ..." },
  zh: { name: "🇨🇳 中文", choose: "🌍 请选择你的语言：", welcome: "👑 欢迎来到 ANON H4X！", menu: "主菜单", ai: "🤖 AI 助手", premium: "💎 高级版", wallet: "💰 钱包", help: "ℹ️ 帮助", language: "🌍 更改语言", aiIntro: "🤖 ANON H4X AI 已就绪！可以提问或请求编写代码。发送 /exit 退出，发送 /reset 清空对话。", thinking: "⏳ 思考中..." },
  ja: { name: "🇯🇵 日本語", choose: "🌍 言語を選択してください：", welcome: "👑 ANON H4Xへようこそ！", menu: "メインメニュー", ai: "🤖 AIアシスタント", premium: "💎 プレミアム", wallet: "💰 ウォレット", help: "ℹ️ ヘルプ", language: "🌍 言語を変更", aiIntro: "🤖 ANON H4X AI の準備ができました。質問やコード作成を依頼できます。/exit で終了、/reset で会話を消去します。", thinking: "⏳ 考えています..." },
  ko: { name: "🇰🇷 한국어", choose: "🌍 언어를 선택해 주세요:", welcome: "👑 ANON H4X에 오신 것을 환영합니다!", menu: "메인 메뉴", ai: "🤖 AI 도우미", premium: "💎 프리미엄", wallet: "💰 지갑", help: "ℹ️ 도움말", language: "🌍 언어 변경", aiIntro: "🤖 ANON H4X AI가 준비되었습니다! 질문하거나 코드 작성을 요청하세요. /exit 종료, /reset 대화 초기화.", thinking: "⏳ 생각 중..." }
};

const MODEL = "gemini-2.5-flash";
const MAX_HISTORY = 12;

const PERSONALITIES = {
  friendly: { tr: "Samimi ve arkadaş canlısı", en: "Friendly and warm", instruction: "Use a warm, friendly, encouraging tone while staying accurate." },
  professional: { tr: "Profesyonel", en: "Professional", instruction: "Use a professional, respectful, clear tone. Avoid slang." },
  concise: { tr: "Kısa ve net", en: "Concise", instruction: "Keep answers concise and direct. Include only useful details." },
  detailed: { tr: "Detaylı anlatım", en: "Detailed", instruction: "Explain topics thoroughly with clear steps and examples when useful." },
  humorous: { tr: "Esprili", en: "Humorous", instruction: "Use light, tasteful humor when appropriate without sacrificing clarity or accuracy." },
  default: { tr: "Varsayılan", en: "Default", instruction: "Use a balanced, natural, helpful tone." }
};

function settingsKeyboard(lang) {
  const tr = lang === "tr";
  return { inline_keyboard: [
    [{ text: tr ? "🎭 Kişilik ayarları" : "🎭 Personality", callback_data: "settings:personality" }],
    [{ text: tr ? "🧠 Hafızayı yönet" : "🧠 Manage memory", callback_data: "settings:memory" }],
    [{ text: tr ? "⬅️ Ana menü" : "⬅️ Main menu", callback_data: "back:home" }]
  ] };
}

function personalityKeyboard(lang, current) {
  const tr = lang === "tr";
  const rows = Object.entries(PERSONALITIES).map(([key, item]) => [{
    text: `${current === key ? "✅ " : ""}${tr ? item.tr : item.en}`,
    callback_data: `personality:${key}`
  }]);
  rows.push([{ text: tr ? "⬅️ Geri" : "⬅️ Back", callback_data: "back:settings" }]);
  return { inline_keyboard: rows };
}

async function sendMemoryMenu(env, chatId, userId, lang) {
  let notes = [];
  try { notes = JSON.parse(await env.BOT_DATA.get(`memory:${userId}`) || "[]"); } catch {}
  if (!Array.isArray(notes)) notes = [];
  const tr = lang === "tr";
  const lines = notes.length
    ? notes.map((note, i) => `${i + 1}. ${String(note).slice(0, 250)}`).join("\n")
    : (tr ? "Henüz kayıtlı not yok." : "No saved notes yet.");
  const rows = notes.map((note, i) => [{
    text: tr ? `🗑️ ${i + 1}. notu sil` : `🗑️ Delete note ${i + 1}`,
    callback_data: `memdel:${i}`
  }]);
  if (notes.length) rows.push([{ text: tr ? "⚠️ Tüm hafızayı sil" : "⚠️ Delete all memory", callback_data: "memory:clear_confirm" }]);
  rows.push([{ text: tr ? "⬅️ Geri" : "⬅️ Back", callback_data: "back:settings" }]);
  await sendText(env, chatId, `🧠 ${tr ? "Hafıza yönetimi" : "Memory management"} (${notes.length}/20)\n\n${lines}`, { reply_markup: { inline_keyboard: rows } });
}


async function deleteTelegramMessage(env, chatId, messageId) {
  if (!messageId) return;
  try {
    await tg(env, "deleteMessage", { chat_id: chatId, message_id: messageId });
  } catch (error) {
    console.error("Could not delete Telegram message", error);
  }
}

async function tg(env, method, data) {
  const response = await fetch(`https://api.telegram.org/bot${env.BOT_TOKEN}/${method}`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(data)
  });
  const result = await response.json();
  if (!result.ok) console.error("Telegram API error", result);
  return result;
}

async function sendText(env, chatId, text, extra = {}) {
  const chunks = [];
  for (let i = 0; i < text.length; i += 3900) chunks.push(text.slice(i, i + 3900));
  for (const chunk of chunks) {
    await tg(env, "sendMessage", { chat_id: chatId, text: chunk, ...extra });
  }
}

function languageKeyboard() {
  const entries = Object.entries(LANGUAGES);
  const rows = [];
  for (let i = 0; i < entries.length; i += 2) {
    rows.push(entries.slice(i, i + 2).map(([code, info]) => ({
      text: info.name, callback_data: `lang:${code}`
    })));
  }
  return { inline_keyboard: rows };
}

function backToHomeKeyboard(lang) {
  const keyboard = mainKeyboard(lang);
  keyboard.inline_keyboard.push([{ text: lang === "tr" ? "⬅️ Geri" : "⬅️ Back", callback_data: "back:home" }]);
  return keyboard;
}

function mainKeyboard(lang) {
  const t = LANGUAGES[lang] || LANGUAGES.en;
  return { inline_keyboard: [
    [{ text: t.ai, callback_data: "menu:ai" }],
    [{ text: t.premium, callback_data: "menu:premium" }, { text: t.wallet, callback_data: "menu:wallet" }],
    [{ text: t.help, callback_data: "menu:help" }, { text: t.language, callback_data: "menu:language" }],
    [{ text: lang === "tr" ? "⚙️ Ayarlar" : "⚙️ Settings", callback_data: "menu:settings" }],
    [{ text: lang === "tr" ? "📁 Dosyalar" : "📁 Files", callback_data: "menu:files" }]
  ] };
}

async function getLang(env, userId) {
  return (await env.BOT_DATA.get(`lang:${userId}`)) || "en";
}

async function showHome(env, chatId, userId, lang) {
  const t = LANGUAGES[lang] || LANGUAGES.en;
  await env.BOT_DATA.put(`lang:${userId}`, lang);
  await env.BOT_DATA.delete(`mode:${userId}`);
  const keyboard = mainKeyboard(lang);
  if (String(userId) === String(env.ADMIN_ID || "")) {
    keyboard.inline_keyboard.push([{ text: "👑 Özel / Yönetici", callback_data: "menu:admin" }]);
  }
  await sendText(env, chatId, `${t.welcome}\n\n${t.menu}`, { reply_markup: keyboard });
}


function getAutoMemoryNote(text) {
  const value = text.trim();
  const lower = value.toLocaleLowerCase();
  const triggers = [
    "bunu hatırla", "bunu hafızana kaydet", "aklında tut", "unutma ki",
    "benim adım ", "adım ", "bana ... diye hitap et",
    "tercih ederim", "tercihim ", "sevdiğim ", "en sevdiğim",
    "remember that", "please remember", "keep in mind", "my name is ",
    "i am called ", "i prefer ", "my preference is", "i like ",
    "ich heiße ", "merk dir", "bitte erinnere dich", "je m'appelle ",
    "souviens-toi", "اسمي ", "تذكر أن", "یاد رکھو", "میرا نام",
    "私の名前は", "覚えておいて", "我叫", "请记住", "제 이름은", "기억해",
    "navê min "
  ];
  if (!triggers.some(phrase => lower.includes(phrase.toLocaleLowerCase()))) return null;
  if (value.length > 300) return null;

  // Never store credentials, financial details, or sensitive personal data automatically.
  const sensitive = /(password|passcode|secret|api[ _-]?key|token|private[ _-]?key|şifre|parola|gizli anahtar|iban|kredi kart|banka hesab|telefon numaram|adresim|hastalığım|teşhis|ilaç kullan|dinim|mezhebim|siyasi görüş|cinsel|ırkım)/i;
  if (sensitive.test(value)) return null;
  return value;
}

async function saveAutoMemory(env, userId, note) {
  if (!note) return false;
  let notes = [];
  try { notes = JSON.parse(await env.BOT_DATA.get(`memory:${userId}`) || "[]"); } catch {}
  if (!Array.isArray(notes)) notes = [];
  const normalized = note.toLocaleLowerCase();
  if (notes.some(item => String(item).toLocaleLowerCase() === normalized)) return false;
  if (notes.length >= 20) return false;
  notes.push(note);
  await env.BOT_DATA.put(`memory:${userId}`, JSON.stringify(notes));
  return true;
}

async function callGemini(env, userId, lang, userText) {
  const historyKey = `history:${userId}`;
  let history = [];
  try { history = JSON.parse(await env.BOT_DATA.get(historyKey) || "[]"); } catch {}
  history.push({ role: "user", parts: [{ text: userText }] });
  history = history.slice(-MAX_HISTORY);

  const languageName = ({ tr:"Turkish", ku:"Kurdish (Kurmanji)", en:"English", ar:"Arabic", fr:"French", de:"German", hi:"Hindi", zh:"Chinese", ja:"Japanese", ko:"Korean" })[lang] || "English";
  let personalMemory = [];
  try { personalMemory = JSON.parse(await env.BOT_DATA.get(`memory:${userId}`) || "[]"); } catch {}
  const memoryContext = personalMemory.length
    ? `\n\nUser-approved personal memory (use only when relevant; do not assume anything beyond these notes):\n- ${personalMemory.join("\n- ")}`
    : "";
  const personalityKey = (await env.BOT_DATA.get(`personality:${userId}`)) || "default";
  const personality = PERSONALITIES[personalityKey] || PERSONALITIES.default;
  const systemInstruction = `You are ANON H4X AI, a helpful, accurate assistant. Reply in ${languageName} unless the user asks for another language. ${personality.instruction} You can explain concepts and write, debug, and review code in common programming languages. When providing code, use clear Markdown code fences with the correct language label, explain how to use it briefly, and never claim code was tested unless it actually was. Be honest about uncertainty. Do not assist with malware, credential theft, account compromise, or harmful cyber abuse; offer safe defensive alternatives.${memoryContext}`;

  const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent`, {
    method: "POST",
    headers: {
      "content-type": "application/json",
      "x-goog-api-key": env.GEMINI_API_KEY
    },
    body: JSON.stringify({
      systemInstruction: { parts: [{ text: systemInstruction }] },
      contents: history,
      generationConfig: { temperature: 0.7, maxOutputTokens: 1800 }
    })
  });

  const data = await response.json();
  if (!response.ok) {
    console.error("Gemini API error", response.status, data);
    if (response.status === 429) throw new Error("LIMIT");
    if (response.status === 400 || response.status === 403) throw new Error("KEY");
    throw new Error("API");
  }

  const answer = data.candidates?.[0]?.content?.parts
    ?.map(part => part.text || "").join("").trim();
  if (!answer) throw new Error("EMPTY");

  history.push({ role: "model", parts: [{ text: answer }] });
  await env.BOT_DATA.put(historyKey, JSON.stringify(history.slice(-MAX_HISTORY)));
  return answer;
}


async function getStoredFiles(env) {
  try {
    const files = JSON.parse(await env.BOT_DATA.get("public:files") || "[]");
    return Array.isArray(files) ? files : [];
  } catch { return []; }
}

async function sendFilesMenu(env, chatId, userId, lang) {
  const files = await getStoredFiles(env);
  const tr = lang === "tr";
  if (!files.length) {
    await sendText(env, chatId, tr ? "📁 Henüz paylaşılmış dosya yok." : "📁 No files have been shared yet.", {
      reply_markup: { inline_keyboard: [[{ text: tr ? "⬅️ Ana menü" : "⬅️ Main menu", callback_data: "back:home" }]] }
    });
    return;
  }
  const rows = files.slice(0, 50).map((file, index) => [{
    text: `📄 ${String(file.name || "Dosya").slice(0, 55)}`,
    callback_data: `file:get:${index}`
  }]);
  rows.push([{ text: tr ? "⬅️ Ana menü" : "⬅️ Main menu", callback_data: "back:home" }]);
  await sendText(env, chatId, tr ? `📁 Paylaşılan dosyalar (${files.length})\nİndirmek istediğin dosyaya dokun:` : `📁 Shared files (${files.length})\nTap a file to download:`, {
    reply_markup: { inline_keyboard: rows }
  });
}

async function saveIncomingDocument(msg, env, customName = "") {
  const doc = msg.document;
  if (!doc?.file_id) return false;
  const files = await getStoredFiles(env);
  const name = String(customName || doc.file_name || "dosya").trim().slice(0, 180);
  const entry = {
    name,
    file_id: doc.file_id,
    file_unique_id: doc.file_unique_id || "",
    size: doc.file_size || 0,
    mime_type: doc.mime_type || "",
    caption: String(msg.caption || "").slice(0, 500),
    updated_at: new Date().toISOString()
  };
  const existing = files.findIndex(item => String(item.name).toLocaleLowerCase() === entry.name.toLocaleLowerCase());
  if (existing >= 0) files[existing] = entry;
  else files.unshift(entry);
  await env.BOT_DATA.put("public:files", JSON.stringify(files.slice(0, 100)));
  return existing >= 0;
}

async function sendAdminPanel(env, chatId, lang) {
  const tr = lang === "tr";
  await sendText(env, chatId, tr ? "👑 Yönetici paneli\nDosya eklemek için önce dosya adını belirle." : "👑 Admin panel\nChoose a name before uploading a file.", {
    reply_markup: { inline_keyboard: [
      [{ text: tr ? "➕ Yeni dosya ekle / güncelle" : "➕ Add / update file", callback_data: "admin:file:add" }],
      [{ text: tr ? "🗂 Dosyaları yönet" : "🗂 Manage files", callback_data: "admin:file:list" }],
      [{ text: tr ? "⬅️ Ana menü" : "⬅️ Main menu", callback_data: "back:home" }]
    ] }
  });
}

async function sendAdminFiles(env, chatId, lang) {
  const files = await getStoredFiles(env);
  const tr = lang === "tr";
  const rows = files.map((file, index) => [
    { text: `📄 ${String(file.name).slice(0, 35)}`, callback_data: `admin:file:noop:${index}` },
    { text: tr ? "🗑 Sil" : "🗑 Delete", callback_data: `admin:file:del:${index}` }
  ]);
  rows.push([{ text: tr ? "⬅️ Geri" : "⬅️ Back", callback_data: "menu:admin" }]);
  await sendText(env, chatId, tr ? `🗂 Dosyaların (${files.length})` : `🗂 Your files (${files.length})`, {
    reply_markup: { inline_keyboard: rows.length ? rows : [[{ text: tr ? "Henüz dosya yok" : "No files yet", callback_data: "menu:admin" }]] }
  });
}

async function handleUpdate(update, env) {
  if (update.message) {
    const msg = update.message;
    if (!msg.from || !msg.chat || (!msg.text && !msg.document)) return;
    const userId = msg.from.id;
    const chatId = msg.chat.id;
    const text = (msg.text || "").trim();

    if (text && String(userId) === String(env.ADMIN_ID || "") && await env.BOT_DATA.get(`admin_step:${userId}`) === "file_name") {
      const name = text.trim().slice(0, 180);
      if (!name) {
        await sendText(env, chatId, "Dosya adı boş olamaz. Tekrar yaz.");
        return;
      }
      await env.BOT_DATA.put(`pending_file_name:${userId}`, name);
      await env.BOT_DATA.put(`admin_step:${userId}`, "file_upload");
      const oldPromptId = await env.BOT_DATA.get(`admin_prompt:${userId}`);
      if (oldPromptId) await deleteTelegramMessage(env, chatId, Number(oldPromptId));
      await deleteTelegramMessage(env, chatId, msg.message_id);
      const prompt = await tg(env, "sendMessage", {
        chat_id: chatId,
        text: `📎 Dosya adı: “${name}”\nŞimdi dosyanın kendisini belge olarak gönder.`,
        reply_markup: { inline_keyboard: [[{ text: "❌ İptal", callback_data: "admin:file:cancel" }]] }
      });
      if (prompt?.result?.message_id) await env.BOT_DATA.put(`admin_prompt:${userId}`, String(prompt.result.message_id));
      return;
    }

    if (msg.document) {
      if (String(userId) !== String(env.ADMIN_ID || "")) {
        await sendText(env, chatId, "⛔ Bu işlem yalnızca bot yöneticisi tarafından yapılabilir.");
        return;
      }
      const pendingName = await env.BOT_DATA.get(`pending_file_name:${userId}`);
      if (!pendingName) {
        await sendText(env, chatId, "Önce 👑 Yönetici panelinden dosya adı belirle.");
        return;
      }
      const replaced = await saveIncomingDocument(msg, env, pendingName);
      await env.BOT_DATA.delete(`pending_file_name:${userId}`);
      await env.BOT_DATA.delete(`admin_step:${userId}`);
      const promptId = await env.BOT_DATA.get(`admin_prompt:${userId}`);
      if (promptId) await deleteTelegramMessage(env, chatId, Number(promptId));
      await env.BOT_DATA.delete(`admin_prompt:${userId}`);
      await deleteTelegramMessage(env, chatId, msg.message_id);
      await sendText(env, chatId, replaced
        ? `♻️ “${pendingName}” dosyası güncellendi. Kullanıcılar Dosyalar bölümünden erişebilir.`
        : `✅ “${pendingName}” dosyası kaydedildi. Kullanıcılar Dosyalar bölümünden erişebilir.`, {
          reply_markup: { inline_keyboard: [[{ text: "👑 Yönetici paneli", callback_data: "menu:admin" }]] }
        });
      return;
    }

    if (text === "/myid") {
      await sendText(env, chatId, `Telegram kullanıcı ID'n: ${userId}\nBunu Cloudflare'da ADMIN_ID secret olarak kaydet.`);
      return;
    }

    if (text === "/files") {
      await sendFilesMenu(env, chatId, userId, await getLang(env, userId));
      return;
    }

    if (text === "/start" || text === "/language") {
      await env.BOT_DATA.delete(`mode:${userId}`);
      const lang = await getLang(env, userId);
      await sendText(env, chatId, LANGUAGES[lang].choose, { reply_markup: languageKeyboard() });
      return;
    }

    if (text === "/settings" || text === "/personality") {
      const lang = await getLang(env, userId);
      await sendText(env, chatId, lang === "tr" ? "⚙️ Kişisel ayarların" : "⚙️ Personal settings", { reply_markup: settingsKeyboard(lang) });
      return;
    }

    if (text === "/help") {
      const lang = await getLang(env, userId);
      await sendText(env, chatId, "Commands: /start, /language, /help, /exit, /reset, /remember <note>, /memory, /forget, /settings, /files, /myid");
      return;
    }

    if (text === "/exit") {
      await env.BOT_DATA.delete(`mode:${userId}`);
      await showHome(env, chatId, userId, await getLang(env, userId));
      return;
    }

    if (text === "/reset") {
      await env.BOT_DATA.delete(`history:${userId}`);
      const lang = await getLang(env, userId);
      await sendText(env, chatId, lang === "tr" ? "🧹 Sohbet geçmişin temizlendi. Kişisel hafızan korunuyor; silmek için /forget yaz." : "🧹 Chat history cleared. Personal memory is kept; use /forget to erase it.");
      return;
    }

    if (text.startsWith("/remember")) {
      const note = text.slice("/remember".length).trim();
      const lang = await getLang(env, userId);
      if (!note) {
        await sendText(env, chatId, lang === "tr" ? "Kullanım: /remember sevdiğim dil Türkçe\nYalnızca kaydetmek istediğin, hassas olmayan bilgileri yaz. Şifre veya gizli anahtar kaydetme." : "Usage: /remember I prefer Turkish\nSave only non-sensitive information you choose to remember. Never save passwords or secret keys.");
        return;
      }
      if (note.length > 300) {
        await sendText(env, chatId, lang === "tr" ? "⚠️ Her hafıza notu en fazla 300 karakter olabilir." : "⚠️ Each memory note can be up to 300 characters.");
        return;
      }
      let notes = [];
      try { notes = JSON.parse(await env.BOT_DATA.get(`memory:${userId}`) || "[]"); } catch {}
      const normalized = note.toLocaleLowerCase();
      if (!notes.some(item => String(item).toLocaleLowerCase() === normalized)) {
        if (notes.length >= 20) {
          await sendText(env, chatId, lang === "tr" ? "Hafıza dolu (20 not). Önce /forget ile temizleyebilirsin." : "Memory is full (20 notes). Use /forget to clear it first.");
          return;
        }
        notes.push(note);
        await env.BOT_DATA.put(`memory:${userId}`, JSON.stringify(notes));
      }
      await sendText(env, chatId, lang === "tr" ? "🧠 Bunu kişisel hafızana kaydettim. Görmek için /memory, silmek için /forget." : "🧠 Saved to your personal memory. Use /memory to view it or /forget to erase it.");
      return;
    }

    if (text === "/memory") {
      const lang = await getLang(env, userId);
      await sendMemoryMenu(env, chatId, userId, lang);
      return;
    }

    if (text === "/forget") {
      await env.BOT_DATA.delete(`memory:${userId}`);
      const lang = await getLang(env, userId);
      await sendText(env, chatId, lang === "tr" ? "🗑️ Kişisel hafızandaki tüm notlar silindi." : "🗑️ All personal memory notes have been deleted.");
      return;
    }

    const lang = await getLang(env, userId);
    const mode = await env.BOT_DATA.get(`mode:${userId}`);
    if (mode !== "ai") {
      await sendText(env, chatId, LANGUAGES[lang].choose, { reply_markup: languageKeyboard() });
      return;
    }

    if (!env.GEMINI_API_KEY) {
      await sendText(env, chatId, "⚠️ GEMINI_API_KEY secret is missing in Cloudflare.");
      return;
    }

    const autoNote = getAutoMemoryNote(text);
    const autoSaved = autoNote ? await saveAutoMemory(env, userId, autoNote) : false;
    if (autoSaved) {
      await sendText(env, chatId, lang === "tr"
        ? "🧠 Bu bilgiyi kişisel hafızana otomatik olarak kaydettim. Görmek için /memory, silmek için /forget."
        : "🧠 I automatically saved this to your personal memory. Use /memory to view it or /forget to erase it.");
    }

    await tg(env, "sendChatAction", { chat_id: chatId, action: "typing" });
    try {
      const answer = await callGemini(env, userId, lang, text);
      await sendText(env, chatId, answer);
    } catch (error) {
      const errText = error.message === "LIMIT"
        ? "⏳ Gemini ücretsiz kullanım limiti dolmuş olabilir. Bir süre sonra tekrar dene."
        : error.message === "KEY"
          ? "🔑 Gemini API anahtarı geçersiz veya API erişimi kapalı. Cloudflare Secret ayarını kontrol et."
          : "⚠️ AI şu anda yanıt veremedi. Biraz sonra tekrar dene.";
      await sendText(env, chatId, errText);
    }
    return;
  }

  if (update.callback_query) {
    const q = update.callback_query;
    const userId = q.from.id;
    const chatId = q.message.chat.id;
    const data = q.data || "";
    await tg(env, "answerCallbackQuery", { callback_query_id: q.id });
    // Remove the screen that launched this action; the next screen/result replaces it.
    await deleteTelegramMessage(env, chatId, q.message?.message_id);
    const lang = await getLang(env, userId);
    const tr = lang === "tr";

    if (data === "menu:admin") {
      if (String(userId) !== String(env.ADMIN_ID || "")) {
        await sendText(env, chatId, "⛔ Yetkin yok.");
        return;
      }
      await sendAdminPanel(env, chatId, lang);
      return;
    }
    if (data === "admin:file:add") {
      if (String(userId) !== String(env.ADMIN_ID || "")) return;
      await env.BOT_DATA.put(`admin_step:${userId}`, "file_name");
      await env.BOT_DATA.delete(`pending_file_name:${userId}`);
      const prompt = await tg(env, "sendMessage", {
        chat_id: chatId,
        text: "✍️ Önce dosyanın kullanıcıların göreceği adını yaz. Örnek: ANON H4X v2.0",
        reply_markup: { inline_keyboard: [[{ text: "❌ İptal", callback_data: "admin:file:cancel" }]] }
      });
      if (prompt?.result?.message_id) await env.BOT_DATA.put(`admin_prompt:${userId}`, String(prompt.result.message_id));
      return;
    }
    if (data === "admin:file:list") {
      if (String(userId) !== String(env.ADMIN_ID || "")) return;
      await sendAdminFiles(env, chatId, lang);
      return;
    }
    if (data.startsWith("admin:file:noop:")) return;
    if (data.startsWith("admin:file:del:")) {
      if (String(userId) !== String(env.ADMIN_ID || "")) return;
      const index = Number(data.split(":")[3]);
      const files = await getStoredFiles(env);
      if (Number.isInteger(index) && index >= 0 && index < files.length) {
        files.splice(index, 1);
        await env.BOT_DATA.put("public:files", JSON.stringify(files));
      }
      await sendAdminFiles(env, chatId, lang);
      return;
    }
    if (data === "admin:file:cancel") {
      if (String(userId) !== String(env.ADMIN_ID || "")) return;
      await env.BOT_DATA.delete(`admin_step:${userId}`);
      await env.BOT_DATA.delete(`pending_file_name:${userId}`);
      const promptId = await env.BOT_DATA.get(`admin_prompt:${userId}`);
      if (promptId) await deleteTelegramMessage(env, chatId, Number(promptId));
      await env.BOT_DATA.delete(`admin_prompt:${userId}`);
      await sendAdminPanel(env, chatId, lang);
      return;
    }

    if (data.startsWith("file:get:")) {
      const index = Number(data.split(":")[2]);
      const files = await getStoredFiles(env);
      if (!Number.isInteger(index) || index < 0 || index >= files.length) {
        await sendText(env, chatId, tr ? "Dosya bulunamadı; /files ile listeyi yenile." : "File not found; refresh with /files.");
        return;
      }
      const file = files[index];
      await tg(env, "sendDocument", {
        chat_id: chatId,
        document: file.file_id,
        caption: file.caption || file.name
      });
      return;
    }

    if (data.startsWith("back:")) {
      const target = data.slice("back:".length);
      if (target === "home") {
        await showHome(env, chatId, userId, lang);
      } else if (target === "settings") {
        await sendText(env, chatId, tr ? "⚙️ Kişisel ayarların" : "⚙️ Personal settings", { reply_markup: settingsKeyboard(lang) });
      } else if (target === "memory") {
        await sendMemoryMenu(env, chatId, userId, lang);
      }
      return;
    }

    if (data.startsWith("lang:")) {
      const lang = data.split(":")[1];
      if (LANGUAGES[lang]) await showHome(env, chatId, userId, lang);
      return;
    }

    const t = LANGUAGES[lang];

    if (data === "menu:files") {
      await sendFilesMenu(env, chatId, userId, lang);
      return;
    }
    if (data === "menu:settings") {
      await sendText(env, chatId, tr ? "⚙️ Kişisel ayarların" : "⚙️ Personal settings", { reply_markup: settingsKeyboard(lang) });
      return;
    }
    if (data === "settings:personality") {
      const current = (await env.BOT_DATA.get(`personality:${userId}`)) || "default";
      const label = PERSONALITIES[current] || PERSONALITIES.default;
      await sendText(env, chatId, `${tr ? "🎭 Mevcut kişiliğin" : "🎭 Current personality"}: ${tr ? label.tr : label.en}\n${tr ? "Bir tarz seç:" : "Choose a style:"}`, { reply_markup: personalityKeyboard(lang, current) });
      return;
    }
    if (data.startsWith("personality:")) {
      const selected = data.split(":")[1];
      if (!PERSONALITIES[selected]) return;
      await env.BOT_DATA.put(`personality:${userId}`, selected);
      const label = PERSONALITIES[selected];
      await sendText(env, chatId, tr ? `✅ Kişilik ayarın: ${label.tr}` : `✅ Personality set to: ${label.en}`, { reply_markup: personalityKeyboard(lang, selected) });
      return;
    }
    if (data === "settings:memory") {
      await sendMemoryMenu(env, chatId, userId, lang);
      return;
    }
    if (data.startsWith("memdel:")) {
      const index = Number(data.split(":")[1]);
      let notes = [];
      try { notes = JSON.parse(await env.BOT_DATA.get(`memory:${userId}`) || "[]"); } catch {}
      if (Array.isArray(notes) && Number.isInteger(index) && index >= 0 && index < notes.length) {
        notes.splice(index, 1);
        if (notes.length) await env.BOT_DATA.put(`memory:${userId}`, JSON.stringify(notes));
        else await env.BOT_DATA.delete(`memory:${userId}`);
      }
      await sendMemoryMenu(env, chatId, userId, lang);
      return;
    }
    if (data === "memory:clear_confirm") {
      await sendText(env, chatId, tr ? "⚠️ Tüm kişisel hafıza notlarını silmek istiyor musun?" : "⚠️ Delete all personal memory notes?", { reply_markup: { inline_keyboard: [
        [{ text: tr ? "Evet, hepsini sil" : "Yes, delete all", callback_data: "memory:clear_yes" }],
        [{ text: tr ? "⬅️ Geri" : "⬅️ Back", callback_data: "back:memory" }]
      ] } });
      return;
    }
    if (data === "memory:clear_yes") {
      await env.BOT_DATA.delete(`memory:${userId}`);
      await sendMemoryMenu(env, chatId, userId, lang);
      return;
    }

    if (data === "menu:ai") {
      await env.BOT_DATA.put(`mode:${userId}`, "ai");
      await sendText(env, chatId, t.aiIntro, { reply_markup: { inline_keyboard: [[{ text: lang === "tr" ? "⬅️ Ana menü" : "⬅️ Main menu", callback_data: "back:home" }]] } });
      return;
    }
    if (data === "menu:language") {
      await env.BOT_DATA.delete(`mode:${userId}`);
      await sendText(env, chatId, t.choose, { reply_markup: languageKeyboard() });
      return;
    }
    if (data === "menu:wallet") {
      const balance = await env.BOT_DATA.get(`wallet:${userId}`) || "0";
      await sendText(env, chatId, `${t.wallet}: ${balance}`, { reply_markup: backToHomeKeyboard(lang) });
      return;
    }
    if (data === "menu:premium") {
      await sendText(env, chatId, "💎 Premium sistemi henüz etkinleştirilmedi.", { reply_markup: backToHomeKeyboard(lang) });
      return;
    }
    if (data === "menu:help") {
      await sendText(env, chatId, "ℹ️ /start — Menü\n/language — Dil değiştir\n/exit — AI modundan çık\n/reset — Sohbet geçmişini temizle\n/remember <bilgi> — Kişisel hafızaya kaydet\n/memory — Hafızayı görüntüle\n/forget — Kişisel hafızayı sil\n/settings — Kişilik ve hafıza ayarları", { reply_markup: backToHomeKeyboard(lang) });
      return;
    }
  }
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === "/setup" && request.method === "GET") {
      if (!env.SETUP_KEY || url.searchParams.get("key") !== env.SETUP_KEY) {
        return new Response("Unauthorized", { status: 401 });
      }
      const result = await tg(env, "setWebhook", { url: `${url.origin}/` });
      return Response.json(result);
    }

    if (request.method === "GET") return new Response("ANON H4X AI bot is running.");
    if (request.method !== "POST") return new Response("Method not allowed", { status: 405 });

    try {
      const update = await request.json();
      await handleUpdate(update, env);
      return new Response("OK");
    } catch (error) {
      console.error("Update handling failed", error);
      return new Response("Internal error", { status: 500 });
    }
  }
};
