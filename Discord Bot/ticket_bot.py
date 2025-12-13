"""
🎫 Captcha Crush - Discord Ticket Bot
Otomatik ticket sistemi ve captcha bazlı indirme botu
"""

import discord
from discord.ext import commands
from discord import app_commands
import os
import io
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv
import aiohttp
import asyncio

# .env dosyasını yükle
load_dotenv()

# Bot ayarları
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

# Panel API Ayarları
PANEL_API_URL = os.getenv("PANEL_API_URL", "https://license-api-5p24.onrender.com")
DISCORD_BOT_API_KEY = os.getenv("DISCORD_BOT_API_KEY", "CaptchaCrushSecretKey2024!@#")

bot = commands.Bot(command_prefix="!", intents=intents)

# Bot durumu kontrolü
async def check_bot_status():
    """Panel'den bot durumunu kontrol et"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{PANEL_API_URL}/bot_status") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get("status", True)
        return True  # API'ye erişilemezse çalışmaya devam et
    except:
        return True  # Hata durumunda çalışmaya devam et

# Konfigürasyon
TICKET_CATEGORY_ID = None  # Manuel olarak ayarlanacak
TICKET_LOGS_CHANNEL_ID = None  # Manuel olarak ayarlanacak
DEVELOPER_ROLE_NAME = "Developer"

# Linkler
CAPTCHA_LINKS = {
    "0030.png": "https://limewire.com/d/A3dqU#J3jfw56jSM",
    "00613.png": "https://limewire.com/d/uYd28#ip4JjnnA1u"
}

# Ticket sayacı
ticket_counter = 0

class TicketView(discord.ui.View):
    """Ana ticket oluşturma butonu"""
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🎫 Ticket Oluştur", style=discord.ButtonStyle.green, custom_id="create_ticket")
    async def create_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await handle_ticket_creation(interaction)

class WelcomeView(discord.ui.View):
    """Ticket açıldığında ilk soru"""
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="✅ Evet", style=discord.ButtonStyle.green, custom_id="yes_purchase")
    async def yes_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await show_captcha_selection(interaction)

    @discord.ui.button(label="❌ Hayır, başka desteğe ihtiyacım var", style=discord.ButtonStyle.red, custom_id="no_purchase")
    async def no_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Developer'ı etiketle
        guild = interaction.guild
        dev_role = discord.utils.get(guild.roles, name=DEVELOPER_ROLE_NAME)

        if dev_role:
            await interaction.response.send_message(
                f"{dev_role.mention} Müşteri farklı bir destek talep ediyor! 👋",
                view=CloseTicketView()
            )
        else:
            await interaction.response.send_message(
                "⚠️ Developer rolü bulunamadı! Lütfen sunucu sahibiyle iletişime geçin.",
                view=CloseTicketView()
            )


class ReadyButtonView(discord.ui.View):
    """Hazır butonu"""
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="✅ Hazır", style=discord.ButtonStyle.success, custom_id="ready_button")
    async def ready_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Developer'ı etiketle
        guild = interaction.guild
        dev_role = discord.utils.get(guild.roles, name=DEVELOPER_ROLE_NAME)

        if dev_role:
            await interaction.response.send_message(
                f"{dev_role.mention} Müşteri hazır! 🎉"
            )
        else:
            await interaction.response.send_message("⚠️ Developer rolü bulunamadı!")

        # Ürün bilgisi
        embed = discord.Embed(
            title="💎 Captcha Crush - Ürün Bilgileri",
            description="Uygulamayı indirdiğiniz için teşekkürler!",
            color=discord.Color.gold(),
            timestamp=datetime.utcnow()
        )

        embed.add_field(
            name="✨ Özellikler",
            value="• 🔄 Aylık sınırsız token\n• 🌐 24/7 kullanılabilir\n• 🚀 Hızlı ve güvenli",
            inline=False
        )

        embed.add_field(
            name="💰 Fiyat",
            value="**20$ / Aylık**",
            inline=False
        )

        embed.add_field(
            name="📞 İletişim",
            value="Developer'ımız size ödeme detaylarını gönderecek!",
            inline=False
        )

        embed.set_footer(text="Captcha Crush License System")

        await interaction.channel.send(embed=embed, view=CloseTicketView())

class CloseTicketView(discord.ui.View):
    """Ticketi kapatma butonu"""
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🔒 Ticketi Kapat", style=discord.ButtonStyle.danger, custom_id="close_ticket")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await close_ticket(interaction)

async def handle_ticket_creation(interaction: discord.Interaction):
    """Ticket oluşturma işlemi"""
    global ticket_counter
    ticket_counter += 1

    guild = interaction.guild
    user = interaction.user

    # Tickets kategorisini bul
    category = discord.utils.get(guild.categories, name="🎫 Tickets")
    if not category:
        category = await guild.create_category("🎫 Tickets")

    # Developer rolünü bul
    dev_role = discord.utils.get(guild.roles, name=DEVELOPER_ROLE_NAME)

    # @printrandom kullanıcısını bul (username ile)
    printrandom_user = discord.utils.get(guild.members, name="printrandom")

    # Ticket kanalını oluştur
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
    }

    if dev_role:
        overwrites[dev_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

    # @printrandom için özel izin ekle
    if printrandom_user:
        overwrites[printrandom_user] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

    ticket_channel = await guild.create_text_channel(
        name=f"ticket-{ticket_counter}",
        category=category,
        overwrites=overwrites
    )

    # Hoş geldin mesajı
    embed = discord.Embed(
        title="🎫 Ticket Oluşturuldu",
        description=f"Merhaba {user.mention}! Sana yardımcı olmak isterim.",
        color=discord.Color.blue(),
        timestamp=datetime.utcnow()
    )

    embed.add_field(
        name="❓ Soru",
        value="**Captcha Crush programını satın almak için mi geldin?**",
        inline=False
    )

    embed.set_footer(text=f"Ticket #{ticket_counter}")

    # Hem kullanıcıyı hem de @printrandom'u etiketle
    mention_text = f"{user.mention}"
    if printrandom_user:
        mention_text += f" {printrandom_user.mention}"

    await ticket_channel.send(
        content=mention_text,
        embed=embed,
        view=WelcomeView()
    )

    # Kullanıcıyı ticket kanalına yönlendir
    redirect_embed = discord.Embed(
        title="🎫 Ticket Oluşturuldu!",
        description=f"**Ticket'in hazır!**\n\n{ticket_channel.mention} kanalına git ve destek almaya başla!",
        color=discord.Color.green()
    )
    redirect_embed.add_field(
        name="📍 Ne Yapmalısın?",
        value=f"Aşağıdaki butona tıkla veya direkt {ticket_channel.mention} kanalına git!",
        inline=False
    )
    redirect_embed.set_footer(text=f"Ticket #{ticket_counter}")

    # Direkt kanala gitme butonu
    view = discord.ui.View(timeout=60)
    button = discord.ui.Button(
        label="🎫 Ticket'ime Git",
        style=discord.ButtonStyle.link,
        url=f"https://discord.com/channels/{interaction.guild_id}/{ticket_channel.id}"
    )
    view.add_item(button)

    await interaction.response.send_message(
        embed=redirect_embed,
        view=view,
        ephemeral=True
    )


async def show_captcha_selection(interaction: discord.Interaction):
    """Captcha seçim ekranını göster - her resim kendi butonu ile"""

    # Ana açıklama mesajı
    embed_intro = discord.Embed(
        title="🖼️ Captcha Seçimi",
        description="**Kullandığın serverlarda hangi captcha görüntüsü var?**\n\nAşağıda 2 farklı captcha resmi göreceksin. Hangisi senin serverında varsa onun altındaki butona tıkla!",
        color=discord.Color.orange(),
        timestamp=datetime.utcnow()
    )
    embed_intro.set_footer(text="Her resmin altında 'Seç' butonu var")

    await interaction.response.send_message(embed=embed_intro)

    # Resim yolları
    image_path_1 = "0030.png"
    image_path_2 = "00613.png"

    # İLK RESİM + BUTONU
    if os.path.exists(image_path_1):
        embed1 = discord.Embed(
            title="🔹 Seçenek 1",
            description="**Bu captcha senin serverında varsa aşağıdaki butona tıkla!**",
            color=discord.Color.blue()
        )
        embed1.set_image(url="attachment://captcha1.png")

        # İlk resim için view
        view1 = discord.ui.View(timeout=None)
        button1 = discord.ui.Button(
            label="✅ İlk Resmi Seç (0030)",
            style=discord.ButtonStyle.primary,
            custom_id="select_captcha_0030"
        )

        async def button1_callback(inter: discord.Interaction):
            await send_download_link(inter, "0030.png")

        button1.callback = button1_callback
        view1.add_item(button1)

        await interaction.channel.send(
            embed=embed1,
            file=discord.File(image_path_1, filename="captcha1.png"),
            view=view1
        )

    # İKİNCİ RESİM + BUTONU
    if os.path.exists(image_path_2):
        embed2 = discord.Embed(
            title="🔹 Seçenek 2",
            description="**Bu captcha senin serverında varsa aşağıdaki butona tıkla!**",
            color=discord.Color.green()
        )
        embed2.set_image(url="attachment://captcha2.png")

        # İkinci resim için view
        view2 = discord.ui.View(timeout=None)
        button2 = discord.ui.Button(
            label="✅ İkinci Resmi Seç (00613)",
            style=discord.ButtonStyle.success,
            custom_id="select_captcha_00613"
        )

        async def button2_callback(inter: discord.Interaction):
            await send_download_link(inter, "00613.png")

        button2.callback = button2_callback
        view2.add_item(button2)

        await interaction.channel.send(
            embed=embed2,
            file=discord.File(image_path_2, filename="captcha2.png"),
            view=view2
        )

async def send_download_link(interaction: discord.Interaction, captcha_type: str):
    """İndirme linkini gönder"""
    link = CAPTCHA_LINKS.get(captcha_type, "")

    embed = discord.Embed(
        title="📥 İndirme Linki Hazır!",
        description=f"**{captcha_type}** için doğru versiyonu seçtin!",
        color=discord.Color.green(),
        timestamp=datetime.utcnow()
    )

    embed.add_field(
        name="🔗 İndirme Linki",
        value=f"[BURAYA TIKLA]({link})",
        inline=False
    )

    embed.add_field(
        name="⚠️ Önemli Uyarılar",
        value=(
            "• Windows Defender'ı **kapat**\n"
            "• Antivirüs'ü **kapat**\n"
            "• **Admin olarak çalıştır**\n"
            "• İndirdikten sonra **'Hazır'** butonuna bas"
        ),
        inline=False
    )

    embed.set_footer(text="Captcha Crush - License System")

    await interaction.response.send_message(
        content="✅ Lütfen bu linkteki uygulamayı indir, indirdikten sonra lütfen bana **'Hazır'** demeyi unutma!",
        embed=embed,
        view=ReadyButtonView()
    )

async def close_ticket(interaction: discord.Interaction):
    """Ticketi kapat ve log'a kaydet"""
    channel = interaction.channel
    guild = interaction.guild

    # Ticket logs kanalını bul veya oluştur
    logs_channel = discord.utils.get(guild.text_channels, name="ticket-logs")
    if not logs_channel:
        # Developer rolünü bul
        dev_role = discord.utils.get(guild.roles, name=DEVELOPER_ROLE_NAME)

        # İzinleri ayarla - sadece bot ve Developer görebilir
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(
                read_messages=False  # Herkes göremez
            ),
            guild.me: discord.PermissionOverwrite(
                read_messages=True,
                send_messages=True
            )
        }

        if dev_role:
            overwrites[dev_role] = discord.PermissionOverwrite(
                read_messages=True,   # Developer görebilir
                send_messages=False   # Developer yazamaz (sadece okur)
            )

        logs_channel = await guild.create_text_channel(
            "ticket-logs",
            overwrites=overwrites,
            topic="📝 Kapatılan ticketlerin kayıtları (Sadece Developer ve Bot görebilir)"
        )

    # Sohbet geçmişini topla
    messages = []
    async for message in channel.history(limit=100, oldest_first=True):
        timestamp = message.created_at.strftime("%d/%m/%Y %H:%M:%S")
        author = f"{message.author.name}#{message.author.discriminator}"
        content = message.content or "[Embed/Dosya]"
        messages.append(f"[{timestamp}] {author}: {content}")

    # Log dosyası oluştur
    log_content = "\n".join(messages)
    log_file = discord.File(
        io.BytesIO(log_content.encode()),
        filename=f"{channel.name}_log.txt"
    )

    # Log kanalına gönder
    embed = discord.Embed(
        title="📝 Ticket Kapatıldı",
        description=f"**Ticket:** {channel.mention}\n**Kapatan:** {interaction.user.mention}",
        color=discord.Color.red(),
        timestamp=datetime.utcnow()
    )

    await logs_channel.send(embed=embed, file=log_file)

    # Ticketi sil
    await interaction.response.send_message("🔒 Ticket 5 saniye içinde silinecek...")
    await asyncio.sleep(5)
    await channel.delete()


