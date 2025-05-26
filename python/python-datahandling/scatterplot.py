# -*- coding: utf-8 -*-
"""
Created on Mon May 12 16:51:28 2025

@author: ingeb
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

folder = 'C:\\Users\\ingeb\\Documents\\Master\\applications\\bf_files'

systems = ['10-90-ACC', '10-90-RAD']


filename1 = '10-90-ACC' + '-results.csv'
file1 = folder + '\\' + filename1
df1 = pd.read_csv(file1)
Parray1 = df1['pmp'].to_numpy()
datesarray = df1.index.to_numpy()
totPA1 = Parray1[0::5]
totPA2 = Parray1[1::5]
totPA3 = Parray1[2::5]
totPA4 = Parray1[3::5]
totPA5 = Parray1[4::5]


filename2 = '10-90-RAD' + '-results.csv'
file2 = folder + '\\' + filename2
df2 = pd.read_csv(file2)
Parray2 = df2['pmp'].to_numpy()
totPR1 = Parray2[0::5]
totPR2 = Parray2[1::5]
totPR3 = Parray2[2::5]
totPR4 = Parray2[3::5]
totPR5 = Parray2[4::5]    

data = pd.DataFrame()

relerrP1 = 100*(totPA1 - totPR1)/totPR1
relerrP2 = 100*(totPA2 - totPR2)/totPR2
relerrP3 = 100*(totPA3 - totPR3)/totPR3
relerrP4 = 100*(totPA4 - totPR4)/totPR4
relerrP5 = 100*(totPA5 - totPR5)/totPR5

abserrP1 = totPA1 - totPR1
abserrP2 = totPA2 - totPR2
abserrP3 = totPA3 - totPR3
abserrP4 = totPA4 - totPR4
abserrP5 = totPA5 - totPR5

#max absolute errors:
maxabserrsP1 = np.sort(abserrP1)[:20]
maxabserrsP2 = np.sort(abserrP2)[:20]
maxabserrsP3 = np.sort(abserrP3)[:20]
maxabserrsP4 = np.sort(abserrP4)[:20]
maxabserrsP5 = np.sort(abserrP5)[:20]

datesP1 = []
datesP2 = []
datesP3 = []
datesP4 = []
datesP5 = []

#accompanying relative errors:
accrelerrP1 = []
accrelerrP2 = []
accrelerrP3 = []
accrelerrP4 = []
accrelerrP5 = []

for k in range(20):
    indxP1 = np.where(abserrP1 == maxabserrsP1[k])
    accrelerrP1.append(relerrP1[indxP1][0])
    datesP1.append(int(datesarray[indxP1[0]*5][0]/5))
    indxP2 = np.where(abserrP2 == maxabserrsP2[k])
    accrelerrP2.append(relerrP2[indxP2][0])
    datesP2.append(int(datesarray[indxP2[0]*5][0]/5))
    indxP3 = np.where(abserrP3 == maxabserrsP3[k])
    accrelerrP3.append(relerrP3[indxP3][0])
    datesP3.append(int(datesarray[indxP3[0]*5][0]/5))
    indxP4 = np.where(abserrP4 == maxabserrsP4[k])
    accrelerrP4.append(relerrP4[indxP4][0])
    datesP4.append(int(datesarray[indxP4[0]*5][0]/5))
    indxP5 = np.where(abserrP5 == maxabserrsP5[k])
    accrelerrP5.append(relerrP5[indxP5][0])
    datesP5.append(int(datesarray[indxP5[0]*5][0]/5))

print('10deg: \n', maxabserrsP1 , '\n', datesP1)
print('30deg: \n', maxabserrsP2 , '\n', datesP2)
print('50deg: \n', maxabserrsP3 , '\n', datesP3)
print('70deg: \n', maxabserrsP4 , '\n', datesP4)
print('90deg: \n', maxabserrsP5 , '\n', datesP5)

fig0, ax0 = plt.subplots(1,1, figsize=(8,6))

#ax0.scatter(abserrP1,relerrP1, color = 'b', label = '10deg', marker = 'o', alpha = 0.2)
#ax0.scatter(abserrP2,relerrP2, color = 'g', label = '30deg', marker = 'o', alpha = 0.2)
#ax0.scatter(abserrP3,relerrP3, color = 'y', label = '50deg', marker = 'o', alpha = 0.2)
#ax0.scatter(abserrP4,relerrP4, color = 'c', label = '70deg', marker = 'o', alpha = 0.2)
#ax0.scatter(abserrP5,relerrP5, color = 'gray', label = '90deg', marker = 'o', alpha = 0.01)


ax0.scatter(maxabserrsP1,accrelerrP1, color = 'b', label = '10deg high', marker = 'o')
ax0.scatter(maxabserrsP2,accrelerrP2, color = 'g', label = '30deg high', marker = 'o')
ax0.scatter(maxabserrsP3,accrelerrP3, color = 'y', label = '50deg high', marker = 'o')
ax0.scatter(maxabserrsP4,accrelerrP4, color = 'c', label = '70deg high', marker = 'o')
ax0.scatter(maxabserrsP5,accrelerrP5, color = 'k', label = '90deg high', marker = 'o')

ax0.axis('scaled')
ax0.set_xlim(-30, 15)
ax0.set_ylim(-30, 5)
ax0.set_title('20 highest module output absolute errors per angle')
ax0.set_xlabel('Absolute error (W)')
ax0.set_ylabel('Relative error (%)')
plt.tight_layout()
plt.legend()
plt.show()
"""
From print, choose following points:
    10deg:
        abserr -26.23981972
        relerr -17.701370917255154
        hour: 2479
            (from RAD-ACC-pow-err.csv)
    30deg:
        abserr -14.48190794
        relerr -10.425317842767488
        hour: 1519
            (from RAD-ACC-pow-err.csv)
    50deg:
        abserr -7.52887828          alternative -10.1319211
        relerr -5.352475969832748   alternative -3.9095681620394473
        hour: 2478
            (from RAD-ACC-pow-err.csv)
    70deg:
        abserr -5.03897462
        relerr -3.275175085250535
        hour: 2135
            (from RAD-ACC-pow-err.csv)
    90deg:
        abserr: -3.12581721
        relerr: -1.714572485935606
        hour: 2005
            (from RAD-ACC-pow-err.csv)

