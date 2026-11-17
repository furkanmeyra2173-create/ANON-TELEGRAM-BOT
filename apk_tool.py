"""Safe APK inspection and metadata editing for APKs the user owns or may modify.

This module does not remove licensing, DRM, payment, authentication, or other access
controls. Uploaded APK files are inspected, never executed.
"""
import asyncio
import os
import re
import secrets
import shutil
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

from androguard.core.apk import APK
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

UPLOAD_APK, CHOOSE_ACTION, NEW_APP_NAME, NEW_PACKAGE_NAME = range(4)
BASE_DIR = Path(os.getenv("APK_TOOL_WORK_DIR", "/tmp/anon_apk_tool"))
MAX_APK_BYTES = 50 * 1024 * 1024
PACKAGE_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_]*(?:\\.[A-Za-z][A-Za-z0-9_]*)+$")
ANDROID_NS = "{http://schemas.android.com/apk/res/android}"


def _user_dir(context: ContextTypes.DEFAULT_TYPE) -> Path:
    path = context.user_data.get("apk_work_dir")
    if not path:
        BASE_DIR.mkdir(parents=True, exist_ok=True)
        path = tempfile.mkdtemp(prefix=f"{context._user_id}_", dir=BASE_DIR)
        context.user_data["apk_work_dir"] = path
    return Path(path)


async def _run(*args: str, timeout: int = 300):
    process = await asyncio.create_subprocess_exec(
        *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    try:
        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)
    except asyncio.TimeoutError:
        process.kill()
        await process.communicate()
        raise RuntimeError("İşlem zaman aşımına uğradı.")
    if process.returncode != 0:
        detail = (stderr or stdout).decode("utf-8", "replace")[-1200:]
        raise RuntimeError(detail or f"Komut başarısız: {args[0]}")
    return stdout.decode("utf-8", "replace")


