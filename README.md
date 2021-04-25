# TP Bot
> A discord bot to play around with.

The adventure hungry **T**ürstopper**P**inguin (Doorstop Penguin - a doorstop
toy in the form of a penguin) is reflected in this
[Discord](https://discordapp.com/) bot.

## Invite link
Make sure, you have the necessary rights to invite a bot to your wanted
discord.

[https://discordapp.com/api/oauth2/authorize?client_id=639876959350030338&permissions=2048&scope=bot](https://discordapp.com/api/oauth2/authorize?client_id=639876959350030338&permissions=2048&scope=bot)

## Modes
### Story-Mode
TP tells you stories. Ask him for some...

Prefix: `| "|>`

Available commands (after the prefix):
- `! [NAME:optional]` TP tells you a story. [NAME] defaults to `TP`.
- `+ [STORY]` tell TP a story. If he likes it, he'll continue to tell it to 
others. Use `<ACTOR>` as the [NAME] placeholder in your adventure. E.g. `| "|> + <ACTOR> is looking for more sushi!`
- `Invite` get the invite link to invite TP to your own discord server.
- `?` help-text

### Adventure-Mode
Create your own character, who levels alongside your stay.

Prefix: `">`

Available commands (after prefix):
- `new-character [FIRST_NAME LAST_NAME: optional] [!:optional]` create a new 
character. If [FIRST_NAME LAST_NAME] are provided, the new character will have 
that name. Otherwise random. [!] allows you to create a new character, even 
though you already have one. E.g. `"> new-character Max Mustermann !`
- `c` or `overview` view your character overview (name, race, level, stats)
- `q` or `questlog` view your active questlog
- `start-quest` go on a random quest (if you're already on a quest, that one 
will be aborted)
- `?` help-text

## Development
Pull requests are welcome. Help by adding features or extending available 
options like race, quests, or names.  Otherwise please send your feature 
requests via
[Github Issues](https://github.com/Bloodmallet/bloodybot/issues/new) or
[Twitter @bloodmallet](https://twitter.com/bloodmallet).
