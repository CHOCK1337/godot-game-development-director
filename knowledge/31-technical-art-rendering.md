# Technical Art & Rendering

先测量后优化。预算按目标设备和代表压力场景制定，不用统一数字套所有游戏。

## Budget domains

Draw calls、visible triangles、texture memory、material count、transparent overdraw、lights/shadows、particles、bones/skinned meshes、shader cost、animation updates、audio voices。

## Degradation order

先删除装饰粒子、远距阴影、次级反射、装饰骨骼和非关键后处理；最后才动影响玩法轮廓、危险提示和交互状态的内容。
