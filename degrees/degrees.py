import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Tom Cruise (a few good men) -> Kevin Bacon (apollo 13) -> gary sinise

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")
    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.

    STATE: A movie and its various actors
    ACTION: Move to a movie from one of those actors

    """

    shortestPath = []

    initialState = (None, source)
    startNode = Node(initialState, None, actions(initialState))
    frontier = QueueFrontier()
    explored = []

    currentNode = startNode
    frontier.add(currentNode)

    while True:
        # If there's no solution, return None
        if frontier.empty():
            return None

        currentNode = frontier.remove()

        if goal(currentNode, target):
            movieName = movies[currentNode.state[0]]["title"]
            currentNode = frontier.remove()

            while currentNode.state != initialState:
                # (movieName, actor/actress) is the value to append
                movieName = movies[currentNode.state[0]]["title"]

                star = people[currentNode.action]["name"]
                shortest_path.append((movieName, star))

                currentNode = currentNode.parent

            shortest_path.reverse()
            return shortest_path

            return True  # TODO: implement returning the solution

        nextActions = actions(currentNode.state)

        for action in nextActions:
            node = Node(
                results(currentNode.state, action),
                currentNode,
                action
            )

            if node.state not in explored and not frontier.contains_state(node.state):
                frontier.add(node)

        explored.append(currentNode.state)


# If the first item in the tuple is the target, we're done
def goal(node, target):
    if target in node.state[1]:
        return True
    return False


# Returns all the next possible actions (which movie-cast node to explore)
def actions(state):
    nextActions = []

    if state[0] is not None:
        stars = movies[state[0]]["stars"]
        for star in stars:
            starsMovies = getSourcesMovies(star)
            for movie in starsMovies:
                nextActions += (star, movie)
    else:
        nextActions = getSourcesMovies(state[1])

    nextActions = set(nextActions)
    return nextActions


# Returns the resulting state (a movie and its cast) based on which movie was chosen (the previous action)
def results(state, action):
    newStateMovie = action      # "action" represents the movie we chose to explore
    newMovieCast = movies[newStateMovie]["stars"]
    newState = (newStateMovie, newMovieCast)
    return newState


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


def getSourcesMovies(source):
    sourcesMovies = []
    for movie in movies:
        if source in movies[movie]["stars"]:
            sourcesMovies.append(movie)

    return sourcesMovies


def printFrontier(frontier):
    i = len(frontier.frontier) - 1
    print("TOP of STACK")
    while i != -1:
        print(f"[{frontier.frontier[i]}]")
        i -= 1

    print("BOTTOM of STACK")


if __name__ == "__main__":
    main()
