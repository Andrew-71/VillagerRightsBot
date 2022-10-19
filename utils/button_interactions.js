const { makeStartButton } = require("./captcha_utils");

module.exports = {
    process_btn: async function(interaction) {

        // Correct captcha answer
        if (interaction.customId.startsWith('correct_'))
        {
            let correct = require('../embeds/captcha_embed').correct
            await interaction.update({embeds: [correct], components: []});

            // Give user the activist role (Base one)
            let { activist_role } = require('../data/config.json').ids;  // ID of the activist role
            let role = interaction.guild.roles.cache.get(activist_role)
            let member = interaction.member;
            await member.roles.add(role);
        }

        // Incorrect captcha answer
        else if (interaction.customId.startsWith('incorrect_'))
        {
            let incorrect = require('../embeds/captcha_embed').incorrect
            await interaction.update({embeds: [incorrect], components: [makeStartButton('Retry')]});
        }

        // Initial request for captcha
        if (interaction.customId === 'captcha_start')
        {
            await require('../commands/captcha').captcha_msg(interaction)
        }
    }
}