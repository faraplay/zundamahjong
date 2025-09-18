function setAnimation(player, action) {
    console.log(player, action);
    switch (action.action_type) {
        case ACTION_DISCARD:
            const discarded_tile_element = document.querySelector(
                `#discard_pool .player_discards.player_${player} > *:last-child`
            );
            discarded_tile_element.classList.add("animate");
            discarded_tile_element.classList.add("animate_discard");
            break;
    }
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
    for (const history_item of history_updates) {
        setAnimation(history_item.player_index, history_item.action);
    }
}