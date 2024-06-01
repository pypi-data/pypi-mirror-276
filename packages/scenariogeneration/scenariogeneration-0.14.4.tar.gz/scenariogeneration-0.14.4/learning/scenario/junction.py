import numpy as np
from scenariogeneration import xodr
from scenariogeneration import xosc
from scenariogeneration import ScenarioGenerator

from pathlib import Path

AUTHOR = "Alexander Bükk"

class Scenario(ScenarioGenerator):
    def __init__(self):
        ScenarioGenerator.__init__(self)
        self.naming = "parameter"

    def road(self, **kwargs):
        odr_name = "Junction"
        odr = xodr.OpenDrive(odr_name)
        
        road1 = xodr.create_road(xodr.Line(100), id=1, left_lanes=2, right_lanes=2)
        road2 = xodr.create_road(xodr.Line(50), id=2, left_lanes=2, right_lanes=2)
        road3 = xodr.create_road(xodr.Line(25), id=3, left_lanes=2, right_lanes=2)

        junction_creator = xodr.CommonJunctionCreator(id=100, name="my_junction", startnum=100)
        junction_creator.add_incoming_road_cartesian_geometry(
            road1, x=-10, y=0, heading=0, road_connection="successor"
        )
        junction_creator.add_incoming_road_cartesian_geometry(
            road2, x=10, y=0, heading=np.pi, road_connection="predecessor"
        )
        junction_creator.add_incoming_road_cartesian_geometry(
            road3, x=10, y=10, heading=-2/4*np.pi, road_connection="predecessor"
        )

        junction_creator.add_connection(road_one_id=1, road_two_id=2)
        junction_creator.add_connection(road_one_id=1, road_two_id=3)

        odr.add_road(road1)
        odr.add_road(road2)
        odr.add_road(road3)
        odr.add_junction_creator(junction_creator)
        
        odr.adjust_roads_and_lanes() # Always needed!
        return odr

    def scenario(self, **kwargs):
        #================================================================
        # Params and references
        #================================================================
        paramdec = xosc.ParameterDeclarations()
        road = xosc.RoadNetwork(roadfile=self.road_file)
        catalog = xosc.Catalog()

        #================================================================
        # Entities
        #================================================================
        # Ego vehicle
        ego_name, ego_vehicle = _create_ego()

        # Target vehicle
        target_name, target_vehicle = _create_target()
        
        # Entities
        entities = xosc.Entities()
        entities.add_scenario_object(ego_name, ego_vehicle)
        entities.add_scenario_object(target_name, target_vehicle)

        #================================================================
        # Storyboard
        #================================================================
        sb = _create_storyboard_with_init(ego_name, target_name)

        scenario_name = Path(__file__).stem
        sce = xosc.Scenario(
            name=scenario_name,
            author=AUTHOR,
            parameters=paramdec,
            entities=entities,
            storyboard=sb,
            roadnetwork=road,
            catalog=catalog,
        )
        return sce


def _create_ego():
    ego_name = "Ego"
    ego_width = 2
    ego_length = 5
    ego_height = 1.8
    ego_x_center = 2  # distance to rear axle
    ego_y_center = 0
    ego_z_center = ego_height / 2

    ego_bounding_box = xosc.BoundingBox(ego_width, ego_length, ego_height, ego_x_center, ego_y_center, ego_z_center)
    ego_front_axle = xosc.Axle(0.523598775598, 0.8, 1.68, 2.98, 0.4)
    ego_rear_axle = xosc.Axle(0.523598775598, 0.8, 1.68, 0, 0.4)
    ego_vehicle = xosc.Vehicle(
        "car_red", xosc.VehicleCategory.car, ego_bounding_box, ego_front_axle, ego_rear_axle, 69, 10, 10
    )
    ego_vehicle.add_property_file("../models/car_red.osgb")
    return ego_name, ego_vehicle


def _create_target():
    target_name = "Target"
    target_width = 2
    target_length = 5
    target_height = 1.8
    target_x_center = 2  # distance to rear axle
    target_y_center = 0
    target_z_center = target_height / 2

    target_bounding_box = xosc.BoundingBox(target_width, target_length, target_height, target_x_center, target_y_center, target_z_center)
    target_front_axle = xosc.Axle(0.523598775598, 0.8, 1.68, 2.98, 0.4)
    target_rear_axle = xosc.Axle(0.523598775598, 0.8, 1.68, 0, 0.4)
    target_vehicle = xosc.Vehicle(
        "car_white", xosc.VehicleCategory.car, target_bounding_box, target_front_axle, target_rear_axle, 69, 10, 10
    )
    target_vehicle.add_property_file("../models/car_blue.osgb")
    return target_name, target_vehicle


def _create_storyboard_with_init(ego_name, target_name):
    transition_dynamics = xosc.TransitionDynamics(
            xosc.DynamicsShapes.step, xosc.DynamicsDimension.time, 1
        )

    # Ego init action
    ego_start_position_s = 30
    ego_start_position_t = 0
    ego_start_lane_id = -2
    ego_start_road_id = 1
    ego_start_teleport_action = xosc.TeleportAction(
        xosc.LanePosition(
            ego_start_position_s, 
            ego_start_position_t, 
            ego_start_lane_id, 
            ego_start_road_id
        )
    )

    ego_init_speed = 50 / 3.6
    ego_init_speed_action = xosc.AbsoluteSpeedAction(ego_init_speed, transition_dynamics)

    # Target init action
    transition_dynamics = xosc.TransitionDynamics(
        xosc.DynamicsShapes.step, xosc.DynamicsDimension.time, 1
    )

    target_start_position_s = 5
    target_start_position_t = 0
    target_start_lane_id = ego_start_lane_id + 1
    target_start_road_id = 1
    target_start_teleport_action = xosc.TeleportAction(
        xosc.LanePosition(
            target_start_position_s, 
            target_start_position_t, 
            target_start_lane_id, 
            target_start_road_id
        )
    )

    target_init_speed = 70 / 3.6
    target_init_speed_action = xosc.AbsoluteSpeedAction(target_init_speed, transition_dynamics)

    # Init
    init = xosc.Init()
    init.add_init_action(ego_name, ego_start_teleport_action)
    init.add_init_action(ego_name, ego_init_speed_action)
    init.add_init_action(target_name, target_start_teleport_action)
    init.add_init_action(target_name, target_init_speed_action)


    # Storyboard
    sim_stop_trigger_delay = 0
    sim_stop_condition_end_time = 10
    sim_stop_trigger = xosc.ValueTrigger(
        "Stop simulation",
        sim_stop_trigger_delay,
        xosc.ConditionEdge.rising,
        xosc.SimulationTimeCondition(
            sim_stop_condition_end_time,
            xosc.Rule.greaterThan
        ),
        "stop"
    )
    sb = xosc.StoryBoard(
        init,
        sim_stop_trigger
    )
    return sb
