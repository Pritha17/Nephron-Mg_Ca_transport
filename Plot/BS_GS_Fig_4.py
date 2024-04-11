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

seg_list = ['PT', 'S3', 'SDL', 'LDL', 'LAL', 'mTAL', 'cTAL', 'DCT', 'CNT', 'CCD', 'OMCD', 'IMCD']
seg_early = ['PT', 'S3', 'SDL', 'LDL', 'LAL', 'mTAL', 'cTAL', 'DCT', 'CNT']
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
solute_conversion = cf_solute
volume_conversion = cf_volume


def get_vals(solute, fname, sex):
    delivery_early_sup = {}
    delivery_early_jux = {}
    delivery_early = {}
    delivery_late = {}
    transport_early_sup = {}
    transport_early_jux = {}
    transport_early = {}
    transport_late = {}


    for seg in seg_list:
        os.chdir(fname)

        if seg in seg_early:
            if seg not in ['LDL', 'LAL']:
                file_sup = open(sex + '_' + humOrrat + '_' + seg + '_flow_of_' + solute + '_in_Lumen_sup.txt', 'r')
                datalist_sup = []
                for i in file_sup:
                    line = i.split(' ')
                    datalist_sup.append(float(line[0]))
                file_sup.close()

            file_jux1 = open(sex + '_' + humOrrat + '_' + seg + '_flow_of_' + solute + '_in_Lumen_jux1.txt', 'r')
            file_jux2 = open(sex + '_' + humOrrat + '_' + seg + '_flow_of_' + solute + '_in_Lumen_jux2.txt', 'r')
            file_jux3 = open(sex + '_' + humOrrat + '_' + seg + '_flow_of_' + solute + '_in_Lumen_jux3.txt', 'r')
            file_jux4 = open(sex + '_' + humOrrat + '_' + seg + '_flow_of_' + solute + '_in_Lumen_jux4.txt', 'r')
            file_jux5 = open(sex + '_' + humOrrat + '_' + seg + '_flow_of_' + solute + '_in_Lumen_jux5.txt', 'r')

            datalist_jux1 = []
            datalist_jux2 = []
            datalist_jux3 = []
            datalist_jux4 = []
            datalist_jux5 = []

            for i in file_jux1:
                line = i.split(' ')
                datalist_jux1.append(float(line[0]))
            for i in file_jux2:
                line = i.split(' ')
                datalist_jux2.append(float(line[0]))
            for i in file_jux3:
                line = i.split(' ')
                datalist_jux3.append(float(line[0]))
            for i in file_jux4:
                line = i.split(' ')
                datalist_jux4.append(float(line[0]))
            for i in file_jux5:
                line = i.split(' ')
                datalist_jux5.append(float(line[0]))

            if seg in ['LDL', 'LAL']:
                delivery_early_sup[seg] = 0.0
            else:
                delivery_early_sup[seg] = solute_conversion * neph_weight[0] * datalist_sup[0]
                file_sup.close()

            temp_jux1_d = solute_conversion * neph_weight[1] * datalist_jux1[0]
            temp_jux2_d = solute_conversion * neph_weight[2] * datalist_jux2[0]
            temp_jux3_d = solute_conversion * neph_weight[3] * datalist_jux3[0]
            temp_jux4_d = solute_conversion * neph_weight[4] * datalist_jux4[0]
            temp_jux5_d = solute_conversion * neph_weight[5] * datalist_jux5[0]

            delivery_early_jux[seg] = temp_jux1_d + temp_jux2_d + temp_jux3_d + temp_jux4_d + temp_jux5_d
            delivery_early[seg] = delivery_early_sup[seg] + delivery_early_jux[seg]

            temp_jux1_t = solute_conversion * neph_weight[1] * (datalist_jux1[0] - datalist_jux1[-1])
            temp_jux2_t = solute_conversion * neph_weight[2] * (datalist_jux2[0] - datalist_jux2[-1])
            temp_jux3_t = solute_conversion * neph_weight[3] * (datalist_jux3[0] - datalist_jux3[-1])
            temp_jux4_t = solute_conversion * neph_weight[4] * (datalist_jux4[0] - datalist_jux4[-1])
            temp_jux5_t = solute_conversion * neph_weight[5] * (datalist_jux5[0] - datalist_jux5[-1])

            if seg in ['LDL', 'LAL']:
                transport_early_sup[seg] = 0.0

            transport_early_sup[seg] = solute_conversion * (datalist_sup[0] - datalist_sup[-1])  # * neph_weight[0]
            transport_early_jux[seg] = temp_jux1_t + temp_jux2_t + temp_jux3_t + temp_jux4_t + temp_jux5_t
            transport_early[seg] = transport_early_sup[seg] + transport_early_jux[seg]

            file_jux1.close()
            file_jux2.close()
            file_jux3.close()
            file_jux4.close()
            file_jux5.close()

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

    del_vals_sup = [delivery_early_sup['PT'], delivery_early_sup['SDL'], delivery_early_sup['LDL'], delivery_early_sup['LAL'], delivery_early_sup['mTAL'],
                    delivery_early_sup['cTAL'], delivery_early_sup['DCT'], delivery_early_sup['CNT'], delivery_late['CCD'], excr]

    del_vals_jux = [delivery_early_jux['PT'], delivery_early_jux['SDL'], delivery_early_jux['LDL'], delivery_early_jux['LAL'], delivery_early_jux['mTAL'],
                    delivery_early_jux['cTAL'], delivery_early_jux['DCT'], delivery_early_jux['CNT'], 0, 0]

    trans_vals_sup = [transport_early_sup['PT'] + transport_early_sup['S3'], transport_early_sup['SDL'], transport_early_sup['LDL'],
                    transport_early_sup['LAL'], transport_early_sup['mTAL'], transport_early_sup['cTAL'], transport_early_sup['DCT'],
                    transport_early_sup['CNT'], transport_late['CCD'] + transport_late['OMCD'] + transport_late['IMCD']]

    trans_vals_jux = [transport_early_jux['PT'] + transport_early_jux['S3'], transport_early_jux['SDL'], transport_early_jux['LDL'],
                    transport_early_sup['LAL'], transport_early_jux['mTAL'], transport_early_jux['cTAL'], transport_early_jux['DCT'],
                    transport_early_jux['CNT'], 0]


    return del_vals_sup, del_vals_jux, trans_vals_sup, trans_vals_jux

