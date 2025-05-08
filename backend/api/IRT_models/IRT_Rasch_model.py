import math
import numpy as np
import copy
import statistics

# 2回目以降に問題の例外パターンを削除するselect_item_patterns()
# data:事前にユーザを削除したデータ　sum_data:問題iの正答数
# item_list_correct:削除した正答問題の総リスト　item_list_incorrect:削除した誤答問題の相リスト
# this_item_correct，this_item_incorrect:前回の削除リスト
# iten_index_list: item_list_correct + item_list_incorrect
# is_delete_items:全ての例外パターンを削除し終えるとTrue
def select_item_patterns(data, sum_data, item_list_correct, item_list_incorrect, this_item_correct, this_item_incorrect, item_index_list, is_delete_items):
    this_correct = []
    for i in range(len(sum_data)):
        # 問題iが全て正答であるパターンの、インデックスの抽出
        if sum_data[i].item() == len(data.keys()):
            if len(this_item_correct) == 0:
                index_counter = 0
                for j in item_index_list:
                    if j <= i:
                        index_counter += 1
                item_list_correct.append(i+index_counter)
                this_correct.append(i+index_counter)
            else:
                index_counter = 0
                for j in item_index_list:
                    if j <= i:
                        index_counter = i + 1
                    elif j > i:
                        index_counter = i
                item_list_correct.append(index_counter)
                this_correct.append(index_counter)
        # 問題iが全て誤答であるパターンの、インデックスの抽出
        elif sum_data[i].item() == 0:
            if len(this_item_incorrect) == 0:
                index_counter = 0
                for j in item_index_list:
                    if j <= i:
                        index_counter += 1
                item_list_incorrect.append(i+index_counter)
            else:
                index_counter = 0
                for j in item_index_list:
                    if j <= i:
                        index_counter = i + 1
                    elif j > i:
                        index_counter = 0
                item_list_incorrect.append(index_counter)
        # 削除パターンがない場合
        else:
            is_delete_items = True
    return item_list_correct, item_list_incorrect, is_delete_items, this_correct

# 2回目以降にユーザの例外パターンを削除するselect_user_patterns()
# check_data_users:問題を削除した後のデータ
# user_list_correct:削除した正答ユーザの総リスト　user_list_incorrect:削除した誤答ユーザの総リスト
# is_delete_users:削除するパターンが存在しない場合にTrue
def select_user_patterns(check_data_users, item_index_list, user_list_correct, user_list_incorrect, is_delete_users):
    # 今回（ループごと）削除したユーザを格納するリスト
    this_user_correct = []
    this_user_incorrect = []
    for u in check_data_users.keys():
        # データから問題の削除
        for idx in item_index_list:
            del check_data_users[u][idx]
        if all(check_data_users[u]):
            user_list_correct.append(u)
            this_user_correct.append(u)
        elif not any(check_data_users[u]):
            user_list_incorrect.append(u)
            this_user_incorrect.append(u)
        else:
            is_delete_users = True
    return user_list_correct, user_list_incorrect,this_user_correct, this_user_incorrect, is_delete_users

# 1回目に問題の例外パターンを削除する
def init_select_item_patterns(data, sum_data, item_list_correct, item_list_incorrect):
    for i in range(len(sum_data)):
        if sum_data[i].item() == len(data.keys()):
            item_list_correct.append(i)
        elif sum_data[i].item() == 0:
            item_list_incorrect.append(i)
    return item_list_correct, item_list_incorrect

# 1回目にユーザの例外パターンを削除する
def init_select_user_patterns(check_data_users, item_index_list, user_list_correct, user_list_incorrect):
    for u in check_data_users.keys():
        for idx in item_index_list:
            del check_data_users[u][idx]
        if all(check_data_users[u]):
            user_list_correct.append(u)
        elif not any(check_data_users[u]):
            user_list_incorrect.append(u)
    return user_list_correct, user_list_incorrect

