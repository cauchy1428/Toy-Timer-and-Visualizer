# 计时器~记录并可视化你的学习时间
一个用Python写的小玩具。能让你非常轻松地记录每天、每周、每月的学习时间，并以日历热力图的形式可视化地呈现它们。

效果如下：

<img src=".\pic\visualize.png"> 

## 特性
- 运行`Tracker.py`来启动计时和停止计时
- 能够记录每日、每周、每月的时长，并自动处理跨天、跨周、跨月、跨年的情况
- 运行`Visualizer.py`来可视化时长

## 依赖
需要安装下面的包：
* pandas
* plotly
* plotly_calplot

```sh
pip install pandas plotly plotly_calplot
```

## 使用方法
1. **启动计时器：** 运行`Recorder.py`，开始计时
2. **停止计时器：** 再次运行`Recorder.py`
3. **时长小结：** 停止计时器时，显示当前周和月的时长
4. **可视化时长：** 运行`Visualizer.py`，根据每日时长创建日历热力图

## 运行原理
看看有没有`start_time.json`。

如果没找到，就创建它，在里面记录开始时间；如果找到了，就作差得到本次时长，更新本日、本周、本月时长，再把`start_time.json`删掉。

## 文件结构
```
.
├── Tracker.py
├── Visualizer.py
├── data/
│   ├── start_time.json # 
│   ├── date_time_.json
│   ├── monthly_weekly_total.json
├── README.md
```

记得把原有的`data`文件夹删掉，里面是我的测试数据。

## bug
创建日历热力图的时候，`plotly_calplot`这个包为了保证热力图是一个大矩形，
会自动在今年开始之前塞一些去年的日子，在今年结束之后塞一些明年的日子。
如果你把鼠标移动到这些被塞进来的日子上，就会看到一些奇怪的结果：

<img src=".\pic\bug.png"> 

另外它应该不能处理跨时区的情况：D

## 别的什么
请随意使用。如果这个小玩具能帮到你，我就很开心了！

可以通过这个邮箱联系我：<ynhan@zju.edu.cn>