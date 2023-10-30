import os
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats
from dotenv import load_dotenv

load_dotenv()


# 正規分布に従うかを確認する関数
# シャピロ・ウィルク検定を用いる
# 引数に結果の入ったファイルのパスを渡す．
def check_seikibunpu(real_faults_result_path,artificial_faults_result_path):
    df_real = pd.read_csv(real_faults_result_path)
    df_artificial = pd.read_csv(artificial_faults_result_path)
    print("実欠陥：")
    print(stats.shapiro(df_real["rank"]))
    print("人工欠陥：")
    print(stats.shapiro(df_artificial["rank"]))
    
# refailに基づき実欠陥，人工欠陥の個数をカウントする．
def calc_num_of_faults_refail(real_faults_result_path,artificial_faults_result_path):
    df_real = pd.read_csv(real_faults_result_path)
    df_artificial = pd.read_csv(artificial_faults_result_path)
    
    projects = ["math","chart","lang","jsoup","jacksoncore","codec"]
    print("実欠陥:")
    for project in projects:
        print(project)
        print(_calc_num_of_faults_refail_specified_project(df_real,project))
    print("人工欠陥:")
    for project in projects:
        print(project)
        print(_calc_num_of_faults_refail_specified_project(df_artificial,project))

def _calc_num_of_faults_refail_specified_project(df,project):
    ret = {"rEFail=0":0,"0<rEFail<1":0,"rEFail=1":0}
    df_tmp = df[df["bug_id"].str.startswith(project)]
    ret["rEFail=0"] = len(df_tmp[df_tmp["rEFail"]==0]) + len(df_tmp[df_tmp["rEFail"].isnull()])
    ret["rEFail=1"]= len(df_tmp[df_tmp["rEFail"]==1])
    ret["0<rEFail<1"] = len(df_tmp) - ret["rEFail=0"] - ret["rEFail=1"]
    return ret
    
# repassに基づき実欠陥，人工欠陥の個数をカウントする．
def calc_num_of_faults_repass(real_faults_result_path,artificial_faults_result_path):
    df_real = pd.read_csv(real_faults_result_path)
    df_artificial = pd.read_csv(artificial_faults_result_path)
    
    projects = ["math","chart","lang","jsoup","jacksoncore","codec"]
    print("実欠陥:")
    for project in projects:
        print(project)
        print(_calc_num_of_faults_repass_specified_project(df_real,project))
    print("人工欠陥:")
    for project in projects:
        print(project)
        print(_calc_num_of_faults_repass_specified_project(df_artificial,project))

def _calc_num_of_faults_repass_specified_project(df,project):
    ret = {"rEPass=0":0,"0<rEPass<1":0,"rEPass=1":0}
    df_tmp = df[df["bug_id"].str.startswith(project)]
    ret["rEPass=0"] = len(df_tmp[df_tmp["rEPass"]==0]) + len(df_tmp[df_tmp["rEPass"].isnull()])
    ret["rEPass=1"]= len(df_tmp[df_tmp["rEPass"]==1])
    ret["0<rEPass<1"] = len(df_tmp) - ret["rEPass=0"] - ret["rEPass=1"]
    return ret
    
# refailに基づき，rTop-5を計算する
def calc_rtopn_based_refail(real_faults_result_path,artificial_faults_result_path,n):
    df_real = pd.read_csv(real_faults_result_path)
    df_artificial = pd.read_csv(artificial_faults_result_path)
    projects = ["math","chart","lang","jsoup","jacksoncore","codec"]
    print("実欠陥:")
    for project in projects:
        print(project)
        print(_calc_rtopn_based_refail_specified_project(df_real,project,n))
    print("人工欠陥:")
    for project in projects:
        print(project)
        print(_calc_rtopn_based_refail_specified_project(df_artificial,project,n))
        
