
# Visual Studio Project Generator

## 目的

随着源代码文件数量和目录结构复杂度的增加，由其他 IDE 转至 Visual Studio 时手动创建解决方案（Solution）是一件非常痛苦的事情，因为不仅要手动创建工程（Project），也要手动创建筛选器（Filter）以维持工程目录结构。
本工具的目标是简化以上过程，通过一些简单的配置，自动生成 Visual Studio 2015 解决方案文件和工程文件。

## 原理

本工具的原理是扫描源文件目录，根据目录结构创建 *.vcxproj, *.vcxproj.filters 以及 *.sln 文件

## 准备

当源文件目录在 Samba 服务器上时，Visual Studio 自带的 IntelliSense 和数据库功能在打开大型项目时会造成卡死，因此最好禁用，如果源文件目录在本地则可忽略。

### 禁用 IntelliSense

    Text Editor -> C/C++ -> IntelliSense -> Disable IntelliSense := True

### 禁用 Database

    Text Editor -> C/C++ -> Browsing/Navigation -> Disable Database := True

## 用法

1.  修改 `config.json`
	- `ext_exclude` 排除特定扩展名的文件，例如 '.o'
	- `dir_exclude` 排除特定名称的目录，例如 '.svn'
	- `src_path` 源代码目录
	- `output_path` 解决方案输出目录
	- `solution_name` 解决方案名称
	- `single_project` 是否为单工程，true 则对于源代码目录中的每个子目录建立工程文件，false 则将所有目录加入同一个工程
2. 运行 `vs_proj_gen.exe` 或者 `python vs_proj_gen.py`（后者需要安装 python2.7 和 scandir 依赖库）
3. 用 Visual Studio 打开生成的解决方案文件 `.sln`，耐心等待 Visual Studio 更新完成
4. 享受用强大的 IDE CODING 的乐趣吧

