const http = require('http');
const amqp = require('amqplib/callback_api');


//Hocus index.html data
// const newHocusPlayer = document.getElementById('newHocusPlayer');

//index.html hocus towera
let fs = require('fs');
let handleRequest = (request, response) => {
    response.writeHead(200, {
        'Content-Type': 'text/html'
    });
    fs.readFile('./index.html', null, function (error, data) {
        if (error) {
            response.writeHead(404);
            respone.write('file not found');
        } else {
            response.write(data);
        }
        response.end();
    });
};



const server = http.createServer(handleRequest).listen(3000, '0.0.0.0', ()=> console.log('Load server on port 3000!!!'));

//creating cors for hocus internal measseging
const socketio = require('socket.io');
const io = socketio(server, {
    cors : {
        origin: "*",
        methods: ["GET", "POST"]
    }
});
const room = 'pocusTower';
let listOfPlayers1 = [];
let listOfNicknames1 = [];
let listOfIDs = [];
//object of players and id-s
var listOfHocusPlayersId = {};



console.log('Server running at http://127.0.0.1:3000/');
io.on('connection', socket=>{
    console.log('connected')


    //message to Restlin to update 1000 points for Pocus tower
    sendAmqpMessage(socket.id, '', disconnect='', shield='', name1='', connectPlayer='yes');
    socket.join(room);
    io.to(room).emit('welcome', 'a new user entered the chat')
    socket.broadcast.emit('welcome2', 'A new user entered a chat!!!')

    socket.on('attackBtn', msg=>{
        io.to(room).emit('messageToClients', msg);

        //connection to rabbitmq i message transmission to pocus tower that they are attacked
        //it has amqp to send Restlin meassage for health update
        if(msg.attack==='attack'){
            var msg1 = msg.attack;
            var we_attacked = 'We attacked Hocus tower';
            io.to(room).emit('we_attack', we_attacked)
            sendAmqpMessage('', msg1, disconnect='', shield='', name1=JSON.stringify(msg))
                    }

         else if(msg.shield==='shield'){
            var msg2 = 'shield';
            io.to(room).emit('shield', msg2)
            sendAmqpMessage('', msg1, disconnect='', shield='shield', name1=JSON.stringify(msg))
                    }

    });

    //check if nickname exist in this room
    socket.on('nick', msg=>{
        io.to(room).emit('nickname', msg)
        console.log(msg)
        sendAmqpMessage(socket.id, msg="", disconnect="", shield="", name1=msg.nickName)
    });
    //attack points for defender
        socket.on('attackResponse1', msg=>{
        io.to(room).emit('attackResponse', msg)
    });
        //health points for hocus
        socket.on('pocusHealthUpdate', msg=>{
        io.to(room).emit('pocusHealthUpdateClient', msg)
    });
    //    shild points response
    socket.on('shieldResponse', msg=>{
        io.to(room).emit('shieldResponseRoom', msg)
    });
    // message to announce who has won this round
    socket.on('win', msg=>{
        io.to(room).emit('winMessage', msg)
    })




    var socketID = socket.id;

    //return name and id from client side
    socket.on('returnNameClientSide', msg=>{
        sendAmqpMessage(msg.id, msg.name)
        console.log(msg, 'from client')
    })

    //emit from amqp that we are under attack
    socket.on("weAttacked", msg => {
        io.to(room).emit('weAreUnderAttack', msg)
  });


    //delete pleyer from round
    socket.on("disconnecting", msg => {
        var socketID = socket.id;
        sendAmqpMessage(socketID, msg="", disconnect="disconnect")
  });



    //prilokom disconnecta obavjestava ostale svoje igrace da je napustio sobu
    //salje amqp Restlinu za update podataka i brtisanje igraca iz baze


    socket.on('disconnect', ()=>{
        io.to(room).emit('bye', 'a user left the chat');
        if(io.sockets.adapter.rooms.get(room).size===1){
            sendAmqpMessage('', 'pocus', 'disconnect', '', '', '', 'endGame', )

        }

    })
})

const opti = { credentials: require('amqplib').credentials.plain('bogi', 'bogi') };


function sendAmqpMessage(playerID="", msg="", disconnect="", shield="", jsonFile="", connectPlayer='no', endGame='') {
    amqp.connect('amqp://bogi:bogi@rabbitmq/',function(error0, connection) {
        if (error0) {
            throw error0;
        }
        connection.createChannel(function(error1, channel) {
            if (error1) {
                throw error1;
            }
            var queue = 'attack';

            var newDefenderConnected = `${playerID}`
            let payload = {"pocusPlayer":newDefenderConnected, "PocusAttackToHocus":`${msg}`, "disconnect":disconnect, "shield":`${shield}`, "name":`${jsonFile}`, 'connect':`${connectPlayer}`, 'endGame':`${endGame}`}
            let sendJson = JSON.stringify(payload)


            channel.assertQueue(queue, {
                durable: false
            });
            channel.sendToQueue(queue, Buffer.from(sendJson));

            console.log(" [x] Sent %s", msg);
        });

    });
}

































