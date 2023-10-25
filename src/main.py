from discord.ext import commands
import discord
import random

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(
    command_prefix="!",  # Change to desired prefix
    case_insensitive=True, # Commands aren't case-sensitive
    intents = intents # Set up basic permissions
)

flood_active = False
flood_users = {}

flood_message_limit = 5
flood_time_limit = 10

bot.author_id = 199469240082890761  # Change to your discord id

@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    print(message.content)
    if (message.content == "Salut tout le monde"):
        response = f"Salut tout seul, {message.author.mention}!"
        await message.channel.send(response)
        
    if flood_active:
        author_id = message.author.id
        current_time = message.created_at
        print(current_time)
        print(author_id)

        if author_id in flood_users:
            last_messages = flood_users[author_id]
            print(last_messages)
            last_messages_in_time_limit = [message for message in last_messages if (current_time - message).total_seconds() < flood_time_limit]
            print(last_messages_in_time_limit)
            print(len(last_messages_in_time_limit))

            if len(last_messages_in_time_limit) > flood_message_limit:
                await message.channel.send(f"{message.author.mention}, stop spam messages.")
                print("send message")

        if author_id not in flood_users:
            flood_users[author_id] = []

        flood_users[author_id].append(current_time)

        await bot.process_commands(message)

    await bot.process_commands(message)

@bot.command()
async def pong(ctx):
    await ctx.send('pong')

@bot.command()
async def name(ctx):
    user_name = ctx.author.name
    await ctx.send(f'Your name is: {user_name}')

@bot.command()
async def d6(ctx):
    result = random.randint(1, 6)
    await ctx.send(f'{result}')

@bot.command()
async def admin(ctx, member_name: str):
    admin_role = discord.utils.get(ctx.guild.roles, name="Admin")
    print(admin_role)
    if not admin_role:
        admin_role = await ctx.guild.create_role(name="Admin", permissions=discord.Permissions.all())
    
    member = discord.utils.get(ctx.guild.members, display_name=member_name)

    print(member)

    if member:
        await member.add_roles(admin_role)
        await ctx.send(f"Assigned 'Admin' role to {member.mention}")
        print('Member found and role assigned')


    else:
        await ctx.send(f"Member with nickname '{member_name}' not found.")
        print('Member not found')

reasons = [
    "Tu es trop nul !",
    "Tu es mauvais !",
    "Tu es trop jeune !",
    "Tu es trop vieux !",
    "Tu n'as pas assez d'expériences !",
    "Tu n'as pas le profil qui correspond aux postes!",
    "Tu ne cultives pas assez d'expériences !"
]
@bot.command()
async def ban(ctx, member_name: str, ban_reason: str = None):
    # Find the member based on the provided nickname
    member = discord.utils.get(ctx.guild.members, display_name=member_name)

    print(member)
    if not member:
        print('Member not found')
        await ctx.send(f"Member with nickname '{member_name}' not found!")

    print(ban_reason)
    if ban_reason == None:
        print('No reason provided')
        ban_reason = random.choice(reasons)
        print(ban_reason)

    await member.ban(reason=ban_reason)
    await ctx.send(f"Banned {member.mention} for: {ban_reason}")
    


@bot.command()
async def flood(ctx):
    global flood_active
    flood_active = not flood_active
    if flood_active:
        await ctx.send("Flood active")
    else:
        await ctx.send("Flood inactive")




token = ""
bot.run(token)  # Starts the bot