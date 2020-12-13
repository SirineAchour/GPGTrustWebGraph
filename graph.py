import pandas as pd
import networkx as nx
import sys

df = pd.DataFrame({'from': [], 'to': []})
sigs = sys.stdin.read()
sigs = sigs.split("pub:")

for specific_key in sigs:
    if specific_key.startswith("tru:") or specific_key == '':
        # ignore this line 5atr idk what to do with it
        continue

    lines = specific_key.splitlines()
    sigs_in_total = []
    main_key_name = ""
    key_name = ""
    pub_key_id = ""
    for line in lines:
        if line.startswith("uid:"):
            uid_stuff = line.split(":")
            key_name = uid_stuff[9]
        if line.startswith("sig:"):
            sig_stuff = line.split(":")
            sig_id = sig_stuff[4]
            sig_name = sig_stuff[9]
            if sig_name != key_name:
                sig_display_name = sig_name + " (" + sig_id + ")"
                sigs_in_total.append(sig_display_name)
            else:
                pub_key_id = sig_id
    main_key_name = key_name + " (" + pub_key_id + ")"
    to_list = []
    if sigs_in_total:
        for i in sigs_in_total:
            to_list.append(main_key_name)
    else:
        sigs_in_total = [main_key_name]
        to_list.append(main_key_name)
    # add it to the dataframe
    df2 = pd.DataFrame({"from": sigs_in_total, "to": to_list})
    df = df.append(df2)

# Graphing the whole thing
G = nx.from_pandas_edgelist(df, 'from', 'to', create_using=nx.DiGraph())
print(nx.drawing.nx_pydot.to_pydot(G))
