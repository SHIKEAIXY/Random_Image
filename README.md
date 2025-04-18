# 随机图API程序

## 使用

下载Releases运行程序
 - Windows外的系统可以直接跑源码...

## 浏览器访问

```
http://127.0.0.1:5366/Fafa
```

如需外部访问需开放5366（默认端口号）

## 开发

1. 使用Gitee
```
git clone https://gitee.com/SHIKEAIXY/Random_Image
```

2. 使用Github
```
git clone https://github.com/SHIKEAIXY/Random_Image
```

## 安装依赖

#### 1在Win上安装依赖

```
pip install flask colorlog requests
```


#### 2在Linux上安装依赖

```
apt install python3-pip -y && pip install flask colorlog requests
```

## 配置

1. 打开./Random_Image/Img/

2. 放置图片
 - '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp'

 使用可爱真寻？

```
git clone --depth 1 -b Episode https://gitee.com/SHIKEAIXY/zhenxun-wallpaper-picture.git ./Random_Image/Img/ZhenXun_wallpaper
```

## 运行

#### 1在Win上运行
```
python main.py
```

#### 2在Linux上运行
```
python3 main.py
```

## 编译 
```
pyinstaller --onefile Random_Image.py
```

## 免责声明

1. 功能仅限内部交流与小范围使用，请勿将 `Random_Image` 用于任何以盈利为目的的场景；
2. 素材均来自于网络，仅供交流学习使用，如有侵权请联系，会立即删除。