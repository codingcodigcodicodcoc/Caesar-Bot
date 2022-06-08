import discord
from discord.ext import commands
import youtube_dl

class music(commands.Cog):
  def __init__(self, client):
    self.client = client
    
  @commands.command()
  async def join(self, ctx):
    if ctx.author.voice is None:
      await ctx.send("You're not in a voice channel")
    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
      await voice_channel.connect()
    else:
      await ctx.voice_client.move_to(voice_channel)

  @commands.command()
  async def disconnect(self, ctx):
    await ctx.voice_client.disconnect()

  @commands.command()
  async def play(self,ctx,url):
    ctx.voice_client.stop()
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    YDL_OPTIONS = {'format':"bestaudio"}
    vc = ctx.voice_client
    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
      info = ydl.extract_info(url, download=False)
      url2 = info['formats'][0]['url']
      source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
      vc.play(source)
#  async def play(ctx, url : str):
#      song_there = os.path.isfile("song.mp3")
#      try:
#          if song_there:
#              os.remove("song.mp3")
#      except PermissionError:
#          await ctx.send("Wait for the current playing music to end or use the 'stop' command")
#          return  
#      voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
#      await voiceChannel.connect()
#      voice = discord.utils.get(client.voice_clients, guild=ctx.guild)  
#      ydl_opts = {
#          'format': 'bestaudio/best',
#          'postprocessors': [{
#              'key': 'FFmpegExtractAudio',
#              'preferredcodec': 'mp3',
#              'preferredquality': '192',
#          }],
#      }
#      with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#          ydl.download([url])
#      for file in os.listdir("./"):
#          if file.endswith(".mp3"):
#              os.rename(file, "song.mp3")
#      voice.play(discord.FFmpegPCMAudio("song.mp3"))
  
#  @commands.command()
#  async def leave(ctx):
#      voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
#      if voice.is_connected():
#          await voice.disconnect()
#      else:
#          await ctx.send("The bot is not connected to a voice channel.")
  
  @commands.command()
  async def pause(self,ctx):
    await ctx.voice_client.pause()
    await ctx.send("Paused")
#    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
#    voice.pause()
  
  @commands.command()
  async def resume(self,ctx):
    await ctx.voice_client.resume()
    await ctx.send("Resuming")
#    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
#    voice.resume()
  
def setup(bot):
  bot.add_cog(music(bot))