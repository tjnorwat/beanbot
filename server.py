#!/usr/bin/env python
import datetime
import requests
import discord
import asyncio
import random
import json
import time
import os
from discord.ext.commands import Bot
from discord.ext import commands
from discord.utils import get

Client = discord.Client() #makes client
client = commands.Bot(command_prefix = ";")
ID_CHANNEL_BOTUSAGE = '461035453399695360'
ID_CHANNEL_BEANS = '461398242525970442'
ID_USER_BEANBOT = '461372954203127808'
ID_ROLE_BEANBOI = '463189878830530560'
ID_ROLE_ADMIN = '461220684983566347'
ID_ROLE_MOD = '461029196647497747'
PATH = ''
rng = random.SystemRandom()

@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name='with beans'))
    print("Bot Online!")
    images()

@client.event
async def on_message(message):

    if str(message.channel) == 'set-roles':
        #got the roles by doing \@Administrator and \@Moderator
        #get a list of roles that the user is in
        #if user is not admin or mod then delete
        if ID_ROLE_ADMIN not in [role.id for role in message.author.roles] and ID_ROLE_MOD not in [role.id for role in message.author.roles]: 
           await client.delete_message(message)
            
    # !private voice command
    elif message.content.lower().startswith('!privatevoice'):
        if str(message.channel) == 'bot-usage': # bot usage channel
            await client.delete_message(message)
            await client.send_file(discord.Object(id= ID_CHANNEL_BOTUSAGE), PATH + "PersonalSpaces/SS2Artboard14.png") #sends file
            await client.send_message(discord.Object(id = ID_CHANNEL_BOTUSAGE), "*Requested by <@" + message.author.id + ">*\n\nHow to create your own private voice channels\nc! summon - create your channel (will be removed after 30 seconds of inactivity)\nc! unlock/lock - open or close your server to the public\nc! add @someone - allow someone to enter your private room\nc! block @someone - block someone from entering your public room") #sends all text

    # Bean command
    elif message.content.lower().find('bean') != -1: # switched this to just be "bean" because "beans" has bean
        if(message.author.id != ID_USER_BEANBOT):
            # please do continue, you are not bean boy
            
            if ID_ROLE_BEANBOI not in [role.id for role in message.author.roles]: # checks to see if user has been placed in "bean boi" role
                role = discord.utils.get(message.server.roles, name = "bean boi")
                await client.add_roles(message.author, role) # if not, place them in it
                await client.send_message(message.channel, "<@" + message.author.id + "> has been successfully added to the \"Bean Boi\" role! please check <#" + ID_CHANNEL_BEANS + ">\nUse \";add <uploaded image/image url>\" to add images to beanbot!" )
                

            if str(message.channel) != 'literally-just-beans':
                await client.send_message(message.channel, "There's a little something something in <#" + ID_CHANNEL_BEANS + "> for <@" + message.author.id + ">...")

            await client.send_message(discord.Object(id= ID_CHANNEL_BEANS), 'I heard <@' + message.author.id + '> likes beans...') #sends message to user who activated keyword
            num_of_files = len(os.listdir(PATH + "BeanImages")) - 1
            num = str(rng.randint(0,num_of_files)) #gets random number between 0 and num of files
            try: #tries to send png image
                await client.send_file(discord.Object(id= ID_CHANNEL_BEANS), PATH + 'BeanImages/' + num + '.png') #sends files to channel
            except FileNotFoundError:
                try:
                    await client.send_file(discord.Object(id= ID_CHANNEL_BEANS), PATH + 'BeanImages/' + num + '.gif')
                except FileNotFoundError:
                    try:
                        await client.send_file(discord.Object(id= ID_CHANNEL_BEANS), PATH + 'BeanImages/' + num + '.jpg')
                    except FileNotFoundError as e:
                        print("Image not working: " + num)
                        print("#############ERROR STARTS HERE############")
                        print(e)
        
    # ;add command
    elif message.content.startswith(';add'):
        
        url = message.content[4:] # gets input after ;add
        try:
            url = message.attachments[0]['url'] #tries to get uploaded image
        except IndexError:
            pass # if none is found, dont do anything

        if url[-4:] == '.jpg' or url[-4:] == 'jpeg': #checks for jpg 
            await addImage(message, url, '.jpg')
        elif url[-4:] == '.png': # checks for png
            await addImage(message, url, '.png')
        elif url[-4:] == '.gif':
            await addImage(message, url, '.gif')
        else:
            await client.send_message(message.channel,"That is not a jpg, png, or gif image!")
        

def images():
    num_of_files = len(os.listdir(PATH + "BeanImages"))
    print("Number of BeanImages: ", num_of_files)
  
async def addImage(message, url, ext):
    r = requests.get(url, allow_redirects=True) #gets image url
    num_of_files = len(os.listdir(PATH + "BeanImages")) #gets the number of files in folder
    filename = str(num_of_files) + ext 
    open(filename,'wb').write(r.content) # saves image to directory that script is in
    os.rename(PATH + filename, PATH + "BeanImages/" + filename) # moves image to this folder
    print("new image was added")
    images()
    await client.send_message(discord.Object(id= ID_CHANNEL_BEANS), "<@" + message.author.id + "> has successfully added a new " + ext + " image, totalling at " + str(num_of_files + 1) + " beans!")
    

if __name__ == "__main__":
    with open("config.json") as config_file:
        config = json.load(config_file)
        client.run(config)