def _calc_rtopn_based_refail_specified_project(df,project,n):
    rank_within_n = {"rEFail=0":0,"0<rEFail<1":0,"rEFail=1":0}
    length_df = _calc_num_of_faults_refail_specified_project(df,project)
    ret = {"rEFail=0":0,"0<rEFail<1":0,"rEFail=1":0}
    df_tmp = df[df["bug_id"].str.startswith(project)]
    
    rank_within_n["rEFail=0"] = len(df_tmp[(df_tmp["rEFail"]==0) & (df_tmp["rank"]<=n)]) + len(df_tmp[(df_tmp["rEFail"].isnull()) & (df_tmp["rank"]<=n)])
    rank_within_n["rEFail=1"] = len(df_tmp[(df_tmp["rEFail"]==1) & (df_tmp["rank"]<=n)])
    rank_within_n["0<rEFail<1"] = len(df_tmp[(df_tmp["rEFail"]>0) & (df_tmp["rEFail"]<1) & (df_tmp["rank"]<=n)])
    
    for category in rank_within_n.keys():
        try:
            ret[category] = rank_within_n[category]/length_df[category]
        except ZeroDivisionError:
            ret[category] = None
    return ret

# repassに基づき，rTop-5を計算する
def calc_rtopn_based_repass(real_faults_result_path,artificial_faults_result_path,n):
    df_real = pd.read_csv(real_faults_result_path)
    df_artificial = pd.read_csv(artificial_faults_result_path)
    projects = ["math","chart","lang","jsoup","jacksoncore","codec"]
    print("実欠陥:")
    for project in projects:
        print(project)
        print(_calc_rtopn_based_repass_specified_project(df_real,project,n))
    print("人工欠陥:")
    for project in projects:
        print(project)
        print(_calc_rtopn_based_repass_specified_project(df_artificial,project,n))
        
def _calc_rtopn_based_repass_specified_project(df,project,n):
    rank_within_n = {"rEPass=0":0,"0<rEPass<1":0,"rEPass=1":0}
    length_df = _calc_num_of_faults_repass_specified_project(df,project)
    ret = {"rEPass=0":0,"0<rEPass<1":0,"rEPass=1":0}
    df_tmp = df[df["bug_id"].str.startswith(project)]
    
    rank_within_n["rEPass=0"] = len(df_tmp[(df_tmp["rEPass"]==0) & (df_tmp["rank"]<=n)]) + len(df_tmp[(df_tmp["rEPass"].isnull()) & (df_tmp["rank"]<=n)])
    rank_within_n["rEPass=1"] = len(df_tmp[(df_tmp["rEPass"]==1) & (df_tmp["rank"]<=n)])
    rank_within_n["0<rEPass<1"] = len(df_tmp[(df_tmp["rEPass"]>0) & (df_tmp["rEPass"]<1) & (df_tmp["rank"]<=n)])
    
    for category in rank_within_n.keys():
        try:
            ret[category] = rank_within_n[category]/length_df[category]
        except ZeroDivisionError:
            ret[category] = None
    return ret

# refailに基づき，実欠陥にてマン・ホイットニーのU検定を実施する
def calc_mannwhitneyutest_refail_realfault(result_path):
    df = pd.read_csv(result_path)
    df_tmp = df
    df0 = df_tmp[(df_tmp["rEFail"]==0) | (df_tmp["rEFail"].isnull())]["rank"]
    df1 = df_tmp[df_tmp["rEFail"]==1]["rank"]
    df_other = df_tmp[(df_tmp["rEFail"]>0) & (df_tmp["rEFail"]<1)]["rank"]
    df_dict = {"rEFail=0": df0, "0<rEFail<1": df_other, "rEFail=1": df1}
    for i in range(len(df_dict.keys())):
        key1 = list(df_dict.keys())[i]
        for j in range(i+1,len(df_dict.keys())):
            key2 = list(df_dict.keys())[j]
            print(key1,key2)
            try:
                print(stats.mannwhitneyu(df_dict[key1], df_dict[key2], alternative='two-sided'))
            except ValueError:
                print("None")

