import os
import subprocess
import shutil
import re
import asyncio
import aiofiles
from androguard.core.apk import APK
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters, CommandHandler

UPLOAD_APK, CHOOSE_ACTION, NEW_APP_NAME, NEW_PACKAGE_NAME, NEW_ICON, CONFIRM_PATCH = range(6)
WORK_DIR = "/tmp/anon_apk_tool"
os.makedirs(WORK_DIR, exist_ok=True)

class APKToolHandler:
    def __init__(self):
        self.user_data = {}

    async def start_apk_tool(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("📦 **ANON APK TOOL**\n\nLütfen düzenlemek ve analiz etmek istediğiniz `.apk` dosyasını gönderin.")
        return UPLOAD_APK

    async def handle_apk_upload(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        file = await update.message.document.get_file()
        file_path = os.path.join(WORK_DIR, f"{update.effective_user.id}_{update.message.document.file_name}")
        await file.download_to_drive(file_path)

        if not file_path.endswith(".apk"):
            await update.message.reply_text("❌ Geçersiz dosya. Lütfen bir APK dosyası gönderin.")
            return UPLOAD_APK

        context.user_data['apk_path'] = file_path
        context.user_data['app_name'] = update.message.document.file_name.replace(".apk", "")
        
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
                [InlineKeyboardButton("🏷️ Ad/Paket Değiştir", callback_data="edit_meta")],
                [InlineKeyboardButton("🔓 Lisans/Kilit Devre Dışı Bırak", callback_data="crack_license")],
                [InlineKeyboardButton("📋 Manifest/İzin Düzenle", callback_data="edit_manifest")],
                [InlineKeyboardButton("⚙️ Hemen Derle ve İmzala", callback_data="build_sign")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(info, parse_mode='Markdown')
            await update.message.reply_text("Yapılacak işlemi seçin:", reply_markup=reply_markup)
            return CHOOSE_ACTION
        except Exception as e:
            await update.message.reply_text(f"❌ APK analizi başarısız: {str(e)}")
            return ConversationHandler.END

    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        action = query.data

        if action == "edit_meta":
            await query.message.reply_text("Yeni uygulama adını yazın (veya /skip ile geçin):")
            return NEW_APP_NAME
        elif action == "crack_license":
            await query.message.reply_text("⚙️ Lisans ve erişim koruma sistemleri devre dışı bırakılıyor...")
            success = await self.patch_license_checks(context.user_data['apk_path'])
            if success:
                await query.message.reply_text("✅ Lisans kontrolleri başarıyla devre dışı bırakıldı.")
            else:
                await query.message.reply_text("⚠️ Belirli bir lisans deseni bulunamadı.")
            return CHOOSE_ACTION
        elif action == "build_sign":
            await query.message.reply_text("⚙️ APK yeniden paketleniyor ve imzalanıyor...")
            output_path = await self.build_and_sign(context.user_data['apk_path'])
            if output_path:
                await query.message.reply_document(document=open(output_path, 'rb'), filename="ANON_Modified.apk")
                self._cleanup(context.user_data['apk_path'])
                return ConversationHandler.END
            else:
                await query.message.reply_text("❌ Derleme hatası.")
                return ConversationHandler.END
        return CHOOSE_ACTION

    async def handle_new_app_name(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        context.user_data['new_app_name'] = update.message.text
        await update.message.reply_text("Yeni paket adını yazın veya /skip:")
        return NEW_PACKAGE_NAME

    async def handle_new_package_name(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.text.lower() != '/skip':
            context.user_data['new_package'] = update.message.text
        return CHOOSE_ACTION

    async def patch_license_checks(self, apk_path: str) -> bool:
        project_dir = os.path.join(WORK_DIR, "decompiled")
        if os.path.exists(project_dir):
            shutil.rmtree(project_dir)
        
        decode_cmd = ["apktool", "d", "-f", "-o", project_dir, apk_path]
        proc = await asyncio.create_subprocess_exec(*decode_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        await proc.communicate()
        
        if proc.returncode != 0:
            return False

        patterns_to_patch = [
            r"invoke-virtual.*->isLicensed\(\)",
            r"invoke-virtual.*->checkLicense\(\)",
            r"invoke-virtual.*->isPremium\(\)",
            r"Lcom/android/vending/billing"
        ]
        
        patched_files = []
        for root, _, files in os.walk(project_dir):
            for file in files:
                if file.endswith(".smali"):
                    smali_path = os.path.join(root, file)
                    with open(smali_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    original_content = content
                    for pattern in patterns_to_patch:
                        if re.search(pattern, content, re.IGNORECASE):
                            content = re.sub(r"if-eqz.*", "goto :license_bypassed", content)
                            content += "\n:license_bypassed\nconst/4 v0, 0x1\nreturn v0\n"
                    
                    if content != original_content:
                        with open(smali_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        patched_files.append(file)

        return len(patched_files) > 0

    async def build_and_sign(self, original_apk_path: str) -> str:
        project_dir = os.path.join(WORK_DIR, "decompiled")
        output_unsigned = os.path.join(WORK_DIR, "unsigned.apk")
        output_signed = os.path.join(WORK_DIR, "ANON_Modified.apk")

        build_cmd = ["apktool", "b", "-o", output_unsigned, project_dir]
        proc = await asyncio.create_subprocess_exec(*build_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        await proc.communicate()
        
        if proc.returncode != 0:
            return None

        sign_cmd = ["apksigner", "sign", "--ks", os.path.join(WORK_DIR, "test.keystore"), "--ks-pass", "pass:anon123", "--out", output_signed, output_unsigned]
        proc_sign = await asyncio.create_subprocess_exec(*sign_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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

def get_apk_tool_conversation():
    handler = APKToolHandler()
    return ConversationHandler(
        entry_points=[CommandHandler("apktool", handler.start_apk_tool)],
        states={
            UPLOAD_APK: [MessageHandler(filters.Document.ALL, handler.handle_apk_upload)],
            CHOOSE_ACTION: [CallbackQueryHandler(handler.button_handler)],
            NEW_APP_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handler.handle_new_app_name)],
            NEW_PACKAGE_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handler.handle_new_package_name)],
        },
        fallbacks=[CommandHandler("cancel", lambda u, c: ConversationHandler.END)],
          )
