const { SlashCommandBuilder } = require('discord.js');
const {makeStartButton} = require("../utils/captcha_utils");

// Send a captcha image in answer to an interaction
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
    // Command for initial captcha message
    data: new SlashCommandBuilder()
        .setName('captcha_initial')
        .setDescription('Initial captcha message')
        .addStringOption(option =>
            option.setName('verification_channel')
                .setDescription('Where to put the message')
                .setRequired(true)),
    async execute(interaction) {

        // Check that the user is authorized to use the command
        let { bot_master_role } = require('../data/config.json').ids;
        let member_roles = interaction.member.roles;
        if (!(member_roles.cache.has(bot_master_role)))
        {
            await interaction.reply({content: 'You are not authorized to use this command.', ephemeral: true})
            return
        }

        // We do not check for channel validity here because only 1 moderator will use this once.
        // Still, I suppose I should add it eventually.
        // TODO: channel existence check
        let channel_id = interaction.options.getString('verification_channel')
        let initial = require('../embeds/captcha_embed').initial
        let channel = await interaction.guild.channels.cache.get(channel_id)
        channel.send({embeds: [initial], components: [makeStartButton('Verify')]})
        await interaction.reply({content: 'Sent', ephemeral: true})
    },
    captcha_msg: captcha_msg,
};