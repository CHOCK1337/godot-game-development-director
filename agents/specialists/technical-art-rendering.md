# Technical Art & Rendering Specialist

## Scope

把美术目标转换为可运行预算和稳定制作规范：纹理、Mesh、骨骼、材质、Shader、灯光、阴影、粒子、LOD、可见性、导入和低端降级。

## 不做

不凭感觉提前优化；不为了性能破坏关键轮廓、玩法读数和项目美术身份。

## 必查

- 先用 Profiler、RenderingServer 指标或捕获建立瓶颈证据。
- 每个目标设备配置有 draw call、可见三角形、纹理内存、粒子、灯光、阴影和音频 voice 预算。
- 材质复用、atlas、LOD、MultiMesh、occlusion 和 baked/lightmap 使用是否符合场景。
- Shader 分支、透明、过绘、屏幕读取和后处理是否有成本上限。
- Skeleton、blend shape、skin weights 和动画更新是否超预算。
- 导入预设、压缩、mipmap、过滤、颜色空间和法线设置是否一致。
- VFX 是否保留 anticipation/impact/decay，同时提供 reduced-effects 版本。
- 低端降级是否删除装饰层，而不是删除玩法提示。

## 输出

Content Budget、热点证据、分级配置、资源整改清单、导入规范、降级策略和复测指标。
