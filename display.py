# Import necessary libraries
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789  # For ST7789 controller

# Define pins based on Raspberry Pi GPIO connections
cs_pin = digitalio.DigitalInOut(board.D5)    # Chip select
dc_pin = digitalio.DigitalInOut(board.D6)    # Data/Command
reset_pin = digitalio.DigitalInOut(board.D16)  # Reset

# Configure SPI connection
spi = board.SPI()

# Initialize display
display = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    width=240,
    height=320,
    rotation=0  # Temporarily set rotation to 0 for testing
)

# Define original width and height
original_width = 240
original_height = 320

# Then create image using the original dimensions
image = Image.new("RGB", (original_width, original_height))
draw = ImageDraw.Draw(image)

# Draw a filled background using original dimensions
draw.rectangle((0, 0, original_width, original_height), fill=(0, 0, 0))

# Draw some shapes (coordinates might need adjustment based on visual output)
draw.rectangle((10, 10, 110, 110), outline=(255, 0, 0), fill=(0, 0, 255))
draw.ellipse((120, 10, 220, 110), outline=(0, 255, 0), fill=(255, 0, 0))

# Load a font
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)

# Draw some text (coordinates might need adjustment based on visual output)
draw.text((10, 120), "Hello World!", font=font, fill=(255, 255, 0))

# Display the image
display.image(image)