# 2回目以降に、問題iの合計点si，ユーザuの合計得点fu，解答パターンuijから問題を削除する
def delete_item_patterns(item_list_correct, item_list_incorrect,this_item_correct, si, fu, uij):
    this_item_index_list = []
    # si（問題iの合計点）から除外
    for i in item_list_correct:
        if i in si:
            del si[i]
            this_item_index_list.append(i)
    for i in item_list_incorrect:
        if i in si:
            del si[i]
            this_item_index_list.append(i)
    # fu（ユーザuの合計得点）から削除
    for u in fu.keys():
        fu[u] = fu[u] - (len(item_list_correct) - len(this_item_correct))
        #fu[u] = fu[u] - len(this_item_correct)
    # uij（問題iに対する学生jの解答）から除外
    for u in uij.keys():
        for i in item_list_correct:
            if i in uij[u]:
                del uij[u][i]
        for i in item_list_incorrect:
            if i in uij[u]:
                del uij[u][i]
    return si,fu,uij,this_item_index_list

# 1回目に、問題iの合計点si，ユーザuの合計得点fu，解答パターンuijから問題を削除する
def init_delete_item_patterns(item_list_correct, item_list_incorrect, si, fu, uij):    
    # si（問題iの合計点）から除外
    for i in item_list_correct:
        del si[i]
    for i in item_list_incorrect:
        del si[i]
    # fu（ユーザuの合計得点）から削除
    for u in fu.keys():
        fu[u] = fu[u] - len(item_list_correct)
    # uij（問題iに対する学生jの解答）から除外
    for u in uij.keys():
        for i in item_list_correct:
            del uij[u][i]
        for i in item_list_incorrect:
            del uij[u][i]
    return si,fu,uij

# 問題iの合計点si，ユーザuの合計得点fu，解答パターンuijからユーザを削除する
def delete_user_patterns(user_list_correct,user_list_incorrect,si,fu,uij):
    # si（問題iの合計点）から除外
    for i in si.keys():
        si[i] = si[i] - len(user_list_correct)  
    # fu（ユーザuの合計得点）から削除
    for u in user_list_correct:
        del fu[u]
    for u in user_list_incorrect:
        del fu[u]  
    # uij（問題iに対する学生jの解答）から除外
    for u in user_list_correct:
        del uij[u]
    for u in user_list_incorrect:
        del uij[u]
    
    return si,fu,uij

