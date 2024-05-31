import configparser, logging, os, socket, struct, threading, time
from datetime import datetime

from ._auxiliary import init_logger, print_time, update_hdr_card, update_hdr_file
from ._ethernet import LTAEthernet, flush, LTA_SOFT_DATABUFF_SIZE
from ._sseq_handler import SmartSequencer

from astropy.io import fits

try:
    import libABCD
    _libABCD_loaded = True

except: _libABCD_loaded = False


logger = init_logger('pyLTA', loglevel=logging.INFO, fileloglevel=logging.DEBUG)
abs_path = os.path.realpath(__file__)


### global constants
LTA_GEN_DONE_MESSAGE = "Done\r\n"
SP_WORK_FLOW_TIMEOUT = 100  # maximum time waiting for a complete answer of the board, in sec

LTA_BIN_FILE_SUFFIX = '.dat'
LTA_SOFT_MAXIMUM_BINARY_FILE_SIZE = 50000000 # maximum size of files in bytes
READOUT_TIMEOUT = 10.0 # maximum time between data packets, in seconds


### module exception
class LTAReadoutException(Exception):
    pass


class _pyLTA:

    def __init__(self, *args, **kwargs) -> None:

        self._image_name = 'image_lta'
        self._img_id = 0
        self._full_image_name = 'image_lta_0'

        self._connected = False

        self._sseq = SmartSequencer()
        self._sseq_hash = ''

        self._logger = logging.getLogger('pyLTA.unnamedLTA')
        self.output_dir = os.path.join(os.path.dirname(abs_path), 'bin_output')

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = value
        self._logger = logging.getLogger(f'pyLTA.{self._name}')
        if self._connected:
            self._readout_thread.name = value

    @property
    def output_dir(self):
        return self._output_dir
    
    @output_dir.setter
    def output_dir(self, new_output_dir: str):
        """The directory where the (binary) output will be produced."""
        self._output_dir = new_output_dir

        if not os.path.exists(new_output_dir):
            os.makedirs(new_output_dir)
            self._logger.info(f'Created new directory: {new_output_dir}')

        self._logger.info(f'Set output directory: {self._output_dir}')
        self.set_image_name(self._image_name)


    def connect(self, board_name: str, host_ip='192.168.133.100',
                  board_ip='192.168.133.7', board_port=2001,
                  nchannels=4):
        '''Establish communication with a specific LTA.

        Parameters
        ----------
        name : str
            A unique name for the target LTA. Used for logging purposes only.
        host_ip : str, optional
            The IP of the computer that is connecting to the LTA. Defaults to
            '192.168.133.100'.
        board_ip : str, optional
            The IP of the target LTA. Defaults to '192.168.133.7'.
        board_port : int, optional
            The port of the target LTA. Defaults to 2001.

        Other Parameters
        ----------------
        nchannels : int, optional
            The number of channels of the target LTA. Defaults to 4.
        '''

        # first disconnect previous connection
        self.disconnect()

        # now configure everything
        self.name = board_name
        self._nchannels = nchannels

        self._control_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._data_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        for sock in [self._control_socket, self._data_socket]:
            
            sock.bind((host_ip, 0))     # 0 to assign port automatically
            sock.connect((board_ip, int(board_port)))
            sock.settimeout(.8)
            self._logger.info(f'Created UDP socket: {sock.getsockname()}')

        flush(self._control_socket)
        self._eth = LTAEthernet(self._control_socket, self._data_socket, board_name)
        self._readout_thread = ReadoutThread(self.name, self._data_socket)

        self._connected = True


    def disconnect(self):
        '''Close the connection to the LTA. If not connected, nothing will
        happen.
        '''

        if not self._connected(): return

        self._eth._stop_idle_thread()
        self._control_socket.close()
        self._data_socket.close()

        self._connected = False


    def _assert_connected(self):
        
        if not self._connected:
            self._logger.error(f'pyLTA not connected. Please run ".connect()".')
            return True


    ### image naming
    def set_image_name(self, new_image_name: str, add_date=False):
        """Set the next image name.

        The next (binary) image will be saved to 
        {self.output_dir}/{new_image_name}_N.dat. `N` is the image id, a number
        starting at 0 and increasing with each consecutive image. This ensures
        that no images will be overwritten even if their name is the same.

        Parameters
        ----------
        new_image_name : str
            The name of the next image.
        add_date : bool, optional
            Whether to add the date to the prefix of the image name, in the 
            format `YYYY-mm-dd_HHMMSS_{new_image_name}`. Default: False.
        
        See also
        --------
        pyLTA.reset_image_id
        """
        # formatting
        if new_image_name[-1] != '_': new_image_name += '_'
        if add_date:
            new_image_name += datetime.now().strftime("%Y%m%d_%H%M%S_")

        self._image_name = new_image_name
        old_image_path = os.path.join(self._output_dir, self._full_image_name)

        while True: # do not overwrite, increase the image id
            full_image_name = new_image_name+f'{self._img_id}'
            if any([f.startswith(full_image_name) for f in os.listdir(self._output_dir)]):
                self._img_id += 1
            else: break

        self._full_image_name = full_image_name
        new_image_path = os.path.join(self._output_dir, full_image_name)
        if old_image_path != new_image_path:
            self._logger.info(f'New image path: {new_image_path}')


    def set_output_dir(self, new_output_dir: str):
        """Change the output directory, creating it if it does not exist.
        
        Parameters
        ----------
        new_output_dir : str
            The full path for the new output directory.
        """
        self.output_dir = new_output_dir


    def reset_image_id(self):
        """Set the image id to 0.
        
        Note that if this would produce a conflict with an existing image, the
        image id will be automatically increased until no more conflicts 
        appear.
        """
        self._img_id = 0

        self._logger.info(f'Reset image id')
        self.set_image_name(self._image_name)

    
    ### low-level communication with board
    def send(self, cmd: str):
        """Send a raw message to the LTA.
        
        If the command is "get [...]", return the LTA answer.

        Parameters
        ----------
        cmd : str
            The raw command that will be sent to the LTA.
        """
        if self._assert_connected(): return

        self._logger.info(f'Sending: {cmd}')

        # add the return character
        send_str = cmd + '\r'

        # communicate with board
        response = self._eth.send_and_recv(send_str, LTA_GEN_DONE_MESSAGE,
                                           SP_WORK_FLOW_TIMEOUT)
        response = response.strip()

        self._logger.info(f'Response: {response}')

        if 'get' in cmd:
            return response
    

    ### "high"-level commands
    def set_sequencer(self, sequencer_file: str):
        
        self._sseq.load(sequencer_file)


    def run_sequencer(self):
        """Only run the sequencer, without performing a readout.
        """
        if self._assert_connected(): return

        if not self._sseq._loaded:
            self._logger.error(f'Sequencer not loaded. Cannot run.')
            return

        self._logger.info(f'Starting sequencer. Duration: {print_time(self._sseq._total_duration)}')

        # stop sequencer
        self.send('sek reset')

        # preload sequencer
        self.send('sek preload')

        # wait for sequencer for preload
        time.sleep(.1)

        # if is_multi:
        #     self.send('sek sync_rdy')
        #     self.send('set syncStop 1')

        # else:
        self.send('sek start')


    def stop_sequencer(self):
        """Stop a running sequencer."""
        self._logger.info(f'Stopping sequencer by user request')

        # stop sequencer
        self.send('sek reset')

        # if is_multi:
        #     # reset syncStop
        #     self.send('set syncStop 0')

    
    def setv(self, vname: str, vval):
        """Set the internal or sequencer variable `vname` to `vval`.

        Parameters
        ----------
        vname : str
            The name of the internal or sequencer variable.
        vval : Any
            The new value of the internal or sequencer variable.

        Notes
        -----
        The function will automatically decide whether `vname` is an internal
        or sequencer variable. However, if one accidentally sets a variable in
        the sequencer that is named exactly as an internal variable, this
        function will only change the sequencer variable. Common practice is to
        assign capital letters to sequencer variables in order to avoid this.
        """
        # check if it is a sequencer variable
        if vname in self._sseq._vars_dict:
            self._sseq.change_value(vname, vval)

        # if it is not, treat it as internal variable
        else:
            self.send(f'set {vname} {vval}')


    def getv(self, vname: str):
        """Return the internal or sequencer variable `vname`.

        Parameters
        ----------
        vname : str
            The name of the internal or sequencer variable.

        Returns
        -------
        The value of the internal or sequencer variable.
            
        Notes
        -----
        The function will automatically decide whether `vname` is an internal
        or sequencer variable. However, if one accidentally sets a variable in
        the sequencer that is named exactly as an internal variable, this
        function will only return the value of the sequencer variable. Common
        practice is to assign capital letters to sequencer variables in order
        to avoid this.
        """
        # check if it is a sequencer variable
        if vname in self._sseq._vars_dict:
            return self._sseq.get_value(vname)

        # if it is not, treat it as internal variable
        else:
            return self.send(f'get {vname}')


    ### readout
    def start_readout(self):
        """Perform a readout with the loaded sequencer.

        Additionaly increase the image id, upload the sequencer if needed, save
        the sequencer hash and save all the internal and sequencer variables to
        a .hdr file.
        """
        # check configuration and sequencer are ok
        if self._assert_connected(): return

        if self._readout_thread.is_active():
            response = 'Readout thread is active. Failed to start readout.'
            self._logger.error(response)
            return

        if not self._sseq._loaded:
            self._logger.error(f'Sequencer not loaded. Cannot start readout.')
            return
        
        expected_samps = self._sseq.get_samps_per_channel() * self._nchannels

        # ensure the image name is loaded correctly and increase counter
        self.set_image_name(self._image_name)
        self._img_id += 1

        # apply changes to sequencer
        new_seq_hash = self._sseq.get_hash()
        if new_seq_hash != self._sseq_hash:

            self._sseq_hash = new_seq_hash
            self._upload_sequencer()

            hashed_seq_path = os.path.join(os.path.dirname(abs_path), 
                                           'hashed_sequencers', self._sseq_hash+'.xml')
            if not os.path.exists(hashed_seq_path):
                self._sseq.save(hashed_seq_path)

        # get board variables
        self._logger.info(f'Requesting firmware and telemetry variables')
        firmware_vars = self.send('get all')
        telemetry_vars = self.send('get telemetry all')

        hdr_file_name = os.path.join(self._output_dir, self._full_image_name+'.hdr')
        _make_hdr_file(hdr_file_name, firmware_vars, telemetry_vars, 
                       self._sseq._vars_dict, self._sseq_hash)

        # start the actual readout
        # start packer
        self.send('set packStart 1')

        output_file_name = os.path.join(self._output_dir, self._full_image_name)
        self._logger.info(f'Starting readout. Output file name: {output_file_name}')

        self._readout_thread.start(output_file_name, expected_samps, hdr_file_name)

        self.run_sequencer()
    

    def run_readout(self, decode=False):
        """Same as `<pyLTA.start_readout>`_ but block until the readout is done.

        If a keyboard interrupt (`ctrl-C`) happens, the function will stop
        blocking but the readout will continue.

        Parameters
        ----------
        decode : bool, optional
            Whether to call the decoder at the end of the readout.
            Default is False.
        """
        self.start_readout()
        self._logger.info('Waiting until readout thread exits.')

        try:
            self._readout_thread.join()
        except KeyboardInterrupt:
            self._logger.warning('Interrupted wait; readout in progress.')
        else:
            self._logger.info('Readout done!')

            if decode:
                from .lta_decoder import decode_bin
                self._logger.info('Decoding...')
                decode_bin(os.path.join(self._output_dir, self._full_image_name), self._nchannels, 
                        output_dir=self._output_dir)
                self._logger.info('Done decoding!')
            

    def stop_readout(self):
        """Stop the readout and the sequencer."""
        self._readout_thread.stop()
        
        # stop packer
        self.send('set packStart 0')

        # stop sequencer
        self.stop_sequencer()


    def _upload_sequencer(self):

        commands_to_send = self._sseq._command_list

        self._logger.info('Uploading new sequencer')

        # send commands to board
        self.send("sek reset")               # stop sequencer
        self.send('sek clear recipes')       # clear sequencer recipes
        self.send('sek clear dynamicVector') # clear sequencer dynamic vector

        for cmd in commands_to_send:
            self.send(cmd)