# =========================
# ÖDEME SİSTEMİ
# =========================
class PaymentConfirmView(discord.ui.View):
    """Ödeme onay butonu - Sadece admin basabilir"""
    def __init__(self, ticket_creator: discord.Member):
        super().__init__(timeout=None)
        self.ticket_creator = ticket_creator

    @discord.ui.button(label="💳 Ödeme Yapıldı", style=discord.ButtonStyle.success, custom_id="payment_confirmed")
    async def payment_confirmed(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Sadece admin basabilir
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ Bu butona sadece yöneticiler basabilir!",
                ephemeral=True
            )
            return

        # Butonu devre dışı bırak
        button.disabled = True
        button.label = "✅ İşleniyor..."
        await interaction.response.edit_message(view=self)

        # API ile lisans oluştur
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{PANEL_API_URL}/api/create_license",
                    json={
                        "api_key": DISCORD_BOT_API_KEY,
                        "duration_days": 30,
                        "note": f"Discord: {self.ticket_creator.name}"
                    }
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        license_key = data.get("license_key")

                        # Başarı mesajı
                        success_embed = discord.Embed(
                            title="🎉 Lisans Oluşturuldu!",
                            description=f"{self.ticket_creator.mention} Ödemeniz onaylandı! İşte lisansınız:",
                            color=discord.Color.gold(),
                            timestamp=datetime.utcnow()
                        )
                        success_embed.add_field(
                            name="🔑 Lisans Key",
                            value=f"```{license_key}```",
                            inline=False
                        )
                        success_embed.add_field(
                            name="⏰ Süre",
                            value="30 Gün",
                            inline=True
                        )
                        success_embed.add_field(
                            name="✅ Durum",
                            value="Aktif",
                            inline=True
                        )
                        success_embed.add_field(
                            name="📝 Kullanım",
                            value="Bu key'i uygulamaya yapıştırarak kullanabilirsin!",
                            inline=False
                        )
                        success_embed.set_footer(text="Captcha Crush License System")

                        # Ticket kanalında paylaş
                        await interaction.channel.send(
                            content=f"{self.ticket_creator.mention}",
                            embed=success_embed
                        )

                        # Müşteriye özel mesaj (DM) gönder
                        try:
                            dm_embed = discord.Embed(
                                title="🎉 Lisans Oluşturuldu!",
                                description=f"Ödemeniz onaylandı! İşte lisansınız:",
                                color=discord.Color.green(),
                                timestamp=datetime.utcnow()
                            )

                            dm_embed.add_field(
                                name="🔑 Lisans Key",
                                value=f"```{license_key}```",
                                inline=False
                            )

                            dm_embed.add_field(
                                name="⏰ Süre",
                                value="30 Gün",
                                inline=True
                            )

                            dm_embed.add_field(
                                name="✅ Durum",
                                value="Aktif",
                                inline=True
                            )

                            dm_embed.add_field(
                                name="📝 Kullanım",
                                value="Bu key'i uygulamaya yapıştırarak kullanabilirsin!",
                                inline=False
                            )

                            dm_embed.set_footer(text="Captcha Crush - Lisans Sistemi")

                            # DM gönder
                            await self.ticket_creator.send(embed=dm_embed)

                            # Ticket'te bilgi ver
                            await interaction.channel.send(
                                f"✅ {self.ticket_creator.mention} Lisans key'i özel mesaj olarak da gönderildi!"
                            )

                        except discord.Forbidden:
                            # DM kapalıysa ticket'te bilgi ver
                            await interaction.channel.send(
                                f"⚠️ {self.ticket_creator.mention} DM'lerin kapalı olduğu için özel mesaj gönderilemedi! Lisans key'ini yukarıdan kopyala."
                            )
                        except Exception as dm_error:
                            print(f"❌ DM gönderilemedi: {dm_error}")

                        # Butonu güncelle
                        button.label = "✅ Ödeme Tamamlandı"
                        button.style = discord.ButtonStyle.secondary
                        await interaction.edit_original_response(view=self)

                    else:
                        error_text = await resp.text()
                        await interaction.channel.send(
                            f"❌ Lisans oluşturulurken hata oluştu! (Status: {resp.status})\n```{error_text}```"
                        )
        except Exception as e:
            await interaction.channel.send(
                f"❌ API bağlantı hatası: {str(e)}"
            )