# 問題iの合計点si，ユーザuの合計得点fu，解答パターンuijの作成
def make_si_fu(data):
    # sample_data = make_data()
    si = {}
    fu = {}
    uij = {}
    N = 0
    item_list_correct = []
    item_list_incorrect = []
    user_list_correct = []
    user_list_incorrect = []
    not_test_finished = []
    num_of_questions = []

    for score in data.values():
        num_of_questions.append(len(score))
    # 問題数n
    n = statistics.mode(num_of_questions)

    init_data_check = data.copy()
    for user,score in init_data_check.items():
        print(user,score,len(score),n)
        if len(score) < n:
            not_test_finished.append(user)
            del data[user]
    print(data,not_test_finished)

    sum_si = np.sum(list(data.values()), axis=0)
    
    # 問題の合計得点si
    for i in range(len(sum_si)):
        si[i] = sum_si[i].item()
    # ユーザの合計得点fu
    for u in data.keys():
        fu[u] = np.sum(list(data[u])).item()
        # ユーザ合計得点の最大値
        if fu[u] > N:
            N = fu[u]
        ui = {}
        # 解答情報uij
        for i in range(len(sum_si)):
            ui[i] = data[u][i]
        uij[u] = ui
    
    #print(fu)

    # 以下のコメントの処理をメソッドに置き換え
    check_data_items = list(data.values())
    sum_data = np.sum(check_data_items, axis=0)
    item_list_correct,item_list_incorrect = init_select_item_patterns(data, sum_data, item_list_correct, item_list_incorrect)
    si,fu,uij = init_delete_item_patterns(item_list_correct, item_list_incorrect, si, fu, uij)
    """print("全問正答項目：１：",item_list_correct)
    print("全問誤答項目：１：",item_list_incorrect)
    print("問題iの合計点：",si)
    print("ユーザuの合計点：",fu)
    print("解答パタン：",uij)
    print("=================")"""

    #以下のコメントの処理をメソッドに置き換え
    item_index_list = item_list_correct + item_list_incorrect
    item_index_list.sort(reverse=True)
    check_data_users = data
    user_list_correct, user_list_incorrect = init_select_user_patterns(check_data_users, item_index_list, user_list_correct, user_list_incorrect)
    si,fu,uij = delete_user_patterns(user_list_correct,user_list_incorrect,si,fu,uij)
    """print("全問正答ユーザ：",user_list_correct)
    print("全問誤答ユーザ：",user_list_incorrect)
    print("問題iの合計点：",si)
    print("ユーザuの合計点：",fu)
    print("解答パタン：",uij)
    print("=================")"""
 
    # 以下のコメントの処理をメソッドにまとめた
    # 削除した分のインデックスを考慮しなきゃ
    is_delete_items = False
    is_delete_users = False
    count = 1
    check = data
    check_data_item = check
    this_user_correct = copy.copy(user_list_correct)
    this_user_incorrect = copy.copy(user_list_incorrect)
    while True:
        if is_delete_items and is_delete_users:
            break
        else:
            count += 1
            this_item_correct = copy.copy(item_list_correct)
            this_item_incorrect = copy.copy(item_list_incorrect)
            user_index_list = this_user_correct + this_user_incorrect
            for u in user_index_list:
                del check_data_item[u]
            
            if len(check_data_item) == 0:
                break
            check_data = list(check_data_item.values())
            sum_data = np.sum(check_data, axis=0)

            # 問題、ユーザを削除したうえでのitem_listの再構成
            item_list_correct,item_list_incorrect,is_delete_items, this_correct = select_item_patterns(check_data_item, sum_data, item_list_correct, item_list_incorrect, this_item_correct, this_item_incorrect, item_index_list, is_delete_items)
            #si,fu,uij,this_item_index_list = delete_item_patterns(list(dict.fromkeys(item_list_correct)), list(dict.fromkeys(item_list_incorrect)),list(dict.fromkeys(this_item_correct)), si, fu, uij)
            si,fu,uij,this_item_index_list = delete_item_patterns(list(dict.fromkeys(item_list_correct)), list(dict.fromkeys(item_list_incorrect)),list(dict.fromkeys(this_item_correct)), si, fu, uij)

            # 問題、ユーザを削除したうえでのuser_listの再構成
            check_data_user = check_data_item
            this_item_index_list.sort(reverse=True)
            # 各ループで削除したitem_indexリストの再構成
            for i in range(len(this_item_index_list)):
                for j in item_index_list:
                    index_count = 0
                    if j <= this_item_index_list[i]:
                        index_count += 1
                    elif j > this_item_index_list[i]:
                        index_count += 0
                    this_item_index_list[i] -= index_count
            user_list_correct, user_list_incorrect,this_user_correct,this_user_incorrect, is_delete_users = select_user_patterns(check_data_user, this_item_index_list, user_list_correct, user_list_incorrect, is_delete_users)
            si,fu,uij = delete_user_patterns(this_user_correct,this_user_incorrect,si,fu,uij)

            item_index_list = item_list_correct + item_list_incorrect
            item_index_list.sort(reverse=True)
            # chekc_data_itemの削除
            check = check_data_item
    
    u = len(fu.keys()) 
    if len(not_test_finished) > 0:
        for user in not_test_finished:
            user_list_incorrect.append(user)
    return si, fu, u, uij, list(dict.fromkeys(item_list_correct)), list(dict.fromkeys(item_list_incorrect)), list(dict.fromkeys(user_list_correct)),list(dict.fromkeys(user_list_incorrect))

