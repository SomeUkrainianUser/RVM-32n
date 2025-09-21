#include "lexer.h"
#include <string.h>

typedef enum { 
  TOKEN_INT,
  TOKEN_RPAR,
  TOKEN_LPAR,
  TOKEN_EQ,
  TOKEN_GT,
  TOKEN_LT,
  TOKEN_IF,
  TOKEN_ELSE,
  TOKEN_IF,
  TOKEN_SEMICOLON
} TokenType;