# refailに基づき，人工欠陥にてマン・ホイットニーのU検定を実施する
def calc_mannwhitneyutest_refail_artificialfault(result_path):
    df = pd.read_csv(result_path)
    category = ["rEFail=0","0<rEFail<1","rEFail=1"]
    projects = ["math","chart","lang","jsoup","jacksoncore","codec"]
    ret = {}
    for project in projects:
        df_tmp = df[df["bug_id"].str.startswith(project)]
        df0 = df_tmp[(df_tmp["rEFail"]==0) | (df_tmp["rEFail"].isnull())]["rank"]
        df1 = df_tmp[df_tmp["rEFail"]==1]["rank"]
        df_other = df_tmp[(df_tmp["rEFail"]>0) & (df_tmp["rEFail"]<1)]["rank"]
        df_dict = {"rEFail=0": df0, "0<rEFail<1": df_other, "rEFail=1": df1}
        print(project)
        for i in range(len(df_dict.keys())):
            key1 = list(df_dict.keys())[i]
            for j in range(i+1,len(df_dict.keys())):
                key2 = list(df_dict.keys())[j]
                print(key1,key2)
                try:
                    print(stats.mannwhitneyu(df_dict[key1], df_dict[key2], alternative='two-sided'))
                except ValueError:
                    print("None")

def rq1():
    str_rq1 = """
RRRRRRRRRRRRRRRRR        QQQQQQQQQ       1111111   
R::::::::::::::::R     QQ:::::::::QQ    1::::::1   
R::::::RRRRRR:::::R  QQ:::::::::::::QQ 1:::::::1   
RR:::::R     R:::::RQ:::::::QQQ:::::::Q111:::::1   
R::::R     R:::::RQ::::::O   Q::::::Q   1::::1   
R::::R     R:::::RQ:::::O     Q:::::Q   1::::1   
R::::RRRRRR:::::R Q:::::O     Q:::::Q   1::::1   
R:::::::::::::RR  Q:::::O     Q:::::Q   1::::l   
R::::RRRRRR:::::R Q:::::O     Q:::::Q   1::::l   
R::::R     R:::::RQ:::::O     Q:::::Q   1::::l   
R::::R     R:::::RQ:::::O  QQQQ:::::Q   1::::l   
R::::R     R:::::RQ::::::O Q::::::::Q   1::::l   
RR:::::R     R:::::RQ:::::::QQ::::::::Q111::::::111
R::::::R     R:::::R QQ::::::::::::::Q 1::::::::::1
R::::::R     R:::::R   QQ:::::::::::Q  1::::::::::1
RRRRRRRR     RRRRRRR     QQQQQQQQ::::QQ111111111111
                                Q:::::Q           
                                QQQQQQ           
    """
    print(str_rq1)
    real_faults_result_path = Path(os.environ["REAL_FAULT_RESULT_CSV_PATH"])
    artificial_faults_result_path = Path(os.environ["ARTIFICIAL_FAULT_RESULT_CSV_PATH"])
    
    # rEFail, rEPassに基づき，該当する欠陥の個数をカウントする
    print("rEFail，rEPassの該当する欠陥の個数")
    print("----------------------------------------------------------------------------")
    calc_num_of_faults_refail(real_faults_result_path,artificial_faults_result_path)
    calc_num_of_faults_repass(real_faults_result_path,artificial_faults_result_path)
    print("\n\n")
    
    # rEFail, rEPassに基づき，rTop-5を計算する
    print("rTop-5の計測")
    print("----------------------------------------------------------------------------")
    calc_rtopn_based_refail(real_faults_result_path,artificial_faults_result_path,5)
    calc_rtopn_based_repass(real_faults_result_path,artificial_faults_result_path,5)
    print("\n\n")
    
    
    # 欠陥箇所の順位が正規分布に従うかチェックする
    print("欠陥箇所の順位が正規分布に従うかの検証")
    print("----------------------------------------------------------------------------")
    check_seikibunpu(real_faults_result_path,artificial_faults_result_path)
    print("\n\n")
    
    
    # マンホイットニーのU検定をする
    print("マンホイットニーのU検定")
    print("----------------------------------------------------------------------------")
    print("実欠陥におけるマンホイットニーのU検定（プロジェクトによる区分をせず，実欠陥全体で検定する）")
    calc_mannwhitneyutest_refail_realfault(real_faults_result_path)
    print("人工欠陥におけるマンホイットニーのU検定（プロジェクトにより区分し，プロジェクト単位で検定する）")
    calc_mannwhitneyutest_refail_artificialfault(artificial_faults_result_path)
    print("\n\n")
    
    

