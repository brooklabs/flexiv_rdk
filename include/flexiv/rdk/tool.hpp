/**
 * @file tool.hpp
 * @copyright Copyright (C) 2016-2024 Flexiv Ltd. All Rights Reserved.
 */

#ifndef FLEXIV_RDK_TOOL_HPP_
#define FLEXIV_RDK_TOOL_HPP_

#include "robot.hpp"

namespace flexiv {
namespace rdk {

/**
 * @class Tool
 * @brief Interface to online update and interact with the robot tools. All updates will take effect
 * immediately without a power cycle. However, the robot must be in IDLE mode when applying changes.
 */
class Tool
{
public:
    /**
     * @brief [Non-blocking] Create an instance and initialize the interface.
     * @param[in] robot Reference to the instance of flexiv::rdk::Robot.
     * @throw std::runtime_error if the initialization sequence failed.
     */
    Tool(const Robot& robot);
    virtual ~Tool();

    /**
     * @brief [Blocking] Get a name list of all configured tools.
     * @return Tool names as a string list.
     * @throw std::runtime_error if failed to get a reply from the connected robot.
     * @note This function blocks until a reply is received.
     */
    const std::vector<std::string> list() const;

    /**
     * @brief [Blocking] Get name of the tool that the robot is currently using.
     * @return Name of the current tool. Return "Flange" if there's no active tool.
     * @throw std::runtime_error if failed to get a reply from the connected robot.
     * @note This function blocks until a reply is received.
     */
    const std::string name() const;

    /**
     * @brief [Blocking] Whether the specified tool already exists.
     * @param[in] name Name of the tool to check.
     * @return True if the specified tool exists.
     * @throw std::runtime_error if failed to get a reply from the connected robot.
     * @note This function blocks until a reply is received.
     */
    bool exist(const std::string& name) const;

    /**
     * @brief [Blocking] Get parameters of the tool that the robot is currently using.
     * @return Parameters result.
     * @throw std::runtime_error if failed to get a reply from the connected robot.
     * @note This function blocks until a reply is received.
     */
    const ToolParams params() const;

    /**
     * @brief [Blocking] Get parameters of an existing tool.
     * @param[in] name Name of the tool to get parameters for, must be an existing one.
     * @return Parameters result.
     * @throw std::logic_error if the specified tool does not exist.
     * @throw std::runtime_error if failed to get a reply from the connected robot.
     * @note This function blocks until a reply is received.
     */
    const ToolParams params(const std::string& name) const;

    /**
     * @brief [Blocking] Add a new tool with user-specified parameters.
     * @param[in] name Name of the new tool, must be unique.
     * @param[in] params Parameters of the new tool.
     * @throw std::logic_error if robot is not in the correct control mode or the specified tool
     * already exists.
     * @throw std::runtime_error if failed to deliver the request to the connected robot.
     * @note Applicable control modes: IDLE.
     * @note This function blocks until the request is successfully delivered.
     */
    void Add(const std::string& name, const ToolParams& params);

    /**
     * @brief [Blocking] Switch to an existing tool. All following robot operations will default to
     * use this tool.
     * @param[in] name Name of the tool to switch to, must be an existing one.
     * @throw std::logic_error if robot is not in the correct control mode or the specified tool
     * does not exist.
     * @throw std::runtime_error if failed to deliver the request to the connected robot.
     * @note Applicable control modes: IDLE.
     * @note This function blocks until the request is successfully delivered.
     */
    void Switch(const std::string& name);

    /**
     * @brief [Blocking] Update the parameters of an existing tool.
     * @param[in] name Name of the tool to update, must be an existing one.
     * @param[in] params New parameters for the specified tool.
     * @throw std::logic_error if robot is not in the correct control mode or the specified tool
     * does not exist.
     * @throw std::runtime_error if failed to deliver the request to the connected robot.
     * @note Applicable control modes: IDLE.
     * @note This function blocks until the request is successfully delivered.
     */
    void Update(const std::string& name, const ToolParams& params);

    /**
     * @brief [Blocking] Remove an existing tool.
     * @param[in] name Name of the tool to remove, must be an existing one but cannot be "Flange".
     * @throw std::logic_error if robot is not in the correct control mode or the specified tool
     * does not exist or trying to remove "Flange".
     * @throw std::runtime_error if failed to deliver the request to the connected robot.
     * @note Applicable control modes: IDLE.
     * @note This function blocks until the request is successfully delivered.
     */
    void Remove(const std::string& name);

private:
    class Impl;
    std::unique_ptr<Impl> pimpl_;
};

} /* namespace rdk */
} /* namespace flexiv */

#endif /* FLEXIV_RDK_TOOL_HPP_ */
