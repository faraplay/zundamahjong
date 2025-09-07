
const discard_pool = document.getElementById('discard_pool');
const calls_list = document.getElementById('calls_list');

function createTableTileElement(tile) {
    const item = createTileElement(tile);
    item.firstChild.classList.add('tile_face');
    for (const class_name of ['tile_left', 'tile_right', 'tile_top', 'tile_bottom']) {
        const side_item = document.createElement('span');
        side_item.classList.add('tile_face');
        side_item.classList.add('tile_side');
        side_item.classList.add(class_name);
        item.appendChild(side_item);
    }
    item.appendChild(item.firstChild);
    return item;
}

function createSeatDiscardsElement(seat, seat_discard_tiles) {
    const seat_discards_item = document.createElement("div");
    seat_discards_item.classList.add("seat_discards");
    const seat_item_title = document.createElement('h4');
    seat_item_title.textContent = `Player ${seat}`;
    seat_discards_item.appendChild(seat_item_title);

    for (const tile of seat_discard_tiles) {
        tile_item = createTableTileElement(tile);
        seat_discards_item.appendChild(tile_item);
    }
    return seat_discards_item;
}

function setDiscards(my_seat, discards) {
    const seat_discard_items = []
    for (var seat = 0; seat < 4; ++seat) {
        const seat_discard_tiles =
            discards.filter(discard => discard.seat == seat)
                .map(discard => discard.tile);
        seat_discard_items.push(createSeatDiscardsElement(seat, seat_discard_tiles))
    }
    for (var i = 0; i < 4; ++i) {
        seat_discard_items[(my_seat + i) % 4].classList.add(`position_${i}`);
    }
    discard_pool.replaceChildren(...seat_discard_items);
}

function createTableCallElement(call) {
    const call_item = document.createElement("span");
    call_item.classList.add('call');
    const call_type_item = document.createElement("h4");
    call_type_item.textContent = call_types[call.call_type];
    call_item.appendChild(call_type_item);
    for (const tile of call.tiles) {
        tile_item = createTableTileElement(tile);
        call_item.appendChild(tile_item);
    }
    return call_item;
}

function createSeatCallsElement(seat, calls) {
    const seat_call_item = document.createElement('div');
    seat_call_item.classList.add('seat_calls');
    const seat_item_title = document.createElement('h4');
    seat_item_title.textContent = `Player ${seat}`;
    seat_call_item.appendChild(seat_item_title);

    for (const call of calls) {
        call_item = createTableCallElement(call);
        seat_call_item.appendChild(call_item);
    }
    return seat_call_item;
}

function setCalls(my_seat, calls) {
    const seat_call_items = []
    for (var seat = 0; seat < 4; ++seat) {
        seat_call_items.push(createSeatCallsElement(seat, calls[seat]))
    }
    for (var i = 0; i < 4; ++i) {
        seat_call_items[(my_seat + i) % 4].classList.add(`position_${i}`);
    }
    calls_list.replaceChildren(...seat_call_items);
}
