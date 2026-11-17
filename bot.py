import logging
import os
import sqlite3
import shutil
import re
import asyncio
from pathlib import Path
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

BOT_NAME = "ANON H4X"
DB_PATH = Path(os.getenv("DATABASE_PATH", "anon_h4x.db"))
ADMIN_IDS = {
    int(value.strip())
    for value in os.getenv("ADMIN_IDS", "").split(",")
    if value.strip().isdigit()
}

LANGUAGES = {
    "tr": {"name": "🇹🇷 Türkçe", "welcome": "👑 ANON H4X'e hoş geldin!", "choose": "🌍 Lütfen dilini seç:", "menu": "Ana menü", "ai": "🤖 Yapay zekâ", "admin": "🛡️ Yönetim paneli", "premium": "💎 Premium", "wallet": "💰 Cüzdan", "help": "ℹ️ Yardım", "language": "🌍 Dil değiştir", "apktool": "🔧 APK TOOL", "soon": "Bu bölüm üzerinde çalışıyoruz. Yakında burada olacak!"},
    "ku": {"name": "🟡 Kurdî", "welcome": "👑 Bi xêr hatî ANON H4X!", "choose": "🌍 Ji kerema xwe zimanê xwe hilbijêre:", "menu": "Menuya sereke", "ai": "🤖 A.I.", "admin": "🛡️ Panela rêveberiyê", "premium": "💎 Premium", "wallet": "💰 Cuzdan", "help": "ℹ️ Alîkarî", "language": "🌍 Ziman biguherîne", "apktool": "🔧 APK TOOL", "soon": "Em li ser vê beşê dixebitin. Zû dê were!"},
    "en": {"name": "🇬🇧 English", "welcome": "👑 Welcome to ANON H4X!", "choose": "🌍 Please choose your language:", "menu": "Main menu", "ai": "🤖 AI assistant", "admin": "🛡️ Admin panel", "premium": "💎 Premium", "wallet": "💰 Wallet", "help": "ℹ️ Help", "language": "🌍 Change language", "apktool": "🔧 APK TOOL", "soon": "This section is under development. Coming soon!"},
    "ar": {"name": "🇸🇦 العربية", "welcome": "👑 أهلاً بك في ANON H4X!", "choose": "🌍 يرجى اختيار لغتك:", "menu": "القائمة الرئيسية", "ai": "🤖 الذكاء الاصطناعي", "admin": "🛡️ لوحة الإدارة", "premium": "💎 بريميوم", "wallet": "💰 المحفظة", "help": "ℹ️ المساعدة", "language": "🌍 تغيير اللغة", "apktool": "🔧 APK TOOL", "soon": "هذا القسم قيد التطوير. قريباً!"},
    "fr": {"name": "🇫🇷 Français", "welcome": "👑 Bienvenue sur ANON H4X !", "choose": "🌍 Veuillez choisir votre langue :", "menu": "Menu principal", "ai": "🤖 Assistant IA", "admin": "🛡️ Panneau admin", "premium": "💎 Premium", "wallet": "💰 Portefeuille", "help": "ℹ️ Aide", "language": "🌍 Changer de langue", "apktool": "🔧 APK TOOL", "soon": "Cette section est en cours de développement. Bientôt !"},
    "de": {"name": "🇩🇪 Deutsch", "welcome": "👑 Willkommen bei ANON H4X!", "choose": "🌍 Bitte wähle deine Sprache:", "menu": "Hauptmenü", "ai": "🤖 KI-Assistent", "admin": "🛡️ Admin-Panel", "premium": "💎 Premium", "wallet": "💰 Wallet", "help": "ℹ️ Hilfe", "language": "🌍 Sprache ändern", "apktool": "🔧 APK TOOL", "soon": "Dieser Bereich wird gerade entwickelt. Demnächst verfügbar!"},
    "hi": {"name": "🇮🇳 हिन्दी", "welcome": "👑 ANON H4X में आपका स्वागत है!", "choose": "🌍 कृपया अपनी भाषा चुनें:", "menu": "मुख्य मेनू", "ai": "🤖 एआई सहायक", "admin": "🛡️ एडमिन पैनल", "premium": "💎 प्रीमियम", "wallet": "💰 वॉलेट", "help": "ℹ️ सहायता", "language": "🌍 भाषा बदलें", "apktool": "🔧 APK TOOL", "soon": "यह अनुभाग विकासाधीन है। जल्द आ रहा है!"},
    "zh": {"name": "🇨🇳 中文", "welcome": "👑 欢迎来到 ANON H4X！", "choose": "🌍 请选择你的语言：", "menu": "主菜单", "ai": "🤖 AI 助手", "admin": "🛡️ 管理面板", "premium": "💎 高级版", "wallet": "💰 钱包", "help": "ℹ️ 帮助", "language": "🌍 更改语言", "apktool": "🔧 APK TOOL", "soon": "此功能正在开发中，敬请期待！"},
    "ja": {"name": "🇯🇵 日本語", "welcome": "👑 ANON H4Xへようこそ！", "choose": "🌍 言語を選択してください：", "menu": "メインメニュー", "ai": "🤖 AIアシスタント", "admin": "🛡️ 管理パネル", "premium": "💎 プレミアム", "wallet": "💰 ウォレット", "help": "ℹ️ ヘルプ", "language": "🌍 言語を変更", "apktool": "🔧 APK TOOL", "soon": "この機能は開発中です。近日公開！"},
    "ko": {"name": "🇰🇷 한국어", "welcome": "👑 ANON H4X에 오신 것을 환영합니다!", "choose": "🌍 언어를 선택해 주세요:", "menu": "메인 메뉴", "ai": "🤖 AI 도우미", "admin": "🛡️ 관리자 패널", "premium": "💎 프리미엄", "wallet": "💰 지갑", "help": "ℹ️ 도움말", "language": "🌍 언어 변경", "apktool": "🔧 APK TOOL", "soon": "이 기능은 개발 중입니다. 곧 공개됩니다!"},
}

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("anon-h4x")

