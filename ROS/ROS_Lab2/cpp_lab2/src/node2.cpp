// include ros client library and message types 
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include "std_msgs/msg/int64.hpp"
#include "cpp_lab2/msg/myinfo.hpp"


using std::placeholders::_1;

class MinimalSubscriber : public rclcpp::Node
{
  public:
    MinimalSubscriber()
    : Node("sub_node")
    {
       //create subscriber object
      subscription_ = this->create_subscription<cpp_lab2::msg::Myinfo>(
      "topic2", 10, std::bind(&MinimalSubscriber::topic_callback, this, _1));
       //create publisher object
      pub = this->create_publisher<std_msgs::msg::Int64>("int_fb", 10);
    }

  private:
    // define callback function
    void topic_callback(const cpp_lab2::msg::Myinfo::SharedPtr msg) const
    {
      RCLCPP_INFO(this->get_logger(), "Counter = '%d'", msg->num);
      // define message of type int
      auto x = std_msgs::msg::Int64();
      // fill fields of the message
      x.data = msg->num ;
      //publish the message
      pub->publish(x);

      
    }
    //decleration of subscriber 
    rclcpp::Subscription<cpp_lab2::msg::Myinfo>::SharedPtr subscription_;
    //decleration of publisher 
    rclcpp::Publisher<std_msgs::msg::Int64>::SharedPtr pub;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<MinimalSubscriber>());
  rclcpp::shutdown();
  return 0;
}