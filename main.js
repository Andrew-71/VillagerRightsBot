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

// This is a basic prototype of the manager for some commands.
// These will be "old-style" so that they don't appear in the slash command list.
// because they are not meant to be used by users.
// only by the bot master.
client.on('messageCreate', message => {
    if (message.content.startsWith('!!message')) {
        let { bot_master_role } = require('data/config.json').ids;
        let member_roles = message.member.roles;
        if (!(member_roles.cache.has(bot_master_role)))
        {
            return // dont even notify the user because they could use this to spam
        }
        // delete the message and send content
        message.delete()
        message.channel.send(message.content.slice(9))
    }
})

// Login
client.login(token).then(r =>
    console.log('Logged in as ' + client.user.tag))

