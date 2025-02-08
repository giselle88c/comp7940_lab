#MASTER

# user 1

def main():
    print("hello world")

def Ex1(factor):
    x=factor

    for i in range(x+1):
        if(i!=0):
            if x%i==0:
                print(i,end=" ")
    print()


if __name__ == '__main__':
    main()
    l = [52633, 8137, 1024, 999]
    for fact in l:
        Ex1(fact)