class APKToolHandler:
    async def start_apk_tool(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        context.user_data.pop("apk_path", None)
        context.user_data.pop("new_app_name", None)
        context.user_data.pop("new_package", None)
        await update.effective_message.reply_text(
            "📦 ANON APK TOOL\\n\\n"
            "Sahibi olduğun veya değiştirme iznin bulunan APK dosyasını gönder. "
            "En fazla 50 MB. Dosya çalıştırılmaz; yalnızca analiz edilir."
        )
        return UPLOAD_APK

    async def handle_apk_upload(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        document = update.effective_message.document
        filename = (document.file_name or "upload.apk").lower()
        if not filename.endswith(".apk"):
            await update.effective_message.reply_text("❌ Lütfen .apk uzantılı bir dosya gönder.")
            return UPLOAD_APK
        if document.file_size and document.file_size > MAX_APK_BYTES:
            await update.effective_message.reply_text("❌ Dosya sınırı 50 MB.")
            return UPLOAD_APK

        work_dir = _user_dir(context)
        apk_path = work_dir / "original.apk"
        telegram_file = await document.get_file()
        await telegram_file.download_to_drive(custom_path=str(apk_path))
        if apk_path.stat().st_size > MAX_APK_BYTES:
            shutil.rmtree(work_dir, ignore_errors=True)
            context.user_data.pop("apk_work_dir", None)
            await update.effective_message.reply_text("❌ Dosya sınırı 50 MB.")
            return ConversationHandler.END

        try:
            apk = APK(str(apk_path))
            permissions = apk.get_permissions() or []
            permission_text = "\\n".join(f"• {p}" for p in permissions[:25]) or "Belirtilmedi"
            if len(permissions) > 25:
                permission_text += f"\\n… ve {len(permissions) - 25} izin daha"
            report = (
                "🔍 APK ANALİZ RAPORU\\n\\n"
                f"Paket: {apk.get_package() or 'Bilinmiyor'}\\n"
                f"Uygulama: {apk.get_app_name() or 'Bilinmiyor'}\\n"
                f"Sürüm: {apk.get_androidversion_name() or 'Bilinmiyor'} "
                f"({apk.get_androidversion_code() or '—'})\\n"
                f"Target SDK: {apk.get_target_sdk_version() or 'Bilinmiyor'}\\n"
                f"İmza mevcut: {'Evet' if apk.is_signed() else 'Hayır'}\\n\\n"
                f"İzinler ({len(permissions)}):\\n{permission_text}\\n\\n"
                "Not: Yeni imza, orijinal geliştiricinin imzası değildir. "
                "Değiştirilmiş APK orijinal uygulamanın üzerine güncelleme olarak kurulamayabilir."
            )
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🏷️ Ad / paket adını değiştir", callback_data="apk:edit")],
                [InlineKeyboardButton("⚙️ Yeniden derle ve imzala", callback_data="apk:build")],
                [InlineKeyboardButton("❌ İptal", callback_data="apk:cancel")],
            ])
            context.user_data["apk_path"] = str(apk_path)
            await update.effective_message.reply_text(report)
            await update.effective_message.reply_text("Bir işlem seç:", reply_markup=keyboard)
            return CHOOSE_ACTION
        except Exception as exc:
            await update.effective_message.reply_text(f"❌ APK okunamadı: {exc}")
            self._cleanup(context)
            return ConversationHandler.END

    async def choose_action(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        if not context.user_data.get("apk_path"):
            await query.message.reply_text("Önce /apktool komutuyla yeni bir APK gönder.")
            return ConversationHandler.END
        if query.data == "apk:edit":
            await query.message.reply_text("Yeni uygulama adını yaz. Değiştirmek istemiyorsan /skip yaz.")
            return NEW_APP_NAME
        if query.data == "apk:build":
            await query.message.reply_text("APK yeniden derleniyor ve geçici bir anahtarla imzalanıyor…")
            try:
                output = await self.build_and_sign(context)
                with output.open("rb") as stream:
                    await query.message.reply_document(
                        document=stream,
                        filename="ANON_Modified.apk",
                        caption="✅ APK hazır. Bu işlem yalnızca uygulama adı/paket metaverisini değiştirir."
                    )
            except Exception as exc:
                await query.message.reply_text(f"❌ Derleme/imzalama başarısız: {exc}")
                return CHOOSE_ACTION
            self._cleanup(context)
            return ConversationHandler.END
        if query.data == "apk:cancel":
            await query.message.reply_text("İşlem iptal edildi. /start ile ana menüye dönebilirsin.")
            self._cleanup(context)
            return ConversationHandler.END
        return CHOOSE_ACTION

    async def handle_new_app_name(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        value = update.effective_message.text.strip()
        if value != "/skip":
            if not value or len(value) > 80:
                await update.effective_message.reply_text("Ad 1–80 karakter olmalı.")
                return NEW_APP_NAME
            context.user_data["new_app_name"] = value
        await update.effective_message.reply_text(
            "Yeni paket adını yaz (örn. com.example.modified). Değiştirmeyeceksen /skip."
        )
        return NEW_PACKAGE_NAME

    async def handle_new_package_name(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        value = update.effective_message.text.strip()
        if value != "/skip":
            if not PACKAGE_RE.fullmatch(value):
                await update.effective_message.reply_text(
                    "❌ Paket adı geçersiz. Örnek: com.example.modified"
                )
                return NEW_PACKAGE_NAME
            context.user_data["new_package"] = value
        await update.effective_message.reply_text(
            "✅ Değişiklikler kaydedildi. Şimdi 'Yeniden derle ve imzala' düğmesine bas."
        )
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("⚙️ Yeniden derle ve imzala", callback_data="apk:build")],
            [InlineKeyboardButton("❌ İptal", callback_data="apk:cancel")],
        ])
        await update.effective_message.reply_text("Devam et:", reply_markup=keyboard)
        return CHOOSE_ACTION

    async def skip(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.effective_message.reply_text("/skip komutunu ilgili adımda kullanabilirsin.")
        return ConversationHandler.END

    async def build_and_sign(self, context: ContextTypes.DEFAULT_TYPE) -> Path:
        apk_path = Path(context.user_data["apk_path"])
        work_dir = _user_dir(context)
        decoded = work_dir / "decoded"
        unsigned = work_dir / "unsigned.apk"
        signed = work_dir / "ANON_Modified.apk"
        keystore = work_dir / "temporary-signing-key.jks"
        manifest_path = decoded / "AndroidManifest.xml"

        await _run("apktool", "d", "-f", "-o", str(decoded), str(apk_path))
        if not manifest_path.exists():
            raise RuntimeError("AndroidManifest.xml bulunamadı.")
        tree = ET.parse(manifest_path)
        root = tree.getroot()
        if "new_package" in context.user_data:
            root.set("package", context.user_data["new_package"])
        if "new_app_name" in context.user_data:
            root.set(ANDROID_NS + "label", context.user_data["new_app_name"])
        tree.write(manifest_path, encoding="utf-8", xml_declaration=True)

        await _run("apktool", "b", "-o", str(unsigned), str(decoded))
        password = secrets.token_urlsafe(24)
        await _run(
            "keytool", "-genkeypair", "-keystore", str(keystore),
            "-storepass", password, "-keypass", password, "-alias", "anon-h4x",
            "-dname", "CN=ANON H4X", "-keyalg", "RSA", "-keysize", "2048",
            "-validity", "10000"
        )
        await _run(
            "apksigner", "sign", "--ks", str(keystore), "--ks-pass",
            f"pass:{password}", "--key-pass", f"pass:{password}",
            "--out", str(signed), str(unsigned)
        )
        if not signed.exists():
            raise RuntimeError("İmzalı APK üretilemedi.")
        return signed

    def _cleanup(self, context: ContextTypes.DEFAULT_TYPE):
        work_dir = context.user_data.pop("apk_work_dir", None)
        if work_dir:
            shutil.rmtree(work_dir, ignore_errors=True)
        for key in ("apk_path", "new_app_name", "new_package"):
            context.user_data.pop(key, None)


def get_apk_tool_conversation():
    handler = APKToolHandler()
    return ConversationHandler(
        entry_points=[
            CommandHandler("apktool", handler.start_apk_tool),
            CallbackQueryHandler(handler.start_apk_tool, pattern=r"^menu:apktool$"),
        ],
        states={
            UPLOAD_APK: [MessageHandler(filters.Document.ALL, handler.handle_apk_upload)],
            CHOOSE_ACTION: [CallbackQueryHandler(handler.choose_action, pattern=r"^apk:")],
            NEW_APP_NAME: [
                CommandHandler("skip", handler.handle_new_app_name),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handler.handle_new_app_name),
            ],
            NEW_PACKAGE_NAME: [
                CommandHandler("skip", handler.handle_new_package_name),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handler.handle_new_package_name),
            ],
        },
        fallbacks=[CommandHandler("cancel", handler.skip)],
        allow_reentry=True,
    )
