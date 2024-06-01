import pandas as pd


class Pepega:
    def __init__():
        print("Hi, my name is Pepega!")
        self.alive = True

    def calculate_pulse(self, pressure, blood_volume):
        data = pd.DataFrame(
            {"pressure": pressure, "blood_volume": blood_volume}
        )
        data["pulse"] = data["pressure"] / data["blood_volume"] * 100

        return data
