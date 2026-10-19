import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QVBoxLayout, QLabel, QMessageBox
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()

#INITIALIZING THE WIDGET -------------------------------------------------------

        self.setWindowTitle("Weather App")
        self.CityLabel = QLabel("Enter the name of the city",self)
        self.CityText = QLineEdit(self)
        self.ShowWeather_btn = QPushButton("Show Weather",self)
        self.Temperature = QLabel(self)
        self.emoji = QLabel(self)
        self.description = QLabel(self)
        self.initUI()

#INITIALIZING THE LAYOUT -------------------------------------------------------

    def initUI(self):
        layout = QVBoxLayout()
        layout.addWidget(self.CityLabel)
        layout.addWidget(self.CityText)
        layout.addWidget(self.ShowWeather_btn)
        layout.addWidget(self.Temperature)
        layout.addWidget(self.emoji)
        layout.addWidget(self.description)

        self.setLayout(layout)

        self.CityLabel.setAlignment(Qt.AlignCenter)
        self.Temperature.setAlignment(Qt.AlignCenter)
        self.emoji.setAlignment(Qt.AlignCenter)
        self.description.setAlignment(Qt.AlignCenter)
        self.CityText.setAlignment(Qt.AlignCenter)


#CSS STYLING -----------------------------------------------------------------

        self.CityLabel.setObjectName("CityLabel")
        self.Temperature.setObjectName("Temp")
        self.emoji.setObjectName("emoji")
        self.description.setObjectName("description")

        self.setStyleSheet("""
            QLabel#CityLabel {
            font-size: 30px;
            font-weight: bold;
            }
            
            QLineEdit{
            padding: 20px;
            font-size: 35px;
            font-weight: bold;
            }

            QPushButton{
            padding : 15px;
            font-size: 20px;
            }
            
            QLabel#Temp{
            font-size: 30px;
            }

            QLabel#emoji{
            font-size: 50px;
            font-family: Segoe UI emoji
            }

            QLabel#description{
            font-size: 40px;
            }

""")

        self.ShowWeather_btn.clicked.connect(self.get_weather)

#GET WEATHER FUNCTION ----------------------------------------------------------

    def get_weather(self):
        api_key = "fdb572c6fa5d47e404f1943059e0322a"
        city = self.CityText.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if data["cod"] == 200:
                self.display_weather(data)
        except requests.exceptions.HTTPError:
            match response.status_code:
                case 400:
                    self.display_error("Bad request\ncheck your input")
                case 401:
                    self.display_error("Unauthorized\ninvalid api key")
                case 403:
                    self.display_error("Forbidden\nAccess denied")
                case 404:
                    self.display_error("Not found\ncity not found")
                case 500:
                    self.display_error("Bad Gateway\ninvalid response form the server")
                case 502:
                    self.display_error("Bad request\ncheck your input")
                case 503:
                    self.display_error("service unavailable\nthe server is down")
                case 504:
                    self.display_error("Gateway Timeout\nno response from the server")
                case _:
                    self.display_error(f"{response.status_code} error")
        except requests.exceptions.ConnectionError:
            self.display_error("Connection error\n check your internet connection")
        except requests.exceptions.Timeout:
            self.display_error("Request timed out ")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many redirects")
        except requests.exceptions.RequestException as reqerror:
            self.display_error(f"request error\n{reqerror}")

#DISPLAY WEATHER FUNCTION -----------------------------------------------------

    def display_weather(self,data):
        pass

#DISPLAY ERROR FUNCTION -----------------------------------------------------

    def display_error(self,message):
        QMessageBox.critical(self,"Error",message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec_())