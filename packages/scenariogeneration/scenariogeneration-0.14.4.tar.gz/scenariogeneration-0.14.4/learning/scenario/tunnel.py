from scenariogeneration import xodr
from scenariogeneration import xosc
from scenariogeneration import ScenarioGenerator

AUTHOR = "Alexander Bükk"

class Scenario(ScenarioGenerator):
    def __init__(self):
        ScenarioGenerator.__init__(self)
        self.naming = "parameter"
    
    def road(self, **kwargs):
        odr_name = "Road with tunnel"
        odr = xodr.OpenDrive(odr_name)
        
        road_id = 0
        road_length = 500
        road = xodr.create_road(xodr.Line(road_length), id=road_id)
        road.add_tunnel(
            xodr.Tunnel(s=20, length=30, id="1", name="My Tunnel")
        )
        odr.add_road(road)
        odr.adjust_roads_and_lanes() # Always needed!
        
        return odr
    
    def scenario(self, **kwargs):
        paramdec = xosc.ParameterDeclarations()
        
        road = xosc.RoadNetwork(roadfile=self.road_file)
        
        catalog = xosc.Catalog()
        
        #================================================================
        # Entities
        #================================================================
        entities = xosc.Entities()
        
        # Ego
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
            "car_white", xosc.VehicleCategory.car, ego_bounding_box, ego_front_axle, ego_rear_axle, 69, 10, 10
        )
        ego_vehicle.add_property_file("../models/car_white.osgb")
        ego_vehicle.add_property("model_id", "0")
        
        entities.add_scenario_object(ego_name, ego_vehicle)
        
        # target_name = "Target"
        
        
        #================================================================
        # Entities
        #================================================================
        
        init = xosc.Init()
        step_time = xosc.TransitionDynamics(
            xosc.DynamicsShapes.step, xosc.DynamicsDimension.time, 1
        )
        
        ego_start_position_s = 25
        ego_start_position_t = 0
        ego_start_lane_id = -1  # right lane
        ego_start_road_id = 0
        ego_start_teleport_action = xosc.TeleportAction(
            xosc.LanePosition(
                ego_start_position_s, 
                ego_start_position_t, 
                ego_start_lane_id, 
                ego_start_road_id
            )
        )
        
        ego_init_speed = 0
        ego_init_speed_action = xosc.AbsoluteSpeedAction(ego_init_speed, step_time)
        
        init.add_init_action(ego_name, ego_start_teleport_action)
        init.add_init_action(ego_name, ego_init_speed_action)

        sb = xosc.StoryBoard(
            init,
            xosc.ValueTrigger(
                "Stop simulation",
                3,
                xosc.ConditionEdge.rising,
                xosc.SimulationTimeCondition(
                    10,
                    xosc.Rule.greaterThan
                ),
                "stop"
            ),
        )
        
        story = xosc.Story("Ego drives with a constant speed")
        
        act = xosc.Act(
            "Constant speed act",
            xosc.ValueTrigger(
                "act_start_trigger",
                0,
                xosc.ConditionEdge.rising,
                xosc.SimulationTimeCondition(0, xosc.Rule.greaterThan)
            )
        )
        mg = xosc.ManeuverGroup("Ego constant speed maneuvers")
        mg.add_actor(ego_name)
        man = xosc.Maneuver("ego man")
        event = xosc.Event("Ego speed change to constant speed", xosc.Priority.overwrite)
        action = xosc.AbsoluteSpeedAction(
            50 / 3.6,
            xosc.TransitionDynamics(
                xosc.DynamicsShapes.linear,
                xosc.DynamicsDimension.time,
                5,
            ),
        )
        event.add_action("change speed action", action)
        trigger = xosc.ValueTrigger(
            "event_start_trigger",
            1.2,
            xosc.ConditionEdge.rising,
            xosc.SimulationTimeCondition(0, xosc.Rule.greaterThan),
        )
        event.add_trigger(trigger)
        man.add_event(event)
        mg.add_maneuver(man)
        act.add_maneuver_group(mg)
        
        story.add_act(act)
        
        sb.add_story(story)
        
        scenario_name = "Constant Speed"
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