### "private" functions
# header
def _make_hdr_file(hdr_file_name: str, firmware_vars: str, telemetry_vars: str, sequencer_vars: dict, seq_hash: str):
    
    hdu = fits.PrimaryHDU()
    hdr = hdu.header
    
    update_hdr_card(hdr, 'SEQ_HASH', seq_hash, 'Sequencer hash')

    for key, value in sequencer_vars.items():
        update_hdr_card(hdr, key, value, 'Smart sequencer variable')

    firmware_vars_list = [s.split('=') for s in firmware_vars.split('\r\n') if '=' in s]
    for item in firmware_vars_list:
        key, value = item
        update_hdr_card(hdr, key.strip(), value.strip(), 'Firmware variable')

    telemetry_vars_list = [s.split('=') for s in telemetry_vars.split('\r\n') if '=' in s]
    for item in telemetry_vars_list:
        key, value = item
        update_hdr_card(hdr, key.strip(), value.strip(), 'Telemetry variable')

    hdr.tofile(hdr_file_name)
    
    logger.info(f'Created header file: {hdr_file_name}')


def _write_timestamp(hdr_file_name, flag):

    timestamp = datetime.now().isoformat(timespec='seconds')
    update_hdr_file(hdr_file_name, f'date{flag}', timestamp, f"Timestamp at {flag} of readout")


