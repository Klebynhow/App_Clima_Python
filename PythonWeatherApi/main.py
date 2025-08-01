
import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore  import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.cityLabel = QLabel("Digite o nome da cidade: ", self)
        self.cityInput = QLineEdit(self)
        self.cityInput.setPlaceholderText("Cidade")
        self.getWeatherButton= QPushButton("Buscar", self)
        self.temperatureLabel = QLabel(self)
        self.emojiLabel = QLabel(self)
        self.descriptionLabel = QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("App de Clima")

        vbox = QVBoxLayout()
        vbox.addWidget(self.cityLabel)
        vbox.addWidget(self.cityInput)
        vbox.addWidget(self.getWeatherButton)
        vbox.addWidget(self.temperatureLabel)
        vbox.addWidget(self.emojiLabel)
        vbox.addWidget(self.descriptionLabel)
        self.setLayout(vbox)

        self.cityLabel.setAlignment(Qt.AlignCenter)
        self.cityInput.setAlignment(Qt.AlignCenter)
        self.temperatureLabel.setAlignment(Qt.AlignCenter)
        self.emojiLabel.setAlignment(Qt.AlignCenter)
        self.descriptionLabel.setAlignment(Qt.AlignCenter)

        self.cityLabel.setObjectName("cityLabel")
        self.cityInput.setObjectName("cityInput")
        self.getWeatherButton.setObjectName("getWeatherButton")
        self.temperatureLabel.setObjectName("temperatureLabel")
        self.emojiLabel.setObjectName("emojiLabel")
        self.descriptionLabel.setObjectName("descriptionLabel")

        self.setStyleSheet("""
            WeatherApp{
                background-color: hsl(198, 74%, 84%);               
            }
            QLabel, QPushButton{
                font-family: calibri;
            }
            QLabel#cityLabel{
                font-size: 40px;
                font-style: italic;        
            }
            QLineEdit#cityInput{
                font-size: 40px;               
            }
            QPushButton#getWeatherButton{
                font-size: 30px;
                font-weight: bold;               
            }
            QLabel#temperatureLabel{
                font-size: 75px;             
            }
            QLabel#emojiLabel{
                font-size: 100px; 
                font-family: Segoe UI emoji;       
            }
            QLabel#descriptionLabel{
                font-size: 50px;        
            }
        """)

        self.getWeatherButton.clicked.connect(self.getWeather)

    def getWeather(self):
        apiKey = "" # INSERIR API KEY AQUI
        city = self.cityInput.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={apiKey}&units=metric&lang=pt_br"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if data["cod"] == 200:
                self.displayWeather(data)
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.displayError("Bad Request\nFavor checar input")
                case 401:
                    self.displayError("Não Autorizado\nChave API inválida, checar linha 74")
                case 403:
                    self.displayError("Proibido\nAcesso Negado")
                case 404:
                    self.displayError("Não Encontrado\nCidade não encontrada")
                case 500:
                    self.displayError("Erro interno do servidor\nTentar novamente mais tarde")
                case 502:
                    self.displayError("Bad Gateway\nResposta inválida pelo servidor")
                case 503:
                    self.displayError("Serviço Indisponivel\nServidor fora de ar")
                case 504:
                    self.displayError("Gateway Timeout\nSem Resposta do Servidor")
                case _:
                    self.displayError(f"Erro HTTP\n{http_error}")
        except requests.exceptions.ConnectionError:
            self.displayError("Erro de Conexão\nChecar conexão com a Internet")
        except requests.exceptions.Timeout:
            self.displayError("Timeout Error\nRequest expirou")
        except requests.exceptions.TooManyRedirects:
            self.displayError("Too Many Redirects\nChecar a URL")
        except requests.exceptions.RequestException as req_error:
            self.displayError(f"Erro de Request\n{req_error}")

    def displayError(self, message):
        self.temperatureLabel.setStyleSheet("font-size: 30px")
        self.temperatureLabel.setText(message)
        self.emojiLabel.clear()
        self.descriptionLabel.clear()

    def displayWeather(self, data):
        self.temperatureLabel.setStyleSheet("font-size: 75px")
        tempC = data["main"]["temp"]
        weather_id = data["weather"][0]["id"]
        weatherDescription = data["weather"][0]["description"]

        self.temperatureLabel.setText(f"{tempC:.0f}°C")
        self.emojiLabel.setText(self.getWeatherEmoji(weather_id))
        self.descriptionLabel.setText(weatherDescription)
    
    @staticmethod
    def getWeatherEmoji(weather_id):
        if 200 <= weather_id <= 232:
            return "⛈" 
        elif 300 <= weather_id <= 321:
            return "☁"
        elif 500 <= weather_id <= 531:
            return "🌧"
        elif 600 <= weather_id <= 622:
            return "❄"
        elif 701 <= weather_id <= 741:
            return "🌫"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "🌪"
        elif weather_id == 781:
            return "🌪"
        elif weather_id == 800:
            return "☀"
        elif 801 <= weather_id <= 804:
            return "☁☁"
        else:
            return ""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    WeatherApp = WeatherApp()
    WeatherApp.show()
    sys.exit(app.exec_())