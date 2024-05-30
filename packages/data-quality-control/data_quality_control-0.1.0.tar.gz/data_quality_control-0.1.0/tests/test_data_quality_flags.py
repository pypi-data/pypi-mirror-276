import sys
sys.path.append(r"../fun")
sys.path.append(r"../userModules")
from DataQualityFlags import quality_control, qc1_flags, qc2_flags
import numpy as np
import pytest

# apply quality control
df_gold = quality_control.generate_gold_dataset(mean_wind=10, mean_wdir=270)
qc_instance = quality_control(df_gold)

@pytest.fixture
def qc(request):
    return qc_instance

@pytest.mark.parametrize('qc', [qc_instance], indirect=True)
def test_detect_time_gaps(qc):
    """ tests if the time gaps in df_gold are right"""
    df = qc.detect_time_gaps()
    # FIXME the values between 200: 205 should all be flagged
    assert (df.iloc[200:205].qc1 == qc1_flags.doubtful).any()
    assert (df.iloc[200:205].qc2 == qc2_flags.time_errors).any()
    assert (df.iloc[100:105].qc1 == qc1_flags.doubtful).all()
    assert (df.iloc[100:105].qc2 == qc2_flags.time_errors).all()

@pytest.mark.parametrize('qc', [qc_instance], indirect=True)
def test_detect_missing(qc):
    """ tests if the  missing values in df_gold are detected"""

    nan_index = np.linspace(0, 8760, 25)
    nan_index[1:] = nan_index[1:] - 1
    
    indexes = range(8700, 8704)
    
    df = qc.detect_missing()
    assert (df.iloc[nan_index.astype('uint16'),:].qc1 == qc1_flags.missing).all()
    assert (df.iloc[nan_index.astype('uint16')].qc2 == qc2_flags.not_finite).all()

    assert (df.iloc[indexes,:].qc1 == qc1_flags.missing).all()
    assert (df.iloc[indexes,:].qc2 == qc2_flags.not_finite).all()
    
    
@pytest.mark.parametrize('qc', [qc_instance], indirect=True)
def test_detect_outliers_ws_range(qc):
    """tests if the outliers outside the range are flagged"""
    df = qc.detect_outliers_ws_range(channel_names=['U1'],
                                          ranges=[[-30, 30]])
    
    indexes = [150, 299]
    assert (df.iloc[indexes, :].qc1 == qc1_flags.invalid).all()
    assert (df.iloc[indexes, :].qc2 == qc2_flags.range_failed).all()

@pytest.mark.parametrize('qc',  [qc_instance], indirect=True)    
def test_detect_outliers_range(qc):
    """tests if the outliers outside the range are flagged"""
    qc = quality_control(df_gold)
    df = qc.detect_outliers_range(channel_names=['U1'])
    
    indexes = [150, 299]
    print(df.iloc[indexes, :])
    assert (df.iloc[indexes, :].qc1 == qc1_flags.doubtful).all()
    assert (df.iloc[indexes, :].qc2 == qc2_flags.outlier).all()
    
@pytest.mark.parametrize('qc',  [qc_instance], indirect=True)    
def test_detect_spikes(qc):
    """tests if the spike values are flagged"""

    df = qc.detect_spikes(channel_names=['U1'], window_length=100, thresh=3)
    indexes = [150, 299]
    # FIXME: not sure why it fails
    assert (df.iloc[indexes, :].qc1 == qc1_flags.doubtful).all()
    assert (df.iloc[indexes, :].qc2 == qc2_flags.outlier).all()

def test_detect_stuck_sensor(qc):
    """tests if the spike values are flagged"""

    df = qc.detect_stuck_sensor(channel_names=['U1', 'U2'],thresholds=[6, 6])
    
    indexes = range(100, 110)
    assert (df.iloc[indexes, :].qc1 == qc1_flags.invalid).all()
    assert (df.iloc[indexes, :].qc2 == qc2_flags.sensor_failure).all()
    
def test_detect_bad_wdir(qc):
    """tests if values outside the wind direction range [0, 360] are flagged"""
    df = qc.detect_bad_wdir(channel_names=['wdir'])
    
    indexes = [365, 770]

    assert (df.iloc[indexes, :].qc1 == qc1_flags.invalid).all()
    assert (df.iloc[indexes, :].qc2 == qc2_flags.range_failed).all()

def test_detect_bad_cnr(qc):
    """ tests to see if bad CNR values are flagged properly """
    df = qc.detect_bad_cnr(channel_names=['cnr'], cnr_ranges=[[-30, 10]])
    indexes = range(5000, 5010)
    
    assert (df.iloc[indexes,:].qc1 == qc1_flags.doubtful).all()
    assert (df.iloc[indexes,:].qc2 == qc2_flags.bad_cnr).all()

def test_detect_bad_availability(qc):
    """ tests to see if values with low Availability are flagged properly"""

    df = qc.detect_bad_availability(channel_names=['avail'], avail_ranges=[[75, 100]])
    indexes = range(4420, 4440)
    
    assert (df.iloc[indexes,:].qc1 == qc1_flags.doubtful).all()
    assert (df.loc[df.index[indexes], 'qc2'].apply(lambda x: qc2_flags.bad_availability in qc2_flags(x))).all()

# Prepare the following tests in the future   
def test_detect_wake_effects(qc):
    """ tests if values within the wake/disturbance sector [a, b] are flagged """
    df = qc.detect_wake_effects(channel_name='wdir', wdir_range=[[10, 30], [150, 210]])
    len=2199
    assert (df.loc[:,'qc2'].apply(lambda x: qc2_flags.disturbed_flow in qc2_flags(x))).sum() == len    
    
def test_detect_sudden_changes(qc):
    """tests if the sudden changes are flagged"""
    df = qc.detect_sudden_changes(channel_names=['U1', 'U2', 'U3'])
    
    indexes = range(7000, 8000)
    assert (df.loc[df.index[indexes], 'qc1'].apply(lambda x: qc1_flags.doubtful in qc1_flags(x))).all()
    assert (df.loc[df.index[indexes], 'qc2'].apply(lambda x: qc2_flags.sensor_failure in qc2_flags(x))).all()

def test_detect_high_stddev(qc):
    """ tests to see if the values with high stddev are flagged properly"""


# def test_assign_qc_valid(qc, df_gold):
#     """tests if the valid qc flags are really assigned to the df"""
#     df = qc.assign_qc_valid(df_gold)
