from .timer import Timer


class CooldownTimer(Timer):
    def __init__(self, cooldown: int = 100):
        """
        Initializes the CooldownTimer with an optional cooldown time in milliseconds.

        :param cooldown: The cooldown time in milliseconds (default is 100).
        """
        self.__last_time_taken: int = self.get_current_ms_time()
        self.__cooldown: int = cooldown
        self.__finished_cooldown: bool = False

    def check_if_cooldown_finished(self) -> bool:
        """
        Checks if the cooldown period has finished.

        :return: True if the cooldown period has finished, otherwise False.
        """
        if not self.__finished_cooldown:
            self.__finished_cooldown = self.__check_if_finished_cooldown()
        return self.__finished_cooldown

    def __check_if_finished_cooldown(self) -> bool:
        """
        Checks if the specified cooldown has finished.

        :return: True if the cooldown has finished, otherwise False.
        """
        current_time = self.get_current_ms_time()
        if current_time >= self.__last_time_taken + self.__cooldown:
            self.__last_time_taken = current_time
            return True
        return False

    def reset_cooldown(self) -> None:
        """
        Resets the cooldown pygame_timer.
        """
        self.__last_time_taken = self.get_current_ms_time()
        self.__finished_cooldown = False

    def debug(self) -> None:
        """
        Prints debugging information for the cooldown pygame_timer.
        """
        print("Debugging: ")
        print(f"current time: {self.get_current_ms_time()}")
        print(f"last time: {self.__last_time_taken}")
        print(f"finished cooldown: {self.__finished_cooldown}")

    def change_cooldown(self, cooldown: int) -> None:
        """
        Changes the cooldown time.

        :param cooldown: The new cooldown time in milliseconds.
        """
        self.__cooldown = cooldown

