class Text:

    @staticmethod
    def instructions():
        return """- Choose number of movies to evaluate.
The larger the number you choose, the more accurate
SHARK-O-MENDATIONS you will recieve.
- I suggest you to choose 50 movies for a first usage.
- You can rate each film from 1 to 5 by selecting the
appropriate shark. If you haven't seen a movie, just
click the skip button.
!!! You can click on each movie title to get 
more information about it !!!
- After you get your SHARK-O-MENDATIONS you can press
the filter button in the upper right corner to specify
the genres of movies you are interested in.
- If you have used this app before you can click
the skip button or rate more movies for more  
accurate SHARK-O-MENDATIONS
Press the button below if you understand the instructions
"""

    @staticmethod
    def first_usage():
        return """Before you start using the application,
read the instructions in the upper right corner"""

    @staticmethod
    def genres_text():
        return """You have to choose at least one genre from
which you want to see SHARK-O-MENDATIONS!!!
"""

    @staticmethod
    def restore_text():
        return """Do you want to clear your data and start
rating movies again?
    """

    @staticmethod
    def shark(): return r"C:\Users\jakub\Projekt\Graphics\rekin.png"

    @staticmethod
    def star_shark(): return r"C:\Users\jakub\Projekt\Graphics\rekin_star.png"

    @staticmethod
    def no_rate(): return "You have to rate at least one movie to use skip button"