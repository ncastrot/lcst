#########################################################################
# to obtain the results by fitting an exponential relationship between  #
# the pwv and the infrared sky temperature                              #
#########################################################################

import numpy as np
import matplotlib
matplotlib.use('qt5Agg')
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import pearsonr
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

dtype1 = [('date', 'U10'), ('hour', 'U8'), ('pwv', float), ('hum', float), ('press', float), ('temp', float)]
dtype2 = [('date', 'U10'), ('hour', 'U8'), ('bcc', float), ('bba1', float), ('bba2', float), ('lux', float), ('lux_white', float), ('uva', float), ('uvb', float), ('t1', float), ('t2', float), ('t3', float), ('t4', float), ('t5', float), ('t6', float), ('t7', float), ('t8', float), ('t9', float), ('t10', float), ('t11', float), ('t12', float), ('t13', float), ('t14', float), ('t15', float), ('t16', float), ('t17', float), ('t18', float), ('t19', float), ('t20', float), ('temp', float), ('press', float), ('hum', float)]

# open the files with the data
apex_bcc = np.loadtxt('/path/to/the/file/apex_bcc.txt', delimiter=',', dtype=dtype1)
apex_bba = np.loadtxt('/path/to/the/file/apex_bba.txt', delimiter=',', dtype=dtype1)
lcst_bcc = np.loadtxt('/path/to/the/file/lcst_bcc.txt', delimiter=',', dtype=dtype2)
lcst_bba = np.loadtxt('/path/to/the/file/lcst_bba.txt', delimiter=',', dtype=dtype2)

# lcst data are multiplied by 100, so to obtain °C, we divide those values
bcc,bba1,bba2 = lcst_bcc['bcc']/100, lcst_bba['bba1']/100, lcst_bba['bba2']/100
pwv_bcc, pwv_bba = apex_bcc['pwv'], apex_bba['pwv']

# this will be the exponential relationship
def expon(x,a,b,c,d):
    return a*np.exp((x+b)/c) + d

# to fit a linear regression in the predicted values, to obtain some metrics
def linear(x,m,b):
    return m*x + b

# this metrics will help us to to quantify the results
def metrics(y_t, y_p1):
    pr1,_ = pearsonr(y_t, y_p1)
    r21   = r2_score(y_t, y_p1)
    rmse1 = np.sqrt(mean_squared_error(y_t, y_p1))
    mae1  = mean_absolute_error(y_t, y_p1)
    std1  = np.std(y_p1)

    exp   = np.array([pr1,r21,rmse1,mae1,std1])
    return exp

# choose the bcc or bba sensor: there are differents times for those measurements
sensor=str(input("Choose a sensor: bcc or bba\n"))

# step input will help us to divide the total array of temperatures into smallest arrays: we can set errors for those measurements based on their standard deviation
step_input = float(input("Number of steps for errors: \n"))


