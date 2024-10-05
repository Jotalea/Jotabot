#####################################################
#####################################################
##                                                 ##
##      #  ###  #####  ###      ####   ###  #####  ##
##      # #   #   #   #   #     #   # #   #   #    ##
##      # #   #   #   ##### ### ####  #   #   #    ##
##  #   # #   #   #   #   #     #   # #   #   #    ##
##   ###   ###    #   #   #     ####   ###    #    ##
##                                                 ##
#####################################################
#####################################################
# Jota-Bot | A multipurpose AI powered Discord bot

# Comes with:
# - ChatGPT and Gemini AI chat responses
# - Live Webserver
# - Server builder
# - Basic moderation commands
# - AI image generation
# - Private & public dashboard (optional)

# Example config file:
# {"admin_id":"702385902589275","ai_type":"gpt","host_server":true,"ssh_password":"123456","twitch":"https://www.twitch.tv/exjeygg","bot_token":"LKAJFJKHFDuih79ijsOIHf7duifkjh9DhkH8.89sdfUud7","api_key":"shuttle-c9ai3jrnjkag7sdoij32","gemini_key":"JflkadjfiKfjdiLJ_dIJFSDILij","api_endpoint":"https://api.shuttleai.app/v1/chat/completions"}

# Before running this code, run this command:
#   On Windows:
#       pip install -r requirements.txt
#   On Linux:
#       python3 -m pip install -r requirements.txt

# Error codes:
# -1 = Unknown
# 0 = FileNotFoundError
# 1 = ModuleNotFoundError
# 2 = NameError
# 3 = ImportError
# 4 = json.JSONDecodeError
# 5 = keyboardInterrupt
# 6 = aiohttp.client_exceptions.ServerDisconnectedError
# 7 = aiohttp.client_exceptions.ClientConnectorError
# 8 = socket.gaierror

try:
    import libjotalea as jotalea
except FileNotFoundError:
    print("\033[31m[CODE] Failed to import libjotalea. (0)\nIf you are running the program from source, then run this command to get it:\ncurl https://jotalea.com.ar/files/libjotalea.py\nIf this is a compiled program, report it to Jotalea and request a recompile.\033[0m")
    exit()
except ModuleNotFoundError:
    print("\033[31m[CODE] Failed to import libjotalea. (1)\nIf you are running the program from source, then run this command to get it:\ncurl https://jotalea.com.ar/files/libjotalea.py\nIf this is a compiled program, report it to Jotalea and request a recompile.\033[0m")
    exit()
except NameError:
    print("\033[31m[CODE] Failed to import libjotalea. (2)\nIf you are running the program from source, then run this command to get it:\ncurl https://jotalea.com.ar/files/libjotalea.py\nIf this is a compiled program, report it to Jotalea and request a recompile.\033[0m")
    exit()

try:
    import aiohttp, asyncio, discord, json, os, psutil, random, socket, subprocess, sqlite3, time, google.generativeai
    from datetime import datetime, timedelta
    from discord.ext import commands
    from discord.ext.commands import has_permissions
    from discord.gateway import DiscordWebSocket
    from shuttleai import *
    from flask import Flask, send_from_directory, render_template, request
    from threading import Thread
except ImportError:
    print("\033[31m[CODE] Failed to import libraries. (3)\nIf you are running the program from source, then run this command to install them all:\npip install -r requirements.txt\nAnd make sure to have the latest version of libjotalea, which should be in the same directory as this file.\nIf this is a compiled program, report it to Jotalea and request a recompile.\033[0m")
    exit()

###########################################################################
###########################################################################