# Na
male_del_Na_sup, male_del_Na_jux, male_trans_Na_sup, male_trans_Na_jux = get_vals('Na', 'Male_rat_normal_multiple', 'male') # Male_rat_normal_multiple
female_del_Na_sup, female_del_Na_jux, female_trans_Na_sup, female_trans_Na_jux = get_vals('Na', 'Female_rat_normal_multiple', 'female')   # Female_rat_normal_multiple

# Ca
male_del_Ca_sup, male_del_Ca_jux, male_trans_Ca_sup, male_trans_Ca_jux = get_vals('Ca', 'Male_rat_normal_multiple', 'male')
female_del_Ca_sup, female_del_Ca_jux, female_trans_Ca_sup, female_trans_Ca_jux = get_vals('Ca', 'Female_rat_normal_multiple', 'female')

# Mg
male_del_Mg_sup, male_del_Mg_jux, male_trans_Mg_sup, male_trans_Mg_jux = get_vals('Mg', 'Male_rat_normal_multiple', 'male')
female_del_Mg_sup, female_del_Mg_jux, female_trans_Mg_sup, female_trans_Mg_jux = get_vals('Mg', 'Female_rat_normal_multiple', 'female')

male_del_Mg_normal = np.array(male_del_Mg_sup) +  np.array(male_del_Mg_jux)
female_del_Mg_normal = np.array(female_del_Mg_sup) +  np.array(female_del_Mg_jux)

# colors
c1 = 'cyan' # paleturquoise
c2 = 'white' #'cyan'
c3 = 'teal'
c4 = 'orchid' # pink
c5 = 'orchid'
c6 = 'darkmagenta'

width = 0.15

# fontsizes
xlab_size = 16
xticklab_size = 16
ylab_size = 20
yticklab_size = 16
title_size = 22
leg_size = 18
inset_size = 16

fig_labels = ['PT', 'SDL', 'LDL', 'LAL', 'mTAL', 'cTAL', 'DCT', 'CNT', 'CD', 'urine']

fig_labels_1 = ['PT', 'SDL', 'LDL', 'LAL', 'mTAL', 'cTAL', 'DCT', 'CNT', 'CD']

# Plotting

fig, ax = plt.subplots(3, 2, sharex=True)
fig.set_figheight(10)
fig.set_figwidth(18)
x = np.arange(len(fig_labels))
x1 = np.arange(len(fig_labels_1))

# Na
# delivery
ax[0,0].bar(x, male_del_Na_sup, width, color=c1, edgecolor='k', label='male')
ax[0,0].bar(x, male_del_Na_jux, width, bottom=male_del_Na_sup, color=c2, edgecolor='k')

ax[0,0].bar(x+width, female_del_Na_sup, width, color=c4, edgecolor='k', label='female')
ax[0,0].bar(x+width, female_del_Na_jux, width, bottom=female_del_Na_sup, color=c2, edgecolor='k')

