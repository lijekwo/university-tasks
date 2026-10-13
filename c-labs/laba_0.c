#include <stdio.h>
#include <math.h>

double read_number(char name){
    double number;
    int scan_result;
    int symbol;

    while (1){
        printf("введите коэффицент %c: ", name);
        scan_result = scanf("%lf", &number);
        symbol = ' ';

        if (scan_result == 1){
            symbol = getchar();
            if (symbol == '\n'){
                return number;
            }
        }

        fputs("ошибка! введите число\n",stderr);

        while (symbol != '\n'){
            symbol = getchar();
        }
    }
}

int main(){
    double coeff_a, coeff_b, coeff_c, discriminant, x, x1, x2;
    int repeat = 1;
    char answer;

    while (repeat == 1){
        puts("давайте решим квадратное уравнение вида ax^2+bx+c=0");
        coeff_a = read_number('a');
        coeff_b = read_number('b');
        coeff_c = read_number('c');

        if (coeff_a == 0 && coeff_b == 0 && coeff_c == 0){
            puts("любое число может быть решением");
        } else if (coeff_a == 0 && coeff_b == 0){
            puts("нет решений");
        } else if (coeff_a == 0){
            x = -coeff_c/coeff_b;
            if (x == 0){ 
                x = 0;
            }
            printf("уравнение линейное, x = %.4lf\n",x);
        } else {
            discriminant = coeff_b * coeff_b - 4 * coeff_a * coeff_c;
            if (discriminant < 0){
                puts("нет корней");
            } else if (discriminant == 0){
                x = -coeff_b/(2*coeff_a);
                if (x == 0){
                    x = 0;
                }
                printf("x = %.4lf\n",x);
            } else {
                x1 = (-coeff_b + sqrt(discriminant))/(2 * coeff_a);
                x2 = (-coeff_b - sqrt(discriminant))/(2 * coeff_a);
                if (x1 == 0){
                    x1 = 0;
                }
                if (x2 == 0){
                    x2 = 0;
                }
                printf("x1 = %.4lf, x2 = %.4lf\n",x1,x2);
            }
        }

        puts("продолжим? (y/n): ");
        scanf(" %c", &answer);

        if (answer == 'y' || answer == 'Y'){
            repeat = 1;
        } else {
            repeat = 0;
        }
    }
    return 0;
}