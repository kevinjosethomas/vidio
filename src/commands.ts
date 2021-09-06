import dotenv from "dotenv";
import { REST } from "@discordjs/rest";
import { Routes } from "discord-api-types/v9";
import { SlashCommandBuilder } from "@discordjs/builders";

import config from "./data/config.json";

dotenv.config();

const utility = [
  new SlashCommandBuilder().setName("stats").setDescription("Provides in-depth bot statistics"),
];

const commands = [...utility].map((cmd) => cmd.toJSON());

const rest = new REST({ version: "9" }).setToken(process.env.TOKEN as string);

(async () => {
  try {
    await rest.put(
      Routes.applicationGuildCommands(process.env.CLIENT_ID as string, config.guild_id) as any,
      {
        body: commands,
      }
    );

    console.log("Successfully registered all commands!");
  } catch (error) {
    console.log(error);
  }
})();
