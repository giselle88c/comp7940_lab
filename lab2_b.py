#Write a Python function that can reverse a string.

def reverse_string(myText):
  newText="".join(list(myText)[::-1])

  return newText

print(reverse_string("Hello, my name is ..."))