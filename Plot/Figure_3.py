import matplotlib

# matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import numpy as np
import os
import argparse
import matplotlib as mpl
label_size = 16
#mpl.rcParams['xtick.labelsize'] = label_size
mpl.rcParams['ytick.labelsize'] = label_size

seg_list = ['PT', 'S3', 'SDL', 'mTAL', 'cTAL', 'DCT', 'CNT', 'CCD', 'OMCD', 'IMCD']
seg_early = ['PT', 'S3', 'SDL', 'mTAL', 'cTAL', 'DCT', 'CNT']
seg_late = ['CCD', 'OMCD', 'IMCD']

humOrrat = 'rat'  # set to 'hum' for human model, 'rat for rat model

# conversion factors
if humOrrat == 'rat':
    sup_ratio = 2.0 / 3.0
    neph_per_kidney = 36000  # number of nephrons per kidney
elif humOrrat == 'hum':
    sup_ratio = 0.85
    neph_per_kidney = 1000000
jux_ratio = 1 - sup_ratio
neph_weight = [sup_ratio, 0.4 * jux_ratio, 0.3 * jux_ratio, 0.15 * jux_ratio, 0.1 * jux_ratio, 0.05 * jux_ratio]

p_to_mu = 1e-6  # convert pmol to micromole
cf_solute = neph_per_kidney * p_to_mu

nl_to_ml = 1e-6  # convert nl to ml
cf_volume = neph_per_kidney * nl_to_ml

solute_conversion = cf_solute
volume_conversion = cf_volume


def get_vals(solute, fname, sex):

    os.chdir(fname)

    file_cd = open(sex + '_' + humOrrat + '_IMCD' + '_flow_of_' + solute + '_in_Lumen.txt', 'r')

    datalist_imcd = []
    for i in file_cd:
        line = i.split(' ')
        datalist_imcd.append(float(line[0]))
        excr = solute_conversion * datalist_imcd[-1]

    file_cd.close()

    os.chdir('..')
    return excr


# Mg
male_baseline = get_vals('Mg', 'Male_rat_normal_sup', 'male')
male_PT_50D = get_vals('Mg', 'Male_rat_normal_sup_PT_50D', 'male')
male_PT_50I = get_vals('Mg', 'Male_rat_normal_sup_PT_50I', 'male')
male_cTAL_50D = get_vals('Mg', 'Male_rat_normal_sup_cTAL_50D', 'male')
male_cTAL_50I = get_vals('Mg', 'Male_rat_normal_sup_cTAL_50I', 'male')
male_TRPM6_100  = get_vals('Mg', 'TRPM6-99_Male_rat', 'male')
male_TRPM6_70  = get_vals('Mg', 'TRPM6-70_Male_rat', 'male')

female_baseline = get_vals('Mg', 'Female_rat_normal_sup', 'female')
female_PT_50D = get_vals('Mg', 'Female_rat_normal_sup_PT_50D', 'female')
female_PT_50I = get_vals('Mg', 'Female_rat_normal_sup_PT_50I', 'female')
female_cTAL_50D = get_vals('Mg', 'Female_rat_normal_sup_cTAL_50D', 'female')
female_cTAL_50I = get_vals('Mg', 'Female_rat_normal_sup_cTAL_50I', 'female')
female_TRPM6_100  = get_vals('Mg', 'TRPM6-99_Female_rat', 'female')
female_TRPM6_70  = get_vals('Mg', 'TRPM6-70_Female_rat', 'female')

male_bar = [np.array(male_PT_50D)/np.array(male_baseline)-1, np.array(male_PT_50I)/np.array(male_baseline)-1,
            np.array(male_cTAL_50D)/np.array(male_baseline)-1, np.array(male_cTAL_50I)/np.array(male_baseline)-1,
            np.array(male_TRPM6_70)/np.array(male_baseline)-1, np.array(male_TRPM6_100)/np.array(male_baseline)-1]

female_bar = [np.array(female_PT_50D)/np.array(female_baseline)-1, np.array(female_PT_50I)/np.array(female_baseline)-1,
            np.array(female_cTAL_50D)/np.array(female_baseline)-1, np.array(female_cTAL_50I)/np.array(female_baseline)-1,
            np.array(female_TRPM6_70)/np.array(female_baseline)-1, np.array(female_TRPM6_100)/np.array(female_baseline)-1]

# colors
c1 = 'paleturquoise'
c2 = 'cyan'
c3 = 'lightsteelblue'
c4 = 'lightskyblue'
c5 = 'cadetblue'
c6 = 'cornflowerblue'
c7 = 'darkblue'
c8 = 'teal'
c9 = 'orchid'

width = 0.15

# fontsizes
xlab_size = 16
xticklab_size = 18
ylab_size = 20
yticklab_size = 16
title_size = 22
leg_size = 18
inset_size = 16

fig_labels = ['PT perm\n(-50%)', 'PT perm\n(+50%)', 'TAL perm\n(-50%)', 'TAL perm\n(+50%)', 'TRPM6+NaMgX\n(-70%)', 'TRPM6+NaMgX\n(-100%)']

# Plotting

fig, ax = plt.subplots()
fig.set_figheight(8)
fig.set_figwidth(14)
x = np.arange(len(fig_labels))

ax.bar(x-0.5*width, male_bar, width, color=c6, edgecolor='k', label='Male')
ax.bar(x+0.5*width, female_bar, width, color=c9, edgecolor='k', label='Female')
ax.axhline(y=0.0, color='black')

ax.set_xticks(np.arange(len(fig_labels)))
ax.set_xticklabels(fig_labels, fontsize=xticklab_size)
ax.set_ylabel("Fractional change in Mg$^{2+}$ excretion", fontsize=ylab_size)
ax.legend(fontsize=ylab_size)


plt.subplots_adjust(left=0.06,
                    bottom=0.1,
                    right=0.98,
                    top=0.97,
                    wspace=0.19,
                    hspace=0.1)

plt.savefig("D:/nephron_Mg/Figures/Figure_3.png")
#plt.show()
