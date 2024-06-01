from scenario.constant_speed import Scenario
from test.conftest import *


def test_straight_road():
    scenario = Scenario()
    xosc_file_path_list, xodr_file_path_list = generate_scenario(scenario)
    Esmini().run_esmini(xosc_file_path_list[0])
    pass
