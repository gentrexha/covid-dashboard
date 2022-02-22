from utils import setup_data

df_deaths, df_recovered, df_total = setup_data()

df_deaths.to_csv("../data/deaths.csv", index=False)
df_recovered.to_csv("../data/recovered.csv", index=False)
df_total.to_csv("../data/total.csv", index=False)
