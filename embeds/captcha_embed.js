const { EmbedBuilder, Embed, Colors } = require('discord.js')

module.exports = {
    data:
    new EmbedBuilder()
        .setColor(0x0099FF)
        .setTitle('Test Captcha')
        .setDescription('Use buttons to submit your answer!')
        .setImage('attachment://captcha_image.png'),
    incorrect:
    new EmbedBuilder()
        .setColor(Colors.DarkRed)
        .setTitle('Incorrect')
        .setDescription('Press the button below to retry'),
    correct:
    new EmbedBuilder()
        .setColor(Colors.DarkGreen)
        .setTitle('Correct')
        .setDescription('You will now receive access to the server!'),
    initial:
    new EmbedBuilder()
        .setColor(0x0099FF)
        .setTitle('Welcome to VillagerRights!')
        .setDescription('Please verify that you are not a bot by completing the captcha below.')
        .addFields([{name: 'Instructions',
            value: 'Click the button below to start the captcha. ' +
                   'Then, click the button that corresponds to the text in the image.', inline: false}])
}