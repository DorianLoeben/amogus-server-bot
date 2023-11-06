import os
import nextcord
from nextcord.ext import commands

import amogus_server_bot.server_data as server_data


def check_if_it_is_me(interaction: nextcord.Interaction):
    return interaction.user.id == int(os.getenv("ADMIN_USER"))


message_text = (
    "Möchtest du Pings für AMOGUS? Klicke auf die Reaktionen!\n"
    + ":red_circle: - Wenn wir Anfangen wollen\n"
    + ":yellow_circle: - Für Polls\n"
)


class Rolebot(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(
        description="(Re-)Initializes the Rolebot",
        guild_ids=[int(os.getenv("GUILD_ID"))],
    )
    async def init(self, interaction: nextcord.Interaction):
        if not check_if_it_is_me(interaction):
            await interaction.response.send_message(
                "Du bist nicht der Admin!", ephemeral=True
            )
            return
        await interaction.response.send_message("Initializing Rolebot...")
        if old_message_id := server_data.get_field_from_guild(
            interaction.guild_id, "rolebot_message_id"
        ):
            # Already initialized. Delete Old Rolebot message
            old_message = await interaction.channel.fetch_message(old_message_id)
            await old_message.delete()
        # Create new Rolebot message
        message = await interaction.channel.send(message_text)
        # Add reactions to message
        await message.add_reaction("🔴")
        await message.add_reaction("🟡")
        # Save message id to server_data
        server_data.set_field_for_guild(
            interaction.guild_id, "rolebot_message_id", message.id
        )
        # Delete slash command interaction
        await interaction.delete_original_message()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: nextcord.RawReactionActionEvent):
        if payload.member.bot:
            return
        if payload.message_id != server_data.get_field_from_guild(
            payload.guild_id, "rolebot_message_id"
        ):
            return
        # Add role to user if role is not already assigned
        guild = self.bot.get_guild(payload.guild_id)
        role_ping = nextcord.utils.get(guild.roles, name="Amogus")
        role_poll = nextcord.utils.get(guild.roles, name="Poll")

        # Check if Role existed. If not, create it
        if not role_ping:
            role_ping = await guild.create_role(name="Amogus")
        if not role_poll:
            role_poll = await guild.create_role(name="Poll")

        if payload.emoji.name == "🔴":
            if role_ping not in payload.member.roles:
                await payload.member.add_roles(role_ping)
            else:
                await payload.member.remove_roles(role_ping)
        elif payload.emoji.name == "🟡":
            if role_poll not in payload.member.roles:
                await payload.member.add_roles(role_poll)
            else:
                await payload.member.remove_roles(role_poll)
        # Delete reaction from message
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        if message.system_content != message_text:
            await message.edit(content=message_text)
        await message.remove_reaction(payload.emoji, payload.member)
