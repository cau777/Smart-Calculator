# Smart-Calculator
 A simple calculator in Python that supports basic operations, variable and parenthesis. It uses postfix notation, stacks and dictionaries.
 I made this project for JetBrains Academy

# How to convert infix to postfix
* Add operands (numbers and variables) to the result (postfix notation) as they arrive.
* If the stack is empty or contains a left parenthesis on top, push the incoming operator on the stack.
* If the incoming operator has higher precedence than the top of the stack, push it on the stack.
* If the precedence of the incoming operator is lower than or equal to that of the top of the stack, pop the stack and add operators to the result until you see an operator that has smaller precedence or a left parenthesis on the top of the stack; then add the incoming operator to the stack.
* If the incoming element is a left parenthesis, push it on the stack.
* If the incoming element is a right parenthesis, pop the stack and add operators to the result until you see a left parenthesis. Discard the pair of parentheses.
* At the end of the expression, pop the stack and add all operators to the result.
