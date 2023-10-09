import mysql.connector
from Adafruit_CircuitPython_SGP30 import Adafruit_SGP30
import Adafruit_DHT
import time
from datetime import datetime

# Initialize the SGP30 sensor
sgp30 = Adafruit_SGP30()

# Initialize the DHT11 sensor
dht_pin = 4  # GPIO pin where the DHT11 sensor is connected
dht_sensor = Adafruit_DHT.DHT11

# Initialize the MySQL database connection
db = mysql.connector.connect(
    host="localhost",
    user="yusuf1",
    password="Nimco005",
    database="database_ws"
)
cursor = db.cursor()

try:
    # Initialize the SGP30 sensor
    sgp30.begin()

    while True:
        # Read data from the SGP30 sensor
        eCO2, TVOC = sgp30.read_measurements()

        # Read data from the DHT11 sensor
        humidity, temperature = Adafruit_DHT.read_retry(dht_sensor, dht_pin)

        # Get the current timestamp
        timestamp = datetime.now()

        # Insert data into the database
        sql = "INSERT INTO SensorReadings (sensor_id, value, timestamp, date) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (1, eCO2, timestamp, timestamp.date()))
        cursor.execute(sql, (2, TVOC, timestamp, timestamp.date()))
        cursor.execute(sql, (3, temperature, timestamp, timestamp.date()))
        cursor.execute(sql, (4, humidity, timestamp, timestamp.date()))

        # Commit the changes to the database
        db.commit()

        # Print the data (for testing)
        print(f"eCO2: {eCO2} ppm, TVOC: {TVOC} ppb, Temperature: {temperature}°C, Humidity: {humidity}%")

        # Wait for a while before taking the next reading
        time.sleep(300)  # 5 minutes

except KeyboardInterrupt:
    pass
finally:
    # Close the database connection
    db.close()
