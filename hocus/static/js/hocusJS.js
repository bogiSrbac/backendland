// console.log('hello world');
//
// const socket = io( );
//
// const alertBox = document.getElementById('alert-box');
// const messageBox = document.getElementById('messages-box');
// const messageInput = document.getElementById('message-input');
// const sendBtn = document.getElementById('send-btn');
//
// // socket.on('welcome', msg=>{
// //     console.log(msg)
// // })
//
// const handleAlerts = (msg, type)=>{
//     alertBox.innerHTML = `<div class="alert alert-${type}" role="alert">${msg}</div>`;
//     setTimeout(()=>{
//         alertBox.innerHTML = '';
//     }, 4000)
// }
//
// socket.on('welcome2', msg=>{
//     handleAlerts(msg, 'primary')
// });
//
// socket.on('bye', msg=>{
//     handleAlerts(msg, 'danger')
// });
//
//
// sendBtn.addEventListener('click', ()=>{
//     const message = messageInput.value;
//     messageInput.value = ''
//     console.log(message)
//
//     socket.emit('message', message)
// });
//
// socket.on('messageToClients', msg=>{
//     messageBox.innerHTML += `<b>${msg}</b><br>`
// })
//
//
//