def count_statements_executed_in_failing_tests_refail(result_path):
    df = pd.read_csv(result_path)
    categories = ["rEFail=0","0<rEFail<1","rEFail=1"]
    projects = ["math","chart","lang","jsoup","jacksoncore","codec"]
    for project in projects:
        print(project)
        ret = {}
        df_tmp = df[df["bug_id"].str.startswith(project)]
        df0 = df_tmp[(df_tmp["rEFail"]==0) | (df_tmp["rEFail"].isnull())]
        df1 = df_tmp[df_tmp["rEFail"]==1]
        df_other = df_tmp[(df_tmp["rEFail"]>0) & (df_tmp["rEFail"]<1)]
        df_dict = {"rEFail=0": df0, "0<rEFail<1": df_other, "rEFail=1": df1}
        for category in categories:
            ret[category] = df_dict[category]["failed_tests_coverage_length"].mean()
        print(ret)
    
def rq2():
    str_rq2 = """
RRRRRRRRRRRRRRRRR        QQQQQQQQQ      222222222222222    
R::::::::::::::::R     QQ:::::::::QQ   2:::::::::::::::22  
R::::::RRRRRR:::::R  QQ:::::::::::::QQ 2::::::222222:::::2 
RR:::::R     R:::::RQ:::::::QQQ:::::::Q2222222     2:::::2 
R::::R     R:::::RQ::::::O   Q::::::Q            2:::::2 
R::::R     R:::::RQ:::::O     Q:::::Q            2:::::2 
R::::RRRRRR:::::R Q:::::O     Q:::::Q         2222::::2  
R:::::::::::::RR  Q:::::O     Q:::::Q    22222::::::22   
R::::RRRRRR:::::R Q:::::O     Q:::::Q  22::::::::222     
R::::R     R:::::RQ:::::O     Q:::::Q 2:::::22222        
R::::R     R:::::RQ:::::O  QQQQ:::::Q2:::::2             
R::::R     R:::::RQ::::::O Q::::::::Q2:::::2             
RR:::::R     R:::::RQ:::::::QQ::::::::Q2:::::2       222222
R::::::R     R:::::R QQ::::::::::::::Q 2::::::2222222:::::2
R::::::R     R:::::R   QQ:::::::::::Q  2::::::::::::::::::2
RRRRRRRR     RRRRRRR     QQQQQQQQ::::QQ22222222222222222222
                                Q:::::Q                   
                                QQQQQQ 
    """
    print(str_rq2)
    real_faults_result_path = Path(os.environ["REAL_FAULT_RESULT_CSV_PATH"])
    artificial_faults_result_path = Path(os.environ["ARTIFICIAL_FAULT_RESULT_CSV_PATH"])
    
    print("失敗テストが実行した文の数")
    print("----------------------------------------------------------------------------")
    print("実欠陥")
    count_statements_executed_in_failing_tests_refail(real_faults_result_path)
    print("人工欠陥")
    count_statements_executed_in_failing_tests_refail(artificial_faults_result_path)


