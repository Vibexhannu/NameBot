const prompt = require('prompt');
const fs = require("fs");
const login = require("fca-unofficial");

console.clear();
console.log('\x1b[33m%s\x1b[0m\n', `░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓███████▓▒░░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓██████▓▒░  ░▒▓██████▓▒░  
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░         ░▒▓█▓▒░     
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░         ░▒▓█▓▒░     
░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░  ░▒▓█▓▒░     
                                                                   
                                                                   
`);

prompt.message = '\x1b[32m'; 
prompt.delimiter = ''; 

const passwordPrompt = {
    name: 'password',
    description: '\x1b[36mPassword : ', 
    hidden: true, 
    replace: '*'
};

const filePathPrompt = {
    name: 'filePath',
    description: '\x1b[36mToken File Path : ', 
};

const targetIDPrompt = {
    name: 'targetID',
    description: '\n\x1b[36mConversation ID : ', 
};

const timerPrompt = {
    name: 'timer',
    description: '\n\x1b[36mEnter Your Delay (in seconds): ', 
    required: true,
    type: 'number'
};

const groupNamePrompt = {
    name: 'groupName',
    description: '\n\x1b[36mEnter Group Name : ', 
    required: true,
};

const nickNamePrompt = {
    name: 'nickName',
    description: '\n\x1b[36mEnter Nick Name : ', 
    required: true,
};

prompt.get([passwordPrompt, filePathPrompt, targetIDPrompt, timerPrompt, groupNamePrompt, nickNamePrompt], function (err, result) {
    if (err) { return onErr(err); }

    const userAgent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36';

    login({ appState: JSON.parse(fs.readFileSync(result.filePath, 'utf8')), userAgent: userAgent }, (err, api) => {
        if (err) return console.error(err);
        fs.writeFileSync("anox11.json", JSON.stringify(api.getAppState(), null, '\t'));

        const ensureGroupName = () => {
            api.getThreadInfo(result.targetID, (err, info) => {
                if (err) return console.error(err);

                if (info.threadName !== result.groupName) {
                    api.setTitle(result.groupName, result.targetID, (err) => {
                        if (err) console.error(`Error setting group name: ${err}`);
                        else console.log(`Group name set to ${result.groupName}`);
                    });
                }
            });
        };

        const ensureNickName = () => {
            api.getThreadInfo(result.targetID, (err, info) => {
                if (err) return console.error(err);

                info.participantIDs.forEach(participant => {
                    if (info.nicknames[participant] !== result.nickName) {
                        api.changeNickname(result.nickName, result.targetID, participant, (err) => {
                            if (err) console.error(`Error setting nickname for participant ${participant}: ${err}`);
                            else console.log(`Nickname set to ${result.nickName} for participant ${participant}`);
                        });
                    }
                });
            });
        };

        const enforceSettings = () => {
            ensureGroupName();
            ensureNickName();
        };

        setInterval(enforceSettings, result.timer * 1000); 
    });
});

function onErr(err) {
    console.error('Error:', err);
    return 1;
}

process.on('unhandledRejection', (err, p) => {
    console.error('Unhandled Rejection:', err);
});
