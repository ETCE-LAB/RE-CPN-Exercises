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
    tBoolean,
)


def create_petrinet():
    # Create a Petri net
    net = PetriNet("ChargingStation")

    # Add places with initial markings
    net.add_place(Place("DriverHasBoughtEnergy", [True], tBoolean))
    net.add_place(Place("DriverWantsToChargeEV", [True], tBoolean))
    net.add_place(Place("ChargingPortIsFree", [(1, 10, 30), (2, 30, 50)]))
    net.add_place(Place("EV_ReadyToCharge", [(1, 10, 50), (2, 15, 20)]))
    net.add_place(Place("DriverHasReservedCP", []))
    net.add_place(Place("DriverHasChargedEV", []))

    net.add_place(Place("ChargingSpeedAgreed", []))
    net.add_place(Place("EV_HasBegunCharging", []))

    # Add transitions
    transitions = [
        Transition("ReserveCP", Expression("paid and wants")),
        Transition(
            "AgreeOnChargingSpeed",
            Expression("(ev_cp[0][2] >= ev_cp[1][1]) and (ev_cp[1][2]>=ev_cp[0][1])"),
        ),
        Transition(
            "ChargingSpeedIncompatible",
            Expression("(ev_cp[0][2] < ev_cp[1][1]) or (ev_cp[1][2] < ev_cp[0][1])"),
        ),
        Transition("BeginCharging"),
        Transition("EndCharging"),
    ]

    for transition in transitions:
        net.add_transition(transition)

    # Add arcs

    net.add_input("DriverHasBoughtEnergy", "ReserveCP", Variable("paid"))
    net.add_output("DriverHasBoughtEnergy", "ReserveCP", Expression("paid"))
    net.add_input("DriverWantsToChargeEV", "ReserveCP", Variable("wants"))
    net.add_output("DriverWantsToChargeEV", "ReserveCP", Expression("wants"))
    net.add_input("ChargingPortIsFree", "ReserveCP", Variable("cp"))

    net.add_input("EV_ReadyToCharge", "ReserveCP", Variable("ev"))
    net.add_output("DriverHasReservedCP", "ReserveCP", Expression("(ev, cp)"))

    net.add_input("DriverWantsToChargeEV", "AgreeOnChargingSpeed", Variable("wants"))
    net.add_input("DriverHasReservedCP", "AgreeOnChargingSpeed", Variable("ev_cp"))
    net.add_output("DriverWantsToChargeEV", "AgreeOnChargingSpeed", Expression("wants"))
    net.add_output(
        "ChargingSpeedAgreed",
        "AgreeOnChargingSpeed",
        Expression(
            "(ev_cp[0], ev_cp[1],(ev_cp[1][2] if ev_cp[1][2] < ev_cp[0][2] else ev_cp[0][2]))"
        ),
    )

    net.add_input("DriverHasReservedCP", "ChargingSpeedIncompatible", Variable("ev_cp"))
    net.add_output(
        "ChargingPortIsFree", "ChargingSpeedIncompatible", Expression("ev_cp[1]")
    )
    net.add_output(
        "EV_ReadyToCharge", "ChargingSpeedIncompatible", Expression("ev_cp[0]")
    )

    net.add_input("ChargingSpeedAgreed", "BeginCharging", Variable("cp_ev_speed"))
    net.add_output("EV_HasBegunCharging", "BeginCharging", Expression("cp_ev_speed"))

    net.add_input("EV_HasBegunCharging", "EndCharging", Variable("cp_ev_speed"))
    net.add_output("DriverHasChargedEV", "EndCharging", Expression("cp_ev_speed[1]"))
    net.add_output("ChargingPortIsFree", "EndCharging", Expression("cp_ev_speed[0]"))

    return net, transitions


(net, transitions) = create_petrinet()

simulator.run_simulation(
    net, transitions, limit=30
)  # Limit the maximum number of transition firings to avoid infinite loops
