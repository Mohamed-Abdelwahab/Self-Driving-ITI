// 1) include ros client library and message types 
#include <chrono>
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include "cpp_lab2/msg/myinfo.hpp"


using namespace std::chrono_literals;

// 2) Create class that inherit from rcl::Node calss
class Node1 : public rclcpp::Node
{
  public:
// 4) Inside class constructor define( node name(uniqe), publisher , timer )
    Node1(): Node("minimal_publisher")
    { 
      //create publisher object this->create_publisher<msg type>("topic_name",queue_size)
      publisher_ = this->create_publisher<cpp_lab2::msg::Myinfo>("topic2", 10);
      // create timer to control publishing rate 
      timer_ = this->create_wall_timer(1000ms, std::bind(&Node1::timer_callback, this));
    }

//3)Inside private declare (Publisher , Subscriber , Timer , Counter , callbacks , services ,..)
  private:
    // 1) define callback function
    void timer_callback()
    {
      //step(1):create message object
      auto message = cpp_lab2::msg::Myinfo();
      //step(2):fill message members
      message.data = "Mohamed Abdelwahab is publishing: " + std::to_string(count_++);
      message.num = count_ ;
      // print statement
      RCLCPP_INFO(this->get_logger(), "Mohamed Abdelwahab is publishing:  '%d'", message.num);
      //step(3):publish the message
      publisher_->publish(message);
    }

    // 2)create timer pointer / placeholder
    rclcpp::TimerBase::SharedPtr timer_;
    // 3)create publisher pointer / placeholder
    rclcpp::Publisher<cpp_lab2::msg::Myinfo>::SharedPtr publisher_;
    size_t count_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<Node1>());
  rclcpp::shutdown();
  return 0;
}