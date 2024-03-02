import pandas as pd

languages = ["arabic","chinese","english","french","russian","spanish"]
metrics = ["editors","absolute-bytes","edited-page","edits","netbytediff","newpages"]

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

#参考框架（复制用不要直接用）：
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
        