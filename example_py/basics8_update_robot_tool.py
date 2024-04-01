#!/usr/bin/env python

"""basics8_update_robot_tool.py

This tutorial shows how to online update and interact with the robot tools. All changes made to 
the robot tool system will take effect immediately without needing to reboot. However, the robot 
must be put into IDLE mode when making these changes.
"""

__copyright__ = "Copyright (C) 2016-2023 Flexiv Ltd. All Rights Reserved."
__author__ = "Flexiv"

import time
import argparse

# Import Flexiv RDK Python library
# fmt: off
import sys
sys.path.insert(0, "../lib_py")
import flexivrdk
# fmt: on


def print_description():
    """
    Print tutorial description.

    """
    print(
        "This tutorial shows how to online update and interact with the robot tools. All "
        "changes made to the robot tool system will take effect immediately without needing to "
        "reboot. However, the robot must be put into IDLE mode when making these changes."
    )
    print()


def main():
    # Program Setup
    # ==============================================================================================
    # Parse arguments
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "robot_sn",
        help="Serial number of the robot to connect to. Remove any space, for example: Rizon4s-123456",
    )
    args = argparser.parse_args()

    # Define alias
    log = flexivrdk.Log()
    mode = flexivrdk.Mode

    # Print description
    log.Info("Tutorial description:")
    print_description()

    try:
        # RDK Initialization
        # ==========================================================================================
        # Instantiate robot interface
        robot = flexivrdk.Robot(args.robot_sn)

        # Clear fault on the connected robot if any
        if robot.fault():
            log.Warn("Fault occurred on the connected robot, trying to clear ...")
            # Try to clear the fault
            if not robot.ClearFault():
                log.Error("Fault cannot be cleared, exiting ...")
                return 1
            log.Info("Fault on the connected robot is cleared")

        # Enable the robot, make sure the E-stop is released before enabling
        log.Info("Enabling robot ...")
        robot.Enable()

        # Wait for the robot to become operational
        while not robot.operational():
            time.sleep(1)

        log.Info("Robot is now operational")

        # Update Robot Tool
        # ==========================================================================================
        # Make sure the robot is in IDLE mode
        robot.SwitchMode(mode.IDLE)

        # Instantiate tool interface
        tool = flexivrdk.Tool(robot)

        # Get and print a list of already configured tools currently in the robot's tools pool
        log.Info("All configured tools:")
        tool_list = tool.list()
        for i in range(len(tool_list)):
            print("[" + str(i) + "]", tool_list[i])
        print()

        # Get and print the current active tool
        log.Info("Current active tool: " + tool.name())

        # Set name and parameters for a new tool
        new_tool_name = "ExampleTool1"
        new_tool_params = flexivrdk.ToolParams()
        new_tool_params.mass = 0.9
        new_tool_params.CoM = [0.0, 0.0, 0.057]
        new_tool_params.inertia = [2.768e-03, 3.149e-03, 5.64e-04, 0.0, 0.0, 0.0]
        new_tool_params.tcp_location = [
            0.0,
            -0.207,
            0.09,
            0.7071068,
            0.7071068,
            0.0,
            0.0,
        ]

        # If there's already a tool with the same name in the robot's tools pool, then remove it
        # first, because duplicate tool names are not allowed
        if tool.exist(new_tool_name):
            log.Warn(
                "Tool with the same name ["
                + new_tool_name
                + "] already exists, removing it now"
            )
            # Switch to other tool or no tool (Flange) before removing the current tool
            tool.Switch("Flange")
            tool.Remove(new_tool_name)

        # Add the new tool
        log.Info("Adding new tool [" + new_tool_name + "] to the robot")
        tool.Add(new_tool_name, new_tool_params)

        # Get and print the tools list again, the new tool should appear at the end
        log.Info("All configured tools:")
        tool_list = tool.list()
        for i in range(len(tool_list)):
            print("[" + str(i) + "]", tool_list[i])
        print()

        # Switch to the newly added tool, i.e. set it as the active tool
        log.Info("Switching to tool [" + new_tool_name + "]")
        tool.Switch(new_tool_name)

        # Get and print the current active tool again, should be the new tool
        log.Info("Current active tool: " + tool.name())

        # Switch to other tool or no tool (Flange) before removing the current tool
        tool.Switch("Flange")

        # Clean up by removing the new tool
        time.sleep(2)
        log.Info("Removing tool [" + new_tool_name + "]")
        tool.Remove(new_tool_name)

        log.Info("Program finished")

    except Exception as e:
        log.Error(str(e))


if __name__ == "__main__":
    main()