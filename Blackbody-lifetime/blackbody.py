import numpy as np
from sympy.physics.wigner import *
import matplotlib.pyplot as plt
import logging

logging.getLogger().setLevel("INFO")

class BBRTransition:
    """
    Calculate blackbody radiation-induced transition rates of ground vibrational state of X\Sigma SrF molecule

    Note: make spectroscopic constants floating-point number to avoid overflow
    """
    
    def __init__(self):
        T = 295

        vi = 0
        Ni = 0
        Ji = 1/2
        Fi = 0
        mFi = 0

        vf = 1
        Nf = 1
        Jf = 3/2
        Ff = 1
        mFf = -1

        print("TRansition rate: {:.2e} 1/s".format(self.TransitionRate(T, vi, Ni, Ji, Fi, mFi, vf, Nf, Jf, Ff, mFf)))
        print("TRansition rate to vibrational state v={:d}: {:.2e} 1/s".format(vf, self.TransitionRateOneVibration(T, vi, Ni, Ji, Fi, mFi, vf)))
        print("TRansition rate total: {:.2e} 1/s".format(self.TransitionRateTotal(T, vi, Ni, Ji, Fi, mFi)))

        self.TransitionRateTemp(vi, Ni, Ji, Fi, mFi)

    def TransitionRateTemp(self, vi, Ni, Ji, Fi, mFi):
        T_list = np.linspace(77, 300, 300)
        r_list = np.array([])
        for T in T_list:
            r_list = np.append(r_list, self.TransitionRateTotal(T, vi, Ni, Ji, Fi, mFi))

        plt.plot(T_list, r_list)
        plt.yscale("log")
        plt.ylabel("Total absorption rate (1/s)")
        plt.xlabel("Temperature/K")
        plt.grid(which='major', linestyle='-')
        plt.grid(which='minor', linestyle='--')
        # plt.show()
        plt.savefig("TransitionTemp.jpg", dpi=600)

    def TransitionRateTotal(self, T, vi, Ni, Ji, Fi, mFi):
        """
        Calculate total blackbody radiation-induced transition rates of a state

        vi: nitial state vibrational quantum number
        Ni: initial state rotational quantum number
        S: electron spin
        I: nuclear spin
        Ji: Ni + S
        Fi: Ji + I
        mFi: component of Fi
        """

        r = 0
        for vf in [0, 1]:
            r += self.TransitionRateOneVibration(T, vi, Ni, Ji, Fi, mFi, vf)

        return r

    def TransitionRateOneVibration(self, T, vi, Ni, Ji, Fi, mFi, vf):
        """
        Calculate total blackbody radiation-induced transition rates to one single vibrational state

        vi: nitial state vibrational quantum number
        Ni: initial state rotational quantum number
        S: electron spin
        I: nuclear spin
        Ji: Ni + S
        Fi: Ji + I
        mFi: component of Fi

        vf: final state vibrational quantum number
        """

        S = 1/2
        I = 1/2

        r = 0
        for Nf in np.arange(np.abs(Ni-1), Ni+2):
            for Jf in np.arange(np.abs(Nf-S), Nf+S+1):
                for Ff in np.arange(np.abs(Jf-I), Jf+I+1):
                    for mFf in np.arange(-Ff, Ff+1):
                        r += self.TransitionRate(T, vi, Ni, Ji, Fi, mFi, vf, Nf, Jf, Ff, mFf)

        return r


    def TransitionRate(self, T, vi, Ni, Ji, Fi, mFi, vf, Nf, Jf, Ff, mFf):
        """
        Calculate blackbody radiation-induced transition rates

        vi: nitial state vibrational quantum number
        Ni: initial state rotational quantum number
        S: electron spin
        I: nuclear spin
        Ji: Ni + S
        Fi: Ji + I
        mFi: component of Fi

        vf: final state vibrational quantum number
        Nf: final state rotational quantum number
        Jf: Nf + S
        Ff: Jf + I
        mFf: component of Ff
        """

        epsilon_0 = 8.8541878128e-12 # SI units, vacuum permittivity
        hbar = 1.05457182e-34 # SI units

        omega_e = 509.0 # 1/cm, vibrational frequency
        B_e = 0.2536 # 1/cm, rotational constant

        nu = (vf-vi)*omega_e+(Nf*(Nf+1)-Ni*(Ni+1))*B_e # transition frequency
        nu = np.abs(nu)

        r = self.BBRSpectrum(nu, T)/(6*epsilon_0*hbar**2)*self.AngleOverlap(Ni, Ji, Fi, mFi, Nf, Jf, Ff, mFf)*self.DipoleMoment(vi, vf)**2

        return r

    def BBRSpectrum(self, nu, T):
        """
        Blackbody radiationi spectrum
        nu: frequency in 1/cm
        T: temperature in Kelvin
        """

        h = 6.62607015e-34 # SI units, Planck's constant
        c = 299792458.0 # SI units, speed of light
        kB = 1.380649e-23 # SI units, Boltzmann constant

        nu *= (100*c) # convert nu to Hz

        if nu == 0:
            return 0
        else:
            return 8*np.pi*h*nu**3/c**3/(np.exp(h*nu/kB/T)-1)

    def DipoleMoment(self, vi, vf):
        """
        Transition dipole moment
        vi: initial state vibrational quantum number
        vf: final state vibrational quantum number
        """

        mu = 3.4963 # Debye, electric dipole moment at equilibrium internuclear distnce
        mu *= 3.33564e-30 # convert to Si units
        dmu = 3.17 # Debye/Bohr radius, derivative of dipole moment at equilibrium internuclear distnce
        dmu *= 3.33564e-30/5.29177210903e-11 # convert to SI units
        hbar = 1.05457182e-34 # SI units
        m = 88*19/(88+19)*1.66053906660e-27 # SI unit, reduced mass of SrF
        omega_e = 509.0 # 1/cm, vibrational frequency
        omega_e *= 2*np.pi*100*299792458 # convert to angular frequency rad/s

        if vf == vi:
            return mu
        elif vf == vi+1:
            return np.sqrt(vi+1)*np.sqrt(hbar/2/m/omega_e)*dmu
        elif vf == vi-1:
            return np.sqrt(vi)*np.sqrt(hbar/2/m/omega_e)*dmu
        else:
            logging.info("Unsupported vi and vf relation: vi={vi}, vf={vf}.")
            return 0

    def AngleOverlap(self, Ni, Ji, Fi, mFi, Nf, Jf, Ff, mFf):
        """
        Calculate angle overlapping of initial and final states

        Ni: initial state rotational quantum number
        S: electron spin
        I: nuclear spin
        Ji: Ni + S
        Fi: Ji + I

        Nf: final state rotational quantum number
        Jf: Nf + S
        Ff: Jf + I
        """

        S = 1/2
        I = 1/2

        a = (2*Fi+1)*(2*Ff+1)*(2*Ji+1)*(2*Jf+1)*(2*Ni+1)*(2*Nf+1)
        a *= wigner_6j(Ji, Fi, I, Ff, Jf, 1)**2
        a *= wigner_6j(Ni, Ji, S, Jf, Nf, 1)**2
        a *= wigner_3j(Nf, 1, Ni, 0, 0, 0)**2

        d = 0
        for p in [-1, 0, 1]:
            d += wigner_3j(Ff, 1, Fi, -mFf, p, mFi)**2

        a *= d

        return a

b = BBRTransition()