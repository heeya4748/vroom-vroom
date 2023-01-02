import pickle

reset = False
load = True

player_log = {"class_num":[], "play_num":[]}
player_info = []

if reset:
    with open("play_log.pickle", "wb") as fw:
        pickle.dump(player_log, fw)
    with open("record_log.pickle", "wb") as fw:
        pickle.dump(player_info, fw)

if load:
    with open("play_log.pickle", "rb") as fr:
        player_log = pickle.load(fr)
    with open("record_log.pickle", "rb") as fr:
        record_log = pickle.load(fr)
    
    print(player_log)
    print(record_log)

if True:
    best_index = []
    best_record = record_log[0][-1]
    del record_log[27]

    for i in range(len(record_log)):
        cur_record = record_log[i][-1]
        if cur_record > best_record:
            best_record = cur_record
            best_index = [i]
        elif cur_record == best_record:
            best_index.append(i)

    print()
    print(best_record)
    for i in best_index:
        print(record_log[i])
        print(i)

# 20103, 20112, 20102