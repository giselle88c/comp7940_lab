#MASTER

# user 1 
# user 2 - 3 -4

# user 1 - commit 2,3
def main():
    print("hello world")

def Ex1(factor):
    x=factor

    for i in range(x+1):
        if(i!=0):
            if x%i==0:
                print(i,end=" ")
    print()
#user 2 commit2

if __name__ == '__main__':
    main()
    l = [52633, 8137, 1024, 999]
    for fact in l:
        Ex1(fact)
