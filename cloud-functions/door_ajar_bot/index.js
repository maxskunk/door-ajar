const http = require('http');
const axios = require('axios');


exports.helloBot = (req, res) => {
  console.log("CALL BACK" + JSON.stringify(req.body));

  function sendMessage(options) {
    const token = process.env.TELEGRAM_KEY;
    const url = `https://api.telegram.org/bot${token}/sendMessage`;


    axios.post(url, {
      chat_id: options.chatId,
      text: options.greetings,
    })
      .then(function (response) {
        res.send({ status: 'OK' });
      })
      .catch(function (error) {
        res.sendStatus(500);
      });
  }

  function sendKeyboard(options) {
    const token = process.env.TELEGRAM_KEY;
    const url = `https://api.telegram.org/bot${token}/sendMessage`;


    axios.post(url, {
      chat_id: options.chatId,
      text: options.greetings,
      reply_markup: {
        inline_keyboard: [[
          {
            text: 'Open The Gate!',
            callback_data: 'open-gate'
          }
        ]]
      }
    })
      .then(function (response) {
        res.send({ status: 'OK' });
      })
      .catch(function (error) {
        res.sendStatus(500);
      });
  }

  const callToken = req.path;
  //Entry Point
  if (req.body.callback_query && callToken !== 'helloBot') {
    const message = req.body.callback_query.message;
    const options = {
      greetings: "Opening the door for ya now, " + message.chat.first_name + "! Give it just a second.",
      chatId: message.chat.id
    };
    sendMessage(options);
  } else if (callToken !== 'helloBot') {
    const message = req.body.message;
    if (message.text === "/generate_button") {
      const options = {
        greetings: "When you have arrived at the gate, Press the button below to open it PLEASE do not press the button until you are here and ready to enter",
        chatId: message.chat.id
      };
      sendKeyboard(options);
    } else {
      res.send({ status: 'OK' });
    }


  } else {
    res.sendStatus(403);
  }
};