# for the bcc we have to open the "mask1" file, or in this case, the "apex_bcc" and "lcst_bcc"
if sensor == 'bcc':
    # we fit the exponential fit to the data, and then we predict the pwv according to that equation
    opt_exp,_ = curve_fit(expon, bcc, pwv_bcc, p0=[28,33,4.8,0.2])
    a,b,c,d = opt_exp
    pred_exp = expon(bcc,a,b,c,d)

    # we fit a linear relationship on the predicted pwv and the real pwv (from apex)
    fit_pred_exp, _= curve_fit(linear, pwv_bcc, pred_exp)
    m1,b1 = fit_pred_exp

    # we calculate the metrics: pearson, r2, rmse, mae and std
    metric = metrics(pwv_bcc, pred_exp)

    # calculate the residuals between the true pwv and the predicted pwv. then we apply the step to calculate the error bars
    residuals = pwv_bcc - pred_exp
    step = (max(bcc) - min(bcc)) / step_input
    bins = np.arange(min(bcc), max(bcc) + step, step)

    # to calculate the errors per group, we will calculate the std in that group and the median value of real pwv, to have: σ = std/median
    std_per_group, median_per_group = [], []
    for i in range(len(bins) - 1):
        group_mask = (bcc >= bins[i]) & (bcc < bins[i + 1])
        group_residuals = residuals[group_mask]
        group_pwv = pwv_bcc[group_mask]

        group_std = np.std(group_residuals)
        group_median = np.median(group_pwv)

        std_per_group.append(group_std)
        median_per_group.append(group_median)

    std_group, median_group = np.array(std_per_group), np.array(median_per_group)
    stds = std_group / median_group
    print(50*'-')
    print("Standard Deviation per group: \n", std_group)
    print("Median of pwv per group: \n", median_group)
    print("Error = std/median: \n", stds)


    # here we make some plots; the sky temperature vs pwv, the exponential fit, the residuals and the errors bars associated to each group
    x=np.linspace(min(pwv_bcc)-2, max(pwv_bcc)+2, len(pwv_bcc))
    fig, (ax1,ax2) = plt.subplots(2,1, figsize=(18,16), sharex=True, gridspec_kw={'height_ratios':[4,1], 'hspace':0})

    ax1.plot(bcc, pwv_bcc, 'b.', alpha=0.3)
    ax1.plot(np.sort(bcc), expon(np.sort(bcc),a,b,c,d), 'r-', lw=2, alpha=0.7, label='Exponential Fit')

    for i in np.arange((2*min(bcc)+step)/2, (max(bcc)), step):
        bin_index = np.digitize(i, bins) - 1
        if 0 <= bin_index < len(stds):
            ax1.errorbar(i, expon(i, a, b, c, d), yerr=stds[bin_index], color='red', fmt='x', ecolor='black', capsize=7, lw=4)
            ax1.text(i-0.33, 0, f"$\\sigma$={stds[bin_index]:.3f}", fontsize=10)
    for i in np.arange(min(bcc), max(bcc)+1, step):
        ax1.vlines(i,-0.3,0.1, color='blue', linestyle='--')

    ax1.text(min(bcc), 2.3, f"r={metric[0]:.4f}")
    ax1.text(min(bcc), 2.2, f"R2={metric[1]:.4f}")
    ax1.text(min(bcc), 2.1, f"RMSE={metric[2]:.4f}")
    ax1.text(min(bcc), 2.0, f"MAE={metric[3]:.4f}")
    ax1.text(min(bcc), 1.9, f"Std={metric[4]:.4f}")

    ax1.set_xlabel("CePIA Sky Temperature [°C]", fontsize=20)
    ax1.set_ylabel("APEX PWV [mm]", fontsize=20)
    ax2.set_xlim(min(bcc)-0.5,max(bcc)+0.5)
    ax1.set_ylim(-0.1,2.75)
    ax1.legend(fontsize=16)

    ax2.plot(bcc, pwv_bcc - pred_exp, 'k.', alpha=0.5)
    ax2.hlines(0,-70,-40, color='red', linestyle='--', alpha=1)
    for i in np.arange(min(bcc), max(bcc)+1, step):
        ax2.vlines(i,-2,2, color='blue', linestyle='--')
    ax2.set_ylabel("Residuals [mm]", fontsize=16)
    ax2.set_xlabel("CePIA Sky Temperature [°C]", fontsize=20)
    ax2.set_xlim(min(bcc)-0.5,max(bcc)+0.5)
    ax2.set_ylim(min(pwv_bcc-pred_exp)-0.1,max(pwv_bcc-pred_exp)+0.1)


    # here we plot the prediction vs the real pwv, expecting a linear relationship between them, the residuals between them, the linear fit, the error bars and the metrics
    x=np.linspace(min(pwv_bcc)-2, max(pwv_bcc)+2, len(pwv_bcc))
    fig, (ax1,ax2) = plt.subplots(2,1, figsize=(18,16), sharex=True, gridspec_kw={'height_ratios':[4,1], 'hspace':0})

    ax1.plot(pwv_bcc, pred_exp, 'b.', alpha=0.3)
    ax1.plot(x,x,'k--', alpha=0.5, label='Ratio 1:1')
    ax1.plot(x,x*m1 + b1, 'r-', label=f"m={m1:.4f} \n$\\sigma$ ={np.std(pred_exp):.4f}")
    ax1.set_ylabel("CePIA PWV [mm]", fontsize=20)
    ax1.set_xlabel("APEX PWV [mm]", fontsize=20)
    ax1.set_xlim(min(pwv_bcc)-0.1,max(pwv_bcc)+0.1)
    ax1.set_ylim(min(pwv_bcc)-0.1,max(pwv_bcc)+0.1)
    ax1.legend(fontsize=16)

    for i in np.arange((2*min(bcc)+step)/2, (max(bcc)), step):
        bin_index = np.digitize(i, bins) - 1
        if 0 <= bin_index < len(stds):
            ax1.errorbar(expon(i,a,b,c,d), expon(i,a,b,c,d)*m1 + b1, yerr=stds[bin_index], color='red', fmt='x', ecolor='black', capsize=7, lw=4)


    ax1.text(min(pwv_bcc), 1.7, f"r={metric[0]:.4f}")
    ax1.text(min(pwv_bcc), 1.6, f"R2={metric[1]:.4f}")
    ax1.text(min(pwv_bcc), 1.5, f"RMSE={metric[2]:.4f}")
    ax1.text(min(pwv_bcc), 1.4, f"MAE={metric[3]:.4f}")
    ax1.text(min(pwv_bcc), 1.3, f"Std={metric[4]:.4f}")

    ax2.plot(pwv_bcc, pwv_bcc - pred_exp, 'k.', alpha=0.5)
    ax2.hlines(0,0,3, color='red', linestyle='--', alpha=1)
    ax2.set_ylabel("Residuals [mm]", fontsize=16)
    ax2.set_xlabel("APEX PWV [mm]", fontsize=20)
    ax2.set_xlim(min(pwv_bcc)-0.1,max(pwv_bcc)+0.1)
    ax2.set_ylim(min(pwv_bcc-pred_exp)-0.1,max(pwv_bcc-pred_exp)+0.1)

    plt.show()


