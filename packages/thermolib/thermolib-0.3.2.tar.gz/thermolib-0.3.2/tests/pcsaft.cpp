#include "pcsaft.h"

#include <cmath>
#include <string>
#include <vector>

#include "C:/document_ygl/code_ygl/_0Nut/include/eigen 3.4.0/Eigen/Dense"
#include "math.h"
using std::vector;
#if defined(HUGE_VAL) && !defined(_HUGE)
#define _HUGE HUGE_VAL
#else
// GCC Version of huge value macro
#if defined(HUGE) && !defined(_HUGE)
#define _HUGE HUGE
#endif
#endif
vector<double> XA_find(vector<double> XA_guess, vector<double> delta_ij,
                       double den, vector<double> x) {
  /**Iterate over this function in order to solve for XA*/
  int num_sites = XA_guess.size();
  vector<double> XA = XA_guess;
  int idxij = -1;  // index for delta_ij
  for (int i = 0; i < num_sites; i++) {
    double summ = 0.;
    for (int j = 0; j < num_sites; j++) {
      idxij += 1;
      summ += den * x[j] * XA_guess[j] * delta_ij[idxij];
    }
    XA[i] = 1. / (1. + summ);
  }
  return XA;
}
vector<double> dXAdt_find(vector<double> delta_ij, double den,
                          vector<double> XA, vector<double> ddelta_dt,
                          vector<double> x) {
  /**Solve for the derivative of XA with respect to temperature.*/
  int num_sites = XA.size();
  Eigen::MatrixXd B = Eigen::MatrixXd::Zero(num_sites, 1);
  Eigen::MatrixXd A = Eigen::MatrixXd::Zero(num_sites, num_sites);
  double summ;
  int ij = 0;
  for (int i = 0; i < num_sites; i++) {
    summ = 0;
    for (int j = 0; j < num_sites; j++) {
      B(i) -= x[j] * XA[j] * ddelta_dt[ij];
      A(i, j) = x[j] * delta_ij[ij];
      summ += x[j] * XA[j] * delta_ij[ij];
      ij += 1;
    }
    A(i, i) = pow(1 + den * summ, 2.) / den;
  }
  Eigen::MatrixXd solution =
      A.lu().solve(B);  // Solves linear system of equations
  vector<double> dXA_dt(num_sites);
  for (int i = 0; i < num_sites; i++) {
    dXA_dt[i] = solution(i);
  }
  return dXA_dt;
}
vector<double> dXAdx_find(vector<int> assoc_num, vector<double> delta_ij,
                          double den, vector<double> XA,
                          vector<double> ddelta_dx, vector<double> x) {
  /**Solve for the derivative of XA with respect to composition, or actually
  rho_i (the molar density of component i, which equals x_i * rho).*/
  int num_sites = XA.size();
  int ncomp = assoc_num.size();
  Eigen::MatrixXd B(num_sites * ncomp, 1);
  Eigen::MatrixXd A =
      Eigen::MatrixXd::Zero(num_sites * ncomp, num_sites * ncomp);
  double sum1, sum2;
  int idx1 = 0;
  int ij = 0;
  for (int i = 0; i < ncomp; i++) {
    for (int j = 0; j < num_sites; j++) {
      sum1 = 0;
      for (int k = 0; k < num_sites; k++) {
        sum1 = sum1 +
               den * x[k] *
                   (XA[k] *
                    ddelta_dx[i * num_sites * num_sites + j * num_sites + k]);
        A(ij, i * num_sites + k) =
            XA[j] * XA[j] * den * x[k] * delta_ij[j * num_sites + k];
      }
      sum2 = 0;
      for (int l = 0; l < assoc_num[i]; l++) {
        sum2 = sum2 +
               XA[idx1 + l] * delta_ij[idx1 * num_sites + l * num_sites + j];
      }
      A(ij, ij) = A(ij, ij) + 1;
      B(ij) = -1 * XA[j] * XA[j] * (sum1 + sum2);
      ij += 1;
    }
    idx1 += assoc_num[i];
  }
  Eigen::MatrixXd solution =
      A.lu().solve(B);  // Solves linear system of equations
  vector<double> dXA_dx(num_sites * ncomp);
  for (int i = 0; i < num_sites * ncomp; i++) {
    dXA_dx[i] = solution(i);
  }
  return dXA_dx;
}
double pcsaft_Z_cpp(double t, double rho, vector<double> x, add_args &cppargs) {
  /**
  Calculate the compressibility factor.
  */
  int ncomp = x.size();  // number of components
  vector<double> d(ncomp);
  for (int i = 0; i < ncomp; i++) {
    d[i] = cppargs.s[i] * (1 - 0.12 * exp(-3 * cppargs.e[i] / t));
  }
  if (!cppargs.z.empty()) {
    for (int i = 0; i < ncomp; i++) {
      if (cppargs.z[i] != 0) {
        d[i] = cppargs.s[i] *
               (1 - 0.12);  // for ions the diameter is assumed to be
                            // temperature independent (see Held et al. 2014)
      }
    }
  }
  double den = rho * N_AV / 1.0e30;
  vector<double> zeta(4, 0);
  double summ;
  for (int i = 0; i < 4; i++) {
    summ = 0;
    for (int j = 0; j < ncomp; j++) {
      summ += x[j] * cppargs.m[j] * pow(d[j], i);
    }
    zeta[i] = PI / 6 * den * summ;
  }
  double eta = zeta[3];
  double m_avg = 0;
  for (int i = 0; i < ncomp; i++) {
    m_avg += x[i] * cppargs.m[i];
  }
  vector<double> ghs(ncomp * ncomp, 0);
  vector<double> denghs(ncomp * ncomp, 0);
  vector<double> e_ij(ncomp * ncomp, 0);
  vector<double> s_ij(ncomp * ncomp, 0);
  double m2es3 = 0.;
  double m2e2s3 = 0.;
  int idx = -1;
  for (int i = 0; i < ncomp; i++) {
    for (int j = 0; j < ncomp; j++) {
      idx += 1;
      if (cppargs.l_ij.empty()) {
        s_ij[idx] = (cppargs.s[i] + cppargs.s[j]) / 2.;
      } else {
        s_ij[idx] =
            (cppargs.s[i] + cppargs.s[j]) / 2. * (1 - cppargs.l_ij[idx]);
      }
      if (!cppargs.z.empty()) {
        if (cppargs.z[i] * cppargs.z[j] <=
            0) {  // for two cations or two anions e_ij is kept at zero to avoid
                  // dispersion between like ions (see Held et al. 2014)
          if (cppargs.k_ij.empty()) {
            e_ij[idx] = sqrt(cppargs.e[i] * cppargs.e[j]);
          } else {
            e_ij[idx] =
                sqrt(cppargs.e[i] * cppargs.e[j]) * (1 - cppargs.k_ij[idx]);
          }
        }
      } else {
        if (cppargs.k_ij.empty()) {
          e_ij[idx] = sqrt(cppargs.e[i] * cppargs.e[j]);
        } else {
          e_ij[idx] =
              sqrt(cppargs.e[i] * cppargs.e[j]) * (1 - cppargs.k_ij[idx]);
        }
      }
      m2es3 = m2es3 + x[i] * x[j] * cppargs.m[i] * cppargs.m[j] * e_ij[idx] /
                          t * pow(s_ij[idx], 3);
      m2e2s3 = m2e2s3 + x[i] * x[j] * cppargs.m[i] * cppargs.m[j] *
                            pow(e_ij[idx] / t, 2) * pow(s_ij[idx], 3);
      ghs[idx] = 1 / (1 - zeta[3]) +
                 (d[i] * d[j] / (d[i] + d[j])) * 3 * zeta[2] / (1 - zeta[3]) /
                     (1 - zeta[3]) +
                 pow(d[i] * d[j] / (d[i] + d[j]), 2) * 2 * zeta[2] * zeta[2] /
                     pow(1 - zeta[3], 3);
      denghs[idx] = zeta[3] / (1 - zeta[3]) / (1 - zeta[3]) +
                    (d[i] * d[j] / (d[i] + d[j])) *
                        (3 * zeta[2] / (1 - zeta[3]) / (1 - zeta[3]) +
                         6 * zeta[2] * zeta[3] / pow(1 - zeta[3], 3)) +
                    pow(d[i] * d[j] / (d[i] + d[j]), 2) *
                        (4 * zeta[2] * zeta[2] / pow(1 - zeta[3], 3) +
                         6 * zeta[2] * zeta[2] * zeta[3] / pow(1 - zeta[3], 4));
    }
  }
  double Zhs =
      zeta[3] / (1 - zeta[3]) +
      3. * zeta[1] * zeta[2] / zeta[0] / (1. - zeta[3]) / (1. - zeta[3]) +
      (3. * pow(zeta[2], 3.) - zeta[3] * pow(zeta[2], 3.)) / zeta[0] /
          pow(1. - zeta[3], 3.);
  static double a0[7] = {0.9105631445,  0.6361281449, 2.6861347891,
                         -26.547362491, 97.759208784, -159.59154087,
                         91.297774084};
  static double a1[7] = {-0.3084016918, 0.1860531159,  -2.5030047259,
                         21.419793629,  -65.255885330, 83.318680481,
                         -33.746922930};
  static double a2[7] = {-0.0906148351, 0.4527842806,  0.5962700728,
                         -1.7241829131, -4.1302112531, 13.776631870,
                         -8.6728470368};
  static double b0[7] = {0.7240946941,  2.2382791861, -4.0025849485,
                         -21.003576815, 26.855641363, 206.55133841,
                         -355.60235612};
  static double b1[7] = {-0.5755498075, 0.6995095521, 3.8925673390,
                         -17.215471648, 192.67226447, -161.82646165,
                         -165.20769346};
  static double b2[7] = {0.0976883116, -0.2557574982, -9.1558561530,
                         20.642075974, -38.804430052, 93.626774077,
                         -29.666905585};
  vector<double> a(7, 0);
  vector<double> b(7, 0);
  for (int i = 0; i < 7; i++) {
    a[i] = a0[i] + (m_avg - 1.) / m_avg * a1[i] +
           (m_avg - 1.) / m_avg * (m_avg - 2.) / m_avg * a2[i];
    b[i] = b0[i] + (m_avg - 1.) / m_avg * b1[i] +
           (m_avg - 1.) / m_avg * (m_avg - 2.) / m_avg * b2[i];
  }
  double detI1_det = 0.0;
  double detI2_det = 0.0;
  double I2 = 0.0;
  for (int i = 0; i < 7; i++) {
    detI1_det += a[i] * (i + 1) * pow(eta, i);
    detI2_det += b[i] * (i + 1) * pow(eta, i);
    I2 += b[i] * pow(eta, i);
  }
  double C1 =
      1. /
      (1. + m_avg * (8 * eta - 2 * eta * eta) / pow(1 - eta, 4) +
       (1 - m_avg) *
           (20 * eta - 27 * eta * eta + 12 * pow(eta, 3) - 2 * pow(eta, 4)) /
           pow((1 - eta) * (2 - eta), 2.0));
  double C2 =
      -1. * C1 * C1 *
      (m_avg * (-4 * eta * eta + 20 * eta + 8) / pow(1 - eta, 5) +
       (1 - m_avg) * (2 * pow(eta, 3) + 12 * eta * eta - 48 * eta + 40) /
           pow((1 - eta) * (2 - eta), 3.0));
  summ = 0.0;
  for (int i = 0; i < ncomp; i++) {
    summ +=
        x[i] * (cppargs.m[i] - 1) / ghs[i * ncomp + i] * denghs[i * ncomp + i];
  }
  double Zid = 1.0;
  double Zhc = m_avg * Zhs - summ;
  double Zdisp = -2 * PI * den * detI1_det * m2es3 -
                 PI * den * m_avg * (C1 * detI2_det + C2 * eta * I2) * m2e2s3;
  // Dipole term (Gross and Vrabec term) --------------------------------------
  double Zpolar = 0;
  if (!cppargs.dipm.empty()) {
    double A2 = 0.;
    double A3 = 0.;
    double dA2_det = 0.;
    double dA3_det = 0.;
    vector<double> adip(5, 0);
    vector<double> bdip(5, 0);
    vector<double> cdip(5, 0);
    vector<double> dipmSQ(ncomp, 0);
    double J2, detJ2_det, J3, detJ3_det;
    static double a0dip[5] = {0.3043504, -0.1358588, 1.4493329, 0.3556977,
                              -2.0653308};
    static double a1dip[5] = {0.9534641, -1.8396383, 2.0131180, -7.3724958,
                              8.2374135};
    static double a2dip[5] = {-1.1610080, 4.5258607, 0.9751222, -12.281038,
                              5.9397575};
    static double b0dip[5] = {0.2187939, -1.1896431, 1.1626889, 0, 0};
    static double b1dip[5] = {-0.5873164, 1.2489132, -0.5085280, 0, 0};
    static double b2dip[5] = {3.4869576, -14.915974, 15.372022, 0, 0};
    static double c0dip[5] = {-0.0646774, 0.1975882, -0.8087562, 0.6902849, 0};
    static double c1dip[5] = {-0.9520876, 2.9924258, -2.3802636, -0.2701261, 0};
    static double c2dip[5] = {-0.6260979, 1.2924686, 1.6542783, -3.4396744, 0};
    const static double conv =
        7242.702976750923;  // conversion factor, see the note below Table 2 in
                            // Gross and Vrabec 2006
    for (int i = 0; i < ncomp; i++) {
      dipmSQ[i] = pow(cppargs.dipm[i], 2.) /
                  (cppargs.m[i] * cppargs.e[i] * pow(cppargs.s[i], 3.)) * conv;
    }
    double m_ij;
    for (int i = 0; i < ncomp; i++) {
      for (int j = 0; j < ncomp; j++) {
        m_ij = sqrt(cppargs.m[i] * cppargs.m[j]);
        if (m_ij > 2) {
          m_ij = 2;
        }
        J2 = 0.;
        detJ2_det = 0.;
        for (int l = 0; l < 5; l++) {
          adip[l] = a0dip[l] + (m_ij - 1) / m_ij * a1dip[l] +
                    (m_ij - 1) / m_ij * (m_ij - 2) / m_ij * a2dip[l];
          bdip[l] = b0dip[l] + (m_ij - 1) / m_ij * b1dip[l] +
                    (m_ij - 1) / m_ij * (m_ij - 2) / m_ij * b2dip[l];
          J2 += (adip[l] + bdip[l] * e_ij[i * ncomp + j] / t) *
                pow(eta, l);  // i*ncomp+j needs to be used for e_ij because it
                              // is formatted as a 1D vector
          detJ2_det += (adip[l] + bdip[l] * e_ij[i * ncomp + j] / t) * (l + 1) *
                       pow(eta, l);
        }
        A2 += x[i] * x[j] * e_ij[i * ncomp + i] / t * e_ij[j * ncomp + j] / t *
              pow(s_ij[i * ncomp + i], 3) * pow(s_ij[j * ncomp + j], 3) /
              pow(s_ij[i * ncomp + j], 3) * cppargs.dip_num[i] *
              cppargs.dip_num[j] * dipmSQ[i] * dipmSQ[j] * J2;
        dA2_det += x[i] * x[j] * e_ij[i * ncomp + i] / t * e_ij[j * ncomp + j] /
                   t * pow(s_ij[i * ncomp + i], 3) *
                   pow(s_ij[j * ncomp + j], 3) / pow(s_ij[i * ncomp + j], 3) *
                   cppargs.dip_num[i] * cppargs.dip_num[j] * dipmSQ[i] *
                   dipmSQ[j] * detJ2_det;
      }
    }
    double m_ijk;
    for (int i = 0; i < ncomp; i++) {
      for (int j = 0; j < ncomp; j++) {
        for (int k = 0; k < ncomp; k++) {
          m_ijk = pow((cppargs.m[i] * cppargs.m[j] * cppargs.m[k]), 1 / 3.);
          if (m_ijk > 2) {
            m_ijk = 2;
          }
          J3 = 0.;
          detJ3_det = 0.;
          for (int l = 0; l < 5; l++) {
            cdip[l] = c0dip[l] + (m_ijk - 1) / m_ijk * c1dip[l] +
                      (m_ijk - 1) / m_ijk * (m_ijk - 2) / m_ijk * c2dip[l];
            J3 += cdip[l] * pow(eta, l);
            detJ3_det += cdip[l] * (l + 2) * pow(eta, (l + 1));
          }
          A3 += x[i] * x[j] * x[k] * e_ij[i * ncomp + i] / t *
                e_ij[j * ncomp + j] / t * e_ij[k * ncomp + k] / t *
                pow(s_ij[i * ncomp + i], 3) * pow(s_ij[j * ncomp + j], 3) *
                pow(s_ij[k * ncomp + k], 3) / s_ij[i * ncomp + j] /
                s_ij[i * ncomp + k] / s_ij[j * ncomp + k] * cppargs.dip_num[i] *
                cppargs.dip_num[j] * cppargs.dip_num[k] * dipmSQ[i] *
                dipmSQ[j] * dipmSQ[k] * J3;
          dA3_det += x[i] * x[j] * x[k] * e_ij[i * ncomp + i] / t *
                     e_ij[j * ncomp + j] / t * e_ij[k * ncomp + k] / t *
                     pow(s_ij[i * ncomp + i], 3) * pow(s_ij[j * ncomp + j], 3) *
                     pow(s_ij[k * ncomp + k], 3) / s_ij[i * ncomp + j] /
                     s_ij[i * ncomp + k] / s_ij[j * ncomp + k] *
                     cppargs.dip_num[i] * cppargs.dip_num[j] *
                     cppargs.dip_num[k] * dipmSQ[i] * dipmSQ[j] * dipmSQ[k] *
                     detJ3_det;
        }
      }
    }
    A2 = -PI * den * A2;
    A3 = -4 / 3. * PI * PI * den * den * A3;
    dA2_det = -PI * den / eta * dA2_det;
    dA3_det = -4 / 3. * PI * PI * den / eta * den / eta * dA3_det;
    if (A2 != 0) {  // when the mole fraction of the polar compounds is 0 then
                    // A2 = 0 and division by 0 occurs
      Zpolar = eta *
               ((dA2_det * (1 - A3 / A2) + (dA3_det * A2 - A3 * dA2_det) / A2) /
                (1 - A3 / A2) / (1 - A3 / A2));
    }
  }
  // Association term -------------------------------------------------------
  double Zassoc = 0;
  if (!cppargs.e_assoc.empty()) {
    int num_sites = 0;
    vector<int> iA;  // indices of associating compounds
    for (std::vector<int>::iterator it = cppargs.assoc_num.begin();
         it != cppargs.assoc_num.end(); ++it) {
      num_sites += *it;
      for (int i = 0; i < *it; i++) {
        iA.push_back(it - cppargs.assoc_num.begin());
      }
    }
    vector<double> x_assoc(
        num_sites);  // mole fractions of only the associating compounds
    for (int i = 0; i < num_sites; i++) {
      x_assoc[i] = x[iA[i]];
    }
    vector<double> XA(num_sites, 0);
    vector<double> delta_ij(num_sites * num_sites, 0);
    int idxa = 0;
    int idxi = 0;  // index for the ii-th compound
    int idxj = 0;  // index for the jj-th compound
    for (int i = 0; i < num_sites; i++) {
      idxi = iA[i] * ncomp + iA[i];
      for (int j = 0; j < num_sites; j++) {
        idxj = iA[j] * ncomp + iA[j];
        if (cppargs.assoc_matrix[idxa] != 0) {
          double eABij = (cppargs.e_assoc[iA[i]] + cppargs.e_assoc[iA[j]]) / 2.;
          double volABij = _HUGE;
          if (cppargs.k_hb.empty()) {
            volABij = sqrt(cppargs.vol_a[iA[i]] * cppargs.vol_a[iA[j]]) *
                      pow(sqrt(s_ij[idxi] * s_ij[idxj]) /
                              (0.5 * (s_ij[idxi] + s_ij[idxj])),
                          3);
          } else {
            volABij = sqrt(cppargs.vol_a[iA[i]] * cppargs.vol_a[iA[j]]) *
                      pow(sqrt(s_ij[idxi] * s_ij[idxj]) /
                              (0.5 * (s_ij[idxi] + s_ij[idxj])),
                          3) *
                      (1 - cppargs.k_hb[iA[i] * ncomp + iA[j]]);
          }
          delta_ij[idxa] = ghs[iA[i] * ncomp + iA[j]] * (exp(eABij / t) - 1) *
                           pow(s_ij[iA[i] * ncomp + iA[j]], 3) * volABij;
        }
        idxa += 1;
      }
      XA[i] = (-1 + sqrt(1 + 8 * den * delta_ij[i * num_sites + i])) /
              (4 * den * delta_ij[i * num_sites + i]);
      if (!std::isfinite(XA[i])) {
        XA[i] = 0.02;
      }
    }
    vector<double> ddelta_dx(num_sites * num_sites * ncomp, 0);
    int idx_ddelta = 0;
    for (int k = 0; k < ncomp; k++) {
      int idxi = 0;  // index for the ii-th compound
      int idxj = 0;  // index for the jj-th compound
      idxa = 0;
      for (int i = 0; i < num_sites; i++) {
        idxi = iA[i] * ncomp + iA[i];
        for (int j = 0; j < num_sites; j++) {
          idxj = iA[j] * ncomp + iA[j];
          if (cppargs.assoc_matrix[idxa] != 0) {
            double eABij =
                (cppargs.e_assoc[iA[i]] + cppargs.e_assoc[iA[j]]) / 2.;
            double volABij = _HUGE;
            if (cppargs.k_hb.empty()) {
              volABij = sqrt(cppargs.vol_a[iA[i]] * cppargs.vol_a[iA[j]]) *
                        pow(sqrt(s_ij[idxi] * s_ij[idxj]) /
                                (0.5 * (s_ij[idxi] + s_ij[idxj])),
                            3);
            } else {
              volABij = sqrt(cppargs.vol_a[iA[i]] * cppargs.vol_a[iA[j]]) *
                        pow(sqrt(s_ij[idxi] * s_ij[idxj]) /
                                (0.5 * (s_ij[idxi] + s_ij[idxj])),
                            3) *
                        (1 - cppargs.k_hb[iA[i] * ncomp + iA[j]]);
            }
            double dghsd_dx =
                PI / 6. * cppargs.m[k] *
                (pow(d[k], 3) / (1 - zeta[3]) / (1 - zeta[3]) +
                 3 * d[iA[i]] * d[iA[j]] / (d[iA[i]] + d[iA[j]]) *
                     (d[k] * d[k] / (1 - zeta[3]) / (1 - zeta[3]) +
                      2 * pow(d[k], 3) * zeta[2] / pow(1 - zeta[3], 3)) +
                 2 * pow((d[iA[i]] * d[iA[j]] / (d[iA[i]] + d[iA[j]])), 2) *
                     (2 * d[k] * d[k] * zeta[2] / pow(1 - zeta[3], 3) +
                      3 * (pow(d[k], 3) * zeta[2] * zeta[2] /
                           pow(1 - zeta[3], 4))));
            ddelta_dx[idx_ddelta] = dghsd_dx * (exp(eABij / t) - 1) *
                                    pow(s_ij[iA[i] * ncomp + iA[j]], 3) *
                                    volABij;
          }
          idx_ddelta += 1;
          idxa += 1;
        }
      }
    }
    int ctr = 0;
    double dif = 1000.;
    vector<double> XA_old = XA;
    while ((ctr < 100) && (dif > 1e-15)) {
      ctr += 1;
      XA = XA_find(XA_old, delta_ij, den, x_assoc);
      dif = 0.;
      for (int i = 0; i < num_sites; i++) {
        dif += std::abs(XA[i] - XA_old[i]);
      }
      for (int i = 0; i < num_sites; i++) {
        XA_old[i] = (XA[i] + XA_old[i]) / 2.0;
      }
    }
    vector<double> dXA_dx(num_sites * ncomp, 0);
    dXA_dx =
        dXAdx_find(cppargs.assoc_num, delta_ij, den, XA, ddelta_dx, x_assoc);
    summ = 0.;
    int ij = 0;
    for (int i = 0; i < ncomp; i++) {
      for (int j = 0; j < num_sites; j++) {
        summ += x[i] * den * x[iA[j]] * (1 / XA[j] - 0.5) * dXA_dx[ij];
        ij += 1;
      }
    }
    Zassoc = summ;
  }
  // Ion term ---------------------------------------------------------------
  double Zion = 0;
  if (!cppargs.z.empty()) {
    vector<double> q(cppargs.z.begin(), cppargs.z.end());
    for (int i = 0; i < ncomp; i++) {
      q[i] = q[i] * E_CHRG;
    }
    summ = 0.;
    for (int i = 0; i < ncomp; i++) {
      summ += cppargs.z[i] * cppargs.z[i] * x[i];
    }
    double kappa =
        sqrt(den * E_CHRG * E_CHRG / kb / t / (cppargs.dielc * perm_vac) *
             summ);  // the inverse Debye screening length. Equation 4 in Held
                     // et al. 2008.
    if (kappa != 0) {
      double chi, sigma_k;
      summ = 0.;
      for (int i = 0; i < ncomp; i++) {
        chi = 3 / pow(kappa * cppargs.s[i], 3) *
              (1.5 + log(1 + kappa * cppargs.s[i]) -
               2 * (1 + kappa * cppargs.s[i]) +
               0.5 * pow(1 + kappa * cppargs.s[i], 2));
        sigma_k = -2 * chi + 3 / (1 + kappa * cppargs.s[i]);
        summ += q[i] * q[i] * x[i] * sigma_k;
      }
      Zion = -1 * kappa / 24. / PI / kb / t / (cppargs.dielc * perm_vac) * summ;
    }
  }
  double Z = Zid + Zhc + Zdisp + Zpolar + Zassoc + Zion;
  return Z;
}
vector<double> pcsaft_lnfug_cpp(double t, double rho, vector<double> x,
                                add_args &cppargs) {
  /**
  Calculate the natural logarithm of the fugacity coefficients for one phase of
  the system.
  */
  int ncomp = x.size();  // number of components
  vector<double> d(ncomp);
  for (int i = 0; i < ncomp; i++) {
    d[i] = cppargs.s[i] * (1 - 0.12 * exp(-3 * cppargs.e[i] / t));
  }
  if (!cppargs.z.empty()) {
    for (int i = 0; i < ncomp; i++) {
      if (cppargs.z[i] != 0) {
        d[i] = cppargs.s[i] *
               (1 - 0.12);  // for ions the diameter is assumed to be
                            // temperature independent (see Held et al. 2014)
      }
    }
  }
  double den = rho * N_AV / 1.0e30;
  vector<double> zeta(4, 0);
  double summ;
  for (int i = 0; i < 4; i++) {
    summ = 0;
    for (int j = 0; j < ncomp; j++) {
      summ += x[j] * cppargs.m[j] * pow(d[j], i);
    }
    zeta[i] = PI / 6 * den * summ;
  }
  double eta = zeta[3];
  double m_avg = 0;
  for (int i = 0; i < ncomp; i++) {
    m_avg += x[i] * cppargs.m[i];
  }
  vector<double> ghs(ncomp * ncomp, 0);
  vector<double> denghs(ncomp * ncomp, 0);
  vector<double> e_ij(ncomp * ncomp, 0);
  vector<double> s_ij(ncomp * ncomp, 0);
  double m2es3 = 0.;
  double m2e2s3 = 0.;
  int idx = -1;
  for (int i = 0; i < ncomp; i++) {
    for (int j = 0; j < ncomp; j++) {
      idx += 1;
      if (cppargs.l_ij.empty()) {
        s_ij[idx] = (cppargs.s[i] + cppargs.s[j]) / 2.;
      } else {
        s_ij[idx] =
            (cppargs.s[i] + cppargs.s[j]) / 2. * (1 - cppargs.l_ij[idx]);
      }
      if (!cppargs.z.empty()) {
        if (cppargs.z[i] * cppargs.z[j] <=
            0) {  // for two cations or two anions e_ij is kept at zero to avoid
                  // dispersion between like ions (see Held et al. 2014)
          if (cppargs.k_ij.empty()) {
            e_ij[idx] = sqrt(cppargs.e[i] * cppargs.e[j]);
          } else {
            e_ij[idx] =
                sqrt(cppargs.e[i] * cppargs.e[j]) * (1 - cppargs.k_ij[idx]);
          }
        }
      } else {
        if (cppargs.k_ij.empty()) {
          e_ij[idx] = sqrt(cppargs.e[i] * cppargs.e[j]);
        } else {
          e_ij[idx] =
              sqrt(cppargs.e[i] * cppargs.e[j]) * (1 - cppargs.k_ij[idx]);
        }
      }
      m2es3 = m2es3 + x[i] * x[j] * cppargs.m[i] * cppargs.m[j] * e_ij[idx] /
                          t * pow(s_ij[idx], 3);
      m2e2s3 = m2e2s3 + x[i] * x[j] * cppargs.m[i] * cppargs.m[j] *
                            pow(e_ij[idx] / t, 2) * pow(s_ij[idx], 3);
      ghs[idx] = 1 / (1 - zeta[3]) +
                 (d[i] * d[j] / (d[i] + d[j])) * 3 * zeta[2] / (1 - zeta[3]) /
                     (1 - zeta[3]) +
                 pow(d[i] * d[j] / (d[i] + d[j]), 2) * 2 * zeta[2] * zeta[2] /
                     pow(1 - zeta[3], 3);
      denghs[idx] = zeta[3] / (1 - zeta[3]) / (1 - zeta[3]) +
                    (d[i] * d[j] / (d[i] + d[j])) *
                        (3 * zeta[2] / (1 - zeta[3]) / (1 - zeta[3]) +
                         6 * zeta[2] * zeta[3] / pow(1 - zeta[3], 3)) +
                    pow(d[i] * d[j] / (d[i] + d[j]), 2) *
                        (4 * zeta[2] * zeta[2] / pow(1 - zeta[3], 3) +
                         6 * zeta[2] * zeta[2] * zeta[3] / pow(1 - zeta[3], 4));
    }
  }
  double ares_hs =
      1 / zeta[0] *
      (3 * zeta[1] * zeta[2] / (1 - zeta[3]) +
       pow(zeta[2], 3.) / (zeta[3] * pow(1 - zeta[3], 2)) +
       (pow(zeta[2], 3.) / pow(zeta[3], 2.) - zeta[0]) * log(1 - zeta[3]));
  double Zhs =
      zeta[3] / (1 - zeta[3]) +
      3. * zeta[1] * zeta[2] / zeta[0] / (1. - zeta[3]) / (1. - zeta[3]) +
      (3. * pow(zeta[2], 3.) - zeta[3] * pow(zeta[2], 3.)) / zeta[0] /
          pow(1. - zeta[3], 3.);
  static double a0[7] = {0.9105631445,  0.6361281449, 2.6861347891,
                         -26.547362491, 97.759208784, -159.59154087,
                         91.297774084};
  static double a1[7] = {-0.3084016918, 0.1860531159,  -2.5030047259,
                         21.419793629,  -65.255885330, 83.318680481,
                         -33.746922930};
  static double a2[7] = {-0.0906148351, 0.4527842806,  0.5962700728,
                         -1.7241829131, -4.1302112531, 13.776631870,
                         -8.6728470368};
  static double b0[7] = {0.7240946941,  2.2382791861, -4.0025849485,
                         -21.003576815, 26.855641363, 206.55133841,
                         -355.60235612};
  static double b1[7] = {-0.5755498075, 0.6995095521, 3.8925673390,
                         -17.215471648, 192.67226447, -161.82646165,
                         -165.20769346};
  static double b2[7] = {0.0976883116, -0.2557574982, -9.1558561530,
                         20.642075974, -38.804430052, 93.626774077,
                         -29.666905585};
  vector<double> a(7, 0);
  vector<double> b(7, 0);
  for (int i = 0; i < 7; i++) {
    a[i] = a0[i] + (m_avg - 1.) / m_avg * a1[i] +
           (m_avg - 1.) / m_avg * (m_avg - 2.) / m_avg * a2[i];
    b[i] = b0[i] + (m_avg - 1.) / m_avg * b1[i] +
           (m_avg - 1.) / m_avg * (m_avg - 2.) / m_avg * b2[i];
  }
  double detI1_det = 0.0;
  double detI2_det = 0.0;
  double I1 = 0.0;
  double I2 = 0.0;
  for (int i = 0; i < 7; i++) {
    detI1_det += a[i] * (i + 1) * pow(eta, i);
    detI2_det += b[i] * (i + 1) * pow(eta, i);
    I2 += b[i] * pow(eta, i);
    I1 += a[i] * pow(eta, i);
  }
  double C1 =
      1. /
      (1. + m_avg * (8 * eta - 2 * eta * eta) / pow(1 - eta, 4) +
       (1 - m_avg) *
           (20 * eta - 27 * eta * eta + 12 * pow(eta, 3) - 2 * pow(eta, 4)) /
           pow((1 - eta) * (2 - eta), 2.0));
  double C2 =
      -1. * C1 * C1 *
      (m_avg * (-4 * eta * eta + 20 * eta + 8) / pow(1 - eta, 5) +
       (1 - m_avg) * (2 * pow(eta, 3) + 12 * eta * eta - 48 * eta + 40) /
           pow((1 - eta) * (2 - eta), 3.0));
  summ = 0.0;
  for (int i = 0; i < ncomp; i++) {
    summ += x[i] * (cppargs.m[i] - 1) * log(ghs[i * ncomp + i]);
  }
  double ares_hc = m_avg * ares_hs - summ;
  double ares_disp =
      -2 * PI * den * I1 * m2es3 - PI * den * m_avg * C1 * I2 * m2e2s3;
  summ = 0.0;
  for (int i = 0; i < ncomp; i++) {
    summ +=
        x[i] * (cppargs.m[i] - 1) / ghs[i * ncomp + i] * denghs[i * ncomp + i];
  }
  double Zhc = m_avg * Zhs - summ;
  double Zdisp = -2 * PI * den * detI1_det * m2es3 -
                 PI * den * m_avg * (C1 * detI2_det + C2 * eta * I2) * m2e2s3;
  vector<double> dghsii_dx(ncomp * ncomp, 0);
  vector<double> dahs_dx(ncomp, 0);
  vector<double> dzeta_dx(4, 0);
  idx = -1;
  for (int i = 0; i < ncomp; i++) {
    for (int l = 0; l < 4; l++) {
      dzeta_dx[l] = PI / 6. * den * cppargs.m[i] * pow(d[i], l);
    }
    for (int j = 0; j < ncomp; j++) {
      idx += 1;
      dghsii_dx[idx] =
          dzeta_dx[3] / (1 - zeta[3]) / (1 - zeta[3]) +
          (d[j] * d[j] / (d[j] + d[j])) *
              (3 * dzeta_dx[2] / (1 - zeta[3]) / (1 - zeta[3]) +
               6 * zeta[2] * dzeta_dx[3] / pow(1 - zeta[3], 3)) +
          pow(d[j] * d[j] / (d[j] + d[j]), 2) *
              (4 * zeta[2] * dzeta_dx[2] / pow(1 - zeta[3], 3) +
               6 * zeta[2] * zeta[2] * dzeta_dx[3] / pow(1 - zeta[3], 4));
    }
    dahs_dx[i] = -dzeta_dx[0] / zeta[0] * ares_hs +
                 1 / zeta[0] *
                     (3 * (dzeta_dx[1] * zeta[2] + zeta[1] * dzeta_dx[2]) /
                          (1 - zeta[3]) +
                      3 * zeta[1] * zeta[2] * dzeta_dx[3] / (1 - zeta[3]) /
                          (1 - zeta[3]) +
                      3 * zeta[2] * zeta[2] * dzeta_dx[2] / zeta[3] /
                          (1 - zeta[3]) / (1 - zeta[3]) +
                      pow(zeta[2], 3) * dzeta_dx[3] * (3 * zeta[3] - 1) /
                          zeta[3] / zeta[3] / pow(1 - zeta[3], 3) +
                      log(1 - zeta[3]) *
                          ((3 * zeta[2] * zeta[2] * dzeta_dx[2] * zeta[3] -
                            2 * pow(zeta[2], 3) * dzeta_dx[3]) /
                               pow(zeta[3], 3) -
                           dzeta_dx[0]) +
                      (zeta[0] - pow(zeta[2], 3) / zeta[3] / zeta[3]) *
                          dzeta_dx[3] / (1 - zeta[3]));
  }
  vector<double> dadisp_dx(ncomp, 0);
  vector<double> dahc_dx(ncomp, 0);
  double dzeta3_dx, daa_dx, db_dx, dI1_dx, dI2_dx, dm2es3_dx, dm2e2s3_dx,
      dC1_dx;
  for (int i = 0; i < ncomp; i++) {
    dzeta3_dx = PI / 6. * den * cppargs.m[i] * pow(d[i], 3);
    dI1_dx = 0.0;
    dI2_dx = 0.0;
    dm2es3_dx = 0.0;
    dm2e2s3_dx = 0.0;
    for (int l = 0; l < 7; l++) {
      daa_dx = cppargs.m[i] / m_avg / m_avg * a1[l] +
               cppargs.m[i] / m_avg / m_avg * (3 - 4 / m_avg) * a2[l];
      db_dx = cppargs.m[i] / m_avg / m_avg * b1[l] +
              cppargs.m[i] / m_avg / m_avg * (3 - 4 / m_avg) * b2[l];
      dI1_dx += a[l] * l * dzeta3_dx * pow(eta, l - 1) + daa_dx * pow(eta, l);
      dI2_dx += b[l] * l * dzeta3_dx * pow(eta, l - 1) + db_dx * pow(eta, l);
    }
    for (int j = 0; j < ncomp; j++) {
      dm2es3_dx += x[j] * cppargs.m[j] * (e_ij[i * ncomp + j] / t) *
                   pow(s_ij[i * ncomp + j], 3);
      dm2e2s3_dx += x[j] * cppargs.m[j] * pow(e_ij[i * ncomp + j] / t, 2) *
                    pow(s_ij[i * ncomp + j], 3);
      dahc_dx[i] += x[j] * (cppargs.m[j] - 1) / ghs[j * ncomp + j] *
                    dghsii_dx[i * ncomp + j];
    }
    dm2es3_dx = dm2es3_dx * 2 * cppargs.m[i];
    dm2e2s3_dx = dm2e2s3_dx * 2 * cppargs.m[i];
    dahc_dx[i] = cppargs.m[i] * ares_hs + m_avg * dahs_dx[i] - dahc_dx[i] -
                 (cppargs.m[i] - 1) * log(ghs[i * ncomp + i]);
    dC1_dx = C2 * dzeta3_dx -
             C1 * C1 *
                 (cppargs.m[i] * (8 * eta - 2 * eta * eta) / pow(1 - eta, 4) -
                  cppargs.m[i] *
                      (20 * eta - 27 * eta * eta + 12 * pow(eta, 3) -
                       2 * pow(eta, 4)) /
                      pow((1 - eta) * (2 - eta), 2));
    dadisp_dx[i] = -2 * PI * den * (dI1_dx * m2es3 + I1 * dm2es3_dx) -
                   PI * den *
                       ((cppargs.m[i] * C1 * I2 + m_avg * dC1_dx * I2 +
                         m_avg * C1 * dI2_dx) *
                            m2e2s3 +
                        m_avg * C1 * I2 * dm2e2s3_dx);
  }
  vector<double> mu_hc(ncomp, 0);
  vector<double> mu_disp(ncomp, 0);
  for (int i = 0; i < ncomp; i++) {
    for (int j = 0; j < ncomp; j++) {
      mu_hc[i] += x[j] * dahc_dx[j];
      mu_disp[i] += x[j] * dadisp_dx[j];
    }
    mu_hc[i] = ares_hc + Zhc + dahc_dx[i] - mu_hc[i];
    mu_disp[i] = ares_disp + Zdisp + dadisp_dx[i] - mu_disp[i];
  }
  // Dipole term (Gross and Vrabec term) --------------------------------------
  vector<double> mu_polar(ncomp, 0);
  if (!cppargs.dipm.empty()) {
    double A2 = 0.;
    double A3 = 0.;
    double dA2_det = 0.;
    double dA3_det = 0.;
    vector<double> dA2_dx(ncomp, 0);
    vector<double> dA3_dx(ncomp, 0);
    static double a0dip[5] = {0.3043504, -0.1358588, 1.4493329, 0.3556977,
                              -2.0653308};
    static double a1dip[5] = {0.9534641, -1.8396383, 2.0131180, -7.3724958,
                              8.2374135};
    static double a2dip[5] = {-1.1610080, 4.5258607, 0.9751222, -12.281038,
                              5.9397575};
    static double b0dip[5] = {0.2187939, -1.1896431, 1.1626889, 0, 0};
    static double b1dip[5] = {-0.5873164, 1.2489132, -0.5085280, 0, 0};
    static double b2dip[5] = {3.4869576, -14.915974, 15.372022, 0, 0};
    static double c0dip[5] = {-0.0646774, 0.1975882, -0.8087562, 0.6902849, 0};
    static double c1dip[5] = {-0.9520876, 2.9924258, -2.3802636, -0.2701261, 0};
    static double c2dip[5] = {-0.6260979, 1.2924686, 1.6542783, -3.4396744, 0};
    const static double conv =
        7242.702976750923;  // conversion factor, see the note below Table 2 in
                            // Gross and Vrabec 2006
    vector<double> dipmSQ(ncomp, 0);
    for (int i = 0; i < ncomp; i++) {
      dipmSQ[i] = pow(cppargs.dipm[i], 2.) /
                  (cppargs.m[i] * cppargs.e[i] * pow(cppargs.s[i], 3.)) * conv;
    }
    vector<double> adip(5, 0);
    vector<double> bdip(5, 0);
    vector<double> cdip(5, 0);
    double J2, dJ2_det, detJ2_det, J3, dJ3_det, detJ3_det;
    double m_ij;
    double m_ijk;
    for (int i = 0; i < ncomp; i++) {
      for (int j = 0; j < ncomp; j++) {
        m_ij = sqrt(cppargs.m[i] * cppargs.m[j]);
        if (m_ij > 2) {
          m_ij = 2;
        }
        J2 = 0.;
        dJ2_det = 0.;
        detJ2_det = 0;
        for (int l = 0; l < 5; l++) {
          adip[l] = a0dip[l] + (m_ij - 1) / m_ij * a1dip[l] +
                    (m_ij - 1) / m_ij * (m_ij - 2) / m_ij * a2dip[l];
          bdip[l] = b0dip[l] + (m_ij - 1) / m_ij * b1dip[l] +
                    (m_ij - 1) / m_ij * (m_ij - 2) / m_ij * b2dip[l];
          J2 += (adip[l] + bdip[l] * e_ij[i * ncomp + j] / t) *
                pow(eta, l);  // i*ncomp+j needs to be used for e_ij because it
                              // is formatted as a 1D vector
          dJ2_det += (adip[l] + bdip[l] * e_ij[i * ncomp + j] / t) * l *
                     pow(eta, l - 1);
          detJ2_det += (adip[l] + bdip[l] * e_ij[i * ncomp + j] / t) * (l + 1) *
                       pow(eta, l);
        }
        A2 += x[i] * x[j] * e_ij[i * ncomp + i] / t * e_ij[j * ncomp + j] / t *
              pow(s_ij[i * ncomp + i], 3) * pow(s_ij[j * ncomp + j], 3) /
              pow(s_ij[i * ncomp + j], 3) * cppargs.dip_num[i] *
              cppargs.dip_num[j] * dipmSQ[i] * dipmSQ[j] * J2;
        dA2_det += x[i] * x[j] * e_ij[i * ncomp + i] / t * e_ij[j * ncomp + j] /
                   t * pow(s_ij[i * ncomp + i], 3) *
                   pow(s_ij[j * ncomp + j], 3) / pow(s_ij[i * ncomp + j], 3) *
                   cppargs.dip_num[i] * cppargs.dip_num[j] * dipmSQ[i] *
                   dipmSQ[j] * detJ2_det;
        if (i == j) {
          dA2_dx[i] += e_ij[i * ncomp + i] / t * e_ij[j * ncomp + j] / t *
                       pow(s_ij[i * ncomp + i], 3) *
                       pow(s_ij[j * ncomp + j], 3) /
                       pow(s_ij[i * ncomp + j], 3) * cppargs.dip_num[i] *
                       cppargs.dip_num[j] * dipmSQ[i] * dipmSQ[j] *
                       (x[i] * x[j] * dJ2_det * PI / 6. * den * cppargs.m[i] *
                            pow(d[i], 3) +
                        2 * x[j] * J2);
        } else {
          dA2_dx[i] += e_ij[i * ncomp + i] / t * e_ij[j * ncomp + j] / t *
                       pow(s_ij[i * ncomp + i], 3) *
                       pow(s_ij[j * ncomp + j], 3) /
                       pow(s_ij[i * ncomp + j], 3) * cppargs.dip_num[i] *
                       cppargs.dip_num[j] * dipmSQ[i] * dipmSQ[j] *
                       (x[i] * x[j] * dJ2_det * PI / 6. * den * cppargs.m[i] *
                            pow(d[i], 3) +
                        x[j] * J2);
        }
        for (int k = 0; k < ncomp; k++) {
          m_ijk = pow((cppargs.m[i] * cppargs.m[j] * cppargs.m[k]), 1 / 3.);
          if (m_ijk > 2) {
            m_ijk = 2;
          }
          J3 = 0.;
          dJ3_det = 0.;
          detJ3_det = 0.;
          for (int l = 0; l < 5; l++) {
            cdip[l] = c0dip[l] + (m_ijk - 1) / m_ijk * c1dip[l] +
                      (m_ijk - 1) / m_ijk * (m_ijk - 2) / m_ijk * c2dip[l];
            J3 += cdip[l] * pow(eta, l);
            dJ3_det += cdip[l] * l * pow(eta, (l - 1));
            detJ3_det += cdip[l] * (l + 2) * pow(eta, (l + 1));
          }
          A3 += x[i] * x[j] * x[k] * e_ij[i * ncomp + i] / t *
                e_ij[j * ncomp + j] / t * e_ij[k * ncomp + k] / t *
                pow(s_ij[i * ncomp + i], 3) * pow(s_ij[j * ncomp + j], 3) *
                pow(s_ij[k * ncomp + k], 3) / s_ij[i * ncomp + j] /
                s_ij[i * ncomp + k] / s_ij[j * ncomp + k] * cppargs.dip_num[i] *
                cppargs.dip_num[j] * cppargs.dip_num[k] * dipmSQ[i] *
                dipmSQ[j] * dipmSQ[k] * J3;
          dA3_det += x[i] * x[j] * x[k] * e_ij[i * ncomp + i] / t *
                     e_ij[j * ncomp + j] / t * e_ij[k * ncomp + k] / t *
                     pow(s_ij[i * ncomp + i], 3) * pow(s_ij[j * ncomp + j], 3) *
                     pow(s_ij[k * ncomp + k], 3) / s_ij[i * ncomp + j] /
                     s_ij[i * ncomp + k] / s_ij[j * ncomp + k] *
                     cppargs.dip_num[i] * cppargs.dip_num[j] *
                     cppargs.dip_num[k] * dipmSQ[i] * dipmSQ[j] * dipmSQ[k] *
                     detJ3_det;
          if ((i == j) && (i == k)) {
            dA3_dx[i] +=
                e_ij[i * ncomp + i] / t * e_ij[j * ncomp + j] / t *
                e_ij[k * ncomp + k] / t * pow(s_ij[i * ncomp + i], 3) *
                pow(s_ij[j * ncomp + j], 3) * pow(s_ij[k * ncomp + k], 3) /
                s_ij[i * ncomp + j] / s_ij[i * ncomp + k] /
                s_ij[j * ncomp + k] * cppargs.dip_num[i] * cppargs.dip_num[j] *
                cppargs.dip_num[k] * dipmSQ[i] * dipmSQ[j] * dipmSQ[k] *
                (x[i] * x[j] * x[k] * dJ3_det * PI / 6. * den * cppargs.m[i] *
                     pow(d[i], 3) +
                 3 * x[j] * x[k] * J3);
          } else if ((i == j) || (i == k)) {
            dA3_dx[i] +=
                e_ij[i * ncomp + i] / t * e_ij[j * ncomp + j] / t *
                e_ij[k * ncomp + k] / t * pow(s_ij[i * ncomp + i], 3) *
                pow(s_ij[j * ncomp + j], 3) * pow(s_ij[k * ncomp + k], 3) /
                s_ij[i * ncomp + j] / s_ij[i * ncomp + k] /
                s_ij[j * ncomp + k] * cppargs.dip_num[i] * cppargs.dip_num[j] *
                cppargs.dip_num[k] * dipmSQ[i] * dipmSQ[j] * dipmSQ[k] *
                (x[i] * x[j] * x[k] * dJ3_det * PI / 6. * den * cppargs.m[i] *
                     pow(d[i], 3) +
                 2 * x[j] * x[k] * J3);
          } else {
            dA3_dx[i] +=
                e_ij[i * ncomp + i] / t * e_ij[j * ncomp + j] / t *
                e_ij[k * ncomp + k] / t * pow(s_ij[i * ncomp + i], 3) *
                pow(s_ij[j * ncomp + j], 3) * pow(s_ij[k * ncomp + k], 3) /
                s_ij[i * ncomp + j] / s_ij[i * ncomp + k] /
                s_ij[j * ncomp + k] * cppargs.dip_num[i] * cppargs.dip_num[j] *
                cppargs.dip_num[k] * dipmSQ[i] * dipmSQ[j] * dipmSQ[k] *
                (x[i] * x[j] * x[k] * dJ3_det * PI / 6. * den * cppargs.m[i] *
                     pow(d[i], 3) +
                 x[j] * x[k] * J3);
          }
        }
      }
    }
    A2 = -PI * den * A2;
    A3 = -4 / 3. * PI * PI * den * den * A3;
    dA2_det = -PI * den / eta * dA2_det;
    dA3_det = -4 / 3. * PI * PI * den / eta * den / eta * dA3_det;
    for (int i = 0; i < ncomp; i++) {
      dA2_dx[i] = -PI * den * dA2_dx[i];
      dA3_dx[i] = -4 / 3. * PI * PI * den * den * dA3_dx[i];
    }
    vector<double> dapolar_dx(ncomp);
    for (int i = 0; i < ncomp; i++) {
      dapolar_dx[i] =
          (dA2_dx[i] * (1 - A3 / A2) + (dA3_dx[i] * A2 - A3 * dA2_dx[i]) / A2) /
          pow(1 - A3 / A2, 2);
    }
    if (A2 != 0) {  // when the mole fraction of the polar compounds is 0 then
                    // A2 = 0 and division by 0 occurs
      double ares_polar = A2 / (1 - A3 / A2);
      double Zpolar =
          eta *
          ((dA2_det * (1 - A3 / A2) + (dA3_det * A2 - A3 * dA2_det) / A2) /
           (1 - A3 / A2) / (1 - A3 / A2));
      for (int i = 0; i < ncomp; i++) {
        for (int j = 0; j < ncomp; j++) {
          mu_polar[i] += x[j] * dapolar_dx[j];
        }
        mu_polar[i] = ares_polar + Zpolar + dapolar_dx[i] - mu_polar[i];
      }
    }
  }
  // Association term -------------------------------------------------------
  vector<double> mu_assoc(ncomp, 0);
  if (!cppargs.e_assoc.empty()) {
    int num_sites = 0;
    vector<int> iA;  // indices of associating compounds
    for (std::vector<int>::iterator it = cppargs.assoc_num.begin();
         it != cppargs.assoc_num.end(); ++it) {
      num_sites += *it;
      for (int i = 0; i < *it; i++) {
        iA.push_back(it - cppargs.assoc_num.begin());
      }
    }
    vector<double> x_assoc(
        num_sites);  // mole fractions of only the associating compounds
    for (int i = 0; i < num_sites; i++) {
      x_assoc[i] = x[iA[i]];
    }
    vector<double> XA(num_sites, 0);
    vector<double> delta_ij(num_sites * num_sites, 0);
    int idxa = 0;
    int idxi = 0;  // index for the ii-th compound
    int idxj = 0;  // index for the jj-th compound
    for (int i = 0; i < num_sites; i++) {
      idxi = iA[i] * ncomp + iA[i];
      for (int j = 0; j < num_sites; j++) {
        idxj = iA[j] * ncomp + iA[j];
        if (cppargs.assoc_matrix[idxa] != 0) {
          double eABij = (cppargs.e_assoc[iA[i]] + cppargs.e_assoc[iA[j]]) / 2.;
          double volABij = _HUGE;
          if (cppargs.k_hb.empty()) {
            volABij = sqrt(cppargs.vol_a[iA[i]] * cppargs.vol_a[iA[j]]) *
                      pow(sqrt(s_ij[idxi] * s_ij[idxj]) /
                              (0.5 * (s_ij[idxi] + s_ij[idxj])),
                          3);
          } else {
            volABij = sqrt(cppargs.vol_a[iA[i]] * cppargs.vol_a[iA[j]]) *
                      pow(sqrt(s_ij[idxi] * s_ij[idxj]) /
                              (0.5 * (s_ij[idxi] + s_ij[idxj])),
                          3) *
                      (1 - cppargs.k_hb[iA[i] * ncomp + iA[j]]);
          }
          delta_ij[idxa] = ghs[iA[i] * ncomp + iA[j]] * (exp(eABij / t) - 1) *
                           pow(s_ij[iA[i] * ncomp + iA[j]], 3) * volABij;
        }
        idxa += 1;
      }
      XA[i] = (-1 + sqrt(1 + 8 * den * delta_ij[i * num_sites + i])) /
              (4 * den * delta_ij[i * num_sites + i]);
      if (!std::isfinite(XA[i])) {
        XA[i] = 0.02;
      }
    }
    vector<double> ddelta_dx(num_sites * num_sites * ncomp, 0);
    int idx_ddelta = 0;
    for (int k = 0; k < ncomp; k++) {
      int idxi = 0;  // index for the ii-th compound
      int idxj = 0;  // index for the jj-th compound
      idxa = 0;
      for (int i = 0; i < num_sites; i++) {
        idxi = iA[i] * ncomp + iA[i];
        for (int j = 0; j < num_sites; j++) {
          idxj = iA[j] * ncomp + iA[j];
          if (cppargs.assoc_matrix[idxa] != 0) {
            double eABij =
                (cppargs.e_assoc[iA[i]] + cppargs.e_assoc[iA[j]]) / 2.;
            double volABij = _HUGE;
            if (cppargs.k_hb.empty()) {
              volABij = sqrt(cppargs.vol_a[iA[i]] * cppargs.vol_a[iA[j]]) *
                        pow(sqrt(s_ij[idxi] * s_ij[idxj]) /
                                (0.5 * (s_ij[idxi] + s_ij[idxj])),
                            3);
            } else {
              volABij = sqrt(cppargs.vol_a[iA[i]] * cppargs.vol_a[iA[j]]) *
                        pow(sqrt(s_ij[idxi] * s_ij[idxj]) /
                                (0.5 * (s_ij[idxi] + s_ij[idxj])),
                            3) *
                        (1 - cppargs.k_hb[iA[i] * ncomp + iA[j]]);
            }
            double dghsd_dx =
                PI / 6. * cppargs.m[k] *
                (pow(d[k], 3) / (1 - zeta[3]) / (1 - zeta[3]) +
                 3 * d[iA[i]] * d[iA[j]] / (d[iA[i]] + d[iA[j]]) *
                     (d[k] * d[k] / (1 - zeta[3]) / (1 - zeta[3]) +
                      2 * pow(d[k], 3) * zeta[2] / pow(1 - zeta[3], 3)) +
                 2 * pow((d[iA[i]] * d[iA[j]] / (d[iA[i]] + d[iA[j]])), 2) *
                     (2 * d[k] * d[k] * zeta[2] / pow(1 - zeta[3], 3) +
                      3 * (pow(d[k], 3) * zeta[2] * zeta[2] /
                           pow(1 - zeta[3], 4))));
            ddelta_dx[idx_ddelta] = dghsd_dx * (exp(eABij / t) - 1) *
                                    pow(s_ij[iA[i] * ncomp + iA[j]], 3) *
                                    volABij;
          }
          idx_ddelta += 1;
          idxa += 1;
        }
      }
    }
    int ctr = 0;
    double dif = 1000.;
    vector<double> XA_old = XA;
    while ((ctr < 100) && (dif > 1e-15)) {
      ctr += 1;
      XA = XA_find(XA_old, delta_ij, den, x_assoc);
      dif = 0.;
      for (int i = 0; i < num_sites; i++) {
        dif += std::abs(XA[i] - XA_old[i]);
      }
      for (int i = 0; i < num_sites; i++) {
        XA_old[i] = (XA[i] + XA_old[i]) / 2.0;
      }
    }
    vector<double> dXA_dx(num_sites * ncomp, 0);
    dXA_dx =
        dXAdx_find(cppargs.assoc_num, delta_ij, den, XA, ddelta_dx, x_assoc);
    int ij = 0;
    for (int i = 0; i < ncomp; i++) {
      for (int j = 0; j < num_sites; j++) {
        mu_assoc[i] += x[iA[j]] * den * dXA_dx[ij] * (1 / XA[j] - 0.5);
        ij += 1;
      }
    }
    for (int i = 0; i < num_sites; i++) {
      mu_assoc[iA[i]] += log(XA[i]) - 0.5 * XA[i] + 0.5;
    }
  }
  // Ion term ---------------------------------------------------------------
  vector<double> mu_ion(ncomp, 0);
  if (!cppargs.z.empty()) {
    vector<double> q(cppargs.z.begin(), cppargs.z.end());
    for (int i = 0; i < ncomp; i++) {
      q[i] = q[i] * E_CHRG;
    }
    summ = 0.;
    for (int i = 0; i < ncomp; i++) {
      summ += cppargs.z[i] * cppargs.z[i] * x[i];
    }
    double kappa =
        sqrt(den * E_CHRG * E_CHRG / kb / t / (cppargs.dielc * perm_vac) *
             summ);  // the inverse Debye screening length. Equation 4 in Held
                     // et al. 2008.
    if (kappa != 0) {
      vector<double> chi(ncomp);
      vector<double> sigma_k(ncomp);
      double summ1 = 0.;
      double summ2 = 0.;
      for (int i = 0; i < ncomp; i++) {
        chi[i] = 3 / pow(kappa * cppargs.s[i], 3) *
                 (1.5 + log(1 + kappa * cppargs.s[i]) -
                  2 * (1 + kappa * cppargs.s[i]) +
                  0.5 * pow(1 + kappa * cppargs.s[i], 2));
        sigma_k[i] = -2 * chi[i] + 3 / (1 + kappa * cppargs.s[i]);
        summ1 += q[i] * q[i] * x[i] * sigma_k[i];
        summ2 += x[i] * q[i] * q[i];
      }
      for (int i = 0; i < ncomp; i++) {
        mu_ion[i] = -q[i] * q[i] * kappa / 24. / PI / kb / t /
                    (cppargs.dielc * perm_vac) * (2 * chi[i] + summ1 / summ2);
      }
    }
  }
  double Z = pcsaft_Z_cpp(t, rho, x, cppargs);
  vector<double> mu(ncomp, 0);
  vector<double> lnfugcoef(ncomp, 0);
  for (int i = 0; i < ncomp; i++) {
    mu[i] = mu_hc[i] + mu_disp[i] + mu_polar[i] + mu_assoc[i] + mu_ion[i];
    lnfugcoef[i] =
        mu[i] - log(Z);  // the natural logarithm of the fugacity coefficient
  }
  return lnfugcoef;
}
vector<double> pcsaft_fugcoef_cpp(double t, double rho, vector<double> x,
                                  add_args &cppargs) {
  /**
  Calculate the fugacity coefficients for one phase of the system.
  */
  int ncomp = x.size();  // number of components
  vector<double> lnfug = pcsaft_lnfug_cpp(t, rho, x, cppargs);
  vector<double> fugcoef(ncomp, 0);
  for (int i = 0; i < ncomp; i++) {
    fugcoef[i] = exp(lnfug[i]);  // the fugacity coefficients
  }
  return fugcoef;
}
double pcsaft_p_cpp(double t, double rho, vector<double> x, add_args &cppargs) {
  /**
  Calculate pressure
  */
  double den = rho * N_AV / 1.0e30;
  double Z = pcsaft_Z_cpp(t, rho, x, cppargs);
  double P = Z * kb * t * den * 1.0e30;  // Pa
  return P;
}
double pcsaft_ares_cpp(double t, double rho, vector<double> x,
                       add_args &cppargs) {
  /**
  Calculate the residual Helmholtz energy
  */
  int ncomp = x.size();  // number of components
  vector<double> d(ncomp);
  for (int i = 0; i < ncomp; i++) {
    d[i] = cppargs.s[i] * (1 - 0.12 * exp(-3 * cppargs.e[i] / t));
  }
  if (!cppargs.z.empty()) {
    for (int i = 0; i < ncomp; i++) {
      if (cppargs.z[i] != 0) {
        d[i] = cppargs.s[i] *
               (1 - 0.12);  // for ions the diameter is assumed to be
                            // temperature independent (see Held et al. 2014)
      }
    }
  }
  double den = rho * N_AV / 1.0e30;
  vector<double> zeta(4, 0);
  double summ;
  for (int i = 0; i < 4; i++) {
    summ = 0;
    for (int j = 0; j < ncomp; j++) {
      summ += x[j] * cppargs.m[j] * pow(d[j], i);
    }
    zeta[i] = PI / 6 * den * summ;
  }
  double eta = zeta[3];
  double m_avg = 0;
  for (int i = 0; i < ncomp; i++) {
    m_avg += x[i] * cppargs.m[i];
  }
  vector<double> ghs(ncomp * ncomp, 0);
  vector<double> e_ij(ncomp * ncomp, 0);
  vector<double> s_ij(ncomp * ncomp, 0);
  double m2es3 = 0.;
  double m2e2s3 = 0.;
  int idx = -1;
  for (int i = 0; i < ncomp; i++) {
    for (int j = 0; j < ncomp; j++) {
      idx += 1;
      if (cppargs.l_ij.empty()) {
        s_ij[idx] = (cppargs.s[i] + cppargs.s[j]) / 2.;
      } else {
        s_ij[idx] =
            (cppargs.s[i] + cppargs.s[j]) / 2. * (1 - cppargs.l_ij[idx]);
      }
      if (!cppargs.z.empty()) {
        if (cppargs.z[i] * cppargs.z[j] <=
            0) {  // for two cations or two anions e_ij is kept at zero to avoid
                  // dispersion between like ions (see Held et al. 2014)
          if (cppargs.k_ij.empty()) {
            e_ij[idx] = sqrt(cppargs.e[i] * cppargs.e[j]);
          } else {
            e_ij[idx] =
                sqrt(cppargs.e[i] * cppargs.e[j]) * (1 - cppargs.k_ij[idx]);
          }
        }
      } else {
        if (cppargs.k_ij.empty()) {
          e_ij[idx] = sqrt(cppargs.e[i] * cppargs.e[j]);
        } else {
          e_ij[idx] =
              sqrt(cppargs.e[i] * cppargs.e[j]) * (1 - cppargs.k_ij[idx]);
        }
      }
      m2es3 = m2es3 + x[i] * x[j] * cppargs.m[i] * cppargs.m[j] * e_ij[idx] /
                          t * pow(s_ij[idx], 3);
      m2e2s3 = m2e2s3 + x[i] * x[j] * cppargs.m[i] * cppargs.m[j] *
                            pow(e_ij[idx] / t, 2) * pow(s_ij[idx], 3);
      ghs[idx] = 1 / (1 - zeta[3]) +
                 (d[i] * d[j] / (d[i] + d[j])) * 3 * zeta[2] / (1 - zeta[3]) /
                     (1 - zeta[3]) +
                 pow(d[i] * d[j] / (d[i] + d[j]), 2) * 2 * zeta[2] * zeta[2] /
                     pow(1 - zeta[3], 3);
    }
  }
  double ares_hs =
      1 / zeta[0] *
      (3 * zeta[1] * zeta[2] / (1 - zeta[3]) +
       pow(zeta[2], 3.) / (zeta[3] * pow(1 - zeta[3], 2)) +
       (pow(zeta[2], 3.) / pow(zeta[3], 2.) - zeta[0]) * log(1 - zeta[3]));
  static double a0[7] = {0.9105631445,  0.6361281449, 2.6861347891,
                         -26.547362491, 97.759208784, -159.59154087,
                         91.297774084};
  static double a1[7] = {-0.3084016918, 0.1860531159,  -2.5030047259,
                         21.419793629,  -65.255885330, 83.318680481,
                         -33.746922930};
  static double a2[7] = {-0.0906148351, 0.4527842806,  0.5962700728,
                         -1.7241829131, -4.1302112531, 13.776631870,
                         -8.6728470368};
  static double b0[7] = {0.7240946941,  2.2382791861, -4.0025849485,
                         -21.003576815, 26.855641363, 206.55133841,
                         -355.60235612};
  static double b1[7] = {-0.5755498075, 0.6995095521, 3.8925673390,
                         -17.215471648, 192.67226447, -161.82646165,
                         -165.20769346};
  static double b2[7] = {0.0976883116, -0.2557574982, -9.1558561530,
                         20.642075974, -38.804430052, 93.626774077,
                         -29.666905585};
  vector<double> a(7, 0);
  vector<double> b(7, 0);
  for (int i = 0; i < 7; i++) {
    a[i] = a0[i] + (m_avg - 1.) / m_avg * a1[i] +
           (m_avg - 1.) / m_avg * (m_avg - 2.) / m_avg * a2[i];
    b[i] = b0[i] + (m_avg - 1.) / m_avg * b1[i] +
           (m_avg - 1.) / m_avg * (m_avg - 2.) / m_avg * b2[i];
  }
  double I1 = 0.0;
  double I2 = 0.0;
  for (int i = 0; i < 7; i++) {
    I1 += a[i] * pow(eta, i);
    I2 += b[i] * pow(eta, i);
  }
  double C1 =
      1. /
      (1. + m_avg * (8 * eta - 2 * eta * eta) / pow(1 - eta, 4) +
       (1 - m_avg) *
           (20 * eta - 27 * eta * eta + 12 * pow(eta, 3) - 2 * pow(eta, 4)) /
           pow((1 - eta) * (2 - eta), 2.0));
  summ = 0.0;
  for (int i = 0; i < ncomp; i++) {
    summ += x[i] * (cppargs.m[i] - 1) * log(ghs[i * ncomp + i]);
  }
  double ares_hc = m_avg * ares_hs - summ;
  double ares_disp =
      -2 * PI * den * I1 * m2es3 - PI * den * m_avg * C1 * I2 * m2e2s3;
  // Dipole term (Gross and Vrabec term) --------------------------------------
  double ares_polar = 0.;
  if (!cppargs.dipm.empty()) {
    double A2 = 0.;
    double A3 = 0.;
    vector<double> dipmSQ(ncomp, 0);
    static double a0dip[5] = {0.3043504, -0.1358588, 1.4493329, 0.3556977,
                              -2.0653308};
    static double a1dip[5] = {0.9534641, -1.8396383, 2.0131180, -7.3724958,
                              8.2374135};
    static double a2dip[5] = {-1.1610080, 4.5258607, 0.9751222, -12.281038,
                              5.9397575};
    static double b0dip[5] = {0.2187939, -1.1896431, 1.1626889, 0, 0};
    static double b1dip[5] = {-0.5873164, 1.2489132, -0.5085280, 0, 0};
    static double b2dip[5] = {3.4869576, -14.915974, 15.372022, 0, 0};
    static double c0dip[5] = {-0.0646774, 0.1975882, -0.8087562, 0.6902849, 0};
    static double c1dip[5] = {-0.9520876, 2.9924258, -2.3802636, -0.2701261, 0};
    static double c2dip[5] = {-0.6260979, 1.2924686, 1.6542783, -3.4396744, 0};
    const static double conv =
        7242.702976750923;  // conversion factor, see the note below Table 2 in
                            // Gross and Vrabec 2006
    for (int i = 0; i < ncomp; i++) {
      dipmSQ[i] = pow(cppargs.dipm[i], 2.) /
                  (cppargs.m[i] * cppargs.e[i] * pow(cppargs.s[i], 3.)) * conv;
    }
    vector<double> adip(5, 0);
    vector<double> bdip(5, 0);
    vector<double> cdip(5, 0);
    double J2, J3;
    double m_ij;
    double m_ijk;
    for (int i = 0; i < ncomp; i++) {
      for (int j = 0; j < ncomp; j++) {
        m_ij = sqrt(cppargs.m[i] * cppargs.m[j]);
        if (m_ij > 2) {
          m_ij = 2;
        }
        J2 = 0.;
        for (int l = 0; l < 5; l++) {
          adip[l] = a0dip[l] + (m_ij - 1) / m_ij * a1dip[l] +
                    (m_ij - 1) / m_ij * (m_ij - 2) / m_ij * a2dip[l];
          bdip[l] = b0dip[l] + (m_ij - 1) / m_ij * b1dip[l] +
                    (m_ij - 1) / m_ij * (m_ij - 2) / m_ij * b2dip[l];
          J2 += (adip[l] + bdip[l] * e_ij[j * ncomp + j] / t) *
                pow(eta, l);  // j*ncomp+j needs to be used for e_ij because it
                              // is formatted as a 1D vector
        }
        A2 += x[i] * x[j] * e_ij[i * ncomp + i] / t * e_ij[j * ncomp + j] / t *
              pow(s_ij[i * ncomp + i], 3) * pow(s_ij[j * ncomp + j], 3) /
              pow(s_ij[i * ncomp + j], 3) * cppargs.dip_num[i] *
              cppargs.dip_num[j] * dipmSQ[i] * dipmSQ[j] * J2;
        for (int k = 0; k < ncomp; k++) {
          m_ijk = pow((cppargs.m[i] * cppargs.m[j] * cppargs.m[k]), 1 / 3.);
          if (m_ijk > 2) {
            m_ijk = 2;
          }
          J3 = 0.;
          for (int l = 0; l < 5; l++) {
            cdip[l] = c0dip[l] + (m_ijk - 1) / m_ijk * c1dip[l] +
                      (m_ijk - 1) / m_ijk * (m_ijk - 2) / m_ijk * c2dip[l];
            J3 += cdip[l] * pow(eta, l);
          }
          A3 += x[i] * x[j] * x[k] * e_ij[i * ncomp + i] / t *
                e_ij[j * ncomp + j] / t * e_ij[k * ncomp + k] / t *
                pow(s_ij[i * ncomp + i], 3) * pow(s_ij[j * ncomp + j], 3) *
                pow(s_ij[k * ncomp + k], 3) / s_ij[i * ncomp + j] /
                s_ij[i * ncomp + k] / s_ij[j * ncomp + k] * cppargs.dip_num[i] *
                cppargs.dip_num[j] * cppargs.dip_num[k] * dipmSQ[i] *
                dipmSQ[j] * dipmSQ[k] * J3;
        }
      }
    }
    A2 = -PI * den * A2;
    A3 = -4 / 3. * PI * PI * den * den * A3;
    if (A2 != 0) {  // when the mole fraction of the polar compounds is 0 then
                    // A2 = 0 and division by 0 occurs
      ares_polar = A2 / (1 - A3 / A2);
    }
  }
  // Association term -------------------------------------------------------
  double ares_assoc = 0.;
  if (!cppargs.e_assoc.empty()) {
    int num_sites = 0;
    vector<int> iA;  // indices of associating compounds
    for (std::vector<int>::iterator it = cppargs.assoc_num.begin();
         it != cppargs.assoc_num.end(); ++it) {
      num_sites += *it;
      for (int i = 0; i < *it; i++) {
        iA.push_back(it - cppargs.assoc_num.begin());
      }
    }
    vector<double> x_assoc(
        num_sites);  // mole fractions of only the associating compounds
    for (int i = 0; i < num_sites; i++) {
      x_assoc[i] = x[iA[i]];
    }
    vector<double> XA(num_sites, 0);
    vector<double> delta_ij(num_sites * num_sites, 0);
    int idxa = 0;
    int idxi = 0;  // index for the ii-th compound
    int idxj = 0;  // index for the jj-th compound
    for (int i = 0; i < num_sites; i++) {
      idxi = iA[i] * ncomp + iA[i];
      for (int j = 0; j < num_sites; j++) {
        idxj = iA[j] * ncomp + iA[j];
        if (cppargs.assoc_matrix[idxa] != 0) {
          double eABij = (cppargs.e_assoc[iA[i]] + cppargs.e_assoc[iA[j]]) / 2.;
          double volABij = _HUGE;
          if (cppargs.k_hb.empty()) {
            volABij = sqrt(cppargs.vol_a[iA[i]] * cppargs.vol_a[iA[j]]) *
                      pow(sqrt(s_ij[idxi] * s_ij[idxj]) /
                              (0.5 * (s_ij[idxi] + s_ij[idxj])),
                          3);
          } else {
            volABij = sqrt(cppargs.vol_a[iA[i]] * cppargs.vol_a[iA[j]]) *
                      pow(sqrt(s_ij[idxi] * s_ij[idxj]) /
                              (0.5 * (s_ij[idxi] + s_ij[idxj])),
                          3) *
                      (1 - cppargs.k_hb[iA[i] * ncomp + iA[j]]);
          }
          delta_ij[idxa] = ghs[iA[i] * ncomp + iA[j]] * (exp(eABij / t) - 1) *
                           pow(s_ij[iA[i] * ncomp + iA[j]], 3) * volABij;
        }
        idxa += 1;
      }
      XA[i] = (-1 + sqrt(1 + 8 * den * delta_ij[i * num_sites + i])) /
              (4 * den * delta_ij[i * num_sites + i]);
      if (!std::isfinite(XA[i])) {
        XA[i] = 0.02;
      }
    }
    int ctr = 0;
    double dif = 1000.;
    vector<double> XA_old = XA;
    while ((ctr < 100) && (dif > 1e-15)) {
      ctr += 1;
      XA = XA_find(XA_old, delta_ij, den, x_assoc);
      dif = 0.;
      for (int i = 0; i < num_sites; i++) {
        dif += std::abs(XA[i] - XA_old[i]);
      }
      for (int i = 0; i < num_sites; i++) {
        XA_old[i] = (XA[i] + XA_old[i]) / 2.0;
      }
    }
    ares_assoc = 0.;
    for (int i = 0; i < num_sites; i++) {
      ares_assoc += x[iA[i]] * (log(XA[i]) - 0.5 * XA[i] + 0.5);
    }
  }
  // Ion term ---------------------------------------------------------------
  double ares_ion = 0.;
  if (!cppargs.z.empty()) {
    vector<double> q(cppargs.z.begin(), cppargs.z.end());
    for (int i = 0; i < ncomp; i++) {
      q[i] = q[i] * E_CHRG;
    }
    summ = 0.;
    for (int i = 0; i < ncomp; i++) {
      summ += cppargs.z[i] * cppargs.z[i] * x[i];
    }
    double kappa =
        sqrt(den * E_CHRG * E_CHRG / kb / t / (cppargs.dielc * perm_vac) *
             summ);  // the inverse Debye screening length. Equation 4 in Held
                     // et al. 2008.
    if (kappa != 0) {
      vector<double> chi(ncomp);
      vector<double> sigma_k(ncomp);
      summ = 0.;
      for (int i = 0; i < ncomp; i++) {
        chi[i] = 3 / pow(kappa * cppargs.s[i], 3) *
                 (1.5 + log(1 + kappa * cppargs.s[i]) -
                  2 * (1 + kappa * cppargs.s[i]) +
                  0.5 * pow(1 + kappa * cppargs.s[i], 2));
        summ += x[i] * q[i] * q[i] * chi[i] * kappa;
      }
      ares_ion = -1 / 12. / PI / kb / t / (cppargs.dielc * perm_vac) * summ;
    }
  }
  double ares = ares_hc + ares_disp + ares_polar + ares_assoc + ares_ion;
  printf("ares_hc=%.12f\n", ares_hc);
  printf("ares_disp=%.12f\n", ares_disp);
  return ares;
}
double pcsaft_dadt_cpp(double t, double rho, vector<double> x,
                       add_args &cppargs) {
  /**
  Calculate the temperature derivative of the residual Helmholtz energy at
  constant density.
  */
  int ncomp = x.size();  // number of components
  vector<double> d(ncomp), dd_dt(ncomp);
  for (int i = 0; i < ncomp; i++) {
    d[i] = cppargs.s[i] * (1 - 0.12 * exp(-3 * cppargs.e[i] / t));
    dd_dt[i] = cppargs.s[i] * -3 * cppargs.e[i] / t / t * 0.12 *
               exp(-3 * cppargs.e[i] / t);
  }
  if (!cppargs.z.empty()) {
    for (int i = 0; i < ncomp; i++) {
      if (cppargs.z[i] != 0) {
        d[i] = cppargs.s[i] *
               (1 - 0.12);  // for ions the diameter is assumed to be
                            // temperature independent (see Held et al. 2014)
        dd_dt[i] = 0.;
      }
    }
  }
  double den = rho * N_AV / 1.0e30;
  vector<double> zeta(4, 0);
  double summ;
  for (int i = 0; i < 4; i++) {
    summ = 0;
    for (int j = 0; j < ncomp; j++) {
      summ += x[j] * cppargs.m[j] * pow(d[j], i);
    }
    zeta[i] = PI / 6 * den * summ;
  }
  vector<double> dzeta_dt(4, 0);
  for (int i = 1; i < 4; i++) {
    summ = 0;
    for (int j = 0; j < ncomp; j++) {
      summ += x[j] * cppargs.m[j] * i * dd_dt[j] * pow(d[j], (i - 1));
    }
    dzeta_dt[i] = PI / 6 * den * summ;
  }
  double eta = zeta[3];
  double m_avg = 0;
  for (int i = 0; i < ncomp; i++) {
    m_avg += x[i] * cppargs.m[i];
  }
  vector<double> ghs(ncomp * ncomp, 0);
  vector<double> dghs_dt(ncomp * ncomp, 0);
  vector<double> e_ij(ncomp * ncomp, 0);
  vector<double> s_ij(ncomp * ncomp, 0);
  double m2es3 = 0.;
  double m2e2s3 = 0.;
  double ddij_dt;
  int idx = -1;
  for (int i = 0; i < ncomp; i++) {
    for (int j = 0; j < ncomp; j++) {
      idx += 1;
      if (cppargs.l_ij.empty()) {
        s_ij[idx] = (cppargs.s[i] + cppargs.s[j]) / 2.;
      } else {
        s_ij[idx] =
            (cppargs.s[i] + cppargs.s[j]) / 2. * (1 - cppargs.l_ij[idx]);
      }
      if (!cppargs.z.empty()) {
        if (cppargs.z[i] * cppargs.z[j] <=
            0) {  // for two cations or two anions e_ij is kept at zero to avoid
                  // dispersion between like ions (see Held et al. 2014)
          if (cppargs.k_ij.empty()) {
            e_ij[idx] = sqrt(cppargs.e[i] * cppargs.e[j]);
          } else {
            e_ij[idx] =
                sqrt(cppargs.e[i] * cppargs.e[j]) * (1 - cppargs.k_ij[idx]);
          }
        }
      } else {
        if (cppargs.k_ij.empty()) {
          e_ij[idx] = sqrt(cppargs.e[i] * cppargs.e[j]);
        } else {
          e_ij[idx] =
              sqrt(cppargs.e[i] * cppargs.e[j]) * (1 - cppargs.k_ij[idx]);
        }
      }
      m2es3 = m2es3 + x[i] * x[j] * cppargs.m[i] * cppargs.m[j] * e_ij[idx] /
                          t * pow(s_ij[idx], 3);
      m2e2s3 = m2e2s3 + x[i] * x[j] * cppargs.m[i] * cppargs.m[j] *
                            pow(e_ij[idx] / t, 2) * pow(s_ij[idx], 3);
      ghs[idx] = 1 / (1 - zeta[3]) +
                 (d[i] * d[j] / (d[i] + d[j])) * 3 * zeta[2] / (1 - zeta[3]) /
                     (1 - zeta[3]) +
                 pow(d[i] * d[j] / (d[i] + d[j]), 2) * 2 * zeta[2] * zeta[2] /
                     pow(1 - zeta[3], 3);
      ddij_dt = (d[i] * d[j] / (d[i] + d[j])) *
                (dd_dt[i] / d[i] + dd_dt[j] / d[j] -
                 (dd_dt[i] + dd_dt[j]) / (d[i] + d[j]));
      dghs_dt[idx] = dzeta_dt[3] / pow(1 - zeta[3], 2.) +
                     3 *
                         (ddij_dt * zeta[2] +
                          (d[i] * d[j] / (d[i] + d[j])) * dzeta_dt[2]) /
                         pow(1 - zeta[3], 2.) +
                     4 * (d[i] * d[j] / (d[i] + d[j])) * zeta[2] *
                         (1.5 * dzeta_dt[3] + ddij_dt * zeta[2] +
                          (d[i] * d[j] / (d[i] + d[j])) * dzeta_dt[2]) /
                         pow(1 - zeta[3], 3.) +
                     6 * pow((d[i] * d[j] / (d[i] + d[j])) * zeta[2], 2.) *
                         dzeta_dt[3] / pow(1 - zeta[3], 4.);
    }
  }
  double dadt_hs =
      1 / zeta[0] *
      (3 * (dzeta_dt[1] * zeta[2] + zeta[1] * dzeta_dt[2]) / (1 - zeta[3]) +
       3 * zeta[1] * zeta[2] * dzeta_dt[3] / pow(1 - zeta[3], 2.) +
       3 * pow(zeta[2], 2.) * dzeta_dt[2] / zeta[3] / pow(1 - zeta[3], 2.) +
       pow(zeta[2], 3.) * dzeta_dt[3] * (3 * zeta[3] - 1) / pow(zeta[3], 2.) /
           pow(1 - zeta[3], 3.) +
       (3 * pow(zeta[2], 2.) * dzeta_dt[2] * zeta[3] -
        2 * pow(zeta[2], 3.) * dzeta_dt[3]) /
           pow(zeta[3], 3.) * log(1 - zeta[3]) +
       (zeta[0] - pow(zeta[2], 3) / pow(zeta[3], 2.)) * dzeta_dt[3] /
           (1 - zeta[3]));
  static double a0[7] = {0.9105631445,  0.6361281449, 2.6861347891,
                         -26.547362491, 97.759208784, -159.59154087,
                         91.297774084};
  static double a1[7] = {-0.3084016918, 0.1860531159,  -2.5030047259,
                         21.419793629,  -65.255885330, 83.318680481,
                         -33.746922930};
  static double a2[7] = {-0.0906148351, 0.4527842806,  0.5962700728,
                         -1.7241829131, -4.1302112531, 13.776631870,
                         -8.6728470368};
  static double b0[7] = {0.7240946941,  2.2382791861, -4.0025849485,
                         -21.003576815, 26.855641363, 206.55133841,
                         -355.60235612};
  static double b1[7] = {-0.5755498075, 0.6995095521, 3.8925673390,
                         -17.215471648, 192.67226447, -161.82646165,
                         -165.20769346};
  static double b2[7] = {0.0976883116, -0.2557574982, -9.1558561530,
                         20.642075974, -38.804430052, 93.626774077,
                         -29.666905585};
  vector<double> a(7, 0);
  vector<double> b(7, 0);
  for (int i = 0; i < 7; i++) {
    a[i] = a0[i] + (m_avg - 1.) / m_avg * a1[i] +
           (m_avg - 1.) / m_avg * (m_avg - 2.) / m_avg * a2[i];
    b[i] = b0[i] + (m_avg - 1.) / m_avg * b1[i] +
           (m_avg - 1.) / m_avg * (m_avg - 2.) / m_avg * b2[i];
  }
  double I1 = 0.0;
  double I2 = 0.0;
  double dI1_dt = 0.0, dI2_dt = 0.;
  for (int i = 0; i < 7; i++) {
    I1 += a[i] * pow(eta, i);
    I2 += b[i] * pow(eta, i);
    dI1_dt += a[i] * dzeta_dt[3] * i * pow(eta, i - 1);
    dI2_dt += b[i] * dzeta_dt[3] * i * pow(eta, i - 1);
  }
  double C1 =
      1. /
      (1. + m_avg * (8 * eta - 2 * eta * eta) / pow(1 - eta, 4) +
       (1 - m_avg) *
           (20 * eta - 27 * eta * eta + 12 * pow(eta, 3) - 2 * pow(eta, 4)) /
           pow((1 - eta) * (2 - eta), 2.0));
  double C2 =
      -1 * C1 * C1 *
      (m_avg * (-4 * eta * eta + 20 * eta + 8) / pow(1 - eta, 5.) +
       (1 - m_avg) * (2 * pow(eta, 3) + 12 * eta * eta - 48 * eta + 40) /
           pow((1 - eta) * (2 - eta), 3));
  double dC1_dt = C2 * dzeta_dt[3];
  summ = 0.;
  for (int i = 0; i < ncomp; i++) {
    summ +=
        x[i] * (cppargs.m[i] - 1) * dghs_dt[i * ncomp + i] / ghs[i * ncomp + i];
  }
  double dadt_hc = m_avg * dadt_hs - summ;
  double dadt_disp =
      -2 * PI * den * (dI1_dt - I1 / t) * m2es3 -
      PI * den * m_avg * (dC1_dt * I2 + C1 * dI2_dt - 2 * C1 * I2 / t) * m2e2s3;
  // Dipole term (Gross and Vrabec term) --------------------------------------
  double dadt_polar = 0.;
  if (!cppargs.dipm.empty()) {
    double A2 = 0.;
    double A3 = 0.;
    double dA2_dt = 0.;
    double dA3_dt = 0.;
    vector<double> dipmSQ(ncomp, 0);
    static double a0dip[5] = {0.3043504, -0.1358588, 1.4493329, 0.3556977,
                              -2.0653308};
    static double a1dip[5] = {0.9534641, -1.8396383, 2.0131180, -7.3724958,
                              8.2374135};
    static double a2dip[5] = {-1.1610080, 4.5258607, 0.9751222, -12.281038,
                              5.9397575};
    static double b0dip[5] = {0.2187939, -1.1896431, 1.1626889, 0, 0};
    static double b1dip[5] = {-0.5873164, 1.2489132, -0.5085280, 0, 0};
    static double b2dip[5] = {3.4869576, -14.915974, 15.372022, 0, 0};
    static double c0dip[5] = {-0.0646774, 0.1975882, -0.8087562, 0.6902849, 0};
    static double c1dip[5] = {-0.9520876, 2.9924258, -2.3802636, -0.2701261, 0};
    static double c2dip[5] = {-0.6260979, 1.2924686, 1.6542783, -3.4396744, 0};
    const static double conv =
        7242.702976750923;  // conversion factor, see the note below Table 2 in
                            // Gross and Vrabec 2006
    for (int i = 0; i < ncomp; i++) {
      dipmSQ[i] = pow(cppargs.dipm[i], 2.) /
                  (cppargs.m[i] * cppargs.e[i] * pow(cppargs.s[i], 3.)) * conv;
    }
    vector<double> adip(5, 0);
    vector<double> bdip(5, 0);
    vector<double> cdip(5, 0);
    double J2, J3, dJ2_dt, dJ3_dt;
    double m_ij;
    double m_ijk;
    for (int i = 0; i < ncomp; i++) {
      for (int j = 0; j < ncomp; j++) {
        m_ij = sqrt(cppargs.m[i] * cppargs.m[j]);
        if (m_ij > 2) {
          m_ij = 2;
        }
        J2 = 0.;
        dJ2_dt = 0.;
        for (int l = 0; l < 5; l++) {
          adip[l] = a0dip[l] + (m_ij - 1) / m_ij * a1dip[l] +
                    (m_ij - 1) / m_ij * (m_ij - 2) / m_ij * a2dip[l];
          bdip[l] = b0dip[l] + (m_ij - 1) / m_ij * b1dip[l] +
                    (m_ij - 1) / m_ij * (m_ij - 2) / m_ij * b2dip[l];
          J2 += (adip[l] + bdip[l] * e_ij[j * ncomp + j] / t) *
                pow(eta, l);  // j*ncomp+j needs to be used for e_ij because it
                              // is formatted as a 1D vector
          dJ2_dt += adip[l] * l * pow(eta, l - 1) * dzeta_dt[3] +
                    bdip[l] * e_ij[j * ncomp + j] *
                        (1 / t * l * pow(eta, l - 1) * dzeta_dt[3] -
                         1 / pow(t, 2.) * pow(eta, l));
        }
        A2 += x[i] * x[j] * e_ij[i * ncomp + i] / t * e_ij[j * ncomp + j] / t *
              pow(s_ij[i * ncomp + i], 3) * pow(s_ij[j * ncomp + j], 3) /
              pow(s_ij[i * ncomp + j], 3) * cppargs.dip_num[i] *
              cppargs.dip_num[j] * dipmSQ[i] * dipmSQ[j] * J2;
        dA2_dt += x[i] * x[j] * e_ij[i * ncomp + i] * e_ij[j * ncomp + j] *
                  pow(s_ij[i * ncomp + i], 3) * pow(s_ij[j * ncomp + j], 3) /
                  pow(s_ij[i * ncomp + j], 3) * cppargs.dip_num[i] *
                  cppargs.dip_num[j] * dipmSQ[i] * dipmSQ[j] *
                  (dJ2_dt / pow(t, 2) - 2 * J2 / pow(t, 3));
        for (int k = 0; k < ncomp; k++) {
          m_ijk = pow((cppargs.m[i] * cppargs.m[j] * cppargs.m[k]), 1 / 3.);
          if (m_ijk > 2) {
            m_ijk = 2;
          }
          J3 = 0.;
          dJ3_dt = 0.;
          for (int l = 0; l < 5; l++) {
            cdip[l] = c0dip[l] + (m_ijk - 1) / m_ijk * c1dip[l] +
                      (m_ijk - 1) / m_ijk * (m_ijk - 2) / m_ijk * c2dip[l];
            J3 += cdip[l] * pow(eta, l);
            dJ3_dt += cdip[l] * l * pow(eta, l - 1) * dzeta_dt[3];
          }
          A3 += x[i] * x[j] * x[k] * e_ij[i * ncomp + i] / t *
                e_ij[j * ncomp + j] / t * e_ij[k * ncomp + k] / t *
                pow(s_ij[i * ncomp + i], 3) * pow(s_ij[j * ncomp + j], 3) *
                pow(s_ij[k * ncomp + k], 3) / s_ij[i * ncomp + j] /
                s_ij[i * ncomp + k] / s_ij[j * ncomp + k] * cppargs.dip_num[i] *
                cppargs.dip_num[j] * cppargs.dip_num[k] * dipmSQ[i] *
                dipmSQ[j] * dipmSQ[k] * J3;
          dA3_dt += x[i] * x[j] * x[k] * e_ij[i * ncomp + i] *
                    e_ij[j * ncomp + j] * e_ij[k * ncomp + k] *
                    pow(s_ij[i * ncomp + i], 3) * pow(s_ij[j * ncomp + j], 3) *
                    pow(s_ij[k * ncomp + k], 3) / s_ij[i * ncomp + j] /
                    s_ij[i * ncomp + k] / s_ij[j * ncomp + k] *
                    cppargs.dip_num[i] * cppargs.dip_num[j] *
                    cppargs.dip_num[k] * dipmSQ[i] * dipmSQ[j] * dipmSQ[k] *
                    (-3 * J3 / pow(t, 4) + dJ3_dt / pow(t, 3));
        }
      }
    }
    A2 = -PI * den * A2;
    A3 = -4 / 3. * PI * PI * den * den * A3;
    dA2_dt = -PI * den * dA2_dt;
    dA3_dt = -4 / 3. * PI * PI * den * den * dA3_dt;
    if (A2 != 0) {  // when the mole fraction of the polar compounds is 0 then
                    // A2 = 0 and division by 0 occurs
      dadt_polar =
          (dA2_dt - 2 * A3 / A2 * dA2_dt + dA3_dt) / pow(1 - A3 / A2, 2.);
    }
  }
  // Association term -------------------------------------------------------
  // only the 2B association type is currently implemented
  double dadt_assoc = 0.;
  if (!cppargs.e_assoc.empty()) {
    int num_sites = 0;
    vector<int> iA;  // indices of associating compounds
    for (std::vector<int>::iterator it = cppargs.assoc_num.begin();
         it != cppargs.assoc_num.end(); ++it) {
      num_sites += *it;
      for (int i = 0; i < *it; i++) {
        iA.push_back(it - cppargs.assoc_num.begin());
      }
    }
    vector<double> x_assoc(
        num_sites);  // mole fractions of only the associating compounds
    for (int i = 0; i < num_sites; i++) {
      x_assoc[i] = x[iA[i]];
    }
    vector<double> XA(num_sites, 0);
    vector<double> delta_ij(num_sites * num_sites, 0);
    vector<double> ddelta_dt(num_sites * num_sites, 0);
    int idxa = 0;
    int idxi = 0;  // index for the ii-th compound
    int idxj = 0;  // index for the jj-th compound
    for (int i = 0; i < num_sites; i++) {
      idxi = iA[i] * ncomp + iA[i];
      for (int j = 0; j < num_sites; j++) {
        idxj = iA[j] * ncomp + iA[j];
        if (cppargs.assoc_matrix[idxa] != 0) {
          double eABij = (cppargs.e_assoc[iA[i]] + cppargs.e_assoc[iA[j]]) / 2.;
          double volABij = _HUGE;
          if (cppargs.k_hb.empty()) {
            volABij = sqrt(cppargs.vol_a[iA[i]] * cppargs.vol_a[iA[j]]) *
                      pow(sqrt(s_ij[idxi] * s_ij[idxj]) /
                              (0.5 * (s_ij[idxi] + s_ij[idxj])),
                          3);
          } else {
            volABij = sqrt(cppargs.vol_a[iA[i]] * cppargs.vol_a[iA[j]]) *
                      pow(sqrt(s_ij[idxi] * s_ij[idxj]) /
                              (0.5 * (s_ij[idxi] + s_ij[idxj])),
                          3) *
                      (1 - cppargs.k_hb[iA[i] * ncomp + iA[j]]);
          }
          delta_ij[idxa] = ghs[iA[i] * ncomp + iA[j]] * (exp(eABij / t) - 1) *
                           pow(s_ij[iA[i] * ncomp + iA[j]], 3) * volABij;
          ddelta_dt[idxa] =
              pow(s_ij[idxj], 3) * volABij *
              (-eABij / pow(t, 2) * exp(eABij / t) *
                   ghs[iA[i] * ncomp + iA[j]] +
               dghs_dt[iA[i] * ncomp + iA[j]] * (exp(eABij / t) - 1));
        }
        idxa += 1;
      }
      XA[i] = (-1 + sqrt(1 + 8 * den * delta_ij[i * num_sites + i])) /
              (4 * den * delta_ij[i * num_sites + i]);
      if (!std::isfinite(XA[i])) {
        XA[i] = 0.02;
      }
    }
    int ctr = 0;
    double dif = 1000.;
    vector<double> XA_old = XA;
    while ((ctr < 100) && (dif > 1e-15)) {
      ctr += 1;
      XA = XA_find(XA_old, delta_ij, den, x_assoc);
      dif = 0.;
      for (int i = 0; i < num_sites; i++) {
        dif += std::abs(XA[i] - XA_old[i]);
      }
      for (int i = 0; i < num_sites; i++) {
        XA_old[i] = (XA[i] + XA_old[i]) / 2.0;
      }
    }
    vector<double> dXA_dt(num_sites, 0);
    dXA_dt = dXAdt_find(delta_ij, den, XA, ddelta_dt, x_assoc);
    for (int i = 0; i < num_sites; i++) {
      dadt_assoc += x[iA[i]] * (1 / XA[i] - 0.5) * dXA_dt[i];
    }
  }
  // Ion term ---------------------------------------------------------------
  double dadt_ion = 0.;
  if (!cppargs.z.empty()) {
    vector<double> q(cppargs.z.begin(), cppargs.z.end());
    for (int i = 0; i < ncomp; i++) {
      q[i] = q[i] * E_CHRG;
    }
    summ = 0.;
    for (int i = 0; i < ncomp; i++) {
      summ += cppargs.z[i] * cppargs.z[i] * x[i];
    }
    double kappa =
        sqrt(den * E_CHRG * E_CHRG / kb / t / (cppargs.dielc * perm_vac) *
             summ);  // the inverse Debye screening length. Equation 4 in Held
                     // et al. 2008.
    double dkappa_dt;
    if (kappa != 0) {
      vector<double> chi(ncomp);
      vector<double> dchikap_dk(ncomp);
      summ = 0.;
      for (int i = 0; i < ncomp; i++) {
        chi[i] = 3 / pow(kappa * cppargs.s[i], 3) *
                 (1.5 + log(1 + kappa * cppargs.s[i]) -
                  2 * (1 + kappa * cppargs.s[i]) +
                  0.5 * pow(1 + kappa * cppargs.s[i], 2));
        dchikap_dk[i] = -2 * chi[i] + 3 / (1 + kappa * cppargs.s[i]);
        summ += x[i] * cppargs.z[i] * cppargs.z[i];
      }
      dkappa_dt = -0.5 * den * E_CHRG * E_CHRG / kb / t / t /
                  (cppargs.dielc * perm_vac) * summ / kappa;
      summ = 0.;
      for (int i = 0; i < ncomp; i++) {
        summ += x[i] * q[i] * q[i] *
                (dchikap_dk[i] * dkappa_dt / t - kappa * chi[i] / t / t);
      }
      dadt_ion = -1 / 12. / PI / kb / (cppargs.dielc * perm_vac) * summ;
    }
  }
  double dadt = dadt_hc + dadt_disp + dadt_assoc + dadt_polar + dadt_ion;
  return dadt;
}
double pcsaft_hres_cpp(double t, double rho, vector<double> x,
                       add_args &cppargs) {
  /**
  Calculate the residual enthalpy for one phase of the system.
  */
  double Z = pcsaft_Z_cpp(t, rho, x, cppargs);
  double dares_dt = pcsaft_dadt_cpp(t, rho, x, cppargs);
  double hres = (-t * dares_dt + (Z - 1)) * kb * N_AV *
                t;  // Equation A.46 from Gross and Sadowski 2001
  return hres;
}
double pcsaft_sres_cpp(double t, double rho, vector<double> x,
                       add_args &cppargs) {
  /**
  Calculate the residual entropy (constant volume) for one phase of the system.
  */
  double gres = pcsaft_gres_cpp(t, rho, x, cppargs);
  double hres = pcsaft_hres_cpp(t, rho, x, cppargs);
  double sres = (hres - gres) / t;
  return sres;
}
double pcsaft_gres_cpp(double t, double rho, vector<double> x,
                       add_args &cppargs) {
  /**
  Calculate the residual Gibbs energy for one phase of the system.
  */
  double ares = pcsaft_ares_cpp(t, rho, x, cppargs);
  double Z = pcsaft_Z_cpp(t, rho, x, cppargs);
  double gres = (ares + (Z - 1) - log(Z)) * kb * N_AV *
                t;  // Equation A.50 from Gross and Sadowski 2001
  return gres;
}
vector<double> flashTQ_cpp(double t, double Q, vector<double> x,
                           add_args &cppargs) {
  bool solution_found = false;
  double p_guess;
  vector<double> output;
  try {
    p_guess = estimate_flash_p(t, Q, x, cppargs);
    output = outerTQ(p_guess, t, Q, x, cppargs);
    solution_found = true;
  } catch (const SolutionError &ex) {
  } catch (const ValueError &ex) {
  }
  // if solution hasn't been found, try cycling through a range of pressures
  if (!solution_found) {
    double p_lbound = -6;  // here we're using log10 of the pressure
    double p_ubound = 9;
    double p_step = 0.1;
    p_guess = p_lbound;
    while (p_guess < p_ubound && !solution_found) {
      try {
        output = outerTQ(pow(10, p_guess), t, Q, x, cppargs);
        solution_found = true;
      } catch (const SolutionError &ex) {
        p_guess += p_step;
      } catch (const ValueError &ex) {
        p_guess += p_step;
      }
    }
  }
  if (!solution_found) {
    throw SolutionError("solution could not be found for TQ flash");
  }
  return output;
}
vector<double> flashTQ_cpp(double t, double Q, vector<double> x,
                           add_args &cppargs, double p_guess) {
  vector<double> output;
  try {
    output = outerTQ(p_guess, t, Q, x, cppargs);
  } catch (const SolutionError &ex) {
    throw ex;
    output = flashTQ_cpp(t, Q, x,
                         cppargs);  // call function without an initial guess
  }
  return output;
}
vector<double> flashPQ_cpp(double p, double Q, vector<double> x,
                           add_args &cppargs) {
  bool solution_found = false;
  double t_guess;
  vector<double> output;
  try {
    t_guess = estimate_flash_t(p, Q, x, cppargs);
    output = outerPQ(t_guess, p, Q, x, cppargs);
    solution_found = true;
  } catch (const SolutionError &ex) {
  } catch (const ValueError &ex) {
  }
  // if solution hasn't been found, try calling the flash function directly with
  // a range of initial temperatures
  if (!solution_found) {
    double t_lbound = 1;
    double t_ubound = 800;
    double t_step = 10;
    if (!cppargs.z.empty()) {
      t_lbound = 264;
      t_ubound = 350;
    }
    t_guess = t_ubound;
    while (t_guess > t_lbound && !solution_found) {
      try {
        output = outerPQ(t_guess, p, Q, x, cppargs);
        solution_found = true;
      } catch (const SolutionError &ex) {
        t_guess -= t_step;
      } catch (const ValueError &ex) {
        t_guess -= t_step;
      }
    }
  }
  if (!solution_found) {
    throw SolutionError("solution could not be found for PQ flash");
  }
  return output;
}
vector<double> flashPQ_cpp(double p, double Q, vector<double> x,
                           add_args &cppargs, double t_guess) {
  vector<double> output;
  try {
    output = outerPQ(t_guess, p, Q, x, cppargs);
  } catch (const SolutionError &ex) {
    output = flashPQ_cpp(p, Q, x,
                         cppargs);  // call function without an initial guess
  }
  return output;
}
vector<double> outerPQ(double t_guess, double p, double Q, vector<double> x,
                       add_args &cppargs) {
  // Based on the algorithm proposed in H. A. J. Watson, M. Vikse, T. Gundersen,
  // and P. I. Barton, “Reliable Flash Calculations: Part 1. Nonsmooth
  // Inside-Out Algorithms,” Ind. Eng. Chem. Res., vol. 56, no. 4, pp. 960–973,
  // Feb. 2017, doi: 10.1021/acs.iecr.6b03956.
  int ncomp = x.size();
  double TOL = 1e-8;
  double MAXITER = 200;
  double x_ions = 0.;  // overall mole fraction of ions in the system
  for (int i = 0; i < ncomp; i++) {
    if (!cppargs.z.empty() && cppargs.z[i] != 0) {
      x_ions += x[i];
    }
  }
  // initialize variables
  vector<double> fugcoef_l(ncomp), fugcoef_v(ncomp), k(ncomp), u(ncomp),
      kprime(ncomp);
  double rhol, rhov;
  double Tref = t_guess - 1;
  double Tprime = t_guess + 1;
  double t = t_guess;
  // calculate sigma for water, if it is present
  std::vector<double>::iterator water_iter =
      std::find(cppargs.e.begin(), cppargs.e.end(), 353.9449);
  int water_idx = -1;
  if (water_iter != cppargs.e.end()) {
    water_idx = std::distance(cppargs.e.begin(), water_iter);
    cppargs.s[water_idx] = calc_sigma(t, &calc_water_sigma);
    cppargs.dielc = dielc_water(
        t);  // Right now only aqueous mixtures are supported. Other solvents
             // could be modeled by replacing the dielc_water function.
  }
  // calculate initial guess for compositions based on fugacity coefficients and
  // Raoult's Law.
  rhol = pcsaft_den_cpp(t, p, x, 0, cppargs);
  rhov = pcsaft_den_cpp(t, p, x, 1, cppargs);
  if ((rhol - rhov) < 1e-4) {
    throw SolutionError("liquid and vapor densities are the same.");
  }
  fugcoef_l = pcsaft_fugcoef_cpp(t, rhol, x, cppargs);
  fugcoef_v = pcsaft_fugcoef_cpp(t, rhov, x, cppargs);
  for (int i = 0; i < ncomp; i++) {
    if (cppargs.z.empty() || cppargs.z[i] == 0) {
      k[i] = fugcoef_l[i] / fugcoef_v[i];
    } else {
      k[i] = 0;  // set k to 0 for ionic components
    }
  }
  vector<double> xl(ncomp);
  vector<double> xv(ncomp);
  double xv_sum = 0;
  double xl_sum = 0;
  for (int i = 0; i < ncomp; i++) {
    xl[i] = x[i] / (1 + Q * (k[i] - 1));
    xl_sum += xl[i];
    xv[i] = k[i] * x[i] / (1 + Q * (k[i] - 1));
    xv_sum += xv[i];
  }
  if (xv_sum != 1) {
    for (int i = 0; i < ncomp; i++) {
      xv[i] = xv[i] / xv_sum;
    }
  }
  if (xl_sum != 1) {
    for (int i = 0; i < ncomp; i++) {
      xl[i] = xl[i] / xl_sum;
    }
  }
  rhol = pcsaft_den_cpp(t, p, xl, 0, cppargs);
  fugcoef_l = pcsaft_fugcoef_cpp(t, rhol, xl, cppargs);
  rhov = pcsaft_den_cpp(t, p, xv, 1, cppargs);
  fugcoef_v = pcsaft_fugcoef_cpp(t, rhov, xv, cppargs);
  for (int i = 0; i < ncomp; i++) {
    k[i] = fugcoef_l[i] / fugcoef_v[i];
    u[i] = std::log(k[i] / kb);
  }
  if (water_idx >= 0) {
    cppargs.s[water_idx] = calc_sigma(Tprime, &calc_water_sigma);
    cppargs.dielc =
        dielc_water(Tprime);  // Right now only aqueous mixtures are supported.
                              // Other solvents could be modeled by replacing
                              // the dielc_water function.
  }
  rhol = pcsaft_den_cpp(Tprime, p, xl, 0, cppargs);
  fugcoef_l = pcsaft_fugcoef_cpp(Tprime, rhol, xl, cppargs);
  rhov = pcsaft_den_cpp(Tprime, p, xv, 1, cppargs);
  fugcoef_v = pcsaft_fugcoef_cpp(Tprime, rhov, xv, cppargs);
  for (int i = 0; i < ncomp; i++) {
    kprime[i] = fugcoef_l[i] / fugcoef_v[i];
  }
  vector<double> t_weight(ncomp);
  double t_sum = 0;
  for (int i = 0; i < ncomp; i++) {
    double dlnk_dt = (kprime[i] - k[i]) / (Tprime - t);
    t_weight[i] = xv[i] * dlnk_dt / (1 + Q * (k[i] - 1));
    t_sum += t_weight[i];
  }
  double kb = 0;
  for (int i = 0; i < ncomp; i++) {
    double wi = t_weight[i] / t_sum;
    if (cppargs.z.empty() || cppargs.z[i] == 0) {
      kb += wi * std::log(k[i]);
    }
  }
  kb = std::exp(kb);
  t_sum = 0;
  for (int i = 0; i < ncomp; i++) {
    double dlnk_dt = (kprime[i] - k[i]) / (Tprime - t);
    t_weight[i] = xv[i] * dlnk_dt / (1 + Q * (kprime[i] - 1));
    t_sum += t_weight[i];
  }
  double kbprime = 0;
  for (int i = 0; i < ncomp; i++) {
    double wi = t_weight[i] / t_sum;
    if (cppargs.z.empty() || cppargs.z[i] == 0) {
      kbprime += wi * std::log(kprime[i]);
    }
  }
  kbprime = std::exp(kbprime);
  double kb0 = kbprime;
  for (int i = 0; i < ncomp; i++) {
    u[i] = std::log(k[i] / kb);
  }
  double B = std::log(kbprime / kb) / (1 / Tprime - 1 / t);
  double A = std::log(kb) - B * (1 / t - 1 / Tref);
  if (B > 0) {
    throw SolutionError("B > 0 in outerPQ");
  }
  // solve
  vector<double> pp(ncomp);
  double maxdif = 1e10 * TOL;
  int itr = 0;
  double Rmin = 0, Rmax = 1;
  while (maxdif > TOL && itr < MAXITER) {
    // save previous values for calculating the difference at the end of the
    // iteration
    vector<double> u_old = u;
    double A_old = A;
    double R0 = kb * Q / (kb * Q + kb0 * (1 - Q));
    double R = BoundedSecantInner(kb0, Q, u, x, cppargs, R0, Rmin, Rmax,
                                  DBL_EPSILON, 1e-8, 200);
    double pp_sum = 0;
    double eupp_sum = 0;
    for (int i = 0; i < ncomp; i++) {
      pp[i] = x[i] / (1 - R + kb0 * R * std::exp(u[i]));
      if (cppargs.z.empty() || cppargs.z[i] == 0) {
        pp_sum += pp[i];
        eupp_sum += std::exp(u[i]) * pp[i];
      }
    }
    kb = pp_sum / eupp_sum;
    t = 1 / (1 / Tref + (std::log(kb) - A) / B);
    for (int i = 0; i < ncomp; i++) {
      if (x_ions == 0) {
        xl[i] = pp[i] / pp_sum;
        xv[i] = std::exp(u[i]) * pp[i] / eupp_sum;
      } else if (cppargs.z.empty() || cppargs.z[i] == 0) {
        xl[i] = pp[i] / pp_sum * (1 - x_ions / (1 - Q));
        xv[i] = std::exp(u[i]) * pp[i] / eupp_sum;
      } else {
        xl[i] = x[i] / (1 - Q);
        xv[i] = 0;
      }
    }
    if (water_idx >= 0) {
      cppargs.s[water_idx] = calc_sigma(t, &calc_water_sigma);
      cppargs.dielc = dielc_water(
          t);  // Right now only aqueous mixtures are supported. Other solvents
               // could be modeled by replacing the dielc_water function.
    }
    rhol = pcsaft_den_cpp(t, p, xl, 0, cppargs);
    fugcoef_l = pcsaft_fugcoef_cpp(t, rhol, xl, cppargs);
    rhov = pcsaft_den_cpp(t, p, xv, 1, cppargs);
    fugcoef_v = pcsaft_fugcoef_cpp(t, rhov, xv, cppargs);
    for (int i = 0; i < ncomp; i++) {
      k[i] = fugcoef_l[i] / fugcoef_v[i];
      u[i] = std::log(k[i] / kb);
    }
    if (itr == 0) {
      B = std::log(kbprime / kb) / (1 / Tprime - 1 / t);
      if (B > 0) {
        throw SolutionError("B > 0 in outerPQ");
      }
    }
    A = std::log(kb) - B * (1 / t - 1 / Tref);
    maxdif = std::abs(A - A_old);
    for (int i = 0; i < ncomp; i++) {
      if (cppargs.z.empty() || cppargs.z[i] == 0) {
        double dif = std::abs(u[i] - u_old[i]);
        if (dif > maxdif) {
          maxdif = dif;
        }
      }
    }
    itr += 1;
  }
  if (!std::isfinite(t) || maxdif > 1e-3 || t < 0) {
    throw SolutionError("outerPQ did not converge to a solution");
  }
  vector<double> result;
  result.push_back(t);
  result.insert(result.end(), xl.begin(), xl.end());
  result.insert(result.end(), xv.begin(), xv.end());
  return result;
}
vector<double> outerTQ(double p_guess, double t, double Q, vector<double> x,
                       add_args &cppargs) {
  // Based on the algorithm proposed in H. A. J. Watson, M. Vikse, T. Gundersen,
  // and P. I. Barton, “Reliable Flash Calculations: Part 1. Nonsmooth
  // Inside-Out Algorithms,” Ind. Eng. Chem. Res., vol. 56, no. 4, pp. 960–973,
  // Feb. 2017, doi: 10.1021/acs.iecr.6b03956.
  int ncomp = x.size();
  double TOL = 1e-8;
  double MAXITER = 200;
  double x_ions = 0.;  // overall mole fraction of ions in the system
  for (int i = 0; i < ncomp; i++) {
    if (!cppargs.z.empty() && cppargs.z[i] != 0) {
      x_ions += x[i];
    }
  }
  // initialize variables
  vector<double> fugcoef_l(ncomp), fugcoef_v(ncomp), k(ncomp), u(ncomp),
      kprime(ncomp);
  double rhol, rhov;
  double Pref = p_guess - 0.01 * p_guess;
  double Pprime = p_guess + 0.01 * p_guess;
  if (p_guess > 1e6) {  // when close to the critical pressure then we need to
                        // have Pprime be less than p_guess
    Pprime = p_guess - 0.005 * p_guess;
  }
  double p = p_guess;
  // calculate initial guess for compositions based on fugacity coefficients and
  // Raoult's Law.
  rhol = pcsaft_den_cpp(t, p, x, 0, cppargs);
  rhov = pcsaft_den_cpp(t, p, x, 1, cppargs);
  if ((rhol - rhov) < 1e-4) {
    throw SolutionError("liquid and vapor densities are the same.");
  }
  fugcoef_l = pcsaft_fugcoef_cpp(t, rhol, x, cppargs);
  fugcoef_v = pcsaft_fugcoef_cpp(t, rhov, x, cppargs);
  for (int i = 0; i < ncomp; i++) {
    if (cppargs.z.empty() || cppargs.z[i] == 0) {
      k[i] = fugcoef_l[i] / fugcoef_v[i];
    } else {
      k[i] = 0;  // set k to 0 for ionic components
    }
  }
  vector<double> xl(ncomp);
  vector<double> xv(ncomp);
  double xv_sum = 0;
  double xl_sum = 0;
  for (int i = 0; i < ncomp; i++) {
    xl[i] = x[i] / (1 + Q * (k[i] - 1));
    xl_sum += xl[i];
    xv[i] = k[i] * x[i] / (1 + Q * (k[i] - 1));
    xv_sum += xv[i];
  }
  if (xv_sum != 1) {
    for (int i = 0; i < ncomp; i++) {
      xv[i] = xv[i] / xv_sum;
    }
  }
  if (xl_sum != 1) {
    for (int i = 0; i < ncomp; i++) {
      xl[i] = xl[i] / xl_sum;
    }
  }
  rhol = pcsaft_den_cpp(t, p, xl, 0, cppargs);
  fugcoef_l = pcsaft_fugcoef_cpp(t, rhol, xl, cppargs);
  rhov = pcsaft_den_cpp(t, p, xv, 1, cppargs);
  fugcoef_v = pcsaft_fugcoef_cpp(t, rhov, xv, cppargs);
  for (int i = 0; i < ncomp; i++) {
    k[i] = fugcoef_l[i] / fugcoef_v[i];
    u[i] = std::log(k[i] / kb);
  }
  rhol = pcsaft_den_cpp(t, Pprime, xl, 0, cppargs);
  fugcoef_l = pcsaft_fugcoef_cpp(t, rhol, xl, cppargs);
  rhov = pcsaft_den_cpp(t, Pprime, xv, 1, cppargs);
  fugcoef_v = pcsaft_fugcoef_cpp(t, rhov, xv, cppargs);
  for (int i = 0; i < ncomp; i++) {
    kprime[i] = fugcoef_l[i] / fugcoef_v[i];
  }
  vector<double> t_weight(ncomp);
  double t_sum = 0;
  for (int i = 0; i < ncomp; i++) {
    double dlnk_dt = (kprime[i] - k[i]) / (Pprime - p);
    t_weight[i] = xv[i] * dlnk_dt / (1 + Q * (k[i] - 1));
    t_sum += t_weight[i];
  }
  double kb = 0;
  for (int i = 0; i < ncomp; i++) {
    double wi = t_weight[i] / t_sum;
    if (cppargs.z.empty() || cppargs.z[i] == 0) {
      kb += wi * std::log(k[i]);
    }
  }
  kb = std::exp(kb);
  t_sum = 0;
  for (int i = 0; i < ncomp; i++) {
    double dlnk_dt = (kprime[i] - k[i]) / (Pprime - p);
    t_weight[i] = xv[i] * dlnk_dt / (1 + Q * (kprime[i] - 1));
    t_sum += t_weight[i];
  }
  double kbprime = 0;
  for (int i = 0; i < ncomp; i++) {
    double wi = t_weight[i] / t_sum;
    if (cppargs.z.empty() || cppargs.z[i] == 0) {
      kbprime += wi * std::log(kprime[i]);
    }
  }
  kbprime = std::exp(kbprime);
  double kb0 = kbprime;
  for (int i = 0; i < ncomp; i++) {
    u[i] = std::log(k[i] / kb);
  }
  double B = std::log(kbprime / kb) / (1 / Pprime - 1 / p);
  double A = std::log(kb) - B * (1 / p - 1 / Pref);
  if (B < 0) {
    throw SolutionError("B < 0 in outerTQ");
  }
  // solve
  vector<double> pp(ncomp);
  double maxdif = 1e10 * TOL;
  int itr = 0;
  double Rmin = 0, Rmax = 1;
  while (maxdif > TOL && itr < MAXITER) {
    // save previous values for calculating the difference at the end of the
    // iteration
    vector<double> u_old = u;
    double A_old = A;
    double R0 = kb * Q / (kb * Q + kb0 * (1 - Q));
    double R = BoundedSecantInner(kb0, Q, u, x, cppargs, R0, Rmin, Rmax,
                                  DBL_EPSILON, 1e-8, 200);
    double pp_sum = 0;
    double eupp_sum = 0;
    for (int i = 0; i < ncomp; i++) {
      pp[i] = x[i] / (1 - R + kb0 * R * std::exp(u[i]));
      if (cppargs.z.empty() || cppargs.z[i] == 0) {
        pp_sum += pp[i];
        eupp_sum += std::exp(u[i]) * pp[i];
      }
    }
    kb = pp_sum / eupp_sum;
    p = 1 / (1 / Pref + (std::log(kb) - A) / B);
    for (int i = 0; i < ncomp; i++) {
      if (x_ions == 0) {
        xl[i] = pp[i] / pp_sum;
        xv[i] = std::exp(u[i]) * pp[i] / eupp_sum;
      } else if (cppargs.z.empty() || cppargs.z[i] == 0) {
        xl[i] = pp[i] / pp_sum * (1 - x_ions / (1 - Q));
        xv[i] = std::exp(u[i]) * pp[i] / eupp_sum;
      } else {
        xl[i] = x[i] / (1 - Q);
        xv[i] = 0;
      }
    }
    rhol = pcsaft_den_cpp(t, p, xl, 0, cppargs);
    fugcoef_l = pcsaft_fugcoef_cpp(t, rhol, xl, cppargs);
    rhov = pcsaft_den_cpp(t, p, xv, 1, cppargs);
    fugcoef_v = pcsaft_fugcoef_cpp(t, rhov, xv, cppargs);
    for (int i = 0; i < ncomp; i++) {
      k[i] = fugcoef_l[i] / fugcoef_v[i];
      u[i] = std::log(k[i] / kb);
    }
    if (itr == 0) {
      B = std::log(kbprime / kb) / (1 / Pprime - 1 / p);
      if (B < 0) {
        throw SolutionError("B < 0 in outerTQ");
      }
    }
    A = std::log(kb) - B * (1 / p - 1 / Pref);
    maxdif = std::abs(A - A_old);
    for (int i = 0; i < ncomp; i++) {
      if (cppargs.z.empty() || cppargs.z[i] == 0) {
        double dif = std::abs(u[i] - u_old[i]);
        if (dif > maxdif) {
          maxdif = dif;
        } else if (!std::isfinite(dif)) {
          maxdif = dif;
        }
      }
    }
    itr += 1;
  }
  if (!std::isfinite(p) || !std::isfinite(maxdif) || maxdif > 0.1 || p < 0) {
    throw SolutionError("outerTQ did not converge to a solution");
  }
  vector<double> result;
  result.push_back(p);
  result.insert(result.end(), xl.begin(), xl.end());
  result.insert(result.end(), xv.begin(), xv.end());
  return result;
}
double resid_inner(double R, double kb0, double Q, vector<double> u,
                   vector<double> x, add_args &cppargs) {
  int ncomp = x.size();
  double error = 0;
  vector<double> pp(ncomp);
  double L = 0;
  for (int i = 0; i < ncomp; i++) {
    if (cppargs.z.empty() || cppargs.z[i] == 0) {
      pp[i] = x[i] / (1 - R + kb0 * R * exp(u[i]));
      L += pp[i];
    } else {
      L += x[i];
    }
  }
  L = (1 - R) * L;
  error = pow((L + Q - 1), 2.);
  return error;
}
double pcsaft_den_cpp(double t, double p, vector<double> x, int phase,
                      add_args &cppargs) {
  /**
  Solve for the molar density when temperature and pressure are given.
  Parameters
  ----------
  t : double
      Temperature (K)
  p : double
      Pressure (Pa)
  x : vector<double>, shape (n,)
      Mole fractions of each component. It has a length of n, where n is
      the number of components in the system.
  phase : int
      The phase for which the calculation is performed. Options: 0 (liquid),
      1 (vapor).
  cppargs : add_args
      A struct containing additional arguments that can be passed for
      use in PC-SAFT:
      m : vector<double>, shape (n,)
          Segment number for each component.
      s : vector<double>, shape (n,)
          Segment diameter for each component. For ions this is the diameter of
          the hydrated ion. Units of Angstrom.
      e : vector<double>, shape (n,)
          Dispersion energy of each component. For ions this is the dispersion
          energy of the hydrated ion. Units of K.
      k_ij : vector<double>, shape (n*n,)
          Binary interaction parameters between components in the mixture.
          (dimensions: ncomp x ncomp)
      e_assoc : vector<double>, shape (n,)
          Association energy of the associating components. For non associating
          compounds this is set to 0. Units of K.
      vol_a : vector<double>, shape (n,)
          Effective association volume of the associating components. For non
          associating compounds this is set to 0.
      dipm : vector<double>, shape (n,)
          Dipole moment of the polar components. For components where the dipole
          term is not used this is set to 0. Units of Debye.
      dip_num : vector<double>, shape (n,)
          The effective number of dipole functional groups on each component
          molecule. Some implementations use this as an adjustable parameter
          that is fit to data.
      z : vector<double>, shape (n,)
          Charge number of the ions
      dielc : double
          Dielectric constant of the medium to be used for electrolyte
          calculations.
  Returns
  -------
  rho : double
      Molar density (mol m^-3)
  */
  // split into grid and find bounds for each root
  int ncomp = x.size();  // number of components
  vector<double> x_lo, x_hi;
  int num_pts = 25;
  double err;
  double rho_guess = 1e-13;
  double rho_guess_prev = rho_guess;
  double err_prev = resid_rho(reduced_to_molar(rho_guess, t, ncomp, x, cppargs),
                              t, p, x, cppargs);
  for (int i = 0; i < num_pts; i++) {
    rho_guess = 0.7405 / (double)num_pts * i + 6e-3;
    err = resid_rho(reduced_to_molar(rho_guess, t, ncomp, x, cppargs), t, p, x,
                    cppargs);
    if (err * err_prev < 0) {
      x_lo.push_back(rho_guess_prev);
      x_hi.push_back(rho_guess);
    }
    err_prev = err;
    rho_guess_prev = rho_guess;
  }
  // solve for appropriate root(s)
  double rho = _HUGE;
  double x_lo_molar, x_hi_molar;
  if (x_lo.size() == 1) {
    rho_guess =
        reduced_to_molar((x_lo[0] + x_hi[0]) / 2., t, ncomp, x, cppargs);
    x_lo_molar = reduced_to_molar(x_lo[0], t, ncomp, x, cppargs);
    x_hi_molar = reduced_to_molar(x_hi[0], t, ncomp, x, cppargs);
    rho = BrentRho(t, p, x, phase, cppargs, x_lo_molar, x_hi_molar, DBL_EPSILON,
                   1e-8, 200);
  } else if (x_lo.size() <= 3 && !x_lo.empty()) {
    if (phase == 0) {
      rho_guess = reduced_to_molar((x_lo.back() + x_hi.back()) / 2., t, ncomp,
                                   x, cppargs);
      x_lo_molar = reduced_to_molar(x_lo.back(), t, ncomp, x, cppargs);
      x_hi_molar = reduced_to_molar(x_hi.back(), t, ncomp, x, cppargs);
      rho = BrentRho(t, p, x, phase, cppargs, x_lo_molar, x_hi_molar,
                     DBL_EPSILON, 1e-8, 200);
    } else if (phase == 1) {
      rho_guess = reduced_to_molar((x_lo[0] + x_hi[0]) / 40., t, ncomp, x,
                                   cppargs);  // starting with a lower guess
                                              // often provides better results
      x_lo_molar = reduced_to_molar(x_lo[0], t, ncomp, x, cppargs);
      x_hi_molar = reduced_to_molar(x_hi[0], t, ncomp, x, cppargs);
      rho = BrentRho(t, p, x, phase, cppargs, x_lo_molar, x_hi_molar,
                     DBL_EPSILON, 1e-8, 200);
    }
  } else if (x_lo.size() > 3) {
    // if multiple roots to check, then find the one with the minimum gibbs
    // energy. Reference: Privat R, Gani R, Jaubert JN. Are safe results
    // obtained when the PC-SAFT equation of state is applied to ordinary pure
    // chemicals?. Fluid Phase Equilibria. 2010 Aug 15;295(1):76-92.
    double g_min = 1e60;
    for (unsigned int i = 0; i < x_lo.size(); i++) {
      rho_guess =
          reduced_to_molar((x_lo[i] + x_hi[i]) / 2., t, ncomp, x, cppargs);
      x_lo_molar = reduced_to_molar(x_lo[i], t, ncomp, x, cppargs);
      x_hi_molar = reduced_to_molar(x_hi[i], t, ncomp, x, cppargs);
      double rho_i = BrentRho(t, p, x, phase, cppargs, x_lo_molar, x_hi_molar,
                              DBL_EPSILON, 1e-8, 200);
      double g_i = pcsaft_gres_cpp(t, rho_i, x, cppargs);
      if (g_i < g_min) {
        g_min = g_i;
        rho = rho_i;
      }
    }
  } else {
    int num_pts = 25;
    double err_min = 1e40;
    double rho_min = _HUGE;
    double err, rho_guess;
    for (int i = 0; i < num_pts; i++) {
      rho_guess = 0.7405 / (double)num_pts * i + 1e-8;
      err = resid_rho(reduced_to_molar(rho_guess, t, ncomp, x, cppargs), t, p,
                      x, cppargs);
      if (std::abs(err) < err_min) {
        err_min = std::abs(err);
        rho_min = reduced_to_molar(rho_guess, t, ncomp, x, cppargs);
      }
    }
    rho = rho_min;
  }
  return rho;
}
double estimate_flash_t(double p, double Q, vector<double> x,
                        add_args &cppargs) {
  /**
  Get a quick estimate of the temperature at which VLE occurs
  */
  double t_guess = _HUGE;
  int ncomp = x.size();
  double x_ions = 0.;  // overall mole fraction of ions in the system
  for (int i = 0; i < ncomp; i++) {
    if (!cppargs.z.empty() && cppargs.z[i] != 0) {
      x_ions += x[i];
    }
  }
  bool guess_found = false;
  double t_step = 30;
  double t_start = 400;
  double t_lbound = 1;
  if (!cppargs.z.empty()) {
    t_step = 15;
    t_start = 350;
    t_lbound = 264;
  }
  while (!guess_found && t_start > t_lbound) {
    // initialize variables
    double Tprime = t_start - 50;
    double t = t_start;
    // calculate sigma for water, if it is present
    std::vector<double>::iterator water_iter =
        std::find(cppargs.e.begin(), cppargs.e.end(), 353.9449);
    int water_idx = -1;
    if (water_iter != cppargs.e.end()) {
      water_idx = std::distance(cppargs.e.begin(), water_iter);
      cppargs.s[water_idx] = calc_sigma(t, &calc_water_sigma);
      cppargs.dielc =
          dielc_water(t);  // Right now only aqueous mixtures are supported for
                           // electrolyte PC-SAFT. Other solvents could be
                           // modeled by replacing the dielc_water function.
    }
    try {
      double p1 = estimate_flash_p(t, Q, x, cppargs);
      double p2 = estimate_flash_p(Tprime, Q, x, cppargs);
      double slope = (std::log10(p1) - std::log10(p2)) / (1 / t - 1 / Tprime);
      double intercept = std::log10(p1) - slope * (1 / t);
      t_guess = slope / (std::log10(p) - intercept);
      guess_found = true;
    } catch (const SolutionError &ex) {
      t_start -= t_step;
    }
  }
  if (!guess_found) {
    throw SolutionError(
        "an estimate for the VLE temperature could not be found");
  }
  return t_guess;
}
double estimate_flash_p(double t, double Q, vector<double> x,
                        add_args &cppargs) {
  /**
  Get a quick estimate of the pressure at which VLE occurs
  */
  double p_guess = _HUGE;
  int ncomp = x.size();
  double x_ions = 0.;  // overall mole fraction of ions in the system
  for (int i = 0; i < ncomp; i++) {
    if (!cppargs.z.empty() && cppargs.z[i] != 0) {
      x_ions += x[i];
    }
  }
  bool guess_found = false;
  double p_start = 10000;
  while (!guess_found && p_start < 1e7) {
    // initialize variables
    vector<double> fugcoef_l(ncomp), fugcoef_v(ncomp), k(ncomp), u(ncomp),
        kprime(ncomp);
    double rhol, rhov;
    double Pprime = 0.99 * p_start;
    double p = p_start;
    // calculate initial guess for compositions based on fugacity coefficients
    // and Raoult's Law.
    rhol = pcsaft_den_cpp(t, p, x, 0, cppargs);
    rhov = pcsaft_den_cpp(t, p, x, 1, cppargs);
    if ((rhol - rhov) < 1e-4) {
      p_start = p_start + 2e5;
      continue;
    }
    fugcoef_l = pcsaft_fugcoef_cpp(t, rhol, x, cppargs);
    fugcoef_v = pcsaft_fugcoef_cpp(t, rhov, x, cppargs);
    for (int i = 0; i < ncomp; i++) {
      if (cppargs.z.empty() || cppargs.z[i] == 0) {
        k[i] = fugcoef_l[i] / fugcoef_v[i];
      } else {
        k[i] = 0;  // set k to 0 for ionic components
      }
    }
    vector<double> xl(ncomp);
    vector<double> xv(ncomp);
    double xv_sum = 0;
    double xl_sum = 0;
    for (int i = 0; i < ncomp; i++) {
      xl[i] = x[i] / (1 + Q * (k[i] - 1));
      xl_sum += xl[i];
      xv[i] = k[i] * x[i] / (1 + Q * (k[i] - 1));
      xv_sum += xv[i];
    }
    if (xv_sum != 1) {
      for (int i = 0; i < ncomp; i++) {
        xv[i] = xv[i] / xv_sum;
      }
    }
    if (xl_sum != 1) {
      for (int i = 0; i < ncomp; i++) {
        xl[i] = xl[i] / xl_sum;
      }
    }
    rhol = pcsaft_den_cpp(t, p, xl, 0, cppargs);
    rhov = pcsaft_den_cpp(t, p, xv, 1, cppargs);
    if ((rhol - rhov) < 1e-4) {
      p_start = p_start + 2e5;
      continue;
    }
    fugcoef_l = pcsaft_fugcoef_cpp(t, rhol, xl, cppargs);
    fugcoef_v = pcsaft_fugcoef_cpp(t, rhov, xv, cppargs);
    double numer = 0;
    double denom = 0;
    for (int i = 0; i < ncomp; i++) {
      if (cppargs.z.empty() || cppargs.z[i] == 0) {
        numer += xl[i] * fugcoef_l[i];
        denom += xv[i] * fugcoef_v[i];
      }
    }
    double ratio = numer / denom;
    rhol = pcsaft_den_cpp(t, Pprime, xl, 0, cppargs);
    rhov = pcsaft_den_cpp(t, Pprime, xv, 1, cppargs);
    if ((rhol - rhov) < 1e-4) {
      p_start = p_start + 2e5;
      continue;
    }
    fugcoef_l = pcsaft_fugcoef_cpp(t, rhol, xl, cppargs);
    fugcoef_v = pcsaft_fugcoef_cpp(t, rhov, xv, cppargs);
    numer = 0;
    denom = 0;
    for (int i = 0; i < ncomp; i++) {
      if (cppargs.z.empty() || cppargs.z[i] == 0) {
        numer += xl[i] * fugcoef_l[i];
        denom += xv[i] * fugcoef_v[i];
      }
    }
    double ratio_prime = numer / denom;
    double slope = (std::log10(ratio) - std::log10(ratio_prime)) /
                   (std::log10(p) - std::log10(Pprime));
    double intercept = std::log10(ratio) - slope * std::log10(p);
    p_guess = pow(10, -intercept / slope);
    guess_found = true;
  }
  if (!guess_found) {
    throw SolutionError("an estimate for the VLE pressure could not be found");
  }
  return p_guess;
}
double reduced_to_molar(double nu, double t, int ncomp, vector<double> x,
                        add_args &cppargs) {
  vector<double> d(ncomp);
  double summ = 0.;
  for (int i = 0; i < ncomp; i++) {
    d[i] = cppargs.s[i] * (1 - 0.12 * std::exp(-3 * cppargs.e[i] / t));
    summ += x[i] * cppargs.m[i] * pow(d[i], 3.);
  }
  return 6 / PI * nu / summ * 1.0e30 / N_AV;
}
double dielc_water(double t) {
  /**
  Return the dielectric constant of water at the given temperature.
  t : double
      Temperature (K)
  This equation was fit to values given in the reference. For temperatures
  from 263.15 to 368.15 K values at 1 bar were used. For temperatures from
  368.15 to 443.15 K values at 10 bar were used.
  Reference:
  D. G. Archer and P. Wang, “The Dielectric Constant of Water and Debye‐Hückel
  Limiting Law Slopes,” J. Phys. Chem. Ref. Data, vol. 19, no. 2, pp. 371–411,
  Mar. 1990.
  */
  double dielc;
  if (t < 263.15) {
    throw ValueError(
        "The current function for the dielectric constant for water is only "
        "valid for temperatures above 263.15 K.");
  } else if (t <= 368.15) {
    dielc = 7.6555618295E-04 * t * t - 8.1783881423E-01 * t + 2.5419616803E+02;
  } else if (t <= 443.15) {
    dielc = 0.0005003272124 * t * t - 0.6285556029 * t + 220.4467027;
  } else {
    throw ValueError(
        "The current function for the dielectric constant for water is only "
        "valid for temperatures less than 443.15 K.");
  }
  return dielc;
}
double calc_water_sigma(double t) {
  return 3.8395 + 1.2828 * std::exp(-0.0074944 * t) -
         1.3939 * std::exp(-0.00056029 * t);
}
add_args get_single_component(int i, add_args &cppargs) {
  add_args args_single;
  args_single.m.push_back(cppargs.m[i]);
  args_single.s.push_back(cppargs.s[i]);
  args_single.e.push_back(cppargs.e[i]);
  if (!cppargs.e_assoc.empty()) {
    args_single.e_assoc.push_back(cppargs.e_assoc[i]);
    args_single.vol_a.push_back(cppargs.vol_a[i]);
  }
  if (!cppargs.dipm.empty()) {
    args_single.dipm.push_back(cppargs.dipm[i]);
    args_single.dip_num.push_back(cppargs.dip_num[i]);
  }
  if (!cppargs.z.empty()) {
    args_single.z.push_back(cppargs.z[i]);
    args_single.dielc = cppargs.dielc;
  }
  if (!cppargs.assoc_num.empty()) {
    args_single.assoc_num.push_back(cppargs.assoc_num[i]);
    if (args_single.assoc_num[0] > 0) {
      int nassoc = cppargs.assoc_num.size();
      int start = 0;
      for (int l = 0; l < (int)cppargs.assoc_num.size(); l++) {
        if (l < i) {
          start += 1;
        }
      }
      for (int j = 0; j < nassoc; j++) {
        for (int k = 0; k < args_single.assoc_num[0]; k++) {
          args_single.assoc_matrix.push_back(
              cppargs.assoc_matrix[j * nassoc + start + k]);
        }
      }
    }
  }
  return args_single;
}
/*
----------------------------------------------------------------------------------------------------------------------
The code for the solvers was taken from CoolProp
(https://github.com/CoolProp/CoolProp) and somewhat modified.
*/
/**
This function implements a 1-D bounded solver using the algorithm from Brent, R.
P., Algorithms for Minimization Without Derivatives. Englewood Cliffs, NJ:
Prentice-Hall, 1973. Ch. 3-4.
a and b must bound the solution of interest and f(a) and f(b) must have opposite
signs.  If the function is continuous, there must be at least one solution in
the interval [a,b].
@param a The minimum bound for the solution of f=0
@param b The maximum bound for the solution of f=0
@param macheps The machine precision
@param tol_abs Tolerance (absolute)
@param maxiter Maximum number of steps allowed.  Will throw a SolutionError if
the solution cannot be found
*/
double BrentRho(double t, double p, vector<double> x, int phase,
                add_args &cppargs, double a, double b, double macheps,
                double tol_abs, int maxiter) {
  int iter;
  double fa, fb, c, fc, m, tol, d, e, pp, q, s, r;
  fa = resid_rho(a, t, p, x, cppargs);
  fb = resid_rho(b, t, p, x, cppargs);
  // If one of the boundaries is to within tolerance, just stop
  if (std::abs(fb) < tol_abs) {
    return b;
  }
  if (std::isnan(fb)) {
    throw ValueError("BrentRho's method f(b) is NAN for b");
  }
  if (std::abs(fa) < tol_abs) {
    return a;
  }
  if (std::isnan(fa)) {
    throw ValueError("BrentRho's method f(a) is NAN for a");
  }
  if (fa * fb > 0) {
    throw ValueError("Inputs in BrentRho do not bracket the root");
  }
  c = a;
  fc = fa;
  iter = 1;
  if (std::abs(fc) < std::abs(fb)) {
    // Goto ext: from BrentRho ALGOL code
    a = b;
    b = c;
    c = a;
    fa = fb;
    fb = fc;
    fc = fa;
  }
  d = b - a;
  e = b - a;
  m = 0.5 * (c - b);
  tol = 2 * macheps * std::abs(b) + tol_abs;
  while (std::abs(m) > tol && fb != 0) {
    // See if a bisection is forced
    if (std::abs(e) < tol || std::abs(fa) <= std::abs(fb)) {
      m = 0.5 * (c - b);
      d = e = m;
    } else {
      s = fb / fa;
      if (a == c) {
        // Linear interpolation
        pp = 2 * m * s;
        q = 1 - s;
      } else {
        // Inverse quadratic interpolation
        q = fa / fc;
        r = fb / fc;
        m = 0.5 * (c - b);
        pp = s * (2 * m * q * (q - r) - (b - a) * (r - 1));
        q = (q - 1) * (r - 1) * (s - 1);
      }
      if (pp > 0) {
        q = -q;
      } else {
        pp = -pp;
      }
      s = e;
      e = d;
      m = 0.5 * (c - b);
      if (2 * pp < 3 * m * q - std::abs(tol * q) ||
          pp < std::abs(0.5 * s * q)) {
        d = pp / q;
      } else {
        m = 0.5 * (c - b);
        d = e = m;
      }
    }
    a = b;
    fa = fb;
    if (std::abs(d) > tol) {
      b += d;
    } else if (m > 0) {
      b += tol;
    } else {
      b += -tol;
    }
    fb = resid_rho(b, t, p, x, cppargs);
    if (std::isnan(fb)) {
      throw ValueError("BrentRho's method f(t) is NAN for t");
    }
    if (std::abs(fb) < macheps) {
      return b;
    }
    if (fb * fc > 0) {
      c = a;
      fc = fa;
      d = e = b - a;
    }
    if (std::abs(fc) < std::abs(fb)) {
      a = b;
      b = c;
      c = a;
      fa = fb;
      fb = fc;
      fc = fa;
    }
    m = 0.5 * (c - b);
    tol = 2 * macheps * std::abs(b) + tol_abs;
    iter += 1;
    if (std::isnan(a)) {
      throw ValueError("BrentRho's method a is NAN");
    }
    if (std::isnan(b)) {
      throw ValueError("BrentRho's method b is NAN");
    }
    if (std::isnan(c)) {
      throw ValueError("BrentRho's method c is NAN");
    }
    if (iter > maxiter) {
      throw SolutionError("BrentRho's method reached maximum number of steps");
    }
    if (std::abs(fb) < 2 * macheps * std::abs(b)) {
      return b;
    }
  }
  return b;
}
double resid_rho(double rhomolar, double t, double p, vector<double> x,
                 add_args &cppargs) {
  double peos = pcsaft_p_cpp(t, rhomolar, x, cppargs);
  double cost = (peos - p) / p;
  if (std::isfinite(cost)) {
    return cost;
  } else {
    return _HUGE;
  }
}
/**
In the secant function, a 1-D Newton-Raphson solver is implemented.  An initial
guess for the solution is provided.
@param x0 The initial guess for the solution
@param xmax The upper bound for the solution
@param xmin The lower bound for the solution
@param dx The initial amount that is added to x in order to build the numerical
derivative
@param tol The absolute value of the tolerance accepted for the objective
function
@param maxiter Maximum number of iterations
@returns If no errors are found, the solution, otherwise the value _HUGE, the
value for infinity
*/
double BoundedSecantInner(double kb0, double Q, vector<double> u,
                          vector<double> x, add_args &cppargs, double x0,
                          double xmin, double xmax, double dx, double tol,
                          int maxiter) {
  double x1 = 0, x2 = 0, x3 = 0, y1 = 0, y2 = 0, R, fval = 999;
  int iter = 1;
  if (std::abs(dx) == 0) {
    throw ValueError("dx cannot be zero");
  }
  while (std::abs(fval) > tol) {
    if (iter == 1) {
      x1 = x0;
      R = x1;
      x3 = R;
    } else if (iter == 2) {
      x2 = x0 + dx;
      R = x2;
      x3 = R;
    } else {
      R = x2;
    }
    fval = resid_inner(R, kb0, Q, u, x, cppargs);
    if (iter == 1) {
      y1 = fval;
    } else {
      if (std::isfinite(fval)) {
        y2 = fval;
      } else {
        y2 = 1e40;
      }
      x3 = x2 - y2 / (y2 - y1) * (x2 - x1);
      // Check bounds, go half the way to the limit if limit is exceeded
      if (x3 < xmin) {
        x3 = (xmin + x2) / 2;
      }
      if (x3 > xmax) {
        x3 = (xmax + x2) / 2;
      }
      y1 = y2;
      x1 = x2;
      x2 = x3;
    }
    if (iter > maxiter) {
      throw SolutionError("BoundedSecant reached maximum number of iterations");
    }
    iter = iter + 1;
  }
  return x3;
}
