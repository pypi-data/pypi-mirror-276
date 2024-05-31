import xml.etree.ElementTree as ET
from ._auxiliary import print_time
import logging, os, zlib

### module logger
logger = logging.getLogger('pyLTA.sseq_handler')


### module constants
SEQ_CONVENTION_READ_NSAMP_NUMBER = "NSAMP"
SEQ_CONVENTION_READ_ROWS_NUMBER = "NROW"
SEQ_CONVENTION_READ_COLS_NUMBER = "NCOL"

SMART_NO_EXTRA_LEVEL_ID = -1


### generic functions
def _parse_words(s: str or None, delim: str): # type: ignore
    if s is None:
        return []
    return [ v for f in s.split(delim) for v in f.split()]


### module exception
class SequencerException(Exception):
    pass


### module main class
class SmartSequencer:

    def __init__(self) -> None:
        self._reset()


    def _reset(self):

        self._name = ''
        self._loaded = False
        self._total_duration = -1

        self._element = ET.Element('sseq')
        self._recipe_dict = {}
        self._vars_dict = {}
        self._states_dict = {}
        self._dyn_vars_dict = {}
        self._active_dyn_var = ''
        self._loaded_rec_list = []
        self._duration_list = []

        self._command_list = []

    
    def load(self, sequencer_file_name: str):

        logger.info(f'Attempting to load: {sequencer_file_name}')

        self._reset()

        # Load the given file
        try:
            with open(sequencer_file_name, 'r') as f:
                readFile = f.read()
        except Exception as e:
            logger.error(f'Could not read sequencer file: {e}')
            return -1
        
        # To parse a sequencer to XML, we need to add a <root> at the beginning
        # and </root> at the end
        outFile = '<sseq>\n' + readFile + '</sseq>\n'

        try:
            self._element = ET.fromstring(outFile)
        except Exception as e:
            logger.error(f'Could not parse the XML file: {e}')
            return -1
        
        try:
            # translate variables
            _load_variables(self)

            # translate dynamic array
            _load_dynamic_variables(self)

            # translate recipes
            _load_recipes(self)

            # translate sequence
            _load_sequence(self)

            # calculate the time it will take to execute the sequencer
            _calculate_sequencer_duration(self)
        
        except SequencerException as e:
            logger.error(f'Could not load sequencer: {e}')
            self._reset()
            return -1
        
        else:
            # if we made it here without a SequencerException, we are good
            self._loaded = True
            self._name = os.path.basename(sequencer_file_name.rpartition('.')[0])
            _make_commands_to_board(self)
            logger.info('Sequencer loaded correctly')
  

    def print_duration(self, verbose=True):
        _print_sequencer_duration(self, verbose)


    def get_samps_per_channel(self):
    
        ncols = int(_resolve_var(self, SEQ_CONVENTION_READ_COLS_NUMBER))
        nrows = int(_resolve_var(self, SEQ_CONVENTION_READ_ROWS_NUMBER))
        nsamp = int(_resolve_var(self, SEQ_CONVENTION_READ_NSAMP_NUMBER))

        return ncols*nrows*nsamp


    def has_dynamic_var(self):
        return self._active_dyn_var != ''


    def print(self):

        s =  'VARIABLES: \n'
        s += '----------\n\n'
        for key, val in self._vars_dict.items():
            s += f'{key} {val}\n'
        s += '\n\n'

        s += 'STATES: \n'
        s += '-------\n\n'
        for key, val in self._states_dict.items():
            s += f'{key} {val}\n'
        s += '\n\n'

        s += 'DYNAMIC VARIABLES: \n'
        s += '------------------\n\n'
        for key, vals in self._dyn_vars_dict.items():
            s += f'{key}= [ '
            for val in vals:
                s += f'{val} '
            s += '] \n\n'
        
        s += f'ACTIVE DYNAMIC VARIABLE: {self._active_dyn_var}\n\n'

        s += 'RECIPE DEFINITION: \n'
        s += '------------------\n\n'
        for key, vals in self._recipe_dict.items():
            s += f'{key}= '
            for val in vals:
                s += f'{val["state"]}({val["delay"]})'
            s += '\n'
        s += '\n'

        s += 'SEQUENCE DEFINITION: \n'
        s += '--------------------\n\n'

        s += '   RECIPE STRUCT DEFINITION \n\n'

        for i, recipe in enumerate(self._loaded_rec_list):
            s += f'\t ------ {i} ------\n'
            for key, val in recipe.items():
                ss = f'"{key}"'
                s += f'\t {ss:20}: {val}\n'

            s += '\t -----------------------------------------------------\n\n'
        
        ### XXX print somewhere else? give option?
        print(s)


    def get_value(self, var_name):

        if var_name not in self._vars_dict:
            logger.error(f'Cannot get {var_name}: not a sequencer variable')
            return

        return _resolve_var(self, var_name)


    def change_value(self, var_name, new_val):

        if var_name not in self._vars_dict:
            logger.error(f'Cannot change {var_name}: not a sequencer variable')
            return
        
        old_val = self._vars_dict[var_name]

        if new_val != old_val:
            logger.info(f'Changing sequencer variable: {var_name} = {new_val} (previously {old_val})')
            self._vars_dict[var_name] = new_val
            # update sequence element
            for var in self._element.find('variables'):
                if var.get('name') == var_name:
                    var.set('val', str(new_val))    # has to be a string or the hash will break
            _calculate_sequencer_duration(self)
            _make_commands_to_board(self)


    def get_hash(self):

        seq_bytes = ET.tostring(self._element)[8:-8]    # ignore the added '<sseq>\n...<\sseq>\n'
        seq_hash = hex(zlib.crc32(seq_bytes))[2:]   # trim '0x'
        return seq_hash


    def save(self, file_name: str):

        seq_bytes = ET.tostring(self._element)[8:-8]
        with open(file_name, 'x') as f:
            f.write(seq_bytes.decode())