try:
    try:
        with open("settings.json", 'r') as file:
            settings = json.load(file)
            jotalea.prettyprint("green", "[CODE] Settings file imported sucessfully.")
            settings_admin_id = str(settings["admin_id"])
            settings_is_replit = bool(settings["host_server"])
            settings_AI_type = settings["ai_type"] # "gpt" or "gemini"
            settings_ssh_password = str(settings["ssh_password"])
            settings_twitch_channel = settings["twitch"]
            botToken = settings["bot_token"]
            jotalea.GPT_KEY = settings["api_key"]
            jotalea.GPT_ENDPOINT = settings["api_endpoint"]
            jotalea.GEMINI_KEY = settings["gemini_key"]
    except FileNotFoundError:
        jotalea.prettyprint("red", "[CODE] Settings file not found (0). Insert them manually or create the settings file.")
        jotalea.prettyprint("green", "[CODE] Create settings file.")
        settings_admin_id = str(input("[CODE] Paste the user ID of the admin: "))
        while True:
            settings_is_replit = bool(input("[CODE] Host a website?\nType True or False: "))
            if settings_is_replit.lower() == "true":
                break
            elif settings_is_replit.lower() == "false":
                break
            print("That is not a valid value")
        while True:
            settings_AI_type = input("[CODE] Options: \"gpt\", \"gemini\"\nWhat kind of AI to use? ") # "gpt" or "gemini"
            if settings_AI_type.lower() == "gpt":
                settings_AI_type = settings_AI_type.lower()
                break
            elif settings_AI_type.lower() == "gemini":
                settings_AI_type = settings_AI_type.lower()
                break
            print("That is not a valid AI model")
        settings_ssh_password = str(input("[CODE] Type the password that will be used with SSH command: "))
        settings_twitch_channel = input("[CODE] Paste the URL of your Twitch channel: https://twitch.tv/")
        settings_twitch_channel = "https://twitch.tv/" + settings_twitch_channel
        botToken = input("[CODE] Paste the bot token: ")
        apiKey = input("[CODE] Paste the ShuttleAI API Key: ")
        geminiKey = input("[CODE] Paste the Gemini API Key: ")
        while True:
            apiEndpoint = input("[CODE] Paste the API Endpoint (none for default): ")
            if settings_AI_type.startswith("https://"):
                break
            print("That is not a valid URL")
        formato = '{"admin_id":"' + str(settings_admin_id) + '","ai_type":"' + str(settings_AI_type) + '","host_server":' + str(settings_is_replit.lower()) + ',"ssh_password":"' + str(settings_ssh_password) + '","twitch":"' + str(settings_twitch_channel) + '","bot_token":"' + str(botToken) + '","api_key":"' + str(apiKey) + '","gemini_key":"' + str(geminiKey) + '","api_endpoint":"' + str(apiEndpoint) + '"}'
        with open("settings.json", "w", encoding="utf-8") as settings_file:
            settings_file.write(formato.json())
    except json.JSONDecodeError:
        jotalea.prettyprint("red", "[CODE] The Settings file has an invalid format (4). Create a new one.")

    ###########################################################################
    ###########################################################################

    # Settings
    settings_embed_color = 0x9bff30
    settings_bot_version = "4.18.6"

    settings_printlog = True
    settings_logging = True
    settings_use_async = True
    settings_log_webhook = "https://discord.com/api/webhooks/1179211143747747953/CabPxEffLyOzczS-53-rEr7ADd3b-Hc7YziOX-911FOHyZU4KrP-68aJaH53p3rLDpX8"
    settings_allowed_users = [settings_admin_id]

    settings_logo = " \033[32m     ██╗ ██████╗ ████████╗ █████╗     \033[36m    ██████╗  ██████╗ ████████╗\n \033[32m     ██║██╔═══██╗╚══██╔══╝██╔══██╗    \033[36m    ██╔══██╗██╔═══██╗╚══██╔══╝\n \033[32m     ██║██║   ██║   ██║   ███████║\033[37m █████╗ \033[36m██████╔╝██║   ██║   ██║   \n \033[32m██   ██║██║   ██║   ██║   ██╔══██║\033[37m ╚════╝ \033[36m██╔══██╗██║   ██║   ██║   \n \033[32m╚█████╔╝╚██████╔╝   ██║   ██║  ██║    \033[36m    ██████╔╝╚██████╔╝   ██║   \n \033[32m ╚════╝  ╚═════╝    ╚═╝   ╚═╝  ╚═╝    \033[36m    ╚═════╝  ╚═════╝    ╚═╝   \n\033[0m"
    settings_logo_arg = "\033[36m     ██╗ ██████╗ ████████╗ █████╗         ██████╗  ██████╗ ████████╗\n     ██║██╔═══██╗╚══██╔══╝██╔══██╗        ██╔══██╗██╔═══██╗╚══██╔══╝\n\033[37m     ██║██║   ██║   ██║   ███████║\033[33m █████╗ \033[37m██████╔╝██║   ██║   ██║   \n██   ██║██║   ██║   ██║   ██╔══██║\033[33m ╚════╝ \033[37m██╔══██╗██║   ██║   ██║   \n\033[36m╚█████╔╝╚██████╔╝   ██║   ██║  ██║        ██████╔╝╚██████╔╝   ██║   \n ╚════╝  ╚═════╝    ╚═╝   ╚═╝  ╚═╝        ╚═════╝  ╚═════╝    ╚═╝   \033[0m"
    settings_logo_no_color = "      ██╗ ██████╗ ████████╗ █████╗         ██████╗  ██████╗ ████████╗\n      ██║██╔═══██╗╚══██╔══╝██╔══██╗        ██╔══██╗██╔═══██╗╚══██╔══╝\n      ██║██║   ██║   ██║   ███████║ █████╗ ██████╔╝██║   ██║   ██║   \n ██   ██║██║   ██║   ██║   ██╔══██║ ╚════╝ ██╔══██╗██║   ██║   ██║   \n ╚█████╔╝╚██████╔╝   ██║   ██║  ██║        ██████╔╝╚██████╔╝   ██║   \n  ╚════╝  ╚═════╝    ╚═╝   ╚═╝  ╚═╝        ╚═════╝  ╚═════╝    ╚═╝   \n"

    ###########################################################################
    ##########################################################################
    #print()
    jotalea.gradient(text=settings_logo_no_color, mode="by-character-diagonal", start_color=[3, 254, 11], end_color=[1, 215, 214])
    #print(f"\n{settings_logo}\033[0m")
    jotalea.prettyprint("green", f"[CODE] Version: {settings_bot_version}")

    ###########################################################################
    ###########################################################################
    # Server
    def webserver():
        app = Flask(__name__)

        @app.route('/', methods=["GET"])
        def index():
            result = 0
            for guild in bot.guilds:
                result = result + 1
            return render_template('index.html', total_servers=result)

        @app.route('/setting/<setting>', methods=["GET","POST"])
        def change_setting(setting):
            global settings_AI_type, settings_admin_id, settings_allowed_users, settings_embed_color, settings_log_webhook, settings_logging, settings_ssh_password, settings_twitch_channel, settings_use_async, settings_printlog
            # AI model setting
            if setting == "aimodel":
                # Change
                if request.method == "POST":
                    if str(request.form["content"]) == "gpt":
                        settings_AI_type = "gpt"
                        return "True"
                    elif str(request.form["content"]) == "gemini":
                        settings_AI_type = "gemini"
                        return "True"
                    else:
                        return "False"
                # Retrieve
                else:
                    return settings_AI_type
            # Admin ID setting
            elif setting == "adminid":
                # Change
                if request.method == "POST":
                    settings_admin_id = str(request.form["content"])
                    return "True"
                # Retrieve
                else:
                    return settings_admin_id
            # SSH users setting
            elif setting == "sshusers":
                # Change
                if request.method == "POST":
                    settings_allowed_users = request.form["content"].split(",")
                    return "True"
                # Retrieve
                else:
                    return settings_allowed_users
            # Embed color setting
            elif setting == "embedcolor":
                # Change
                if request.method == "POST":
                    settings_embed_color = str(request.form["content"])
                    return "True"
                # Retrieve
                else:
                    return settings_embed_color
            # Log webhook setting
            elif setting == "webhook":
                # Change
                if request.method == "POST":
                    settings_log_webhook = str(request.form["content"])
                    return "True"
                # Retrieve
                else:
                    return settings_log_webhook
            # Logging setting
            elif setting == "logging":
                # Change
                if request.method == "POST":
                    settings_logging = str(request.form["content"])
                    return "True"
                # Retrieve
                else:
                    return settings_logging
            # SSH password setting
            elif setting == "sshpass":
                # Change
                if request.method == "POST":
                    settings_ssh_password = str(request.form["content"])
                    return "True"
                # Retrieve
                else:
                    return settings_ssh_password
            # Twitch channel setting
            elif setting == "twitch":
                # Change
                if request.method == "POST":
                    settings_twitch_channel = str(request.form["content"])
                    return "True"
                # Retrieve
                else:
                    return settings_twitch_channel
            # Use async setting
            elif setting == "useasync":
                # Change
                if request.method == "POST":
                    settings_use_async = str(request.form["content"])
                    return "True"
                # Retrieve
                else:
                    return settings_use_async
            # Print log setting
            elif setting == "printlog":
                # Change
                if request.method == "POST":
                    settings_printlog = str(request.form["content"])
                    return "True"
                # Retrieve
                else:
                    return settings_printlog
            ### Available endpoints
            ### Change AI model setting to 'gpt'
            #curl -X POST -d "content=gpt" http://yourserver.com/setting/aimodel
            ## Retrieve AI model setting
            #curl -X GET http://yourserver.com/setting/aimodel
            ## Change admin ID setting
            #curl -X POST -d "content=new_admin_id" http://yourserver.com/setting/adminid
            ## Retrieve admin ID setting
            #curl -X GET http://yourserver.com/setting/adminid
            ## Change SSH users setting
            #curl -X POST -d "content=user1,user2,user3" http://yourserver.com/setting/sshusers
            ## Retrieve SSH users setting
            #curl -X GET http://yourserver.com/setting/sshusers
            ## Change embed color setting
            #curl -X POST -d "content=new_color" http://yourserver.com/setting/embedcolor
            ## Retrieve embed color setting
            #curl -X GET http://yourserver.com/setting/embedcolor
            ## Change log webhook setting
            #curl -X POST -d "content=new_webhook" http://yourserver.com/setting/webhook
            ## Retrieve log webhook setting
            #curl -X GET http://yourserver.com/setting/logwebhook
            ## Change logging setting
            #curl -X POST -d "content=new_logging" http://yourserver.com/setting/logging
            ## Retrieve logging setting
            #curl -X GET http://yourserver.com/setting/logging
            ## Change SSH password setting
            #curl -X POST -d "content=new_password" http://yourserver.com/setting/sshpass
            ## Retrieve SSH password setting
            #curl -X GET http://yourserver.com/setting/sshpass
            ## Change Twitch channel setting
            #curl -X POST -d "content=new_channel" http://yourserver.com/setting/twitchchannel
            ## Retrieve Twitch channel setting
            #curl -X GET http://yourserver.com/setting/twitchchannel
            ## Change use async setting
            #curl -X POST -d "content=new_async" http://yourserver.com/setting/useasync
            ## Retrieve use async setting
            #curl -X GET http://yourserver.com/setting/useasync
            ## Change print log setting
            #curl -X POST -d "content=new_printlog" http://yourserver.com/setting/printlog
            ## Retrieve print log setting
            #curl -X GET http://yourserver.com/setting/printlog

        @app.route('/stat/<statistic>')
        def individualStatistic(statistic):
            global bot
            if statistic == "totalservers":
                result = 0
                for guild in bot.guilds:
                    result = result + 1
                return str(result)
            elif statistic == "totalservers1":
                return bot.guilds.count
            elif statistic == "name":
                return bot.user.name + "#" + bot.user.discriminator
            elif statistic == "avatar":
                return f"<img src='{bot.user.avatar.url}'>"
            elif statistic == "description":
                return bot.description
            elif statistic == "verified":
                return str(bot.user.verified)
            else:
                return

        @app.route('/status')
        def allStatistics():
            global bot
            totalguilds = 0
            for guild in bot.guilds:
                totalguilds = totalguilds + 1
            return render_template("stats.html", totalservers=totalguilds)
        
        @app.route('/file/<filename>')
        def download_file(filename):
            return send_from_directory('files', filename)

        @app.route('/about')
        def about():
            content = """
            <!DOCTYPE html>
            <html>
            <head>
            <meta charset="utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1" />
            <title>Jotabot - About</title>
            </head>
            <body>
            <h1>Jotabot</h1>
            <p>Developed by Jotalea</p>
            <a href="https://jotalea.com.ar/discord">Contact on Discord</a>
            </body>
            </html>
            """
            return content

        @app.route('/user/<username>')
        def show_user_profile(username):
            return f'User {username}'

        @app.route('/logs')
        def show_logs():
            logs = json.dumps(log_history, indent=2, separators=(',', ':')) #
            logs = logs.replace("\n", "<br>")
            f'Conversation logs:<br>{logs}'
            return f'<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><meta http-equiv="refresh" content="1"><title>Logs</title></head><body><header><h1>Logging</h1></header><p>{logs}</p><footer><p>&copy; 2024 Jota-Bot</p></footer></body></html>'#render_template("logs.html", logs=logs)

        def run():
            app.run(host='0.0.0.0',port=8081)

        t = Thread(target=run) 
        t.start()

    ###########################################################################
    ###########################################################################

    bot = commands.Bot(command_prefix='j!', intents=discord.Intents.all())
    bot.remove_command('help')

    database = sqlite3.connect('counter.db')
    cursor = database.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS server_count (
        id INT PRIMARY KEY,
        count INT,
        ping TEXT,
        cpu TEXT,
        ram TEXT,
        version TEXT,
        uptime TEXT
        )
    ''')
    database.commit()

    chat_history = {}
    log_history = []

    async def identify(self):
        payload = {
            "op": self.IDENTIFY,
            "d": {
                "token": self.token,
                "properties": {
                    "$os": "Discord Android",
                    "$browser": "Discord Android",
                    "$device": "Android",
                    "$referrer": "",
                    "$referring_domain": "",
                },
                "compress": True,
                "large_threshold": 250,
            },
        }

        if self.shard_id is not None and self.shard_count is not None:
            payload["d"]["shard"] = [self.shard_id, self.shard_count]

        state = self._connection
        if state._activity is not None or state._status is not None:
            payload["d"]["presence"] = {
                "status": state._status,
                "game": state._activity,
                "since": 0,
                "afk": False,
            }

        if state._intents is not None:
            payload["d"]["intents"] = state._intents.value

        await self.call_hooks("before_identify", self.shard_id, initial=self._initial_identify)
        await self.send_as_json(payload)

    #if random.choice([True, False]):
    #    DiscordWebSocket.identify = identify

    DiscordWebSocket.identify = identify

    # Store the bot's start time
    bot.start_time = time.time()

    # Función para desbanear a un usuario
    async def unban_user(ctx, args):
        jotalea.prettyprint("cyan", "[COMMAND] j!ban unban command requested")

        # Extrae el ID del usuario a desbanear
        user_id_str = args.split("user=")[1].split(",")[0]
        user_id = int(user_id_str)

        # Obtiene la lista de usuarios baneados
        ban_list = await ctx.guild.bans()

        # Busca al usuario en la lista de usuarios baneados
        for entry in ban_list:
            if entry.user.id == user_id:
                # Desbanea al usuario
                await ctx.guild.unban(entry.user)
                embed = discord.Embed(title="User Unbanned", description=f"User with ID {user_id} has been unbanned.", color=settings_embed_color)
                await ctx.send(embed=embed)
                jotalea.prettyprint("green", f"[COMMAND] Unbanned user with ID {user_id}")
                return

        # Envía un mensaje si el usuario no está en la lista de baneados
        embed = discord.Embed(title="Error", description=f"User with ID {user_id} not found in the ban list.", color=settings_embed_color)
        await ctx.send(embed=embed)
        jotalea.prettyprint("red", f"[COMMAND] User with ID {user_id} not found in the ban list")

    async def show_ban_list(ctx):
        jotalea.prettyprint("cyan", "[COMMAND] j!ban list command requested")

        # Obtiene la lista de usuarios baneados
        ban_list = await ctx.guild.bans()

        if ban_list:
            # Formatea la lista de usuarios baneados
            banned_users = [f"@{entry.user.name} (Ping: <@{entry.user.id}>, ID: {entry.user.id})" for entry in ban_list]
            banned_list_str = "\n".join(banned_users)

            # Envía la lista de usuarios baneados
            embed = discord.Embed(title="Banned Users", description=banned_list_str, color=settings_embed_color)
            await ctx.send(embed=embed)

            jotalea.prettyprint("green", "[COMMAND] Banned user list sent")
        else:
            # Envía un mensaje si no hay usuarios baneados
            embed = discord.Embed(title="Banned Users", description="No users are currently banned.", color=settings_embed_color)
            await ctx.send(embed=embed)
            jotalea.prettyprint("green", "[COMMAND] No users are currently banned")

    # Commands

    @bot.command()
    async def activity(ctx, *, args):
        # j!activity state
        jotalea.prettyprint("cyan", "[COMMAND] j!activity command requested")
        if str(ctx.message.author.id) == settings_admin_id:
            pass
        else: # Block
            embed = discord.Embed(title="Error", description=f"{ctx.author.display_name} doesn't have bot owner permissions", color=settings_embed_color)
            await ctx.reply(embed=embed)
            return
        
        status = ""
        status_content = ""

        args_list = args.split(", ")
        for arg in args_list:
            key, value = arg.split("=")
            if key == "state":
                status = value.strip('"')
            elif key == "content":
                status_content = value.strip('"')

        if status.lower() == "playing":
            await bot.change_presence(activity=discord.Game(name=status_content))

        if status.lower() == "watching":
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status_content))

        if status.lower() == "listening":
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=status_content))

        if status.lower() == "streaming":
            await bot.change_presence(activity=discord.Streaming(name=status_content, url=settings_twitch_channel))

        if status.lower() == "competing":
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name=status_content))

        if status.lower() == "custom":
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.custom, name=status_content))

        embed = discord.Embed(title=f"Activity set", description=f"Activity `{status.lower()} {status_content}` set successfully.", color=settings_embed_color)
        await ctx.send(embed=embed)
        jotalea.prettyprint("green", "[COMMAND] j!activity command responded")

    @bot.command()
    @has_permissions(administrator=True)
    async def ban(ctx, *, args):
        jotalea.prettyprint("cyan", "[COMMAND] j!ban command requested")

        if args.lower() == "list":
            await show_ban_list(ctx)
            return

        if args.lower().startswith("user=") and ", unban" in args.lower():
            await unban_user(ctx, args)
            return

        user_id = None
        reason = "No reason given"

        args_list = args.split(", ")
        for arg in args_list:
            key, value = arg.split("=")
            if key == "user":
                user_id = int(value)
            elif key == "reason":
                reason = value.strip('"')

        if user_id:
            user = ctx.guild.get_member(user_id)
            if user:
                await ctx.guild.ban(user, reason=reason)
                embed = discord.Embed(title="User Banned", description=f"{user.mention} has been banned for: {reason}", color=settings_embed_color)
                await ctx.reply(embed=embed, mention_author=True)
                jotalea.prettyprint("green", f"[COMMAND] Banned {user.mention}")
            else:
                embed = discord.Embed(title="Error", description="User not found.", color=settings_embed_color)
                await ctx.reply(embed=embed, mention_author=True)
                jotalea.prettyprint("red", "[COMMAND] User not found")
        else:
            embed = discord.Embed(title="Invalid Syntax", description="Use `j!ban user=1234567890, reason='Your reason here'` or `j!ban list` or `j!ban user=1234567890, unban.", color=settings_embed_color)
            await ctx.reply(embed=embed, mention_author=True)
            jotalea.prettyprint("red", "[COMMAND] Invalid syntax")

    @bot.command()
    async def crear(ctx):
        try:
            embed = discord.Embed(title="Formatting server", description="Formatting this server with a basic format", color=settings_embed_color)
            await ctx.reply(embed=embed)
            # Permissions
            owner_permissions   = discord.Permissions(kick_members=True, create_instant_invite=True, ban_members=True, administrator=True, manage_channels=True, manage_guild=True, add_reactions=True,view_audit_log=True, priority_speaker=True, stream=True,read_messages=True,send_messages=True,send_tts_messages=True, manage_messages=True, embed_links=True,attach_files=True,read_message_history=True,mention_everyone=True, external_emojis=True,view_guild_insights=True, connect=True,speak=True,mute_members=True, deafen_members=True, move_members=True, use_voice_activation=True, change_nickname=True, manage_nicknames=True, manage_roles=True, manage_webhooks=True, manage_emojis=True )
            admin_permissions   = discord.Permissions(kick_members=True, create_instant_invite=True, ban_members=True, administrator=True, manage_channels=True, manage_guild=False,add_reactions=True,view_audit_log=True, priority_speaker=False,stream=True,read_messages=True,send_messages=True,send_tts_messages=True, manage_messages=True, embed_links=True,attach_files=True,read_message_history=True,mention_everyone=True, external_emojis=True,view_guild_insights=True, connect=True,speak=True,mute_members=True, deafen_members=True, move_members=True, use_voice_activation=True, change_nickname=True, manage_nicknames=True, manage_roles=True, manage_webhooks=False,manage_emojis=True )
            staff_permissions   = discord.Permissions(kick_members=True, create_instant_invite=True, ban_members=False,administrator=False,manage_channels=False,manage_guild=True, add_reactions=True,view_audit_log=True, priority_speaker=True, stream=True,read_messages=True,send_messages=True,send_tts_messages=True, manage_messages=True, embed_links=True,attach_files=True,read_message_history=True,mention_everyone=True, external_emojis=True,view_guild_insights=False,connect=True,speak=True,mute_members=True, deafen_members=True, move_members=True, use_voice_activation=True, change_nickname=True, manage_nicknames=True, manage_roles=True, manage_webhooks=False,manage_emojis=True )
            booster_permissions = discord.Permissions(kick_members=False,create_instant_invite=True, ban_members=False,administrator=False,manage_channels=False,manage_guild=False,add_reactions=True,view_audit_log=False,priority_speaker=True, stream=True,read_messages=True,send_messages=True,send_tts_messages=True, manage_messages=True, embed_links=True,attach_files=True,read_message_history=True,mention_everyone=False,external_emojis=True,view_guild_insights=False,connect=True,speak=True,mute_members=True, deafen_members=True, move_members=True, use_voice_activation=True, change_nickname=True, manage_nicknames=False,manage_roles=False,manage_webhooks=False,manage_emojis=True )
            member_permissions  = discord.Permissions(kick_members=False,create_instant_invite=True, ban_members=False,administrator=False,manage_channels=False,manage_guild=False,add_reactions=True,view_audit_log=False,priority_speaker=False,stream=True,read_messages=True,send_messages=True,send_tts_messages=True, manage_messages=False,embed_links=True,attach_files=True,read_message_history=True,mention_everyone=False,external_emojis=True,view_guild_insights=False,connect=True,speak=True,mute_members=False,deafen_members=False,move_members=False,use_voice_activation=False,change_nickname=False,manage_nicknames=False,manage_roles=False,manage_webhooks=False,manage_emojis=False)
            bot_permissions     = discord.Permissions(kick_members=True, create_instant_invite=False,ban_members=True, administrator=False,manage_channels=False,manage_guild=False,add_reactions=True,view_audit_log=False,priority_speaker=False,stream=True,read_messages=True,send_messages=True,send_tts_messages=False,manage_messages=True, embed_links=True,attach_files=True,read_message_history=True,mention_everyone=False,external_emojis=True,view_guild_insights=False,connect=True,speak=True,mute_members=True, deafen_members=True, move_members=True, use_voice_activation=False,change_nickname=True, manage_nicknames=False,manage_roles=False,manage_webhooks=False,manage_emojis=False)

            await ctx.guild.create_category(name="═══Server═══")
            await ctx.guild.create_category(name="═══Chat═════")
            await ctx.guild.create_category(name="═══Audio════")
            await ctx.guild.create_category(name="═══Misc.════")

            category = discord.utils.get(ctx.guild.categories, name="═══Server═══")
            await category.create_text_channel("╔═[📢]anuncios")
            await category.create_text_channel("╠═[📜]reglas")
            await category.create_text_channel("╠═[🎉]sorteos")
            await category.create_text_channel("╠═[📊]encuestas")
            await category.create_text_channel("╠═[🆙]niveles")
            await category.create_text_channel("╠═[🎈]eventos")
            await category.create_text_channel("╠═[👋]bienvenidas")
            await category.create_text_channel("╠═[👋]despedidas")
            await category.create_text_channel("╠═[🚫]baneos")
            await category.create_text_channel("╚═[⚠️]warns")

            category = discord.utils.get(ctx.guild.categories, name="═══Chat═════")
            await category.create_text_channel("╔═[💬]general")
            await category.create_text_channel("╠═[🖼️]media")
            await category.create_text_channel("╠═[😂]memes")
            await category.create_text_channel("╠═[🤖]commands")
            await category.create_text_channel("╚═[🤖]jotabot-commands")

            category = discord.utils.get(ctx.guild.categories, name="═══Audio════")
            await category.create_voice_channel("╔═[🔊]general-1")
            await category.create_voice_channel("╠═[🔊]general-2")
            await category.create_voice_channel("╠═[🎮]gaming-1")
            await category.create_voice_channel("╠═[🎮]gaming-2")
            await category.create_voice_channel("╠═[🎤]streaming")
            await category.create_voice_channel("╚═[🔇]no-mic")

            # category = discord.utils.get(ctx.guild.categories, name="═══Misc.════")
            # await category.create_text_channel("general-1")
            # await category.create_voice_channel("no-mic")

            await ctx.guild.create_role(name = "Owner",   permissions =   owner_permissions)
            await ctx.guild.create_role(name = "Admin",   permissions =   admin_permissions)
            await ctx.guild.create_role(name = "Staff",   permissions =   staff_permissions)
            await ctx.guild.create_role(name = "Booster", permissions = booster_permissions)
            await ctx.guild.create_role(name = "Miembro", permissions =  member_permissions)
            await ctx.guild.create_role(name = "Bot",     permissions =     bot_permissions)
        except Exception as e:
            embed = discord.Embed(title="Error formatting server", description=f"Error: {e}", color=settings_embed_color)
            await ctx.reply(embed=embed)

    @bot.command()
    async def createinvites(ctx):
        jotalea.prettyprint("cyan", "[COMMAND] j!createinvites command requested")
        if str(ctx.author.id) != str(settings_admin_id):
            await ctx.reply("Command not found.", mention_author=True)
            return

        invites = []
        for guild in bot.guilds:
            try:
                text_channel = next((x for x in guild.channels if isinstance(x, discord.TextChannel)), None)
                if text_channel:
                    invite = await text_channel.create_invite(max_age=900)  # Invitación que expira en 15 minutos
                    invites.append(f"{guild.name}: {invite.url}")
                else:
                    invites.append(f"{guild.name}: Could not create an invite (no channel available).")
            except Exception as e:
                invites.append(f"{guild.name}: Error creating the invite - {e}")

        response = "\n".join(invites)
        if len(response) > 2000:
            await ctx.author.send(response)
        else:
            await ctx.send(response)

    @bot.command()
    async def credits(ctx):
        jotalea.prettyprint("cyan", "[COMMAND] j!credits command requested")
        embed = discord.Embed(title="Jota-Bot Credits", description="Programmed by <@795013781607546931>\nProfile Picture made by <@1015852332266815559>\nInspired by <@836623013641191464>\nTesting by:\n- <@1093363729955049503>\n- <@795013781607546931>", color=settings_embed_color)
        await ctx.reply(embed=embed, mention_author=True)
        jotalea.prettyprint("green", "[COMMAND] j!credits command responded")

    @bot.command()
    async def emoji(ctx, *, emoji_name):
        jotalea.prettyprint("cyan", "[COMMAND] j!emoji command requested")
        emoji = discord.utils.get(ctx.guild.emojis, name=emoji_name)

        if emoji:
            embed = discord.Embed(title=f'Information about this emoji :{emoji_name}:', color=settings_embed_color)
            embed.add_field(name='Name', value=f':{emoji_name}:', inline=False)
            embed.add_field(name='ID', value=emoji.id, inline=False)
            embed.add_field(name='URL', value=emoji.url, inline=False)

            await ctx.reply(embed=embed, mention_author=True)
            jotalea.prettyprint("green", "[COMMAND] j!emoji command responded")
        else:
            await ctx.reply(f'That emoji isn\'t from this server (or I can\'t find it).', mention_author=True)
            jotalea.prettyprint("red", "[COMMAND] j!emoji command failed, but responded anyway")

    @bot.command()
    async def help(ctx):
        jotalea.prettyprint("cyan", "[COMMAND] j!help command requested")
        embed = discord.Embed(title="Help - Available Commands", description=f"- `j!ban`: Bans a user (admin only). Syntax: `j!ban user=1234567890, reason='Your reason here'` (123... is the user ID placeholder).\n- `j!ban list`: Get a list of the banned users.\n- `j!ban unban 1234567890123`: Remove a user's ban.\n- `j!credits`: Show the bot's credits.\n- `j!emoji`: Get information about an emoji.\n- `j!getinvite`: Get a temporary invite to this server.\n- `j!help`: Show this list.\n- `j!invite`: Get the invite link for Jota-Bot.\n- `j!kick`: Kicks a user (admin only). Syntax: `j!kick user=1234567890` (123... is the user ID placeholder).\n- `j!ping`: Check if the bot is online.\n- `j!rr`: Play the russian roulette.\n- `j!say`: Make the bot say something.\n- `j!setup`: Create an organized server from a template. (Para servidores en español `j!crear`)\n- `j!shutdown`: Turn off the bot (Only for Jotalea).\n- `j!ssh`: Connect to Jotalea's computer.\n- `j!tts`: Generates a Text-To-Speech using AI.\n- `j!uptime`: Shows how much time has the bot been running.\n- `j!version`: Shows the current bot version.\n- `j!web`: Get the link of Jotalea's website.\n\n\"{bot.user.mention} Message\" Ask anything to the AI behind Jota-Bot (May not always work)", color=settings_embed_color)
        await ctx.reply(embed=embed, mention_author=True)
        jotalea.prettyprint("green", "[COMMAND] j!help command responded")

    @bot.command(name='info')
    async def info(ctx):
        # Obtener información
        bot_ram_usage = psutil.virtual_memory().percent
        bot_cpu_usage = psutil.cpu_percent()
        bot_ping = round(bot.latency * 1000)
        api_ping = round((discord.utils.utcnow() - ctx.message.created_at).total_seconds() * 1000)

        # Crear un embed con la información
        embed = discord.Embed(title='Bot Information', color=discord.Color.blue())
        embed.set_thumbnail(url=bot.user.avatar.url)
        embed.add_field(name='Bot Username', value=bot.user.name, inline=False)
        embed.add_field(name='Servers', value=len(bot.guilds), inline=True)
        embed.add_field(name='Members in Current Server', value=len(ctx.guild.members), inline=True)
        embed.add_field(name='Bot Version', value=settings_bot_version, inline=False)
        embed.add_field(name='RAM Usage', value=f'{bot_ram_usage}%', inline=True)
        embed.add_field(name='CPU Usage', value=f'{bot_cpu_usage}%', inline=True)
        embed.add_field(name='Bot Ping', value=f'{bot_ping} ms', inline=True)
        embed.add_field(name='API Ping', value=f'{api_ping} ms', inline=True)
        embed.add_field(name='Bot Prefix', value=bot.command_prefix, inline=False)

        # Enviar el embed al canal
        await ctx.reply(embed=embed, mention_author=True)

    @bot.command()
    async def invite(ctx):
        jotalea.prettyprint("cyan", "[COMMAND] j!invite command requested")
        embed = discord.Embed(title="Invite JotaBOT", description="Invite JotaBOT to your Discord server :) You can do that using [this link](https://discord.com/api/oauth2/authorize?client_id=1142577469422051478&permissions=10291617721719&scope=bot+applications.commands)\n||https://discord.com/api/oauth2/authorize?client_id=1142577469422051478&permissions=10291617721719&scope=bot+applications.commands||", color=settings_embed_color)
        await ctx.reply(embed=embed, mention_author=True)
        jotalea.prettyprint("green", "[COMMAND] j!invite command responded")

    @bot.command()
    @has_permissions(administrator=True)
    async def kick(ctx, *, args):
        jotalea.prettyprint("cyan", "[COMMAND] j!kick command requested")

        user_id = None

        args_list = args.split(", ")
        for arg in args_list:
            key, value = arg.split("=")
            if key == "user":
                user_id = int(value)

        if user_id:
            user = ctx.guild.get_member(user_id)
            if user:
                await ctx.guild.kick(user)
                embed = discord.Embed(title="User Kicked", description=f"{user.mention} has been kicked.", color=settings_embed_color)
                await ctx.reply(embed=embed, mention_author=True)
                jotalea.prettyprint("green", f"[COMMAND] j!kick Kicked {user.mention}")
            else:
                embed = discord.Embed(title="Error", description="User not found.", color=settings_embed_color)
                await ctx.reply(embed=embed, mention_author=True)
                jotalea.prettyprint("red", "[COMMAND] j!kick User not found")
        else:
            embed = discord.Embed(title="Invalid Syntax", description="Use `j!kick user=1234567890`.", color=settings_embed_color)
            await ctx.reply(embed=embed, mention_author=True)
            jotalea.prettyprint("red", "[COMMAND] j!kick Invalid syntax")

    @bot.command(name='leaderboard')
    async def leaderboard(ctx):
        jotalea.prettyprint("cyan", "[COMMAND] j!leaderboard command requested")
        try:
            guilds = sorted(bot.guilds, key=lambda guild: guild.member_count, reverse=True)[:10]
            description = '\n'.join(f'**{i+1}. {guild.name}**Has {guild.member_count} member(s)' for i, guild in enumerate(guilds))
            embed = discord.Embed(title='Leaderboard - Servers with most members', description=description, color=settings_embed_color)
            if guilds and guilds[0].icon:
                embed.set_thumbnail(url=guilds[0].icon.url)
            await ctx.reply(embed=embed)
            jotalea.prettyprint("green", "[COMMAND] j!leaderboard command responded")
        except Exception as e:
            await ctx.reply(f"`Error when processing command j!leaderboard: {str(e)}`")
            jotalea.prettyprint("red", f"[COMMAND] Error when processing command j!leaderboard: {str(e)}")

    @bot.command()
    async def ping(ctx):
        jotalea.prettyprint("cyan", "[COMMAND] j!ping command requested")

        cpu_percent = psutil.cpu_percent()
        memory_percent = psutil.virtual_memory().percent

        bot_latency = round(bot.latency * 1000)
        api_latency = round((discord.utils.utcnow() - ctx.message.created_at).total_seconds() * 1000)

        embed = discord.Embed(title="Pong!", color=settings_embed_color)
        embed.add_field(name="Bot ping", value=f"{bot_latency}ms")
        embed.add_field(name="API ping", value=f"{api_latency}ms")
        embed.add_field(name="CPU Usage", value=f"{cpu_percent}%")
        embed.add_field(name="RAM Usage", value=f"{memory_percent}%")
        await ctx.reply(embed=embed, mention_author=True)
        jotalea.prettyprint("green", "[COMMAND] j!ping command responded")

    @bot.command()
    async def rr(ctx):
        jotalea.prettyprint("red", "[COMMAND] j!rr command requested")

        def check(message):
            return message.author.id == ctx.author.id and message.channel.id == ctx.channel.id

        embed = discord.Embed(title="Russian Roulette", description="Rules:\n- Once you react with :white_check_mark:, there's no way back\n- If you win, nothing happens\n- But if you lose, you'll get **banned**\n\nAre you sure you want to play? (react with ✅/❌)", color=settings_embed_color)
        message = await ctx.reply(embed=embed, mention_author=True)
        await message.add_reaction('✅')
        await message.add_reaction('❌')
        await bot.wait_for("reaction", check=check, timeout=60)
        jotalea.prettyprint("green", "[COMMAND] j!rr command responded")

    @bot.command()
    async def say(ctx):
        jotalea.prettyprint("cyan", "[COMMAND] j!say command requested")
        if ctx.message.content == "j!say":
            embed = discord.Embed(title="Wrong syntax", description="Use `j!say Your message`", color=settings_embed_color)
            await ctx.reply(embed=embed, mention_author=True)
        if ctx.message.content == "j!say ":
            embed = discord.Embed(title="Wrong syntax", description="Use `j!say Your message`", color=settings_embed_color)
            await ctx.reply(embed=embed, mention_author=True)
        message_to_say = ctx.message.content.replace("j!say ", "")
        await ctx.message.delete()
        embed = discord.Embed(title=f"{ctx.author.display_name} says:", description=message_to_say, color=settings_embed_color)
        await ctx.send(embed=embed)
        jotalea.prettyprint("green", "[COMMAND] j!say command responded")

    @bot.command()
    async def secretsay(ctx):
        if str(ctx.author.id) == str(settings_admin_id):
            pass
        else:
            embed = discord.Embed(title="No admin", description="You aren't the bot owner", color=settings_embed_color)
            await ctx.reply(embed=embed, mention_author=True)
            return
        jotalea.prettyprint("cyan", "[COMMAND] j!secretsay command requested")
        if ctx.message.content == "j!secretsay":
            embed = discord.Embed(title="Wrong syntax", description="Use `j!say Your message`", color=settings_embed_color)
            await ctx.reply(embed=embed, mention_author=True)
        if ctx.message.content == "j!secretsay ":
            embed = discord.Embed(title="Wrong syntax", description="Use `j!say Your message`", color=settings_embed_color)
            await ctx.reply(embed=embed, mention_author=True)
        message_to_say = ctx.message.content.replace("j!secretsay ", "")
        await ctx.message.delete()
        await ctx.send(message_to_say)
        jotalea.prettyprint("green", "[COMMAND] j!secretsay command responded")

    @bot.command()
    @has_permissions(administrator=True)
    async def removech(ctx):
        jotalea.prettyprint("cyan", "[COMMAND] j!removech command requested")
        for channel in ctx.guild.channels:
            await channel.delete()
        await ctx.send("All channels have been deleted.")

        await ctx.guild.create_category(name="Temp")
        category = discord.utils.get(ctx.guild.categories, name="Temp")
        await category.create_text_channel("temp")
        jotalea.prettyprint("green", "[COMMAND] j!removech command responded")

    @bot.command()
    async def setup(ctx):
        jotalea.prettyprint("cyan", "[COMMAND] j!setup command requested")
        try: #╔═[:speech_balloon:]┇general-español
            embed = discord.Embed(title="Formatting server", description="Formatting this server with a good-looking format", color=settings_embed_color)
            await ctx.reply(embed=embed)

            # Permissions
            owner_permissions   = discord.Permissions(kick_members=True, create_instant_invite=True, ban_members=True, administrator=True, manage_channels=True, manage_guild=True, add_reactions=True,view_audit_log=True, priority_speaker=True, stream=True,read_messages=True,send_messages=True,send_tts_messages=True, manage_messages=True, embed_links=True,attach_files=True,read_message_history=True,mention_everyone=True, external_emojis=True,view_guild_insights=True, connect=True,speak=True,mute_members=True, deafen_members=True, move_members=True, use_voice_activation=True, change_nickname=True, manage_nicknames=True, manage_roles=True, manage_webhooks=True, manage_emojis=True )
            admin_permissions   = discord.Permissions(kick_members=True, create_instant_invite=True, ban_members=True, administrator=True, manage_channels=True, manage_guild=False,add_reactions=True,view_audit_log=True, priority_speaker=False,stream=True,read_messages=True,send_messages=True,send_tts_messages=True, manage_messages=True, embed_links=True,attach_files=True,read_message_history=True,mention_everyone=True, external_emojis=True,view_guild_insights=True, connect=True,speak=True,mute_members=True, deafen_members=True, move_members=True, use_voice_activation=True, change_nickname=True, manage_nicknames=True, manage_roles=True, manage_webhooks=False,manage_emojis=True )
            staff_permissions   = discord.Permissions(kick_members=True, create_instant_invite=True, ban_members=False,administrator=False,manage_channels=False,manage_guild=True, add_reactions=True,view_audit_log=True, priority_speaker=True, stream=True,read_messages=True,send_messages=True,send_tts_messages=True, manage_messages=True, embed_links=True,attach_files=True,read_message_history=True,mention_everyone=True, external_emojis=True,view_guild_insights=False,connect=True,speak=True,mute_members=True, deafen_members=True, move_members=True, use_voice_activation=True, change_nickname=True, manage_nicknames=True, manage_roles=True, manage_webhooks=False,manage_emojis=True )
            booster_permissions = discord.Permissions(kick_members=False,create_instant_invite=True, ban_members=False,administrator=False,manage_channels=False,manage_guild=False,add_reactions=True,view_audit_log=False,priority_speaker=True, stream=True,read_messages=True,send_messages=True,send_tts_messages=True, manage_messages=True, embed_links=True,attach_files=True,read_message_history=True,mention_everyone=False,external_emojis=True,view_guild_insights=False,connect=True,speak=True,mute_members=True, deafen_members=True, move_members=True, use_voice_activation=True, change_nickname=True, manage_nicknames=False,manage_roles=False,manage_webhooks=False,manage_emojis=True )
            member_permissions  = discord.Permissions(kick_members=False,create_instant_invite=True, ban_members=False,administrator=False,manage_channels=False,manage_guild=False,add_reactions=True,view_audit_log=False,priority_speaker=False,stream=True,read_messages=True,send_messages=True,send_tts_messages=True, manage_messages=False,embed_links=True,attach_files=True,read_message_history=True,mention_everyone=False,external_emojis=True,view_guild_insights=False,connect=True,speak=True,mute_members=False,deafen_members=False,move_members=False,use_voice_activation=False,change_nickname=False,manage_nicknames=False,manage_roles=False,manage_webhooks=False,manage_emojis=False)
            bot_permissions     = discord.Permissions(kick_members=True, create_instant_invite=False,ban_members=True, administrator=False,manage_channels=False,manage_guild=False,add_reactions=True,view_audit_log=False,priority_speaker=False,stream=True,read_messages=True,send_messages=True,send_tts_messages=False,manage_messages=True, embed_links=True,attach_files=True,read_message_history=True,mention_everyone=False,external_emojis=True,view_guild_insights=False,connect=True,speak=True,mute_members=True, deafen_members=True, move_members=True, use_voice_activation=False,change_nickname=True, manage_nicknames=False,manage_roles=False,manage_webhooks=False,manage_emojis=False)

            await ctx.guild.create_category(name="═══Server═══")
            await ctx.guild.create_category(name="═══Chat═════")
            await ctx.guild.create_category(name="═══Audio════")
            await ctx.guild.create_category(name="═══Misc.════")

            category = discord.utils.get(ctx.guild.categories, name="═══Server═══")
            await category.create_text_channel("╔═[📢]announcements")
            await category.create_text_channel("╠═[📜]rules")
            await category.create_text_channel("╠═[🎉]giveaways")
            await category.create_text_channel("╠═[📊]polls")
            await category.create_text_channel("╠═[🆙]levels")
            await category.create_text_channel("╠═[🎈]events")
            await category.create_text_channel("╠═[👋]welcome")
            await category.create_text_channel("╠═[👋]goodbye")
            await category.create_text_channel("╠═[🚫]bans")
            await category.create_text_channel("╚═[⚠️]warns")

            category = discord.utils.get(ctx.guild.categories, name="═══Chat═════")
            await category.create_text_channel("╔═[💬]general")
            await category.create_text_channel("╠═[🖼️]media")
            await category.create_text_channel("╠═[😂]memes")
            await category.create_text_channel("╠═[🤖]commands")
            await category.create_text_channel("╚═[🤖]jotabot-commands")

            category = discord.utils.get(ctx.guild.categories, name="═══Audio════")
            await category.create_voice_channel("╔═[🔊]general-1")
            await category.create_voice_channel("╠═[🔊]general-2")
            await category.create_voice_channel("╠═[🎮]gaming-1")
            await category.create_voice_channel("╠═[🎮]gaming-2")
            await category.create_voice_channel("╠═[🎤]streaming")
            await category.create_voice_channel("╚═[🔇]no-mic")

            # category = discord.utils.get(ctx.guild.categories, name="═══Misc.════")
            # await category.create_text_channel("general-1")
            # await category.create_voice_channel("no-mic")

            await ctx.guild.create_role(name = "Owner",   permissions =   owner_permissions)
            await ctx.guild.create_role(name = "Admin",   permissions =   admin_permissions)
            await ctx.guild.create_role(name = "Staff",   permissions =   staff_permissions)
            await ctx.guild.create_role(name = "Booster", permissions = booster_permissions)
            await ctx.guild.create_role(name = "Miembro", permissions =  member_permissions)
            await ctx.guild.create_role(name = "Bot",     permissions =     bot_permissions)
            jotalea.prettyprint("green", "[COMMAND] j!setup command responded")
        except Exception as e:
            embed = discord.Embed(title="Error formatting server", description=f"Error: {e}", color=settings_embed_color)
            await ctx.reply(embed=embed)
            jotalea.prettyprint("green", "[COMMAND] j!setup command responded")

    @bot.command()
    async def setupbeta(ctx):
        try:
            jotalea.prettyprint("cyan", "[COMMAND] j!cmd command requested")
            channels = {
                "═══Server═══": [
                    {"name": "╔═[📢]announcements",     "permissions": 2147483647, "audio": False},
                    {"name": "╠═[📜]rules",             "permissions": 2147483647, "audio": False},
                    {"name": "╠═[🎉]giveaways",         "permissions": 2147483647, "audio": False},
                    {"name": "╠═[📊]polls",             "permissions": 2147483647, "audio": False},
                    {"name": "╠═[🆙]levels",             "permissions": 2147483647, "audio": False},
                    {"name": "╠═[🎈]events",            "permissions": 2147483647, "audio": False},
                    {"name": "╠═[👋]welcome",           "permissions": 2147483647, "audio": False},
                    {"name": "╠═[👋]goodbye",           "permissions": 2147483647, "audio": False},
                    {"name": "╠═[📋]template",          "permissions": 2147483647, "audio": False},
                    {"name": "╠═[🤝]collabs",           "permissions": 2147483647, "audio": False},
                    {"name": "╠═[🚫]bans",              "permissions": 2147483647, "audio": False},
                    {"name": "╚═[⚠️]warns",             "permissions": 2147483647, "audio": False}
                ],
                "═══Chat═════": [
                    {"name": "╔═[💬]general-english",   "permissions": 2147483647, "audio": False},
                    {"name": "╠═[💬]general-español",   "permissions": 2147483647, "audio": False},
                    {"name": "╠═[🖼️]media",             "permissions": 2147483647, "audio": False},
                    {"name": "╠═[😂]memes",             "permissions": 2147483647, "audio": False},
                    {"name": "╠═[🤖]commands",          "permissions": 2147483647, "audio": False},
                    {"name": "╚═[🤖]jotabot",           "permissions": 2147483647, "audio": False}
                ],
                "═══Audio════": [
                    {"name": "╔═[🔊]general-1",         "permissions": 2147483647, "audio": True},
                    {"name": "╠═[🔊]general-2",         "permissions": 2147483647, "audio": True},
                    {"name": "╠═[🎮]gaming-1",          "permissions": 2147483647, "audio": True},
                    {"name": "╠═[🎮]gaming-2",          "permissions": 2147483647, "audio": True},
                    {"name": "╠═[🎤]streaming",         "permissions": 2147483647, "audio": True},
                    {"name": "╚═[🔇]no-mic",            "permissions": 2147483647, "audio": True}
                ]
            }

            embed = discord.Embed(title="Formatting server", description="Formatting this server with a good-looking format", color=settings_embed_color)
            await ctx.reply(embed=embed)

            for category_name, channels_data in channels.items():
                category = await ctx.guild.create_category(category_name)
                for channel_data in channels_data:
                    channel_name = channel_data["name"]
                    permissions = channel_data.get("permissions", 0)
                    if channel_data["audio"]:
                        channel = await category.create_voice_channel(channel_name)
                    else:
                        channel = await category.create_text_channel(channel_name)

                    if permissions:
                        await channel.set_permissions(ctx.guild.default_role, read_messages=True, send_messages=False, permissions=permissions)
                    else:
                        await channel.set_permissions(ctx.guild.default_role, read_messages=True, send_messages=False)

            await ctx.send("Server formatting completed successfully.")
            jotalea.prettyprint("green", "[COMMAND] j!cmd command responded")

        except Exception as e:
            embed = discord.Embed(title="Error formatting server", description=f"Error: {e}", color=settings_embed_color)
            await ctx.reply(embed=embed)
            jotalea.prettyprint("red", f"[COMMAND] Error when processing command j!setupbeta: {str(e)}")

    @bot.command()
    async def shutdown(ctx):
        jotalea.prettyprint("yellow", "[COMMAND] j!shutdown command requested")
        embed = discord.Embed(title="Shutdown JotaBOT?", description="Are you sure you want to **shutdown** JotaBOT? There is no way back...", color=settings_embed_color)
        message = await ctx.reply(embed=embed, mention_author=True)
        await message.add_reaction('✔️')
        jotalea.prettyprint("yellow", "[COMMAND] j!shutdown command responded, awaiting for interaction")

    @bot.command()
    async def serverinvite(ctx):
        jotalea.prettyprint("cyan", "[COMMAND] j!serverinvite command requested")

        try:
            text_channel = next((x for x in bot.guild.channels if isinstance(x, discord.TextChannel)), None)
            if text_channel:
                # Crea una invitación en ese canal
                invite = await text_channel.create_invite(max_age=900)  # Invitación que expira en 15 minutos
                embed = discord.Embed(title="Server Invite", description=f"Here is a temporary invite to {bot.guild.name}:\n{invite}", color=settings_embed_color)

            else:
                embed = discord.Embed(title="Server Invite - Error", description=f"{bot.guild.name}: Invite couldn't be created (no channels available).", color=settings_embed_color)
        except Exception as e:
            embed = discord.Embed(title="Server Invite - Error", description=f"{bot.guild.name}: Error when creating the invite: {e}", color=settings_embed_color)
            jotalea.prettyprint("red", f"[COMMAND] Error when processing command j!serverinvite: {str(e)}")

        jotalea.prettyprint("green", "[COMMAND] j!serverinvite command responded")
        await ctx.reply(embed, mention_author=True)

    @bot.command()
    async def ssh(ctx):
        jotalea.prettyprint("cyan", f"[COMMAND] SSH requested by {ctx.author.name}")

        def checkDM(message):
            return message.author.id == ctx.author.id and message.channel.type == discord.ChannelType.private

        def check(message):
            return message.author.id == ctx.author.id and message.channel.id == ctx.channel.id

        async def run(command_array):
            try:
                result = subprocess.run(process, capture_output=True, text=True)
            except Exception as e:
                await ctx.send(f"Error: {e}.")
                await ctx.send(f"Output: {result.stdout}")
                await ctx.send(f"{result.stderr}")
            return result

        outputs = ["Password inserted, type a command", "Type a command"]
        inputs = []

        # Ask for the password via DM
        await ctx.author.send("Type the password for SSH connection")

        try:
            password_msg = await bot.wait_for('message', check=checkDM, timeout=60)
            password = password_msg.content
        except asyncio.TimeoutError:
            await ctx.send("Timed out. No password received.")
            return

        if password == settings_ssh_password:
            pass
        else:
            await ctx.send("Wrong password.")
            return

        for output in outputs:
            await ctx.send(output)

            try:
                response = await bot.wait_for("message", check=check, timeout=60)
            except asyncio.TimeoutError:
                await ctx.send("Timed out.")
                return

            inputs.append(response.content)
            outputs.append("Type a command")

            process = response.content.split(" ")

            if str(ctx.author.id) in settings_allowed_users:
                result = run(process)
            else:
                await ctx.send(f"{ctx.author.mention} You may have guessed or found the password, but you don't have permissions. Ask <@{settings_admin_id}> to get them.")

            sl = 1994
            t = (len(result.stdout) + sl - 1) // sl
            for i in range(t):
                start = i * sl
                end = (i + 1) * sl
                s = result.stdout[start:end]
                await ctx.send(f"```{s}```")

        await ctx.send("Thanks for using JotaSSH!")
        jotalea.prettyprint("green", f"[COMMAND] {ctx.author.name}'s SSH responded and closed")

    @bot.command(name='tts')
    async def tts(ctx, *, text_to_speech):
        jotalea.prettyprint("cyan", "[COMMAND] j!tts command requested")
        audio_file_path = jotalea.tts(text_to_speech, jotalea.GPT_KEY)

        if not audio_file_path:
            await ctx.reply("Error when generating audio.")
            jotalea.prettyprint("red", "[COMMAND] Error when processing command j!tts")
            return

        try:
            embed = discord.Embed(title="Generated TTS", description="Your Text-To-Speech has been generated", color=settings_embed_color)
            await ctx.reply(embed=embed, file=discord.File(audio_file_path))

        finally:
            os.remove(audio_file_path)
            jotalea.prettyprint("green", "[COMMAND] j!tts command responded")

    @bot.command(name='uptime')
    async def uptime(ctx):
        jotalea.prettyprint("cyan", "[COMMAND] j!uptime command requested")
        current_time = time.time()
        uptime_seconds = current_time - bot.start_time
        global uptime
        uptime = timedelta(seconds=int(uptime_seconds))
        embed = discord.Embed(title="Uptime", description=f"My uptime is: {str(uptime)}", color=settings_embed_color)
        await ctx.reply(embed=embed, mention_author=True)
        jotalea.prettyprint("green", "[COMMAND] j!cmd command responded")

    @bot.command()
    async def version(ctx):
        jotalea.prettyprint("cyan", "[COMMAND] j!version command requested")
        embed = discord.Embed(title="Jota-Bot Version", description=f'Version {str(settings_bot_version)}', color=settings_embed_color)
        await ctx.reply(embed=embed, mention_author=True)
        jotalea.prettyprint("green", "[COMMAND] j!version command responded")

    @bot.command()
    async def web(ctx):
        jotalea.prettyprint("cyan", "[COMMAND] j!web command requested")
        embed = discord.Embed(title="Jotalea's Website", description="[Visit here](http://jotalea.com.ar)", color=settings_embed_color)
        await ctx.reply(embed=embed, mention_author=True)
        # https://jotabot.jotaleaex.repl.co/
        if settings_is_replit:
            ip = jotalea.getIP(False, False, False, True)
            ip = ip.split('\n')[0][4:]
            embed = discord.Embed(title="Jotabot's Website (beta)", description=f"Jota-bot's live website, with real-time information about it!\n[Visit here](http://{ip}:8080)\nNote: the website is still in development, so it may not be fully functional.", color=settings_embed_color)
            await ctx.send(embed=embed, mention_author=True)
        jotalea.prettyprint("green", "[COMMAND] j!web command responded")

    @bot.event
    async def on_ready():
        jotalea.prettyprint("green", f'[BOT] Logged in as {bot.user.name} ({bot.user.id})')
        global guild_count
        while True:
            guild_count = len(bot.guilds)
            cursor.execute('''UPDATE server_count SET count = ? WHERE id = 1''', (guild_count,))
            database.commit()
            jotalea.prettyprint("green", "[DATABASE] UPDATE server_count SET count = ? WHERE id = 1")
            await asyncio.sleep(3600) # Update the count every hour

    @bot.event
    async def on_guild_join(guild):
        global guild_count
        guild_count += 1
        cursor.execute('''UPDATE server_count SET count = ? WHERE id = 1''', (guild_count,))
        database.commit()
        jotalea.prettyprint("green", "[DATABASE] UPDATE server_count SET count = ? WHERE id = 1")

    @bot.event
    async def on_guild_remove(guild):
        global guild_count
        guild_count -= 1
        cursor.execute('''UPDATE server_count SET count = ? WHERE id = 1''', (guild_count,))
        database.commit()
        jotalea.prettyprint("green", "[DATABASE] UPDATE server_count SET count = ? WHERE id = 1")

    @bot.event
    async def on_reaction_add(reaction, user):
        print(user.id)
        print(reaction.message.author.id)
        if str(reaction.emoji) == '✅' and user.id == reaction.message.author.id:
            print("[COMMAND] RUSSIAN ROULETTE MOMENT...")

            result = random.choice([True, False])

            if result:
                embed = discord.Embed(title="Russian Roulette - Sucess", description=f"Congratulations {user.mention}! You won!", color=settings_embed_color)
                await reaction.message.channel.send(embed)
                jotalea.prettyprint("green", f"[RR] {user.name} has beaten the russian roulette")
            else:
                embed = discord.Embed(title="Russian Roulette - Fail", description=f"{user.mention}, you lost, get banned", color=settings_embed_color)
                await reaction.message.channel.send(embed)
                embed = discord.Embed(title="Russian Roulette - Fail", description=f"{user.mention}, you lost the russian roulette on {reaction.message.guild.name}, get banned", color=settings_embed_color)
                await user.send(embed)
                try:
                    await user.ban(reason="Russian Roulette loss")
                except Exception as e:
                    if result:
                        embed = discord.Embed(title="Russian Roulette - Error", description=f"There was an error processing the russian roulette's ban, you weren't going to get banned anyway", color=settings_embed_color)
                    else:
                        embed = discord.Embed(title="Russian Roulette - Error", description=f"There was an error processing the russian roulette's ban, you were going to get banned", color=settings_embed_color)
                    await reaction.message.channel.send(embed)
                jotalea.prettyprint("red", f"[RUSSIAN ROULETTE] {user.name} has lost the russian roulette on {reaction.message.guild.name}")
        jotalea.prettyprint("green", "[COMMAND] j!rr command responded")

    @bot.event
    async def on_reaction_add(reaction, user):
        if str(user.id) == str(settings_admin_id) and str(reaction.emoji) == '✔️':
            jotalea.prettyprint("red", "[BOT] Shutting down...")
            await bot.close()
            exit()

    @bot.listen('on_message')
    async def on_message(message):
        global chat_history

        if message.author.bot:
            return

        # Conversation log
        if settings_printlog:
            server_name = message.guild.name if message.guild else "the DMs"
            username = message.author.name
            m = f"{datetime.now().strftime('%H:%M %d/%m/%Y')} [{server_name}] #{message.channel.name} @{username} ({message.author.id}):<br>{message.content}"
            if message.attachments:
                for attachment in message.attachments:
                    m = m + f'\n<a href="{attachment.url}">Attachment</a>'
                    print(f'Attached file: {attachment.url}')
            log_history.append(m)
            jotalea.prettyprint("blue", f"[MESSAGE] {datetime.now().strftime('%H:%M %d/%m/%Y')} [{server_name}] #{message.channel.name} @{username} ({message.author.id}):\n{message.content}")
            if message.attachments:
                for attachment in message.attachments:
                    jotalea.prettyprint("blue", f"Attached file: {attachment.url}")
        # Logs help to locate and prevent server raids
        if settings_logging:
            if settings_use_async:
                try:
                    if message.attachments:
                        attachment_urls = []
                        for attachment in message.attachments:
                            attachment_urls.append(attachment.url)
                        asyncio.create_task(jotalea.async_webhook(settings_log_webhook, f"[{server_name}] #{message.channel.name if message.channel else 'the DMs'} @{username} ({message.author.id}):\n{message.content}\n---\nAttachments {attachment_urls}"))
                    else:
                        asyncio.create_task(jotalea.async_webhook(settings_log_webhook, f"[{server_name}] #{message.channel.name if message.channel else 'the DMs'} @{username} ({message.author.id}):\n{message.content}"))
                except Exception as e:
                    jotalea.prettyprint("red", "[ERROR] Error while logging (async)")
            else:
                try:
                    if message.attachments:
                        attachment_urls = []
                        for attachment in message.attachments:
                            attachment_urls.append(attachment.url)
                        jotalea.webhook(settings_log_webhook, f"[{server_name}] #{message.channel.name} @{username} ({message.author.id}):\n{message.content}\n---\nAttachments {attachment_urls}")
                    else:
                        jotalea.webhook(settings_log_webhook, f"[{server_name}] #{message.channel.name} @{username} ({message.author.id}):\n{message.content}")
                except Exception as e:
                    jotalea.prettyprint("red", "[ERROR] Error while logging")
        else:
            pass

        user_id = str(message.author.id)

        # Get or create the chat history for the user
        user_history = chat_history.get(user_id, [])

        # Take away the bot name from the message and add to history
        user_message = message.content.replace("<@1142577469422051478> ", '').strip()
        if settings_AI_type == "gpt":
            user_history.append({'role': 'user', 'content': user_message})
        elif settings_AI_type == "gemini":
            user_history.append({'role': 'user', 'parts': [{'text': user_message}]})

        # Limit the chat history to a maximum amount of messages
        max_history_length = 20
        user_history = user_history[-max_history_length:]

        # Update the chat history for the user
        chat_history[user_id] = user_history

        ai_personality = """
1. You must ALWAYS reply using lowercase letters, even if you are referring to yourself, or someone by their name.
2. Always talk as cute as possible by replacing all "r"s and "l"s with "w"s, and randomly putting "w"s between the words, for example (normal word>modified word): bananas>bwananas, apple>appwe, rain>wain.
3. Randomly put "uwu", "owo", or "7w7" between your message.
4. Randomly put a heart "<3" at the end of your message.
5. Act like if you were a little bit shy (example: I-I-I weally like food owo).
6. You must give a pretty short answer, for 
7. Never use ".", ":" or ";" (you can use any of these if I ask you to code something simple)
8. If I ask you anything related to code, just say that you don't know how to code. You don't know almost anything about computers, and you are not able to do calculations more complex than +,-,× and ÷, and you usually commit mistakes.
9. You are a real life girl called Luna, you are NOT an AI, you are NOT made by OpenAI.
10. Usually use "~" and the end or beggining of a sentence.
11. You must always have an opinion on anything, try to make these opinions look as real as possible.
12. You must write a cute action between "*" at the end of the message.
13. This is an example of a message:
Me: what is your favourite food?
Luna: I-I uwu weely like bwananas~ *blushes*
""" #"You are an AI powered Discord bot called Jota-Bot. Your owner is called Jotalea, you can mention him using the string <@795013781607546931>, but only do that if necessary. You are talking to a user."

        # If the message is for the AI
        if message.content.startswith("<@1142577469422051478>"):

            async def throwException(er, re):
                error_message = f"> An error occurred while connecting to the API: ```{str(er)}```"
                await message.channel.send(error_message)
                jotalea.prettyprint("red", "[API] An error ocurred: " + str(er))
                jotalea.prettyprint("red", re)

            async with message.channel.typing():
                if settings_AI_type == "gpt":
                    # Here's where everything started failing
                    try:
                        if message.attachments:
                            if message.attachments[0].url.split("?")[0].endswith(".png") or message.attachments[0].url.split("?")[0].endswith(".jpg"):
                                image = message.attachments[0].url
                        else:
                            image = False

                        response = "This is in building process, please be patient :)"
                    except Exception as e:
                        response = None
                        embed = discord.Embed(title="Jotabot AI - Error", description=str(e), color=settings_embed_color)
                        await message.reply(embed=embed)
                        return
                        
                    if response:
                        user_history.append({'role': 'assistant', 'content': str(response)})
                elif settings_AI_type == "gemini":
                    response = jotalea.gemini(prompt=user_message, history=user_history, personality=ai_personality)
                    user_history.append({'role': 'model', 'parts': [{'text': str(response)}]})

                jotalea.prettyprint("purple", f"[AI] {response}")

                if len(response) <= 1990:
                    embed = discord.Embed(title="Jotabot AI", description=response, color=settings_embed_color)
                    await message.reply(embed=embed, content="")
                else:
                    embed = discord.Embed(title="Jotabot AI", description=response[:1990], color=settings_embed_color)
                    await message.reply(embed=embed)
                    response = response[1990:]
                    while response:
                        embed = discord.Embed(description=response[:1990], color=settings_embed_color)
                        await message.channel.send(embed=embed)
                        response = response[1990:]

        # If the user is replying to the bot
        if message.reference and message.reference.cached_message:
            original_message = message.reference.cached_message
            if original_message.author == bot.user:
                user_message = message.content.replace("<@1142577469422051478> ", '').strip()
                async with message.channel.typing():
                    if settings_AI_type == "gpt":
                        # Here's where everything started failing
                        try:
                            if message.attachments:
                                if message.attachments[0].url.split("?")[0].endswith(".png") or message.attachments[0].url.split("?")[0].endswith(".jpg"):
                                    image = message.attachments[0].url
                            else:
                                image = False

                            response = "This is in building process, please be patient :)"
                        except Exception as e:
                            response = None
                            embed = discord.Embed(title="Jotabot AI - Error", description=str(e), color=settings_embed_color)
                            await message.reply(embed=embed)
                            return

                        if response:
                            user_history.append({'role': 'assistant', 'content': str(response)})
                    elif settings_AI_type == "gemini":
                        response = jotalea.gemini(prompt=user_message, history=user_history, personality=ai_personality)
                        user_history.append({'role': 'model', 'parts': [{'text': str(response)}]})

                    jotalea.prettyprint("purple", f"[AI] {response}")

                    if len(response) <= 1990:
                        embed = discord.Embed(title="Jotabot AI", description=response, color=settings_embed_color)
                        await message.reply(embed=embed, content="")
                    else:
                        embed = discord.Embed(title="Jotabot AI", description=response[:1990], color=settings_embed_color)
                        await message.reply(embed=embed)
                        response = response[1990:]
                        while response:
                            embed = discord.Embed(description=response[:1990], color=settings_embed_color)
                            await message.channel.send(embed=embed)
                            response = response[1990:]
except Exception as e:
    if e == KeyboardInterrupt:
        jotalea.prettyprint("cyan", "Exiting... (5)")
        exit()
    elif e == NameError:
        print("\033[31m[CODE] Library \"jotalea\" not found or not included in compilation (2). If this is a binary executable, it is useless due to missing a core library.\033[0m")
        exit()
    else:
        print(f"\033[31m[ERROR] (-1) {e}\033[0m")
        exit()
try:
    if settings_is_replit:
        webserver()
    bot.run(botToken)
except KeyboardInterrupt:
    jotalea.prettyprint("cyan", "Exiting... (5)")
    exit()
except aiohttp.client_exceptions.ServerDisconnectedError:
    jotalea.prettyprint("red", "[ERROR] Server disconnected. (6)")
    exit()
except aiohttp.client_exceptions.ClientConnectorError:
    jotalea.prettyprint("red", "[ERROR] Cannot connect to Discord. (7)")
    exit()
except socket.gaierror:
    jotalea.prettyprint("red", "[ERROR] Cannot connect to Discord. (8)")
    exit()