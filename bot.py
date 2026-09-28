import discord
from discord.ext import commands
from config import token
from logic2 import *

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

class PersistentView(discord.ui.View):
    def __init__(self, owner):
        super().__init__(timeout=None)
        self.owner = owner

    @discord.ui.button(label="Terima Balasan", style=discord.ButtonStyle.primary, custom_id="text_ans")
    async def text_ans_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        obj = TextAnalysis.memory[self.owner][-1]
        # Berikan teks cadangan jika obj.response kosong
        pesan = obj.response if obj.response else "Maaf, respon tidak ditemukan."
        await interaction.response.send_message(pesan, ephemeral=True)

    @discord.ui.button(label="Terjemahkan Pesan", style=discord.ButtonStyle.secondary, custom_id="text_translate")
    async def text_translate_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        obj = TextAnalysis.memory[self.owner][-1]
        # Perbaikan utama: Pastikan teks tidak kosong agar Discord tidak eror
        pesan_terjemahan = obj.translation if obj.translation and obj.translation.strip() else "Gagal menerjemahkan teks (Kuota API mungkin habis)."
        await interaction.response.send_message(pesan_terjemahan, ephemeral=True)


@bot.event
async def on_ready():
    print(f'Berhasil log in sebagai {bot.user}')

@bot.command(name="start")
async def start(ctx, *, text: str):
    TextAnalysis(text, ctx.author.name)
    view = PersistentView(ctx.author.name)
    await ctx.send("Pesanmu diterima! Apa yang kamu ingin aku lakukan?", view=view)

bot.run(token)