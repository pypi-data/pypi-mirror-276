from pygame.time import get_ticks


class Timer:
    @staticmethod
    def get_current_ms_time() -> int:
        """
        Gets the current time in milliseconds via pygame.

        :return: The current time in milliseconds.
        """
        return get_ticks()

