# _author_ = 'sixueyang'
# _date_ = 2023/9/21 17:25
import pandas as pd
import os
import numpy as np
from sklearn.impute import KNNImputer
import argparse

# 缺失值填充
class Missing_value_filling:
    '''
    input:列为代谢物，行为样本
    return:填充后数据
    '''
    def __init__(self,data:pd.DataFrame):
        self.data = data

    # 过滤掉缺失值过多的代谢物 去掉缺失率在50%以上的代谢物
    def feature_remove(self,re_P=50):
        # 计算每列缺失值的百分比
        missing_percentage = (self.data.isnull().sum() / len(self.data)) * 100
        # 获取缺失值在50%以上的列名
        columns_to_drop = missing_percentage[missing_percentage >= re_P].index
        # 删除这些列
        self.data.drop(columns=columns_to_drop, inplace=True)



    def KNN_imputer(self,k=None):
        # 超参数 k值取 2/3 样本量
        if not k:
            k = int(len(self.data.index)*0.5)
            if k <= 2:
                k = 2
        knn_imputer = KNNImputer(n_neighbors=k)
        filled_data_knn = knn_imputer.fit_transform(self.data)
        return pd.DataFrame(filled_data_knn,index=self.data.index,columns=self.data.columns)

    def min_imputer(self):
        return self.data.fillna(self.data.min(axis=0))

    def median_imputer(self):
        return self.data.fillna(self.data.median(axis=0))

    def mean_imputer(self):
        return self.data.fillna(self.data.mean(axis=0))


# 按照IQR进行过滤
def data_filter(data:pd.DataFrame,threshold=1.5):
    '''
    input:列为代谢物，行为样本
    return:过滤存在异常值的代谢物
    '''
    Q1 = data.quantile(0.25, axis=0)
    Q3 = data.quantile(0.75, axis=0)

    IQR = Q3 - Q1
    outliers = ((data < (Q1 - threshold * IQR)) | (data > (Q3 + threshold * IQR)))
    data[outliers] = np.nan

    return data.dropna(axis=1)


# 对样本各个代谢物进行归一化，以消除样本间系统误差  Quantile归一化 对每个样本，所有代谢物进行归一化
def normalize(data:pd.DataFrame):
    '''
    input:列为代谢物，行为样本
    return:过滤存在异常值的代谢物
    '''
    return data.rank(axis=1) / (data.shape[1] + 1)


# 解析分组对应关系
def parse_group(path):
    map_dic = {}
    with open(path) as file_obj:
        for line in file_obj:
            tag = line.strip().split('\t')
            map_dic[tag[0]] = tag[1]

    return map_dic


# 重新拟定代谢物编号，并输出
def make_metabolism_id(metabolism:list):
    rename_list = []
    for i in range(1,len(metabolism) + 1):
        rename_list.append(f'JZ_{str(i).zfill(5)}')
    return zip(metabolism,rename_list)

# 获取每个化合物代表的kegg id
def get_kegg_id(data:pd.DataFrame,id_tag,kegg_tag):
    return data.set_index(id_tag)[kegg_tag].to_dict()


# 设置传参
def get_args():
    parser = argparse.ArgumentParser(description="代谢组分析 - 数据预处理")
    parser.add_argument("-i", "--input", help="检测数据", required=True)
    parser.add_argument("-t", "--ionmode_type", help="提取的正负离子类型",choices=['pos','neg',''], default='')
    parser.add_argument("-o", "--out_matrix", help="预处理后的矩阵", required=True)
    parser.add_argument("-l", "--change_log", help="代谢物编号重命名日志", required=True)
    parser.add_argument("-g", "--group", help="分组文件", required=True)
    parser.add_argument("-m", "--fill_model", help="填充缺失值的方法，有四种方法可选 KNN/min/median/mean", choices=['KNN','min','median','mean'],default='KNN')
    return parser.parse_args()

if __name__ == '__main__':

    # 设置参数
    argv = get_args()
    input_file = argv.input
    output_file = argv.out_matrix
    group_data = argv.group
    fill_model = argv.fill_model
    change_log = argv.change_log
    ionmode_type = argv.ionmode_type


    my_raw_data = pd.read_excel(input_file)
    if ionmode_type:
        if ionmode_type == 'pos':
            ionmode = '+'
        else:
            ionmode = '-'
        my_raw_data = my_raw_data[my_raw_data['ionmode'] == ionmode]

    kegg_dic = get_kegg_id(my_raw_data,'id','KEGG_ID')
    # 暂时针对百趣的分析报告
    ana_col = [my_raw_data.columns[0]] + list(my_raw_data.columns[13:])

    my_analysis_data = my_raw_data.loc[:,ana_col]
    my_analysis_data = my_analysis_data.set_index(my_analysis_data.columns[0]).T

    # 开始数据预处理
    miss_fill = Missing_value_filling(my_analysis_data)
    miss_fill.feature_remove()

    if fill_model == 'KNN':
        miss_fill_df = miss_fill.KNN_imputer()
    elif fill_model == 'min':
        miss_fill_df = miss_fill.min_imputer()
    elif fill_model == 'mean':
        miss_fill_df = miss_fill.mean_imputer()
    else:
        miss_fill_df = miss_fill.median_imputer()


    # 根据IQR过滤异常值
    miss_fill_iqr_df = data_filter(miss_fill_df)

    # Quantile归一化
    miss_fill_iqr_normalize_df = normalize(miss_fill_iqr_df)

    # 重命名编号
    rename_metas = []
    with open(change_log, 'w') as change_log_obj:
        for meta, rename_meta in make_metabolism_id(miss_fill_iqr_normalize_df.columns):
            print('\t'.join(map(str, [meta, rename_meta,kegg_dic[meta]])), file=change_log_obj)
            rename_metas.append(rename_meta)
    miss_fill_iqr_normalize_df.columns = rename_metas

    # 注释组别
    map_dic = parse_group(group_data)
    miss_fill_iqr_normalize_df['Group'] = miss_fill_iqr_normalize_df.index.map(map_dic)

    miss_fill_iqr_normalize_df.to_csv(output_file,sep='\t')



