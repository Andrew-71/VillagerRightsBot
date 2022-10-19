let svgCaptcha = require('svg-captcha');
const {ButtonBuilder, ButtonStyle, ActionRowBuilder} = require("discord.js");
const path = require("path");
svgCaptcha.loadFont(path.resolve(__dirname, '../data/OpenSans-VariableFont.ttf'))

// Convert SVG captcha to a PNG for display in the embed
function svgToPng(svg, filename)
{
    const svg2img = require('svg2img');
    const fs = require('fs');

    svg2img(svg, function(error, buffer) {
        if (error) throw error;
        fs.writeFileSync(path.resolve(__dirname, filename), buffer);
    });
}

// Generate a captcha image. Returns answer and saves file to data/captcha_image.png
function generateCaptcha()
{
    let captcha = svgCaptcha.create({size: 6,
        noise: 2,
        color: false,
        background: '#eaeaea',
        width: 300,
        height: 100,});

    // Save to file
    let filename = '../data/captcha_image.png';
    svgToPng(captcha.data, filename);

    return captcha.text; // return the answer
}

// Create unique ID for the captcha buttons to ensure they are unique (Doesn't affect anything, still good idea)
function makeId(length) {
    let result = '';
    let characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let charactersLength = characters.length;
    for (let i = 0; i < length; i++)
    {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
}

// Create a button row for captcha.
// Returns action tow with 4 buttons. One has correct answer, others fake one. All buttons are in random order.
function makeActionRow(correct_answer)
{
    let buttons = [
        new ButtonBuilder()
            .setCustomId('correct_' + makeId(20))
            .setLabel(correct_answer)
            .setStyle(ButtonStyle.Secondary),
        new ButtonBuilder()
            .setCustomId('incorrect_' + makeId(20))
            .setLabel(makeId(6))
            .setStyle(ButtonStyle.Secondary),
        new ButtonBuilder()
            .setCustomId('incorrect_' + makeId(20))
            .setLabel(makeId(6))
            .setStyle(ButtonStyle.Secondary),
        new ButtonBuilder()
            .setCustomId('incorrect_' + makeId(20))
            .setLabel(makeId(6))
            .setStyle(ButtonStyle.Secondary),
    ]

    // Shuffle the buttons
    for (let i = buttons.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [buttons[i], buttons[j]] = [buttons[j], buttons[i]];
    }

    return new ActionRowBuilder()
        .addComponents(buttons);
}

// Create a button to start the captcha
function makeStartButton(msg)
{
    return new ActionRowBuilder()
        .addComponents(
            new ButtonBuilder()
                .setCustomId('captcha_start')
                .setLabel(msg)
                .setStyle(ButtonStyle.Success))
}

module.exports = {
    generateCaptcha: generateCaptcha,
    makeActionRow: makeActionRow,
    makeStartButton: makeStartButton
}