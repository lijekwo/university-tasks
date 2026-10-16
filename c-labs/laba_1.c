#include <stdio.h>
#include <limits.h>
#include <math.h>
 
#define BASE 10
#define MAX_DIGIT (BASE - 1)
#define MAX_SUM (2 * MAX_DIGIT)
#define MAX_N ((int)(sizeof(long long) * CHAR_BIT))
#define REPEAT_KEY 'y'
#define SYMBOLS 6
 
int isDigit(int symbol){
    return symbol >= '0' && symbol <= '9';
}
 
int isLetter(int symbol){
    return (symbol >= 'a' && symbol <= 'z') || (symbol >= 'A' && symbol <= 'Z');
}
 
int nextChar(){
    int symbol = getchar();
    while (symbol == ' ' || symbol == '\t' || symbol == '\r'){
        symbol = getchar();
    }
    return symbol;
}
 
int main(){
    long long pascalTriangle[MAX_N][MAX_N];
    long long coef, big;
    int symbol;
    int firstArg, secondArg;
    int answer;
    int limit = 0;
    int power;
    int bad, cnt;
    int position;
    int row, col;
    int termIndex;
    int firstExp, secondExp;
    int cellWidth;
    int printed, zeros;

    big = 1;
    while (big <= LLONG_MAX / MAX_SUM){
        big = big * MAX_SUM;
        limit++;
    }
 
    do{
        fputs("Введите выражение вида (a + b) ^ n: ", stdout);
 
        symbol = nextChar();
        if (symbol == EOF){
            break;
        }
 
        bad = 0;
        firstArg = 0;
        secondArg = 0;
        power = 0;
 
        if (symbol != '('){
            bad = 1;
        }
 
        for (position = 1; position < SYMBOLS && bad == 0; position++){
            symbol = nextChar();
            if (symbol == '\n' || symbol == EOF){
                bad = 1;
            } else if (position == 1){
                firstArg = symbol;
            } else if (position == 2 && symbol != '+'){
                bad = 1;
            } else if (position == 3){
                secondArg = symbol;
            } else if (position == 4 && symbol != ')'){
                bad = 1;
            } else if (position == 5 && symbol != '^'){
                bad = 1;
            }

            if (bad == 0 && (position == 1 || position == 3) && isDigit(symbol)){
                symbol = getchar();
                if (symbol == '.' || symbol == ','){
                    zeros = 0;
                    symbol = getchar();
                    while (symbol == '0'){
                        zeros++;
                        symbol = getchar();
                    }
                    if (zeros == 0 || isDigit(symbol)){
                        bad = 3;
                    }
                }
                if (bad == 0){
                    ungetc(symbol, stdin);
                }
            }
        }
 
        if (bad == 0){
            cnt = 0;
            symbol = nextChar();
            while (isDigit(symbol)){
                if (power <= limit){
                    power = power * BASE + (symbol - '0');
                }
                cnt++;
                symbol = getchar();
            }

            if (cnt > 0 && (symbol == '.' || symbol == ',')){
                zeros = 0;
                symbol = getchar();
                while (symbol == '0'){
                    zeros++;
                    symbol = getchar();
                }
                if (zeros == 0 || isDigit(symbol)){
                    bad = 3;
                }
            }
 
            while (symbol == ' ' || symbol == '\t' || symbol == '\r'){
                symbol = getchar();
            }
 
            if (bad == 0){
                if (cnt == 0 || (symbol != '\n' && symbol != EOF)){
                    bad = 1;
                } else if (power > limit){
                    bad = 2;
                }
            }
        }
 
        while (symbol != '\n' && symbol != EOF){
            symbol = getchar();
        }
 
        if (bad == 1){
            fputs("Ошибка: неверный формат. Пример: (6 + a) ^ 7\n", stderr);
        } else if (bad == 3){
            fputs("Ошибка: дробная часть должна быть нулевой (можно 1.0 или 1,0, нельзя 1.5)\n", stderr);
        } else if (!(isDigit(firstArg) || isLetter(firstArg)) || !(isDigit(secondArg) || isLetter(secondArg))){
            fputs("Ошибка: аргумент - это одна цифра или одна буква\n", stderr);
        } else if (isLetter(firstArg) && firstArg == secondArg){
            fputs("Ошибка: буквы должны быть разными\n", stderr);
        } else if (bad == 2){
            fputs("Ошибка: n слишком большое\n", stderr);
            printf("Допустимо: n от 0 до %d\n", limit);
        } else{

            for (row = 0; row <= power; row++){
                pascalTriangle[row][0] = 1;
                pascalTriangle[row][row] = 1;
                for (col = 1; col < row; col++){
                    pascalTriangle[row][col] = pascalTriangle[row - 1][col - 1] + pascalTriangle[row - 1][col];
                }
            }

            cellWidth = 1;
            coef = pascalTriangle[power][power / 2];
            while (coef >= BASE){
                coef = coef / BASE;
                cellWidth++;
            }
            cellWidth++;
 
            puts("\nТреугольник Паскаля:");
            for (row = 0; row <= power; row++){
                printf("%*s", (power - row) * cellWidth / 2, "");
                for (col = 0; col <= row; col++){
                    printf("%*lld", cellWidth, pascalTriangle[row][col]);
                }
                puts("");
            }
 
            printf("\n(%c + %c) ^ %d = ", firstArg, secondArg, power);
 
            if (isDigit(firstArg) && isDigit(secondArg)){
                coef = 1;
                for (termIndex = 1; termIndex <= power; termIndex++){
                    coef = coef * ((firstArg - '0') + (secondArg - '0'));
                }
                printf("%lld", coef);
            } else{
                printed = 0;
                for (termIndex = 0; termIndex <= power; termIndex++){
                    coef = pascalTriangle[power][termIndex];
                    firstExp = 0;
                    secondExp = 0;
 
                    if (isDigit(firstArg)){
                        coef = coef * llround(pow(firstArg - '0', power - termIndex));
                    } else{
                        firstExp = power - termIndex;
                    }
 
                    if (isDigit(secondArg)){
                        coef = coef * llround(pow(secondArg - '0', termIndex));
                    } else{
                        secondExp = termIndex;
                    }
 
                    if (coef != 0){
                        if (printed == 1){
                            fputs(" + ", stdout);
                        }
 
                        if (coef != 1 || (firstExp == 0 && secondExp == 0)){
                            printf("%lld", coef);
                        }
 
                        if (firstExp > 0){
                            printf("%c", firstArg);
                            if (firstExp > 1){
                                printf("^%d", firstExp);
                            }
                        }
 
                        if (secondExp > 0){
                            printf("%c", secondArg);
                            if (secondExp > 1){
                                printf("^%d", secondExp);
                            }
                        }
 
                        printed = 1;
                    }
                }
 
                if (printed == 0){
                    fputs("0", stdout);
                }
            }
            puts("");
        }
 
        printf("\nПовторить? (%c - да, иначе выход): ", REPEAT_KEY);
        answer = nextChar();
        symbol = answer;
        while (symbol != '\n' && symbol != EOF){
            symbol = getchar();
        }
    } while (answer == REPEAT_KEY);
 
    return 0;
}