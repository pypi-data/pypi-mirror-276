from scenario.tunnel import Scenario
from test.conftest import *


def test_tunnel():
    scenario = Scenario()
    xosc_file_path_list, xodr_file_path_list = generate_scenario(scenario)
    Esmini().run_esmini(xosc_file_path_list[0])
    # Esmini().run_odrviewer(xodr_file_path_list[0])
    pass