# =========================
# SLASH COMMANDS
# =========================
@bot.tree.command(name="iban", description="IBAN bilgilerini göster")
async def iban_command(interaction: discord.Interaction):
    """IBAN bilgilerini paylaş ve ödeme onay butonu göster"""

    # DEBUG: Komut çağrıldı
    print(f"🔍 /iban komutu çağrıldı! Kanal: {interaction.channel.name}")

    # Sadece ticket kanallarında çalışır
    if not interaction.channel.name.startswith("ticket-"):
        await interaction.response.send_message(
            "❌ Bu komut sadece ticket kanallarında kullanılabilir!",
            ephemeral=True
        )
        print(f"⚠️ Yanlış kanal: {interaction.channel.name}")
        return

    print(f"✅ Ticket kanalında, devam ediliyor...")

    # Ticket sahibini bul (kanalı oluşturan)
    ticket_creator = None
    async for message in interaction.channel.history(limit=50, oldest_first=True):
        if message.embeds:
            for embed in message.embeds:
                if embed.title == "🎫 Ticket Oluşturuldu":
                    # İlk mention edilen kullanıcı ticket sahibi
                    if message.mentions:
                        ticket_creator = message.mentions[0]
                        break
        if ticket_creator:
            break

    if not ticket_creator:
        # Fallback: Kanal izinlerinden bul
        for member in interaction.guild.members:
            permissions = interaction.channel.permissions_for(member)
            if permissions.read_messages and not member.bot and member != interaction.guild.me:
                if not member.guild_permissions.administrator:
                    ticket_creator = member
                    break

    print(f"🔍 Ticket creator bulundu: {ticket_creator}")

    # IBAN embed'i oluştur
    iban_embed = discord.Embed(
        title="💳 Ödeme Bilgileri",
        description="Aşağıdaki IBAN'a ödemenizi yaptıktan sonra bu mesajın altındaki butona basın.",
        color=discord.Color.blue(),
        timestamp=datetime.utcnow()
    )

    iban_embed.add_field(
        name="🏦 IBAN",
        value="```TR57 0006 4000 0011 2820 1138 36```",
        inline=False
    )

    iban_embed.add_field(
        name="👤 Alıcı Adı Soyadı",
        value="**Muharrem Canbey**",
        inline=False
    )

    iban_embed.add_field(
        name="💰 Tutar",
        value="**20$** (Güncel TL karşılığı)",
        inline=False
    )

    iban_embed.add_field(
        name="⚠️ Önemli",
        value="• Ödeme açıklamasına ticket numaranızı yazın\n• Ödeme yaptıktan sonra dekont fotoğrafını buraya atın\n• Admin onayladıktan sonra lisansınız otomatik oluşturulacak",
        inline=False
    )

    iban_embed.set_footer(text="Captcha Crush - Ödeme Sistemi")

    # Ödeme onay butonu (sadece admin basabilir)
    view = PaymentConfirmView(ticket_creator) if ticket_creator else None

    print(f"✅ IBAN embed'i gönderiliyor...")

    await interaction.response.send_message(
        embed=iban_embed,
        view=view
    )

    print(f"✅ /iban komutu başarıyla tamamlandı!")

