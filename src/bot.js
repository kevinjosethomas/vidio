const fs = require("fs");
const path = require("path");
const dotenv = require("dotenv");
const moment = require("moment");
const { Client, Collection, Intents } = require("discord.js");

dotenv.config();

const client = new Client({ intents: [Intents.FLAGS.GUILDS] });
client.commands = new Collection();

const commandFolders = fs.readdirSync(path.join(__dirname, "./commands"));

for (const folder of commandFolders) {
  const files = fs
    .readdirSync(path.join(__dirname, `commands/${folder}`))
    .filter((file) => file.endsWith(".js"));
  for (const file of files) {
    const command = require(path.join(__dirname, `commands/${folder}/${file}`));
    client.commands.set(command.data.name, command);
  }
}

client.on("interactionCreate", async (interaction) => {
  if (interaction.isCommand()) {
    const command = client.commands.get(interaction.commandName);

    if (!command) return;

    try {
      await command.execute(interaction);
    } catch (error) {
      console.log(error);
    }
  }
});

client.once("ready", () => {
  console.log("hello!");
  client.startup = moment();
});

client.login(process.env.TOKEN);
