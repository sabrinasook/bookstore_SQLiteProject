# Programme for bookstore clerk
import sqlite3

db = sqlite3.connect('ebookstore_db')
cursor = db.cursor()

# Create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS books(id INTEGER PRIMARY KEY, title TEXT, author TEXT, qty INTEGER)
    ''')
db.commit()

# Add books from task list
book_list = [(3001,'A Tale of Two Cities', 'Charles Dickens', 30),
             (3002,'Harry Potter and the Philosopher\'s Stone', 'J.K. Rowling', 40),
             (3003,'The Lion, the Witch and the Wardrobe', 'C.S. Lewis', 25),
             (3004,'The Lord of the Rings', 'J.R.R. Tolkien', 37),
             (3005,'Alice in Wonderland','Lewis Carroll', 12)]

try:
    cursor.executemany('''INSERT INTO books(id,title,author,qty) VALUES (?,?,?,?)''', book_list)
    db.commit()
except sqlite3.IntegrityError:
    pass

def view_db():
    cursor.execute('''SELECT * FROM books''')
    view_books = cursor.fetchall()
    print(f'\n{view_books}')

def add_book():
    id = input('Enter the book ID: ')
    try:
        id = int(id)
        pass
    except ValueError:
        id = input('ID should be a number. Please enter the book ID: ')
    title = input('Enter the book title: ')
    author = input('Enter the book author: ')
    qty = input('Enter the current book quantity: ')

    cursor.execute('''INSERT INTO books(id,title,author,qty)
    VALUES(?,?,?,?)''', (id,title,author,qty))
    db.commit()
    print('\nBook added to database.')

def update_book():
    id = int(input('Enter the ID of the book you would like to update: '))
    cursor.execute('''SELECT title, qty FROM books WHERE id = ?''',(id,))
    quant = cursor.fetchone()
    print(f'Title and current quantity: {quant}')
    update = int(input('Please enter the new book quantity: '))
    cursor.execute('''UPDATE books
    SET qty = ?
    WHERE id = ?''', (update,id))
    db.commit()
    print('\nQuantity updated.')

def delete_book():
    id = int(input('Enter the ID of the book you would like to delete: '))
    cursor.execute('''SELECT title FROM books 
    WHERE id = ?''', (id,))
    title = cursor.fetchone()
    delete = input(f'Confirm deletion of {title} - yes or no: ').lower()
    if delete == 'no':
        print('\nBook not deleted.')
        pass
    elif delete == 'yes':
        cursor.execute('''DELETE FROM books WHERE id = ?''', (id,))
        db.commit()
        print('\nBook deleted from database.')

# Search for books from database
def search_book():
    search_by = input('''What would you like to search by? 
    id - ID 
    t - Title 
    a - Author
    : ''').lower()
    if search_by == 'id':
        id = int(input('Enter the ID of the book you would like to search: '))
        cursor.execute('''SELECT * FROM books WHERE id = ?''', (id,))
        books = cursor.fetchall()
        if books == []:
            print('\nNot found in database.')
        else:
            print(books)
    elif search_by == 't':
        title = input('Enter the title of the book you would like to search: ').strip(' ')
        cursor.execute('''SELECT * FROM books WHERE title = ?''', (title,))
        books = cursor.fetchall()
        if books == []:
            print('\nNot found in database.')
        else:
            print(books)
    elif search_by == 'a':
        author = input('Enter the author of the book you would like to search: ').strip(' ')
        cursor.execute('''SELECT * FROM books WHERE author = ?''', (author,))
        books = cursor.fetchall()
        if books == []:
            print('\nNot found in database.')
        else:
            print(books)
    else:
        print('Option from list not selected')

# Present menu
while True:
    menu = input('''\nMenu:
    1 - Add book to database
    2 - Update book quantity
    3 - Delete book from database
    4 - Search database
    5 - View database
    0 - Exit
    
    x - Delete database
    : ''')

    if menu == '1':
        add_book()

    elif menu == '2':
        update_book()

    elif menu == '3':
        delete_book()

    elif menu == '4':
        search_book()

    elif menu == '5':
        view_db()

    elif menu == '0':
        print('\nGoodbye!')
        exit()

    elif menu == 'x':
       confirm = input('Confirm deletion of database - yes or no: ').lower()
       if confirm == 'no':
           print('\nDatabase not deleted.')
           pass
       elif confirm == 'yes':
           cursor.execute('''DROP TABLE books''')
           db.commit()
           print('\nDatabase deleted.')

    else:
        print('\nPlease select an option from the menu.')
        pass





