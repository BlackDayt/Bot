import discord
import config


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_raw_reaction_add(self, payload):
        if payload.message_id == config.ID_POST:
            channel = self.get_channel(payload.channel_id)  # получаем объект канала
            message = await channel.fetch_message(payload.message_id)  # получаем объект сообщения
            member = discord.utils.get(message.guild.members, id=payload.user_id)  # получаем объект пользователя
            print(payload.channel_id, payload.message_id, message.guild.members, payload.user_id)
            try:
                emoji = str(payload.emoji)  # эмоджи который выбрал юзер
                role = discord.utils.get(message.guild.roles, id=config.ROLES[emoji])  # объект выбранной роли (если есть)
                await member.add_roles(role)
                print('[SUCCESS] User {0.display_name} has been granted with role {1.name}'.format(member, role))

            except KeyError as e:
                print('[ERROR] KeyError, no role found for ' + str(payload.emoji))
            except Exception as e:
                print(repr(e))

    async def on_raw_reaction_remove(self, payload):
        channel = self.get_channel(payload.channel_id)  # получаем объект канала
        message = await channel.fetch_message(payload.message_id)  # получаем объект сообщения
        member = discord.utils.get(message.guild.members, id=payload.user_id)  # получаем объект пользователя

        try:
            emoji = str(payload.emoji)  # эмоджик который выбрал юзер
            role = discord.utils.get(message.guild.roles, id=config.ROLES[emoji])  # объект выбранной роли
            await member.remove_roles(role)
            print('[SUCCESS] Role {1.name} has been remove for user {0.display_name}'.format(member, role))

        except KeyError as e:
            print('[ERROR] KeyError, no role found for ' + str(payload.emoji))
        except Exception as e:
            print(repr(e))


# RUN
client = MyClient(intents=discord.Intents.all())
client.run(config.TOKEN)