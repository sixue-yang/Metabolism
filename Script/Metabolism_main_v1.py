# _author_ = 'sixueyang'
# _date_ = 2023/11/1 9:44
import subprocess as sp
import yaml
import sys
import os
import argparse


# 创建qsub投递日志目录
def check_out_Dir(yaml_path):
    with open(yaml_path, 'r') as config_file:
        config_data = yaml.safe_load(config_file)
        for rule in config_data:
            if 'output' in config_data[rule]:
                strout = os.path.join(os.path.dirname(os.path.dirname(config_data[rule]['output'])), rule)
                os.makedirs(strout,exist_ok=True)

# 设置传参
def get_args():
    parser = argparse.ArgumentParser(description="代谢组 - 高级分析")
    parser.add_argument("-i", "--input", help="下机比对数据 -- 百趣", required=True)
    parser.add_argument("-m", "--miss_model", help="缺失值填充方法",choices=['KNN','min','median','mean'], default='KNN')
    parser.add_argument("-c", "--compare_list", help="比较组合列表",default='')
    parser.add_argument("-db", "--dbpath", help="数据库所在路径",default=os.path.join(os.path.dirname(os.path.dirname(sys.argv[0])),'DB'))
    parser.add_argument("-g", "--group", help="样本分群文件", required=True)
    parser.add_argument("-a", "--adjust_model", help="p-value 矫正方法", default='none')
    parser.add_argument("-n", "--n_cluster", help="kmeans 聚类簇数量",type=int, default=9)
    parser.add_argument("-S", "--spe", help="KEGG 建库使用的物种缩写", default='osa')
    parser.add_argument("-job", "--max_jobs", help="最大并行任务数，默认100", type=int,default=100)
    parser.add_argument("-wt", "--wait_time", help="任务执行后等待结果的时间，默认300秒", type=int, default=300)
    parser.add_argument("-sn", "--snakemake", help="snakemake软件路径", default='/work1/Users/yangsixue/tools/conda/envs/snakemake/bin/snakemake')
    return parser.parse_args()

if __name__ == '__main__':
    argv = get_args()
    input = argv.input
    miss_model = argv.miss_model
    compare_list = argv.compare_list
    dbpath = argv.dbpath
    group = argv.group
    adjust_model = argv.adjust_model
    spe = argv.spe
    n_cluster = argv.n_cluster
    job = argv.max_jobs
    wait_time = argv.wait_time
    snakemake = argv.snakemake

    cluster_contig_path = os.path.join(os.path.dirname(sys.argv[0]),'cluster.yml')
    # 创建投递标准输出目录
    check_out_Dir(cluster_contig_path)
    # 写项目配置文件
    input_configfile = {
        'input': input,
        'group_list': group,
        'species': spe,
        'missing_value_filling_model': miss_model,
        'DB_dir': dbpath,
        'compare_list': compare_list,
        'adjust_model': adjust_model,
        'n_cluster': n_cluster,
        'script_dir': os.path.dirname(sys.argv[0])
    }
    with open('input_config.yaml', 'w') as config_file:
        yaml.dump(input_configfile, config_file)

    snakemake_script = os.path.join(os.path.dirname(sys.argv[0]),'Metabolism.snakemake')
    sub_cmd = f'''{snakemake} -s {snakemake_script} --configfile input_config.yaml --cluster-config {cluster_contig_path} --cluster "qsub -V -cwd -l vf={{cluster.memory}},p={{cluster.threads}} -q all.q,big -o {{cluster.output}} -e {{cluster.error}}" --jobs {job} --latency-wait {wait_time} --keep-going
    '''
    print('命令',sub_cmd)
    sp.call(sub_cmd,shell=True)

