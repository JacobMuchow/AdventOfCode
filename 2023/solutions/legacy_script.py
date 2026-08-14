import os
import runpy

from solutions.solution import Solution

class LegacyScriptSolution(Solution):
    """Adapts a pre-migration, self-contained script to the Solution interface.

    These scripts are top-level code that opens its puzzle input by bare
    filename, so they are executed with the working directory set to that
    day's resources folder. They run exactly as originally written.
    """

    def __init__(self, script_path: str, resource_dir: str):
        self.script_path = script_path
        self.resource_dir = resource_dir

    def run(self) -> None:
        prev_cwd = os.getcwd()
        os.chdir(self.resource_dir)
        try:
            runpy.run_path(self.script_path, run_name="__main__")
        finally:
            os.chdir(prev_cwd)
