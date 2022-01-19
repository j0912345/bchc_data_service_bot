import discord
from discord import guild
from discord.ext import commands
from discord.commands import Option
from discord.ui import button, View
import time
import logging
import editor_functions_cs
import os
import asyncio
logging.basicConfig(level=logging.INFO)
    

#setup values
prefix="ds: "
bot_nickname = "(!save hacking bot!)"
working_server_ids=[898279702677037117]
bot_owner_id=587040662915121155
dir_of_bot = r"I:\coding\python\discord-bots\temp_save_dir\\"
with open("recover_from_crash.txt", "r") as bot_settings_1: #reads token from file
    token=bot_settings_1.read(59)


client = commands.Bot(command_prefix=prefix, activity=discord.Game(name='with your save'))
#client = discord.client(activity=discord.Game(name='with your save'))#makes "playing with your save file" as the status
non_en_editor_support_warning="**WARNING!!!**\nfiery henry's save editor doesn't work well with saves that aren't en. please back up your save now in case something goes wrong."
game_location=""
time_to_wait_before_timeout = 30

#                                           ==== buttons ====

@client.slash_command(guild_ids=working_server_ids)
async def help_hack(ctx):
    """help for the \"hack\" command"""
    await ctx.respond("the \"hack\" command uses comma separated values for the option numbers and the attached save file as the file to hack.")


