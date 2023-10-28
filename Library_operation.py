class Library:
    def __init__(self, books):
        self.books=books
    
    def list_books(self):
        for book in self.books:
            print(book)
    
    def remove_book(self,book_name):
        if(book_name in self.books):
            print('!!! Get your '+book_name+' book now !!!')
            self.books.remove(book_name)
        else:
            print("Please enter available book\n")
    
    def receive_book(self, book_name):
        self.books.append(book_name)

book_list=['Java', 'C', 'C++']    
lib1=Library(book_list)
print(lib1.books)
msg="""
    1. Display Book list
    2. Borrow Book
    3. Return Book
""" 

while True:
    print(msg)
    input_choice = int(input("Enter the  choice:"))

    if(input_choice==1):
        print("\nAvailable books are:")
        lib1.list_books()
    elif(input_choice==2):
        book_name=input("Enter the book name:")
        lib1.remove_book(book_name)
    elif(input_choice==3):
        book_name=input("Enter the book name:")
        lib1.receive_book(book_name)
    else:
        print("\nThank you, come again !!!")
        quit()
    

