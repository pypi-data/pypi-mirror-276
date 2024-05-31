# import sys, glob, os
# from seiscod import Stream, Trace  # not part of this package
# from readdat.tusmus.read_tusmus import read_tus_mus, MusChannelError
#
# tus_files = sys.argv[1:-1]
# npz_file = sys.argv[-1]
#
# for tus_file in tus_files:
#     assert os.path.isfile(tus_file)
#     assert tus_file.lower().endswith('.tus')
# assert not os.path.isfile(npz_file)
# assert npz_file.endswith('.seiscodstream.npz')
#
# st = Stream()
# for tus_file in tus_files:
#     for channel in range(100):
#         try:
#             stats, data = read_tus_mus(tus_file, channel=channel)
#         except MusChannelError:
#             break
#
#         tr = Trace(data=data, **stats)
#         st.append(tr)
#
# st.savez(npz_file)
