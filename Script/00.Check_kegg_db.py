# _author_ = 'sixueyang'
# _date_ = 2023/10/18 11:17
import argparse
from bioservices import KEGG
import os
from io import BytesIO
from PIL import Image

# 下载pathway图
def load_pathway(kegg_obj,id,outdir):
    out_path = outdir + os.sep + id + '.png'
    picture = kegg_obj.get(id, "image")
    image = Image.open(BytesIO(picture))
    # 保存图像为 PNG 格式文件
    image.save(out_path, 'PNG')

# 设置传参
def get_args():
    parser = argparse.ArgumentParser(description="代谢组分析 - kegg库生成")
    parser.add_argument("-k", "--kegg_spe", help="kegg物种缩写代码", required=True)
    parser.add_argument("-o", "--out_dir", help="输出目录", required=True)
    return parser.parse_args()


def check_db(db_path):
    return os.path.exists(db_path)

if __name__ == '__main__':

    # 设置参数
    argv = get_args()
    kegg_spe = argv.kegg_spe
    out_dirs = argv.out_dir
    out_head = ['ID', 'COMPOUND', 'pathway', 'pathway_id', 'class']

    db_path = out_dirs + os.sep + kegg_spe + '.xls'
    pathway_dir = out_dirs + os.sep + kegg_spe
    os.makedirs(pathway_dir,exist_ok=True)
    if not check_db(db_path):
        with open(db_path,'w') as sp_obj:
            print('\t'.join(out_head),file=sp_obj,flush=True)
            k = KEGG()
            k.organism = kegg_spe
            pathway_info = k.pathwayIds
            # 打印物种和对应通路信息
            for pat in pathway_info:
                # print(pat)
                # 下载pathway图片
                load_pathway(k,pat,pathway_dir)
                data = k.parse(k.get(pat))
                # pprint(data)
                if 'CLASS' in data.keys():
                    path_class = data['CLASS']
                else:
                    path_class = ''
                if 'NAME' in data.keys():
                    path_name = data['NAME']
                else:
                    continue
                if 'COMPOUND' in data.keys():
                    coms_dic = data['COMPOUND']
                    for com in coms_dic:
                        com_name = coms_dic[com]
                        print('\t'.join([com, com_name, path_name[0], pat, path_class]), file=sp_obj, flush=True)

