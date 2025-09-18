function setAnimation(player, action, delay_milliseconds) {
    console.log(player, action);
    let duration_milliseconds;
    switch (action.action_type) {
        case ACTION_DRAW:
            duration_milliseconds = 250;
            const drawn_tile_element = document.querySelector(
                `#table_hands .table_hand_outer.player_${player} .table_hand > *:last-child`
            );
            drawn_tile_element.classList.add("animate");
            drawn_tile_element.classList.add("animate_draw");
            drawn_tile_element.style.setProperty("--animation-duration", `${duration_milliseconds}ms`);
            drawn_tile_element.style.setProperty("--animation-delay", `${delay_milliseconds}ms`);
            break;
        case ACTION_DISCARD:
            duration_milliseconds = 250;
            const discarded_tile_element = document.querySelector(
                `#discard_pool .player_discards.player_${player} > *:last-child`
            );
            discarded_tile_element.classList.add("animate");
            discarded_tile_element.classList.add("animate_discard");
            discarded_tile_element.style.setProperty("--animation-duration", `${duration_milliseconds}ms`);
            discarded_tile_element.style.setProperty("--animation-delay", `${delay_milliseconds}ms`);
            break;
        case ACTION_CHI_A:
        case ACTION_CHI_B:
        case ACTION_CHI_C:
        case ACTION_PON:
        case ACTION_OPEN_KAN:
            duration_milliseconds = 250;
            const call_element = document.querySelector(
                `#calls_list .player_calls.player_${player} > *:last-child`
            );
            call_element.classList.add("animate");
            call_element.classList.add("animate_call");
            call_element.style.setProperty("--animation-duration", `${duration_milliseconds}ms`);
            call_element.style.setProperty("--animation-delay", `${delay_milliseconds}ms`);
            break;
    }
    return duration_milliseconds;
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