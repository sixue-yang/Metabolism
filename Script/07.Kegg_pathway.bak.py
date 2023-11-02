# _author_ = 'sixueyang'
# _date_ = 2023/10/23 18:17
import pandas as pd
from bioservices import KEGG
from io import BytesIO
from PIL import Image
import argparse
import os


# 下载pathway图
def load_pathway(kegg_obj,id,outdir):
    out_path = outdir + os.sep + id + '.png'
    picture = kegg_obj.get(id, "image")
    image = Image.open(BytesIO(picture))
    # 保存图像为 PNG 格式文件
    image.save(out_path, 'PNG')

# 设置传参
def get_args():
    parser = argparse.ArgumentParser(description="代谢组分析 - 差异分析 KEGG pathway")
    parser.add_argument("-k", "--kegg_result", help="kegg 富集分析结果", required=True)
    parser.add_argument("-d", "--db", help="kegg 物种注释库", required=True)
    parser.add_argument("-o", "--out_dir", help="pathway 输出目录", required=True)
    return parser.parse_args()



if __name__ == '__main__':
    # 设置参数
    argv = get_args()
    kegg_result = argv.kegg_result
    spe_database = argv.db
    out_dir = argv.out_dir
    # print(os.path.getsize(kegg_result))
    if os.path.getsize(kegg_result) == 0:
        os.makedirs(out_dir, exist_ok=True)
    else:
        kegg_enrich_result = pd.read_csv(kegg_result,sep='\t')
        os.makedirs(out_dir, exist_ok=True)
        db_df = pd.read_csv(spe_database,sep='\t')
        kegg_map_dic = db_df.set_index('pathway')['pathway_id'].to_dict()

        kegg_enrich_result['pathway_id'] = kegg_enrich_result['ID'].map(kegg_map_dic)

        pathway_ids = kegg_enrich_result['pathway_id'].tolist()

        kegg = KEGG()
        for id_ in pathway_ids:
            load_pathway(kegg,id_,out_dir)