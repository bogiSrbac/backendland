const defenderBtn = document.getElementById('defenderBtn');
const tower = document.getElementById('id_tower');
const nickname = document.getElementById('id_nickname');
const defender = document.getElementById('defender');
const alert = document.getElementById('alert');

defender.addEventListener('submit', e=>{
    e.preventDefault();
    console.log('test1');
    const defenderXHR = new FormData();
    defenderXHR.append('csrfmiddlewaretoken', csrftoken);
    defenderXHR.append('nickname', nickname.value);
    defenderXHR.append('tower', tower.value);
    let updateXHR = new XMLHttpRequest();
    updateXHR.responseType = 'json';
    updateXHR.enctype = 'multipart/form-data';
    updateXHR.data = defenderXHR;
    let updateURL = `/hocus/create-defender/`;
    updateXHR.open('POST', updateURL, true);
    updateXHR.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    console.log('test2');
    updateXHR.onload = function () {
        update = updateXHR.response;

        var nicknameCheck = nickname.value;

        if(update.submit==='hocus'){
            newPlayerName(nicknameCheck)

         }else if (update.submit==='pocus'){
            console.log('pocus')
            newPlayerName(nicknameCheck)

        }
        nickname.value = '';
        tower.value = '';

        if(update.submit==='hocus'){
           openLink('hocus')

         }else if (update.submit==='pocus'){
            openLink('pocus')

        }else{
            alert.style.display = 'block';
            alert.innerHTML = `<p>We already have requested nickname ${nicknameCheck} in this round.</p><br>
                                <p>Please, choose another nick.</p>`
            setTimeout(function(){
                alert.style.display = 'none';
            }, 6000)
        }


    };
    updateXHR.send(defenderXHR);

});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');



function openLink(tower) {
    if(tower==='hocus'){
        window.location.href = "http://127.0.0.1:666/"
    }else{
        window.location.href = "http://127.0.0.1:3000/"
    }
}

//create first round and towers hocus and pocus
function createInitialGame(funct) {
    document.addEventListener('DOMContentLoaded', (event)=>{
        funct
    })
}



function createFunc() {
    let createXHR = new XMLHttpRequest();
    createXHR.responseType = 'json';
    createXHR.enctype = 'multipart/form-data';
    let createURL = `/hocus/create-first-round/`;
    createXHR.open('POST', createURL, true);
    createXHR.setRequestHeader("X-CSRFToken", csrftoken);
    createXHR.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    console.log('createLoad');
    createXHR.onload = function () {
        send = createXHR.response;
    };
    createXHR.send();
}

createInitialGame(createFunc())



function newPlayerName(name) {
    let sendXHR = new XMLHttpRequest();
    sendXHR.responseType = 'json';
    sendXHR.enctype = 'multipart/form-data';
    let sendURL = `/hocus/create-nick/${name}/`;
    sendXHR.open('GET', sendURL, true);
    sendXHR.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    console.log('test2');
    sendXHR.onload = function () {
        send = sendXHR.response;
    };
    sendXHR.send();
}

