import pandas as pd
import numpy as np
from scipy.stats import pearsonr
from scipy.stats import kendalltau
from scipy.stats import theilslopes
import matplotlib.pyplot as plt
import csv
import seaborn as sns

languages = ["arabic", "chinese", "english", "french", "russian", "spanish"]
metrics = ["editors", "absolute-bytes",
           "edited-page", "edits", "netbytediff", "newpages"]

user_dataset = []
anon_dataset = []
for lan in languages:
    user_lan_dataset = []
    anon_lan_dataset = []
    for met in metrics:
        file_name = lan+"-"+met+".csv"

        data = pd.read_csv("./data/"+file_name)
        user_data = data["total.user"].to_list()
        anon_data = data["total.anonymous"].to_list()
        user_lan_dataset.append(user_data)
        anon_lan_dataset.append(anon_data)
    user_dataset.append(user_lan_dataset)
    anon_dataset.append(anon_lan_dataset)

# 参考框架（复制用不要直接用）：
# for i in range(len(user_dataset)):
#     lan = languages[i]
#     print(lan+"------------------------------------------")
#     user_lan_dataset = user_dataset[i]
#     anon_lan_dataset = anon_dataset[i]

#     #number of editors
#     user_editors = user_lan_dataset[0]
#     anon_editors = anon_lan_dataset[0]

#     #other metrics
#     for j in range(len(user_lan_dataset[1:])):
#         met = metrics[j+1]
#         print(met)
#         user_lan_met_data = user_lan_dataset[j+1]
#         anon_lan_met_data = anon_lan_dataset[j+1]
    
def write_file(csv_file, data_lst):
    with open(csv_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data_lst)

for i in range(len(user_dataset)):
    lan = languages[i]
    print(lan+"------------------------------------------")
    user_lan_dataset = user_dataset[i]
    anon_lan_dataset = anon_dataset[i]

    # number of editors
    user_editors = user_lan_dataset[0]
    anon_editors = anon_lan_dataset[0]

    # metric_user_values = user_lan_dataset[1]
    # print(user_editors)
    # print("------------------")
    # print(metric_user_values)
    # metric = metrics[1]
    # plt.plot(user_editors, metric_user_values)
    # plt.title(lan + " metric for users")
    # plt.xlabel(lan)
    # plt.ylabel(metric)
    # plt.show()
    # plt.legend()

    pcc_user = []
    pp_user = []
    pcc_anon = []
    pp_anon = []

    kcc_user = []
    kp_user = []
    kcc_anon = []
    kp_anon = []

    slopes_user = []
    intercepts_user = []
    slopes_anon = []
    intercepts_anon = []

    for j in range(1, len(user_dataset)):
        metric = metrics[j]
        metric_user_values = user_lan_dataset[j]
        metric_anon_values = anon_lan_dataset[j]

        user_editors_normalized = (user_editors - np.min(user_editors)) / np.ptp(user_editors)
        user_metric_normalized = (metric_user_values - np.min(metric_user_values)) / np.ptp(metric_user_values)
        anon_editors_normalized = (anon_editors - np.min(anon_editors)) / np.ptp(anon_editors)
        anon_metric_normalized = (metric_anon_values - np.min(metric_anon_values)) / np.ptp(metric_anon_values)

        print("Calculating Pearson's correlation between number of editors vs.",
              metric, "for users")
        correlation_user, p_value_user = pearsonr(
            user_editors_normalized, user_metric_normalized)
        print(f"Pearson's correlation coefficient: {correlation_user}")
        print(f"P-value: {p_value_user}")
        pcc_user.append(correlation_user)
        pp_user.append(p_value_user)

        print("Calculating Pearson's correlation between number of editors vs.",
              metric, "for anonymous")
        correlation_anon, p_value_anon = pearsonr(
            anon_editors_normalized, anon_metric_normalized)
        print(f"Pearson's correlation coefficient: {correlation_anon}")
        print(f"P-value: {p_value_anon}")
        pcc_anon.append(correlation_anon)
        pp_anon.append(p_value_anon)

        print("Calculating Kendall rank correlation between number of editors vs.",
              metric, "for users")
        tau_user, p_tau_user = kendalltau(user_editors_normalized, user_metric_normalized)
        print(f"Kendall's tau: {tau_user}")
        print(f"P-value: {p_tau_user}")
        kcc_user.append(tau_user)
        kp_user.append(p_tau_user)

        print("Calculating Kendall rank correlation between number of editors vs.",
              metric, "for anonymous")
        tau_anon, p_tau_anon = kendalltau(anon_editors_normalized, anon_metric_normalized)
        print(f"Kendall's tau: {tau_anon}")
        print(f"P-value: {p_tau_anon}")
        kcc_anon.append(tau_anon)
        kp_anon.append(p_tau_anon)

        print("Calculating Theil-Sen estimator between number of editors vs.",
              metric, "for users")
        slope_user, intercept_user, _, _ = theilslopes(
            user_metric_normalized, user_editors_normalized, 0.95)
        print(f"Slope: {slope_user}")
        print(f"Intercept: {intercept_user}")
        slopes_user.append(slope_user)
        intercepts_user.append(intercept_user)

        print("Calculating Theil-Sen estimator between number of editors vs.",
              metric, "for anonymous")
        slope_anon, intercept_anon, _, _ = theilslopes(
            anon_metric_normalized, anon_editors_normalized, 0.95)
        print(f"Slope: {slope_anon}")
        print(f"Intercept: {intercept_anon}")
        slopes_anon.append(slope_anon)
        intercepts_anon.append(intercept_anon)
    
    print(slopes_user)
    files = [ 'stats/theil-slope-user.csv', 'stats/theil-intercept-user.csv', \
        'stats/theil-slope-anon.csv', 'stats/theil-intercept-anon.csv',]
    lsts = [slopes_user, intercepts_user, slopes_anon, intercepts_anon]
    for i in range(len(files)):
        csv_file = files[i]
        data_lst = lsts[i]
        write_file(csv_file, data_lst)


