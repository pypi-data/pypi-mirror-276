import os
from pathlib import Path
import shutil

from scenariogeneration import esmini
from scenariogeneration import ScenarioGenerator


TEST_DIR_PATH = Path(__file__).parent.resolve()
GENERATED_DIR_PATH = TEST_DIR_PATH / "generated"
SCENARIO_PARENT_DIR_PATH = GENERATED_DIR_PATH / "scenario"

ESMINI_DIR_PATH = Path("~/Downloads/esmini-demo_Linux/esmini-demo").expanduser()


def generate_scenario_dir(scenario_name):
    scenario_dir_path = SCENARIO_PARENT_DIR_PATH / scenario_name
    _rmtree_and_mkdir(scenario_dir_path)
    return scenario_dir_path

def _rmtree_and_mkdir(dir_path):
    if dir_path.exists():
        shutil.rmtree(dir_path)
    dir_path.mkdir(parents=True)

def run_esmini(scenario):
    esmini(scenario, esminipath=ESMINI_DIR_PATH)


class Esmini():
    ESMINI_BIN_DIR_PATH = ESMINI_DIR_PATH / "bin"
    ESMINI_EXE_FILE_PATH = ESMINI_BIN_DIR_PATH / "esmini"
    ODRVIEWER_EXE_FILE_PATH = ESMINI_BIN_DIR_PATH / "odrviewer"

    def __init__(self):
        pass
    
    def run_esmini(self, xosc_file_path, **kwargs):
        cmd_list = []
        
        cmd_list.append(f"{self.ESMINI_EXE_FILE_PATH}")
        
        cmd_list.append("--osc")
        cmd_list.append(f"{xosc_file_path}")
        
        cmd_list.append("--window")
        cmd_list.append("0 0 1600 900")
        
        cmd_str = " ".join(cmd_list)
        
        os.system(cmd_str)


    def run_odrviewer(self, xodr_file_path):
        cmd_list = []
        
        cmd_list.append(f"{self.ODRVIEWER_EXE_FILE_PATH}")
        
        cmd_list.append("--odr")
        cmd_list.append(f"{xodr_file_path}")
        
        cmd_list.append("--window")
        cmd_list.append("0 0 1600 900")
        
        cmd_str = " ".join(cmd_list)
        
        os.system(cmd_str)


def generate_scenario(scenario: ScenarioGenerator):
    scenario_dir_path = generate_scenario_dir(scenario.basename)
    xosc_file_str_list, xodr_file_str_list = scenario.generate(scenario_dir_path, write_relative_road_path=False)
    xosc_file_path_list = [Path(path) for path in xosc_file_str_list]
    xodr_file_path_list = [Path(path) for path in xodr_file_str_list]
    return xosc_file_path_list, xodr_file_path_list 