@bot.tree.command(name="setup", description="Bot kurulumunu yap (Sadece Admin)")
@app_commands.default_permissions(administrator=True)
async def setup_command(interaction: discord.Interaction):
    """Bot kurulumu"""
    guild = interaction.guild

    # Developer rolü var mı kontrol et
    dev_role = discord.utils.get(guild.roles, name=DEVELOPER_ROLE_NAME)
    if not dev_role:
        dev_role = await guild.create_role(
            name=DEVELOPER_ROLE_NAME,
            color=discord.Color.red(),
            permissions=discord.Permissions(administrator=True)
        )

    # Eski emoji'siz Tickets kategorisini sil (varsa)
    old_category = discord.utils.get(guild.categories, name="Tickets")
    if old_category:
        # Kategorideki tüm kanalları sil
        for channel in old_category.channels:
            await channel.delete()
        # Kategoriyi sil
        await old_category.delete()

    # Tickets kategorisi oluştur (🎫 ikon ile)
    category = discord.utils.get(guild.categories, name="🎫 Tickets")
    if not category:
        category = await guild.create_category("🎫 Tickets")

    # ticket-olustur kanalı oluştur (yazma yasak, sadece buton)
    ticket_create_channel = discord.utils.get(guild.text_channels, name="ticket-olustur")
    if not ticket_create_channel:
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(
                read_messages=True,
                send_messages=False,  # Yazma yasak!
                add_reactions=False
            ),
            guild.me: discord.PermissionOverwrite(
                read_messages=True,
                send_messages=True
            )
        }
        ticket_create_channel = await guild.create_text_channel(
            "ticket-olustur",
            category=category,
            overwrites=overwrites,
            topic="🎫 Ticket oluşturmak için aşağıdaki butona tıklayın!"
        )

    # ticket-logs kanalı oluştur
    logs_channel = discord.utils.get(guild.text_channels, name="ticket-logs")
    if not logs_channel:
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(
                read_messages=False
            ),
            guild.me: discord.PermissionOverwrite(
                read_messages=True,
                send_messages=True
            )
        }
        if dev_role:
            overwrites[dev_role] = discord.PermissionOverwrite(
                read_messages=True,
                send_messages=False
            )

        logs_channel = await guild.create_text_channel(
            "ticket-logs",
            category=category,
            overwrites=overwrites,
            topic="📝 Kapatılan ticketlerin kayıtları"
        )

    # ticket-olustur kanalına paneli gönder
    # Önce eski mesajları temizle
    await ticket_create_channel.purge(limit=100)

    # Yeni panel gönder
    embed = discord.Embed(
        title="🎫 Captcha Crush - Destek Sistemi",
        description=(
            "**Hoş geldiniz!**\n\n"
            "Captcha Crush programını satın almak veya destek almak için "
            "aşağıdaki butona tıklayarak ticket oluşturun.\n\n"
            "📌 **Ticket açtıktan sonra:**\n"
            "• Size özel bir kanal oluşturulacak\n"
            "• Sadece siz ve yetkililer görebilir\n"
            "• Bot size adım adım yardımcı olacak"
        ),
        color=discord.Color.blue(),
        timestamp=datetime.utcnow()
    )

    embed.set_thumbnail(url=bot.user.display_avatar.url)
    embed.set_footer(text="Captcha Crush License System")

    await ticket_create_channel.send(embed=embed, view=TicketView())

    embed = discord.Embed(
        title="✅ Kurulum Tamamlandı",
        description="Bot başarıyla kuruldu!",
        color=discord.Color.green(),
        timestamp=datetime.utcnow()
    )

    embed.add_field(
        name="✅ Oluşturulanlar",
        value=(
            f"• Rol: {dev_role.mention}\n"
            f"• Kategori: **Tickets**\n"
            f"• Kanal: {ticket_create_channel.mention} (sadece buton, yazma yasak)\n"
            f"• Logs: {logs_channel.mention}"
        ),
        inline=False
    )

    embed.add_field(
        name="📝 Tamamlandı",
        value=f"Ticket paneli {ticket_create_channel.mention} kanalına otomatik eklendi!\n\nMüşteriler artık ticket oluşturabilir!",
        inline=False
    )

    await interaction.response.send_message(embed=embed, ephemeral=True)

