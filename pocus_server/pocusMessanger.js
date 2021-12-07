const io = require('socket.io-client');
var socket = io('http://127.0.0.1:3000/');



var amqp = require('amqplib/callback_api');
const opt = { credentials: require('amqplib').credentials.plain('bogi', 'bogi') };


let listOfPlayers1 = [];
let listOfNicknames1 = [];
let listOfIDs = [];
//object of players and id-s
var listOfHocusPlayersId = {};


amqp.connect('amqp://bogi:bogi@rabbitmq:5672', function(error0, connection) {
  if (error0) {
    throw error0;
  }
  connection.createChannel(function(error1, channel) {
    if (error1) {
      throw error1;
    }
    var queue = 'rpc_queue';

    channel.assertQueue(queue, {
      durable: false
    });
    channel.prefetch(1);
    console.log(' [x] Awaiting RPC requests');
    channel.consume(queue, function reply(msg) {
      var json = String.fromCharCode.apply(String, msg.content);
      var n = JSON.parse(json);


      let r='';

      //creating object with data players in room pocus
      if(checkIfPlayerInList(listOfNicknames1, n.name)){
          r = {'status':'exist', 'name':n.name};
      }else{

        addPlayerToList(listOfPlayers1, listOfNicknames1, n.name);
        socket.emit('name', n.name);
        r = {'status': 'no', 'name':n.name}
      }


      setTimeout(function () {
            channel.sendToQueue(msg.properties.replyTo,
            Buffer.from(JSON.stringify(r)), {
            correlationId: msg.properties.correlationId
        });
    }, 1000);


      channel.ack(msg);
    });
  });
});

function addPlayerToList(listOfPlayers, listOfNicknames, player) {
    var lenOfArray = listOfPlayers.length;
    listOfPlayers.push(`player${lenOfArray}`);
    listOfNicknames.push(player)
    console.log(listOfPlayers, listOfNicknames)

}

function checkIfPlayerInList(list, name) {
  for(let i = 0; i < list.length; i++){
    if(name === list[i]){
      return true
    }
  }
}



amqp.connect('amqp://bogi:bogi@rabbitmq:5672',  function(error0, connection) {
  if (error0) {
    throw error0;
  }
  connection.createChannel(function(error1, channel) {
    if (error1) {
      throw error1;
    }
    var exchange = 'logs';

    channel.assertExchange(exchange, 'fanout', {
      durable: false
    });

    channel.assertQueue('', {
      exclusive: true
    }, function(error2, q) {
      if (error2) {
        throw error2;
      }
      console.log(" [*] Waiting for messages in %s. To exit press CTRL+C", q.queue);
      channel.bindQueue(q.queue, exchange, '');

      channel.consume(q.queue, function(msg) {
        if(msg.content) {
            var json = String.fromCharCode.apply(String, msg.content);
            let nick = JSON.parse(json);
            console.log(nick)

            setTimeout(function () {
                    if(typeof nick.nickName !== 'undefined' && nick.tower === 'Pocus'){
               socket.emit('nick', nick);
               socket.on('idToList', msg=>{
        })
            }else if(nick.shieldPoints && nick.pocus === 'pocus'){
                        socket.emit('shieldResponse', nick)

                    }
                    else if (nick.attackPoints && nick.pocus === 'pocus'){
                        socket.emit('attackResponse1', nick);

                    }else if(nick.pocusHealth){
                        socket.emit('pocusHealthUpdate', nick)
                    }else if(nick.win){
                        socket.emit('win', nick)
                    }else if(nick.winEnd){
                        socket.emit('win', nick)
                    }
                    if(nick.HocusAttackToPocus === 'attack'){
                        socket.emit('weAttacked', nick)
                    }
            }, 1000)
          }
      }, {
        noAck: true
      });
    });
  });
});



































































































