from learning.scenario.cutin_relative_distance_trigger_in_road_coordinates import Scenario
from learning.test.conftest import *


def test_run():
    scenario = Scenario()
    xosc_file_path_list, xodr_file_path_list = generate_scenario(scenario)
    Esmini().run_esmini(xosc_file_path_list[0])
    pass