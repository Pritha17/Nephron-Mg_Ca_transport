# About
This is the mathematical model for epithelial transport along superficial and juxtamedullary nephrons, specifically focusing on magnesium and calcium transport which is implemented in Python 3. The models account for sex differences, providing a better understanding of nephron functionality. The model also includes nephron adaptations in Type 1 Bartter's syndrome and Gitelman's syndrome. Related research papers are listed below. Please cite appropriately. 

# Instructions
To run the parallel simulation code use command: **python3 parallel_simulate.py --sex [option] --species rat --type [option] --inhibition [option]**

The options here are:

sex: **Male, Female** (required);
type: **superficial, multiple**;
inhibition: **NKCC2-70, NCC-70, ENaC-70, TRPM6-70, TRPM6-99, NKCC2-100 (for Type 1 Bartter's syndorme), NCC-100 (for Gitelman's syndrome)**.

Notes:
* Model parameters can be found in the folder 'datafiles'. For example, PTparams_M_rat.dat contains the male rat parameters for the proximal tubule.
* The code for the in silico inhibition experiments can be found in set_params.py: NKCC2-70 (lines 694-697), NCC-70 (lines 716-721), ENaC-70 (lines 736-738), TRPM6-70 (lines 850-854), TRPM6-99 (lines 856-860).
* The nephron adaptations modeled for Type 1 Bartter's syndrome and Gitelman's syndrome can be found in set_params.py: NKCC2-100 (lines 165-170, 288-293, 713-746), NCC-100 (lines 173-183, 296-306, 757-770).
* Plot folder contains the scripts for plotting the figures shown in the papers.
* Baseline_results.zip contains the baseline output files.

### Understanding output

All the output files' names are in following structure: 'sex_species_segment_concentration/flow_of_solute_in_compartment.txt'. 

Here is an example: female_rat_ccd_con_of_Cl_in_Bath.txt. It contains interstitial concentration of Chloride along cortical collecting duct in female rat.

Another example: male_hum_pt_flow_of_Na_in_Lumen.txt. It contains luminal flow of Sodium along proximal convolute tubule in male human.

These results are scaled per nephron.

The unit of concentration from outputs is **mmol/L (mM)**.

The unit of volume is **nl/min**.

The unit of flow is **pmol/min**.

## Related Work
Please cite appropriate paper(s) when using this model.

Published papers:
* [2024 Dutta et al. "How the kidney regulates magnesium: a modelling study"](https://royalsocietypublishing.org/doi/full/10.1098/rsos.231484)
* [2023 Hakimi et al. "Coupling of renal sodium and calcium transport: A modeling analysis of transporter inhibition and sex differences"](https://journals.physiology.org/doi/abs/10.1152/ajprenal.00145.2023)
* [2019 Hu et al. "Functional implications of the sex differences in transporter abundance along the rat nephron: modeling and analysis"](https://journals.physiology.org/doi/full/10.1152/ajprenal.00352.2019)




### Previous versions
Previous versions of this model code are available [here](https://github.com/Layton-Lab/nephron).
