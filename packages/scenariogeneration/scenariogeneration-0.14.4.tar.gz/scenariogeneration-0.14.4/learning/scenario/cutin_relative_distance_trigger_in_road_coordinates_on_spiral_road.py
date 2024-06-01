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
        odr_name = "Spiral Road"
        odr = xodr.OpenDrive(odr_name)

        road_id = 0
        road_length = 300
        
        spiral_start_curvature = 10*1/road_length
        spiral_end_curvature = 10*-1/road_length
        geometry = xodr.Spiral(spiral_start_curvature, spiral_end_curvature, road_length)

        n_left_lanes = 2
        n_right_lanes = 2
        road = xodr.create_road(geometry, id=road_id, left_lanes=n_left_lanes, right_lanes=n_right_lanes)
        odr.add_road(road)
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

        # Target vehicle
        target_name = "Target"
        target_width = 2
        target_length = 5
        target_height = 1.8
        target_x_center = 2  # distance to rear axle
        target_y_center = 0
        target_z_center = ego_height / 2

        target_bounding_box = xosc.BoundingBox(target_width, target_length, target_height, target_x_center, target_y_center, target_z_center)
        target_front_axle = xosc.Axle(0.523598775598, 0.8, 1.68, 2.98, 0.4)
        target_rear_axle = xosc.Axle(0.523598775598, 0.8, 1.68, 0, 0.4)
        target_vehicle = xosc.Vehicle(
            "car_white", xosc.VehicleCategory.car, target_bounding_box, target_front_axle, target_rear_axle, 69, 10, 10
        )
        target_vehicle.add_property_file("../models/car_blue.osgb")

        # Entities
        entities = xosc.Entities()
        entities.add_scenario_object(ego_name, ego_vehicle)
        entities.add_scenario_object(target_name, target_vehicle)

        #================================================================
        # Storyboard
        #================================================================
        transition_dynamics = xosc.TransitionDynamics(
            xosc.DynamicsShapes.step, xosc.DynamicsDimension.time, 1
        )

        # Ego init action
        ego_start_position_s = 30
        ego_start_position_t = 0
        ego_start_lane_id = -2
        ego_start_road_id = 0
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
        target_start_road_id = 0
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

        # Action: change lane / cut-in
        dest_lane_id = target_start_lane_id - 1
        lane_change_duration = 2
        lane_change_action = xosc.AbsoluteLaneChangeAction(
            dest_lane_id,
            xosc.TransitionDynamics(
                xosc.DynamicsShapes.sinusoidal, xosc.DynamicsDimension.time, lane_change_duration
            )
        )

        # Entity Condition
        relative_distance = 0
        rdc = xosc.RelativeDistanceCondition(
            relative_distance, 
            xosc.Rule.greaterThan,
            xosc.RelativeDistanceType.longitudinal, 
            ego_name,
            freespace=True,
            coordinate_system=xosc.CoordinateSystem.road,
        )

        headway_time = 0
        thc = xosc.TimeHeadwayCondition(
            target_name,
            headway_time,
            xosc.Rule.greaterThan,
            freespace=True,
            distance_type=xosc.RelativeDistanceType.longitudinal,
            coordinate_system=xosc.CoordinateSystem.road
        )

        # Entity Trigger
        entity_trigger_delay = 0
        et_rdc = xosc.EntityTrigger(
            "Trigger: target's relative distance to ego in s coordinates",
            entity_trigger_delay,
            xosc.ConditionEdge.none,
            rdc,
            target_name
        )

        et_thc = xosc.EntityTrigger(
            "Trigger: ego has headway time to ego",
            entity_trigger_delay,
            xosc.ConditionEdge.none,
            thc,
            ego_name
        )

        # Event Condition / trigger Group
        cg = xosc.ConditionGroup("start")
        cg.add_condition(et_rdc)
        cg.add_condition(et_thc)

        # Event
        event = xosc.Event("Even: Target lane change", xosc.Priority.overwrite)

        event.add_action(
            "Action: lane change", 
            lane_change_action
        )
        event.add_trigger(cg)

        # Maneuver
        man = xosc.Maneuver("Maneuver: Target lane change")
        man.add_event(event)

        # Maneuver group
        mg = xosc.ManeuverGroup("Maneuver Group: Target lane change")
        mg.add_actor(target_name)
        mg.add_maneuver(man)

        # Act
        act_start_trigger_delay = 0
        act_start_condition_start_time = 0
        act_start_condition = xosc.SimulationTimeCondition(
            act_start_condition_start_time, 
            xosc.Rule.greaterThan
        )
        act_start_trigger = xosc.ValueTrigger(
            "act_start_trigger",
            act_start_trigger_delay,
            xosc.ConditionEdge.rising,
            act_start_condition,
            "start"
        )
        act = xosc.Act(
            "Act: Target lane change",
            act_start_trigger
        )
        act.add_maneuver_group(mg)
        
        # Story
        story = xosc.Story("Story: Target lane change")
        story.add_act(act)

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
        sb.add_story(story)

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
