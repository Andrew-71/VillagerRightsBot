const { SlashCommandBuilder, Embed, Colors } = require('discord.js');

// Basic command, which every bot seems to have
// Basically just replies with a pong. To see if the bot is alive and well.
module.exports = {
    data: new SlashCommandBuilder()
        .setName('ping')
        .setDescription('pong'),
    async execute(interaction) {
        await interaction.reply({embeds: [new Embed({
                title: 'Pong!',
                description: 'Pong! (Replied in ' + (interaction.createdTimestamp - Date.now()) + 'ms)',
                color: Colors.Blue,
        })]});
    }
};
