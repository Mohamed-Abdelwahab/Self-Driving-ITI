#include <iostream>

using namespace std;

class my_class

{
private:
    /* data */
public:
    my_class
    (/* args */);
    my_class
    (double,double);
    ~my_class
    ();
};



int main() {

    double x , y;

    cout << "Enter first number"<<"\n";
    cin >> x;
    cout << "Enter second number"<<"\n";
    cin >> y;

    my_class c(x,y);

    return 0 ;
}

my_class::my_class(){};
my_class::my_class(double x , double y )
{
    cout<< "numbers initialized"<<endl;
    cout<< "The addition result is " << x + y << endl;

};

my_class
::~my_class
()
{
}