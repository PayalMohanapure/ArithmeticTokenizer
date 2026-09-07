%{
#include <stdio.h>
%}

DIGIT     [0-9]
ID        [a-zA-Z_][a-zA-Z0-9_]*

%%

{DIGIT}+"."{DIGIT}+   { printf("%-15s FLOAT\n", yytext); }
{DIGIT}+              { printf("%-15s INTEGER\n", yytext); }
{ID}                  { printf("%-15s IDENTIFIER\n", yytext); }
"+"                   { printf("%-15s PLUS\n", yytext); }
"-"                   { printf("%-15s MINUS\n", yytext); }
"*"                   { printf("%-15s MULTIPLY\n", yytext); }
"/"                   { printf("%-15s DIVIDE\n", yytext); }
"%"                   { printf("%-15s MODULO\n", yytext); }
"^"                   { printf("%-15s POWER\n", yytext); }
"("                   { printf("%-15s LPAREN\n", yytext); }
")"                   { printf("%-15s RPAREN\n", yytext); }
"="                   { printf("%-15s ASSIGN\n", yytext); }
[ \t]+                { /* ignore whitespace */ }
\n                    { /* ignore newline */ }
.                     { printf("%-15s ERROR: invalid character\n", yytext); }

%%

int main(int argc, char **argv) {
    yylex();
    return 0;
}

int yywrap() {
    return 1;
}
