import json, math, sys, datetime, asyncio
import discord, time
from discord.ext import commands


with open("config.json", "r") as dosya:
    veri = json.load(dosya)

ajaxvare = veri.get("Ajax", {})
roleid_ = ajaxvare.get("role_id")

db = 1
class BBot:
    @staticmethod
    def online(token, prefix, bbc, kanal, roleid=roleid_):
        print(f" Bot started at {time.strftime('%H:%M')}")
        if db == 1:
            print("Bota Bağlanılıyor...")
            intents = discord.Intents.all()
            Bot = commands.Bot(command_prefix=f"{prefix}", intents= discord.Intents.all())
            intents.members = True
            intents.presences = True
            intents.message_content = True
        
            @Bot.event
            async def on_ready():
                print(f"Bot {Bot.user.name} olarak Başlatıldı!")
                await Bot.tree.sync()
            global komutCount
            global tagcount
            komutCount = 0
            @Bot.command(name="yardım")
            async def helpcommand(ctx):
                embed = discord.Embed(title="Yardım menüsü", description="✨ En yakın kordiyi bulmak için: *kordibul [dünyaismi] [x] [y]\n\n🌍 **Dünyalar**: Sancak, Yakamoz, Avrasya, Pruva, Velena, Flador, Astra")
                embed.set_footer(text=f"istek atan: {ctx.author.name} | by: github.com/iAlperenS")
                await ctx.send(embed=embed)

            @Bot.command(name="bilgi")
            async def helpcommand2(ctx):
                global komutCount
                global hesaplar
                tagcount = 0
                toplam_hesap_sayisi = len(hesaplar)
                for member in ctx.guild.members:
                    if len(member.activities) > 0:
                        activity_name = member.activities[0].name
                        tags = ["github.com/iAlperenS/ajax", "github.com/iAlperenS"]
                        if activity_name in tags:
                            print(f"{member.display_name}'s current activity: {activity_name}")
                            tagcount += 1
                        else:
                            pass
                    else:
                        pass
                embed = discord.Embed(title=f"Hesaplar Ve Daha Fazlası", description=f"📦 Kayıtlı Hesap: **{toplam_hesap_sayisi}**\n⭐ Komut **{komutCount}** Kez Kullanıldı!\n🏆 **{tagcount}** Kişide tag var.")
                embed.set_footer(text=f"istek atan: {ctx.author.name} | by: github.com/iAlperenS")
                await ctx.send(embed=embed)

            @Bot.command(name="kordibul")
            async def TrdBtn(ctx, dunya_adi: str, girilen_x: float, girilen_y: float, bilgi: str, zaman: str):
                if db == 1:
                    global hesaplar
                    global komutCount
                    komutCount += 1
                    hesaplar = json.load(open("data.json", "r"))

                    def en_yakin_hesap_bul(dunya_adi):
                        en_yakin_hesap = None
                        en_kucuk_fark = float('inf')

                        for hesap_isim, alt_hesaplar in hesaplar.items():
                            if dunya_adi in alt_hesaplar:
                                if "x" in alt_hesaplar[dunya_adi] and "y" in alt_hesaplar[dunya_adi]:
                                    x_miktar = alt_hesaplar[dunya_adi]["x"]
                                    y_miktar = alt_hesaplar[dunya_adi]["y"]
                                    fark = abs(girilen_x - x_miktar) + abs(girilen_y - y_miktar)

                                    if fark < en_kucuk_fark:
                                        en_kucuk_fark = fark
                                        en_yakin_hesap = (hesap_isim, x_miktar, y_miktar)

                        return en_yakin_hesap

                    # En yakın hesap bul
                    en_yakin_hesap = en_yakin_hesap_bul(dunya_adi)
                    with open("config.json", "r") as dosya:
                        veri = json.load(dosya)

                    ajaxvare = veri.get("Ajax", {})
                    roleid2 = ajaxvare.get("role_id")
                    roleid3 = int(roleid2)
                    
                    # Zaman kontrolü
                    if roleid3 in [role.id for role in ctx.author.roles]:
                        if en_yakin_hesap:
                            hesap_isim, x_miktar, y_miktar = en_yakin_hesap
                            mesafe_hesap = math.sqrt((girilen_x - x_miktar) ** 2 + (girilen_y - y_miktar) ** 2)
                            mesafe_mesaj = f"{mesafe_hesap:.2f} blok uzaklıkta"
                            embed = discord.Embed(
                                title="En Yakın Kordi",
                                description=f"🌍 > En yakın hesap ({dunya_adi} dünyasında): **{hesap_isim}**, x: **{x_miktar}**, y: **{y_miktar}**\n🏃‍♂️ > **{mesafe_mesaj}**\n📖 Bilgi: {bilgi}\n🕕 Patlama zamanı: {zaman}",
                                color=discord.Color.green()
                            )
                            embed.set_footer(text=f"istek atan: {ctx.author.name} | by: github.com/iAlperenS")
                            await ctx.send(embed=embed)
                            if mesafe_hesap < int(bbc):
                                channel = Bot.get_channel(int(kanal))
                                await channel.send(f"> Koşulacak Cl (**{dunya_adi}**) (**{hesap_isim}**) (**{mesafe_mesaj}**)\n🏃‍♂️ Gidilecek kordinat: X:**{girilen_x}** - Y: **{girilen_y}**")
                                # Mesajı gönder
                            while True:
                                current_time = datetime.datetime.now().strftime("%H.%M")
                                print(current_time)
                                if current_time == zaman or current_time > zaman:
                                    await channel.send(f"💣 > Cl Patladı (**{dunya_adi}**) ({girilen_x}, {girilen_y}) @AlperenS")
                                    break
                                await asyncio.sleep(1)  # Zamanı her sny kontrol et
                        else:
                            embed = discord.Embed(
                                title="Kordi Bulunamadı",
                                description=f"Üzgünüm herhangi bir kordi bulamadım veya birşeyler ters gitti",
                                color=discord.Color.red()
                            )
                            embed.set_footer(text=f"istek atan: {ctx.author.name} | by: github.com/iAlperenS")
                            await ctx.send(embed=embed)
                    else:
                        await ctx.send("Bu Komutu Kullanmaya Yetkiniz Yok!")
                else:
                    await ctx.send("Bu Komutu Kullanmaya Yetkiniz Yok!")


            Bot.run(token)
        else:
            sys.exit()

bot_token = ajaxvare.get("token")
prefix = ajaxvare.get("prefix")
block = ajaxvare.get("uzaklik")
channel = ajaxvare.get("kanal")

BBot.online(bot_token, prefix, block, channel)