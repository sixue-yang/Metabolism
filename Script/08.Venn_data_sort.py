# _author_ = 'sixueyang'
# _date_ = 2023/10/24 15:04
import argparse
import pandas as pd
import os


# 设置传参
def get_args():
    parser = argparse.ArgumentParser(description="代谢组分析 - 差异代谢物结果汇总")
    parser.add_argument("-is", "--inputs", nargs="*",help="各组差异分析结果", required=True)
    parser.add_argument("-l", "--change_log", help="kegg 物种注释库", required=True)
    parser.add_argument("-op", "--out_plot_data_path", help="输出绘图数据", required=True)
    parser.add_argument("-ov", "--out_result_path", help="输出各种差异代谢物编号矩阵路径", required=True)
    return parser.parse_args()


if __name__ == '__main__':
    # 设置参数
    argv = get_args()
    input_files = argv.inputs
    change_log = argv.change_log
    output = argv.out_plot_data_path
    result = argv.out_result_path

    data_list = []
    for file in input_files:
        group_name = os.path.basename(os.path.dirname(file))
        raw_data = pd.read_csv(file,sep='\t')
        if raw_data.shape[0] ==0:
            continue
        sig_df = raw_data[~(raw_data['types']=='NoSig')]
        sig_df.loc[:,group_name] = [1 for i in sig_df.index]
        data = pd.DataFrame(sig_df.loc[:,['metabolin',group_name]]).set_index('metabolin')
        data_list.append(data)
    merge = pd.concat(data_list, axis=1)
    merge = merge.fillna(0)

    merge.to_csv(output,sep='\t')

    change_log_df = pd.read_csv(change_log,sep='\t',header=None)
    change_log_df.columns = ['raw_id','new_id','kegg_id']
    raw_id_dic = change_log_df.set_index('new_id')['raw_id'].to_dict()
    merge.loc[:,'ID'] = merge.index.map(raw_id_dic)
    merge.to_csv(result,sep='\t',index=False)