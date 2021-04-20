#include <iostream>

using namespace std;

int main()
{
   int arr[3];
   cout << "Enter num of elements: ";
   int x, sum = 0;
   cin >> x;

   for(int i = 0; i < x; ++i)
   {
       cout<<"Enter number "<< i + 1<<":  " ;
      cin >> arr[i];
      sum += arr[i];
   }
   cout << "Average =  " << sum / x << endl;

   return 0;
}