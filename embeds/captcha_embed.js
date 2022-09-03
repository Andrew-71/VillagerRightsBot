const { EmbedBuilder, Embed, Colors } = require('discord.js')

module.exports = {
    data:
    new EmbedBuilder()
        .setColor(0x0099FF)
        .setTitle('Test Captcha')
        .setDescription('Use buttons to submit your answer!')
        .setImage('attachment://captcha_image.png')
        .setTimestamp()
        .setColor(Colors.Fuchsia)
}