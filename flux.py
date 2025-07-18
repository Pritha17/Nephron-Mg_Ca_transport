import numpy as np
from defs import *
from values import *
from set_params import set_torq_params
import electrochemical 
import water
import glucose
import cotransport
import NHE3
import ATPase
import NKCC
import KCC
import NCC
import ENaC
import Pendrin
import AE1
import NHE1
import math

import TRPV5
import NCX1

import TRPM6
import NaMgX

def compute_fluxes (cell,j):
    # update LIS-bath surface area, based on LIS volume
    cell.area[4][5] = 0.02*max(cell.vol[4]/cell.volref[4],1.0)
    cell.area[5][4] = cell.area[4][5]  
    
    # compute water fluxes
    jvol = water.compute_water_fluxes(cell)
    # if cell.segment == 'PT':
    #     print('Water Fluxes:')
    #     print(jvol)
    #     pause = input()
    
    # compute electrochemical convective and diffusive fluxes
    jsol,delmu,electro_flux,convective_flux = electrochemical.compute_ecd_fluxes(cell,jvol)
    
    for i in range(len(cell.trans)):
        
        transporter_type = cell.trans[i].type
        memb_id = cell.trans[i].membrane_id
      
        # compute flux through specific transporters
        if transporter_type == 'SGLT1':
            solute_id,fluxsglt1=glucose.sglt1(cell,cell.ep,memb_id,cell.trans[i].act,cell.area)
            for i in range(len(solute_id)):
                jsol[solute_id[i]][memb_id[0]][memb_id[1]] += fluxsglt1[i]
        elif transporter_type == 'SGLT2':
            solute_id,fluxsglt2=glucose.sglt2(cell,cell.ep,memb_id,cell.trans[i].act,cell.area)           
            for i in range(len(solute_id)):
                jsol[solute_id[i]][memb_id[0]][memb_id[1]] += fluxsglt2[i]
        elif transporter_type == 'GLUT1':
            solute_id,fluxglut1=glucose.glut1(cell,cell.ep,memb_id,cell.trans[i].act,cell.area)           
            jsol[solute_id][memb_id[0]][memb_id[1]] += fluxglut1
        elif transporter_type == 'GLUT2':
            solute_id,fluxglut2=glucose.glut2(cell,cell.ep,memb_id,cell.trans[i].act,cell.area)           
            jsol[solute_id][memb_id[0]][memb_id[1]] += fluxglut2      
        elif transporter_type == 'NHE3':
            solute_id,fluxnhe3=NHE3.nhe3(cell,cell.ep,memb_id,cell.trans[i].act,cell.area)
            for i in range(len(solute_id)):
                jsol[solute_id[i]][memb_id[0]][memb_id[1]] += fluxnhe3[i]  
        elif transporter_type == 'NaKATPase':
            solute_id,fluxnakatpase=ATPase.nakatpase(cell,cell.ep,memb_id,cell.trans[i].act,cell.area)
            for i in range(len(solute_id)):
                jsol[solute_id[i]][memb_id[0]][memb_id[1]] += fluxnakatpase[i]
        elif transporter_type == 'HATPase':
            solute_id,fluxhatpase=ATPase.hatpase(cell,cell.ep,memb_id,cell.trans[i].act,cell.area)  
            for i in range(len(solute_id)):
                jsol[solute_id[i]][memb_id[0]][memb_id[1]] += fluxhatpase[i]     
        elif transporter_type == 'NKCC2A':
            solute_id,fluxnkcc2a=NKCC.nkcc2(cell,memb_id,cell.trans[i].act,cell.area,'A')
            for i in range(len(solute_id)):
                jsol[solute_id[i]][memb_id[0]][memb_id[1]] += fluxnkcc2a[i]
        elif transporter_type == 'NKCC2B':
            solute_id,fluxnkcc2b=NKCC.nkcc2(cell,memb_id,cell.trans[i].act,cell.area,'B')
            for i in range(len(solute_id)):
                jsol[solute_id[i]][memb_id[0]][memb_id[1]] += fluxnkcc2b[i]
        elif transporter_type == 'NKCC2F':
            solute_id,fluxnkcc2f=NKCC.nkcc2(cell,memb_id,cell.trans[i].act,cell.area,'F')
            for i in range(len(solute_id)):
                jsol[solute_id[i]][memb_id[0]][memb_id[1]] += fluxnkcc2f[i] 
        elif transporter_type == 'KCC4':
            solute_id,fluxkcc4=KCC.kcc4(cell.conc,memb_id,cell.trans[i].act,cell.area)
            for i in range(len(solute_id)):
                jsol[solute_id[i]][memb_id[0]][memb_id[1]] += fluxkcc4[i]
        elif transporter_type == 'ENaC':
            solute_id,fluxENaC=ENaC.ENaC(cell,j,memb_id,cell.trans[i].act,cell.area,jvol)
            for i in range(len(solute_id)):
                jsol[solute_id[i]][memb_id[0]][memb_id[1]] +=fluxENaC[i]
        elif transporter_type == 'NCC':
            solute_id,fluxncc=NCC.NCC(cell,j,memb_id,cell.trans[i].act,cell.area)
            for i in range(len(solute_id)):
                jsol[solute_id[i]][memb_id[0]][memb_id[1]] +=fluxncc[i]
        elif transporter_type == 'Pendrin':
            solute_id,fluxPendrin=Pendrin.Pendrin(cell,memb_id,cell.trans[i].act,cell.area)
            for i in range(len(solute_id)):
                jsol[solute_id[i]][memb_id[0]][memb_id[1]] +=fluxPendrin[i]
        elif transporter_type =='AE1':
            solute_id,fluxAE1=AE1.AE1(cell,memb_id,cell.trans[i].act,cell.area)
            for i in range(len(solute_id)):
                jsol[solute_id[i]][memb_id[0]][memb_id[1]] +=fluxAE1[i]
        elif transporter_type == 'HKATPase':
            solute_id,fluxhkatpase=ATPase.hkatpase(cell,memb_id,cell.trans[i].act,cell.area)
            for i in range(len(solute_id)):
                jsol[solute_id[i]][memb_id[0]][memb_id[1]] +=fluxhkatpase[i]
        elif transporter_type == 'NHE1':
            solute_id,fluxnhe1=NHE1.NHE1(cell,memb_id,cell.trans[i].act,cell.area)
            for i in range(len(solute_id)):
                jsol[solute_id[i]][memb_id[0]][memb_id[1]] +=fluxnhe1[i]
        elif transporter_type == 'NKCC1':
            solute_id,fluxnakcl2=NKCC.nkcc1(cell,memb_id,cell.trans[i].act,delmu)
            for i in range(len(solute_id)):
                jsol[solute_id[i]][memb_id[0]][memb_id[1]] +=fluxnakcl2[i]

        # Ca2+ related fluxes: (more details given in each module)
        elif transporter_type == 'CaATPase':
            if cell.segment == 'PT' or cell.segment =='S3':
                solute_id,fluxCalatapse=ATPase.calatapse(cell,cell.ep,memb_id,cell.trans[i].act,cell.area)
            else:
                solute_id,fluxCalatapse=ATPase.calatapse_mtal(cell,j,cell.ep,memb_id,cell.trans[i].act,cell.area)
            for i in range(len(solute_id)):
                jsol[solute_id[i]][memb_id[0]][memb_id[1]] += fluxCalatapse[i]
        elif transporter_type == 'MgATPase':
            solute_id,fluxMgatapse=ATPase.Mgatapse(cell,cell.ep,memb_id,cell.trans[i].act,cell.area)
            for i in range(len(solute_id)):
                jsol[solute_id[i]][memb_id[0]][memb_id[1]] += fluxMgatapse[i]
        elif transporter_type == 'TRPV5':
            solute_id, fluxTRPV5 = TRPV5.trpv5(cell, j, cell.ep, memb_id, cell.trans[i].act, cell.area)
            for i in range(len(solute_id)):
                jsol[solute_id[i]][memb_id[0]][memb_id[1]] += fluxTRPV5[i]
        elif transporter_type == 'NCX1':
            solute_id, fluxNCX1 = NCX1.ncx1(cell, j, cell.ep, memb_id, cell.trans[i].act, cell.area)
            for i in range(len(solute_id)):
                jsol[solute_id[i]][memb_id[0]][memb_id[1]] += fluxNCX1[i]

        # Mg2+ related fluxes
        elif transporter_type == 'TRPM6':
            solute_id,fluxTRPM6=TRPM6.trpm6(cell,cell.ep,memb_id,cell.trans[i].act,cell.area)
            for i in range(len(solute_id)):
                jsol[solute_id[i]][memb_id[0]][memb_id[1]] += fluxTRPM6[i]
        elif transporter_type == 'NaMgX':
            solute_id,fluxNaMgX=NaMgX.namgx(cell,memb_id,cell.trans[i].act,cell.area)
            for i in range(len(solute_id)):
                jsol[solute_id[i]][memb_id[0]][memb_id[1]] += fluxNaMgX[i]
        else:
            print('What is this?',transporter_type)
            

    active_jsol = jsol[:] - electro_flux[:] - convective_flux[:]

    jsol = cotransport.compute_cotransport(cell,delmu,jsol)

    # Torque modulated effects:
    if cell.segment=='PT' or cell.segment == 'S3':

        if cell.segment == 'PT':
            TS = 1.3
            scaleT = 1.0
        elif cell.segment == 'S3':
            TS = 1.3
            scaleT = 0.5

        #torque-modulated effects
        
        PM=cell.pres[0]
        Radref,torqR,torqvm,PbloodPT,torqL,torqd = set_torq_params(cell.species,cell.sex,cell.preg)

        if cell.species == 'rat':
            fac1 = 8.0*visc*(cell.vol_init[0]*Vref)*torqL/(Radref**2)
        elif cell.species == 'mou':
            fac1 = 8.0*visc*(cell.vol_init[0]*Vref)*torqL/(Radref**2)
        elif cell.species == 'hum':
            fac1 = 8.0*visc*(cell.volref[0]*Vref)*torqL/(Radref**2)
        else:
            print('cell.species: ' + str(cell.species))
            raise Exception('what is species?')
        fac2 = 1.0 + (torqL+torqd)/Radref + 0.50*((torqL/Radref)**2)
        TM0= fac1*fac2
    
        RMtorq = torqR*(1.0e0+torqvm*(PM - PbloodPT))
        # # tracking
        # fname1 = 'tracking_RMtorq_fluxfile.txt'
        # f1 = open(fname1, 'a')
        # f1.write(str(RMtorq) + '\n')
        # f1.close()

        factor1 = 8.0*visc*(cell.vol[0]*Vref)*torqL/(RMtorq**2) 
        factor2 = 1.0 + (torqL+torqd)/RMtorq + 0.50*((torqL/RMtorq)**2)
        Torque = factor1*factor2
    
        Scaletorq = 1.0 + TS*scaleT*(Torque/TM0-1.0)
        # Scale flux along PCT and S3.
        for i in range(NS):
            jsol[i][0][1]=Scaletorq*jsol[i][0][1]
            jsol[i][1][4]=Scaletorq*jsol[i][1][4]
            jsol[i][1][5]=Scaletorq*jsol[i][1][5]

            active_jsol[i][0][1]=Scaletorq*active_jsol[i][0][1]
            active_jsol[i][1][4]=Scaletorq*active_jsol[i][1][4]
            active_jsol[i][1][5]=Scaletorq*active_jsol[i][1][5]

            electro_flux[i][0][1]=Scaletorq*electro_flux[i][0][1]
            electro_flux[i][1][4]=Scaletorq*electro_flux[i][1][4]
            electro_flux[i][1][5]=Scaletorq*electro_flux[i][1][5]

            convective_flux[i][0][1]=Scaletorq*convective_flux[i][0][1]
            convective_flux[i][1][4]=Scaletorq*convective_flux[i][1][4]
            convective_flux[i][1][5]=Scaletorq*convective_flux[i][1][5]
   
        jvol[0][1]=Scaletorq*jvol[0][1]
        jvol[1][4]=Scaletorq*jvol[1][4]
        jvol[1][5]=Scaletorq*jvol[1][5]
    # if cell.segment == 'LDL':
    #     print(jsol)
    #     input('pause')
    #print("flux", jsol[16,1,4], jsol[16,1,5])
    return jvol,jsol, electro_flux,convective_flux, active_jsol

    
