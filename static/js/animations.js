function add_animation(element, animation_style, duration_milliseconds, delay_milliseconds) {
    element.classList.add("animate");
    element.classList.add(animation_style);
    element.style.setProperty("--animation-duration", `${duration_milliseconds}ms`);
    element.style.setProperty("--animation-delay", `${delay_milliseconds}ms`);
    return duration_milliseconds;
}

function setAnimation(player, action, delay_milliseconds) {
    console.log(player, action);
    switch (action.action_type) {
        case ACTION_DRAW:
            return setDrawAnimation(player, action, delay_milliseconds);
        case ACTION_DISCARD:
            return setDiscardAnimation(player, action, delay_milliseconds);
        case ACTION_CHI_A:
        case ACTION_CHI_B:
        case ACTION_CHI_C:
        case ACTION_PON:
            return setCallAnimation(player, action, delay_milliseconds);
        case ACTION_OPEN_KAN:
        case ACTION_CLOSED_KAN:
            return setNewKanAnimation(player, action, delay_milliseconds);
        case ACTION_ADD_KAN:
            return setAddKanAnimation(player, action, delay_milliseconds);
        case ACTION_FLOWER:
            return setFlowerAnimation(player, action, delay_milliseconds);
    }
}

function setDrawAnimation(player, action, delay_milliseconds) {
    const drawn_tile_element = document.querySelector(
        `#table_hands .table_hand_outer.player_${player} .table_hand > *:last-child`
    );
    return add_animation(
        drawn_tile_element,
        "animate_draw",
        250,
        delay_milliseconds
    );
}

function setDiscardAnimation(player, action, delay_milliseconds) {
    const discarded_tile_element = document.querySelector(
        `#discard_pool .player_discards.player_${player} > *:last-child`
    );
    return add_animation(
        discarded_tile_element,
        "animate_discard",
        250,
        delay_milliseconds
    );
}

function setCallAnimation(player, action, delay_milliseconds) {
    const call_element = document.querySelector(
        `#calls_list .player_calls.player_${player} > *:last-child`
    );
    return add_animation(
        call_element,
        "animate_call",
        250,
        delay_milliseconds
    );
}

function setNewKanAnimation(player, action, delay_milliseconds) {
    const open_kan_element = document.querySelector(
        `#calls_list .player_calls.player_${player} > *:last-child`
    );
    const drawn_tile_element = document.querySelector(
        `#table_hands .table_hand_outer.player_${player} .table_hand > *:last-child`
    );
    add_animation(
        open_kan_element,
        "animate_call",
        250,
        delay_milliseconds
    );
    add_animation(
        drawn_tile_element,
        "animate_draw",
        250,
        delay_milliseconds + 250
    );
    return 500
}

function setAddKanAnimation(player, action, delay_milliseconds) {
    const add_kan_tile = document.querySelector(
        `.tile_id_${action.tile}`
    )
    const drawn_tile_element = document.querySelector(
        `#table_hands .table_hand_outer.player_${player} .table_hand > *:last-child`
    );
    add_animation(
        add_kan_tile,
        "animate_add_kan",
        250,
        delay_milliseconds
    );
    add_animation(
        drawn_tile_element,
        "animate_draw",
        250,
        delay_milliseconds + 250
    );
    return 500
}

function setFlowerAnimation(player, action, delay_milliseconds) {
    const flower_element = document.querySelector(
        `.tile_id_${action.tile}`
    );
    const flower_drawn_tile_element = document.querySelector(
        `#table_hands .table_hand_outer.player_${player} .table_hand > *:last-child`
    );
    add_animation(
        flower_element,
        "animate_call",
        250,
        delay_milliseconds
    );
    add_animation(
        flower_drawn_tile_element,
        "animate_draw",
        250,
        delay_milliseconds + 250
    );
    return 250;
}

function unsetAnimation(animated_element) {
    const classes = Array.from(animated_element.classList.values());
    animated_element.classList.remove(
        classes.filter(className => className.startsWith("animate"))
    );
}

function setAnimations(history_updates) {
    const animated_elements = document.querySelectorAll(".animate");
    for (const animated_element of animated_elements) {
        unsetAnimation(animated_element);
    }
    var delay_milliseconds = 0;
    for (const history_item of history_updates) {
        delay_milliseconds += setAnimation(
            history_item.player_index, history_item.action, delay_milliseconds);
    }
}