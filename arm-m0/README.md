sudo apt-get install gcc-arm-none-eabi
sudo apt-get install gdb-arm-none-eabi
sudo apt-get install libusb-1.0.0-dev
sudo apt-get install cmake
sudo apt-get install python-serial python3-serial

git clone git@github.com:texane/stlink.git
cd stlink
make release
make install
cd ..

---------------------------------------------

### More details

The next set of tools on our list is [stlink](https://github.com/texane/stlink). This allows us to flash binaries to the board. Depending on your operating system, it may be available in your package manager -- otherwise refer to their Github page for instructions on how to [compile it from source](https://github.com/texane/stlink/blob/master/doc/compiling.md) (in that case, be careful to use libusb-1.0.0-dev, not libusb-0.1).

For the host-side, we rely on the `pyserial` module. Your package repository might offer python-serial or python-pyserial directly. Alternatively, this can be easily installed from PyPA by calling pip install pyserial (or pip3, depending on your system). If you do not have pip installed yet, you can typically find it as python3-pip using your package manager.

The last dependency is [libopencm3](https://github.com/libopencm3/libopencm3/). We've already packaged that; you only need to compile it, by typing `make` in the `libopencm3` directory.

---------------------------------------------

### Hooking up the board

you should need:

- An STM32F407 Discovery board
- A mini-USB to USB cable
- A UART-USB-connector
- Two (female-female) dupont / jumper cables

Connect the board to your machine using the mini-USB port. It should show up in `lsusb` as `STMicroelectronics ST-LINK/V2`.

We are using a UART-USB-connector that has a PL2303 chip on board. The driver should be loaded in your kernel by default. If not, it is typically called `pl2303`. When you plug in the device, it should show up as `Prolific Technology, Inc. PL2303 Serial Port` when you type `lsusb`.

Using the two dupont cables, connect the TX pin of the USB connector to the PA3 pin on the board, and connect RX to PA2. There is no need to connect any of the other pins.

---------------------------------------------

### Testing ARM

The code consists of two parts: code for the host (i.e. your laptop), and code for the board.

Let's start with the host, as that's easiest. Since we're only doing one-way communication at runtime (only the board outputs messages), we suffice with a simple Python script that listens to anything coming in on the relevant device. If the device does not show up on `/dev/ttyUSB0` but on a different port, modify the script accordingly. Simply start this script in a terminal (`python3 listener.py`), and leave it open (in `arm-utilities/hostside`).

To run code on the board, we compile `.bin` files. Try compiling `gimli.bin` by calling `make gimli.bin` in the `STM32F407` directory.

After compiling it, flash it onto the board by calling `st-flash write gimli.bin 0x8000000`.

Flashing a binary should automatically run it, and output should appear in your other shell (you still have that open, right?), in the Python listener. If output does not appear, try pressing the black RESET button. If it still does not work, check your cabling.