ax[0,0].set_xticks(np.arange(len(fig_labels)))
ax[0,0].set_xticklabels(fig_labels, fontsize=xticklab_size)
ax[0,0].set_ylabel("Na$^{2+}$ delivery\n($\mu$mol/min)", fontsize=ylab_size)
ax[0,0].legend(fontsize=leg_size)


# Transport
ax[0,1].bar(x1, male_trans_Na_sup, width, color=c1, edgecolor='k')
ax[0,1].bar(x1, male_trans_Na_jux, width, bottom=male_trans_Na_sup, color=c2, edgecolor='k')

ax[0,1].bar(x1+width, female_trans_Na_sup, width, color=c4, edgecolor='k')
ax[0,1].bar(x1+width, female_trans_Na_jux, width, bottom=female_trans_Na_sup, color=c2, edgecolor='k')

ax[0,1].set_xticks(np.arange(len(fig_labels)))
ax[0,1].set_xticklabels(fig_labels, fontsize=xticklab_size)
ax[0,1].set_ylabel("Na$^{2+}$ transport\n($\mu$mol/min)", fontsize=ylab_size)


# Mg
# delivery
ax[1,0].bar(x, male_del_Mg_sup, width, color=c1, edgecolor='k')
ax[1,0].bar(x, male_del_Mg_jux, width, bottom=male_del_Mg_sup, color=c2, edgecolor='k')

ax[1,0].bar(x+width, female_del_Mg_sup, width, color=c4, edgecolor='k')
ax[1,0].bar(x+width, female_del_Mg_jux, width, bottom=female_del_Mg_sup, color=c2, edgecolor='k')

ax[1,0].set_xticks(np.arange(len(fig_labels)))
ax[1,0].set_xticklabels(fig_labels, fontsize=xticklab_size)
ax[1,0].set_ylabel("Mg$^{2+}$ delivery\n($\mu$mol/min)", fontsize=ylab_size)

# transport
ax[1,1].bar(x1, male_trans_Mg_sup, width, color=c1, edgecolor='k')
ax[1,1].bar(x1, male_trans_Mg_jux, width, bottom=male_trans_Mg_sup, color=c2, edgecolor='k')

ax[1,1].bar(x1+width, female_trans_Mg_sup, width, color=c4, edgecolor='k')
ax[1,1].bar(x1+width, female_trans_Mg_jux, width, bottom=female_trans_Mg_sup, color=c2, edgecolor='k')

ax[1,1].set_xticks(np.arange(len(fig_labels)))
ax[1,1].set_xticklabels(fig_labels, fontsize=xticklab_size)
ax[1,1].set_ylabel("Mg$^{2+}$ transport\n($\mu$mol/min)", fontsize=ylab_size)

# Ca
# delivery
ax[2,0].bar(x, male_del_Ca_sup, width, color=c1, edgecolor='k', label='male')
ax[2,0].bar(x, male_del_Ca_jux, width, bottom=male_del_Ca_sup, color=c2, edgecolor='k')

ax[2,0].bar(x+width, female_del_Ca_sup, width, color=c4, edgecolor='k', label='female')
ax[2,0].bar(x+width, female_del_Ca_jux, width, bottom=female_del_Ca_sup, color=c2, edgecolor='k')

ax[2,0].set_xticks(np.arange(len(fig_labels)))
ax[2,0].set_xticklabels(fig_labels, fontsize=xticklab_size)
ax[2,0].set_ylabel("Ca$^{2+}$ delivery\n($\mu$mol/min)", fontsize=ylab_size)

# transport
ax[2,1].bar(x1, male_trans_Ca_sup, width, color=c1, edgecolor='k')
ax[2,1].bar(x1, male_trans_Ca_jux, width, bottom=male_trans_Ca_sup, color=c2, edgecolor='k')

ax[2,1].bar(x1+width, female_trans_Ca_sup, width, color=c4, edgecolor='k')
ax[2,1].bar(x1+width, female_trans_Ca_jux, width, bottom=female_trans_Ca_sup, color=c2, edgecolor='k')

ax[2,1].set_xticks(np.arange(len(fig_labels)))
ax[2,1].set_xticklabels(fig_labels, fontsize=xticklab_size)
ax[2,1].set_ylabel("Ca$^{2+}$ transport\n($\mu$mol/min)", fontsize=ylab_size)

plt.subplots_adjust(left=0.08,
                    bottom=0.1,
                    right=0.99,
                    top=0.95,
                    wspace=0.2,
                    hspace=0.1)

plt.savefig("D:/nephron_Mg/Figures/Figure_4.png")
#plt.show()
