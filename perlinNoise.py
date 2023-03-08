class Perlin:
  def __init__(self, repeat: int=-1):
    self.repeat = repeat
    __permutation = [
      151, 160, 137, 91, 90, 15, 131, 13, 201, 95, 96, 53, 194, 233, 7, 225,
      140, 36, 103, 30, 69, 142, 8, 99, 37, 240, 21, 10, 23, 190, 6, 148, 247,
      120, 234, 75, 0, 26, 197, 62, 94, 252, 219, 203, 117, 35, 11, 32, 57,
      177, 33, 88, 237, 149, 56, 87, 174, 20, 125, 136, 171, 168, 68, 175, 74,
      165, 71, 134, 139, 48, 27, 166, 77, 146, 158, 231, 83, 111, 229, 122, 60,
      211, 133, 230, 220, 105, 92, 41, 55, 46, 245, 40, 244, 102, 143, 54, 65,
      25, 63, 161, 1, 216, 80, 73, 209, 76, 132, 187, 208, 89, 18, 169, 200,
      196, 135, 130, 116, 188, 159, 86, 164, 100, 109, 198, 173, 186, 3, 64,
      52, 217, 226, 250, 124, 123, 5, 202, 38, 147, 118, 126, 255, 82, 85, 212,
      207, 206, 59, 227, 47, 16, 58, 17, 182, 189, 28, 42, 223, 183, 170, 213,
      119, 248, 152, 2, 44, 154, 163, 70, 221, 153, 101, 155, 167, 43, 172, 9,
      129, 22, 39, 253, 19, 98, 108, 110, 79, 113, 224, 232, 178, 185, 112,
      104, 218, 246, 97, 228, 251, 34, 242, 193, 238, 210, 144, 12, 191, 179,
      162, 241, 81, 51, 145, 235, 249, 14, 239, 107, 49, 192, 214, 31, 181,
      199, 106, 157, 184, 84, 204, 176, 115, 121, 50, 45, 127, 4, 150, 254,
      138, 236, 205, 93, 222, 114, 67, 29, 24, 72, 243, 141, 128, 195, 78, 66,
      215, 61, 156, 180,
    ]
    self.__p = [__permutation[_ % 256] for _ in range(512)]

  def OctavePerlin(self,
                   x: float,
                   y: float,
                   z: float,
                   octaves: int,
                   persistence: float) -> float:
    total = 0
    frequency = 1
    amplitude = 1
    maxValue = 0
    for i in range(octaves):
      total += self.perlin(x * frequency, y * frequency,
                           z * frequency) * amplitude
      maxValue += amplitude
      amplitude *= persistence
      frequency *= 2
    return total / maxValue

  def perlin(self, x: float, y: float=0, z: float=0) -> float:
    if self.repeat > 0:
      x = x % self.repeat
      y = y % self.repeat
      z = z % self.repeat
    xi = int(x) & 255
    yi = int(y) & 255
    zi = int(z) & 255
    xf = x - int(x)
    yf = y - int(y)
    zf = z - int(z)
    u = self.fade(xf)
    v = self.fade(yf)
    w = self.fade(zf)

    aaa = self.__p[self.__p[self.__p[xi] + yi] + zi]
    aba = self.__p[self.__p[self.__p[xi] + self.inc(yi)] + zi]
    aab = self.__p[self.__p[self.__p[xi] + yi] + self.inc(zi)]
    abb = self.__p[self.__p[self.__p[xi] + self.inc(yi)] + self.inc(zi)]
    baa = self.__p[self.__p[self.__p[self.inc(xi)] + yi] + zi]
    bba = self.__p[self.__p[self.__p[self.inc(xi)] + self.inc(yi)] + zi]
    bab = self.__p[self.__p[self.__p[self.inc(xi)] + yi] + self.inc(zi)]
    bbb = self.__p[self.__p[self.__p[self.inc(xi)] + self.inc(yi)] +
                   self.inc(zi)]

    x1 = self.lerp(
      self.grad(aaa, xf, yf, zf), self.grad(baa, xf - 1, yf, zf), u)
    x2 = self.lerp(
      self.grad(aba, xf, yf - 1, zf), self.grad(bba, xf - 1, yf - 1, zf), u)
    y1 = self.lerp(x1, x2, v)
    x1 = self.lerp(
      self.grad(aab, xf, yf, zf - 1), self.grad(bab, xf - 1, yf, zf - 1), u)
    x2 = self.lerp(
      self.grad(abb, xf, yf - 1, zf - 1),
      self.grad(bbb, xf - 1, yf - 1, zf - 1), u)
    y2 = self.lerp(x1, x2, v)

    return (self.lerp(y1, y2, w) + 1) / 2

  def inc(self, num: int) -> int:
    num += 1
    if self.repeat > 0:
      num %= self.repeat
    return num

  def grad(self, hash: int, x: float, y: float, z: float) -> float:
    h = hash & 15
    u = x if h < 8 else y
    if h < 4:
      v = y
    elif h == 12 or h == 14:
      v = x
    else:
      v = z
    return (u if (h & 1) == 0 else -u) + (v if (h & 2) == 0 else -v)

  def fade(self, t: float) -> float:
    return t * t * t * (t * (t * 6 - 15) + 10)

  def lerp(self, a: float, b: float, x: float) -> float:
    return a + x * (b - a)


if __name__ == '__main__':
  import random
  prln = Perlin()
  for i in range(64):
    x = random.uniform(-1, 1)
    y = random.uniform(-1, 1)
    z = random.uniform(-1, 1)
    #print('/ --- --- ---')
    #print('rnd:x',x)
    #print('rnd:y',y)
    #print('rnd:z',z)
    print('prln:', prln.perlin(x=x, y=y, z=z))
    #print('--- --- --- /')

