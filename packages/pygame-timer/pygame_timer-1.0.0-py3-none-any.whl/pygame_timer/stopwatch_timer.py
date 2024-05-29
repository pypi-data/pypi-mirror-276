from .timer import Timer


class StopwatchTimer(Timer):
    def __init__(self):
        """
        Initializes the StopwatchTimer.
        """
        self.__started_timer: bool = False
        self.__ms_start: int = 0
        self.__ms_ended: int = 0
        self.__total_ms_spent: int = 0

    def reset(self) -> None:
        """
        Resets the stopwatch pygame_timer.
        """
        self.__ms_start = 0
        self.__ms_ended = 0
        self.__total_ms_spent = 0
        self.__started_timer = False

    @property
    def get_current_elapsed_time(self) -> int:
        """
        Gets the current elapsed time of the stopwatch in milliseconds.

        :return: The current elapsed time in milliseconds.
        """
        if self.__started_timer:
            return self.__total_ms_spent + (self.get_current_ms_time() - self.__ms_start)
        return self.__total_ms_spent

    def start(self) -> None:
        """
        Starts or resumes the stopwatch pygame_timer.
        """
        self.__ms_start = self.get_current_ms_time()
        self.__started_timer = True

    def pause(self) -> None:
        """
        Pauses the stopwatch pygame_timer.
        """
        self.__ms_ended = self.get_current_ms_time()
        self.__total_ms_spent += self.__ms_ended - self.__ms_start
        self.__started_timer = False

