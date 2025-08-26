# 1.Importar librerias 

import os
os.system("cls")
from typing import List
import json

# 2.Creation of the book class

class Book:
    def __init__(self,title_: str,author: str,year_: int,available_: bool=True):
        self.title_ = title_
        self.author = author
        self.year_ = year_
        self.available_ = available_
    
    def __repr__(self) -> str:
        return f'{self.title_} - {self.author} ({self.year_}) - {"[Available]" if self.available_ else "[On loan]"}'
    

    # 3. Creation of the user class

class User:
    def __init__(self,name:str):
        self.name_ = name
        self.books_on_loan: List[Book] = []
    
    def to_dict(self)-> dict:
        return {
            'nombre':self.name_,
            'books_loan': [book.title_ for book in self.books_on_loan]
            }
    
    def __repr__(self):
        return f"User({self.name_}, libros={[b.title_ for b in self.books_on_loan]})"
    
# Creation of the library class

class Library:
    def __init__(self, file_: str = "books.json"):
        self.file_ = file_
        self.books: List[Book] = self.load_books()
        self.users: List[User] = []

#========================================================================================================

    def load_books(self):
        try:
            with open(self.file_, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [Book(**book) for book in data] # Los asteriscos ** sirven para usar los valores del diccionario como args del Book.
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []
        
#========================================================================================================
        
    def save_books(self):
        with open(self.file_, "w", encoding="utf-8") as f:
            json.dump([book.__dict__ for book in self.books],f, indent=4, ensure_ascii=False)

#========================================================================================================
    
    def add_book(self, book: Book):
        for b in self.books:
            if b.title_.lower() == book.title_.lower() and b.author.lower() == book.author.lower():
                print(f'{book.title_} ya fue agregado a la Library')
                return
        self.books.append(book)

#========================================================================================================

    def search_for_title(self, title: str) -> List[Book]:
        return [book for book in self.books if title.lower() in book.title_.lower() ]
    
#========================================================================================================

    def search_for_author(self, author: str) -> List[Book]:
        return [book for book in self.books if author.lower()  in book.author.lower() ]
    
#========================================================================================================

    def lend_a_book(self, user: str, title: str):
        # Buscar si el libro esta disponible 
        book = next((b for b in self.books if b.title_ == title and b.available_),None)
        if not book:
            print(f'❌ El libro: {title} no esta disponible!')
            return

        # Buscar usuario ya registrado 
        user_ = next((u for u in self.users if u.name_.lower() == user.lower()),None)
        if not user_:
            user_ = User(user)
            self.users.append(user_)
            print(f'👤 Usuario {user_.name_} registrado!')
        
        #Prestar el libro 
        user_.books_on_loan.append(book)
        book.available_ = False
        print(f'Se ha prestado el libro "{title}" a {user_.name_}')

#========================================================================================================

    def return_book(self, user: str, title:str):

        user_ = next((u for u in self.users if u.name_.lower() == user.lower()),None)
        if not user_:
            print(f"❌ El usuario '{user}' no existe en el sistema.")
            return

        book = next((b for b in self.books if b.title_.lower() == title.lower()),None)
        if not book:
            print(f'El usuario: {user} no tiene el libro {title}')
            return
        
        # Devolver libro 
        if len(user_.books_on_loan) <= 0:
            print("Este usuario no tiene ningun libro en prestamo")
            return 
        
        user_.books_on_loan.remove(book)
        book.available_ = True
        print(f'El libro "{book.title_}" ha sido devuelto por {user_.name_}.')

#========================================================================================================



# MENU PRINCIPAL

def menu():
    my_library = Library()
    my_library.load_books()
    my_library.save_books()
    user = input("Ingresa tu nombre para acceder a la Biblioteca: ")

    while True:
        print("\n=== MENÚ BIBLIOTECA ===")
        print("1. Ver libros disponibles")
        print("2. Buscar por título")
        print("3. Buscar por autor")
        print("4. Prestar libro")
        print("5. Devolver libro")
        print("6. Salir")

        option : int = int(input('Ingresa una opción: '))

        if option == 1:
            for book in my_library.books:
                if book.available_ == True:
                    print(book)
        elif option == 2:
            title = input('Ingresa el libro a buscar: ')
            results = my_library.search_for_title(title)
            if results:
                print("Resultados:")
                for book in results:
                    print(book)
            else:
                print('❌ No se encontró ningún libro con ese título.')
        elif option == 3:
            author = input('Ingresa el autor a bucar: ')
            results = my_library.search_for_author(author)
            if results:
                print("Resultados:")
                for book in results:
                    print(book)
            else:
                print('❌ No se encontró ningún libro con ese título.')
        elif option == 4:
            book = input('Que libro deceas llevarte? ')
            my_library.lend_a_book(user,book)
        elif option == 5:
            book = input(f'Hola {user}, que libro deceas regresar? ')
            my_library.return_book(user,book)
        elif option == 6:
            print('Saliedo...')
            break
        else: print('Por favor seleccione una opcion valida!')

if __name__ == "__main__":
    menu()
