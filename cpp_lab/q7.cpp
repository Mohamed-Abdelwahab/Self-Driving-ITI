#include <iostream>

using namespace std;

class complex

{
private:
    /* data */
    double real1;
    double real2;
    double img1;
    double img2;
public:
    complex
    (/* args */);
    complex
    (double,double,double,double);
    ~complex
    ();
    void add();
};

int main() {

    double x1 , y1,x2,y2;

    cout << "Enter first real"<<"\n";
    cin >> x1;
    cout << "Enter first img"<<"\n";
    cin >> y1;
    cout << "Enter second real"<<"\n";
    cin >> x2;
    cout << "Enter second img"<<"\n";
    cin >> y2;

    complex c(x1,y1,x2,y2);

    c.add();

    return 0 ;
}

complex::complex(){};
complex::complex(double x1 , double y1,double x2 , double y2 )
{
    cout<< "numbers initialized"<<endl;
     real1 = x1 ;
     real2 = x2 ;
     img1 = y1 ;
     img2 = y2 ;

};

complex
::~complex
()
{
}

void complex
::add(){

cout<< "The sum of real part = "<< real1 + real2 <<endl;
cout<< "The sum of imaginary part = "<< img1 + img2 <<endl;

};
