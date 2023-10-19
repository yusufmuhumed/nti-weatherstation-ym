import mysql.connector
from scd30_i2c import SCD30
import time
from datetime import datetime

# Initialize the SGP30 sensor
gassensor = SCD30()

#scd30.set_measurement_interval(2)
#scd30.start_periodic_measurement()

time.sleep(2)



# Initialize the MySQL database connection
db = mysql.connector.connect(
    host="localhost",
    user="yusuf1",
    password="Nimco005",
    database="database_ws"
)
cursor = db.cursor()

try:
    

    while True:
        if gassensor.get_data_ready():
            # Read data from the SGP30 sensor
            co2, temperature, humidity = gassensor.read_measurement()

    
        

        # Get the current timestamp
        timestamp = datetime.now()

        # Insert data into the database
        sql = "INSERT INTO SensorReadings (sensor_id, value, timestamp, date) VALUES (%s, %s, %s)"
        cursor.execute(sql, (1, co2, timestamp, timestamp.date()))
       
        cursor.execute(sql, (3, temperature, timestamp, timestamp.date()))
        cursor.execute(sql, (4, humidity, timestamp, timestamp.date()))

        # Commit the changes to the database
        db.commit()

        # Print the data (for testing)
        print(f"eCO2: {co2} ppm, Temperature: {temperature}°C, Humidity: {humidity}%")

        # Wait for a while before taking the next reading
        time.sleep(300)  # 5 minutes

except KeyboardInterrupt:
    pass
finally:
    # Close the database connection
    db.close()
