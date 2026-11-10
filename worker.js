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

function mainKeyboard(lang) {
  const t = LANGUAGES[lang] || LANGUAGES.en;
  return { inline_keyboard: [
    [{ text: t.ai, callback_data: "menu:ai" }],
    [{ text: t.premium, callback_data: "menu:premium" }, { text: t.wallet, callback_data: "menu:wallet" }],
    [{ text: t.help, callback_data: "menu:help" }, { text: t.language, callback_data: "menu:language" }]
  ] };
}

async function getLang(env, userId) {
  return (await env.BOT_DATA.get(`lang:${userId}`)) || "en";
}

async function showHome(env, chatId, userId, lang) {
  const t = LANGUAGES[lang] || LANGUAGES.en;
  await env.BOT_DATA.put(`lang:${userId}`, lang);
  await env.BOT_DATA.delete(`mode:${userId}`);
  await sendText(env, chatId, `${t.welcome}\n\n${t.menu}`, { reply_markup: mainKeyboard(lang) });
}

async function callGemini(env, userId, lang, userText) {
  const historyKey = `history:${userId}`;
  let history = [];
  try { history = JSON.parse(await env.BOT_DATA.get(historyKey) || "[]"); } catch {}
  history.push({ role: "user", parts: [{ text: userText }] });
  history = history.slice(-MAX_HISTORY);

  const languageName = ({ tr:"Turkish", ku:"Kurdish (Kurmanji)", en:"English", ar:"Arabic", fr:"French", de:"German", hi:"Hindi", zh:"Chinese", ja:"Japanese", ko:"Korean" })[lang] || "English";
  const systemInstruction = `You are ANON H4X AI, a helpful, accurate assistant. Reply in ${languageName} unless the user asks for another language. You can explain concepts and write, debug, and review code in common programming languages. When providing code, use clear Markdown code fences with the correct language label, explain how to use it briefly, and never claim code was tested unless it actually was. Be honest about uncertainty. Do not assist with malware, credential theft, account compromise, or harmful cyber abuse; offer safe defensive alternatives.`;

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

async function handleUpdate(update, env) {
  if (update.message) {
    const msg = update.message;
    if (!msg.from || !msg.chat || !msg.text) return;
    const userId = msg.from.id;
    const chatId = msg.chat.id;
    const text = msg.text.trim();

    if (text === "/start" || text === "/language") {
      await env.BOT_DATA.delete(`mode:${userId}`);
      const lang = await getLang(env, userId);
      await sendText(env, chatId, LANGUAGES[lang].choose, { reply_markup: languageKeyboard() });
      return;
    }

    if (text === "/help") {
      const lang = await getLang(env, userId);
      await sendText(env, chatId, "Commands: /start, /language, /help, /exit, /reset");
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
      await sendText(env, chatId, lang === "tr" ? "🧹 Sohbet geçmişin temizlendi." : "🧹 Chat history cleared.");
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

    if (data.startsWith("lang:")) {
      const lang = data.split(":")[1];
      if (LANGUAGES[lang]) await showHome(env, chatId, userId, lang);
      return;
    }

    const lang = await getLang(env, userId);
    const t = LANGUAGES[lang];

    if (data === "menu:ai") {
      await env.BOT_DATA.put(`mode:${userId}`, "ai");
      await sendText(env, chatId, t.aiIntro);
      return;
    }
    if (data === "menu:language") {
      await env.BOT_DATA.delete(`mode:${userId}`);
      await sendText(env, chatId, t.choose, { reply_markup: languageKeyboard() });
      return;
    }
    if (data === "menu:wallet") {
      const balance = await env.BOT_DATA.get(`wallet:${userId}`) || "0";
      await sendText(env, chatId, `${t.wallet}: ${balance}`, { reply_markup: mainKeyboard(lang) });
      return;
    }
    if (data === "menu:premium") {
      await sendText(env, chatId, "💎 Premium sistemi henüz etkinleştirilmedi.", { reply_markup: mainKeyboard(lang) });
      return;
    }
    if (data === "menu:help") {
      await sendText(env, chatId, "ℹ️ /start — Menü\n/language — Dil değiştir\n/exit — AI modundan çık\n/reset — AI sohbetini temizle", { reply_markup: mainKeyboard(lang) });
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
