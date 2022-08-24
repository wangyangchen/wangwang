# wangwang
## 2022.08.22
读论文《Regularizing Visual Semantic Embedding With Contrastive Learning for Image-Text Matching》，ConVSE论文采用了双塔的模型。
问题：在没有来自图像-图像或文本-文本对的建模约束的情况下，生成的视觉语义嵌入不可避免地面临相似图像或相似文本之间的语义错位问题。（我的理解就是，没有同模态语义的学习，语义的学习不够充分）
论文的创新点：1. 在单模态中引入了对比学习对模态内的相似图片或者相似文本进行学习。正样本的构造通过对特征进行dropout。
损失：采用了三元损失。
数据集：采用scan代码中提供的经过Faster-Rcnn提取的特征，文本为文字，输入采用了一张图5句话的方式。
训练结果：（20220815，2080ti，bs:128）Image to text: 81.4, 96.6, 98.4, 1.0, 1.7 Text to image: 62.6, 90.3, 95.3, 1.0, 4.6。
## 2022.08.2
1. 将PascalSenternce数据集通过预训练好的clip提取特征，获得512维的特征。然后将特征输入DSCMR网络，获得ImgToText0.68,TextToImg0.69,平均0.69的结果。DSCMR原论文代码提供的特征计算结果为ImgToText0.70,TextToImg0.71,平均0.70。
## 2022.08.24
1. 发现之前有个参数max_samples_per_epoch，固定为32000，对数据的训练不知道有没有影响，在尝试过程中，因为断网，训练停止。
2. 尝试将clip中提取的特征输入wjc的论文代码中，修改中发现自己的想法有问题。
