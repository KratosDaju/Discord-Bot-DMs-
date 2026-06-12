# 📬 Discord Message Forwarder Bot

A Discord bot that forwards server messages and DMs to a specific user (the bot owner) and allows replying directly from DMs.  
Perfect for monitoring servers without being online 24/7.

## ✨ Features

- **Forwards all messages** from:
  - Direct Messages (DMs) to the bot
  - Server channels (optionally restrict to a single channel)
- **Rich embeds** with message details (author, server, channel, jump link)
- **Attachment forwarding** (links to files)
- **Reply system** – use `@reply <message_id> <your reply>` from your DMs to respond
- **Channel restriction** – limit forwarding to one specific channel
- **List recent messages** – view recently forwarded messages with IDs
- **Status & invite commands** – check bot status and generate invite link
- **Owner‑only commands** – secure control

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- A Discord bot token ([Discord Developer Portal](https://discord.com/developers/applications))
- Your Discord user ID (enable Developer Mode → right‑click your name → Copy ID)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/discord-message-forwarder.git
   cd discord-message-forwarder
   Install dependencies
   
### Command	Description	Access
@reply <message_id> <text>	Reply to a forwarded message. 
The bot sends your reply to the original user/channel.	

### Owner only
@list_messages [limit=10]	Shows the most recently forwarded messages with their IDs.
@set_channel [channel_id]	Restrict forwarding to a specific channel. If no ID given, uses current channel.
@remove_channel	Remove channel restriction – forward from all channels again.

### Everyone
@status	Display bot status (name, ID, monitored channel, forwarded messages count).	
@invite	Generate an OAuth2 invite link to add the bot to another server.	

### 🔧 How It Works
Message forwarding

Any message in a DM with the bot → forwarded to you (owner) via embed + attachment links.

Any message in a server channel (or only the allowed channel) → forwarded similarly with server/channel info.

Replying

Each forwarded message includes a Message ID.

In your DM with the bot, type @reply <ID> <your message>.

The bot sends your reply back to the original user/channel.

Data storage

The bot keeps a dictionary user_messages mapping forwarded message IDs to (user_id, channel_id, is_dm).

This is in‑memory only – restarting the bot clears the map.

⚠️ Notes
The bot must have Message Content Intent enabled in the Discord Developer Portal.

For server forwarding, ensure the bot has Send Messages and Read Message History permissions.

The bot only works for messages received after it starts – past messages are not forwarded.

For replying in server channels, the bot needs permission to Send Messages in that channel.

🛠️ Customisation
Change the command prefix by modifying command_prefix='@' in commands.Bot(...).

Modify embed colours and titles in the on_message and reply command sections.

📄 License
MIT – use freely, modify, and share.

Made with ❤️ for Discord server owners who need a lightweight monitoring solution.

