import os, struct
import numpy as np
from astropy.io import fits
from ._auxiliary import init_logger, update_hdr_card
import pandas as pd

logger = init_logger('lta_decoder')
abs_path = os.path.realpath(__file__)

### module constants
CNTR_FIRST_BIT_POSITION_IN_64_BIT_WORD = 60
CNTR_NBITS = 4
ID_FIRST_BIT_POSITION_IN_64_BIT_WORD = 56
ID_NBITS = 4
DATA_NBITS = 32
STARTUP_PACKETS = 20

BIN_FILE_SUFFIX = '.dat'
HDR_FILE_SUFFIX = '.hdr'

SEQ_CONVENTION_READ_NSAMP_NUMBER = "NSAMP"
SEQ_CONVENTION_READ_ROWS_NUMBER = "NROW"
SEQ_CONVENTION_READ_COLS_NUMBER = "NCOL"


### module exception
class LTADecoderException(Exception):
    pass


### "private" functions
def _decode_npdata_chid(arr: np.array):
    '''Decode the channel id from LTA data'''
    
    chid_arr = (arr >> ID_FIRST_BIT_POSITION_IN_64_BIT_WORD).astype('uint8')
    chid_arr &= (1 << ID_NBITS) - 1
    return chid_arr


def _decode_npdata_idx(arr: np.array):
    '''Decode the counter idx from LTA data'''

    idx_arr = (arr >> CNTR_FIRST_BIT_POSITION_IN_64_BIT_WORD).astype('uint8')
    idx_arr &= (1 << ID_NBITS) - 1
    return idx_arr


def _decode_npdata_value(arr: np.array):
    '''Decode the values from LTA data'''

    return -1*(arr & ((1 << DATA_NBITS) - 1)).astype('int32')


def _parse_hdr_file(file_name: str):
    
    # load the hdr file
    hdr_file_name = file_name+HDR_FILE_SUFFIX
    try:
        with fits.open(hdr_file_name) as hdul:
            primary_hdu = hdul[0]

    except FileNotFoundError:
        raise LTADecoderException(f'Header file not found: {hdr_file_name}')
    
    header = primary_hdu.header
    try:
        ncol = int(header[SEQ_CONVENTION_READ_COLS_NUMBER])
        nrow = int(header[SEQ_CONVENTION_READ_ROWS_NUMBER])
        nsamp = int(header[SEQ_CONVENTION_READ_NSAMP_NUMBER])
    
    except KeyError as e:
        raise LTADecoderException(f'Key not found at hdr file: {e}')

    logger.info(f'Parsed hdr file: "{hdr_file_name}"')
    return header, ncol, nrow, nsamp


def _decode_single_dat(dat_file, data_channels, nchannels, initial_data_count, file_base_name):
    
    logger.info(f'Processing file: {dat_file}. ADC count up to here: {initial_data_count}')
    data_list = []
    with open(dat_file, 'rb') as f:
        # first three bytes have the UDP package information
        pack_header = f.read(3)
        while len(pack_header) == 3: # until EOF
            n_words, pack_type, pack_idx = struct.unpack('<BBB', pack_header)
            
            # decode n_words unsigned 64-bit integers from package 
            pack_data = struct.unpack(f'<{n_words}Q', f.read(8*n_words))
            
            # save the package data
            package_dict = {'pack_idx': pack_idx,
                            'pack_data': pack_data} 
            data_list.append(package_dict)

            # read next three bytes
            pack_header = f.read(3)

    # copy the data to a numpy array
    data_arr = np.array([x for entry in data_list for x in entry['pack_data']],
                            dtype='uint64')
    package_arr = np.array([entry['pack_idx'] for entry in data_list for x in \
                            entry['pack_data']], dtype='uint8')
    data_list.clear()

    # decode the data
    data_idx_arr = _decode_npdata_idx(data_arr)
    data_chid_arr = _decode_npdata_chid(data_arr)
    data_channels = np.unique(np.concatenate((data_chid_arr, data_channels)))
    if len(data_channels) > nchannels:
        s = 'More channels than expected: '
        for chid in data_channels:
            s += f'chID {chid} ;'
        logger.error(s)
        raise LTADecoderException('Too many channels in data')

    data_values_arr = _decode_npdata_value(data_arr)
    del data_arr

    # check data consistency
    idx_diff = ((data_idx_arr[1:]-data_idx_arr[:-1])+16)%16
    if np.any(idx_diff != 1):
        for idx in np.where(idx_diff != 1)[0]:
            data_gap_position = initial_data_count+idx
            pkg_gap = (package_arr[idx], package_arr[idx+1])

            s = f'Lost data! Word index: {data_idx_arr[idx+1]} (prev {data_idx_arr[idx]}),'
            s += f'packet index: {pkg_gap[1]} (prev {pkg_gap[0]}), '
            logger.warning(s)
            s = f'this is word {idx} of the packet and word {data_gap_position} of the run'
            logger.warning(s)

    data_count = len(data_idx_arr)

    # copy to a pandas dictionary (for sorting into channels)
    df = pd.DataFrame()
    df['chid'] = data_chid_arr
    df['value'] = data_values_arr

    # save to temporary bin files
    abs_dir = os.path.dirname(abs_path)
    for chid, dh in df.groupby('chid'):
        with open(os.path.join(abs_dir, 'decoder_temp',f'{file_base_name}_{chid}.bin'), 'ba') as f:
            f.write(dh['value'].to_numpy().tobytes())

    return data_count+initial_data_count, data_channels