### "private" functions
def _load_variables(sseq: SmartSequencer):

    variables = sseq._element.find('variables')
    if variables is None:
        raise SequencerException('Missing "variables" in sequencer file.')
    
    for var in variables:

        typeStr = var.tag
        nameStr = var.get('name')
        valStr = var.get('val')

        if typeStr == 'var': 
            d = sseq._vars_dict
        elif typeStr == 'state':
            d = sseq._states_dict
        else: continue

        d[nameStr] = valStr
    
    mandatory_vars = [SEQ_CONVENTION_READ_COLS_NUMBER, 
                      SEQ_CONVENTION_READ_ROWS_NUMBER, 
                      SEQ_CONVENTION_READ_NSAMP_NUMBER]

    for v in mandatory_vars:
        if v not in sseq._vars_dict:
            raise SequencerException(f'"{v}" missing in sequencer')


def _load_dynamic_variables(sseq: SmartSequencer):

    dvars = sseq._element.find('dynamicVariables')
    if dvars is None:
        raise SequencerException('Missing "dynamicVariables" in sequencer file.')
    
    for dvar in dvars:
        name = dvar.get('name')
        vals = dvar.get('vals')

        sseq._dyn_vars_dict[name] = _parse_words(vals, ',')


def _load_recipes(sseq: SmartSequencer):

    recipes = sseq._element.find('recipes')
    if recipes is None:
        raise SequencerException('Missing "recipes" in sequencer file.')
    
    for recipe in recipes:
        nameStr = recipe.get('name')
        steps = []
        for step in recipe:
            stateStr = step.get('state')
            delayStr = step.get('delay')
            steps.append({'state': stateStr, 'delay': delayStr})
        sseq._recipe_dict[nameStr] = steps


