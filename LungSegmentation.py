import numpy as np
from scipy import ndimage

def LungSegmentation(Img, init_mask, max_its, alpha):
    I = Img.astype(float)
    phi = mask2phi(init_mask)   #Mengubah Mask to Phi (Menggunakan menggunakan metode bwdist)

    for its in range(max_its):
        # print('loop:', its)
        idx = np.where((phi <= 3.0) & (phi >= -3.0))
        idx = list(zip(idx[1], idx[0]))
        idx_size = list(np.shape(idx))[0]

        upts = np.where(phi < 0.0)
        upts = list(zip(upts[0], upts[1]))

        vpts = np.where(phi > 0)
        vpts = list(zip(vpts[0], vpts[1]))

        sum_u = 0
        sum_v = 0

        for i in upts:
            sum_u += (I[i])

        for i in vpts:
            sum_v += (I[i])

        u = (sum_u / (len(upts) + np.spacing(1)))
        v = (sum_v / (len(vpts) + np.spacing(1)))

        F = np.zeros(np.shape(I))
        for i in range(idx_size):
            x = idx[i][0]
            y = idx[i][1]
            F[y][x] = ((I[y, x] - u) ** 2) - ((I[y, x] - v) ** 2)

        curvature = get_curvature(phi, idx, idx_size)

        dphidt = np.zeros(np.shape(I))
        for i in range(idx_size):
            x = idx[i][0]
            y = idx[i][1]
            dphidt[y][x] = F[y][x] / np.amax(np.abs(F)) + alpha * curvature[y][x]

        dt = 0.45 / np.amax(dphidt) + np.spacing(1)

        for i in range(idx_size):
            x = idx[i][0]
            y = idx[i][1]
            phi[y][x] = phi[y][x] + dt * dphidt[y][x]

        phi = sussman(phi, 0.5)

    seg = np.where(phi <= 0, 255, 0)
    return seg

# converts a mask to a SDF
def mask2phi(init_a):
    def bwdist(M):
        res = ndimage.distance_transform_edt(1 - M)
        return res

    def im2double(im):
        min_val = np.min(im.ravel())
        max_val = np.max(im.ravel())
        out = (im.astype('float') - min_val) / (max_val - min_val)
        return out

    phi = bwdist(init_a)-bwdist(1-init_a)+im2double(init_a)-0.5
    return phi

# compute curvature along SDF
def get_curvature(phi, idx, idx_size):
    curvature = np.zeros(np.shape(phi))
    for i in range(idx_size):
        x = idx[i][0]
        y = idx[i][1]

        phi_x = (phi[y, x + 1]) - (phi[y, x - 1])
        phi_y = (phi[y + 1, x]) - (phi[y - 1, x])
        phi_xx = (phi[y, x - 1]) - 2 * (phi[y, x]) + (phi[y, x + 1])
        phi_yy = (phi[y - 1, x]) - 2 * (phi[y, x]) + (phi[y + 1, x])
        phi_xy = (-(phi[y - 1, x - 1]) - (phi[y + 1, x + 1]) + (phi[y - 1, x + 1]) + (phi[y + 1, x - 1])) / 4
        phi_x2 = phi_x ** 2
        phi_y2 = phi_y ** 2

        curvature[y][x] = (phi_x2 * phi_yy + phi_y2 * phi_xx - 2 * phi_x * phi_y * phi_xy) / \
                          np.power((phi_x2 + phi_y2 + np.spacing(1)), 3 / 2)

    return curvature

# Derivative
def shiftR(M):
    ls = list(range(0, np.size(M[1]) - 1))
    ls.insert(0, 0)
    shift = np.array(M[:, ls])
    return shift


def shiftL(M):
    ls = list(range(1, np.size(M[1])))
    ls.append(np.size(M[1]) - 1)
    shift = np.array(M[:, ls])
    return shift


def shiftD(M):
    ls = list(range(0, np.size(M[1]) - 1))
    ls.insert(0, 0)
    shift = np.array(M[ls, :])
    return shift


def shiftU(M):
    ls = list(range(1, np.size(M[1])))
    ls.append(np.size(M[1]) - 1)
    shift = np.array(M[ls, :])
    return shift


def sussman_sign(D):
    s = D / (np.sqrt(np.power(D, 2) + 1))
    return s

# Level set re-initialization by the sussman methood
def sussman(D, dt):
    a = D - shiftR(D)  # backward
    b = shiftL(D) - D  # forward
    c = D - shiftD(D)  # backward
    d = shiftU(D) - D  # forward

    a_p = np.where(a < 0, 0, a)
    a_n = np.where(a > 0, 0, a)

    b_p = np.where(b < 0, 0, b)
    b_n = np.where(b > 0, 0, b)

    c_p = np.where(c < 0, 0, c)
    c_n = np.where(c > 0, 0, c)

    d_p = np.where(d < 0, 0, d)
    d_n = np.where(d > 0, 0, d)

    dD = np.zeros(shape=D.shape)
    D_neg_ind = np.where(D < 0)
    D_neg_ind = list(zip(D_neg_ind[1], D_neg_ind[0]))
    D_neg_ind_size = list(np.shape(D_neg_ind))[0]

    D_pos_ind = np.where(D > 0)
    D_pos_ind = list(zip(D_pos_ind[1], D_pos_ind[0]))
    D_pos_ind_size = list(np.shape(D_pos_ind))[0]

    for i in range(D_pos_ind_size):
        x = D_pos_ind[i][0]
        y = D_pos_ind[i][1]

        dD[y][x] = np.sqrt(np.maximum(np.power(a_p[y, x], 2), np.power(b_n[y, x], 2)) +
                          np.maximum(np.power(c_p[y, x], 2), np.power(d_n[y, x], 2))) - 1

    for i in range(D_neg_ind_size):
        x = D_neg_ind[i][0]
        y = D_neg_ind[i][1]
        dD[y][x] = np.sqrt(np.maximum(np.power(a_n[y, x], 2), np.power(b_p[y, x], 2)) +
                          np.maximum(np.power(c_n[y, x], 2), np.power(d_p[y, x], 2))) - 1

    D = D - dt * sussman_sign(D) * dD
    return D