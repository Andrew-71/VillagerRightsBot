const fs = require('node:fs');
const path = require('node:path');
const { Client, GatewayIntentBits, Collection } = require('discord.js');
const { token } = require('./data/config.json');
const {process_btn} = require("./utils/button_interactions");

const client = new Client({ intents: [GatewayIntentBits.Guilds] });

// Load in slash commands
client.commands = new Collection();
const commandsPath = path.join(__dirname, 'commands');
const commandFiles = fs.readdirSync(commandsPath).filter(file => file.endsWith('.js'));
for (const file of commandFiles) {
    const filePath = path.join(commandsPath, file);
    const command = require(filePath);
    client.commands.set(command.data.name, command);
    console.log(`Loaded command ${command.data.name} from ${filePath}`);
}

// Notify that the bot is ready
client.once('ready', () => {
    console.log('Ready!');
    console.log('Commands:');
    client.commands.forEach(command => {
        console.log(`- ${command.data.name}`);
    })
    client.user.setActivity('Team Fortress 3');  // Valve please
});

// handle slash commands
client.on('interactionCreate', async interaction => {
    if (!interaction.isChatInputCommand()) return;
    console.log(`Received slash command ${interaction.id} from ${interaction.user.tag} (${interaction.user.id})`);

    const command = interaction.client.commands.get(interaction.commandName);
    if (!command) return;

    try {
        await command.execute(interaction);
    } catch (error) {
        console.error(error);
        await interaction.reply({ content: 'There was an error while executing this command!', ephemeral: true });
    }
});

// handle buttons
client.on('interactionCreate', async interaction => {
    if (!interaction.isButton()) return;
    console.log(`Received button ${interaction.customId} from ${interaction.user.tag} (${interaction.user.id})`);

    await process_btn(interaction)
})

// Login
client.login(token).then(r =>
    console.log('Logged in as ' + client.user.tag))

