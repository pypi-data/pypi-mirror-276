import logging, math, socket, struct, threading, time

logger = logging.getLogger('pyLTA.ethernet')


### global constants
LTA_SOFT_DATABUFF_SIZE = 2000

ETH_MEM_WIDTH_BYTES = 4
ETH_MAX_DATALENGTH = 256    # max length of a string, sent or received

# places in ethernet memory (where soft is master and board is slave)
ETH_ADDR_MASTER_DREADY = 0x0    # master -> slave: the data is ready
ETH_ADDR_MASTER_DATA = 0x6      # to copy the data
ETH_ADDR_MASTER_DACK = 0x1      # slave -> master: taking the data

# memory values
ETH_VAL_DREADY_START = 0x78787878   # data is ready to be read
ETH_VAL_DREADY_END = 0xCDCDCDCD     # data transmition ended from master end
ETH_VAL_DACK_START = 0xABABABAB     # slave is processing the message
ETH_VAL_DACK_END = 0xEFEFEFEF       # slave finished processing the message

# places in ethernet memory (where board is master and soft is slave)
ETH_ADDR_SLAVE_DREADY = 0x3     # master -> slave: the data is ready
ETH_ADDR_SLAVE_DLENGTH = 0x5    # to store the number of bytes sent by the board
ETH_ADDR_SLAVE_DATA = 70        # to copy the data
ETH_ADDR_SLAVE_DACK = 0x4       # slave -> master: data has been collected

# wait times (in seconds)
ETH_SHORTWAIT = .001    # we don't know when the LTA will be ready for us
ETH_LONGWAIT = .005     # we don't expect the LTA to be ready for the next 10 ms

# block selection (ots_block_sel in ethernet_interface.vhd)
eUser = 0
eEth = 1


### module exception
class LTAEthernetException(Exception):
    pass


### "public" functions
def flush(flush_sock: socket.socket):

    staleBytes = 0

    while True:
        try: dataBuff = flush_sock.recv(LTA_SOFT_DATABUFF_SIZE)
        # except TimeoutError: break
        except socket.timeout: break    # changed for compatibility with python 3.7
        else: staleBytes += len(dataBuff)
    logger.info(f'{flush_sock.getsockname()} | Discarded {staleBytes} stale bytes')


### "private" functions
def _request_string_from_board(sock: socket.socket, nchar: int, print_packets):
    
    blockInt = eUser
    address = ETH_ADDR_SLAVE_DATA

    # number of 32-bit words
    n = math.ceil((nchar+3)/4)

    # Buffer structure:
    # < : little-endian
    # BB: r/w flag, number of words
    # LL : address.
    buffer = struct.pack('<BBLL', 0, n, address, blockInt)

    # logger.debug(f'request: r/w={buffer[0]}, n={buffer[1]}, address=0x{address:08X} (block {blockInt})')

    flag = 0

    while not flag:
        
        # request data @address to board
        sentbytes = sock.send(buffer)
        if sentbytes < len(buffer):
            logger.error(f'{sock.getsockname()} | Error sending UDP control packet')
            raise LTAEthernetException
        
        # read data back from board
        exp_length = 2 + 8*n
        recBuff_length = exp_length +8 # add extra 8 bytes just in case
        try:
            recBuff, clientAddr = sock.recvfrom(recBuff_length)
        except Exception as e:
            logger.warning(f'{sock.getsockname()} | UDP error, no message received: ' + e)
        
        else:
            flag = 1
            numRecBytes = len(recBuff)
            if print_packets: logger.debug(f'numRecBytes={numRecBytes}, packType={recBuff[0]}, packCounter={recBuff[1]}')

            if numRecBytes != exp_length:
                logger.warning(f'{sock.getsockname()} | Unexpected packet size: {numRecBytes} (expected {exp_length})')

            quadWordsCount = (numRecBytes - 2) // 8

            response_bytes = b''
            for i in range(quadWordsCount):
                buffer, response_addr = struct.unpack_from('<4sL', recBuff, offset=2+i*8)
                if response_addr < ETH_ADDR_SLAVE_DATA:
                    logger.warning(f'{sock.getsockname()} | Unexpected response address: 0x{response_addr:X} (expected 0x{ETH_ADDR_SLAVE_DATA:X})')
                if print_packets: logger.debug(f'response[{i}]: addr 0x{response_addr:08X}, data 0x{buffer.hex()}')
                response_bytes += buffer

            response_bytes = response_bytes.partition(b'\0')[0]  # store the bytes before the null ending
            
            if len(response_bytes) != nchar:
                logger.warning(f'{sock.getsockname()} | Unexpected response string length: {len(response_bytes)} (expected {nchar})')

    return response_bytes.decode()


