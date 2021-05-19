string = "twagszagtcagrmagcbagtwamszamtcamrmamcbamtwbsszbstcbsrmbscbbstwctszcttcctrmctcbcttwgaszgatcgarmgacbgatwhpszhptchprmhpcbhptwiasziatciarmiacbiatwkdszkdtckdrmkdcbkdtwmkszmktcmkrmmkcbmktwmmszmmtcmmrmmmcbmmtwmtszmttcmtrmmtcbmttwmfszmftcmfrmmfcbmftwahszahtcahrmahcbahtwppszpptcpprmppcbpptwpmszpmtcpmrmpmcbpmtwsiszsitcsirmsicbsitwspszsptcsprmspcbsptwscszsctcscrmsccbsctwsmszsmtcsmrmsmcbsmtwssszsstcssrmsscbsstwtrsztrtctrrmtrcbtrtwwhszwhtcwhrmwhcbwhtwwwszwwtcwwrmwwcbww"

with open("out", 'w') as out_file:
    for char in range(0, len(string), 4):
        substring = string[char:char+4]
        out_file.write(substring + "\n")