# for the bba we have to open the "mask2" file, or in this case, the "apex_bba" and "lcst_bba". we have two sensors: bba1 and bba2, so we make the same twice
if sensor == 'bba':
    # we fit the exponential fit to the data, and then we predict the pwv according to that equation
    opt_exp,_ = curve_fit(expon, bba1, pwv_bba, p0=[28,33,4.8,0.2])
    a,b,c,d = opt_exp
    pred_exp = expon(bba1,a,b,c,d)

    # we fit a linear relationship on the predicted pwv and the real pwv (from apex)
    fit_pred_exp, _= curve_fit(linear, pwv_bba, pred_exp)
    m1,b1 = fit_pred_exp

    # we calculate the metrics: pearson, r2, rmse, mae and std
    metric = metrics(pwv_bba, pred_exp)

    # calculate the residuals between the true pwv and the predicted pwv. then we apply the step to calculate the error bars
    residuals = pwv_bba - pred_exp
    step = (max(bba1) - min(bba1)) / step_input
    bins = np.arange(min(bba1), max(bba1) + step, step)

    # to calculate the errors per group, we will calculate the std in that group and the median value of real pwv, to have: σ = std/median
    std_per_group, median_per_group = [], []
    for i in range(len(bins) - 1):
        group_mask = (bba1 >= bins[i]) & (bba1 < bins[i + 1])
        group_residuals = residuals[group_mask]
        group_pwv = pwv_bba[group_mask]

        group_std = np.std(group_residuals)
        group_median = np.median(group_pwv)

        std_per_group.append(group_std)
        median_per_group.append(group_median)

    std_group, median_group = np.array(std_per_group), np.array(median_per_group)
    stds = std_group / median_group
    print(50*'-')
    print("Standard Deviation per group: \n", std_group)
    print("Median of pwv per group: \n", median_group)
    print("Error = std/median: \n", stds)


    # here we make some plots; same as for the bcc sensor
    x=np.linspace(min(pwv_bba)-2, max(pwv_bba)+2, len(pwv_bba))
    fig, (ax1,ax2) = plt.subplots(2,1, figsize=(18,16), sharex=True, gridspec_kw={'height_ratios':[4,1], 'hspace':0})

    ax1.plot(bba1, pwv_bba, 'b.', alpha=0.3)
    ax1.plot(np.sort(bba1), expon(np.sort(bba1),a,b,c,d), 'r-', lw=2, alpha=0.7, label='Exponential Fit')

    for i in np.arange((2*min(bba1)+step)/2, (max(bba1)), step):
        bin_index = np.digitize(i, bins) - 1
        if 0 <= bin_index < len(stds):
            ax1.errorbar(i, expon(i, a, b, c, d), yerr=stds[bin_index], color='red', fmt='x', ecolor='black', capsize=7, lw=4)
            ax1.text(i-0.33, 0, f"$\\sigma$={stds[bin_index]:.3f}", fontsize=10)
    for i in np.arange(min(bba1), max(bba1)+1, step):
        ax1.vlines(i,-0.3,0.1, color='blue', linestyle='--')

    ax1.set_xlabel("CePIA Sky Temperature [°C]", fontsize=20)
    ax1.set_ylabel("APEX PWV [mm]", fontsize=20)
    ax1.set_xlim(min(bba1)-0.5,max(bba1)+0.5)
    ax1.set_ylim(-0.1,2.75)
    ax1.legend(fontsize=16)


    ax2.plot(bba1, pwv_bba - pred_exp, 'k.', alpha=0.5)
    ax2.hlines(0,-70,-40, color='red', linestyle='--', alpha=1)
    for i in np.arange(min(bba1), max(bba1)+1, step):
        ax2.vlines(i,-2,2, color='blue', linestyle='--')
    ax2.set_ylabel("Residuals [mm]", fontsize=16)
    ax2.set_xlabel("CePIA Sky Temperature [°C]", fontsize=20)
    ax2.set_xlim(min(bba1)-0.5,max(bba1)+0.5)
    ax2.set_ylim(min(pwv_bba-pred_exp)-0.1,max(pwv_bba-pred_exp)+0.1)


    x=np.linspace(min(pwv_bba)-2, max(pwv_bba)+2, len(pwv_bba))
    fig, (ax1,ax2) = plt.subplots(2,1, figsize=(18,16), sharex=True, gridspec_kw={'height_ratios':[4,1], 'hspace':0})

    ax1.plot(pwv_bba, pred_exp, 'b.', alpha=0.3)
    ax1.plot(x,x,'k--', alpha=0.5, label='Ratio 1:1')
    ax1.plot(x,x*m1 + b1, 'r-', label=f"m={m1:.4f} \n$\\sigma$ ={np.std(pred_exp):.4f}")

    for i in np.arange((2*min(bba1)+step)/2, (max(bba1)), step):
        bin_index = np.digitize(i, bins) - 1
        if 0 <= bin_index < len(stds):
            ax1.errorbar(expon(i,a,b,c,d), expon(i,a,b,c,d)*m1 + b1, yerr=stds[bin_index], color='red', fmt='x', ecolor='black', capsize=7, lw=4)

    ax1.text(min(pwv_bba), 1.7, f"r={metric[0]:.4f}")
    ax1.text(min(pwv_bba), 1.6, f"R2={metric[1]:.4f}")
    ax1.text(min(pwv_bba), 1.5, f"RMSE={metric[2]:.4f}")
    ax1.text(min(pwv_bba), 1.4, f"MAE={metric[3]:.4f}")
    ax1.text(min(pwv_bba), 1.3, f"Std={metric[4]:.4f}")

    ax1.set_ylabel("CePIA PWV [mm]", fontsize=20)
    ax1.set_xlabel("APEX PWV [mm]", fontsize=20)
    ax1.set_xlim(min(pwv_bba)-0.1,max(pwv_bba)+0.1)
    ax1.set_ylim(min(pwv_bba)-0.1,max(pwv_bba)+0.1)
    ax1.legend(fontsize=16)

    ax2.plot(pwv_bba, pwv_bba - pred_exp, 'k.', alpha=0.5)
    ax2.hlines(0,0,3, color='red', linestyle='--', alpha=1)
    ax2.set_ylabel("Residuals [mm]", fontsize=16)
    ax2.set_xlabel("APEX PWV [mm]", fontsize=20)
    ax2.set_xlim(min(pwv_bba)-0.1,max(pwv_bba)+0.1)
    ax2.set_ylim(min(pwv_bba-pred_exp)-0.1,max(pwv_bba-pred_exp)+0.1)

    plt.show()


    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    # here we make exactly the same, but for the bba2 sensor

    opt_exp,_ = curve_fit(expon, bba2, pwv_bba, p0=[28,33,4.8,0.2])
    a,b,c,d = opt_exp
    pred_exp = expon(bba2,a,b,c,d)

    fit_pred_exp, _= curve_fit(linear, pwv_bba, pred_exp)
    m1,b1 = fit_pred_exp

    metric = metrics(pwv_bba, pred_exp)

    residuals = pwv_bba - pred_exp
    step = (max(bba2) - min(bba2)) / step_input
    bins = np.arange(min(bba2), max(bba2) + step, step)

    std_per_group, median_per_group = [], []
    for i in range(len(bins) - 1):
        group_mask = (bba2 >= bins[i]) & (bba2 < bins[i + 1])
        group_residuals = residuals[group_mask]
        group_pwv = pwv_bba[group_mask]

        group_std = np.std(group_residuals)
        group_median = np.median(group_pwv)

        std_per_group.append(group_std)
        median_per_group.append(group_median)

    std_group, median_group = np.array(std_per_group), np.array(median_per_group)
    stds = std_group / median_group
    print(50*'-')
    print("Standard Deviation per group: \n", std_group)
    print("Median of pwv per group: \n", median_group)
    print("Error = std/median: \n", stds)

    x=np.linspace(min(pwv_bba)-2, max(pwv_bba)+2, len(pwv_bba))
    fig, (ax1,ax2) = plt.subplots(2,1, figsize=(18,16), sharex=True, gridspec_kw={'height_ratios':[4,1], 'hspace':0})

    ax1.plot(bba2, pwv_bba, 'b.', alpha=0.3)
    ax1.plot(np.sort(bba2), expon(np.sort(bba2),a,b,c,d), 'r-', lw=2, alpha=0.7, label='Exponential Fit')
    ax1.set_xlabel("CePIA Sky Temperature [°C]", fontsize=20)
    ax1.set_ylabel("APEX PWV [mm]", fontsize=20)
    ax1.set_xlim(min(bba2)-0.5,max(bba2)+0.5)
    ax1.set_ylim(-0.1,2.75)
    ax1.legend(fontsize=16)
    for i in np.arange((2*min(bba2)+step)/2, (max(bba2)), step):
        bin_index = np.digitize(i, bins) - 1
        if 0 <= bin_index < len(stds):
            ax1.errorbar(i, expon(i, a, b, c, d), yerr=stds[bin_index], color='red', fmt='x', ecolor='black', capsize=7, lw=4)
            ax1.text(i-0.33, 0, f"$\\sigma$={stds[bin_index]:.3f}", fontsize=10)
    for i in np.arange(min(bba2), max(bba2)+1, step):
        ax1.vlines(i,-0.3,0.1, color='blue', linestyle='--')

    ax2.plot(bba2, pwv_bba - pred_exp, 'k.', alpha=0.5)
    ax2.hlines(0,-70,-40, color='red', linestyle='--', alpha=1)
    for i in np.arange(min(bba2), max(bba2)+1, step):
        ax2.vlines(i,-2,2, color='blue', linestyle='--')
    ax2.set_ylabel("Residuals [mm]", fontsize=16)
    ax2.set_xlabel("CePIA Sky Temperature [°C]", fontsize=20)
    ax2.set_xlim(min(bba2)-0.5,max(bba2)+0.5)
    ax2.set_ylim(min(pwv_bba-pred_exp)-0.1,max(pwv_bba-pred_exp)+0.1)

    x=np.linspace(min(pwv_bba)-2, max(pwv_bba)+2, len(pwv_bba))
    fig, (ax1,ax2) = plt.subplots(2,1, figsize=(18,16), sharex=True, gridspec_kw={'height_ratios':[4,1], 'hspace':0})

    ax1.plot(pwv_bba, pred_exp, 'b.', alpha=0.3)
    ax1.plot(x,x,'k--', alpha=0.5, label='Ratio 1:1')
    ax1.plot(x,x*m1 + b1, 'r-', label=f"m={m1:.4f} \n$\\sigma$ ={np.std(pred_exp):.4f}")
    ax1.set_ylabel("CePIA PWV [mm]", fontsize=20)
    ax1.set_xlabel("APEX PWV [mm]", fontsize=20)
    ax1.set_xlim(min(pwv_bba)-0.1,max(pwv_bba)+0.1)
    ax1.set_ylim(min(pwv_bba)-0.1,max(pwv_bba)+0.1)
    ax1.legend(fontsize=16)

    for i in np.arange((2*min(bba2)+step)/2, (max(bba2)), step):
        bin_index = np.digitize(i, bins) - 1
        if 0 <= bin_index < len(stds):
            ax1.errorbar(expon(i,a,b,c,d), expon(i,a,b,c,d)*m1 + b1, yerr=stds[bin_index], color='red', fmt='x', ecolor='black', capsize=7, lw=4)


    ax1.text(min(pwv_bba), 1.7, f"r={metric[0]:.4f}")
    ax1.text(min(pwv_bba), 1.6, f"R2={metric[1]:.4f}")
    ax1.text(min(pwv_bba), 1.5, f"RMSE={metric[2]:.4f}")
    ax1.text(min(pwv_bba), 1.4, f"MAE={metric[3]:.4f}")
    ax1.text(min(pwv_bba), 1.3, f"Std={metric[4]:.4f}")

    ax2.plot(pwv_bba, pwv_bba - pred_exp, 'k.', alpha=0.5)
    ax2.hlines(0,0,3, color='red', linestyle='--', alpha=1)
    ax2.set_ylabel("Residuals [mm]", fontsize=16)
    ax2.set_xlabel("APEX PWV [mm]", fontsize=20)
    ax2.set_xlim(min(pwv_bba)-0.1,max(pwv_bba)+0.1)
    ax2.set_ylim(min(pwv_bba-pred_exp)-0.1,max(pwv_bba-pred_exp)+0.1)

    plt.show()
