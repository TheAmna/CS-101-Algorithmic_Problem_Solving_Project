import datetime

# LIST OF HU IDS NAMED ids_list
ids_list = ["aa00001", "za00002", "hk00003", "lk00004", "sb00005",
            "zi00006", "as00007", "ma00008", "aa00009", "sb00010",
            "ja00011", "lk00012", "sa00013", "ss00014", "mm00015",
            "fk00016", "mh00017", "ba00018", "fa00019", "ah00020",
            "ka00021", "aa00022", "aa00023", "tj00024", "jm00025",
            "hk00026", "mz00027", "sf00028", "zm00029", "ik00030",
            "hh00031", "mm00032", "ns00033", "ma00034", "ns00035",
            "zk00036", "fm00037", "lk00038", "am00039", "mn00040",
            "yj00041", "fk00042", "ua00043", "zk00044", "sr00045",
            "at00046", "ff00047", "sr00048", "kz00049", "rz00050"]

# LIST OF BOOKS AVAILABLE IN THE LIBRARY NAMED library_books
library_books = ["APS", "Algorithmic Problem Solving", "Shakespeare Tales", "Harry Potter",
                 "Interstellar", "The Lord of the Rings", "The Hobbit", "Geography",
                 "Crime and Punishment", "Chemistry", "Sociology", "History",
                 "King Lear", "Merchant of Venice", "The Road", "Physics", "Biology",
                 "The Alchemist", "Frankenstein", "Business Studies", "Accounts",
                 "The Outsiders", "The Handmaids Tale", "The Kite Runner", "Economics",
                 "Inception", "Calculus", "Architecture", "Jane Eyre", "Oxford Dictionary",
                 "Renewable Energy", "The Book Thief", "Secret Garden", "Literature",
                 "Animal Farm", "Almanac", "Psychology", "English Language", "Arabic",
                 "On the Road", "Reader's Digest", "Mathematics", "Computer Science"]

borrowed_books = {}  # TRACKS BORROWED BOOK FOR EACH USER
return_dates = {}  # STORES DUE DATE FOR BORROWED BOOKS


# FUNCTION TO VALIDATE USER ID
def validate_user(hu_id):
    return hu_id in ids_list


# FUNCTION TO DISPLAY ALL BOOKS IN THE LIBRARY
def display_books():
    print("\n--- Available Books in the Library ---")
    for book in library_books:
        print(f"- {book}")
    print("--------------------------------------\n")


# FUNCTION TO SEARCH FOR BOOKS RECURSIVELY
def search_books(search_term):
    matches = [book for book in library_books if search_term.lower() in book.lower()]
    if matches:
        print("\n--- Search Results ---")
        for book in matches:
            print(f"- {book}")
    else:
        print("No books found matching your search.")

    # Ask if the user wants to search again
    retry = input("Would you like to search for another book? (yes/no): ").lower()
    if retry == "yes":
        new_search_term = input("Enter the title or keyword to search for: ")
        search_books(new_search_term)  # Recursive call to search again


# FUNCTION TO HANDLE USER ACTION
def handle_user_action(hu_id):
    while True:
        user_action = input("Would you like to borrow, return, search, or exit? (search/borrow/return/exit): ").lower()

        if user_action == "return":
            while True:
                book_name = input("Kindly enter the name of the book to be returned: \n")
                if book_name in borrowed_books.get(hu_id, []):
                    return_book(hu_id, book_name)
                    break  # Exit the loop after successful return
                else:
                    print(f"ERROR - You have not borrowed the book '{book_name}'. Please try again.")
                    continue  # Continue asking for a valid book name

        elif user_action == "borrow":
            display_books()
            while True:
                book_name = input("Kindly enter the name of the book to be borrowed: \n")
                if book_name in library_books:
                    borrow_book(hu_id, book_name)
                    break  # Exit the loop after successful borrowing
                else:
                    print(f"ERROR - The book '{book_name}' is not available in the library.")
                    retry_or_exit = input("Would you like to try another book? (yes/exit): ").lower()
                    if retry_or_exit == "exit":
                        print("Exiting borrowing process.")
                        break  # Exit the borrowing loop
                    elif retry_or_exit == "yes":
                        continue  # Retry to borrow another book
                    else:
                        print("Invalid choice. Please try again.")

        elif user_action == "search":
            search_term = input("Enter the title or keyword to search for: ")
            search_books(search_term)  # Call the recursive search function

        elif user_action == "exit":
            print('Thank you for using the HABIB UNIVERSITY LIBRARY MANAGEMENT SYSTEM!')
            return  # Exit the program

        else:
            print("Error - Your desired action is invalid! Please try again.")


# FUNCTION TO BORROW BOOK
def borrow_book(hu_id, book_name):
    borrow_limit = 3
    if hu_id not in borrowed_books:
        borrowed_books[hu_id] = []

    if book_name in borrowed_books[hu_id]:
        print(f"You have already borrowed '{book_name}'.")
        return

    if len(borrowed_books[hu_id]) >= borrow_limit:
        print("You have borrowed the maximum number of books (3). Please return a book before borrowing more.")
        return

    borrowed_books[hu_id].append(book_name)  # Add book to the borrowed list
    library_books.remove(book_name)  # Remove book from the library
    due_date = datetime.date.today() + datetime.timedelta(days=14)  # Set due date (2 weeks)
    return_dates[book_name] = due_date  # Record due date
    print(f"You have successfully borrowed '{book_name}'. Please return it by {due_date}.\n")


# FUNCTION TO CALCULATE FINE
def calculate_fine(book_name):
    today = datetime.date.today()
    due_date = return_dates.get(book_name)

    if due_date and today > due_date:
        overdue_days = (today - due_date).days
        fine = overdue_days * 100  # Fine is 100 units per day overdue
        print(f"The book '{book_name}' is overdue by {overdue_days} days. Fine: {fine} units.")
        return fine
    else:
        return 0  # No fine if the book is returned on time


# FUNCTION TO RETURN BOOK
def return_book(hu_id, book_name):
    if hu_id in borrowed_books and book_name in borrowed_books[hu_id]:
        fine = calculate_fine(book_name)
        borrowed_books[hu_id].remove(book_name)
        del return_dates[book_name]  # Remove due date for returned book
        library_books.append(book_name)  # Add the book back to the library

        if fine > 0:
            print(f"You have returned '{book_name}' with a fine of {fine} units. Thank you!")
        else:
            print(f"You have successfully returned '{book_name}'. Thank you!")
    else:
        print(f"ERROR - You have not borrowed the book '{book_name}'.")


# MAIN PROGRAM FLOW
def main():
    print("Welcome to the HABIB UNIVERSITY LIBRARY MANAGEMENT SYSTEM!\n")

    while True:
        hu_id = input("Please enter your HU ID: ")

        if validate_user(hu_id):
            print(f"Welcome, {hu_id}! Let's get started.\n")
            handle_user_action(hu_id)  # Continuously handle user actions
            break  # Exit the loop after the user selects "exit" from the actions
        else:
            print("Invalid HU ID. Please try again.")  # Prompt user to try again if ID is invalid


# Start the program
main()
