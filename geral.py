import discord
import asyncio
import platform
import io
import random
import secrets
import string
import traceback
import os
from os import listdir
from os.path import isfile, join
from discord.ext.commands import Bot
from discord.ext import commands
from Area51.utils import user_bd
import discord
from datetime import datetime
import datetime


client = discord.Client()
bot = Bot(description="Uma maga disposta a fazer muitos truques por vc (づ｡◕‿‿◕｡)づ",
          command_prefix=commands.when_mentioned_or('!'), pm_help=False,
          help_attrs=dict(hidden=True, brief="Magicos não precisam de ajuda... ou precisam rs"))
bot.remove_command('help')
cogs_dir = "cogs"


@bot.event
async def on_ready():
    print('Logada como ' + bot.user.name + ' (ID:' + bot.user.id + ') | Conectada a ' + str(
        len(bot.servers)) + ' servidores | Em contato com ' + str(len(set(bot.get_all_members()))) + ' usuarios')
    print('-------------------------------------------------------------------------------------------------')
    print('Versão do Discord.py : {} | Versão do Python : {}'.format(discord.__version__, platform.python_version()))
    print('-------------------------------------------------------------------------------------------------')
    print('Link de convite da {}:'.format(bot.user.name))
    print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(bot.user.id))
    print('-------------------------------------------------------------------------------------------------')
    print('Servidor Discord : https://discord.me/discordialol')
    print('Github Link: https://github.com/ThalesMorandi/MeguminBot')
    print('-------------------------------------------------------------------------------------------------')
    return await bot.change_presence(game=discord.Game(name='caixas aleatoriamente'))


@bot.event
async def on_message(message):
        if not message.content.startswith('!') and not message.author.bot is True:
            usuario = message.author
            server = message.server
            xpganha = random.randint(1, 5)
            usuario_local_xp = await user_bd.get_xp(server.id, usuario.id)
            usuario_local_level = await user_bd.get_level(usuario_local_xp)
            usuario_new_level = await user_bd.get_level(usuario_local_xp + xpganha)

            if usuario_local_level != usuario_new_level:
                embed = discord.Embed(color=0x06ff2c)
                embed.set_thumbnail(url=usuario.avatar_url)
                embed.add_field(name=usuario.name, value='Upou para o **level {}**!'.format(usuario_local_level + 1),
                                inline=False)
                embed.add_field(name='Ganhou', value='**100** Eris <:eris:420848536444207104>.')
                await bot.send_message(message.channel, embed=embed)
                await user_bd.set_token(usuario.id, 100)
            await user_bd.user_add_xp(usuario.id, xpganha)


class Membro():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.cooldown(2, 10, commands.BucketType.user)
    async def perfil(self, ctx, member: discord.Member = None):
        """Exibe o seu perfil ou de um membro."""
        if member is None:
            member = ctx.message.author
        if member.bot is False:
            d = datetime.datetime.utcnow() - ctx.message.timestamp
            ping = d.seconds * 1000 + d.microseconds // 1000
            rep = await user_bd.get_rep(member.id)
            eris = await user_bd.get_token(member.id)
            xpe = await user_bd.get_xp(member.id)
            level = await user_bd.get_level(xpe)
            barra = await user_bd.get_xpbar(member.id)
            exp = await user_bd.get_exp(member.id)
            tempo = member.joined_at.strftime('%d/%m/%y ás %H:%M')
            embedperfil = discord.Embed(title="Nome : " + member.name, color=0x46EEFF)
            if member.avatar_url == "":
                avatar_url = 'http://www.bool-tech.com/wp-content/uploads/bb-plugin/cache/WBBQ55TF_o-square.jpg'
            else:
                avatar_url = member.avatar_url
            embedperfil.set_thumbnail(url=avatar_url)

            embedperfil.add_field(name='Informação global',
                                  value='Level: {0} ({1})\n{2}\nRank: #1 | XP Total : {3}'.format(level, exp, barra,
                                                                                                  xpe))
            embedperfil.add_field(name='Bio', value='hehehihi (18)')
            embedperfil.add_field(name='Tokens', value='{} :moneybag:'.format(eris))
            embedperfil.add_field(name='Conquistas', value='Nenhuma (ainda!)')
            embedperfil.set_footer(text='membro desde ' + tempo + ' | tempo de resposta: {}ms'.format(ping))
            await self.bot.send_message(ctx.message.channel, embed=embedperfil)


bot.run(token)
