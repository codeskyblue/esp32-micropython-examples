from micropython import const
import struct
import bluetooth
from bluetooth import UUID
from hid_services import HumanInterfaceDevice, Advertiser

F_READ = bluetooth.FLAG_READ
F_WRITE = bluetooth.FLAG_WRITE
F_READ_WRITE = bluetooth.FLAG_READ | bluetooth.FLAG_WRITE
F_READ_NOTIFY = bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY
F_READ_WRITE_NORESPONSE = bluetooth.FLAG_READ | bluetooth.FLAG_WRITE | bluetooth.FLAG_WRITE_NO_RESPONSE

DSC_F_READ = 0x02
DSC_F_WRITE = 0x03

# Class that represents the Consumer Control service for media keys
class ConsumerControl(HumanInterfaceDevice):
    def __init__(self, name="Bluetooth Consumer Control"):
        super(ConsumerControl, self).__init__(name)
        self.device_appearance = 962  # Device appearance ID, 962 = remote control

        self.HIDS = (
            UUID(0x1812),  # Human Interface Device
            (
                (UUID(0x2A4A), F_READ),  # 0x2A4A = HID information, to be read by client
                (UUID(0x2A4B), F_READ),  # 0x2A4B = HID report map, to be read by client
                (UUID(0x2A4C), F_READ_WRITE_NORESPONSE),  # 0x2A4C = HID control point, to be written by client
                (UUID(0x2A4D), F_READ_NOTIFY, (  # 0x2A4D = HID report, to be read by client after notification
                    (UUID(0x2908), DSC_F_READ),  # 0x2908 = HID reference, to be read by client
                )),
                (UUID(0x2A4E), F_READ_WRITE_NORESPONSE),  # 0x2A4E = HID protocol mode, to be written & read by client
            ),
        )

        # fmt: off
        self.HID_INPUT_REPORT = [
            # Consumer Control descriptor
            0x05, 0x0C,                    # USAGE_PAGE (Consumer Devices)
            0x09, 0x01,                    # USAGE (Consumer Control)
            0xA1, 0x01,                    # COLLECTION (Application)
            0x15, 0x00,                    # LOGICAL_MINIMUM (0)
            0x25, 0x01,                    # LOGICAL_MAXIMUM (1)
            0x75, 0x01,                    # REPORT_SIZE (1)
            0x95, 0x07,                    # REPORT_COUNT (7)
            0x09, 0xE9,                    # USAGE (Volume Up)
            0x09, 0xEA,                    # USAGE (Volume Down)
            0x09, 0xE2,                    # USAGE (Mute)
            0x09, 0xCD,                    # USAGE (Play/Pause)
            0x09, 0xB5,                    # USAGE (Scan Next Track)
            0x09, 0xB6,                    # USAGE (Scan Previous Track)
            0x09, 0xB7,                    # USAGE (Stop)
            0x81, 0x02,                    # INPUT (Data,Var,Abs)
            0x95, 0x01,                    # REPORT_COUNT (1)
            0x75, 0x01,                    # REPORT_SIZE (1)
            0x81, 0x01,                    # INPUT (Cnst,Ary,Abs)
            0xC0                           # END_COLLECTION
        ]
        # fmt: on

        # Define the initial consumer control state
        self.control_bits = 0
        self.services.append(self.HIDS)

    # Overwrite super to start the service
    def start(self):
        super(ConsumerControl, self).start()

        print("Registering consumer control services")
        handles = self._ble.gatts_register_services(self.services)
        self.save_service_characteristics(handles)
        self.write_service_characteristics()
        # Create an Advertiser for the HID service
        self.adv = Advertiser(self._ble, [UUID(0x1812)], self.device_appearance, self.device_name)
        print("Consumer control server started")

    # Overwrite super to save HID specific characteristics
    def save_service_characteristics(self, handles):
        super(ConsumerControl, self).save_service_characteristics(handles)

        (h_info, h_hid, h_ctrl, self.h_rep, h_d1, h_proto) = handles[3]  # Get the handles for the HIDS characteristics

        state = struct.pack("B", self.control_bits)

        print("Saving Consumer Control HID service characteristics")
        self.characteristics[h_info] = ("HID information", b"\x01\x01\x00\x00")  # HID info: ver=1.1, country=0, flags=000000cw with c=normally connectable w=wake up signal
        self.characteristics[h_hid] = ("HID input report map", bytes(self.HID_INPUT_REPORT))  # HID input report map
        self.characteristics[h_ctrl] = ("HID control point", b"\x00")  # HID control point
        self.characteristics[self.h_rep] = ("HID input report", state)  # HID report
        self.characteristics[h_d1] = ("HID input reference", struct.pack("<BB", 1, 1))  # HID reference: id=1, type=input
        self.characteristics[h_proto] = ("HID protocol mode", b"\x01")  # HID protocol mode: report

    # Send a consumer control command
    def send_control(self, control_code):
        if self.is_connected():
            # Set the appropriate bit based on the control code
            control_bits = 0
            if control_code == 'VOLUME_UP':
                control_bits = 0x01  # Bit 0 - Volume Up
            elif control_code == 'VOLUME_DOWN':
                control_bits = 0x02  # Bit 1 - Volume Down
            elif control_code == 'MUTE':
                control_bits = 0x04  # Bit 2 - Mute
            elif control_code == 'PLAY_PAUSE':
                control_bits = 0x08  # Bit 3 - Play/Pause
            elif control_code == 'NEXT_TRACK':
                control_bits = 0x10  # Bit 4 - Next Track
            elif control_code == 'PREV_TRACK':
                control_bits = 0x20  # Bit 5 - Previous Track
            elif control_code == 'STOP':
                control_bits = 0x40  # Bit 6 - Stop
            
            # Pack the control bits as a single byte
            state = struct.pack("B", control_bits)
            
            # Send the consumer control report
            self.characteristics[self.h_rep] = ("HID input report", state)
            self._ble.gatts_notify(self.conn_handle, self.h_rep, state)
            print("Notify with consumer control: ", control_bits)
            
            # Wait a bit before releasing
            import utime
            utime.sleep_ms(100)  # Longer delay to ensure the command is processed
            
            # BUG: not working
            # Release the control by sending zeros
            release_state = struct.pack("B", 0)
            self.characteristics[self.h_rep] = ("HID input report", release_state)
            self._ble.gatts_notify(self.conn_handle, self.h_rep, release_state)
            print("Released")


    # Convenience methods for common media controls
    def volume_up(self):
        self.send_control('VOLUME_UP')
        
    def volume_down(self):
        self.send_control('VOLUME_DOWN')
        
    def mute(self):
        self.send_control('MUTE')
        
    def play_pause(self):
        self.send_control('PLAY_PAUSE')
        
    def next_track(self):
        self.send_control('NEXT_TRACK')
        
    def previous_track(self):
        self.send_control('PREV_TRACK')
        
    def stop(self):
        self.send_control('STOP')
