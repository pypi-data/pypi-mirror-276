import pythonAssist as pa
from DataQualityFlags import quality_control, qc1_flags, qc2_flags

# apply quality control
df_gold = quality_control.generate_gold_dataset(mean_wind=10,
                                                mean_wdir=270)
qc = quality_control(df_gold)

# detect time gaps
df_gold = qc.detect_time_gaps()

# detect missing samples
df_gold = qc.detect_missing(channel_name=['U1', 'U2', 'U3'])  # works

# detect outliers in ws ranges
df_gold = qc.detect_outliers_ws_range(channel_names=['U1', 'U2'],
                                        ranges=[[-30, 30]])  # works

# detect stuck sensors
df_gold = qc.detect_stuck_sensor(channel_names=['U1', 'U2'],
                                    thresholds=[6, 6])  # works

df_gold = qc.detect_bad_wdir(channel_names=['wdir'])  # works

# df_gold = qc.detect_sudden_changes(channel_names = ['U1', 'U2', 'U3'],plot_figure=True) # does not work

df_gold = qc.detect_wake_effects(channel_name='wdir',
                                    wdir_range=[[10, 30], [150, 210]])

# df_gold = qc.detect_spikes(channel_name='U1', threshold=5, window_length=100, plot_figure=True, verbose=True)
# drop a row of dates
# df_gold.drop(index='2021-12-31 21:00:00')

# filter out missing values using qualty flags qc1 and qc2
# df_gold[df_gold.qc1==qc1_flags.missing.value]

# Check and validate different results
df_gold.iloc[365, :]['qc1']

# prepare df
df_gold = qc.prepare_df(filter_out_regex='3$', replace_nan=[-9999.99, 999])

df_gold = qc.assign_qc_valid(df_gold)
