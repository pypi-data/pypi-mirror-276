import configparser, json, logging, os, socket
from datetime import datetime


try:
    import libABCD
    _libABCD_loaded = True

except: _libABCD_loaded = False


### python version of Linux nc, copied from some forum
def nc(hostname, port, content):

    # create the connection and send the data
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((hostname,port))
        s.sendall(content)
        s.shutdown(socket.SHUT_WR)

        # listen to the answer
        d_data_s = ''
        while True:
            s.settimeout(1)
            try:
                data = s.recv(4096)
            except socket.timeout:
                pass
            else:
                if data == b'':
                    break
                d_data = data.decode()
                d_data_s += d_data

        # return the answer
        return d_data_s
    

class legacyLTA():

    def __init__(self, name='', json_file=None, **kwargs):

        ### default values
        self.name = name
        # communication variables
        self.hostname = 'localhost'
        self.port = 8888

        # Voltages and switches
        self.voltage_keys = ['v1ah', 'v1bh', 'v2ch', 'v3ah', 'v3bh', 
                        'v1al', 'v1bl', 'v2cl', 'v3al', 'v3bl',
                        'h1ah', 'h1bh', 'h2ch', 'h3ah', 'h3bh',
                        'h1al', 'h1bl', 'h2cl', 'h3al', 'h3bl',
                        'tgah', 'tgbh', 
                        'tgal', 'tgbl', 
                        'swah', 'swal', 
                        'swbh', 'swbl',
                        'rgah', 'rgbh', 
                        'rgal', 'rgbl',
                        'ogah', 'ogbh', 
                        'ogal', 'ogbl', 
                        'dgah', 'dgbh', 
                        'dgal', 'dgbl', 
                        'vdrain', 'vdd', 'vr', 'vsub']
        
        self.switch_keys = ['p15v_sw', 'm15v_sw', 
                       'vdrain_sw', 'vdd_sw', 'vsub_sw', 'vr_sw']

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
        
        self.logger = logging.getLogger(__name__+'.lta')

        ### user-defined values
        if json_file: self.init_from_json(json_file)
        else: self.init(**kwargs)

        ### configuration variables
        self.config = None

        ### path
        self.cwd = None
        self.run_log = None
        self.run_dir = None
        self.img_name = None

        
    ### when the object is called, it redirects arguments to LTA daemon
    def __call__(self, *args, **kwargs):
        self.send(*args, **kwargs)

    
    ### set or change initialization parameters
    @property
    def voltage_keys(self):
        return self._voltage_keys
    
    @voltage_keys.setter
    def voltage_keys(self, value):
        self._voltage_keys = value
        self.voltages = {key: None for key in self.voltage_keys}
    
    @property
    def switch_keys(self):
        return self._switch_keys
    
    @switch_keys.setter
    def switch_keys(self, value):
        self._switch_keys = value
        self.switches = {key: None for key in self.switch_keys}


    def init(self, **kwargs):
        
        for key, val in kwargs.items():
            if key == 'name':
                self.name = val

            if key == 'hostname':
                self.hostname = val

            if key == 'port':
                self.port = val

            if key == 'voltage_shortcuts':
                self.voltage_shortcuts = val

            if key == 'switch_shortcuts':
                self.switch_shortcuts = val
            
            if key == 'voltage_keys':
                self.voltage_keys = val

            if key == 'switch_keys':
                self.switch_keys = val


    def init_from_json(self, json_file):
        
        with open(json_file, 'r') as f:
            init_dict = json.load(f)

        self.init(**init_dict)
            

    ### communicate with LTA daemon
    def send(self, s: str):
        '''Send command `s` to the LTA daemon through TCP port'''

        self.logger.info(f'Sending: {s}')
        try:
            answer = nc(self.hostname, self.port, s.encode())
            
        except ConnectionRefusedError:
            self.logger.warning("Connection to port Refused")
            return None

        else:
            self.logger.info(f'Answer: {answer}')

    
    def set(self, name, value):
        '''Send `lta set <name> <value>`. 
        If <name> is in the voltages key list, update its value too.'''

        if name in self.voltages:
            self.voltages[name] = value
        elif name in self.switches:
            self.switches[name] = value
        self.send(f'set {name} {value}')

    
    ### voltages
    def set_voltages(self, v_dict: dict):
        '''Load voltages and send them to LTA from dictionary 
        `v_dict`'''

        for key, val in v_dict.items():
            if key in self.voltages:
                self.set(key, val)

            elif key in self.voltage_shortcuts:
                for vname in self.voltage_shortcuts[key]:
                    self.set(vname, val)
            else:
                self.logger.warning(f'Don\'t know what to do with voltage key {key}. Ignoring.')


    ### switches
    def enable_15v_switches(self):
        
        for key in self.switch_shortcuts['pm15v']:
            self.set(key, 1)


    def disable_15v_switches(self):
        
        for key in self.switch_shortcuts['pm15v']:
            self.set(key, 0)


    def enable_bias_switches(self):
        
        for key in self.switch_shortcuts['bias']:
            self.set(key, 1)
    

    def disable_bias_switches(self):
        
        for key in self.switch_shortcuts['bias']:
            self.set(key, 0)


    ### board configuration
    def load_config(self, config_file_name, apply=True):

        config = configparser.ConfigParser(inline_comment_prefixes=[';', '#'])
        self.logger.info(f'Loading config from {config_file_name}')

        try:
            with open(config_file_name) as f:
                config.read_file(f)
        except FileNotFoundError:
            self.logger.error(f'No such config file: {config_file_name}')
            return
        
        s = 'Loaded configuration file:\n'
        for section_name, section in config.items():
            s += section_name + '\n'
            s += '-' * len(section_name) + '\n'
            for option, val in section.items():
                s += f'  {option}={val}\n'
        self.logger.info(s)

        self.config = config

        if apply: self.apply_config()


    def apply_config(self):

        if self.config is None:
            self.logger.error('Configuration not loaded - cannot apply.')
            return

        for section_name, section in self.config.items():

            if section_name == 'VOLTAGES':
                self.set_voltages(section)
            
            elif section_name == 'SEQUENCER':
                for option, val in section.items():
                    if option == 'sequencer':
                        self.set_sequencer(val)
                    else: self.logger.warning(f'Ignored option {option} under section "SEQUENCER"')
            
            elif section_name == 'CDS':
                for option, val in section.items():
                    self.set(option, val)


    def set_sequencer(self, sequencer_file_name):
        
        self.send('sseq ' + sequencer_file_name)
        self.logger.info(f'loaded sequencer: {sequencer_file_name}')

        self.write_run_log(f'sequencer: {sequencer_file_name}')


    ### run settings
    def set_run(self, run_name, user, comment=None, run_dir=None):
        
        self.run_name = datetime.now().strftime("%Y-%m-%d-") + run_name
        self.cwd = os.path.join(run_dir, self.run_name)

        # create working directory
        os.makedirs(self.cwd, exist_ok=True)

        self.logger.info(f'Changed working directory to {self.cwd}')

        # create the run_{ccd_client}.dat (run_log) file
        self.run_log = os.path.join(self.cwd, f'run_{self.name}.dat')
        self.write_run_log(f'Run initiated by user {user}')
        if comment:
            self.write_run_log(f'comment: {comment}')


    def write_run_log(self, s: str):
        
        if self.run_log is None:
            return
        
        s = datetime.now().strftime('%Y%m%d %H%M%S')+' - '+s+'\n'

        with open(self.run_log, 'a') as f:
            f.write(s)


    ### image settings
    def set_image_name(self, name, add_date):
        
        # add a trailing underscore if needed
        if name[-1] != '_': name += '_'

        self.img_name = name
        if add_date:
            self.img_name = name + datetime.now().strftime("%Y%m%d_%H%M%S_")

        # send the image name to the LTA
        self.send('name '+os.path.join(self.cwd, self.img_name))


    # high-level API
    def take_image(self, name, add_date=True, **seq_vars):
        
        self.set_image_name(name, add_date)
        for key, val in seq_vars.items():
            self.send(f'{key} {val}')

        self.logger.info(f'Starting taking image {self.img_name}')
        self.send('read')
        self.logger.info(f'Done taking image {self.img_name}')

        # send the image name to run.dat
        self.write_run_log(f'image: {self.img_name}')

        # send the image name via MQTT so that the image builder gets it
        if _libABCD_loaded and libABCD.mqttp:
            libABCD.publish('lta/done', self.img_name)


    def erase_epurge(self):

        self.write_run_log('ccd erase + ccd epurge')
        self.send('exec ccd_erase')
        self.send('exec ccd_epurge')


    def shutdown_skipper(self):

        # hard-coded: set vsub to minimum value
        self.set('vsub', 7)
        self.disable_bias_switches()

    
    # regular and emergency stops (needed for compatibility with CDAQ)
    def stop_current(self):
        self.logger.warning(f'Cannot "stop_current" in LTA. Ignoring.')

    def emergency_stop(self):
        self.shutdown_skipper()
