const { SlashCommandBuilder, Embed, Colors } = require('discord.js');

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
