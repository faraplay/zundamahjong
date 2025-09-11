const actions_div = document.getElementById('actions');
const actions_disambiguation_div = document.getElementById('actions_disambiguation');

function sendAction(e, action) {
    e.preventDefault();
    disableActions();
    socket.emit('action', my_player, action, () => {
        actions_div.classList.add('hidden');
    });
}

function createDisambiguationActionButtonElement(action, last_discard) {
    const action_item = document.createElement('button');
    action_item.type = "button";
    action_item.classList.add('disambig_action_button');
    switch (action.action_type) {
        case ACTION_CHI_A:
            for (const tile of [last_discard, last_discard + 1, last_discard + 2]) {
                action_item.appendChild(createStraightTileElement(tile))
            }
            break;
        case ACTION_CHI_B:
            for (const tile of [last_discard - 1, last_discard, last_discard + 1]) {
                action_item.appendChild(createStraightTileElement(tile))
            }
            break;
        case ACTION_CHI_C:
            for (const tile of [last_discard - 2, last_discard - 1, last_discard]) {
                action_item.appendChild(createStraightTileElement(tile))
            }
            break;
        case ACTION_ADD_KAN:
        case ACTION_CLOSED_KAN:
        case ACTION_FLOWER:
            action_item.appendChild(createStraightTileElement(action.tile))
            break;
    }
    action_item.addEventListener('click', (e) => sendAction(e, action))
    return action_item;
}

function createActionSupertypeElement(action_supertype) {
    const action_supertype_item = document.createElement('button');
    action_supertype_item.type = "button";
    action_supertype_item.classList.add('action_button');
    action_supertype_item.classList.add(`action_${action_supertype}`);
    const supertype = action_supertype_strings[action_supertype];
    action_supertype_item.dataset.text = supertype;
    const text_item = document.createElement('div');
    text_item.classList.add('action_button_text');
    text_item.textContent = supertype;
    action_supertype_item.appendChild(text_item);
    return action_supertype_item;
}

function createActionDisambiguationElement(actions, last_discard) {
    const disambig_item = document.createElement('div');
    disambig_item.classList.add('hidden');
    disambig_item.classList.add('disambig_div');
    const text_item = document.createElement('div');
    text_item.classList.add('disambig_text');
    text_item.textContent = "Select an option";
    disambig_item.appendChild(text_item);
    if (actions[0].action_type <= ACTION_CHI_C) {
        actions.sort((a, b) => b.action_type - a.action_type);
    } else {
        actions.sort((a, b) => a.tile - b.tile);
    }
    for (const action of actions) {
        disambig_item.appendChild(
            createDisambiguationActionButtonElement(action, last_discard)
        );
    }
    return disambig_item;
}

function setActions(actions, last_discard) {
    actions_div.replaceChildren();
    actions_div.classList.remove('hidden');
    actions_disambiguation_div.replaceChildren();
    if (actions.length <= 1) {
        return;
    }
    const action_supertypes_dict = {};
    for (const action of actions) {
        const action_supertype = action_supertypes[action.action_type];
        if (action_supertype == 0) {
            continue;
        }
        if (!action_supertypes_dict[action_supertype]) {
            action_supertypes_dict[action_supertype] = [];
        }
        action_supertypes_dict[action_supertype].push(action);
    }

    const keys = Object.keys(action_supertypes_dict).sort((a, b) => b - a);
    for (const key of keys) {
        const action_supertype_item = createActionSupertypeElement(key);
        const supertype_actions = action_supertypes_dict[key];
        if (supertype_actions.length > 1) {
            const disambig_item =
                createActionDisambiguationElement(supertype_actions, last_discard);
            actions_disambiguation_div.appendChild(disambig_item);
            action_supertype_item.addEventListener('click',
                (e) => {
                    e.preventDefault();
                    actions_div.classList.add('hidden');
                    disambig_item.classList.remove('hidden');
                }
            )
        } else {
            const action = supertype_actions[0];
            action_supertype_item.addEventListener('click',
                (e) => sendAction(e, action)
            )
        }
        actions_div.appendChild(action_supertype_item);
    }
    // for (var i=7; i>=1; --i) {
    //     actions_div.appendChild(createActionSupertypeElement(i));
    // }
}
