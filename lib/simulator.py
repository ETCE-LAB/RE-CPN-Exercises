#!/usr/bin/env python3

import snakes.plugins
import random

# Load SNAKES with graphviz plugin for drawing
snakes.plugins.load("gv", "snakes.nets", "nets")

from nets import (
    PetriNet,
    Place,
    Transition,
    tString,
    tInteger,
    Expression,
    Variable,
    tTuple,
)


def run_once(net: PetriNet, transitions: list) -> bool:
    enabled_transitions = []
    for transition in transitions:
        modes = transition.modes()
        if modes:
            enabled_transitions.append(transition)

    if not enabled_transitions:
        return None

    chosen_transition = random.choice(enabled_transitions)

    chosen_transition.fire(random.choice(chosen_transition.modes()))

    return str(chosen_transition)


def run_simulation(net: PetriNet, transitions: list, limit=20) -> bool:

    counter = 0
    net.draw(str(net) + "-" + str(counter) + ".png")
    chosen_transition = run_once(net, transitions)
    while (chosen_transition is not None) and (counter < limit):
        print(chosen_transition)
        counter += 1
        net.draw(str(net) + "-" + str(counter) + ".png")
        chosen_transition = run_once(net, transitions)

    net.draw(str(net) + "-" + str(counter) + ".png")
    return counter
