from .timer import Timer
from .stopwatch_timer import StopwatchTimer


class TargetTimer(Timer):
    def __init__(self, target_ms_time: int = 0):
        """
        Initializes the TargetTimer with an optional target time in milliseconds.

        :param target_ms_time: The target time in milliseconds (default is 0).
        """
        self.__started: bool = False
        self.__timer_finished: bool = False
        self.__pause_timer: StopwatchTimer = StopwatchTimer()
        self.__target_ms_time: int = target_ms_time
        self.__ms_restarted: int = 0

    def add_target_time(self, add_ms_time: int) -> None:
        """
        Adds milliseconds to the target time.

        :param add_ms_time: The additional time in milliseconds to be added to the target time.
        """
        self.__target_ms_time += add_ms_time

    def set_target_time(self, target_ms_time: int) -> None:
        """
        Sets a new target time in milliseconds.

        :param target_ms_time: The new target time in milliseconds.
        """
        self.__target_ms_time = target_ms_time

    def reset(self) -> None:
        """
        Resets the pygame_timer.
        """
        self.__ms_restarted = self.get_current_ms_time()
        self.__pause_timer.reset()
        self.__timer_finished = False

    def check_if_finished_timer(self) -> bool:
        """
        Checks if the pygame_timer has reached the target time.

        :return: True if the target time is reached, otherwise False.
        """
        if self.get_current_elapsed_ms >= self.__target_ms_time:
            self.__timer_finished = True
        return self.__timer_finished

    @property
    def get_current_elapsed_ms(self) -> int:
        """
        Gets the current elapsed time of the pygame_timer in milliseconds.

        :return: The current elapsed time in milliseconds.
        """
        return self.get_current_ms_time() - self.__pause_timer.get_current_elapsed_time - self.__ms_restarted

    def debug(self) -> None:
        """
        Prints debugging information for the pygame_timer.
        """
        print(
            f"current time: {self.get_current_elapsed_ms} | ms restarted: {self.__ms_restarted} | "
            f"pause time: {self.__pause_timer.get_current_elapsed_time} | target time: {self.__target_ms_time}")

    def pause(self) -> None:
        """
        Pauses the pygame_timer.
        """
        self.__pause_timer.start()

    def resume(self) -> None:
        """
        Resumes the pygame_timer.
        """
        self.__pause_timer.pause()