'''
def _create_large_image_fits(bin_file_path: str, chid, nrow, ncol, nsamp):
    
    # create a dummy array and assign the header
    data = np.zeros((100,100), dtype=np.float32)
    hdu = fits.ImageHDU(data=data)
    header = hdu.header

    # "cheat" by manually changing these
    header['NAXIS1'] = ncol*nsamp
    header['NAXIS2'] = nrow
    
    # add hdu-specific information to headers
    header['CHID'] = (chid, "Amplifier ID for this HDU")
    header.append() # leave a blank card for future use

    # save header to file
    fits_path = bin_file_path.rpartition('.')[0] + '.fits'
    header.tofile(fits_path)

    # now enlarge the file to the correct size
    with open(fits_path, 'rb+') as fobj:

        # 32-bit means 4 bytes per pixel
        fobj.seek(len(header.tostring()) + (ncol*nsamp*nrow*4) - 1)
        fobj.write(b'\0')

        # copy chunks
        fobj.seek(len(header.tostring()))
        with open(bin_file_path, 'rb') as bobj:
            npix = 0
            while True:
                bytes_chunk = bobj.read(DECODER_CHUNK_SIZE)
                if len(bytes_chunk) == 0: break
                npix += len(bytes_chunk)
                fobj.write(bytes_chunk)

    return fits_path, npix
'''

def _get_bin_file_list(file_name: str):

    file_dir = os.path.dirname(file_name)
    file_base_name = os.path.basename(file_name)

    input_file_list = [ os.path.join(file_dir,f) for f in os.listdir(file_dir) \
                       if f.startswith(file_base_name) and f.endswith(BIN_FILE_SUFFIX)]
    
    if len(input_file_list) == 0:
        raise LTADecoderException(f'No files found named "{file_name}"')

    # sort accordingly
    input_file_list.sort(key=lambda s: int(s.rpartition('_')[2].partition('.')[0]))
    logger.info('Processing files in the following order: ')
    for f in input_file_list:
        logger.info(f)
    
    return input_file_list


def _make_image_hdu_list(file_base_name, data_channels, nrow, ncol, nsamp):

    image_hdu_list = []

    for chid in data_channels:

        data_bin_file = os.path.join(os.path.dirname(abs_path), 'decoder_temp',f'{file_base_name}_{chid}.bin')

        # load and reshape the data
        hdu_data = np.memmap(data_bin_file, dtype='int32', mode='r', shape=(nrow, ncol*nsamp))
        # hdu_read_data = np.fromfile(data_bin_file, dtype='int32')
        # hdu_data = np.zeros(nrow*ncol*nsamp, dtype='int32')
        # hdu_data[:hdu_read_data.size] = hdu_read_data   # this will leave the missing data at the end
        # hdu_data = hdu_data.reshape((nrow,-1))
        
        # create the image extension        
        hdu = fits.ImageHDU(data=hdu_data)
        
        # add hdu-specific information to headers
        hdu.header['CHID'] = (chid, "Amplifier ID for this HDU")
        hdu.header['NPIX'] = (hdu_data.size, "Number of pixels read in this channel")

        # append to the list
        image_hdu_list.append(hdu)

    return image_hdu_list


def _decode_binary_files(input_file_list, nchannels, file_base_name, 
                         expected_pixels_per_channel, header):

    data_count = 0
    data_channels = np.array([], dtype='uint8')
    for bin_file in input_file_list:
        data_count, data_channels = _decode_single_dat(bin_file, data_channels, nchannels,
                                                       data_count, file_base_name)

    # check for missing data
    missing_data = expected_pixels_per_channel*nchannels-data_count
    if missing_data > 0:
        logger.warning(f'Lost {missing_data} samples')
        update_hdr_card(header, 'MISSDATA', missing_data, "Number of data samples lost")
    else: logger.info(f'Collected number of samples matches expected')

    return data_channels


### "public" functions
def decode_bin(file_name: str, nchannels: int, output_dir=None, overwrite=False):

    file_base_name = os.path.basename(file_name)
    
    # default output directory is ./images/
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(abs_path), 'images')

    # check if decoded file exists
    output_file_name = os.path.join(output_dir, f'{file_base_name}.fits.bz2')
    if os.path.exists(output_file_name):
        if overwrite:
            logger.info(f'Will overwrite {output_file_name}')
        else:
            logger.warning(f'Decoded file "{output_file_name}" already exists. Please use "overwrite=True" if you want to overwrite it. Exiting.')
            return

    # load the hdr file
    header, ncol, nrow, nsamp = _parse_hdr_file(file_name)

    # calculate the total pixels and array size
    expected_pixels_per_channel = nrow*ncol*nsamp
    
    # load the list of files
    input_file_list = _get_bin_file_list(file_name)

    # decode the binary files, save them into temporary files
    ### TODO: see if this can be accomplished with a mmap
    try:
        data_channels = _decode_binary_files(input_file_list, nchannels, file_base_name,
                                            expected_pixels_per_channel, header)

        # create the fits HDUs
        primary_hdu = fits.PrimaryHDU(header=header)
        image_hdu_list = _make_image_hdu_list(file_base_name, data_channels, 
                                                        nrow, ncol, nsamp)
        hdu_list = fits.HDUList([primary_hdu, *image_hdu_list])

        # write fits to disk
        hdu_list.writeto(output_file_name, overwrite=True)
    
    except Exception as e:
        logger.exception(f'Could not create fits image. Error: {e}')

    else:
        logger.info(f'fits image created: {output_file_name}')

        # clean up
        for chid in data_channels:
            os.remove(os.path.join(os.path.dirname(abs_path), 'decoder_temp',f'{file_base_name}_{chid}.bin'))
        for bin_file in input_file_list:
            os.remove(bin_file)
        os.remove(file_name+HDR_FILE_SUFFIX)
        logger.info('removed binary and temporary files')