def _request_word_from_board(sock: socket.socket, block, address, print_packets):

    # Buffer structure:
    # < : little-endian
    # BB: r/w flag, number of words
    # LL : address.
    buffer = struct.pack('<BBLL', 0, 1, address, block)

    if print_packets: logger.debug(f'request: r/w={buffer[0]}, n={buffer[1]}, address=0x{address:08X} (block {block})')

    flag = 0
    while not flag:
        # request data @address to board
        if sock.send(buffer) < len(buffer):
            logger.error(f'{sock.getsockname()} | Error sending UDP control packet')
            raise LTAEthernetException

        try:            
            recBuff, clientAddr = sock.recvfrom(20)
        except Exception as e:
            logger.warning(f'{sock.getsockname()} | UDP error on control port, no message received: {e}')
            return 
        
        flag = 1
        numRecBytes=len(recBuff)
        if print_packets: logger.debug(f'numRecBytes={numRecBytes}, packType={recBuff[0]}, packCounter={recBuff[1]}')

        if numRecBytes != 10:
            logger.warning(f'{sock.getsockname()} | Unexpected packet size: {numRecBytes} (should normally be 10 for a single-word read)')

        if block == eUser:
            recData, responseAddr = struct.unpack_from('<LL', recBuff, offset=2)
            if print_packets: logger.debug(f'response: addr 0x{responseAddr:08X}, data 0x{recData:08X}')

            if responseAddr != address:
                logger.warning(f'{sock.getsockname()} | response address (0x{responseAddr:X}) does not match request address (0x{address:X})')

        if block == eEth:
            recData = struct.unpack_from('<Q', recBuff, offset=2)[0]
            if print_packets: logger.debug(f'response: 0x{recData:016X}')

    return recData


def _send_string_to_board(sock: socket.socket, string: str, print_packets):
        
    logger.debug(f'Sending to {sock.getsockname()}: {string}')

    blockInt = eUser
    address = ETH_ADDR_MASTER_DATA
    sendBuff = string.encode()

    # number of 32-bit words needed to hold the string
    size_w = math.ceil((len(sendBuff)+1)/ETH_MEM_WIDTH_BYTES)

    # Buffer structure:
    # < : little-endian
    # BB: r/w flag, number of 64-bit words
    # LL : address, block
    # Q: data

    buffer = struct.pack('<BBLL', 1, size_w, address, blockInt)
    for i in range(size_w):
        buffer += struct.pack('<4sxxxx', sendBuff[i*4:(i+1)*4]) # only fill the bottom 4 bytes of each word
    
    if print_packets: logger.debug(f'write: r/w={buffer[0]}, n={buffer[1]}, address=0x{address:08X} (block {blockInt}), value={string}')

    if sock.send(buffer) < len(buffer):
        logger.error(f'{sock.getsockname()} | Error sending UDP control packet')
        raise LTAEthernetException
    

def _send_word_to_board(sock: socket.socket, block, address, value, print_packets):

    # Buffer structure:
    # < : little-endian
    # BB: r/w flag, number of 64-bit words
    # LL : address, block
    # Q: data

    buffer = struct.pack('<BBLLQ', 1, 1, address, block, value)

    if print_packets: logger.debug(f'write: r/w={buffer[0]}, n={buffer[1]}, address=0x{address:08X}, value=0x{value:016X}')

    if sock.send(buffer) < len(buffer):
        logger.error(f'{sock.getsockname()} | Error sending UDP control packet')
        raise LTAEthernetException
    

