import ptj_lex

code = """\
class ? Factorial(ArithmeticOperation):
 def factorial(self, x):
  if x == 0 or x is 1 :
   return 1
  else:
   return factorial(x-1)*
factorial = Factorial()
print "And the result is:", str(factorial.factorial(3*3+3))
"""

if __name__ == "__main__":
    ptj_lex.ptj_lexer.input(code)
    for token in ptj_lex.ptj_lexer:
        print str(token)

