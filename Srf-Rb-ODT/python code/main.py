import numpy as np
from classes import *


LaserPower_W = 5 # laser power in W
LaserRadius_inve2_um = 40 # 1/e^2 radius of laser beam, in um
LaserIntensity_kW_invcm2 = (LaserPower_W/2/np.pi/(LaserRadius_inve2_um/2)**2)/1e3*1e8 # peak Laser intensity in kW/cm^2
LaserPolarization = 0 # ODT laser polarization, 0 for linear, +/-1 for circular

SrF_state_1 = Hunds_case_b_state(label="SrF XSigma", Lambda=0, N=1, S=1/2, J=3/2, I=1/2, F=2, mF=0)
SrF_state_2 = Hunds_case_b_state(label="SrF XSigma", Lambda=0, N=1, S=1/2, J=3/2, I=1/2, F=1, mF=0, JMixing=[{"mixing coefficient":0.8880, "J":3/2}, {"mixing coefficient":0.45984345162, "J":1/2}])
SrF_state_3 = Hunds_case_b_state(label="SrF XSigma", Lambda=0, N=1, S=1/2, J=1/2, I=1/2, F=0, mF=0)
SrF_state_4 = Hunds_case_b_state(label="SrF XSigma", Lambda=0, N=1, S=1/2, J=1/2, I=1/2, F=1, mF=0, JMixing=[{"mixing coefficient":-0.45984345162, "J":3/2}, {"mixing coefficient":0.8880, "J":1/2}])

SrF_state_5 = Hunds_case_b_state(label="SrF XSigma", Lambda=0, N=0, S=1/2, J=1/2, I=1/2, F=1, mF=0)
SrF_state_6 = Hunds_case_b_state(label="SrF XSigma", Lambda=0, N=0, S=1/2, J=1/2, I=1/2, F=0, mF=0)

SrFacStarkShift(SrF_state_6, LaserWavelength_nm=1064, LaserIntensity_kW_invcm2=LaserIntensity_kW_invcm2, print_dipole_moment=False, print_polarizability=False, print_stark_shift=False, print_scattering_rate=True)

# for state in [SrF_state_1, SrF_state_2, SrF_state_3, SrF_state_4, SrF_state_5, SrF_state_6]:
#     SrFacStarkShift(state, LaserWavelength_nm=1064, LaserIntensity_kW_invcm2=LaserIntensity_kW_invcm2, print_dipole_moment=False, print_polarizability=False, print_stark_shift=False, print_scattering_rate=True)
#     break

Rb_state_1 = Rb_ground_state(label="Rb 5S", energy=0, J=1/2, I=3/2, F=1, mF=0)
Rb_state_2 = Rb_ground_state(label="Rb 5S", energy=0, J=1/2, I=3/2, F=2, mF=0)

for state in [Rb_state_1, Rb_state_2]:
    a = RbacStarkShift(state, LaserWavelength_nm=1064, LaserIntensity_kW_invcm2=LaserIntensity_kW_invcm2, LaserPolarization=LaserPolarization,
                        print_polarizability=False, print_stark_shift=True, print_scattering_rate=True)