# =========================
# BOT EVENTS
# =========================
@bot.event
async def on_ready():
    """Bot hazır olduğunda"""
    print(f"✅ Bot hazır: {bot.user.name} (ID: {bot.user.id})")
    print(f"🌐 Sunucu sayısı: {len(bot.guilds)}")

    # Slash komutları senkronize et (FORCE SYNC)
    try:
        # Her zaman sync yap - komutlar güncellensin
        synced = await bot.tree.sync()
        print(f"✅ {len(synced)} slash komutu senkronize edildi")
        print(f"📋 Komutlar: {', '.join([cmd.name for cmd in synced])}")
    except discord.HTTPException as e:
        if e.status == 429:
            print(f"⚠️ Rate limit! 3 saniye bekleniyor...")
            await asyncio.sleep(3)
            try:
                synced = await bot.tree.sync()
                print(f"✅ {len(synced)} slash komutu senkronize edildi (tekrar deneme)")
            except:
                print(f"⚠️ Slash komutlar sync edilemedi ama bot çalışıyor")
        else:
            print(f"❌ Slash komut senkronizasyonu başarısız: {e}")
    except Exception as e:
        print(f"❌ Beklenmeyen hata: {e}")

    # Bot durumunu ayarla
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="Tickets | 🎫 Ticket Oluştur"
        )
    )

# =========================
# MAIN
# =========================

if __name__ == "__main__":
    # Token'ı environment variable'dan al
    TOKEN = os.getenv("DISCORD_BOT_TOKEN")

    if not TOKEN:
        print("❌ DISCORD_BOT_TOKEN bulunamadı!")
        print("Environment variable olarak ayarlayın veya .env dosyası oluşturun.")
    else:
        bot.run(TOKEN)

