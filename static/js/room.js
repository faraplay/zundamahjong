
socket.on('message', (msg) => {
    console.log(msg);
});

const name_form = document.getElementById('name_form');
const name_input = document.querySelector('#name_form input');

name_form.addEventListener('submit', (e) => {
    e.preventDefault();
    if (name_input.value) {
        socket.emit('set_name', name_input.value, (name) => {
            if (!name) return;
            console.log(`Name successfully set to ${name}`);
        });
    }
});

const create_room_form = document.getElementById('create_room_form');
const create_room_name_input = document.querySelector('#create_room_form input');
const create_room_player_count_select
    = document.querySelector('#create_room_form #player_count_select');

create_room_form.addEventListener('submit', (e) => {
    e.preventDefault();
    let player_count = Number(create_room_player_count_select.value);
    if (!(player_count == 3 || player_count == 4)) return;
    if (!create_room_name_input.value) return;
    socket.emit(
        'create_room',
        create_room_name_input.value,
        player_count,
        (room_name) => {
            if (!room_name) return;
            console.log(`Created room ${room_name}`)
        });
});

const join_room_form = document.getElementById('join_room_form');
const room_list_select = document.getElementById('room_list');
const refresh_room_list_button = document.getElementById('refresh_room_list');

refresh_room_list_button.addEventListener('click', (e) => {
    e.preventDefault();
    socket.emit('get_rooms', (rooms) => {
        if (!rooms) return;
        room_list_select.options.length = 0;
        for (const room of rooms) {
            const room_option = document.createElement("option");
            room_option.value = room;
            room_option.textContent = room;
            room_list_select.options.add(room_option);
        }
    });
})

join_room_form.addEventListener('submit', (e) => {
    e.preventDefault();
    if (room_list_select.value) {
        socket.emit('join_room', room_list_select.value, (room_name) => {
            if (!room_name) return;
            console.log(`Joined room ${room_name}`)
        });
    }
});

const leave_room_button = document.getElementById('leave_room');
leave_room_button.addEventListener('click', (e) => {
    e.preventDefault();
    socket.emit('leave_room', (room_name) => {
        if (!room_name) return;
        console.log(`Left room ${room_name}`)
    })
})