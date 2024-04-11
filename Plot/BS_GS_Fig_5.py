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

mu_conv = 1e-3  # from mumol to mmol
min_per_day = 1440
solute_conversion = cf_solute  # mu_conv #* min_per_day
volume_conversion = cf_volume

fig_labels = ['PT', 'SDL', 'mTAL', 'cTAL', 'DCT', 'CNT', 'CD', 'urine']


def get_vals(solute, fname, sex):
    delivery_early_sup = {}
    delivery_early_jux = {}
    delivery_early = {}
    delivery_late = {}

    if solute == 'Vol':
        for seg in seg_list:
            os.chdir(fname)
            if seg in seg_early:
                file_sup = open(sex + '_' + humOrrat + '_' + seg + '_water_volume_in_Lumen_sup.txt', 'r')
                file_jux1 = open(sex + '_' + humOrrat + '_' + seg + '_water_volume_in_Lumen_jux1.txt', 'r')
                file_jux2 = open(sex + '_' + humOrrat + '_' + seg + '_water_volume_in_Lumen_jux2.txt', 'r')
                file_jux3 = open(sex + '_' + humOrrat + '_' + seg + '_water_volume_in_Lumen_jux3.txt', 'r')
                file_jux4 = open(sex + '_' + humOrrat + '_' + seg + '_water_volume_in_Lumen_jux4.txt', 'r')
                file_jux5 = open(sex + '_' + humOrrat + '_' + seg + '_water_volume_in_Lumen_jux5.txt', 'r')

                temp_jux1 = volume_conversion * neph_weight[1] * float(file_jux1.readline())
                temp_jux2 = volume_conversion * neph_weight[2] * float(file_jux2.readline())
                temp_jux3 = volume_conversion * neph_weight[3] * float(file_jux3.readline())
                temp_jux4 = volume_conversion * neph_weight[4] * float(file_jux4.readline())
                temp_jux5 = volume_conversion * neph_weight[5] * float(file_jux5.readline())

                delivery_early_sup[seg] = volume_conversion * neph_weight[0] * float(file_sup.readline())
                delivery_early_jux[seg] = temp_jux1 + temp_jux2 + temp_jux3 + temp_jux4 + temp_jux5
                delivery_early[seg] = delivery_early_sup[seg] + delivery_early_jux[seg]

                file_sup.close()
                file_jux1.close()
                file_jux2.close()
                file_jux3.close()
                file_jux4.close()
                file_jux5.close()

            if seg in seg_late:
                file_cd = open(sex + '_' + humOrrat + '_' + seg + '_water_volume_in_Lumen.txt', 'r')

                if seg == 'IMCD':
                    datalist_imcd = []
                    for i in file_cd:
                        line = i.split(' ')
                        datalist_imcd.append(float(line[0]))

                    delivery_late[seg] = volume_conversion * datalist_imcd[0]
                    excr = volume_conversion * datalist_imcd[-1]
                else:
                    delivery_late[seg] = volume_conversion * float(file_cd.readline())
                file_cd.close()

            os.chdir('..')

    else:
        for seg in seg_list:
            os.chdir(fname)

            if seg in seg_early:
                file_sup = open(sex + '_' + humOrrat + '_' + seg + '_flow_of_' + solute + '_in_Lumen_sup.txt', 'r')
                file_jux1 = open(sex + '_' + humOrrat + '_' + seg + '_flow_of_' + solute + '_in_Lumen_jux1.txt', 'r')
                file_jux2 = open(sex + '_' + humOrrat + '_' + seg + '_flow_of_' + solute + '_in_Lumen_jux2.txt', 'r')
                file_jux3 = open(sex + '_' + humOrrat + '_' + seg + '_flow_of_' + solute + '_in_Lumen_jux3.txt', 'r')
                file_jux4 = open(sex + '_' + humOrrat + '_' + seg + '_flow_of_' + solute + '_in_Lumen_jux4.txt', 'r')
                file_jux5 = open(sex + '_' + humOrrat + '_' + seg + '_flow_of_' + solute + '_in_Lumen_jux5.txt', 'r')

                temp_jux1 = solute_conversion * neph_weight[1] * float(file_jux1.readline())
                temp_jux2 = solute_conversion * neph_weight[2] * float(file_jux2.readline())
                temp_jux3 = solute_conversion * neph_weight[3] * float(file_jux3.readline())
                temp_jux4 = solute_conversion * neph_weight[4] * float(file_jux4.readline())
                temp_jux5 = solute_conversion * neph_weight[5] * float(file_jux5.readline())

                delivery_early_sup[seg] = solute_conversion * neph_weight[0] * float(file_sup.readline())
                delivery_early_jux[seg] = temp_jux1 + temp_jux2 + temp_jux3 + temp_jux4 + temp_jux5
                delivery_early[seg] = delivery_early_sup[seg] + delivery_early_jux[seg]

                file_sup.close()
                file_jux1.close()
                file_jux2.close()
                file_jux3.close()
                file_jux4.close()
                file_jux5.close()

            if seg in seg_late:
                file_cd = open(sex + '_' + humOrrat + '_' + seg + '_flow_of_' + solute + '_in_Lumen.txt', 'r')

                if seg == 'IMCD':
                    datalist_imcd = []
                    for i in file_cd:
                        line = i.split(' ')
                        datalist_imcd.append(float(line[0]))

                    delivery_late[seg] = solute_conversion * datalist_imcd[0]
                    excr = solute_conversion * datalist_imcd[-1]
                else:
                    delivery_late[seg] = solute_conversion * float(file_cd.readline())
                file_cd.close()

            os.chdir('..')

    del_vals = [delivery_early['PT'], delivery_early['SDL'],
                delivery_early['mTAL'], delivery_early['cTAL'], delivery_early['DCT'],
                delivery_early['CNT'], delivery_late['CCD'], excr]

    return del_vals


