# ban-notifier
A simple bot for bans and mutes


# Setup

Setting up this bot is quite simple, just create a second discord server and get all of the members in your main discord to join.
Make sure you also have the bot in the secondary server as well. That's it. 


# Usage

You can see some commands using .help but here's a list of all.

- .help - shows some commands
- .ban {user} {reason} bans a person
- .unban {user} unbans a person
- .mute {user} {reason} mutes a person
- .unmute {user} unmutes a person
- .clear {amount} deletes the last X messages
- .ping shows ping
- .dm {user} {message} dms user
- .status {user} shows status of user, ex. Banned: True
- .reject {user} rejects a ban appeal

That's all the commands.


# FAQ

# Q: Why do I need to create a secondary server?
A: It isn't neccesarry but it is if you want to let the person know that they are unbanned.

# Q: Help! The commands aren't working!
A: Make sure you use the @ of the user. If it doesnt show up its most likely because they are banned or left the server. If they were banned and you want to use a command on them go to ```log.txt``` and find the user id, it should look something like this: `[15:32:46.703717] Banned abc123#0669 with user id of <@!733932411934736385> for reason: None`. Now copy and paste the number in this format `<@!{number}>` then execute the command. `Ex. .status <@!733932411934736385>.`

More FAQs will be added as issue arise