# 初期値計算式
def group_0(odd, odds):
    sum_odds = np.sum(list(odds.values()))
    return odd - (sum_odds.item() / len(odds.keys()))

# 正解のlog-odds式
def log_odd(s, u):
    #return math.log(s / u)
    if s < 0:
        s = 0
    if u < 0:
        u = 0
    """try:
        odd = math.log(s / u)
    except ValueError:
        odd = math.log(0.001 / u)
    except ZeroDivisionError:
        odd = math.log(s / 0.001)"""
    odd = math.log(s / u)
    return odd
    """P = s / u
    if P <= 0:
        return math.log(0.001 / (1 - 0.001))
    elif P == 1:
        return math.log(0.999 / (1 - 0.999))
    else: 
        return math.log(P / (1 - P))"""

# 不正解のlog-odds式
def diff_log_odd(s, u):
    #return math.log(u / s)
    if s < 0:
        s = 0
    if u < 0:
        u = 0
    """try:
        odd = math.log(u / s)
    except ValueError:
        odd = math.log(0.001 / s)
    except ZeroDivisionError:
        odd = math.log(u / 0.001)"""
    odd = math.log(u / s)
    return odd
    """P = s / u
    if P <= 0:
        return math.log((1 - 0.001) / 0.001)
    elif P == 1:
        return math.log((1 - 0.999) / 0.999)
    else:
        return math.log((1 - P) / P)"""

# Raschモデル
def L1P_model(uij, theta, beta):
    #return (1 / (1 + math.exp(-(theta - beta))))
    return (math.exp(theta - beta) / (1 + math.exp(theta - beta)))
    """if uij == 1:
        return (math.exp(theta - beta) / (1 + math.exp(theta - beta)))
    else:
        return (math.exp(0) / (1 + math.exp(theta - beta)))"""
    #return (math.exp(uij * (theta - beta)) / (1 + math.exp(theta -beta)))

# 期待確率の算出
def ExceptionScore(theta, beta, uij):
    e_scores_user = {}
    e_scores_item = {}
    for user in theta.keys():
        e_score_list = []
        for item in beta.keys():
            e_score_list.append(L1P_model(uij[user][item], theta[user], beta[item]))
        e_scores_user[user] = e_score_list  
    for item in beta.keys():
        e_score_list = []
        for user in theta.keys():
            e_score_list.append(L1P_model(uij[user][item], theta[user], beta[item]))
        e_scores_item[item] = e_score_list
    return e_scores_user, e_scores_item

# 初期値に対応する期待確率の算出
def Init_ExceptScore(si, fu, u, uij):
    beta_0 = {}
    theta_0 = {}
    beta_logodds = {}
    theta_odds = {}
    theta_logodds = {}
    e_scores_user = {}
    e_scores_item = {}

    # 項目難易度の初期値beta_0の計算
    # prox法
    for i in si.keys():
        beta_logodds[i] = diff_log_odd(si[i], u-si[i])
    for item in beta_logodds.keys():
        beta_0[item] = group_0(beta_logodds[item], beta_logodds)

    # 学生能力値の初期値theta_0の計算
    for user in fu.keys():
        theta_odds[user] = log_odd(fu[user], len(si)-fu[user])
        theta_logodds[user] = diff_log_odd(fu[user], len(si))
    theta_0 = theta_odds
    """for user in theta_odds.keys():
        theta_0[user] = group_0(theta_odds[user],beta_logodds)"""

    # 期待得点の計算
    e_scores_user, e_scores_item = ExceptionScore(theta_0, beta_0, uij)
    
    return theta_0, beta_0, e_scores_user, e_scores_item