def calc_rtopn_based_stefail(result_path,n):
    df = pd.read_csv(result_path)
    categories = ["rSTEFail=0","0<rSTEFail<1","rSTEFail=1"]
    projects = ["math","chart","lang","jsoup","jacksoncore","codec"]
    for project in projects:
        print(project)
        ret = {}
        df_tmp = df[df["bug_id"].str.startswith(project)]
        df0 = df_tmp[(df_tmp["num_failed_stetest"]==0)]
        df1 = df_tmp[df_tmp["num_failed_stetest"]==df_tmp["num_failed_test"]]
        df_other = df_tmp[(df_tmp["num_failed_stetest"]>0) & (df_tmp["num_failed_stetest"]!=df_tmp["num_failed_test"])]
        df_dict = {"rSTEFail=0": df0, "0<rSTEFail<1": df_other, "rSTEFail=1": df1}
        for category in categories:
            try:
                ret[category] = len(df_dict[category][df_dict[category]["rank"]<=n])/len(df_dict[category])
            except ZeroDivisionError:
                ret[category] = None
        print(ret)

def calc_averank_based_stefail(result_path):
    df = pd.read_csv(result_path)
    categories = ["rSTEFail=0","0<rSTEFail<1","rSTEFail=1"]
    projects = ["math","chart","lang","jsoup","jacksoncore","codec"]
    for project in projects:
        print(project)
        ret = {}
        df_tmp = df[df["bug_id"].str.startswith(project)]
        df0 = df_tmp[(df_tmp["num_failed_stetest"]==0)]
        df1 = df_tmp[df_tmp["num_failed_stetest"]==df_tmp["num_failed_test"]]
        df_other = df_tmp[(df_tmp["num_failed_stetest"]>0) & (df_tmp["num_failed_stetest"]!=df_tmp["num_failed_test"])]
        df_dict = {"rSTEFail=0": df0, "0<rSTEFail<1": df_other, "rSTEFail=1": df1}
        for category in categories:
            try:
                ret[category] = df_dict[category]["rank"].mean()
            except ZeroDivisionError:
                ret[category] = None
        print(ret)
        
def calc_rtopn_based_cefail(result_path,n):
    df = pd.read_csv(result_path)
    categories = ["rCEFail=0","0<rCEFail<1","rCEFail=1"]
    projects = ["math","chart","lang","jsoup","jacksoncore","codec"]
    for project in projects:
        print(project)
        ret = {}
        df_tmp = df[df["bug_id"].str.startswith(project)]
        df0 = df_tmp[(df_tmp["num_failed_cetest"]==0)]
        df1 = df_tmp[df_tmp["num_failed_cetest"]==df_tmp["num_failed_test"]]
        df_other = df_tmp[(df_tmp["num_failed_cetest"]>0) & (df_tmp["num_failed_cetest"]!=df_tmp["num_failed_test"])]
        df_dict = {"rCEFail=0": df0, "0<rCEFail<1": df_other, "rCEFail=1": df1}
        for category in categories:
            try:
                ret[category] = len(df_dict[category][df_dict[category]["rank"]<=n])/len(df_dict[category])
            except ZeroDivisionError:
                ret[category] = None
        print(ret)


def calc_rtopn_all_based_cefail(result_path,n):
    df = pd.read_csv(result_path)
    categories = ["rCEFail=0","0<rCEFail<1","rCEFail=1"]
    ret = {}
    df_tmp = df
    df0 = df_tmp[(df_tmp["num_failed_cetest"]==0)]
    df1 = df_tmp[df_tmp["num_failed_cetest"]==df_tmp["num_failed_test"]]
    df_other = df_tmp[(df_tmp["num_failed_cetest"]>0) & (df_tmp["num_failed_cetest"]!=df_tmp["num_failed_test"])]
    df_dict = {"rCEFail=0": df0, "0<rCEFail<1": df_other, "rCEFail=1": df1}
    for category in categories:
        try:
            ret[category] = len(df_dict[category][df_dict[category]["rank"]<=n])/len(df_dict[category])
        except ZeroDivisionError:
            ret[category] = None
    print(ret)
    
