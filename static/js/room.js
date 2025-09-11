
socket.on('message', (msg) => {
    console.log(msg);
});

const room_info_element = document.getElementById('room_info');

const name_form = document.getElementById('name_form');
const name_input = document.querySelector('#name_form input');

const create_room_form = document.getElementById('create_room_form');
const create_room_name_input = document.querySelector('#create_room_form input');
const create_room_player_count_select
    = document.querySelector('#create_room_form #player_count_select');
const create_room_button = document.querySelector('#create_room_form button');

const join_room_form = document.getElementById('join_room_form');
const room_list_select = document.getElementById('room_list');
const join_room_button = document.querySelector('#join_room_form button');
const refresh_room_list_button = document.getElementById('refresh_room_list');

const leave_room_button = document.getElementById('leave_room');

const start_game_button = document.getElementById('start_game');

var my_player = null;
var my_room_info = null;

function setRoomInfo(room_info) {
    my_room_info = room_info;
    if (room_info) {
        room_info_element.textContent =
            `Room ${room_info.room_name} --- `
            + `${room_info.player_count} player game --- `
            + `Players: ${room_info.joined_players.join(", ")}`;
        create_room_button.disabled = true;
        join_room_button.disabled = true;
        leave_room_button.disabled = false;
        start_game_button.disabled =
            !(room_info.joined_players.length == room_info.player_count);
    } else {
        room_info_element.textContent = ""
        create_room_button.disabled = false;
        join_room_button.disabled = false;
        leave_room_button.disabled = true;
        start_game_button.disabled = true;
    }
}

socket.on('room_info', setRoomInfo);

function refreshRoomList() {
    socket.emit('get_rooms', (rooms) => {
        if (!rooms) return;
        room_list_select.options.length = 0;
        for (const room_info of rooms) {
            const room_option = document.createElement("option");
            room_option.value = room_info.room_name;
            room_option.textContent =
                `${room_info.room_name} (${room_info.joined_players.length}/${room_info.player_count})`;
            room_option.disabled = room_info.joined_players.length == room_info.player_count;
            room_list_select.options.add(room_option);
        }
    });
}


name_form.addEventListener('submit', (e) => {
    e.preventDefault();
    if (name_input.value) {
        socket.emit('set_name', name_input.value, (player, room_info, is_in_game) => {
            if (!player) return;
            my_player = player;
            setRoomInfo(room_info);
            if (!room_info) {
                showScreen("lobby_screen");
                refreshRoomList();
            } else if (!is_in_game) {
                showScreen("room_screen");
            } else {
                showScreen("game_screen");
            }
        });
    }
});

create_room_form.addEventListener('submit', (e) => {
    e.preventDefault();
    let player_count = Number(create_room_player_count_select.value);
    if (!(player_count == 3 || player_count == 4)) return;
    if (!create_room_name_input.value) return;
    socket.emit(
        'create_room',
        create_room_name_input.value,
        player_count,
        (room_info) => {
            if (!room_info) return;
            setRoomInfo(room_info);
            console.log(`Created room ${room_info.room_name}`)
            showScreen("room_screen");
        });
});

refresh_room_list_button.addEventListener('click', (e) => {
    e.preventDefault();
    refreshRoomList();
})

join_room_form.addEventListener('submit', (e) => {
    e.preventDefault();
    if (room_list_select.value) {
        socket.emit('join_room', room_list_select.value, (room_info) => {
            if (!room_info) return;
            setRoomInfo(room_info);
            console.log(`Joined room ${room_info.room_name}`)
            showScreen("room_screen");
        });
    }
});

leave_room_button.addEventListener('click', (e) => {
    e.preventDefault();
    socket.emit('leave_room', (room_info) => {
        if (!room_info) return;
        setRoomInfo(null);
        console.log(`Left room ${room_info.room_name}`)
        showScreen("lobby_screen");
    })
})

start_game_button.addEventListener('click', (e) => {
    e.preventDefault();
    socket.emit('start_game', my_room_info.room_name)
})