"""




fig, ax = plt.subplots(1,1, figsize=(8,6))

ax.scatter(abserrP1,relerrP1, color = 'b', label = '10deg', marker = 'o', alpha = 0.5)
ax.scatter(abserrP2,relerrP2, color = 'g', label = '30deg', marker = 'o', alpha = 0.5)
ax.scatter(abserrP3,relerrP3, color = 'y', label = '50deg', marker = 'o', alpha = 0.5)
ax.scatter(abserrP4,relerrP4, color = 'c', label = '70deg', marker = 'o', alpha = 0.5)
ax.scatter(abserrP5,relerrP5, color = 'k', label = '90deg', marker = 'o', alpha = 0.5)

ax.scatter([-26.23981972],[-17.701370917255154], color = 'r', marker = "D", s = 100, label = ' Selected \n points \n highlighted')
ax.scatter([-26.23981972],[-17.701370917255154], color = 'b', marker = "o")
ax.scatter([-14.48190794],[-10.425317842767488], color = 'r', marker = "D", s = 100)
ax.scatter([-14.48190794],[-10.425317842767488], color = 'g', marker = "o")
ax.scatter([-7.52887828],[-5.352475969832748], color = 'r', marker = "D", s = 100)
ax.scatter([-7.52887828],[-5.352475969832748], color = 'y', marker = "o")
ax.scatter([-5.03897462],[-3.275175085250535], color = 'r', marker = "D", s = 100)
ax.scatter([-5.03897462],[-3.275175085250535], color = 'c', marker = "o")
ax.scatter([-3.12581721],[-1.714572485935606], color = 'r', marker = "D", s = 100)
ax.scatter([-3.12581721],[-1.714572485935606], color = 'k', marker = "o")

"""
New data from high-accuracy radiance runs:
    mod1prod: 130.2073926
    mod2prod: 124.9228658
    mod3prod: 133.815609
    mod4prod: 149.3625391
    mod5prod: 179.8601903
    (data found in specialhours-results.csv and folder specialhours-high)
    (these are pmp for the module for the special hour)

New data from very high accuracy radiance run:
    mod1prod: 123.2417628
    (data found in veryspecialhours-results.csv and folder specialhour-veryhigh)

data from low accelerad runs:
    mod1prod: 121.996268
    mod2prod: 124.429041
    mod3prod: 133.1327207
    mod4prod: 148.8146207
    mod5prod: 179.1830229
    (data found in 10-90-ACC-results.csv and folder 10-90-ACC)
"""

RadH1 = 130.2073926
RadH2 = 124.9228658
RadH3 = 133.815609
RadH4 = 149.3625391
RadH5 = 179.8601903

RadVH1 = 123.2417628

ACCL1 = 121.996268
ACCL2 = 124.429041
ACCL3 = 133.1327207
ACCL4 = 148.8146207
ACCL5 = 179.1830229

abs1 = ACCL1 - RadH1
rel1 = 100*abs1/RadH1
abs2 = ACCL2 - RadH2
rel2 = 100*abs2/RadH2
abs3 = ACCL3 - RadH3
rel3 = 100*abs3/RadH3
abs4 = ACCL4 - RadH4
rel4 = 100*abs4/RadH4
abs5 = ACCL5 - RadH5
rel5 = 100*abs5/RadH5

absVH1 = ACCL1 - RadVH1
relVH1 = 100*absVH1/RadVH1

ax.scatter([abs1],[rel1], color = 'r', marker = 's', s=120, label = ' Improved \n RAD high')
ax.scatter([abs2],[rel2], color = 'r', marker = 's', s=120)
ax.scatter([abs3],[rel3], color = 'r', marker = 's', s=120)
ax.scatter([abs4],[rel4], color = 'r', marker = 's', s=120)
ax.scatter([abs5],[rel5], color = 'r', marker = 's', s=120)
ax.scatter([absVH1],[relVH1], color = 'r', marker = 'd', s=200, label = ' Improved \n RAD very \n high')
ax.scatter([abs1],[rel1], color = 'b', marker = 'o')
ax.scatter([abs2],[rel2], color = 'g', marker = '<', s = 100)
ax.scatter([abs3],[rel3], color = 'y', marker = '>', s = 100)
ax.scatter([abs4],[rel4], color = 'c', marker = '^', s = 100)
ax.scatter([abs5],[rel5], color = 'k', marker = 'v', s = 70)
ax.scatter([absVH1],[relVH1], color = 'b', marker = 'o')


ax.axis('scaled')
ax.set_xlim(-30, 15)
ax.set_ylim(-30, 5)
ax.set_title('Module output errors')
ax.set_xlabel('Absolute error (W)')
ax.set_ylabel('Relative error (%)')
plt.tight_layout()
plt.legend()
plt.show()

