
const name_form = document.getElementById('name_form');
const name_input = document.getElementById('name_input');

name_form.addEventListener('submit', (e) => {
    e.preventDefault();
    if (name_input.value) {
        socket.emit('set_name', name_input.value);
    }
});

socket.on('name_in_use_error', () => {
    console.log("Name is already in use");
})

socket.on('set_name_success', () => {
    console.log("Name successfully set");
})
