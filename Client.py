# Client.py
import Pyro4


front_end = Pyro4.Proxy("PYRONAME:example.front_end")

while True:
    print("\nMENU:")
    print("1) Retrieve Rating")
    print("2) Submit/Update Rating")
    print("3) Exit")
    choice = input("Enter choice (1,2 or 3): ")
    if choice == "1": #return movie rating for given movieID
        movie = input("Enter movie ID (1-5060): ")
        rating = front_end.retrieve(movie)
        if rating == "0":
            print("You haven't rated that movie yet")
        else:
            print("The rating of movie",movie,"is",rating)
    elif choice == "2": #update/create new rating for given movieID
        movie = input("Enter movie ID (1-5060): ")
        rating = input("Enter rating (1-5): ")
        front_end.update(movie,rating)
    else:
        break
