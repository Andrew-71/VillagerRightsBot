const { EmbedBuilder, ActionRowBuilder, ButtonBuilder, ButtonStyle} = require('discord.js')

module.exports = {
    embed:
        new EmbedBuilder()
            .setColor(0x0099FF)
            .setTitle('Declaration')
            .setImage('attachment://captcha_image.png'),
    button_row:
        new ActionRowBuilder()
            .addComponents(
            new ButtonBuilder()
                .setStyle(ButtonStyle.Link)
                .setURL('https://www.reddit.com/r/villagerrights/comments/ipvejn')
                .setLabel("Declaration")
            )
}