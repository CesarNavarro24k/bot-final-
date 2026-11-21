import discord
from dotenv import load_dotenv 
import asyncio
import random
import webserver
import os
from discord.ext import commands

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hola, soy un bot {bot.user}!')

@bot.command()
async def heh(ctx, count_heh = 5):
    await ctx.send("he" * count_heh)

@bot.command()
async def ppt(ctx):
    opciones = ["piedra","papel","tijera"]
    gana = {"piedra":"tijera", "papel":"piedra", "tijera":"papel"}

    victorias = 0
    derrotas = 0
    empates = 0

    await ctx.send("Piedra, papel o tijera, escribe tu jugada o escribe salir:")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    while True:
        try:
            msg = await bot.wait_for("message", check=check, timeout=120)
        except asyncio.TimeoutError:
            await ctx.send("Pasaron 2 minutos sin jugar, juego terminado")
            break 
        jugada = msg.content.lower()
        if jugada == "salir":
            break 
        bot_jugada = random.choice(opciones)

        if jugada == bot_jugada:
            resultado = "Empate"
            empates += 1 
        elif gana[jugada] == bot_jugada:
            resultado = "Ganaste"
            victorias += 1
        else:
            resultado = "Perdiste"
            derrotas += 1
        await ctx.send(f"El bot a elegido: {bot_jugada}")
        await ctx.send(f"El resultado es: {resultado}")

        await ctx.send("Los marcadores son:")
        await ctx.send(f"Ganadas: {victorias}")
        await ctx.send(f"Perdidas: {derrotas}")
        await ctx.send(f"Empates: {empates}")

@bot.command()
async def imagenes(ctx):
    img = os.listdir(random.choice("imagenes"))
    with open(f"imagenes/{img}", "rb") as f:
        picture = discord.File(f)
    await ctx.send(file=picture)

@bot.command()
async def adivinar(ctx):
    numero = random.randint(1,50)
    intentos = 0
    max_intentos = 7 

    await ctx.send(f"Pense en un numero entre el 1 y el 50, tienes {max_intentos} intentos para adivinar")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel 

    while intentos < max_intentos:
        try:
            mensaje = await bot.wait_for("message", check=check, timeout=30)
        except Exception:
            await ctx.send(f"Se acabo el tiempo, el numero era: {numero}")

        intento = int(mensaje.content)

        if intentos < 1 or intento > 50:
            await ctx.send("El numero debe estar entre 1 y 50")
            continue 
        intentos += 1
        restantes = max_intentos - intentos 

        if intento == numero:
            await ctx.send(f"Felicidades, has adivinado el numero")
        elif intento > numero:
            await ctx.send("El numero que debes adivinar es menor")
        else:
            await ctx.send("El numero que debes adivinar es mayor")
webserver.keep_alive()
bot.run(DISCORD_TOKEN)
