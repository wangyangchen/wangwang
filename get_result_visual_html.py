'''
# 创建html文件，能够显示
# image2text_html 图片检索文本的前十结果，左侧为正确的结果，右为前十的结果。
# text2image_html 文本检索图片，左侧为正确的结果，右侧为前十的结果
'''

import os
from html_utils import HTML
import numpy as np

import dominate
from dominate.tags import a
from dominate.tags import attr
from dominate.tags import br
from dominate.tags import h3
from dominate.tags import img
from dominate.tags import meta
from dominate.tags import p
from dominate.tags import source
from dominate.tags import span
from dominate.tags import table
from dominate.tags import td
from dominate.tags import tr
from dominate.tags import video

class HTML:
  """Class to save images and write texts into a single HTML file.

  It consists of functions such as <add_header> (add a text header to the
  HTML file),
  <add_images> (add a row of images to the HTML file), and <save> (save the
  HTML to the disk).
  It is based on Python library 'dominate', a Python library for creating and
  manipulating HTML documents using a DOM API.
  """

  def __init__(self, web_dir, title, refresh=0):
    """Initialize the HTML classes.

    Args:
      web_dir: a directory that stores the webpage. HTML file will
      be
      created at <web_dir>/index.html; images will be saved at
      <web_dir/images/
      title: the webpage name
      refresh: how often the website refresh itself; if 0; no
      refreshing
    """
    self.title = title
    self.web_dir = web_dir
    self.img_dir = os.path.join(self.web_dir, "images")
    if not os.path.exists(self.web_dir):
      os.makedirs(self.web_dir)
    if not os.path.exists(self.img_dir):
      os.makedirs(self.img_dir)

    self.doc = dominate.document(title=title)
    if refresh > 0:
      with self.doc.head:
        meta(http_equiv="refresh", content=str(refresh))

  def get_image_dir(self):
    """Return the directory that stores images."""
    return self.img_dir

  def add_header(self, text):
    """Insert a header to the HTML file.

    Args:
      text: the header text
    """
    with self.doc:
      h3(text)

  def add_videos(self, vids, txts, links, width=400, hidden_tag="hidden"):
    """add images to the HTML file.

    Args:
      vids: a list of image paths
      txts: a list of image names shown on the website
      links:  a list of hyperref links; when you click an
      image,
      it will redirect you to a new page
      width: width
      hidden_tag: hidden_tag
    """
    self.t = table(border=1, style="table-layout: fixed;")  # Insert a table
    self.doc.add(self.t)
    colors = ["red", "blue", "gold", "salman"]
    with self.t:
      with tr():
        for vid, txt, link in zip(vids, txts, links):
          td_style = "word-wrap: break-word; width:{}px".format(width)
          with td(style=td_style, halign="center", valign="top"):
            with p():
              vid_path = str(vid)
              if vid_path == hidden_tag:
                p_style = "font-weight: bold; width:{}px;"
                p_style = p_style.format(width * 3)
                p("hidden video", style=p_style)
              else:
                with a(href=str(link)):
                  with video():
                    attr(controls="controls", width=width)
                    source(src=vid_path, type="video/mp4")
              br()
              rows = txt.split("<br>")
              for idx, row in enumerate(rows):
                color = colors[idx % len(colors)]
                bold_tag = "<b>"
                if not row.startswith(bold_tag):
                  s_style = "color:{};".format(color)
                else:
                  s_style = "color:black; font-weight: bold;"
                  row = row[len(bold_tag):]
                span(row, style=s_style)
                br()

  def add_imagesToText(self, ims, r_txts, g_txts, links, width=400):
    """Add images retrieval texts result to the HTML file.
    Args:
      ims: a list of image paths
      r_txts: a list of right texts
      g_txts: a list of texts get form net
      links:  a list of hyperref links; when you click an image, it will redirect you to a new page
      col_num: the number of
      width: width
    """
    self.t = table(border=1, style="table-layout: fixed;")  # Insert a table
    self.doc.add(self.t)
    num = 0
    data_gen = iter(zip(ims, r_txts,g_txts, links))
    # with 建立标签的前半部分
    with self.t:
      for row in range(len(ims)):
        with tr():
          td_style = "word-wrap: break-word;"
          with td(style=td_style, halign="center", valign="top"):
            (im, r_txt, g_txt, link) = next(data_gen)
            with p():
              with a(href=link):
                num = num+1
                img(style="width:%dpx" % width, src=im,)
              br()
              for i in range(5):
                p(r_txt[i])
          with td(style=td_style, halign="center", valign="top"):
            for j in range(10):
              if g_txt[j] in r_txt:
                p(g_txt[j])
              else:
                p(g_txt[j], style="color:red")
    print("get %d image" % num)

  def add_textsToImage(self, txts, r_imgs, g_imgs, links, col_num=10, width=400):
    """Add Text retreival to Image Result to the HTML file.
    Args:
      txts: a list of captions
      r_imgs: a list of right images path
      g_imgs: a list of images path get form net
      links:  a list of hyperref links; when you click an image, it will redirect you to a new page
      col_num: the number of
      width: width
    """
    self.t = table(border=1, style="table-layout: fixed;")  # Insert a table
    self.doc.add(self.t)
    txt_num = 0
    data_gen = iter(zip(txts, r_imgs, g_imgs, links))

    with self.t:
      for row in range(len(txts)):
        txt_num=txt_num+1
        with tr():
          td_style = "word-wrap: break-word;"
          with td(style=td_style, halign="center", valign="top"):
            (txts, r_imgs, g_imgs, link) = next(data_gen)
            with p():
              p(txts)
              with a(href=link):
                img(style="width:%dpx" % width,src=r_imgs, )
              br()
          for i in range(10):
            with td(style=td_style, halign="center", valign="top"):
              with p():
                with a(href=g_imgs[i]):
                  img(style="width:%dpx" % 200, src=g_imgs[i], )
    print("get %d txt" % txt_num)

  def save(self, name):
    """Save the current content to the HMTL file."""
    html_file = "%s/%s.html" % (self.web_dir, name)
    f = open(html_file, "wt")
    f.write(self.doc.render())
    f.close()