# Na
male_del_Na_normal = get_vals('Na', 'Male_rat_normal_multiple', 'male')
female_del_Na_normal = get_vals('Na', 'Female_rat_normal_multiple', 'female')
male_del_Na_NKCC2_100 = get_vals('Na', 'NKCC2-100_Male_rat', 'male')
female_del_Na_NKCC2_100 = get_vals('Na', 'NKCC2-100_Female_rat', 'female')
male_del_Na_NCC_100 = get_vals('Na', 'NCC-100_Male_rat', 'male')
female_del_Na_NCC_100 = get_vals('Na', 'NCC-100_Female_rat', 'female')

# Ca
male_del_Ca_normal = get_vals('Ca', 'Male_rat_normal_multiple', 'male')
female_del_Ca_normal = get_vals('Ca', 'Female_rat_normal_multiple', 'female')
male_del_Ca_NKCC2_100 = get_vals('Ca', 'NKCC2-100_Male_rat', 'male')
female_del_Ca_NKCC2_100 = get_vals('Ca', 'NKCC2-100_Female_rat', 'female')
male_del_Ca_NCC_100 = get_vals('Ca', 'NCC-100_Male_rat', 'male')
female_del_Ca_NCC_100 = get_vals('Ca', 'NCC-100_Female_rat', 'female')

# Mg
male_del_Mg_normal = get_vals('Mg', 'Male_rat_normal_multiple', 'male')
female_del_Mg_normal = get_vals('Mg', 'Female_rat_normal_multiple', 'female')
male_del_Mg_NKCC2_100 = get_vals('Mg', 'NKCC2-100_Male_rat', 'male')
female_del_Mg_NKCC2_100 = get_vals('Mg', 'NKCC2-100_Female_rat', 'female')
male_del_Mg_NCC_100 = get_vals('Mg', 'NCC-100_Male_rat', 'male')
female_del_Mg_NCC_100 = get_vals('Mg', 'NCC-100_Female_rat', 'female')

# colors
c1 = 'paleturquoise'
c2 = 'cyan'
c3 = 'teal'
c4 = 'pink'
c5 = 'orchid'
c6 = 'darkmagenta'

width = 0.15

# fontsizes
xlab_size = 16
xticklab_size = 20
ylab_size = 20
yticklab_size = 16
title_size = 22
leg_size = 18
inset_size = 16

# Plotting

fig, ax = plt.subplots(3, 2, sharey='row') # sharex=True,
fig.set_figheight(16)
fig.set_figwidth(16)
x = np.arange(len(fig_labels))

