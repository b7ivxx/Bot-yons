import discord
from discord import app_commands
from discord.ext import commands
import asyncio
from flask import Flask
from threading import Thread

# تشغيل سيرفر ويب صغير في الخلفية لحماية البوت من النوم في السيرفر السحابي
app = Flask('')
@app.route('/')
def home():
    return "بوت بدر المساعد شغال أونلاين 24/7 للأبد!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 🔑 1. ضع هنا التوكن الجديد الخاص ببوتك (تأكد إنه بين علامات التنصيص)
BOT_TOKEN = "MTU1OTkyNjgzNTIyMjAyNDMwNA.Gxzj1_.7zbXdcZYDUftviX2dzWz71zD1Z9QQj_uxS0Fhk"

# 🆔 2. ضع هنا الآيدي الخاص بحسابك الشخصي في الديسكورد
YOUR_DISCORD_ID = 1559545442340053094  

# 🔒 3. ضع هنا آيدي الروم الوحيد المسموح كتابة الأمر فيه (روم التحكم)
ALLOWED_CHANNEL_ID = 1559924040888623206  

# 🏰 4. ضع هنا آيدي سيرفرك للتحديث الفوري قسرياً
GUILD_ID = 1559563442048864361  

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        guild = discord.Object(id=GUILD_ID)
        self.tree.add_command(send_to_any_channel, guild=guild)
        await self.tree.sync(guild=guild)
        print("🚀 تم تثبيت المربع الاحترافي الشامل والمكشوف للجميع بنجاح!")

bot = MyBot()

@bot.event
async def on_ready():
    print(f'🤖 تم تشغيل البوت بنجاح باسم: {bot.user.name}')
    await bot.change_presence(activity=discord.Game(name="مساعد السيرفر الذكي 👑"))

# أمر السلاش السريع والمكشوف بحرف (b)
@app_commands.command(name="b", description="أرسل رسالة إدارية داخل مربع فخم يشمل النصوص والميديا للجميع")
@app_commands.describe(
    channel="اختر الروم الذي تريد إرسال الرسالة إليه",
    message="اكتب النص أو الكلام الذي تريد من البوت نقله وتكبيره",
    file="اضغط هنا لتحميل صورة أو فيديو مباشرة من لابتوبك ليظهر داخل المربع للجميع"
)
async def send_to_any_channel(
    interaction: discord.Interaction, 
    channel: discord.TextChannel, 
    message: str, 
    file: discord.Attachment = None
):
    if interaction.user.id != YOUR_DISCORD_ID:
        await interaction.response.send_message("❌ عذراً، هذا الأمر حصري لمالك السيرفر فقط!", ephemeral=True)
        return

    if interaction.channel_id != ALLOWED_CHANNEL_ID:
        await interaction.response.send_message("❌ خطأ: مسموح باستخدام الأمر فقط في روم التحكم الخاص!", ephemeral=True)
        return

    await interaction.response.defer(ephemeral=True)

    try:
        formatted_message = (
            f"👑 ┃ **مـرسـول مـن الإدارة**\n"
            f"• ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬ •\n\n"
            f"# **{message}**\n\n"
            f"• ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬ •"
        )
        
        embed = discord.Embed(
            description=formatted_message,
            color=discord.Color.from_rgb(47, 49, 54)
        )
        embed.set_footer(text="✨ شكراً لكم لكونكم جزءاً من سيرفرنا")
        
        if file:
            embed.set_image(url=file.url)
            await channel.send(embed=embed)
        else:
            await channel.send(embed=embed)
            
        await interaction.followup.send(f"✅ تم بنجاح إرسال الرسالة والميديا داخل المربع للجميع في روم {channel.mention}!", ephemeral=True)
        
    except discord.Forbidden:
        await interaction.followup.send(f"❌ خطأ: البوت لا يملك صلاحية الكتابة في روم {channel.mention}!", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"❌ حدث خطأ غير متوقع: {str(e)}", ephemeral=True)

# تشغيل سيرفر الويب والبوت معاً للأبد
keep_alive()
try:
    bot.run(BOT_TOKEN)
except discord.errors.LoginFailure:
    print("❌ خطأ: التوكن غير صحيح!")