class continue_button(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="continue", style=discord.ButtonStyle.gray)
    async def continue_button(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        await interaction.response.send_message("please upload your save")
        self.stop()

#                                       ==== save location buttons ====
##class save_location(discord.ui.View):
##    def __init__(self):
##        super().__init__()
##        self.value = None
##
##
##    @discord.ui.button(label="en", style=discord.ButtonStyle.gray)
##    async def is_en(
##        self, button: discord.ui.Button, interaction: discord.Interaction
##    ):
##        view = continue_button()
##        await interaction.response.send_message("please back up your save now in case something goes wrong. press continue when you save is backed up", view=view)
##        global game_location
##        game_location = "en"
##        self.stop()
##        
##
##    @discord.ui.button(label="jp", style=discord.ButtonStyle.gray)
##    async def is_jp(
##        self, button: discord.ui.Button, interaction: discord.Interaction
##    ):
##        view = continue_button()
##        await interaction.response.send_message(non_en_editor_support_warning+"\npress continue when you save is backed up", view=view)
##        global game_location
##        game_location = "jp"
##        self.stop()
##
##    @discord.ui.button(label="kr", style=discord.ButtonStyle.gray)
##    async def is_kr(
##        self, button: discord.ui.Button, interaction: discord.Interaction
##    ):
##        view = continue_button()
##        await interaction.response.send_message(non_en_editor_support_warning+"\npress continue when you save is backed up", view=view)
##        global game_location
##        game_location = "kr"
##        self.stop()
##
##    @discord.ui.button(label="tw", style=discord.ButtonStyle.gray)
##    async def is_tw(
##        self, button: discord.ui.Button, interaction: discord.Interaction
##    ):
##        view = continue_button()
##        await interaction.response.send_message(non_en_editor_support_warning+"\npress continue when you save is backed up", view=view)
##        global game_location
##        game_location = "tw"
##        self.stop()



@client.event
async def on_ready():
    print(f'logged in to \"{client.user}\"')

def decode_csv_to_list(input_csv):
    output_list = []
    letter = ""
    letter_num = 0
    temp_part_read_csv = ""
    for ___letter___ in range(0, len(input_csv)):
        letter = input_csv[letter_num]
        letter_num = letter_num + 1
        if letter != ",":
            temp_part_read_csv += letter
        else:
            output_list.append(temp_part_read_csv)
            temp_part_read_csv = ""
    output_list.append(temp_part_read_csv)
    return(output_list)
    

debug_mode = 0
##@client.event
##async def on_message_delete(message):
#        deleted_message_amount
##    if message.author == client.user:
##        return
##
##    if debug_mode == 1 and message.author.id == bot_owner_id:
##        embed_var = discord.Embed(colour=discord.Colour.from_rgb(100, 100, 100), title=f"message deleted by {message.author}:")
##        embed_var.add_field(name="message:", value=f"{message.content}")
##        if message.attachments != []:
##            embed_var.add_field(name="note:", value=f"this message had attachment(s).\n\nclass data from the attachment(s):\n\n{message.attachments[:]}", inline=False)
##        await message.channel.send(embed=embed_var)


#debug_mode = 1
@client.event
async def on_message(message):
    if message.author == client.user:
        return
#                                          ==== commands ====
    else:
        if message.content.startswith(prefix+"reset nick") and client.get_guild(857886691938795541).get_member(client.application_id).nick != bot_nickname:
            TEMP_BOT_NICK_DAT = client.get_guild(857886691938795541).get_member(client.application_id)
            print("\nold nickname: "+TEMP_BOT_NICK_DAT.nick)
            await TEMP_BOT_NICK_DAT.edit(nick = bot_nickname)
            print("new nickname: "+client.get_guild(857886691938795541).get_member(client.application_id).nick+"\n")
            await message.channel.send("nickname for bchc has been reset to: "+client.get_guild(857886691938795541).get_member(client.application_id).nick)
        
        elif debug_mode == 1 and message.author != await client.fetch_user(bot_owner_id) and message.content.startswith(prefix):
            await message.channel.send("the bot has been disabled for bug fixes.")
            return

        elif message.content.startswith(prefix+"off"):
            if message.author.id == bot_owner_id:
                print("shuting off the bot")
                await message.channel.send("turning off...")
                await client.close()

#(note from past: if something doesn't work, try adding a "after" or "before" prefix.)
# how to use the audit log:
##        elif message.author.id == bot_owner_id and message.content.startswith(prefix+"audit"):
##            print("getting log...")
##            with open("audit_log.txt", "wb") as log_file:
##                async for entry in client.get_guild(857886691938795541).audit_logs(limit=100):
##                    log_file.write(bytes(f'{entry.user} did {entry.action} to {entry.target} because: {entry.reason} | extra: {entry.extra}\nfull data={entry}'+"\n\n\n", "utf-16"))
##            print("done!")
                    
        elif message.content.startswith(prefix+"ping"):
            await message.channel.send("pong")

        elif message.content.startswith(prefix+"help"):
            embed_var = discord.Embed(colour=discord.Colour.from_rgb(100, 100, 100), title="data service bot help")
            embed_var.add_field(name="cmd list:", value=f"1: \"{prefix}ping\", to make sure that the bot didn't die. should return \"pong\".\n\n2: \"{prefix}hack\", used for hacking your save. you need to attach your save file in the same message that this command is used. because you need to upload your save in chat(until the save transfer system gets cracked by {await client.fetch_user(bot_owner_id)}), you probably want to use this command in DMs.\n\nnote: if your save gets banned, {await client.fetch_user(bot_owner_id)} and {client.user} are NOT responsible.", inline=False)
            embed_var.add_field(name="hack command help (part 1):", value=f"when you use \"{prefix}at\", i ask you for a list of hacks in a csv(comma separated values) format. this is how to make one of these lists:\n\nthe first item of the csv list is the game language version code (en, jp, tw, etc...).\nafter that, there is the option numbers (see the list of input numbers). if an option number says \"takes one input\", that means it will use the next item in the csv list as the input.\nthe last item in the list is always \"end\". ")
            embed_var.add_field(name="list of input numbers (part 2):", value="1: catfood. takes one input. uses the input as what to set the catfood to. you probably want to stay under 45000 or 20000 to be safe.\n\n2: xp. takes one input. uses the input as what to set the xp to. you probably want to stay under 99999999 xp.", inline=True)
            embed_var.add_field(name="examples of lists of hacks for an en save (part 3):", value="this is how you set the catfood to 500:\nen,1,500,end\n\nset the xp to 600 and catfood to 800:\nen,2,600,1,800,end\n\nor you could use:\nen,1,800,2,600,end\n\nset the xp to 900:\nen,2,900,end", inline=False)
            await message.channel.send(embed=embed_var)
            
##        elif message.content.startswith(prefix+"t1"):
##            view = save_location()
##            await message.channel.send("what language is your save file?", view=view)

        elif message.content.startswith(prefix+"hack"):
            if message.attachments != []:

                author = message.author.id
#                author_username = await client.fetch_user(author)
                attachment = message.attachments[0]
                user_save_name = f"{attachment.filename}"
                temp_save_filename = f"{user_save_name}_at_"+str(round(time.time()))+"_by_"+str(author)
                await attachment.save("temp_save_dir/"+temp_save_filename)
                print("\ndownloaded a save file: "+temp_save_filename)
                help_hack_message = f"please reply to this message with a list of hacks in a csv format. use \"{prefix} help\" for examples of these lists + how to make one."
                await message.channel.send(help_hack_message)
                def check_for_reply(m):
##                    print(m.content != None)
##                    print(message.author != client.user)
##                    print("\n== new message check ==")
##                    print(m.author.id)
##                    print(author)
##                    print(client.user)
##                    print(m.content)
##                    print("")
                    return m.content != None and m.content != help_hack_message and message.author != client.user and m.author.id == author

                try:
                    list_of_hacks_message = await client.wait_for("message", check=check_for_reply, timeout=time_to_wait_before_timeout)
                except asyncio.TimeoutError:
                    await message.channel.send("timeout error, please try again when your list of hacks is ready.")
                    return
                else:
                    hack_list = decode_csv_to_list(list_of_hacks_message.content)
#                    await message.channel.send(hack_list)#"👍")
                    game_language = hack_list[0]
#                    await message.channel.send(game_language)

                    done_hacking = False


                    #i couldn't use i in a function, it just wouldn't work
                    i = 0
                    temp_user_save_dir = dir_of_bot+temp_save_filename
                    try:
                        while done_hacking == False:
                            i = i + 1
    ##                        print("loop"+str(i))
    ##                        print(hack_list)
                            if hack_list[i] != "end":
                                match hack_list[i]:
                                    case "1":
                                        i = i + 1
                                        editor_functions_cs.edit_catfood(temp_user_save_dir, int(hack_list[i]))
                                    case "2":
                                        i = i + 1
                                        editor_functions_cs.edit_xp(temp_user_save_dir, int(hack_list[i]))
                                    case _:
                                        await message.channel.send("error, your list of hacks has an option number that doesn't exist!")
                                        os.remove(temp_user_save_dir)
                                        return
                            else:
                                done_hacking = True
                        await message.channel.send("here is your hacked save!", file=discord.File(temp_user_save_dir, "hacked_"+user_save_name))

                    except IndexError:
                        await message.channel.send("error, it looks like your list of hacks don't have \"end\" at the end!")
                    os.remove(temp_user_save_dir)
                    print(f"\nsave was hacked. person who started the hack dialog: {author} | save edit options: {hack_list} | time of save hack: {time.time()}")
            #if there is no attachments:
            else:
                await message.channel.send("error, no save file attached")
                    
                    

client.run(token)
print("bot was shut down")

