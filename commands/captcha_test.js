const { SlashCommandBuilder, ActionRowBuilder, ButtonBuilder, ButtonStyle } = require('discord.js');
const Discord = require('discord.js')
const {data: embed, initial} = require("../embeds/captcha_embed");
const {makeStartButton} = require("../utils/captcha_utils");

async function captcha_msg(interaction) {
    let captcha_text = require('../utils/captcha_utils').generateCaptcha()
    const row = require('../utils/captcha_utils').makeActionRow(captcha_text)
    let embed = require('../embeds/captcha_embed').data
    await interaction.reply({
        embeds: [embed], files: [{
            attachment: 'data/captcha_image.png',
            name: 'captcha_image.png'
        }], components: [row], ephemeral: true
    });
}

module.exports = {
    data: new SlashCommandBuilder()
        .setName('captcha_initial')
        .setDescription('Initial captcha message')
        .addStringOption(option =>
            option.setName('verification_channel')
                .setDescription('Where to put the message')
                .setRequired(true)),
    async execute(interaction) {
        let channel_id = interaction.options.getString('verification_channel')
        let initial = require('../embeds/captcha_embed').initial
        let channel = await interaction.guild.channels.cache.get(channel_id)
        channel.send({embeds: [initial], components: [makeStartButton('Verify')]})
        await interaction.reply({content: 'Sent', ephemeral: true})
    },
    captcha_msg: captcha_msg,
};