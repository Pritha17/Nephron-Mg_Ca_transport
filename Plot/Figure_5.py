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

#fig_labels = ['PT', 'SDL', 'mTAL', 'cTAL', 'DCT', 'CNT', 'CD', 'urine']
fig_labels_1 = ['cTAL', 'DCT', 'CNT', 'CD', 'urine']
fig_labels_2 = ['cTAL', 'DCT', 'CNT', 'CD']

def get_vals(solute, fname, sex):
    delivery_early_sup = {}
    delivery_late = {}
    transport_early_sup = {}
    transport_late = {}

    for seg in seg_list:
        os.chdir(fname)

        if seg in seg_early:
            file_sup = open(sex + '_' + humOrrat + '_' + seg + '_flow_of_' + solute + '_in_Lumen_sup.txt', 'r')

            datalist_sup = []
            for i in file_sup:
                line = i.split(' ')
                datalist_sup.append(float(line[0]))

            delivery_early_sup[seg] = solute_conversion * datalist_sup[0]

            transport_early_sup[seg] = solute_conversion * (datalist_sup[0] - datalist_sup[-1])

            file_sup.close()

        if seg in seg_late:
            file_cd = open(sex + '_' + humOrrat + '_' + seg + '_flow_of_' + solute + '_in_Lumen.txt', 'r')

            datalist_cd = []
            for i in file_cd:
                line = i.split(' ')
                datalist_cd.append(float(line[0]))
            file_cd.close()

            delivery_late[seg] = solute_conversion * datalist_cd[0]
            transport_late[seg] = solute_conversion * (datalist_cd[0] - datalist_cd[-1])

            if seg == 'IMCD':
                excr = solute_conversion * datalist_cd[-1]

        os.chdir('..')

    del_vals = [delivery_early_sup['cTAL'], delivery_early_sup['DCT'],
                delivery_early_sup['CNT'], delivery_late['CCD'], excr]

    trans_vals = [transport_early_sup['cTAL'], transport_early_sup['DCT'],
                  transport_early_sup['CNT'], transport_late['CCD'] + transport_late['OMCD'] + transport_late['IMCD']]

    return del_vals, trans_vals


male_del_Mg_normal, male_trans_Mg_normal = get_vals_del('Mg', 'Male_rat_normal_sup', 'male')
female_del_Mg_normal, female_trans_Mg_normal = get_vals_del('Mg', 'Female_rat_normal_sup', 'female')
male_del_Mg_NKCC2_70, male_trans_Mg_NKCC2_70 = get_vals_del('Mg', 'NKCC2-70_Male_rat', 'male')
female_del_Mg_NKCC2_70, female_trans_Mg_NKCC2_70 = get_vals_del('Mg', 'NKCC2-70_Female_rat', 'female')
male_del_Mg_NCC_70, male_trans_Mg_NCC_70 = get_vals_del('Mg', 'NCC-70_Male_rat', 'male')
female_del_Mg_NCC_70, female_trans_Mg_NCC_70 = get_vals_del('Mg', 'NCC-70_Female_rat', 'female')
male_del_Mg_ENaC_70, male_trans_Mg_ENaC_70 = get_vals_del('Mg', 'ENaC-70_Male_rat', 'male')
female_del_Mg_ENaC_70, female_trans_Mg_ENaC_70 = get_vals_del('Mg', 'ENaC-70_Female_rat', 'female')

# colors
c1 = 'paleturquoise'
c2 = 'cyan'
c3 = 'teal'
c4 = 'deepskyblue'

c6 = 'pink'
c7 = 'hotpink'
c8 = 'orchid'
c9 = 'darkmagenta'

width = 0.15

# fontsizes
xlab_size = 16
xticklab_size = 18
ylab_size = 20
yticklab_size = 16
title_size = 22
leg_size = 20
inset_size = 16

# Plotting

