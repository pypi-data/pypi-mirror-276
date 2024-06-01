class labcomm_packet():
    def __init__(self):
        '''
        LABCOMM PACKET FRAME DEFINITION:
        ┌──────────┬─────────┬────────────────┬────────────────┬──────────────┬─────────────┬──────────┐
        │ PREAMBLE │ VERSION │ DESTINATION ID │    SOURCE ID   │ PAYLOAD SIZE │   PAYLOAD   │ ENDAMBLE │
        └──────────┴─────────┴────────────────┴────────────────┴──────────────┴─────────────┴──────────┘
        │◄───10B──►│◄──1B───►│◄──────2B──────►│◄──────2B──────►│◄─────4B─────►│◄─SIZE(P/L)─►│◄───4B───►│
        '''
        self.PREAMBLE           = "L@BC0MmADI"
        self.ENDAMBLE           = "TeoM"
        self.VERSION            = "1"
        self.ENDAMBLE_LEN       = len(self.ENDAMBLE)
        self.ENDPOINT_LEN       = 2
        self.PAYLOAD_SIZE_LEN   = 4
        self.META_SIZE          = len(self.PREAMBLE) + len(self.VERSION) + 2*self.ENDPOINT_LEN + self.PAYLOAD_SIZE_LEN
                
    def assemble(self, source, destination, payload):        
        return  bytes(self.PREAMBLE, "latin-1")                                             + \
                bytes(self.VERSION, "latin-1")                                              + \
                int.to_bytes(destination, length=self.ENDPOINT_LEN, byteorder="big")        + \
                int.to_bytes(source, length=self.ENDPOINT_LEN, byteorder="big")             + \
                int.to_bytes(len(payload), length=self.PAYLOAD_SIZE_LEN, byteorder="big")   + \
                bytes(payload, "latin-1")                                                   + \
                bytes(self.ENDAMBLE, "latin-1")

class labcomm_parser(labcomm_packet):
    def __init__(self, interface):
        super().__init__()
        self.clear_buffers()
        self.preamble_buffer    = ""
        self.state              = "waiting"
        self.valid_message      = False
        self.interface          = interface

    def clear_buffers(self):
        self.version_buffer             = ""
        self.preamble                   = ""
        self.destination_id_buffer      = ""
        self.source_id_buffer           = ""
        self.payload_size_buffer        = ""
        self.payload_buffer_as_string   = ""
        self.endamble_buffer            = ""
        self.payload_buffer_as_list     = []

    def detect_preamble(self, byte):
        if len(self.preamble_buffer) < len(self.PREAMBLE):  # Build buffer to length of PREAMBLE
            self.preamble_buffer += byte                    #
        elif self.state != "get_payload":                   # Acquired length of PREAMBLE, disregard in payload read
            self.preamble_buffer = self.preamble_buffer[1:] # Shift left one byte
            self.preamble_buffer += byte                    # Append new byte
        if self.preamble_buffer == self.PREAMBLE:           # Check for match
            self.state = "get_version"                      # Increment state
            self.clear_buffers()
            self.preamble = self.preamble_buffer
            self.valid_message = False

    def get_version(self, byte):
        self.version_buffer += byte
        self.state = "get_destination_id"
        
    def get_destination_id(self, byte):
        if len(self.destination_id_buffer) < self.ENDPOINT_LEN:
            self.destination_id_buffer += byte
        if len(self.destination_id_buffer) == self.ENDPOINT_LEN:
            self.state = "get_source_id"

    def get_source_id(self, byte):
        if len(self.source_id_buffer) < self.ENDPOINT_LEN:
            self.source_id_buffer += byte
        if len(self.source_id_buffer) == self.ENDPOINT_LEN:
            self.state = "get_payload_size"

    def get_payload_size(self, byte):
        if len(self.payload_size_buffer) < self.PAYLOAD_SIZE_LEN:
            self.payload_size_buffer += byte
        if len(self.payload_size_buffer) == self.PAYLOAD_SIZE_LEN:
            self._compute_payload_size(self.payload_size_buffer[0:4])
            self.state = "get_payload"

    def get_payload(self, byte):
        if len(self.payload_buffer_as_list) < self.payload_size:
            self.payload_buffer_as_list.append(ord(byte))
            self.payload_buffer_as_string += byte
        if len(self.payload_buffer_as_list) == self.payload_size:
            self.payload_buffer_as_integer = int.from_bytes(self.payload_buffer_as_string.encode("latin-1"), 'big')
            self.state = "get_endamble"

    def get_endamble(self, byte):
        if len(self.endamble_buffer) < self.ENDAMBLE_LEN:
            self.endamble_buffer += byte
        if len(self.endamble_buffer) == self.ENDAMBLE_LEN:
            self.state = "waiting"
            self.valid_message = self.endamble_buffer == self.ENDAMBLE

    def parse_byte(self, byte):
        if self.state == "get_version":
            self.get_version(byte)
        elif self.state == "get_destination_id":
            self.get_destination_id(byte)
        elif self.state == "get_source_id":
            self.get_source_id(byte)
        elif self.state == "get_payload_size":
            self.get_payload_size(byte)
        elif self.state == "get_payload":
            self.get_payload(byte)
        elif self.state == "get_endamble":
            self.get_endamble(byte)
        self.detect_preamble(byte) # Asynchronous start of packet detection
        
    def _compute_payload_size(self, string):
        try:
            self.payload_size = ord(string[0])*256**3 + ord(string[1])*256**2 + ord(string[2])*256 + ord(string[3])
        except:
            print(f'\n\nLabcomm debug breakpoint in _compute_payload_size()...\nPayload_size came back as "{string}".\n\n')
            self.payload_size = 0

    def read_message(self):
        meta_data = self.interface.read(self.META_SIZE)
        self._compute_payload_size(meta_data[self.META_SIZE-self.PAYLOAD_SIZE_LEN:self.META_SIZE])
        payload = self.interface.read(size=self.payload_size)
        endamble = self.interface.read(size=self.ENDAMBLE_LEN)
        if endamble != self.ENDAMBLE:
            self.interface.reset_input_buffer()
            print('\n\n*** Labcomm Packet Error *******    Malformed Packet Received. READ ABORTED!!!')
            # print(f'Possible Labcomm Version:           {ord(meta_data[len(self.PREAMBLE)])}')
            # print(f'Possible Labcomm Preamble:          {meta_data[0:len(self.PREAMBLE)]}')
            # print(f'Possible Labcomm Target address:    {ord(meta_data[10])*256 + ord(meta_data[11])}')
            # print(f'Possible Labcomm Sender address:    {ord(meta_data[8])*256 + ord(meta_data[9])}')
            print(f'Actual Message:                     {(meta_data + payload + endamble).encode("latin-1")}\n\n')
        else:
            for byte in meta_data + payload + endamble:
                self.parse_byte(byte)
        if self.interface.in_waiting:
            print(f"\n*** LABCOMM WARNING *** Still have {self.interface.in_waiting} bytes waiting to be picked up.")
            print("Extraneous Packet:")
            print(self.read_message())
            print()
        return {"preamble"      : self.preamble,
                "version"       : self.version_buffer,
                "dest_ID"       : self.destination_id_buffer,
                "source_ID"     : self.source_id_buffer,
                "payload_size"  : self.payload_size,
                "payload"       : payload.encode("latin-1"),
                "endamble"      : endamble
                }