def calc_rtopn_all_based_stefail(result_path,n):
    df = pd.read_csv(result_path)
    categories = ["rSTEFail=0","0<rSTEFail<1","rSTEFail=1"]
    ret = {}
    df_tmp = df
    df0 = df_tmp[(df_tmp["num_failed_stetest"]==0)]
    df1 = df_tmp[df_tmp["num_failed_stetest"]==df_tmp["num_failed_test"]]
    df_other = df_tmp[(df_tmp["num_failed_stetest"]>0) & (df_tmp["num_failed_stetest"]!=df_tmp["num_failed_test"])]
    df_dict = {"rSTEFail=0": df0, "0<rSTEFail<1": df_other, "rSTEFail=1": df1}
    for category in categories:
        try:
            ret[category] = len(df_dict[category][df_dict[category]["rank"]<=n])/len(df_dict[category])
        except ZeroDivisionError:
            ret[category] = None
    print(ret)

def calc_averank_based_cefail(result_path):
    df = pd.read_csv(result_path)
    categories = ["rCEFail=0","0<rCEFail<1","rCEFail=1"]
    projects = ["math","chart","lang","jsoup","jacksoncore","codec"]
    for project in projects:
        print(project)
        ret = {}
        df_tmp = df[df["bug_id"].str.startswith(project)]
        df0 = df_tmp[(df_tmp["num_failed_cetest"]==0)]
        df1 = df_tmp[df_tmp["num_failed_cetest"]==df_tmp["num_failed_test"]]
        df_other = df_tmp[(df_tmp["num_failed_cetest"]>0) & (df_tmp["num_failed_cetest"]!=df_tmp["num_failed_test"])]
        df_dict = {"rCEFail=0": df0, "0<rCEFail<1": df_other, "rCEFail=1": df1}
        for category in categories:
            try:
                ret[category] = df_dict[category]["rank"].mean()
            except ZeroDivisionError:
                ret[category] = None
        print(ret)

def calc_averank_all_based_cefail(result_path):
    df = pd.read_csv(result_path)
    categories = ["rCEFail=0","0<rCEFail<1","rCEFail=1"]
    ret = {}
    df_tmp = df
    df0 = df_tmp[(df_tmp["num_failed_cetest"]==0)]
    df1 = df_tmp[df_tmp["num_failed_cetest"]==df_tmp["num_failed_test"]]
    df_other = df_tmp[(df_tmp["num_failed_cetest"]>0) & (df_tmp["num_failed_cetest"]!=df_tmp["num_failed_test"])]
    df_dict = {"rCEFail=0": df0, "0<rCEFail<1": df_other, "rCEFail=1": df1}
    for category in categories:
        try:
            ret[category] = df_dict[category]["rank"].mean()
        except ZeroDivisionError:
            ret[category] = None
    print(ret)
    
def calc_averank_all_based_stefail(result_path):
    df = pd.read_csv(result_path)
    categories = ["rSTEFail=0","0<rSTEFail<1","rSTEFail=1"]
    ret = {}
    df_tmp = df
    df0 = df_tmp[(df_tmp["num_failed_stetest"]==0)]
    df1 = df_tmp[df_tmp["num_failed_stetest"]==df_tmp["num_failed_test"]]
    df_other = df_tmp[(df_tmp["num_failed_stetest"]>0) & (df_tmp["num_failed_stetest"]!=df_tmp["num_failed_test"])]
    df_dict = {"rSTEFail=0": df0, "0<rSTEFail<1": df_other, "rSTEFail=1": df1}
    for category in categories:
        try:
            ret[category] = df_dict[category]["rank"].mean()
        except ZeroDivisionError:
            ret[category] = None
    print(ret)

