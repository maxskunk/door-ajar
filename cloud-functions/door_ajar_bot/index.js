const http = require('http');
const axios = require('axios');
const request = require('request');


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
    if (message.chat.type === "private") {
      res.send({ status: 'OK' });
    } else {
      const dak = process.env.DOOR_ACCESS_KEY;
      let url = "https://us-central1-zokya-media.cloudfunctions.net/dooraccess?key=" + dak; //or production  
      request.post({
        headers: {
          'content-type': 'application/x-www-form-urlencoded'
        },
        url: url
      }, (error, response, body) => {
        if (error) {
          const options = {
            greetings: "Shit Something went wrong: " + JSON.stringify(response),
            chatId: message.chat.id
          };
          sendMessage(options);
        } else {
          const statusCode = response.statusCode;
          if (statusCode === 401) {
            const options = {
              greetings: req.body.callback_query.from.first_name+", Unfortunatly that button seems to be invalid, Perhaps it is expired? Better talk to Max.",
              chatId: message.chat.id
            };
            sendMessage(options);
          } else if(statusCode === 200) {
            const options = {
              greetings: "Opening the door for you now, " + req.body.callback_query.from.first_name + "! Give it just a second.",
              chatId: message.chat.id
            };
            sendMessage(options);
          } else if(statusCode === 500) {
            const options = {
              greetings: "Sorry " + req.body.callback_query.from.first_name + ", it appears we lost connection to the local switcher. Better Tell Max!",
              chatId: message.chat.id
            };
            sendMessage(options);
          } else {
            const options = {
              greetings: "Something rather unexpected happened, Better talk to Max."+JSON.stringify(response),
              chatId: message.chat.id
            };
            sendMessage(options);
          }
        }
      });
    }

  } else if (callToken !== 'helloBot') {
    const message = req.body.message;
    if (message.text === "/generate_button") {
      if (message.chat.type === "private") {
        res.send({ status: 'OK' });
      } else {
        const options = {
          greetings: "***ATTENTION*** PLEASE do not press the button until you are in-front of the gate and ready to enter! When you have arrived at the gate, Press the button below to open it.",
          chatId: message.chat.id
        };
        sendKeyboard(options);
      }
    } else {
      res.send({ status: 'OK' });
    }


  } else {
    res.sendStatus(403);
  }
};