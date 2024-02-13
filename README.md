# About
This is latest version of sex-specific mathematical models for epithelial transport along the nephron implemented in Python 3. Related research papers are listed below. Please cite appropriately. To improve computation time, parallel computation of different types of nephron is implemented for the multiple nephron model. 

# Instructions
To run the parallel simulation code use command: **python3 parallel_simulate.py --sex [option] --species rat --type superficial --inhibition [option]**

The options here are:

sex: **Male, Female** (required);

inhibition: **NKCC2-70, NCC-70, ENaC-70, TRPM6-70, TRPM6-99**.

Notes:
* Model parameters can be found in the folder 'datafiles'.
* The code for the in silico inhibition experiments can be found in set_params.py.

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
* **superficial nephron (sex-specific):** [2019 Hu et al. "Functional implications of the sex differences in transporter abundance along the rat nephron: modeling and analysis"](https://journals.physiology.org/doi/full/10.1152/ajprenal.00352.2019)
* **superficial nephron (sex-specific):** [2023 Hakimi et al. "Coupling of renal sodium and calcium transport: A modeling analysis of transporter inhibition and sex differences"] (https://journals.physiology.org/doi/abs/10.1152/ajprenal.00145.2023)
* **superficial nephron (sex-specific):** [2024 Dutta et al. "Magnesium and Calcium Transport along the Male Rat Kidney: Effect of Diuretics. Mathematical and Computational Applications"] (https://www.mdpi.com/2297-8747/29/1/13)


### Previous versions
Previous versions of this model code are available [here](https://github.com/uwrhu).
