import discord
from discord.ext import commands
from datetime import datetime
import requests


now = datetime.now().time()

print('Logging in...')
client = commands.Bot(command_prefix='.', help_command=None)

#on start
@client.event
async def on_ready():
    print('Logged in as {0} | {1}'.format(client.user, client.user.id))
    await client.change_presence(activity=discord.Game(name=".help for commands"))
    f = open("log.txt", "a")
    f.write("\n[{0}] Logged in as {1} | {2}".format(now, client.user, client.user.id))
    f.close()

#status
@client.command()
async def status(ctx, *, user=None):
    try:
        user = await commands.converter.UserConverter().convert(ctx, user)
        print(user)

    except:
        await ctx.send("Error: user could not be found!")
        return
    try:
        bans = tuple(ban_entry.user for ban_entry in await ctx.guild.bans())
        if user in bans:


            embed: discord.Embed = discord.Embed(
                title="Status of {0}".format(user),
                description="Banned: `True`",
                color=discord.Color.red()
            )
            embed.set_author(name="ddozzi bot")
            # embed.add_field(name="", value="Shows a list of commands", inline=True)

            await ctx.send(embed=embed)

        else:
            embed: discord.Embed = discord.Embed(
                title="Status of {0}".format(user),
                description="Banned: `False`",
                color=discord.Color.dark_green()
            )
            embed.set_author(name="ddozzi bot")
            # embed.add_field(name="", value="Shows a list of commands", inline=True)

            await ctx.send(embed=embed)

    except discord.Forbidden:
        print('discord.Forbidden:')

#get id
@client.command()
async def getid(ctx, user: discord.User):
    try:
        await ctx.send(user.id)
        print(user.id)
    except discord.ext.commands.errors.MissingRequiredArgument:
        print('User/Member not mentioned')

#fake ban
@client.command()
async def fakeban(ctx, member : discord.Member):
    try:
        embed: discord.Embed = discord.Embed(
            title="You have been banned!", description="You may appeal here: [INSERT]", color=discord.Color.red()
        )

        embed.set_author(name="ddozzi bot")
        #embed.add_field(name="", value="Shows a list of commands", inline=True)

        await member.send(embed=embed)
    except discord.ext.commands.errors.MissingRequiredArgument:
        print('User/Member not mentioned')

#reject appeal
@client.command()
@commands.has_permissions(manage_messages=True)
async def reject(ctx, user : discord.User):
        print("rejected user {0} with id {1} ban appeal".format(user, user.id))

        embed: discord.Embed = discord.Embed(
            title="Your ban appeal has been denied!", description="You will be unbanned in 1 week.", color=discord.Color.red()
        )

        embed.set_author(name="ddozzi bot")
        #embed.add_field(name="", value="Shows a list of commands", inline=True)

        f = open("log.txt", "a")
        f.write("\n[{0}] Rejected {1} with user id of <@!{2}>".format(now, user, user.id))
        f.close()
        await user.send(embed=embed)

#fake unban
@client.command()
async def fakeunban(ctx, member : discord.Member):
    try:
        embed: discord.Embed = discord.Embed(
            title="You have been unbanned :)",
            description="Thank you for appealing. You may join back here: [INSERT]",
            color=discord.Color.dark_green()
        )
        embed.set_author(name="ddozzi bot")
        # embed.add_field(name="", value="Shows a list of commands", inline=True)

        await member.send(embed=embed)
    except discord.ext.commands.errors.MissingRequiredArgument:
        print('User/Member not mentioned')

#DM
@client.command(pass_context=True)
async def dm(ctx, member: discord.User, *, content: str):
    try:
        await member.send(content)

        print('{0} with an id of <@!{2}> has been sent a dm of {1}!'.format(member, content, member.id))
        f = open("log.txt", "a")
        f.write("\n[{0}] {1} with user id of <@!{2}> has sent message: {3}".format(now, member, member.id, content))
        f.close()
    except discord.ext.commands.errors.MissingRequiredArgument:
        print('User/Member not mentioned')

#Mute
@client.command(description="Mutes the specified user.")
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, send_messages=False)
    embed = discord.Embed(title="Muted", description=f"{member.mention} was muted ", colour=discord.Colour.light_gray())
    embed.add_field(name="Reason:", value=reason, inline=False)
    await ctx.send(embed=embed)
    await member.add_roles(mutedRole, reason=reason)
    embed: discord.Embed = discord.Embed(
        title="You have been muted!", description="Please wait out your mute!",
        color=discord.Color.gold()
    )
    embed.set_author(name="ddozzi bot")
    # embed.add_field(name="", value="Shows a list of commands", inline=True)

    await member.send(embed=embed)
    f = open("log.txt", "a")
    f.write("\n[{0}] Muted {1} with user id of <@!{2}> for reason: {3}".format(now, member, member.id, reason))
    f.close()

#Unmute
@client.command(description="Unmutes a specified user.")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
   mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

   await member.remove_roles(mutedRole)
   embed = discord.Embed(title="Unmute", description=f" Unmuted-{member.mention}",colour=discord.Colour.light_gray())
   await ctx.send(embed=embed)
   embed: discord.Embed = discord.Embed(
       title="You have been unmuted :)",
       description="Thank you for waiting. You may join back here: [INSERT]",
       color=discord.Color.dark_green()
   )
   embed.set_author(name="ddozzi bot")
   # embed.add_field(name="", value="Shows a list of commands", inline=True)

   await member.send(embed=embed)
   f = open("log.txt", "a")
   f.write("\n[{0}] Unmuted {1} with user id of <@!{2}>".format(now, member, member.id))
   f.close()

#Clear Chat
@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=None):
    await ctx.channel.purge(limit=int(amount))
    print('{0} Lines have been deleted'.format(amount))
    f = open("log.txt", "a")
    f.write("\n[{0}] Cleared {1} lines.".format(now, amount))
    f.close()