# NewtonRaphson法によるthetaの推定
def NR_theta(fu,beta,theta_0,e_scores_user,uij):
    theta_t1 = 0
    thetas = {}
    theta_t = theta_0
    e_scores_user, e_scores_item = ExceptionScore(theta_t, beta, uij)
    for user in e_scores_user.keys():
        P_sum = 0
        PQ_sum = 0
        for i in e_scores_user[user]:
            P = i
            Q = 1 - i
            P_sum = P_sum + P
            PQ_sum = PQ_sum + (P * Q)
        theta_t1 = theta_t[user] + ((fu[user] - P_sum) / PQ_sum)
        thetas[user] = theta_t1
    return thetas

# NewtonRaphson法によるbetaの推定
def NR_beta(si,fu,beta,theta,e_scores_item, uij):
    beta_t1 = 0
    betas = {}
    beta_t = beta
    # 分散を求める
    # 更新する難易度の計算
    for item in e_scores_item.keys():
        P_sum = 0
        PQ_sum = 0
        user = list(fu.keys())
        user_count = 0
        for u in e_scores_item[item]:
            P = u
            Q = 1 - P
            #P_sum = P_sum + (fu[user[user_count]] * P)
            #PQ_sum = PQ_sum + (fu[user[user_count]] * P * Q)
            user_count = user_count + 1
            P_sum = P_sum + P
            PQ_sum = PQ_sum + (P * Q)
        beta_t1 = beta_t[item] - ((si[item] - P_sum) / PQ_sum)
        betas[item] = beta_t1 
    return betas

def NR_theta_model(fu, beta, theta, uij):
    thetas = {}
    while True:
        e_scores_user, e_scores_item = ExceptionScore(theta, beta, uij)
    #for t in range(10):
        is_theta = False
        thetas = NR_theta(fu, beta, theta, e_scores_user, uij)
        theta_ave = np.sum(list(thetas.values())).item() / len(thetas)
        is_theta = False
        for user in thetas.keys():
            if -0.05 < thetas[user] - theta[user] < 0.05:
                is_theta = True
                thetas[user] = thetas[user] - theta_ave
            else:
                is_theta = False
                break
        if is_theta:
            e_scores_user, e_scores_item = ExceptionScore(thetas, beta, uij)
            return thetas
        else:
            theta = thetas
            continue

def NR_beta_model(si, fu, beta, theta, uij):
    betas = {}
    while True:
        e_scores_user, e_scores_item = ExceptionScore(theta, beta, uij)
    #for t in range(10):
        is_betas = []
        betas = NR_beta(si, fu, beta, theta, e_scores_item, uij)
        beta_ave = np.sum(list(betas.values())).item() / len(betas)
        for item in betas.keys():
            is_beta = -0.05 < betas[item] - beta[item] < 0.05
            is_betas.append(is_beta)
        #print(is_betas)
        if all(is_betas):
            for item in betas.keys():
                betas[item] =  betas[item] - beta_ave
            return betas
        else:
            beta = betas
            continue

# NewtonRaphson法による推定
def NR_theory(data):
    si,fu,u,uij,item_list_correct, item_list_incorrect, user_list_correct,user_list_incorrect = make_si_fu(data)
    theta, beta, e_scores_user, e_scores_item = Init_ExceptScore(si, fu, u, uij)
    betas = {}
    thetas = {}
    beta_ave = 0
    theta_ave = 0

    while True:
        betas = NR_beta_model(si, fu, beta, theta, uij)
        thetas = NR_theta_model(fu, betas, theta, uij)
        beta_ave = np.sum(list(beta.values())).item() / len(beta)
        betas_ave = np.sum(list(betas.values())).item() / len(betas)
        theta_ave = np.sum(list(theta.values())).item() / len(theta)
        thetas_ave = np.sum(list(thetas.values())).item() / len(thetas)
        if (-0.05 < betas_ave - beta_ave < 0.05) and (-0.05 < thetas_ave - theta_ave < 0.05):
            break
        else:
            beta = betas
            theta = thetas
            
    """print(si)
    print(fu)
    print("推定値")
    print(betas)
    print(thetas)
    print("---------------------------------")"""
    
    return betas, thetas, user_list_correct, user_list_incorrect, item_list_correct, item_list_incorrect