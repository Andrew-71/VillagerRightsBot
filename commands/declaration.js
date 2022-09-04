const { SlashCommandBuilder, Embed, Colors } = require('discord.js');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('declaration')
        .setDescription('declaration of the rights of villagers'),
    async execute(interaction) {
        let { embed, button_row } = require('../embeds/declaration')
        await interaction.reply({embeds: [embed], components: [button_row]});
    }
};