class ReadoutThread:
    
    def __init__(self, name, data_socket: socket.socket) -> None:

        self._t = threading.Thread(name=name)
        self._t.run()

        self.name = name
        self._event = threading.Event()
        self._data_socket = data_socket
        
        self._bin_file_names = []
        self._readout_status = [0]

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = value
        self._logger = logging.getLogger(f'pyLTA.{self._name}.rt')


    def start(self, out_file_name, expected_samps, hdr_file_name):

        if self.is_active():
            response = 'Readout thread is active. Failed to start readout.'
            self._logger.error(response)
            raise LTAReadoutException(response)
        
        self._event.set()  # set Event to True

        # clear list of binary files
        self._bin_file_names.clear()

        # create readout thread
        self._t = threading.Thread(target=self._dump_data, 
                                   args=(out_file_name, expected_samps, hdr_file_name), 
                                   daemon=True)

        # start
        self._logger.info('Starting readout thread')
        self._t.start()

        while self._readout_status[0] != 1:    # wait until readout thread starts
            time.sleep(.01)


    def stop(self):

        if self.is_active():
            self._logger.info('Requesting readout thread to exit')
            self._event.clear()
            self._t.join()


    def join(self):
        while self._readout_status[0] != 0:
            time.sleep(.1)


    def is_active(self):
        return self._readout_status[0] != 0


    # fits files
    def _create_bin_file(self, file_name: str, numbering: int):
        
        new_file_name = file_name + f'_{numbering}{LTA_BIN_FILE_SUFFIX}'
        
        if os.path.exists(new_file_name):
            logger.warning(f'Will overwrite existing binary file {new_file_name}')
            os.remove(new_file_name)

        try:
            out_file = open(new_file_name, 'xb')
        except Exception as e:
            self._logger.error(f'Cannot create file {new_file_name} to save data. Exiting.')
            raise LTAReadoutException(e)
        
        self._bin_file_names.append(new_file_name)
        self._logger.info(f'Created file: {new_file_name}')

        return out_file


    # readout thread main function
    def _dump_data(self, out_file_name, expected_samps, hdr_file_name):

        current_subrun_number = 0
        
        out_file = self._create_bin_file(out_file_name, current_subrun_number)

        # clear stale data from the socket
        flush(self._data_socket)

        # write timestamp at start of readout
        _write_timestamp(hdr_file_name, 'start')

        self._readout_status[0] = 1
        self._logger.info('Readout thread is ready for data')

        this_file_bytes = 0
        packet_count = 0
        read_samps = 0
        
        timeout_time = time.monotonic() + READOUT_TIMEOUT

        # start receiving data from ethernet
        while self._event.is_set():

            if LTA_SOFT_MAXIMUM_BINARY_FILE_SIZE > 0:
                if this_file_bytes >= LTA_SOFT_MAXIMUM_BINARY_FILE_SIZE:
                    out_file.close()
                    current_subrun_number += 1
                    out_file = self._create_bin_file(out_file_name, current_subrun_number)
                    this_file_bytes = 0
            
            try:
                data, client_addr = self._data_socket.recvfrom(LTA_SOFT_DATABUFF_SIZE)

            except TimeoutError:

                if self._readout_status[0] == 2:
                    
                    # if we have the correct amount of data, we are happy to end the thread
                    if read_samps == expected_samps:
                        self._logger.info('Received all expected data')
                        self._readout_status[0] = 3
                        break              
                    
            except Exception as e:
                self._logger.warning(f'Error on data port: {e}')

            else:
                n_rec_bytes = len(data)

                if n_rec_bytes > 0:
                    if self._readout_status[0] == 1:
                        self._logger.info('First data packet received')

                    self._readout_status[0] = 2

                    timeout_time = time.monotonic() + READOUT_TIMEOUT   # extend the timeout

                    # write the number of quadwords in the udp package before saving the data
                    if n_rec_bytes%8 != 2:
                        self._logger.warning(f'Unexpected packet size: {n_rec_bytes} (should normally be 2 mod 8)')
                    
                    quad_words_count = (n_rec_bytes-2)//8

                    out_file.write(struct.pack('<B', quad_words_count))
                    out_file.write(data)

                    packet_count += 1
                    this_file_bytes += n_rec_bytes
                    read_samps += quad_words_count

            finally:
                # end the thread if the timeout is reached
                if time.monotonic()>timeout_time:
                    self._logger.info(f"No data in a while: readout done? we got {read_samps} samples, expected {expected_samps}")
                    self._readout_status[0] = 3
                    break

        out_file.close()
        self._logger.info(f'Readout thread exiting, got {read_samps} samples')

        # write timestamp at end of readout
        _write_timestamp(hdr_file_name, 'end')

        update_hdr_file(hdr_file_name, 'NPIX', read_samps, "Pixels read by LTA")
        self._readout_status[0] = 0


