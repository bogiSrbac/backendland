const  http = require('http');
const server = http.createServer();

const socketio = require('socket.io');

const io = socketio(server, {
    cors : {
        origin: 'http://127.0.0.1:8000',
        methods: ["GET", "POST"]
    }
});

const room = 'testRoom';

io.on('connection', socket=>{
    console.log('connected')
    console.log(socket.id)

    socket.join(room)
    io.to(room).emit('welcome', 'a new user entered the chat')
    socket.broadcast.emit('welcome2', 'A new user entered a chat!!!')

    socket.on('message', msg=>{
        io.to(room).emit('messageToClients', msg)
        if(msg==='attack'){
            const amqp = require('amqplib/callback_api');

// Step 1: Create Connection
            amqp.connect('amqp://localhost', (connError, connection) => {
                if (connError) {
                    throw connError;
                }
                // Step 2: Create Channel
                connection.createChannel((channelError, channel) => {
                    if (channelError) {
                        throw channelError;
                    }
                    // Step 3: Assert Queue
                    const QUEUE = 'codingtest'
                    channel.assertQueue(QUEUE);
                    // Step 4: Send message to queue
                    channel.sendToQueue(QUEUE, Buffer.from('hello from its coding time'));
                    console.log(`Message send ${QUEUE}`);
                })
            })
                    }
                })

    socket.on('disconnect', ()=>{
        io.to(room).emit('bye', 'a user left the chat')
    })
})

server.listen(8000, ()=> console.log('Listening to server load!!!'));