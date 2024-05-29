from .timer import Timer


class IntervalTimer(Timer):
    def __init__(self, interval: int = 100):
        """
        Initializes the IntervalTimer with an optional interval time in milliseconds.

        :param interval: The interval time in milliseconds (default is 100).
        """
        self.__last_time: int = self.get_current_ms_time()
        self.__interval: int = interval

    def time_interval_finished(self) -> bool:
        """
        Checks if the interval time has finished.

        :return: True if the interval time has finished, otherwise False.
        """
        current_time = self.get_current_ms_time()
        if current_time - self.__last_time >= self.__interval:
            self.__last_time = current_time
            return True
        return False

    def debug(self) -> None:
        """
        Prints debugging information for the interval pygame_timer.
        """
        print("Debugging: ")
        print(f"current time: {self.get_current_ms_time()}")
        print(f"last time: {self.__last_time}")
        print(f"interval: {self.__interval}\n")

    def change_interval(self, interval: int) -> None:
        """
        Changes the interval time.

        :param interval: The new interval time in milliseconds.
        """
        self.__interval = interval

    def add_to_last_time(self, add_time: int) -> None:
        """
        Adds milliseconds to the last recorded time.

        :param add_time: The additional time in milliseconds to be added to the last recorded time.
        """
        self.__last_time += add_time
