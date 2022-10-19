// This script registers all the commands for the bot in Discord.
// Since their command system is extremely strange.

const fs = require('node:fs');
const path = require('node:path');
const { REST } = require('@discordjs/rest');
const { Routes } = require('discord.js');
const { app_id, token } = require('./data/config.json');
const { guild } = require('./data/config.json').ids;

const commands = [];
const commandsPath = path.join(__dirname, 'commands');
const commandFiles = fs.readdirSync(commandsPath).filter(file => file.endsWith('.js'));

for (const file of commandFiles) {
    const filePath = path.join(commandsPath, file);
    const command = require(filePath);
    commands.push(command.data.toJSON());
}

const rest = new REST({ version: '10' }).setToken(token);

// Register commands
rest.put(Routes.applicationGuildCommands(app_id, guild), { body: commands })
    .then(() =>
    {
        console.log('Successfully registered application commands.')
        console.log('Commands:');
        commands.forEach(command => {
            console.log(`- ${command.name}`);
        })
    })
    .catch(console.error);