#Help
@client.command()
async def help(ctx, option=None):

    if option is not None:
        if option == 'fakeban':
            embed: discord.Embed = discord.Embed(
                color=discord.Color.blue()
            )
            embed.set_author(name="Scythe Plugin Commands")
            embed.add_field(name="FakeBan", value=" `Use .fakeban {person} make sure its an @!`", inline=True)
            await ctx.send(embed=embed)
        elif option == 'ping':
            embed: discord.Embed = discord.Embed(
                color=discord.Color.blue()
            )
            embed.set_author(name="Scythe Plugin Commands")
            embed.add_field(name="Ping", value=" `Use .ping to see the latency of this bot!`", inline=True)
            await ctx.send(embed=embed)
        elif option == 'ban':
            embed: discord.Embed = discord.Embed(
                color=discord.Color.blue()
            )
            embed.set_author(name="Scythe Plugin Commands")
            embed.add_field(name="Ban",
                            value=" `Use .ban {person} {reason} to ban the specified person. Don't try it if you dont have perms, it wont work :)`",
                            inline=True)
            await ctx.send(embed=embed)

        elif option == 'unban':
                embed: discord.Embed = discord.Embed(
                    color=discord.Color.blue()
                )
                embed.set_author(name="Scythe Plugin Commands")
                embed.add_field(name="Unban",
                                value=" `Use .unban {person} to unban the specified person. Don't try it if you dont have perms, it wont work :)`",
                                inline=True)
                await ctx.send(embed=embed)
        elif option == 'getid':
            embed: discord.Embed = discord.Embed(
                color=discord.Color.blue()
            )
            embed.set_author(name="Scythe Plugin Commands")
            embed.add_field(name="Getting ID",
                            value=" `Use .getid {person} to get their id`",
                            inline=True)
            await ctx.send(embed=embed)

        elif option == 'mute':
            embed: discord.Embed = discord.Embed(
                color=discord.Color.blue()
            )
            embed.set_author(name="Scythe Plugin Commands")
            embed.add_field(name="Mute",
                            value=" `Use .mute {person} to mute`",
                            inline=True)
            await ctx.send(embed=embed)

        elif option == 'clear':
            embed: discord.Embed = discord.Embed(
                color=discord.Color.blue()
            )
            embed.set_author(name="Scythe Plugin Commands")
            embed.add_field(name="Clear",
                            value=" `Use .clear {amount} to delete that many messages [ADMIN ONLY]`",
                            inline=True)
            await ctx.send(embed=embed)



    elif option is None:

        embed: discord.Embed = discord.Embed(
            color=discord.Color.blue()
        )
        #embed.add_field(name="Field1", value="hi", inline=True)
        #embed.set_image(url='[INSERT]')
        embed.set_thumbnail(url='[INSERT]')
        embed.set_author(name="Scythe Plugin Commands")
        embed.add_field(name="FakeBan", value=" `.help fakeban`", inline=True)
        embed.add_field(name="Ping", value='`.help ping`', inline=True)
        embed.add_field(name="Ban", value='`.help ban`', inline=True)
        embed.add_field(name='Unban', value='`.help unban`', inline=True)
        embed.add_field(name='Mute', value='`.help mute`', inline=True)
        embed.add_field(name='Clear', value='`.help clear`', inline=True)


        await ctx.send(embed=embed)

#Ban
@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.User, *, reason=None):
    try:
        print(member)

        embed: discord.Embed = discord.Embed(
            title="You have been banned!", description="You may appeal here: [INSERT]",
            color=discord.Color.red()
        )
        embed.set_author(name="ddozzi bot")
        # embed.add_field(name="", value="Shows a list of commands", inline=True)

        await member.send(embed=embed)
        # message = "This Message is sent via DM"
        membere = await commands.converter.MemberConverter().convert(ctx, str(member))
        await membere.ban(reason=reason)
        print('banned {0} with user id of <@!{1}>'.format(member, member.id))
        f = open("log.txt", "a")
        f.write("\n[{0}] Banned {1} with user id of <@!{2}> for reason: {3}".format(now, member, member.id, reason))
        f.close()

        await ctx.channel.purge(limit=2)
        # await user.send(message)
    except discord.ext.commands.errors.MissingRequiredArgument:
        print('User/Member not mentioned')

#Unban
@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, user=None):
    try:
        user = await commands.converter.UserConverter().convert(ctx, user)
        print(user)

    except:
        await ctx.send("Error: user could not be found!")
        return
    try:
        bans = tuple(ban_entry.user for ban_entry in await ctx.guild.bans())
        if user in bans:

            await ctx.guild.unban(user, reason="Responsible moderator: " + str(ctx.author))

        else:
            await ctx.send("User not banned!")
            await ctx.channel.purge(limit=2)
            return
    except discord.Forbidden:
        print('discord.Forbidden: unbanned but embed makes it think they arent')

    await ctx.send(f"Successfully unbanned {user.mention}!")
    await ctx.channel.purge(limit=2)

    embed: discord.Embed = discord.Embed(
        title="You have been unbanned :)",
        description="Thank you for appealing. You may join back here: [INSERT]",
        color=discord.Color.dark_green()
    )
    embed.set_author(name="ddozzi bot")
    # embed.add_field(name="", value="Shows a list of commands", inline=True)

    await user.send(embed=embed)

    f = open("log.txt", "a")
    f.write("\n[{0}] Unbanned {1} with user id of <@!{2}>".format(now, user, user.id))
    f.close()

    print('Unban message has been sent!')

#Ping
@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! In {round(client.latency * 1000)}ms')
    print('Latency has been checked!')

client.run('[INSERT api key]')
