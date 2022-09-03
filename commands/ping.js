const { SlashCommandBuilder, Embed, Colors } = require('discord.js');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('pong')
        .setDescription('pong'),
    async execute(interaction) {
        await interaction.reply({embeds: [new Embed({
                title: 'Pong!',
                description: 'Pong!',
                color: Colors.Blue,
        })]});
    }
};
