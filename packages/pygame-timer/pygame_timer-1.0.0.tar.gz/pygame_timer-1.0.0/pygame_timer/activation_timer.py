from .timer import Timer


class ActivationTimer(Timer):
    def __init__(self, interval: int = 100):
        """
        Initializes the ActivationTimer with an optional interval time in milliseconds.

        :param interval: The interval time in milliseconds (default is 100).
        """
        self.__last_time_taken: int = self.get_current_ms_time()
        self.__interval: int = interval

    def activation_stopped(self, activated: bool) -> bool:
        """
        Checks if the activation has stopped for a certain time.

        :param activated: The current activation state.
        :return: True if the activation has stopped for the specified interval, otherwise False.
        """
        current_time = self.get_current_ms_time()
        if activated:
            self.__last_time_taken = current_time
        return self.__check_if_finished_interval(current_time=current_time)

    def activation_started(self, activated: bool) -> bool:
        """
        Checks if the activation has started for a certain time.

        :param activated: The current activation state.
        :return: True if the activation has started for the specified interval, otherwise False.
        """
        current_time = self.get_current_ms_time()
        if not activated:
            self.__last_time_taken = current_time
        return self.__check_if_finished_interval(current_time=current_time)

    def __check_if_finished_interval(self, current_time: int) -> bool:
        """
        Checks if the specified interval has finished.

        :param current_time: The current time in milliseconds.
        :return: True if the interval has finished, otherwise False.
        """
        if current_time >= self.__last_time_taken + self.__interval:
            self.__last_time_taken = current_time
            return True
        return False

    def debug(self) -> None:
        """
        Prints debugging information for the activation pygame_timer.
        """
        print("Debugging: ")
        print(f"current time: {self.get_current_ms_time()}")
        print(f"last time: {self.__last_time_taken}")
        print(f"interval: {self.__interval}\n")

    def change_interval(self, interval: int) -> None:
        """
        Changes the interval time.

        :param interval: The new interval time in milliseconds.
        """
        self.__interval = interval

