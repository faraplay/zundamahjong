function add_animation(element, animation_style, duration_milliseconds, delay_milliseconds) {
    element.classList.add("animate");
    animation = element.style.getPropertyValue("animation");
    if (animation) {
        animation = ",\n" + animation;
    }
    element.style.setProperty(
        "animation",
        `${animation_style} ${duration_milliseconds}ms ease-out `
        + `${delay_milliseconds}ms 1 normal both`
        + animation
    )
    return duration_milliseconds;
}

function setDrawAnimation(player, action, delay_milliseconds) {
    const drawn_tile_element = document.querySelector(
        `#table_hands .table_hand_outer.player_${player} .table_hand > *:last-child`
    );
    return add_animation(
        drawn_tile_element,
        "drawAnimation",
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
        "discardAnimation",
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
        "callAnimation",
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
        "callAnimation",
        250,
        delay_milliseconds
    );
    add_animation(
        drawn_tile_element,
        "drawAnimation",
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
        "addKanAnimation",
        250,
        delay_milliseconds
    );
    add_animation(
        drawn_tile_element,
        "drawAnimation",
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
        "callAnimation",
        250,
        delay_milliseconds
    );
    add_animation(
        flower_drawn_tile_element,
        "drawAnimation",
        250,
        delay_milliseconds + 250
    );
    return 500;
}

function setWinAnimation(player, action, delay_milliseconds) {
    const win_hand_element = document.querySelector(
        `.table_hand_outer.player_${player} .table_hand`
    );
    add_animation(
        win_hand_element,
        "winAnimation",
        500,
        delay_milliseconds
    );
    add_animation(
        win_info,
        "showAnimation",
        0,
        delay_milliseconds + 1000
    )
    return 1000;
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
        case ACTION_RON:
        case ACTION_TSUMO:
            return setWinAnimation(player, action, delay_milliseconds);
        default:
            return 0;
    }
}

function unsetAnimation(animated_element) {
    const classes = Array.from(animated_element.classList.values());
    animated_element.classList.remove(
        classes.filter(className => className.startsWith("animate"))
    );
    animated_element.style.setProperty("animation", "");
}

function setAnimations(history_updates) {
    const animated_elements = document.querySelectorAll(".animate");
    for (const animated_element of animated_elements) {
        unsetAnimation(animated_element);
    }
    let delay_milliseconds = 0;
    for (const history_item of history_updates) {
        delay_milliseconds += setAnimation(
            history_item.player_index, history_item.action, delay_milliseconds);
    }
}