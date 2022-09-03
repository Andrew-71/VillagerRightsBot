const { SlashCommandBuilder, ActionRowBuilder, ButtonBuilder, ButtonStyle } = require('discord.js');
const Discord = require('discord.js')

module.exports = {
    data: new SlashCommandBuilder()
        .setName('ping')
        .setDescription('Generate a test captcha!'),
    async execute(interaction) {
        let captcha_text = require('../utils/captcha_utils').generateCaptcha()
        const row = require('../utils/captcha_utils').makeActionRow(captcha_text)
        let embed = require('../embeds/captcha_embed').data
        await interaction.reply({embeds: [embed], files: [{
            attachment: 'data/captcha_image.png',
            name: 'captcha_image.png'
            }], components: [row], ephemeral: true});
    },
};