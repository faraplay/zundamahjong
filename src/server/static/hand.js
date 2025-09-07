const hand_div = document.getElementById('hand');

function createHandTileElement(tile) {
    const button = document.createElement('button');
    button.classList.add('hand_tile_button');
    const tile_item = createStraightTileElement(tile);
    button.appendChild(tile_item);
    button.addEventListener('click', (e) => {
        e.preventDefault();
        socket.emit('action', {
            'action_type': ACTION_DISCARD,
            'tile': tile
        })
    });
    return button;
}

function setHand(hand) {
    hand_div.replaceChildren(...hand.map(createHandTileElement));
}

function disableHandDiscards() {
    for (const button of hand_div.children) {
        button.disabled = true;
    }
}