from discord.ext import commands
import discord
from tinydb import TinyDB, Query

intents = discord.Intents.all()


thank_points = TinyDB('bot_db.json')
User = Query()
bot = commands.Bot(command_prefix="!",intents = intents)


def run():
    @bot.event
    
                
    async def on_ready():
        print(thank_points.all())

    @bot.command()
    async def thanks(ctx, mention):
        await ctx.send("{} has been thanked".format(mention))
        print(mention)
        #print(ctx.author.id)
        await ctx.send("{} is the user".format(mention))

        if not thank_points.contains(User['id']==mention):
            thank_points.insert({'id':mention,'points':1})
        else:
            [result] = thank_points.search(User['id']==mention)
            thank_points.update({'points':(result['points']+1)},User['id']==mention)

        print(thank_points.all())

    @bot.command()
    async def thank_leaderboard(ctx):
        # Creating an embed object
        embed = discord.Embed(
            title="Leaderboard",
            description="This is the description of the embed.",
            color=discord.Color.blue()  # You can customize the color of the embed
        )
        #embed.set_author(name="Author Name", icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url="https://t3.ftcdn.net/jpg/00/92/53/56/360_F_92535664_IvFsQeHjBzfE6sD4VHdO8u5OHUSc6yHF.jpg")  #URL of the thumbnail image

        for item in sorted(thank_points.all(),key=lambda x: x['points'],reverse = True):
            user_id = item['id']
            user = await bot.fetch_user(int(user_id.strip("<@!>")))

            embed.add_field(name=user.name, value=item['points'], inline=False)
        #sort in increasing order
        # Sending the embed
        await ctx.send(embed=embed)

    bot.run('MTEzMzM1NDE4Mjk3MjI4NTAyOQ.GZ3J4b.zFTMptJ5c9z053aPT9uGr4h2iqumg67cpRKB3U')

run()