const screen_ids = [
    "name_screen",
    "lobby_screen",
    "room_screen",
    "game_screen",
];

const screens = Object.fromEntries(screen_ids.map(
    id => [id, document.getElementById(id)]
));

function showScreen(screen_id) {
    for (const id of screen_ids) {
        screens[id].hidden = (id != screen_id);
    }
}