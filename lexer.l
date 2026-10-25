%{
#include <stdio.h>
#include <string.h>

int line_num = 1;

void count_newlines(const char *str) {
    while (*str) {
        if (*str == '\n') line_num++;
        str++;
    }
}
%}

DIGIT       [0-9]
HEX_DIGIT   [0-9a-fA-F]
LETTER      [a-zA-Z_]
ID          {LETTER}({LETTER}|{DIGIT})*

%%

\r\n|\n                 { line_num++; }
[ \t\r]+                { /* ignore whitespace */ }

"//".*                  { printf("%-5d\t%-20s\t%s\n", line_num, "COMMENT", yytext); }
"/*"([^*]|\*+[^*/])*\*+"/" { 
                            printf("%-5d\t%-20s\t%s\n", line_num, "COMMENT", yytext); 
                            count_newlines(yytext); 
                        }

#[ \t]*(include|define|undef|ifdef|ifndef|if|else|elif|endif|pragma) {
    printf("%-5d\t%-20s\t%s\n", line_num, "PREPROCESSOR", yytext);
}

"<"[a-zA-Z0-9_./\\]+">" {
    printf("%-5d\t%-20s\t%s\n", line_num, "HEADER_FILE", yytext);
}

\"([^\"\\]|\\.)*\"      { 
                            printf("%-5d\t%-20s\t%s\n", line_num, "STRING_LITERAL", yytext); 
                            count_newlines(yytext); 
                        }

\'([^\'\\]|\\.)*\'      { 
                            printf("%-5d\t%-20s\t%s\n", line_num, "CHAR_LITERAL", yytext); 
                        }

"auto"|"break"|"case"|"char"|"const"|"continue"|"default"|"do"|"double"|"else"|"enum"|"extern"|"float"|"for"|"goto"|"if"|"inline"|"int"|"long"|"register"|"restrict"|"return"|"short"|"signed"|"sizeof"|"static"|"struct"|"switch"|"typedef"|"union"|"unsigned"|"void"|"volatile"|"while" {
    printf("%-5d\t%-20s\t%s\n", line_num, "KEYWORD", yytext);
}

0[xX]{HEX_DIGIT}+       { printf("%-5d\t%-20s\t%s\n", line_num, "INTEGER", yytext); }
{DIGIT}+"."{DIGIT}+([eE][+-]?{DIGIT}+)? { printf("%-5d\t%-20s\t%s\n", line_num, "FLOAT", yytext); }
{DIGIT}+[eE][+-]?{DIGIT}+               { printf("%-5d\t%-20s\t%s\n", line_num, "FLOAT", yytext); }
{DIGIT}+                { printf("%-5d\t%-20s\t%s\n", line_num, "INTEGER", yytext); }

{ID}                    { printf("%-5d\t%-20s\t%s\n", line_num, "IDENTIFIER", yytext); }

"++"                    { printf("%-5d\t%-20s\t%s\n", line_num, "INC_OP", yytext); }
"--"                    { printf("%-5d\t%-20s\t%s\n", line_num, "DEC_OP", yytext); }
"->"                    { printf("%-5d\t%-20s\t%s\n", line_num, "ARROW", yytext); }

"<<"                    { printf("%-5d\t%-20s\t%s\n", line_num, "LEFT_SHIFT", yytext); }
">>"                    { printf("%-5d\t%-20s\t%s\n", line_num, "RIGHT_SHIFT", yytext); }
"<="                    { printf("%-5d\t%-20s\t%s\n", line_num, "LE_OP", yytext); }
">="                    { printf("%-5d\t%-20s\t%s\n", line_num, "GE_OP", yytext); }
"=="                    { printf("%-5d\t%-20s\t%s\n", line_num, "EQ_OP", yytext); }
"!="                    { printf("%-5d\t%-20s\t%s\n", line_num, "NE_OP", yytext); }
"&&"                    { printf("%-5d\t%-20s\t%s\n", line_num, "LOGICAL_AND", yytext); }
"||"                    { printf("%-5d\t%-20s\t%s\n", line_num, "LOGICAL_OR", yytext); }

"+="                    { printf("%-5d\t%-20s\t%s\n", line_num, "ADD_ASSIGN", yytext); }
"-="                    { printf("%-5d\t%-20s\t%s\n", line_num, "SUB_ASSIGN", yytext); }
"*="                    { printf("%-5d\t%-20s\t%s\n", line_num, "MUL_ASSIGN", yytext); }
"/="                    { printf("%-5d\t%-20s\t%s\n", line_num, "DIV_ASSIGN", yytext); }
"%="                    { printf("%-5d\t%-20s\t%s\n", line_num, "MOD_ASSIGN", yytext); }

"+"                     { printf("%-5d\t%-20s\t%s\n", line_num, "PLUS", yytext); }
"-"                     { printf("%-5d\t%-20s\t%s\n", line_num, "MINUS", yytext); }
"*"                     { printf("%-5d\t%-20s\t%s\n", line_num, "MULTIPLY", yytext); }
"/"                     { printf("%-5d\t%-20s\t%s\n", line_num, "DIVIDE", yytext); }
"%"                     { printf("%-5d\t%-20s\t%s\n", line_num, "MODULO", yytext); }
"^"                     { printf("%-5d\t%-20s\t%s\n", line_num, "BIT_XOR", yytext); }
"="                     { printf("%-5d\t%-20s\t%s\n", line_num, "ASSIGN", yytext); }
"<"                     { printf("%-5d\t%-20s\t%s\n", line_num, "LT_OP", yytext); }
">"                     { printf("%-5d\t%-20s\t%s\n", line_num, "GT_OP", yytext); }
"!"                     { printf("%-5d\t%-20s\t%s\n", line_num, "LOGICAL_NOT", yytext); }
"&"                     { printf("%-5d\t%-20s\t%s\n", line_num, "BIT_AND", yytext); }
"|"                     { printf("%-5d\t%-20s\t%s\n", line_num, "BIT_OR", yytext); }
"~"                     { printf("%-5d\t%-20s\t%s\n", line_num, "BIT_NOT", yytext); }
"?"                     { printf("%-5d\t%-20s\t%s\n", line_num, "QUESTION", yytext); }
":"                     { printf("%-5d\t%-20s\t%s\n", line_num, "COLON", yytext); }
"."                     { printf("%-5d\t%-20s\t%s\n", line_num, "DOT", yytext); }

"("                     { printf("%-5d\t%-20s\t%s\n", line_num, "LPAREN", yytext); }
")"                     { printf("%-5d\t%-20s\t%s\n", line_num, "RPAREN", yytext); }
"{"                     { printf("%-5d\t%-20s\t%s\n", line_num, "LBRACE", yytext); }
"}"                     { printf("%-5d\t%-20s\t%s\n", line_num, "RBRACE", yytext); }
"["                     { printf("%-5d\t%-20s\t%s\n", line_num, "LBRACKET", yytext); }
"]"                     { printf("%-5d\t%-20s\t%s\n", line_num, "RBRACKET", yytext); }
";"                     { printf("%-5d\t%-20s\t%s\n", line_num, "SEMICOLON", yytext); }
","                     { printf("%-5d\t%-20s\t%s\n", line_num, "COMMA", yytext); }

.                       { printf("%-5d\t%-20s\t%s\n", line_num, "ERROR", yytext); }

%%

int main(int argc, char **argv) {
    yylex();
    return 0;
}

int yywrap() {
    return 1;
}
