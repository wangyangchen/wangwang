##文件用来获得 图片检索文本，图片检索文本，获取前十的结果。
## 输入4个文件：图片特征、文本特征、图片原来的链接、文本的原来的句子
## 输出4个文件：图片搜索文本、文本搜索图片的top10结果，以及正确的位置索引

import numpy as np
import scipy.spatial

# 需要文件: 图片特征、文本特征、图片原来的链接、文本的原来的句子
test_img_embs = np.load("E:/project/extract_feature/data/Mscoco_clip_1k/test_img_feature.npy")
test_cap_embs = np.load("E:/project/extract_feature/data/Mscoco_clip_1k/test_text_feature.npy")
test_img_flist = "E:/project/extract_feature/data/Mscoco_clip_1k/test_local.txt"
test_cap_flist = "E:/project/extract_feature/data/Mscoco_clip_1k/test_caps.txt"


# 得到的文件：计算 得到的 图片搜索文本、文本搜索图片的top10结果，以及正确的位置在哪里。
i2t_top10_file = "E:/project/extract_feature/visualization/i2t_top10_list.npy"
i2t_ind_file = "E:/project/extract_feature/visualization/i2t_ind_list.npy"
t2i_top10_file = "E:/project/extract_feature/visualization/t2i_top10_list.npy"
t2i_ind_file = "E:/project/extract_feature/visualization/t2i_ind_list.npy"

all_img_list = []
all_cap_list = []
with open(test_img_flist, "r", encoding="utf-8") as f:
    for line in f:
        all_img_list.append(line.replace("\n", ""))
with open(test_cap_flist, "r", encoding="utf-8") as f:
    for line in f:
        all_cap_list.append(line.replace("\n", ""))
all_img_list_1k = all_img_list[::5]

def visual_i2t(sims):
    npts = sims.shape[0]
    # ranks = np.zeros(npts,5)
    images_top10 = []
    images_ranks = []
    for index in range(npts):
        temp = []
        inds = np.argsort(sims[index])
        images_top10.append([all_cap_list[i] for i in list(inds[:10])])
        # ScoreS
        for i in range(5 * index, 5 * index + 5, 1):
            print(index)
            # print(inds, i, index, npts)
            tmp = np.where(inds == i)[0][0]
            temp.append(all_cap_list[tmp])
        images_ranks.append(temp)
    # <! 保存为 npy文件
    np.save(i2t_top10_file,images_top10)
    np.save(i2t_ind_file, images_ranks)

    # <! 保存为 txt文件
    # with open(i2t_top10_file,"a",encoding="utf-8") as f:
    #     f.write(str(images_top10))
    #     f.close()
    # with open(i2t_ind_file,"a",encoding="utf-8") as f:
    #     f.write(str(images_ranks))
    #     f.close()

    return images_top10, images_ranks

def visual_t2i(sims):
    npts = sims.shape[1]
    captions_top10 = []
    captions_ranks = []
   
    for index in range(npts):
        temp = []
        for i in range(5):
            inds = np.argsort(sims[5 * index + i])
            captions_top10.append([all_img_list_1k[j] for j in list(inds[:10])])
            tmp = np.where(inds == index)[0][0]
            temp.append(all_img_list_1k[tmp])
        captions_ranks.append(temp)
        
    # <! 保存为 npy文件
    np.save(t2i_top10_file, captions_top10)
    np.save(t2i_ind_file, captions_ranks)
    
    # <! 保存为 txt文件
    # with open(t2i_top10_file,"a",encoding="utf-8") as f:
    #     f.write(str(captions_top10))
    #     f.close()
    # with open(t2i_ind_file,"a",encoding="utf-8") as f:
    #     f.write(str(captions_ranks))
    #     f.close()
    return captions_top10, captions_ranks

test_img_embs=test_img_embs.reshape(-1,512)[::5]
test_cap_embs=test_cap_embs.reshape(-1,512)

sims = scipy.spatial.distance.cdist(test_img_embs, test_cap_embs, 'cosine')

visual_i2t(sims)
visual_t2i(sims.T)




