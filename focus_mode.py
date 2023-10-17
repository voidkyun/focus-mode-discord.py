import discord
from discord import app_commands
import asyncio
import datetime

TOKEN = 'Your token here'
intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

class FocusFor(discord.ui.View):
	h=0
	m=0
	canceled=False
	@discord.ui.select(placeholder='hour',options=[discord.SelectOption(label=f'{i}',value=i) for i in range(11)])
	async def hrselect(self,ctx,select):
		self.h=select.values[0]
		await ctx.response.edit_message(content=f'Focus for\n## **{self.h:>02}**h**{self.m:>02}**m')
	@discord.ui.select(placeholder='minute',options=[discord.SelectOption(label=f'{i}',value=i) for i in range(0,60,10)])
	async def minselect(self,ctx,select):
		self.m=select.values[0]
		await ctx.response.edit_message(content=f'Focus for\n## **{self.h:>02}**h**{self.m:>02}**m')
	@discord.ui.button(label="start", style=discord.ButtonStyle.green)
	async def submit(self, interaction:discord.Integration, button:discord.ui.Button):
		button.disabled=True
		self.hrselect.disabled=True
		self.minselect.disabled=True
		await interaction.response.edit_message(view=self)
		message=await interaction.followup.send(content=f"Let's focus for {self.h:>02}h{self.m:>02}m!")
		for i in range(3,-1,-1):
			await asyncio.sleep(1)
			if i>0:
				edited_message=f"Let's focus for {self.h:>02}h{self.m:>02}m!\n## {i}"
				await interaction.followup.edit_message(message_id=message.id, content=edited_message)
				filename='countdown.mp3'
			else:
				await interaction.followup.send(content='start')
				filename='mute.mp3'
#			await play(interaction,filename)
		channel=interaction.user.voice.channel
		for member in channel.members:
			if not member.bot:
				await member.edit(mute=True)
		dt_start=datetime.datetime.now()
		td=datetime.datetime.now()-dt_start
		while(td<datetime.timedelta(hours=int(self.h),minutes=int(self.m))):
			td=datetime.datetime.now()-dt_start
			await asyncio.sleep(1)
		for member in channel.members:
			if not member.bot:
				await member.edit(mute=False)
#		await play(interaction,'unmute.mp3')
		fc_channel=interaction.message.channel
		await fc_channel.send(content='end')

@tree.command(
		name='recovery',
		description='Unmute yourself.'
)
async def recovery(ctx:discord.Interaction):
	await ctx.response.send_message(content='Recovered!',ephemeral=True)
	try:
		user=ctx.user
		await user.edit(mute=False)
	except:
		pass
@tree.command(
	name="fc",
	description="Focus for a specified time."
)
async def fc(ctx:discord.Interaction):
	if ctx.user.voice!=None:
		focusfor=FocusFor()
		await ctx.response.send_message(content='Focus for\n## **00**h**00**m',view=focusfor)
	else:
		await ctx.response.send_message(content='Not in a vc!',ephemeral=True)

@client.event
async def on_ready():
	print('Succesfully logined')
	await tree.sync()

@client.event
async def on_message(message):
	pass
@client.event
async def on_member_join(member):
	if member.bot :
		pass

client.run(TOKEN)