UPLOAD_APK, CHOOSE_ACTION, NEW_APP_NAME, NEW_PACKAGE_NAME = range(4)
WORK_DIR = "/tmp/anon_apk_tool"
os.makedirs(WORK_DIR, exist_ok=True)

def db():
    connection = sqlite3.connect(DB_PATH)
    connection.execute(
        """CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            language TEXT NOT NULL DEFAULT 'en',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS wallets (
            user_id INTEGER PRIMARY KEY,
            credits INTEGER NOT NULL DEFAULT 0
        )"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS memberships (
            user_id INTEGER PRIMARY KEY,
            tier TEXT NOT NULL DEFAULT 'free',
            expires_at TEXT
        )"""
    )
    connection.commit()
    return connection

def get_language(user_id: int) -> str | None:
    with db() as connection:
        row = connection.execute(
            "SELECT language FROM users WHERE user_id = ?", (user_id,)
        ).fetchone()
        return row[0] if row else None

def save_language(user_id: int, language: str) -> None:
    with db() as connection:
        connection.execute(
            """INSERT INTO users (user_id, language) VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET language = excluded.language""",
            (user_id, language),
        )
        connection.execute(
            "INSERT OR IGNORE INTO wallets (user_id) VALUES (?)", (user_id,)
        )
        connection.execute(
            "INSERT OR IGNORE INTO memberships (user_id) VALUES (?)", (user_id,)
        )

def language_keyboard():
    rows = []
    buttons = [
        InlineKeyboardButton(info["name"], callback_data=f"lang:{code}")
        for code, info in LANGUAGES.items()
    ]
    for index in range(0, len(buttons), 2):
        rows.append(buttons[index : index + 2])
    return InlineKeyboardMarkup(rows)