fig, ax = plt.subplots(2, 2, sharey='row')
fig.set_figheight(10)
fig.set_figwidth(10)
x1 = np.arange(len(fig_labels_1))
x2 = np.arange(len(fig_labels_2))

# Male Mg delivery
ax[0,0].bar(x1-2*width, male_del_Mg_normal, width, color=c1, edgecolor='k', label='baseline')
ax[0,0].bar(x1-width, male_del_Mg_NKCC2_70, width, color=c2, edgecolor='k', label='NKCC2-70')
ax[0,0].bar(x1, male_del_Mg_NCC_70, width, color=c3, edgecolor='k', label='NCC-70')
ax[0,0].bar(x1+width, male_del_Mg_ENaC_70, width, color=c4, edgecolor='k', label='ENaC-70')

ax[0,0].set_xticks(np.arange(len(fig_labels_1)))
ax[0,0].set_xticklabels(fig_labels_1, fontsize=xticklab_size)
ax[0,0].set_ylabel("Mg$^+$ delivery ($\mu$mol/min)", fontsize=ylab_size)
ax[0, 0].set_title("Male", fontsize=title_size)


# Female Mg delivery
ax[0,1].bar(x1-2*width, female_del_Mg_normal, width, color=c6, edgecolor='k', label='baseline')
ax[0,1].bar(x1-width, female_del_Mg_NKCC2_70, width, color=c7, edgecolor='k', label='NKCC2-70')
ax[0,1].bar(x1, female_del_Mg_NCC_70, width, color=c8, edgecolor='k', label='NCC-70')
ax[0,1].bar(x1+width, female_del_Mg_ENaC_70, width, color=c9, edgecolor='k', label='ENaC-70')

ax[0,1].set_xticks(np.arange(len(fig_labels_1)))
ax[0,1].set_xticklabels(fig_labels_1, fontsize=xticklab_size)
ax[0, 1].set_title("Female", fontsize=title_size)


# Male Mg transport
ax[1,0].bar(x2-2*width, male_trans_Mg_normal, width, color=c1, edgecolor='k', label='baseline')
ax[1,0].bar(x2-width, male_trans_Mg_NKCC2_70, width, color=c2, edgecolor='k', label='NKCC2-70')
ax[1,0].bar(x2, male_trans_Mg_NCC_70, width, color=c3, edgecolor='k', label='NCC-70')
ax[1,0].bar(x2+width, male_trans_Mg_ENaC_70, width, color=c4, edgecolor='k', label='ENaC-70')

ax[1,0].set_xticks(np.arange(len(fig_labels_2)))
ax[1,0].set_xticklabels(fig_labels_2, fontsize=xticklab_size)
ax[1,0].set_ylabel("Mg$^{2+}$ transport ($\mu$mol/min)", fontsize=ylab_size)


# Female Mg transport
ax[1,1].bar(x2-2*width, female_trans_Mg_normal, width, color=c6, edgecolor='k', label='baseline')
ax[1,1].bar(x2-width, female_trans_Mg_NKCC2_70, width, color=c7, edgecolor='k', label='NKCC2-70')
ax[1,1].bar(x2, female_trans_Mg_NCC_70, width, color=c8, edgecolor='k', label='NCC-70')
ax[1,1].bar(x2+width, female_trans_Mg_ENaC_70, width, color=c9, edgecolor='k', label='ENaC-70')

ax[1,1].set_xticks(np.arange(len(fig_labels_2)))
ax[1,1].set_xticklabels(fig_labels_2, fontsize=xticklab_size)

ax[0,0].legend(loc='upper right', bbox_to_anchor=(0.99, 0.99), fontsize=leg_size)
ax[0,1].legend(loc='upper right', bbox_to_anchor=(0.99, 0.99), fontsize=leg_size)

plt.subplots_adjust(left=0.11,
                    bottom=0.05,
                    right=0.98,
                    top=0.96,
                    wspace=0.04,
                    hspace=0.11)

plt.savefig("D:/nephron_Mg/Figures/Figure_5.png")