### module main class
class LTAEthernet:

    def __init__(self, control_socket: socket.socket, 
                 data_socket: socket.socket, lta_name: str, print_packets=False):

        self.name = lta_name
        self.sock = control_socket
        self.print_packets = print_packets

        self._configure_board(data_socket.getsockname())

        self._idle_event = threading.Event()
        self._start_idle_thread()
        

    def _start_idle_thread(self):
        
        self._idle_event.set()
        self._idle_thread = threading.Thread(target=_flush_output, 
                                             args=(self,),
                                             daemon=True)      
        self._idle_thread.start()

    
    def _stop_idle_thread(self):

        self._idle_event.clear()
        self._idle_thread.join()
    

    def _receive_cmd(self):
        '''Get String'''

        # s_dready start
        # check if there is a call from the board
        ready = _request_word_from_board(self.sock, eUser, ETH_ADDR_SLAVE_DREADY, 
                                          self.print_packets) # recv handshake step 1

        # return if the board is not calling
        if ready != ETH_VAL_DREADY_START:

            if ready != ETH_VAL_DREADY_END:
                raise LTAEthernetException(f'Unexpected handshake value: ready=0x{ready:08X}')
            # raise LTAEthernetException(f'Board is not calling')
            return ''
        
        # check the length of the data being sent by the board
        ndata = _request_word_from_board(self.sock, eUser, ETH_ADDR_SLAVE_DLENGTH, self.print_packets) # recv handshake step 2

        if ndata > ETH_MAX_DATALENGTH:
            raise LTAEthernetException(f'ndata unreasonably large: 0x{ndata:08X}')
        
        # read the data
        response = _request_string_from_board(self.sock, ndata, 
                                               self.print_packets) # recv handshake step 3

        # s_dack start
        _send_word_to_board(self.sock, eUser, ETH_ADDR_SLAVE_DACK, ETH_VAL_DACK_START,
                             self.print_packets) # recv handshake step 4

        # s_dready end
        ready = 0
        while True:
            ready = _request_word_from_board(self.sock, eUser, 
                                              ETH_ADDR_SLAVE_DREADY,
                                              self.print_packets) # recv handshake step 5

            if ready == ETH_VAL_DREADY_END: break

            if ready != ETH_VAL_DREADY_START:
                logger.warning(f'Unexpected handshake value: ready=0x{ready:08X}')
            time.sleep(ETH_SHORTWAIT)   # wait for eth_sdata_put to check ETH_ADDR_SLAVE_DREADY
        
        # s_dack end
        _send_word_to_board(self.sock, eUser, ETH_ADDR_SLAVE_DACK, ETH_VAL_DACK_END,
                             self.print_packets) # recv  handshake step 6

        # uB sleeps for 10 ms after it sets ETH_ADDR_SLAVE_DREADY, so calling code should wait before checking for the next message

        return response
    

    def _send_cmd(self, cmd_buffer: str):
        '''Send command'''

        _send_string_to_board(self.sock, cmd_buffer, 
                               self.print_packets) # send handshake step 1

        while True:
            # m_dready start
            _send_word_to_board(self.sock, eUser, ETH_ADDR_MASTER_DREADY, 
                                ETH_VAL_DREADY_START, 
                                self.print_packets)  # send handshake step 2

            # m_dack start
            ack = _request_word_from_board(self.sock, eUser, ETH_ADDR_MASTER_DACK, 
                                            self.print_packets)  # send handshake step 3
            if ack == ETH_VAL_DACK_START: break
            time.sleep(ETH_SHORTWAIT)   # wait for eth_mdata_get to run
        
        while True:
            # m_dready end
            _send_word_to_board(self.sock, eUser, ETH_ADDR_MASTER_DREADY, ETH_VAL_DREADY_END, 
                                 self.print_packets)# send handshake step 4

            # m_dack end
            ack = _request_word_from_board(self.sock, eUser, ETH_ADDR_MASTER_DACK,
                                            self.print_packets)   # send handshake step 5

            if ack == ETH_VAL_DACK_END: break

            time.sleep(ETH_LONGWAIT)    # uB waits for 10 ms after setting ETH_ADDR_MASTER_DACK


    def _listen_to_board_response(self, exp_response: str, timeout: float):

        response = ''
        timeout_time = time.monotonic() + timeout
        
        # get response from the board
        while True:
            buffer = self._receive_cmd()
            response += buffer
            if buffer != '': 
                logger.debug(f'Received from LTA: {buffer.strip()}')

            # "ERROR" should break you out of the loop (important for "read" or "runseq")
            if 'ERROR' in response:
                raise LTAEthernetException(f'Possible error: {response}')

            if response == exp_response:
                # got exactly the expected response
                break

            if exp_response in response:
                logger.debug('Got expected response plus additional messages')
                break

            time.sleep(ETH_LONGWAIT)    # we don't expect another string for 10 ms

            if time.monotonic() > timeout_time:
                raise TimeoutError(f'Timeout while waiting for "{exp_response}"')
            
        # logger.debug(f'LTA response: {response}')
        
        return response
    

    def _configure_board(self, data_addr):

        # set firmware in dynamic mac resolution mode for data mode
        _send_word_to_board(self.sock, eEth, 0xB, 1, self.print_packets)

        # set IP address and port for burst data
        # logger.info(f'Writing burst destination = {data_addr}')

        # encode the burst destination IP so that the board understands it
        ip_addr_list = data_addr[0].split('.')
        enc_ip = sum([int(x)<<i*8 for i,x in enumerate(ip_addr_list[::-1])])

        # send the IP
        _send_word_to_board(self.sock, eEth, 0x6, enc_ip, self.print_packets)

        # send the port
        _send_word_to_board(self.sock, eEth, 0x8, data_addr[1], self.print_packets)

        # read back the configuration
        resp_ip = _request_word_from_board(self.sock, eEth, 0x6, self.print_packets)
        resp_port = _request_word_from_board(self.sock, eEth, 0x8, self.print_packets)

        if resp_ip == enc_ip:
            if data_addr[1] == resp_port:
                logger.info('Correctly sent writing burst destination')
                return
            
            else: 
                logger.error(f'Badly configured port for writing burst destination: sent {data_addr[1]} but received {resp_port}')
                raise LTAEthernetException
        
        # extract IP
        received_ip = '.'.join([(resp_ip >> i*8) & 0xFF for i in range(4)][::-1])

        logger.error(f'Could not configure writing burst destination: sent {data_addr[0]} but received {received_ip}')
        raise LTAEthernetException
    

    def send_and_recv(self, send_cmd: str, exp_response: str, timeout: float):
        
        self._stop_idle_thread()
        
        self._send_cmd(send_cmd)
        response = self._listen_to_board_response(exp_response, timeout)
        
        self._start_idle_thread()

        return response


def _flush_output(eth: LTAEthernet):

    logger = logging.getLogger(f'pyLTA.{eth.name}_eth')
    # logger.info('started idle thread')
    while eth._idle_event.is_set():
        
        response = eth._receive_cmd()
        if response and response != '':
            logger.info(response.strip('\r\n'))

        time.sleep(.01)
    # logger.info('stopped idle thread')
    