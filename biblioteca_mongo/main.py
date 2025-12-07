from database import books_collection
from bson.objectid import ObjectId


def add_book():
    title = input("Título del libro: ")
    author = input("Autor: ")
    genre = input("Género: ")
    read = input("¿Leído? (s/n): ").lower() == "s"

    book = {
        "title": title,
        "author": author,
        "genre": genre,
        "read": read
    }

    books_collection.insert_one(book)
    print(" Libro agregado con éxito.\n")


def list_books():
    print("\n LISTA DE LIBROS")
    books = books_collection.find()

    for book in books:
        print(
            f"ID: {book['_id']} | "
            f"Título: {book['title']} | "
            f"Autor: {book['author']} | "
            f"Género: {book['genre']} | "
            f"Leído: {'Sí' if book['read'] else 'No'}"
        )
    print()


def update_book():
    book_id = input("ID del libro a actualizar: ")

    try:
        book = books_collection.find_one({"_id": ObjectId(book_id)})
    except:
        print(" ID inválido.\n")
        return

    if not book:
        print(" No existe un libro con ese ID.\n")
        return

    print("Deja vacío si no quieres cambiar el campo.")

    new_title = input(f"Nuevo título ({book['title']}): ")
    new_author = input(f"Nuevo autor ({book['author']}): ")
    new_genre = input(f"Nuevo género ({book['genre']}): ")
    read_input = input(f"¿Leído? (s/n) actual ({'sí' if book['read'] else 'no'}): ").lower()

    update_fields = {}

    if new_title:
        update_fields["title"] = new_title
    if new_author:
        update_fields["author"] = new_author
    if new_genre:
        update_fields["genre"] = new_genre
    if read_input in ("s", "n"):
        update_fields["read"] = read_input == "s"

    books_collection.update_one(
        {"_id": ObjectId(book_id)},
        {"$set": update_fields}
    )

    print(" Libro actualizado.\n")


def delete_book():
    book_id = input("ID del libro a eliminar: ")

    try:
        result = books_collection.delete_one({"_id": ObjectId(book_id)})
    except:
        print(" ID inválido.\n")
        return

    if result.deleted_count > 0:
        print(" Libro eliminado.\n")
    else:
        print(" No existe un libro con ese ID.\n")


def search_books():
    term = input("Buscar por título, autor o género: ")

    query = {
        "$or": [
            {"title": {"$regex": term, "$options": "i"}},
            {"author": {"$regex": term, "$options": "i"}},
            {"genre": {"$regex": term, "$options": "i"}},
        ]
    }

    results = books_collection.find(query)

    print("\n🔎 RESULTADOS")
    found = False

    for book in results:
        found = True
        print(
            f"ID: {book['_id']} | "
            f"Título: {book['title']} | "
            f"Autor: {book['author']} | "
            f"Género: {book['genre']} | "
            f"Leído: {'Sí' if book['read'] else 'No'}"
        )

    if not found:
        print("No se encontraron coincidencias.\n")

    print()


def menu():
    while True:
        print("""
======== MENÚ BIBLIOTECA =========
1. Agregar libro
2. Actualizar libro
3. Eliminar libro
4. Ver lista de libros
5. Buscar libros
6. Salir
=================================
""")
        option = input("Seleccione una opción: ")

        if option == "1":
            add_book()
        elif option == "2":
            update_book()
        elif option == "3":
            delete_book()
        elif option == "4":
            list_books()
        elif option == "5":
            search_books()
        elif option == "6":
            print(" Saliendo del programa...")
            break
        else:
            print(" Opción inválida.\n")


if __name__ == "__main__":
    menu()