def main_keyboard(language: str, user_id: int):
    labels = LANGUAGES[language]
    rows = [
        [InlineKeyboardButton(labels["ai"], callback_data="menu:ai")],
        [InlineKeyboardButton(labels["apktool"], callback_data="menu:apktool")],
        [
            InlineKeyboardButton(labels["premium"], callback_data="menu:premium"),
            InlineKeyboardButton(labels["wallet"], callback_data="menu:wallet"),
        ],
        [
            InlineKeyboardButton(labels["help"], callback_data="menu:help"),
            InlineKeyboardButton(labels["language"], callback_data="menu:language"),
        ],
    ]
    if user_id in ADMIN_IDS:
        rows.append([InlineKeyboardButton(labels["admin"], callback_data="menu:admin")])
    return InlineKeyboardMarkup(rows)

async def send_language_picker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "🌍 Choose your language / Dilini seç / اختر لغتك"
    if update.message:
        await update.message.reply_text(text, reply_markup=language_keyboard())
    elif update.callback_query:
        await update.callback_query.edit_message_text(
            text, reply_markup=language_keyboard()
        )

async def show_home(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int):
    language = get_language(user_id) or "en"
    labels = LANGUAGES[language]
    text = f"{labels['welcome']}\n\n{labels['menu']}"
    if update.callback_query:
        await update.callback_query.edit_message_text(
            text, reply_markup=main_keyboard(language, user_id)
        )
    elif update.message:
        await update.message.reply_text(
            text, reply_markup=main_keyboard(language, user_id)
        )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    language = get_language(user_id)
    if language is None:
        await send_language_picker(update, context)
    else:
        await show_home(update, context, user_id)

async def language_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_language_picker(update, context)

