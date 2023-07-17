#include <stdio.h>
void swap(int *a,int *b){
    int temp = *a;
    *a = *b;
    *b = temp;
}

int main(){
    int x = 2;
    int y = 3;
    swap(&x,&y);
    printf("%d,%d",x,y);
}
