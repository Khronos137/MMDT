cmake_minimum_required(VERSION 2.8.3)

project(mmdt_rat20)

## Add support for C++11, supported in ROS Kinetic and newer
add_definitions(-std=c++11)

find_package(catkin REQUIRED COMPONENTS
  roscpp 
  gazebo_ros 
)
 
# Depend on system install of Gazebo
find_package(gazebo REQUIRED)

link_directories(${GAZEBO_LIBRARY_DIRS})
include_directories(${Boost_INCLUDE_DIR} ${catkin_INCLUDE_DIRS} ${GAZEBO_INCLUDE_DIRS})

# For model_mass_plugin plugin
# add_library(model_mass_plugin plugins/model_mass.cc)
# target_link_libraries(model_mass_plugin ${catkin_LIBRARIES} ${GAZEBO_LIBRARIES})
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${GAZEBO_CXX_FLAGS}")

add_library(contact SHARED plugins/ContactPlugin.cc)
target_link_libraries(contact ${GAZEBO_LIBRARIES})

catkin_package(
	DEPENDS
		roscpp
		gazebo_ros
)

find_package(roslaunch)

foreach(dir config launch meshes urdf)
	install(DIRECTORY ${dir}/
		DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/${dir})
endforeach(dir)