# Male Na
ax[0,0].bar(x-width, male_del_Na_normal, width, color=c1, edgecolor='k')
ax[0,0].bar(x, male_del_Na_NKCC2_100, width, color=c2, edgecolor='k')
ax[0,0].bar(x+width, male_del_Na_NCC_100, width, color=c3, edgecolor='k')

ax[0,0].set_xticks(np.arange(len(fig_labels)))
ax[0,0].set_xticklabels(fig_labels, fontsize=xticklab_size)
ax[0,0].set_ylabel("Na$^+$ delivery\n($\mu$mol/min)", fontsize=ylab_size)
ax[0, 0].set_title("Male", fontsize=title_size)

fig_labels_2 = ['urine']
x2 = np.arange(len(fig_labels_2))
left_in, bottom_in, width_in, height_in = [0.85, 0.43, 0.13, 0.52]

ax_in_10 = ax[0,0].inset_axes([left_in, bottom_in, width_in, height_in])
ax_in_10.bar(x2-width, male_del_Na_normal[7], width, color=c1, edgecolor='k') # male_del_Na_normal[5:]
ax_in_10.bar(x2, male_del_Na_NKCC2_100[7], width, color=c2, edgecolor='k')
ax_in_10.bar(x2+width, male_del_Na_NCC_100[7], width, color=c3, edgecolor='k')
ax_in_10.set_xticks(np.arange(len(fig_labels_2)))
ax_in_10.set_xticklabels(fig_labels_2, fontsize=inset_size)
ax_in_10.yaxis.set_tick_params(labelsize=inset_size)


# Female Na
ax[0,1].bar(x-width, female_del_Na_normal, width, color=c4, edgecolor='k')
ax[0,1].bar(x, female_del_Na_NKCC2_100, width, color=c5, edgecolor='k')
ax[0,1].bar(x+width, female_del_Na_NCC_100, width, color=c6, edgecolor='k')

ax[0,1].set_xticks(np.arange(len(fig_labels)))
ax[0,1].set_xticklabels(fig_labels, fontsize=xticklab_size)
ax[0, 1].set_title("Female", fontsize=title_size)

ax_in_10 = ax[0,1].inset_axes([left_in, bottom_in, width_in, height_in])
ax_in_10.bar(x2-width, female_del_Na_normal[7], width, color=c4, edgecolor='k')
ax_in_10.bar(x2, female_del_Na_NKCC2_100[7], width, color=c5, edgecolor='k')
ax_in_10.bar(x2+width, female_del_Na_NCC_100[7], width, color=c6, edgecolor='k')
ax_in_10.set_xticks(np.arange(len(fig_labels_2)))
ax_in_10.set_xticklabels(fig_labels_2, fontsize=inset_size)
ax_in_10.yaxis.set_tick_params(labelsize=inset_size)

# Male Mg
ax[1,0].bar(x-width, male_del_Mg_normal, width, color=c1, edgecolor='k', label='baseline')
ax[1,0].bar(x, male_del_Mg_NKCC2_100, width, color=c2, edgecolor='k', label='NKCC2-70')
ax[1,0].bar(x+width, male_del_Mg_NCC_100, width, color=c3, edgecolor='k', label='NKCC2-100')

ax[1,0].set_xticks(np.arange(len(fig_labels)))
ax[1,0].set_xticklabels(fig_labels, fontsize=xticklab_size)
ax[1,0].set_ylabel("Mg$^{2+}$ delivery\n($\mu$mol/min)", fontsize=ylab_size)

ax_in_10 = ax[1,0].inset_axes([left_in, bottom_in, width_in, height_in])
ax_in_10.bar(x2-width, male_del_Mg_normal[7], width, color=c1, edgecolor='k')
ax_in_10.bar(x2, male_del_Mg_NKCC2_100[7], width, color=c2, edgecolor='k')
ax_in_10.bar(x2+width, male_del_Mg_NCC_100[7], width, color=c3, edgecolor='k')
ax_in_10.set_xticks(np.arange(len(fig_labels_2)))
ax_in_10.set_xticklabels(fig_labels_2, fontsize=inset_size)
ax_in_10.yaxis.set_tick_params(labelsize=inset_size)


