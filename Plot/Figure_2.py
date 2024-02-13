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
    delivery_early_sup = {}
    delivery_late = {}
    transport_early_sup = {}
    transport_late = {}
    conc_seg = []

    for seg in seg_list:
        os.chdir(fname)

        if seg in seg_early:
            file_sup = open(sex + '_' + humOrrat + '_' + seg + '_flow_of_' + solute + '_in_Lumen_sup.txt', 'r')
            file_sup_c = open(sex + '_' + humOrrat + '_' + seg + '_con_of_' + solute + '_in_Lumen_sup.txt', 'r')

            datalist_sup = []
            for i in file_sup:
                line = i.split(' ')
                datalist_sup.append(float(line[0]))

            for i in file_sup_c:
                line = i.split(' ')
                conc_seg.append(float(line[0]))

            delivery_early_sup[seg] = solute_conversion * datalist_sup[0] #* neph_weight[0]

            transport_early_sup[seg] = solute_conversion * (datalist_sup[0] - datalist_sup[-1])

            file_sup.close()
            file_sup_c.close()

        if seg in seg_late:
            file_cd = open(sex + '_' + humOrrat + '_' + seg + '_flow_of_' + solute + '_in_Lumen.txt', 'r')
            file_cd_c = open(sex + '_' + humOrrat + '_' + seg + '_con_of_' + solute + '_in_Lumen.txt', 'r')

            datalist_cd = []
            for i in file_cd:
                line = i.split(' ')
                datalist_cd.append(float(line[0]))
            file_cd.close()

            for i in file_cd_c:
                line = i.split(' ')
                conc_seg.append(float(line[0]))
            file_cd_c.close()

            delivery_late[seg] = solute_conversion * datalist_cd[0]
            transport_late[seg] = solute_conversion * (datalist_cd[0] - datalist_cd[-1])

            if seg == 'IMCD':
                excr = solute_conversion * datalist_cd[-1]

        os.chdir('..')

    del_vals = [delivery_early_sup['PT'], delivery_early_sup['SDL'],
                delivery_early_sup['mTAL'], delivery_early_sup['cTAL'], delivery_early_sup['DCT'],
                delivery_early_sup['CNT'], delivery_late['CCD'], excr]

    trans_vals = [transport_early_sup['PT'] + transport_early_sup['S3'], transport_early_sup['SDL'],
                  transport_early_sup['mTAL'], transport_early_sup['cTAL'], transport_early_sup['DCT'],
                  transport_early_sup['CNT'], transport_late['CCD'] + transport_late['OMCD'] + transport_late['IMCD']]


    return del_vals, trans_vals, conc_seg


# Na
male_del_Na, male_trans_Na, male_con_Na = get_vals('Na', 'Male_rat_normal_sup', 'male')
female_del_Na, female_trans_Na, female_con_Na = get_vals('Na', 'Female_rat_normal_sup', 'female')

# Mg
male_del_Mg, male_trans_Mg, male_con_Mg = get_vals('Mg', 'Male_rat_normal_sup', 'male')
female_del_Mg, female_trans_Mg, female_con_Mg = get_vals('Mg', 'Female_rat_normal_sup', 'female')


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
leg_size = 20
inset_size = 16

fig_labels = ['PT', 'SDL', 'mTAL', 'cTAL', 'DCT', 'CNT', 'CD', 'urine']
fig_labels_1 = ['PT', 'SDL', 'mTAL', 'cTAL', 'DCT', 'CNT', 'CD']

# Plotting

fig, ax = plt.subplots(3, 2)
fig.set_figheight(15)
fig.set_figwidth(17)
x = np.arange(len(fig_labels))
x1 = np.arange(len(fig_labels_1))

# Mg delivery
ax[0,0].bar(x-width, male_del_Mg, width, color=c6, edgecolor='k')
ax[0,0].bar(x, female_del_Mg, width, color=c9, edgecolor='k')

ax[0,0].set_xticks(np.arange(len(fig_labels)))
ax[0,0].set_xticklabels(fig_labels, fontsize=xticklab_size)
ax[0,0].set_ylabel("Mg$^{2+}$ delivery ($\mu$mol/min)", fontsize=ylab_size)

fig_labels_2 = ['CNT', 'CD', 'urine']
x2 = np.arange(len(fig_labels_2))
left_in, bottom_in, width_in, height_in = [0.65, 0.43, 0.33, 0.52]

ax_in_00 = ax[0,0].inset_axes([left_in, bottom_in, width_in, height_in])
ax_in_00.bar(x2-width, male_del_Mg[5:], width, color=c6, edgecolor='k')
ax_in_00.bar(x2, female_del_Mg[5:], width, color=c9, edgecolor='k')
ax_in_00.set_xticks(np.arange(len(fig_labels_2)))
ax_in_00.set_xticklabels(fig_labels_2, fontsize=12)
ax_in_00.yaxis.set_tick_params(labelsize=14)

# Na delivery
ax[0,1].bar(x-width, male_del_Na, width, color=c6, edgecolor='k', label='Male')
ax[0,1].bar(x, female_del_Na, width, color=c9, edgecolor='k', label='Female')

