const fs = require('node:fs');
const path = require('node:path');
const { Client, GatewayIntentBits, Collection } = require('discord.js');
const { token } = require('./data/config.json');
const {makeStartButton} = require("./utils/captcha_utils");
const {process_btn} = require("./utils/button_interactions");

const client = new Client({ intents: [GatewayIntentBits.Guilds] });
client.commands = new Collection();
const commandsPath = path.join(__dirname, 'commands');
const commandFiles = fs.readdirSync(commandsPath).filter(file => file.endsWith('.js'));

for (const file of commandFiles) {
    const filePath = path.join(commandsPath, file);
    const command = require(filePath);
    // Set a new item in the Collection
    // With the key as the command name and the value as the exported module
    client.commands.set(command.data.name, command);
    console.log(`Loaded command ${command.data.name} from ${filePath}`);
}

client.once('ready', () => {
    console.log('Ready!');
    console.log('Commands:');
    client.commands.forEach(command => {
        console.log(`- ${command.data.name}`);
    })

    client.user.setActivity('Team Fortress 3');
});

client.on('interactionCreate', async interaction => {
    console.log(`Received interaction ${interaction.id} from ${interaction.user.tag} (${interaction.user.id})`);
    if (!interaction.isChatInputCommand()) return;

    const command = interaction.client.commands.get(interaction.commandName);

    if (!command) return;

    try {
        await command.execute(interaction);
    } catch (error) {
        console.error(error);
        await interaction.reply({ content: 'There was an error while executing this command!', ephemeral: true });
    }
});

client.on('interactionCreate', async interaction => {
    if (!interaction.isButton()) return;
    console.log(`Received button ${interaction.customId} from ${interaction.user.tag} (${interaction.user.id})`);

    await process_btn(interaction)
})

client.login(token).then(r =>
    console.log('Logged in as ' + client.user.tag))