def _parse_recipe_recursive(sseq: SmartSequencer, recipe: ET.Element):
    '''Populate several fields in the recipe list recursively'''
    
    # initialize 'mother' field
    if len(sseq._loaded_rec_list) == 0: motherId = SMART_NO_EXTRA_LEVEL_ID
    else: motherId = len(sseq._loaded_rec_list) - 1

    for step in recipe:

        # check if recipe exists
        recipe_name = step.get('name')
        if recipe_name not in sseq._recipe_dict:
            raise SequencerException(f'Recipe "{recipe_name}" does not exist')

        # create recipe dictionary
        recipe_dict = {'recipe_name': recipe_name,
                       'mother': motherId,
                       'daughter': SMART_NO_EXTRA_LEVEL_ID,
                       'sister': SMART_NO_EXTRA_LEVEL_ID,
                       'times_to_execute': '',
                       'is_dynamic': False,
                       'ncluster': [],
                       'id_depend': []}

        times_string = step.get('n')

        if times_string in sseq._dyn_vars_dict: # it's a dynamic variable

            recipe_dict['times_to_execute'] = '-1'
            recipe_dict['is_dynamic'] = True
            if sseq._active_dyn_var != '':
                raise SequencerException('Multiple recipes with dynamic variables')
            
            sseq._active_dyn_var = times_string

            # parse dynamic variable usage
            dynIndUpdateValue = _parse_words(step.get('ncluster'), ',')
            parentIndex = len(sseq._loaded_rec_list) - 1

            for dynVal in dynIndUpdateValue: # look up the parents of this pseudorecipe, the dynamic var depends on them
                parentIndex = sseq._loaded_rec_list[parentIndex]['mother']
                recipe_dict['ncluster'].append(dynVal)
                recipe_dict['id_depend'].append(parentIndex)
        
        else:   # it is either an integer or a non-dynamic variable reference
            recipe_dict['times_to_execute'] = times_string

        sseq._loaded_rec_list.append(recipe_dict)
        _parse_recipe_recursive(sseq, step)


def _parse_recipes(sseq: SmartSequencer, sequenceElement):
    '''Populate the loaded recipes list. Each recipe will be a dictionary '''
    
    # populate the recipe list
    _parse_recipe_recursive(sseq, sequenceElement)
    
    # iterate through each recipe to get 'sister' and 'daughter' values
    for i, this_recipe in enumerate(sseq._loaded_rec_list):

        if i == len(sseq._loaded_rec_list)-1: break

        if sseq._loaded_rec_list[i+1]['mother'] == i: 
            this_recipe['daughter'] = i+1
        
        for j, other_recipe in enumerate(sseq._loaded_rec_list[i+1:]):
            if other_recipe['mother'] == this_recipe['mother']:
                this_recipe['sister'] = i+1+j
                break


def _load_sequence(sseq: SmartSequencer):
    '''Convert the XML <sequence> element into a recipe list formatted for the LTA'''
    
    sequenceElement = sseq._element.find('sequence')
    if sequenceElement is None:
        raise SequencerException('Missing "sequence" in sequencer file.')

    if len(sequenceElement) == 0:
        raise SequencerException('Sequence element has no child element')
    
    _parse_recipes(sseq, sequenceElement)


def _calculate_pseudo_recipe_duration(sseq: SmartSequencer, pseudo_recipe: dict):
    
    recipe = sseq._recipe_dict[pseudo_recipe["recipe_name"]]
    total_time = 0
    for step in recipe:
        total_time += float(_resolve_var(sseq, step["delay"]))
    return total_time


def _print_sequencer_duration(sseq: SmartSequencer, verbose):

    s =  '============================\n'
    s += f'Loaded sequencer: {sseq._name}\n\n'

    if verbose:
        s +=   'Calculation of seq duration:\n'

        for i, lrec in enumerate(sseq._duration_list):
            indent = ' '*lrec['nest depth']*5
            s += indent + f'({i+1}) {lrec["recipe name"]}\n'
            s += indent + f' -step duration:          {lrec["step duration"]}\n'
            s += indent + f' -total times to execute: {lrec["total times to execute"]}\n'
            s += indent + f' -total recipe duration:  {lrec["total recipe duration"]}\n'

    s += f'\nTotal duration: {print_time(sseq._total_duration)}\n'
    s += '============================\n'

    print(s)