class APKToolHandler:
    async def start_apk_tool(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "📦 **ANON APK TOOL**\n\nLütfen düzenlemek ve analiz etmek istediğiniz `.apk` dosyasını gönderin.",
            parse_mode="Markdown",
        )
        return UPLOAD_APK

    async def handle_apk_upload(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        from androguard.core.apk import APK
        
        file = await update.message.document.get_file()
        file_path = os.path.join(
            WORK_DIR, f"{update.effective_user.id}_{update.message.document.file_name}"
        )
        await file.download_to_drive(file_path)

        if not file_path.endswith(".apk"):
            await update.message.reply_text("❌ Geçersiz dosya. Lütfen bir APK dosyası gönderin.")
            return UPLOAD_APK

        context.user_data["apk_path"] = file_path

        try:
            apk = APK(file_path)
            info = (
                f"🔍 **APK Analiz Raporu**\n\n"
                f"📌 Paket Adı: `{apk.get_package()}`\n"
                f"🏷️ Uygulama Adı: `{apk.get_app_name()}`\n"
                f"📱 Versiyon: `{apk.get_androidversion_code()} ({apk.get_androidversion_name()})`\n"
                f"🔑 İmza Doğrulandı: {'Evet' if apk.is_signed() else 'Hayır'}\n"
                f"🛡️ Hedef SDK: `{apk.get_target_sdk_version()}`\n"
            )

            keyboard = [
                [InlineKeyboardButton("🏷️ Ad/Paket Değiştir", callback_data="apk:edit_meta")],
                [InlineKeyboardButton("🔓 Lisans Devre Dışı Bırak", callback_data="apk:crack")],
                [InlineKeyboardButton("⚙️ Derle ve İmzala", callback_data="apk:build")],
                [InlineKeyboardButton("⬅️ Ana Menü", callback_data="menu:home")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(info, parse_mode="Markdown")
            await update.message.reply_text("Yapılacak işlemi seçin:", reply_markup=reply_markup)
            return CHOOSE_ACTION
        except Exception as e:
            await update.message.reply_text(f"❌ APK analizi başarısız: {str(e)}")
            return ConversationHandler.END

    async def apk_button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        action = query.data

        if action == "apk:edit_meta":
            await query.message.reply_text("Yeni uygulama adını yazın (veya /skip ile geçin):")
            return NEW_APP_NAME
        elif action == "apk:crack":
            await query.message.reply_text("⚙️ Lisans kontrolleri devre dışı bırakılıyor...")
            success = await self.patch_license_checks(context.user_data["apk_path"])
            if success:
                await query.message.reply_text("✅ Lisans kontrolleri devre dışı bırakıldı.")
            else:
                await query.message.reply_text("⚠️ Lisans deseni bulunamadı veya manuel inceleme gerekebilir.")
            return CHOOSE_ACTION
        elif action == "apk:build":
            await query.message.reply_text("⚙️ APK derleniyor ve imzalanıyor...")
            output_path = await self.build_and_sign(context.user_data["apk_path"], context)
            if output_path and os.path.exists(output_path):
                await query.message.reply_document(
                    document=open(output_path, "rb"),
                    filename="ANON_Modified.apk",
                    caption="✅ Düzenlenmiş APK hazır.",
                )
                self._cleanup(context.user_data["apk_path"])
                return ConversationHandler.END
            else:
                await query.message.reply_text("❌ Derleme hatası.")
                return ConversationHandler.END
        elif action == "menu:home":
            user_id = query.from_user.id
            await show_home(update, context, user_id)
            return ConversationHandler.END

        return CHOOSE_ACTION

    async def handle_new_app_name(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        context.user_data["new_app_name"] = update.message.text
        await update.message.reply_text("Yeni paket adını yazın (örn: com.anon.modified) veya /skip:")
        return NEW_PACKAGE_NAME

    async def handle_new_package_name(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.text.lower() != "/skip":
            context.user_data["new_package"] = update.message.text
        await update.message.reply_text("✅ Meta veriler kaydedildi. Şimdi 'Derle ve İmzala' seçeneğini kullanabilirsiniz.")
        return CHOOSE_ACTION

    async def patch_license_checks(self, apk_path: str) -> bool:
        project_dir = os.path.join(WORK_DIR, "decompiled")
        if os.path.exists(project_dir):
            shutil.rmtree(project_dir)

        decode_cmd = ["apktool", "d", "-f", "-o", project_dir, apk_path]
        proc = await asyncio.create_subprocess_exec(
            *decode_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        await proc.communicate()

        if proc.returncode != 0:
            return False

        patterns_to_patch = [
            r"invoke-virtual.*->isLicensed\(\)",
            r"invoke-virtual.*->checkLicense\(\)",
            r"invoke-virtual.*->isPremium\(\)",
            r"Lcom/android/vending/billing",
        ]

        patched_files = []
        for root, _, files in os.walk(project_dir):
            for file in files:
                if file.endswith(".smali"):
                    smali_path = os.path.join(root, file)
                    try:
                        with open(smali_path, "r", encoding="utf-8") as f:
                            content = f.read()

                        original_content = content
                        for pattern in patterns_to_patch:
                            if re.search(pattern, content, re.IGNORECASE):
                                content = re.sub(r"if-eqz.*", "goto :license_bypassed", content)
                                content += "\n:license_bypassed\nconst/4 v0, 0x1\nreturn v0\n"

                        if content != original_content:
                            with open(smali_path, "w", encoding="utf-8") as f:
                                f.write(content)
                            patched_files.append(file)
                    except Exception:
                        continue

        return len(patched_files) > 0

    async def build_and_sign(self, original_apk_path: str, context: ContextTypes.DEFAULT_TYPE) -> str:
        project_dir = os.path.join(WORK_DIR, "decompiled")
        output_unsigned = os.path.join(WORK_DIR, "unsigned.apk")
        output_signed = os.path.join(WORK_DIR, "ANON_Modified.apk")
        keystore_path = os.path.join(WORK_DIR, "test.keystore")

        manifest_path = os.path.join(project_dir, "AndroidManifest.xml")
        if os.path.exists(manifest_path):
            with open(manifest_path, "r", encoding="utf-8") as f:
                manifest = f.read()
            if "new_package" in context.user_data:
                manifest = re.sub(r'package="[^"]+"', f'package="{context.user_data["new_package"]}"', manifest)
            if "new_app_name" in context.user_data:
                manifest = re.sub(r'android:label="[^"]+"', f'android:label="{context.user_data["new_app_name"]}"', manifest, count=1)
            with open(manifest_path, "w", encoding="utf-8") as f:
                f.write(manifest)

        build_cmd = ["apktool", "b", "-o", output_unsigned, project_dir]
        proc = await asyncio.create_subprocess_exec(
            *build_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        await proc.communicate()

        if proc.returncode != 0:
            return None

        sign_cmd = [
            "apksigner", "sign",
            "--ks", keystore_path,
            "--ks-pass", "pass:anon123",
            "--out", output_signed,
            output_unsigned,
        ]
        proc_sign = await asyncio.create_subprocess_exec(
            *sign_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        await proc_sign.communicate()

        if proc_sign.returncode == 0 and os.path.exists(output_signed):
            return output_signed
        return None

    def _cleanup(self, apk_path: str):
        if os.path.exists(apk_path):
            os.remove(apk_path)
        project_dir = os.path.join(WORK_DIR, "decompiled")
        if os.path.exists(project_dir):
            shutil.rmtree(project_dir)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    data = query.data or ""

    if data.startswith("lang:"):
        await query.answer()
        language = data.split(":", 1)[1]
        if language not in LANGUAGES:
            return
        save_language(user_id, language)
        await show_home(update, context, user_id)
        return

    if data == "menu:language":
        await query.answer()
        await send_language_picker(update, context)
        return

    if data == "menu:apktool":
        await query.answer()
        await query.message.reply_text(
            "📦 **ANON APK TOOL**\n\nLütfen `.apk` dosyasını bu sohbete gönderin veya /apktool komutunu kullanın.",
            parse_mode="Markdown",
        )
        return

    await query.answer()
    language = get_language(user_id) or "en"
    labels = LANGUAGES[language]

    if data == "menu:admin":
        if user_id not in ADMIN_IDS:
            await query.answer("Not authorized.", show_alert=True)
            return
        await query.edit_message_text(
            f"🛡️ {labels['admin']}\n\n"
            f"Admin ID: {user_id}\n"
            "Use /stats to view basic bot statistics.",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("⬅️ " + labels["menu"], callback_data="menu:home")]]
            ),
        )
        return

    if data == "menu:home":
        await show_home(update, context, user_id)
        return

    section = data.split(":", 1)[1] if ":" in data else ""
    if section == "help":
        message = "/start — open the bot\n/language — change language\n/help — show help\n/apktool — APK düzenleme"
    elif section == "ai":
        message = labels["soon"] + "\n\nAI provider will be connected in a later setup step."
    elif section == "premium":
        message = labels["soon"] + "\n\nPremium activation and payments are not enabled yet."
    elif section == "wallet":
        with db() as connection:
            credits = connection.execute(
                "SELECT credits FROM wallets WHERE user_id = ?", (user_id,)
            ).fetchone()
        message = f"{labels['wallet']}: {credits[0] if credits else 0}"
    else:
        message = labels["soon"]

    await query.edit_message_text(
        message,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("⬅️ " + labels["menu"], callback_data="menu:home")]]
        ),
    )

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ This command is for bot admins only.")
        return
    with db() as connection:
        count = connection.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    await update.message.reply_text(f"📊 Registered users: {count}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    language = get_language(upd            WORK_DIR, f"{update.effective_user.id}_{update.message.document.file_name}"
        )
        await file.download_to_drive(file_path)

        if not file_path.endswith(".apk"):
            await update.message.reply_text("❌ Geçersiz dosya. Lütfen bir APK dosyası gönderin.")
            return UPLOAD_APK

        context.user_data["apk_path"] = file_path

        try:
            apk = APK(file_path)
            info = (
                f"🔍 **APK Analiz Raporu**\n\n"
                f"📌 Paket Adı: `{apk.get_package()}`\n"
                f"🏷️ Uygulama Adı: `{apk.get_app_name()}`\n"
                f"📱 Versiyon: `{apk.get_androidversion_code()} ({apk.get_androidversion_name()})`\n"
                f"🔑 İmza Doğrulandı: {'Evet' if apk.is_signed() else 'Hayır'}\n"
                f"🛡️ Hedef SDK: `{apk.get_target_sdk_version()}`\n"
            )

            keyboard = [
                [InlineKeyboardButton("🏷️ Ad/Paket Değiştir", callback_data="apk:edit_meta")],
                [InlineKeyboardButton("🔓 Lisans Devre Dışı Bırak", callback_data="apk:crack")],
                [InlineKeyboardButton("⚙️ Derle ve İmzala", callback_data="apk:build")],
                [InlineKeyboardButton("⬅️ Ana Menü", callback_data="menu:home")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(info, parse_mode="Markdown")
            await update.message.reply_text("Yapılacak işlemi seçin:", reply_markup=reply_markup)
            return CHOOSE_ACTION
        except Exception as e:
            await update.message.reply_text(f"❌ APK analizi başarısız: {str(e)}")
            return ConversationHandler.END

    async def apk_button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        action = query.data

        if action == "apk:edit_meta":
            await query.message.reply_text("Yeni uygulama adını yazın (veya /skip ile geçin):")
            return NEW_APP_NAME
        elif action == "apk:crack":
            await query.message.reply_text("⚙️ Lisans kontrolleri devre dışı bırakılıyor...")
            success = await self.patch_license_checks(context.user_data["apk_path"])
            if success:
                await query.message.reply_text("✅ Lisans kontrolleri devre dışı bırakıldı.")
            else:
                await query.message.reply_text("⚠️ Lisans deseni bulunamadı.")
            return CHOOSE_ACTION
        elif action == "apk:build":
            await query.message.reply_text("⚙️ APK derleniyor ve imzalanıyor...")
            output_path = await self.build_and_sign(context.user_data["apk_path"])
            if output_path and os.path.exists(output_path):
                await query.message.reply_document(
                    document=open(output_path, "rb"),
                    filename="ANON_Modified.apk",
                    caption="✅ Düzenlenmiş APK hazır.",
                )
                self._cleanup(context.user_data["apk_path"])
                return ConversationHandler.END
            else:
                await query.message.reply_text("❌ Derleme hatası.")
                return ConversationHandler.END
        elif action == "menu:home":
            user_id = query.from_user.id
            language = get_language(user_id) or "en"
            labels = LANGUAGES[language]
            text = f"{labels['welcome']}\n\n{labels['menu']}"
            await query.edit_message_text(text, reply_markup=main_keyboard(language, user_id))
            return ConversationHandler.END

        return CHOOSE_ACTION

    async def handle_new_app_name(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        context.user_data["new_app_name"] = update.message.text
        await update.message.reply_text("Yeni paket adını yazın (örn: com.anon.modified) veya /skip:")
        return NEW_PACKAGE_NAME

    async def handle_new_package_name(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.text.lower() != "/skip":
            context.user_data["new_package"] = update.message.text
        await update.message.reply_text("✅ Meta veriler kaydedildi.")
        return CHOOSE_ACTION

    async def patch_license_checks(self, apk_path: str) -> bool:
        project_dir = os.path.join(WORK_DIR, "decompiled")
        if os.path.exists(project_dir):
            shutil.rmtree(project_dir)

        decode_cmd = ["apktool", "d", "-f", "-o", project_dir, apk_path]
        proc = await asyncio.create_subprocess_exec(
            *decode_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        await proc.communicate()

        if proc.returncode != 0:
            return False

        patterns_to_patch = [
            r"invoke-virtual.*->isLicensed\(\)",
            r"invoke-virtual.*->checkLicense\(\)",
            r"invoke-virtual.*->isPremium\(\)",
            r"Lcom/android/vending/billing",
        ]

        patched_files = []
        for root, _, files in os.walk(project_dir):
            for file in files:
                if file.endswith(".smali"):
                    smali_path = os.path.join(root, file)
                    with open(smali_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    original_content = content
                    for pattern in patterns_to_patch:
                        if re.search(pattern, content, re.IGNORECASE):
                            content = re.sub(r"if-eqz.*", "goto :license_bypassed", content)
                            content += "\n:license_bypassed\nconst/4 v0, 0x1\nreturn v0\n"

                    if content != original_content:
                        with open(smali_path, "w", encoding="utf-8") as f:
                            f.write(content)
                        patched_files.append(file)

        return len(patched_files) > 0

    async def build_and_sign(self, original_apk_path: str) -> str:
        project_dir = os.path.join(WORK_DIR, "decompiled")
        output_unsigned = os.path.join(WORK_DIR, "unsigned.apk")
        output_signed = os.path.join(WORK_DIR, "ANON_Modified.apk")

        build_cmd = ["apktool", "b", "-o", output_unsigned, project_dir]
        proc = await asyncio.create_subprocess_exec(
            *build_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        await proc.communicate()

        if proc.returncode != 0:
            return None

        sign_cmd = [
            "apksigner",
            "sign",
            "--ks",
            os.path.join(WORK_DIR, "test.keystore"),
            "--ks-pass",
            "pass:anon123",
            "--out",
            output_signed,
            output_unsigned,
        ]
        proc_sign = await asyncio.create_subprocess_exec(
            *sign_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        await proc_sign.communicate()

        if proc_sign.returncode == 0 and os.path.exists(output_signed):
            return output_signed
        return None

    def _cleanup(self, apk_path: str):
        if os.path.exists(apk_path):
            os.remove(apk_path)
        project_dir = os.path.join(WORK_DIR, "decompiled")
        if os.path.exists(project_dir):
            shutil.rmtree(project_dir)


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    data = query.data or ""

    if data.startswith("lang:"):
        await query.answer()
        language = data.split(":", 1)[1]
        if language not in LANGUAGES:
            return
        save_language(user_id, language)
        await show_home(update, context, user_id)
        return

    if data == "menu:language":
        await query.answer()
        await send_language_picker(update, context)
        return

    if data == "menu:apktool":
        await query.answer()
        await query.edit_message_text(
            "📦 **ANON APK TOOL**\n\nLütfen `.apk` dosyasını gönderin.",
            parse_mode="Markdown",
        )
        return

    await query.answer()
    language = get_language(user_id) or "en"
    labels = LANGUAGES[language]

    if data == "menu:admin":
        if user_id not in ADMIN_IDS:
            await query.answer("Not authorized.", show_alert=True)
            return
        await query.edit_message_text(
            f"🛡️ {labels['admin']}\n\n"
            f"Admin ID: {user_id}\n"
            "Use /stats to view basic bot statistics.",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("⬅️ " + labels["menu"], callback_data="menu:home")]]
            ),
        )
        return

    if data == "menu:home":
        await show_home(update, context, user_id)
        return

    section = data.split(":", 1)[1] if ":" in data else ""
    if section == "help":
        message = "/start — open the bot\n/language — change language\n/help — show help"
    elif section == "ai":
        message = labels["soon"] + "\n\nAI provider will be connected in a later setup step."
    elif section == "premium":
        message = labels["soon"] + "\n\nPremium activation and payments are not enabled yet."
    elif section == "wallet":
        with db() as connection:
            credits = connection.execute(
                "SELECT credits FROM wallets WHERE user_id = ?", (user_id,)
            ).fetchone()
        message = f"{labels['wallet']}: {credits[0] if credits else 0}"
    else:
        message = labels["soon"]

    await query.edit_message_text(
        message,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("⬅️ " + labels["menu"], callback_data="menu:home")]]
        ),
    )


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ This command is for bot admins only.")u:home")]]
        ),
    )


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ This command is for bot admins only.")
        return
    with db() as connection:
        count = connection.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    await update.message.reply_text(f"📊 Registered users: {count}")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    language = get_language(update.effective_user.id) or "en"
    labels = LANGUAGES[language]
    await update.message.reply_text(
        f"{BOT_NAME}\n\n/start — {labels['menu']}\n"
        "/language — change language\n/help — help"
    )


def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN is missing. Add it as an environment secret.")
    db().close()
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("language", language_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CallbackQueryHandler(button_handler))
    logger.info("%s is starting", BOT_NAME)
    application.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
