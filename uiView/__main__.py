from math import floor
from colorsys import hsv_to_rgb

import numpy as np

import ui

# https://yuki67.github.io/post/perlin_noise/
class Perlin():
  def __init__(self):
    self.slopes = 2 * np.random.random((256, 2)) - 1
    self.rand_index = np.zeros(512, dtype=np.int)
    for i, rand in enumerate(np.random.permutation(256)):
      self.rand_index[i] = rand
      self.rand_index[i + 256] = rand

  @staticmethod
  def lerp(a, b, t):
    return a + (b - a) * t

  def hash(self, i, j):
    # 前提条件: 0 <= i, j <= 256
    return self.rand_index[self.rand_index[i] + j]

  def fade(x):
    return 6 * x**5 - 15 * x**4 + 10 * x**3

  def weight(self, ix, iy, dx, dy):
    # 格子点(ix, iy)に対する(ix + dx, iy + dy)の重みを求める
    ix %= 256
    iy %= 256
    ax, ay = self.slopes[self.hash(ix, iy)]
    return ax * dx + ay * dy

  def noise(self, x, y):
    ix = floor(x)
    iy = floor(y)
    dx = x - floor(x)
    dy = y - floor(y)

    # 重みを求める
    w00 = self.weight(ix, iy, dx, dy)
    w10 = self.weight(ix + 1, iy, dx - 1, dy)
    w01 = self.weight(ix, iy + 1, dx, dy - 1)
    w11 = self.weight(ix + 1, iy + 1, dx - 1, dy - 1)

    # 小数部分を変換する
    wx = Perlin.fade(dx)
    wy = Perlin.fade(dy)

    # 線形補間して返す
    y0 = Perlin.lerp(w00, w10, wx)
    y1 = Perlin.lerp(w01, w11, wx)
    return (Perlin.lerp(y0, y1, wy) + 0.5)




class DrawView(ui.View):
  def __init__(self, frame, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    # todo:マス目数を変えたいとき
    self.div = 64
    # todo: 格子点の数を決めてノイズの粗さを決める
    self.w = 4
    self.width = frame[2]
    self.height = frame[3]

  def draw(self):
    x = self.width
    y = self.height
    xw = x / self.div
    # todo: 縦マス目 1/2
    yh = y / self.div / 2

    pl = Perlin()

    for i in range(self.div):
      mul = xw * i
      # todo: 縦の敷き詰めを2倍
      for j in range(self.div * 2):
        H = pl.noise((i * self.w / self.div), ((j * self.w * 2) / (self.div * 2)))

        #ui.set_color(H)
        ui.set_color(hsv_to_rgb(H, 1, 1))
        rect = ui.Path.oval(mul, xw * j, xw, xw)
        rect.fill()

class MainView(ui.View):
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.bg_color = 1
    self.tint_color = .25
    self.viewCount = 1

  def draw(self):
    self.add_subview(DrawView(self.frame))

  def layout(self):
    self.name = f'#_{self.viewCount:03d}'



def reload_view(sender):
  bv.remove_subview(bv.subviews[0])
  bv.viewCount += 1
  bv.add_subview(DrawView())


def save_view(sender):
  w_im = bv.subviews[0].frame[2]
  h_im = bv.subviews[0].frame[3]
  with ui.ImageContext(w_im, h_im) as ctx:
    bv.subviews[0].draw_snapshot()
    im = ctx.get_image()
    im.show()


bv = MainView()
reload_icon = ui.Image.named('iob:ios7_refresh_outline_32')
reload_btn = ui.ButtonItem(image=reload_icon)
reload_btn.action = reload_view

save_icon = ui.Image.named('iob:ios7_download_outline_32')
save_btn = ui.ButtonItem(image=save_icon)
save_btn.action = save_view

bv.right_button_items = [reload_btn, save_btn]

bv.present()

