import time
from RPLCD.i2c import CharLCD

# Create an LCD instance, assuming you are using I2C
# Adjust the I2C address and port accordingly if different
lcd = CharLCD('PCF8574', 0x20)  # Change 0x27 to your I2C address if different

# Clear the LCD
lcd.clear()

# Write 'Hello, World!' to the LCD
lcd.write_string('Hello, World!')

# Keep the message on the screen for 5 seconds
time.sleep(5)

# Clear the display again
lcd.clear()
