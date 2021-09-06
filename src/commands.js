const fs = require("fs");
const path = require("path");
const dotenv = require("dotenv");
const { REST } = require("@discordjs/rest");
const { Routes } = require("discord-api-types/v9");

const { guild_id } = require("./data/config.json");

dotenv.config();

const commands = [];
const commandFolders = fs.readdirSync(path.join(__dirname, "commands"));

commandFolders.map((folder) => {
  const files = fs
    .readdirSync(path.join(__dirname, `commands/${folder}`))
    .filter((file) => file.endsWith(".js"));
  for (const file of files) {
    const command = require(path.join(__dirname, `commands/${folder}/${file}`));
    commands.push(command.data.toJSON());
  }
});

const rest = new REST({ version: "9" }).setToken(process.env.TOKEN);

(async () => {
  try {
    await rest.put(Routes.applicationGuildCommands(process.env.CLIENT_ID, guild_id), {
      body: commands,
    });

    console.log("Successfully registered all commands!");
  } catch (error) {
    console.log(error);
  }
})();
