#include "ContactPlugin.hh"

#include "ros/ros.h"
#include "std_msgs/String.h"

#include <sstream>


#include <functional>
#include <gazebo/gazebo.hh>
#include <gazebo/physics/physics.hh>
#include <gazebo/common/common.hh>
#include <ignition/math/Vector3.hh>
#include <thread>

#include "ros/callback_queue.h"
#include "ros/subscribe_options.h"
#include "std_msgs/Float32.h"
#include <gazebo/transport/transport.hh>
#include <gazebo/msgs/msgs.hh>

// #include <node_handle.h>

using namespace gazebo;
GZ_REGISTER_SENSOR_PLUGIN(ContactPlugin)



// http://classic.gazebosim.org/tutorials?tut=contact_sensor&cat=sensors

// int argc = 0;
// char **argv = NULL;
// ros::init(argc, argv, "talker");
// ros::NodeHandle n;
// ros::Publisher chatter_pub = n.advertise<std_msgs::String>("chatter", 1000);
// ros::Rate loop_rate(10);


/////////////////////////////////////////////////
ContactPlugin::ContactPlugin() : SensorPlugin(){}

/////////////////////////////////////////////////
ContactPlugin::~ContactPlugin(){}

/////////////////////////////////////////////////
void ContactPlugin::Load(sensors::SensorPtr _sensor, sdf::ElementPtr /*_sdf*/)
{


  // Get the parent sensor.
  this->parentSensor =
    std::dynamic_pointer_cast<sensors::ContactSensor>(_sensor);

  // Make sure the parent sensor is valid.
  if (!this->parentSensor)
  {
    gzerr << "ContactPlugin requires a ContactSensor.\n";
    return;
  }
  // Connect to the sensor update event.
  this->updateConnection = this->parentSensor->ConnectUpdated(
      std::bind(&ContactPlugin::OnUpdate, this));

  // Make sure the parent sensor is active.
  this->parentSensor->SetActive(true);



// ************** INICIO - INICIALIZACION TOPICOS DE ROS ************************

// Initialize ros, if it has not already bee initialized.
  if (!ros::isInitialized())
  {
    std::cout << "Nodo ROS no inicializadoooooooooooooooo! " << "\n";
    int argc = 0;
    char **argv = NULL;
    ros::init(argc, argv, "collision_rosnode",
        ros::init_options::NoSigintHandler);
  }
  // Create our ROS node. This acts in a similar manner to
  // the Gazebo node
  this->rosNode.reset(new ros::NodeHandle("collision_rosnode"));

  this->chatter_pub = this->rosNode->advertise<std_msgs::Float32>("cantColisiones", 1);
  // this->chatter_pub = this->rosNode.advertise<std_msgs::String>("chatter", 1000);
  // this->chatter_pub = this->rosNode(ros::NodeHandle::advertise<std_msgs::String>("chatter", 1000));

  // ros::Rate loop_rate(10);

  // ros::Publisher chatter_pub = rosNode.advertise<std_msgs::String>("chatter", 1000);
  // ros::Rate loop_rate(10);

// ************** FIN - INICIALIZACION TOPICOS DE ROS ************************
  

}
/////////////////////////////////////////////////
void ContactPlugin::OnUpdate()
{

  // Get all the contacts.
  msgs::Contacts contacts;
  contacts = this->parentSensor->Contacts();

  // for (unsigned int i = 0; i < contacts.contact_size(); ++i)
  // {
  //   std::cout << "Collision between[" << contacts.contact(i).collision1()
  //             << "] and [" << contacts.contact(i).collision2() << "]\n";

  //   for (unsigned int j = 0; j < contacts.contact(i).position_size(); ++j)
  //   {
  //     std::cout << j << "  Position:"
  //               << contacts.contact(i).position(j).x() << " "
  //               << contacts.contact(i).position(j).y() << " "
  //               << contacts.contact(i).position(j).z() << "\n";
  //     std::cout << "   Normal:"
  //               << contacts.contact(i).normal(j).x() << " "
  //               << contacts.contact(i).normal(j).y() << " "
  //               << contacts.contact(i).normal(j).z() << "\n";
  //     std::cout << "   Depth:" << contacts.contact(i).depth(j) << "\n";
  //   }
  // }

  //  *************** INICIO - PARTE DE ROS ******************

  // EJEMPLO PARA IMPRIMIR STRING, PARA A FUTURO DESARROLLAR DETALLE DE COLISION
  // std_msgs::String msg;
  // std::stringstream ss;
  // ss << "hello world " << 1;
  // msg.data = ss.str();
  // ROS_INFO("%s", msg.data.c_str());
  // this->chatter_pub.publish(msg);
  // ros::spinOnce();
  // this->loop_rate.sleep();

  // PARA IMPRIMIR CUANTAS COLISIONES SE DIERON:
  float colisiones=10000;
  std_msgs::Float32 msg;
  colisiones= contacts.contact_size();

  if(colisiones>0){
    std::cout << "Cantidad de colisiones: "<< contacts.contact_size() << "\n";
  }
  
  msg.data = colisiones;
  this->chatter_pub.publish(msg);
  ros::spinOnce();
  ros::Rate loop_rate(5);
  loop_rate.sleep();
  // this->loop_rate.sleep();

//  *************** FIN - PARTE DE ROS ******************

}