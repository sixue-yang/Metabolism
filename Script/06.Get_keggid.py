# _author_ = 'sixueyang'
# _date_ = 2023/10/23 11:41
import os

import pandas as pd
import argparse

# 设置传参
def get_args():
    parser = argparse.ArgumentParser(description="代谢组分析 - 差异分析 KEGG ID 获取")
    parser.add_argument("-d", "--diff_analysis", help="检测数据", required=True)
    parser.add_argument("-l", "--change_log", help="id 替换日志路径", required=True)
    parser.add_argument("-o", "--out_id", help="kegg id输出路径", required=True)
    return parser.parse_args()

if __name__ == '__main__':
    # 设置参数
    argv = get_args()
    diff_file = argv.diff_analysis
    change_log = argv.change_log
    out_id = argv.out_id


    diff_df = pd.read_csv(diff_file,sep='\t')
    if not diff_df.empty:
        change_df = pd.read_csv(change_log,sep='\t',header=None)
        change_df.columns = ['raw_id','new_id','kegg_id']
        kegg_dic = change_df.set_index('new_id')['kegg_id'].to_dict()

        sig_df = diff_df[~(diff_df['types']=='NoSig')]
        sig_df['kegg_id'] = sig_df['metabolin'].map(kegg_dic)
        sig_df = sig_df.dropna()
        print(sig_df)
        sig_ids = sig_df['kegg_id'].tolist()
    else:
        sig_ids = []
    with open(out_id,'w') as out_obj:
        print('ID',file=out_obj,flush=True)
        for i in sig_ids:
            for id_ in i.split(';'):
                print(id_,file=out_obj,flush=True)







