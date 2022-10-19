const { SlashCommandBuilder, Embed, Colors } = require('discord.js');

// This is a legacy command that returns declaration of villager rights.
module.exports = {
    data: new SlashCommandBuilder()
        .setName('declaration')
        .setDescription('declaration of the rights of villagers'),
    async execute(interaction) {
        let { embed, button_row } = require('../embeds/declaration')
        await interaction.reply({embeds: [embed], components: [button_row]});
    }
};