def rq3():
    str_rq3="""
RRRRRRRRRRRRRRRRR        QQQQQQQQQ      333333333333333   
R::::::::::::::::R     QQ:::::::::QQ   3:::::::::::::::33 
R::::::RRRRRR:::::R  QQ:::::::::::::QQ 3::::::33333::::::3
RR:::::R     R:::::RQ:::::::QQQ:::::::Q3333333     3:::::3
R::::R     R:::::RQ::::::O   Q::::::Q            3:::::3
R::::R     R:::::RQ:::::O     Q:::::Q            3:::::3
R::::RRRRRR:::::R Q:::::O     Q:::::Q    33333333:::::3 
R:::::::::::::RR  Q:::::O     Q:::::Q    3:::::::::::3  
R::::RRRRRR:::::R Q:::::O     Q:::::Q    33333333:::::3 
R::::R     R:::::RQ:::::O     Q:::::Q            3:::::3
R::::R     R:::::RQ:::::O  QQQQ:::::Q            3:::::3
R::::R     R:::::RQ::::::O Q::::::::Q            3:::::3
RR:::::R     R:::::RQ:::::::QQ::::::::Q3333333     3:::::3
R::::::R     R:::::R QQ::::::::::::::Q 3::::::33333::::::3
R::::::R     R:::::R   QQ:::::::::::Q  3:::::::::::::::33 
RRRRRRRR     RRRRRRR     QQQQQQQQ::::QQ 333333333333333   
                                Q:::::Q                  
                                QQQQQQ
    """
    print(str_rq3)
    
    
    real_faults_result_path = Path(os.environ["REAL_FAULT_RESULT_CSV_PATH"])
    artificial_faults_result_path = Path(os.environ["ARTIFICIAL_FAULT_RESULT_CSV_PATH"])
    
    
    print("rSTEFailによる区分ごとのrTop-5")
    print("----------------------------------------------------------------------------")
    print("実欠陥")
    calc_rtopn_based_stefail(real_faults_result_path,5)
    print("人工欠陥")
    calc_rtopn_based_stefail(artificial_faults_result_path,5)
    print("\n\n")
    
    print("rCEFailによる区分ごとのrTop-5")
    print("----------------------------------------------------------------------------")
    print("実欠陥")
    calc_rtopn_based_cefail(real_faults_result_path,5)
    print("人工欠陥")
    calc_rtopn_based_cefail(artificial_faults_result_path,5)
    print("\n\n")
    
    print("rSTEFailによる区分ごとのave(Rank)")
    print("----------------------------------------------------------------------------")
    print("実欠陥")
    calc_averank_based_stefail(real_faults_result_path)
    print("人工欠陥")
    calc_averank_based_stefail(artificial_faults_result_path)
    print("\n\n")
    
    print("rCEFailによる区分ごとのave(Rank)")
    print("----------------------------------------------------------------------------")
    print("実欠陥")
    calc_averank_based_cefail(real_faults_result_path)
    print("人工欠陥")
    calc_averank_based_cefail(artificial_faults_result_path)
    print("\n\n")
    
    print("rSTEFailによる区分ごとのrTop5-All")
    print("----------------------------------------------------------------------------")
    print("実欠陥")
    calc_rtopn_all_based_stefail(real_faults_result_path,5)
    print("人工欠陥")
    calc_rtopn_all_based_stefail(artificial_faults_result_path,5)
    print("\n\n")
    
    print("rCEFailによる区分ごとのrTop5-All")
    print("----------------------------------------------------------------------------")
    print("実欠陥")
    calc_rtopn_all_based_cefail(real_faults_result_path,5)
    print("人工欠陥")
    calc_rtopn_all_based_cefail(artificial_faults_result_path,5)
    print("\n\n")
    
    print("rSTEFailによる区分ごとのave(Rank)-All")
    print("----------------------------------------------------------------------------")
    print("実欠陥")
    calc_averank_all_based_stefail(real_faults_result_path)
    print("人工欠陥")
    calc_averank_all_based_stefail(artificial_faults_result_path)
    print("\n\n")
    
    print("rCEFailによる区分ごとのave(Rank)-All")
    print("----------------------------------------------------------------------------")
    print("実欠陥")
    calc_averank_all_based_cefail(real_faults_result_path)
    print("人工欠陥")
    calc_averank_all_based_cefail(artificial_faults_result_path)
    print("\n\n")
    
    

if __name__ == "__main__":
    # 論文中で利用するデータの生成
    rq1()
    rq2()
    rq3()

