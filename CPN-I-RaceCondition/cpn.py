import snakes.plugins

# Load SNAKES with graphviz plugin for drawing
snakes.plugins.load("gv", "snakes.nets", "nets")

from lib import simulator

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


def create_petrinet():
    # Create a Petri net
    net = PetriNet("RaceCondition")

    # Add places with initial markings
    net.add_place(Place("Filesystem", [("file1.txt", "some random text--")], tTuple))
    net.add_place(Place("Program_wants_to_read", [1, 2], tInteger))  # Two programs
    net.add_place(Place("Program_has_read", []))
    net.add_place(Place("Program_has_written", [], tInteger))

    # Add transitions
    transitions = [
        Transition("ReadFile"),
        Transition("WriteFile", Expression("pid_and_file[1][0] == file[0]")),
    ]

    for transition in transitions:
        net.add_transition(transition)

    # Add arcs
    # Program requests read
    net.add_input("Program_wants_to_read", "ReadFile", Variable("pid"))
    # Read content from file
    net.add_input("Filesystem", "ReadFile", Variable("file"))
    # Store read data with program ID
    net.add_output("Program_has_read", "ReadFile", Expression("(pid, file)"))
    net.add_output("Filesystem", "ReadFile", Expression("file"))

    # Program ready to write
    net.add_input("Program_has_read", "WriteFile", Variable("pid_and_file"))
    net.add_input("Filesystem", "WriteFile", Variable("file"))
    # Append program's data and write back
    net.add_output(
        "Filesystem",
        "WriteFile",
        Expression(("(file[0], str(pid_and_file[1][1] + str(pid_and_file[0])))")),
    )
    # Mark program as finished writing
    net.add_output("Program_has_written", "WriteFile", Expression("pid_and_file[0]"))

    return net, transitions


(net, transitions) = create_petrinet()

simulator.run_simulation(
    net, transitions, limit=20
)  # Limit the maximum number of transition firings to avoid infinite loops