def _calculate_sequencer_duration(sseq: SmartSequencer):
    
    clock_duration = 1/15e6   # seconds (clock runs at 15 MHz)
    total_duration = 0
    sseq._duration_list.clear()

    for i, lrec in enumerate(sseq._loaded_rec_list):

        total_times_to_execute = int(_resolve_var(sseq, lrec['times_to_execute']))
        mother_id = lrec['mother']
        nest_depth = 0

        while mother_id != SMART_NO_EXTRA_LEVEL_ID:
            total_times_to_execute *= int(_resolve_var(sseq, sseq._loaded_rec_list[mother_id]['times_to_execute']))
            mother_id = sseq._loaded_rec_list[mother_id]['mother']
            nest_depth += 1

        indent = ' '*5*nest_depth
        recipe_clocks = _calculate_pseudo_recipe_duration(sseq, lrec)
        recipe_duration = recipe_clocks*clock_duration
        total_recipe_duration = recipe_duration*total_times_to_execute

        sseq._duration_list.append({
                    'nest depth': nest_depth,
                    'recipe name': lrec["recipe_name"],
                    'step duration': print_time(recipe_duration),
                    'total times to execute': total_times_to_execute,
                    'total recipe duration': print_time(total_recipe_duration)})

        total_duration += total_recipe_duration
    
    sseq._total_duration = total_duration


def _resolve_var(sseq: SmartSequencer, var_name: str):
    
    strval = var_name
    while strval in sseq._vars_dict:
        strval = sseq._vars_dict[strval]
    return strval


def _resolve_state(sseq: SmartSequencer, val: str):

    if all(any([x in c for x in ['0', '1']]) for c in val): # it is a bitstring
        return val
    
    if val in sseq._states_dict:    # it is a state name
        return _resolve_state(sseq, sseq._states_dict[val])

    words = _parse_words(val, '|')
    if len(words) < 2:
        raise SequencerException(f'Bad state value: {val}')
    
    result = 0
    for word in words:
        bin_word = _resolve_state(sseq, word)
        result |= int(bin_word, 2)  # translate str to int and apply "or" operator

    return bin(result)[2:].zfill(32)  # trim "0b" and pad to 32 chars


def _make_commands_to_board(sseq: SmartSequencer):

        commands_to_board = []

        if sseq._active_dyn_var != '':   # if we are using a dynamic variable
            dynamic_var_value = sseq._dyn_vars_dict[sseq._active_dyn_var]
            for i in range(len(dynamic_var_value)):
                value = _resolve_var(sseq, dynamic_var_value[i])
                s = f'sek dynamicVector {i} {value}'
                commands_to_board.append(s)
        
        for i, recipe in enumerate(sseq._loaded_rec_list):
            
            for rel in ['daughter', 'mother', 'sister']:
                s = f'sek recipe {i} {rel} {recipe[rel]}'
                commands_to_board.append(s)

            recipe_states = sseq._recipe_dict[recipe['recipe_name']]
            
            for j, state_dict in enumerate(recipe_states):
                
                state = int(_resolve_state(sseq, state_dict['state']), 2)
                delay = int(_resolve_var(sseq, state_dict['delay']))

                s = f'sek recipe {i} status {j} {state} {delay}'
                commands_to_board.append(s)
            
            if recipe['is_dynamic']:
                s = f'sek recipe {i} dynamic'
                commands_to_board.append(s)
                for j, ncluster_val in enumerate(recipe['ncluster']):
                    value = int(_resolve_var(sseq, ncluster_val))
                    s = f'sek recipe {i} dynamicDependence {j} {recipe["id_depend"][j]} {value}'
                    commands_to_board.append(s)
            
            else:
                s = f'sek recipe {i} dynamic 0'
                commands_to_board.append(s)

                value = int(_resolve_var(sseq, recipe['times_to_execute']))
                s = f'sek recipe {i} n {value}'
                commands_to_board.append(s)
        
        sseq._command_list = commands_to_board