ax[0,1].set_xticks(np.arange(len(fig_labels)))
ax[0,1].set_xticklabels(fig_labels, fontsize=xticklab_size)
ax[0,1].set_ylabel("Na$^+$ delivery ($\mu$mol/min)", fontsize=ylab_size)   #$\mu$mol/min

ax_in_01 = ax[0,1].inset_axes([left_in, bottom_in, width_in, height_in])
ax_in_01.bar(x2-width, male_del_Na[5:], width, color=c6, edgecolor='k')
ax_in_01.bar(x2, female_del_Na[5:], width, color=c9, edgecolor='k')
ax_in_01.set_xticks(np.arange(len(fig_labels_2)))
ax_in_01.set_xticklabels(fig_labels_2, fontsize=12)
ax_in_01.yaxis.set_tick_params(labelsize=14)

# Mg transport
ax[1,0].bar(x1-width, male_trans_Mg, width, color=c6, edgecolor='k', label='Male')
ax[1,0].bar(x1, female_trans_Mg, width, color=c9, edgecolor='k', label='Female')

ax[1,0].set_xticks(np.arange(len(fig_labels_1)))
ax[1,0].set_xticklabels(fig_labels_1, fontsize=xticklab_size)
ax[1,0].set_ylabel("Mg$^{2+}$ transport ($\mu$mol/min)", fontsize=ylab_size)
ax[1,0].legend(loc='upper left', fontsize=leg_size)

# Na transport
ax[1,1].bar(x1-width, male_trans_Na, width, color=c6, edgecolor='k', label='Male')
ax[1,1].bar(x1, female_trans_Na, width, color=c9, edgecolor='k', label='Female')

ax[1,1].set_xticks(np.arange(len(fig_labels_1)))
ax[1,1].set_xticklabels(fig_labels_1, fontsize=xticklab_size)
ax[1,1].set_ylabel("Na$^+$ transport ($\mu$mol/min)", fontsize=ylab_size)   #$\mu$mol/min

fig_labels_3 = ['CNT', 'CD']
x3 = np.arange(len(fig_labels_3))
left_in_3, bottom_in_3, width_in_3, height_in_3 = [0.77, 0.43, 0.2, 0.45]

ax_in_11 = ax[1,1].inset_axes([left_in_3, bottom_in_3, width_in_3, height_in_3])
ax_in_11.bar(x3-width, male_trans_Na[5:], width, color=c6, edgecolor='k')
ax_in_11.bar(x3, female_trans_Na[5:], width, color=c9, edgecolor='k')
ax_in_11.set_xticks(np.arange(len(fig_labels_3)))
ax_in_11.set_xticklabels(fig_labels_3, fontsize=12)
ax_in_11.yaxis.set_tick_params(labelsize=14)

# Mg concentration
lens_sup = {'PT': 2, 'SDL': 0.14, 'mTAL': 0.2, 'cTAL': 0.2, 'DCT': 0.1, 'CNT': 0.2, 'CCD':0.2, 'OMCD':0.2, 'IMCD':0.46}

pos_PT = [lens_sup['PT']*i/200 for i in range(201)] #this is PCT/S3
pos_SDL = [pos_PT[-1]+lens_sup['SDL']*i/199 for i in range(200)]
pos_mTAL = [pos_SDL[-1]+lens_sup['mTAL']*i/199 for i in range(200)]
pos_cTAL = [pos_mTAL[-1]+lens_sup['cTAL']*i/199 for i in range(200)]
pos_DCT = [pos_cTAL[-1]+lens_sup['DCT']*i/199 for i in range(200)]
pos_CNT = [pos_DCT[-1]+lens_sup['CNT']*i/199 for i in range(200)]
pos_CCD = [pos_CNT[-1]+lens_sup['CCD']*i/199 for i in range(200)]
pos_OMCD = [pos_CCD[-1]+lens_sup['OMCD']*i/199 for i in range(200)]
pos_IMCD = [pos_OMCD[-1]+lens_sup['IMCD']*i/199 for i in range(200)]

pos_TAL = pos_mTAL + pos_cTAL
pos_CD = pos_CCD + pos_OMCD + pos_IMCD

ax[2,0].plot(pos_PT, male_con_Mg[0:201], color=c6, linewidth=3.0, label='Male')
ax[2,0].plot(pos_SDL, male_con_Mg[201:401], color=c6, linewidth=3.0)
ax[2,0].plot(pos_TAL, male_con_Mg[401:801], color=c6, linewidth=3.0)
ax[2,0].plot(pos_DCT, male_con_Mg[801:1001], color=c6, linewidth=3.0)
ax[2,0].plot(pos_CNT, male_con_Mg[1001:1201], color=c6, linewidth=3.0)
ax[2,0].plot(pos_CD, male_con_Mg[1201:1801], color=c6, linewidth=3.0)

