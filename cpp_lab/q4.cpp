#include <iostream>

using namespace std;

int main() {

    int arr[5];
   cout << "Enter number 1: ";
   cin >> arr[0];

   double max = 0;
   max = arr[0];

   for(int i = 1; i < 100; ++i)
    {
        cout<<"Enter number "<< i + 1<<":  " ;
    
        cin >> arr[i];
        if (arr[i] > max)
        {
            max = arr[i];

        }
        
        }
 
    cout << "Largest element = " << max <<"\n";
   
    return 0 ;
}