import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_BOT_TOKEN', 'MTQ4NjM0MjQ0NjcxNDQ1NDA4Ng.GieYay.u71eAj3a3XtYlHtRP-kRffWV7JQC5GdbaHfFNE')

YOUR_USER_ID = int(os.getenv('YOUR_USER_ID', '753629960173912154'))

ALLOWED_CHANNEL_ID = int(os.getenv('ALLOWED_CHANNEL_ID')) if os.getenv('ALLOWED_CHANNEL_ID') else None

intents = discord.Intents.default()
intents.message_content = True
intents.private_messages = True
intents.guild_messages = True

bot = commands.Bot(command_prefix='@', intents=intents)

user_messages = {}

@bot.event
async def on_ready():

    print(f'{bot.user} is now online!')

    try:
        user = await bot.fetch_user(YOUR_USER_ID)
        await user.send(" He is online and ready to forward messages!")
        print("Test message sent to your DMs")
    except Exception as e:
        print(f"Could not send test message: {e}")

@bot.event
async def on_message(message):

    if message.author == bot.user:
        return

    target_user = await bot.fetch_user(YOUR_USER_ID)

    if isinstance(message.channel, discord.DMChannel):
        original_msg_id = message.id
        user_messages[original_msg_id] = (message.author.id, None, True)

        embed = discord.Embed(
            title=f"📨 NEW DM from {message.author}",
            description=message.content if message.content else "No text content",
            color=discord.Color.blue(),  # Blue color for DMs
            timestamp=message.created_at
        )
        embed.add_field(name="User ID", value=message.author.id, inline=True)
        embed.add_field(name="Username", value=str(message.author), inline=True)
        embed.add_field(name="Message ID", value=original_msg_id, inline=True)

        if message.attachments:
            embed.add_field(name="Attachments", value=f"{len(message.attachments)} file(s)", inline=False)

        await target_user.send(embed=embed)

        for attachment in message.attachments:
            await target_user.send(f"📎 {attachment.url}")

        await message.channel.send("✅ Message forwarded! You can reply to this message and I'll send it back.")

    elif message.guild:
        if ALLOWED_CHANNEL_ID and message.channel.id != ALLOWED_CHANNEL_ID:
            await bot.process_commands(message)
            return

        original_msg_id = message.id
        user_messages[original_msg_id] = (message.author.id, message.channel.id, False)

        embed = discord.Embed(
            title=f"💬 Message from {message.author.display_name}",
            description=message.content if message.content else "No text content",
            color=discord.Color.purple(),
            timestamp=message.created_at
        )
        embed.add_field(name="User", value=str(message.author), inline=True)
        embed.add_field(name="Server", value=message.guild.name, inline=True)
        embed.add_field(name="Channel", value=f"#{message.channel.name}", inline=True)
        embed.add_field(name="Message ID", value=original_msg_id, inline=True)
        embed.add_field(name="Jump Link", value=f"[Click Here]({message.jump_url})", inline=False)

        if message.attachments:
            embed.add_field(name="Attachments", value=f"{len(message.attachments)} file(s)", inline=False)

        await target_user.send(embed=embed)

        for attachment in message.attachments:
            await target_user.send(f"📎 {attachment.url}")

    await bot.process_commands(message)



@bot.command(name='reply')
@commands.is_owner()
async def reply(ctx, message_id: int, *, reply_message):

    if message_id not in user_messages:
        await ctx.send(
            "❌ Message ID not found or expired. Make sure you copied the correct ID from the forwarded message.")
        return

    user_id, channel_id, is_dm = user_messages[message_id]

    try:
        user = await bot.fetch_user(user_id)

        if is_dm:
            embed = discord.Embed(
                title="📨 Reply from Owner",
                description=reply_message,
                color=discord.Color.gold()
            )
            await user.send(embed=embed)
            await ctx.send(f"✅ Reply sent to {user.name} via DM!")
        else:
            channel = bot.get_channel(channel_id)
            if channel:
                embed = discord.Embed(
                    title=f"📨 Reply from {ctx.author.display_name}",
                    description=reply_message,
                    color=discord.Color.gold()
                )
                await channel.send(f"<@{user_id}>", embed=embed)
                await ctx.send(f"✅ Reply sent to {user.name} in {channel.mention}!")
            else:
                await ctx.send("❌ Could not find the channel. The channel might have been deleted.")
    except Exception as e:
        await ctx.send(f"❌ Error sending reply: {e}")


@bot.command(name='list_messages')
@commands.is_owner()
async def list_messages(ctx, limit: int = 10):

    if not user_messages:
        await ctx.send("No messages have been forwarded yet.")
        return

    embed = discord.Embed(
        title="Recent Forwarded Messages",
        color=discord.Color.blue()
    )

    recent = list(user_messages.items())[-limit:]
    for msg_id, (user_id, channel_id, is_dm) in reversed(recent):
        try:
            user = await bot.fetch_user(user_id)
            location = "DM" if is_dm else f"Channel ID: {channel_id}"
            embed.add_field(
                name=f"📝 Message ID: {msg_id}",
                value=f"User: {user.name}\nLocation: {location}\n---",
                inline=False
            )
        except:
            continue

    await ctx.send(embed=embed)


@bot.command(name='set_channel')
@commands.is_owner()
async def set_channel(ctx, channel_id: int = None):

    global ALLOWED_CHANNEL_ID

    if channel_id is None:
        channel_id = ctx.channel.id

    ALLOWED_CHANNEL_ID = channel_id

    embed = discord.Embed(
        title="✅ Channel Set",
        description=f"Bot will now only forward messages from <#{channel_id}>",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

    owner = await bot.fetch_user(YOUR_USER_ID)
    await owner.send(f"✅ Channel monitoring set to: <#{channel_id}>")


@bot.command(name='remove_channel')
@commands.is_owner()
async def remove_channel(ctx):
    global ALLOWED_CHANNEL_ID
    ALLOWED_CHANNEL_ID = None

    embed = discord.Embed(
        title="✅ Channel Restriction Removed",
        description="Bot will now forward messages from all channels",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

    owner = await bot.fetch_user(YOUR_USER_ID)
    await owner.send("✅ Channel restriction removed. Now forwarding from all channels.")


@bot.command(name='status')
async def status(ctx):

    embed = discord.Embed(
        title="🤖 Bot Status",
        color=discord.Color.purple()
    )
    embed.add_field(name="Bot Name", value=bot.user.name, inline=True)
    embed.add_field(name="Bot ID", value=bot.user.id, inline=True)
    embed.add_field(name="Your User ID", value=YOUR_USER_ID, inline=False)
    embed.add_field(
        name="Monitored Channel",
        value=f"<#{ALLOWED_CHANNEL_ID}>" if ALLOWED_CHANNEL_ID else "All channels",
        inline=False
    )
    embed.add_field(name="Servers", value=len(bot.guilds), inline=True)
    embed.add_field(name="Forwarded Messages", value=len(user_messages), inline=True)

    await ctx.send(embed=embed)


@bot.command(name='invite')
async def invite(ctx):

    invite_url = discord.utils.oauth_url(
        bot.user.id,
        permissions=discord.Permissions(3072),
        scopes=('bot', 'applications.commands')
    )
    embed = discord.Embed(
        title="🔗 Invite Me!",
        description=f"[Click here to invite the bot to another server]({invite_url})",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)

if __name__ == "__main__":
    bot.run(TOKEN)