if __name__ == "__main__":  # we show an example usage here.
    # 测试集的文本和图片地址
    test_img_flist = "E:/project/extract_feature/data/Mscoco_clip_1k/test_local.txt"
    test_cap_flist = "E:/project/extract_feature/data/Mscoco_clip_1k/test_caps.txt"
    all_img_list = [] #所有的图片地址
    all_cap_list = [] #所有的文本
    with open(test_img_flist, "r", encoding="utf-8") as f:
        for line in f:
            all_img_list.append(line.replace("\n", ""))
    with open(test_cap_flist, "r", encoding="utf-8") as f:
        for line in f:
            all_cap_list.append(line.replace("\n", ""))
    # i2t_top10 和 t2i_top10
    i2t_top10_file = "E:/project/extract_feature/visualization/i2t_top10_list.npy"
    t2i_top10_file = "E:/project/extract_feature/visualization/t2i_top10_list.npy"
    i2t_top10 = np.load(i2t_top10_file)
    t2i_top10 = np.load(t2i_top10_file)

    all_img_list_1k = all_img_list[::5]
    
    imgs, right_texts, get_texts, links1 = [], [], [], []
    img_length = len(all_img_list_1k)
    for i in range(img_length):
        imgs.append(all_img_list_1k[i])
        sentences = []
        for j in range(5):
            sentences.append(all_cap_list[i*5+j])
        right_texts.append(sentences)
        get_texts.append(i2t_top10[i])
        links1.append(all_img_list_1k[i])

    txts, right_images, get_images, links2 = [], [], [], []
    txt_length = len(all_cap_list)
    for k in range(txt_length):
        txts.append(all_cap_list[k])
        right_images.append(all_img_list[k])
        get_images.append(t2i_top10[k])
        links2.append(all_img_list[k])

    html_txt = HTML("web/", "image2text_html")
    html_txt.add_header("image2text")
    html_txt.add_imagesToText(imgs, right_texts, get_texts, links1)

    html_img = HTML("web/", "text2image_html")
    html_img.add_header("text2image")
    html_img.add_textsToImage(txts, right_images, get_images, links2)

    html_txt.save("image2text")
    html_img.save("text2image")
     
