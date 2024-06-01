import numpy as np


class HealthCheck:
    def __init__():
        print("Hi, I'll do the health check of pepega!")

    @staticmethod
    def is_alive(pulse):
        return np.all((pulse >= 60) & (pulse <= 100))
