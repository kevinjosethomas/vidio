const moment = require("moment");
const { MessageEmbed } = require("discord.js");
const { SlashCommandBuilder } = require("@discordjs/builders");

const { red } = require.main.require("./data/config");

const data = new SlashCommandBuilder()
  .setName("stats")
  .setDescription("Provides in-depth statistics about the bot");

const execute = async (interaction) => {
  const guilds = interaction.client.guilds.cache.size;
  const users = interaction.client.users.cache.size;

  const duration = moment.duration(moment().diff(interaction.client.startup)).humanize();
  const since = interaction.client.startup.calendar();

  const memory = Math.round(process.memoryUsage().heapUsed / 1024 / 1024);
  const latency = interaction.client.ws.ping;

  const embed = new MessageEmbed()
    .setDescription(
      `
  vidio is in -
  • **${guilds}** servers
  • with **${users}** users

  vidio has been online for -
  • **${duration}**
  • since **${since}**

  vidio is using -
  • **${memory}mb** of RAM
  with a response time of **${latency}ms**

  [More Stats](https://statcord.com/bot/689210550680682560)
  `
    )
    .setColor(red);
  await interaction.reply({ embeds: [embed] });
};

module.exports = {
  data: data,
  execute: execute,
};
