const { MessageEmbed } = require("discord.js");
const { SlashCommandBuilder } = require("@discordjs/builders");

const { red } = require.main.require("./data/config");
const { ping } = require.main.require("./data/emojis");

const data = new SlashCommandBuilder()
  .setName("ping")
  .setDescription("Returns the bot's latency to Discord's API");

const execute = async (interaction) => {
  const embed = new MessageEmbed()
    .setDescription(`${ping} Pong! \`\`${interaction.client.ws.ping}ms\`\``)
    .setColor(red);
  await interaction.reply({ embeds: [embed] });
};

module.exports = {
  data: data,
  execute: execute,
};