ax[2,0].plot(pos_PT, female_con_Mg[0:201], color=c9, linewidth=3.0, label='Female')
ax[2,0].plot(pos_SDL, female_con_Mg[201:401], color=c9, linewidth=3.0)
ax[2,0].plot(pos_TAL, female_con_Mg[401:801], color=c9, linewidth=3.0)
ax[2,0].plot(pos_DCT, female_con_Mg[801:1001], color=c9, linewidth=3.0)
ax[2,0].plot(pos_CNT, female_con_Mg[1001:1201], color=c9, linewidth=3.0)
ax[2,0].plot(pos_CD, female_con_Mg[1201:1801], color=c9, linewidth=3.0)

ax[2,0].axvline(x=pos_PT[-1], ls='--', color='grey')
ax[2,0].text(pos_PT[60],0.1,'PT', fontsize=xticklab_size)
ax[2,0].axvline(x=pos_SDL[-1], ls='--', color='grey')
ax[2,0].text(pos_PT[-6],0.5,'SDL', fontsize=xticklab_size)
ax[2,0].axvline(x=pos_TAL[-1], ls='--', color='grey')
ax[2,0].text(pos_TAL[80],0.1,'TAL', fontsize=xticklab_size)
ax[2,0].axvline(x=pos_DCT[-1], ls='--', color='grey')
ax[2,0].text(pos_TAL[-90],1.1,'DCT', fontsize=xticklab_size)
ax[2,0].axvline(x=pos_CNT[-1], ls='--', color='grey')
ax[2,0].text(pos_DCT[-5],0.5,'CNT', fontsize=xticklab_size)
#ax[2,0].axvline(x=1801, ls='--', color='grey')
ax[2,0].text(pos_CD[300],0.1,'CD', fontsize=xticklab_size)

ax[2,0].margins(x=0)
ax[2,0].tick_params(axis='x', labelsize=xticklab_size)
ax[2,0].set_xlabel("Nephron length (cm)", fontsize=ylab_size)
ax[2,0].set_ylabel("Mg$^{2+}$ concentration (mM)", fontsize=ylab_size)
ax[2,0].legend(fontsize=leg_size)

# Na concentration
ax[2,1].plot(pos_PT, male_con_Na[0:201], color=c6, linewidth=3.0, label='Male')
ax[2,1].plot(pos_SDL, male_con_Na[201:401], color=c6, linewidth=3.0)
ax[2,1].plot(pos_TAL, male_con_Na[401:801], color=c6, linewidth=3.0)
ax[2,1].plot(pos_DCT, male_con_Na[801:1001], color=c6, linewidth=3.0)
ax[2,1].plot(pos_CNT, male_con_Na[1001:1201], color=c6, linewidth=3.0)
ax[2,1].plot(pos_CD, male_con_Na[1201:1801], color=c6, linewidth=3.0)

ax[2,1].plot(pos_PT, female_con_Na[0:201], color=c9, linewidth=3.0, label='Female')
ax[2,1].plot(pos_SDL, female_con_Na[201:401], color=c9, linewidth=3.0)
ax[2,1].plot(pos_TAL, female_con_Na[401:801], color=c9, linewidth=3.0)
ax[2,1].plot(pos_DCT, female_con_Na[801:1001], color=c9, linewidth=3.0)
ax[2,1].plot(pos_CNT, female_con_Na[1001:1201], color=c9, linewidth=3.0)
ax[2,1].plot(pos_CD, female_con_Na[1201:1801], color=c9, linewidth=3.0)

ax[2,1].axvline(x=pos_PT[-1], ls='--', color='grey')
ax[2,1].text(pos_PT[60],20,'PT', fontsize=xticklab_size)
ax[2,1].axvline(x=pos_SDL[-1], ls='--', color='grey')
ax[2,1].text(pos_PT[-6],80,'SDL', fontsize=xticklab_size)
ax[2,1].axvline(x=pos_TAL[-1], ls='--', color='grey')
ax[2,1].text(pos_TAL[80],20,'TAL', fontsize=xticklab_size)
ax[2,1].axvline(x=pos_DCT[-1], ls='--', color='grey')
ax[2,1].text(pos_TAL[-90],150,'DCT', fontsize=xticklab_size)
ax[2,1].axvline(x=pos_CNT[-1], ls='--', color='grey')
ax[2,1].text(pos_DCT[-5],100,'CNT', fontsize=xticklab_size)
#ax[2,0].axvline(x=1801, ls='--', color='grey')
ax[2,1].text(pos_CD[300],20,'CD', fontsize=xticklab_size)

ax[2,1].margins(x=0)
#ax[2,0].set_xticks([])
ax[2,1].tick_params(axis='x', labelsize=xticklab_size)
ax[2,1].set_xlabel("Nephron length (cm)", fontsize=ylab_size)
ax[2,1].set_ylabel("Na$^{+}$ concentration (mM)", fontsize=ylab_size)

texts = ['A', 'B', 'C', 'D', 'E', 'F']
axes = fig.get_axes()
for a,l in zip(axes, texts):
    a.annotate(l, xy=(-0.04, 1.03), xycoords="axes fraction", fontsize=20, weight = 'bold')

plt.subplots_adjust(left=0.07,
                    bottom=0.06,
                    right=0.99,
                    top=0.96,
                    wspace=0.16,
                    hspace=0.2)

plt.savefig("D:/nephron_Mg/Figures/Figure_2.png")