# Female Mg
ax[1,1].bar(x-width, female_del_Mg_normal, width, color=c4, edgecolor='k', label='baseline')
ax[1,1].bar(x, female_del_Mg_NKCC2_100, width, color=c5, edgecolor='k', label='NKCC2-70')
ax[1,1].bar(x+width, female_del_Mg_NCC_100, width, color=c6, edgecolor='k', label='NKCC2-100')

ax[1,1].set_xticks(np.arange(len(fig_labels)))
ax[1,1].set_xticklabels(fig_labels, fontsize=xticklab_size)

ax_in_10 = ax[1,1].inset_axes([left_in, bottom_in, width_in, height_in])
ax_in_10.bar(x2-width, female_del_Mg_normal[7], width, color=c4, edgecolor='k')
ax_in_10.bar(x2, female_del_Mg_NKCC2_100[7], width, color=c5, edgecolor='k')
ax_in_10.bar(x2+width, female_del_Mg_NCC_100[7], width, color=c6, edgecolor='k')
ax_in_10.set_xticks(np.arange(len(fig_labels_2)))
ax_in_10.set_xticklabels(fig_labels_2, fontsize=inset_size)
ax_in_10.yaxis.set_tick_params(labelsize=inset_size)

# Male Ca
ax[2,0].bar(x-width, male_del_Ca_normal, width, color=c1, edgecolor='k', label='baseline')
ax[2,0].bar(x, male_del_Ca_NKCC2_100, width, color=c2, edgecolor='k', label='Type 1 BS')
ax[2,0].bar(x+width, male_del_Ca_NCC_100, width, color=c3, edgecolor='k', label='GS')

ax[2,0].set_xticks(np.arange(len(fig_labels)))
ax[2,0].set_xticklabels(fig_labels, fontsize=xticklab_size)
ax[2,0].set_ylabel("Ca$^{2+}$ delivery\n($\mu$mol/min)", fontsize=ylab_size)

ax_in_10 = ax[2,0].inset_axes([left_in, bottom_in, width_in, height_in])
ax_in_10.bar(x2-width, male_del_Ca_normal[7], width, color=c1, edgecolor='k')
ax_in_10.bar(x2, male_del_Ca_NKCC2_100[7], width, color=c2, edgecolor='k')
ax_in_10.bar(x2+width, male_del_Ca_NCC_100[7], width, color=c3, edgecolor='k')
ax_in_10.set_xticks(np.arange(len(fig_labels_2)))
ax_in_10.set_xticklabels(fig_labels_2, fontsize=inset_size)
ax_in_10.yaxis.set_tick_params(labelsize=inset_size)


# Female Ca
ax[2,1].bar(x-width, female_del_Ca_normal, width, color=c4, edgecolor='k', label='baseline')
ax[2,1].bar(x, female_del_Ca_NKCC2_100, width, color=c5, edgecolor='k', label='Type 1 BS')
ax[2,1].bar(x+width, female_del_Ca_NCC_100, width, color=c6, edgecolor='k', label='GS')

ax[2,1].set_xticks(np.arange(len(fig_labels)))
ax[2,1].set_xticklabels(fig_labels, fontsize=xticklab_size)

ax_in_10 = ax[2,1].inset_axes([left_in, bottom_in, width_in, height_in])
ax_in_10.bar(x2-width, female_del_Ca_normal[7], width, color=c4, edgecolor='k')
ax_in_10.bar(x2, female_del_Ca_NKCC2_100[7], width, color=c5, edgecolor='k')
ax_in_10.bar(x2+width, female_del_Ca_NCC_100[7], width, color=c6, edgecolor='k')
ax_in_10.set_xticks(np.arange(len(fig_labels_2)))
ax_in_10.set_xticklabels(fig_labels_2, fontsize=inset_size)
ax_in_10.yaxis.set_tick_params(labelsize=inset_size)

ax[2,0].legend(loc='upper center', bbox_to_anchor=(0.5, -0.12), fancybox=True, shadow=False, ncol=3, fontsize=leg_size)
ax[2,1].legend(loc='upper center', bbox_to_anchor=(0.5, -0.12), fancybox=True, shadow=False, ncol=3, fontsize=leg_size)

plt.subplots_adjust(left=0.09,
                    bottom=0.08,
                    right=0.98,
                    top=0.96,
                    wspace=0.04,
                    hspace=0.1)

plt.savefig("D:/nephron_Mg/Figures/Figure_5.png")
#plt.show()