class pyLTA(_pyLTA):
    """
    High-level object used to communicate with an LTA.

    Attributes
    ----------
    voltage_shortcuts: dict
        A dictionary whose keys are abbreviations for a list of voltages
        (for example, "vh" is an abbreviation for ['v1ah', 'v1bh', 'v2ch',
        'v3ah', 'v3bh']).
    switch_shortcuts: dict
        A dictionary whose keys are abbreviations for a list of switches
        (for example, "pm15v" is an abbreviation for ['p15v_sw', 'm15v_sw']).
    output_dir

    Notes
    -----
    The `args` and `kwargs` arguments are currently ignored, although they may be
    used in the future.
    """
    
    def __init__(self, *args, **kwargs) -> None:

        super().__init__(*args, **kwargs)

        self.voltage_shortcuts = {
                        'vh': ['v1ah', 'v1bh', 'v2ch', 'v3ah', 'v3bh'],
                        'vl': ['v1al', 'v1bl', 'v2cl', 'v3al', 'v3bl'],
                        'hh': ['h1ah', 'h1bh', 'h2ch', 'h3ah', 'h3bh'],
                        'hl': ['h1al', 'h1bl', 'h2cl', 'h3al', 'h3bl'],
                        'th': ['tgah', 'tgbh'], 
                        'tl': ['tgal', 'tgbl'], 
                        'sh': ['swah', 'swbh'], 
                        'sl': ['swal', 'swbl'],
                        'rh': ['rgah', 'rgbh'], 
                        'rl': ['rgal', 'rgbl'],
                        'oh': ['ogah', 'ogbh'], 
                        'ol': ['ogal', 'ogbl'], 
                        'dh': ['dgah', 'dgbh'], 
                        'dl': ['dgal', 'dgbl']}
        
        self.switch_shortcuts = {
                        'pm15v': ['p15v_sw', 'm15v_sw'],
                        'bias': ['vdrain_sw', 'vdd_sw', 'vsub_sw', 'vr_sw']}
        
        self.run_log = None


    ### voltages
    def set_voltages(self, v_dict: dict):
        """Load voltages and send them to LTA from dictionary `v_dict`.
        
        Parameters
        ----------
        v_dict : dict
            The dictionary, in the form {`key`: `value`} where `key` is a 
            voltage name or shortcut.

        See also
        --------
        pyLTA.voltage_shortcuts
        """
        for key, val in v_dict.items():
            if key in self.voltage_shortcuts:
                for vname in self.voltage_shortcuts[key]:
                    self.setv(vname, val)
            else:
                self.setv(key, val)


    ### switches
    def enable_15v_switches(self):
        """Set 15V switches to 1."""
        for key in self.switch_shortcuts['pm15v']:
            self.setv(key, 1)


    def disable_15v_switches(self):
        """Set 15V switches to 0."""
        for key in self.switch_shortcuts['pm15v']:
            self.setv(key, 0)


    def enable_bias_switches(self):
        """Set bias switches to 1."""
        for key in self.switch_shortcuts['bias']:
            self.setv(key, 1)
    

    def disable_bias_switches(self):
        """Set bias switches to 0."""
        for key in self.switch_shortcuts['bias']:
            self.setv(key, 0)


    ### board configuration
    def load_config(self, config_file_name, apply=True):
        """Load a configuration from a .ini file.
        
        Parameters
        ----------
        config_file_name: str or Path
            Full path of the .ini file.
        apply: bool, optional
            Whether to apply the configuration immediately. If False, only
            applies the "NETWORK" section to connect to the LTA, and saves the
            rest of the information in an internal dictionary. Default is True.

        Notes
        -----
        The file should be formatted as described in the `configparser
        <https://docs.python.org/3/library/configparser.html>`_ module. Valid
        sections and options are shown in the example below, although all are
        optional::

            [NETWORK]
            # board_name = 
            # host_ip = 
            # board_ip = 
            # board_port = 
            [SEQUENCER] # full path of the sequencer you want to use.
            # sequencer = path/to/sequencer.xml
            [CDS] # LTA internal variables, such as psamp, ssamp, sinit, pinit, etc.
            # psamp =
            # ssamp =
            [VOLTAGES] # Can be voltage shortcuts or the actual variable
            # vsub = 
            # vr = 
            # vh = 
            # vl = 
        
        See also
        --------
        pyLTA.voltage_shortcuts
        pyLTA.apply_config
        pyLTA.connect
        """
        config = configparser.ConfigParser(inline_comment_prefixes=[';', '#'])
        self._logger.info(f'Loading config from {config_file_name}')

        try:
            with open(config_file_name) as f:
                config.read_file(f)
        except FileNotFoundError:
            self._logger.error(f'No such config file: {config_file_name}')
            return
        
        s = 'Loaded configuration file:\n'
        for section_name, section in config.items():
            s += section_name + '\n'
            s += '-' * len(section_name) + '\n'
            for option, val in section.items():
                s += f'  {option}={val}\n'
        self._logger.info(s)

        self.config = config

        # connect to the LTA if the correct option is defined
        if config.has_option('NETWORK', 'board_name'):
            self.connect(**config['NETWORK'])

        if apply: self.apply_config()


    def apply_config(self):
        """Apply the configuration loaded by ``pyLTA.load_config``.
        
        See also
        --------
        pyLTA.load_config
        """
        if self.config is None:
            self._logger.error('Configuration not loaded - cannot apply.')
            return

        for section_name, section in self.config.items():

            if section_name == 'VOLTAGES':
                self.set_voltages(section)
            
            elif section_name == 'SEQUENCER':
                for option, val in section.items():
                    if option == 'sequencer':
                        self.set_sequencer(val)
                    else: self._logger.warning(f'Ignored option {option} under section "SEQUENCER"')
            
            elif section_name == 'CDS':
                for option, val in section.items():
                    self.setv(option, val)


    def set_sequencer(self, sequencer_file: str, upload=False):
        """Set a sequencer from an XML file.

        Additionally, write the sequencer file name to the run log.

        Parameters
        ----------
        sequencer_file : str or Path
            The full path of the XML file of the sequencer.
        upload : bool
            Whether to upload the sequencer to the LTA. Default is False.
        
        Notes
        -----
        Sending the sequencer to the LTA takes some time. Usually, one will
        change some sequencer variables before starting a readout, therefore
        it is not desired to upload the sequencer each time a variable is
        modified. To solve this, by default the sequencer will only be uploaded
        just before the readout starts. If you only want to run the sequencer
        without performing a readout, set `upload` to True.
        """
        super().set_sequencer(sequencer_file)
        if upload:
            self._upload_sequencer()
        self.write_run_log(f'sequencer: {sequencer_file}')


    ### run settings
    def set_run(self, run_name, user, comment=None, run_dir=None, 
                add_date=True):
        """Set the run name.
        
        A run is a group of images taken in a specific context, so they are
        saved to the same directory. The output directory will be defined
        according to the `run_dir`, `add_date` and `run_name` parameters.
        Creates a run log named `run_{self.name}.dat` in the output directory.
        The `user` and `comment` information will be added to the run log.

        Parameters
        ----------
        run_name : str
            A descriptive name of the run.
        user : str
            The name of the user who set the run.
        comment : str, optional
            A description of the run.
        run_dir : str or Path, optional
            The directory in which the run folder will be created. Defaults to
            the previous run directory, or to ``self.output_dir``.
        add_date : bool, optional
            Whether to add a date to the output directory, in the format
            YYYY-mm-dd-{run_name}. Defaults to True.

        See also
        --------
        pyLTA.set_output_dir
        """
        if add_date:
            run_name = datetime.now().strftime("%Y-%m-%d-") + run_name
        
        if run_dir is None:
            run_dir = os.path.dirname(self.output_dir)
        self.set_output_dir(os.path.join(run_dir, run_name))

        # create the run_{ccd_client}.dat (run_log) file
        self.run_log = os.path.join(self._output_dir, f'run_{self.name}.dat')
        self.write_run_log(f'Run initiated by user {user}')
        if comment:
            self.write_run_log(f'comment: {comment}')


    def write_run_log(self, text: str):
        """Write an entry to the run log.
        
        The run log is located at `{self.output_dir}/run_{self.name}.dat`. Each
        entry will be added in the format `ỲYYY-mm-dd HH:MM:SS - text`.

        Parameters
        ----------
        text : str
            The text that will be added to the log.
        """
        if self.run_log is None:
            return
        
        s = datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' - '+text+'\n'

        with open(self.run_log, 'a') as f:
            f.write(s)


    ### image
    def take_image(self, name, add_date=True, decode=True, **other_params):
        """Set the image name and start a readout, waiting until completion.

        Additionally, write an entry to the run log with the image name, and
        if `libABCD <https://gitlab.com/bertou/libabcd>`_ is initialized, send
        the image name to the topic "{self.name}/done".

        Parameters
        ----------
        name : str
            The prefix of the image.
        add_date : bool, optional
            Whether to add the date to the prefix of the image name, in the 
            format `YYYY-mm-dd_HHMMSS_{name}`. Default: True.
        decode : bool, optional
            Whether to automatically decode the image at the end of the
            readout. Default: True.
        
        Other parameters
        ----------------
        **other_params : dict, optional
            Additional parameters that will be changed before the readout.
            These can be sequencer variables, e.g. `NSAMP=400`, or internal
            variables, e.g. `ssamp=200`.
        """
        self.set_image_name(name, add_date)
        for key, val in other_params.items():
            self.setv(key, val)

        self.run_readout(decode=decode)

        # send the image name to run.dat
        self.write_run_log(f'image: {self._full_image_name}')

        if _libABCD_loaded and libABCD.mqttp:
            # send the image name via MQTT so that the image builder gets it
            libABCD.publish(f'{self.name}/done', self._full_image_name)
        

    def erase_epurge(self):
        """Execute `ccd_erase` and `ccd_epurge` routines.

        Additionally, write to the run log this information.
        """
        self.write_run_log('ccd erase + ccd epurge')
        self.send('exec ccd_erase')
        self.send('exec ccd_epurge')


    def shutdown_ccd(self):
        """Set `vsub` to 7 (the minimum value in LTAv2) and disable the bias
        switches.

        See also
        --------
        pyLTA.disable_bias_switches
        """
        # hard-coded: set vsub to minimum value
        self.setv('vsub', 7)
        self.disable_bias_switches()


    ### emergency
    def emergency_stop(self):
        '''Stop the current readout and then shutdown the CCD.

        See also
        --------
        pyLTA.stop_readout
        pyLTA.shutdown_ccd
        '''
        self.stop_readout()
        self.shutdown_ccd()
        