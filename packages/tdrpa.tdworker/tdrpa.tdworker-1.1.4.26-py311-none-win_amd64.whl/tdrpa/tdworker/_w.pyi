import uiautomation as uia

class Window:
    @staticmethod
    def close(target: str | uia.Control) -> None:
        """
        关闭窗口

        Window.close(target)

        :param target: [必选参数]tdRPA拾取器获取的目标窗口元素特征字符串或uia目标窗口元素对象，也可选取窗口内始终存在的元素。
        :return: None
        """
    @staticmethod
    def getActive() -> uia.Control:
        """
        获取活动窗口

        Window.getActive()

        :return:control
        """
    @staticmethod
    def setActive(target: str | uia.Control) -> bool:
        """
        设置活动窗口

        Window.setActive(target)

        :param target: [必选参数]tdRPA拾取器获取的目标窗口元素特征字符串或uia目标窗口元素对象，也可选取窗口内始终存在的元素。
        :return: bool。激活成功返回True，否则返回False
        """
    @staticmethod
    def show(target: str | uia.Control, showStatus: str = 'show') -> bool:
        '''
        更改窗口显示状态

        Window.show(target, showStatus="show")

        :param target: [必选参数]tdRPA拾取器获取的目标窗口元素特征字符串或uia目标窗口元素对象，也可选取窗口内始终存在的元素。
        :param showStatus: [可选参数] 显示：\'show\' 隐藏：\'hide\' 最大化：\'max\' 最小化：\'min\' 还原：\'restore\'。默认\'show\'
        :return: bool。执行成功返回True，否则返回False
        '''
    @staticmethod
    def exists(target: str | uia.Control) -> bool:
        """
        判断窗口是否存在

        Window.exists(target)

        :param target: [必选参数]tdRPA拾取器获取的目标窗口元素特征字符串或uia目标窗口元素对象，也可选取窗口内始终存在的元素。
        :return: bool。窗口存在返回True,否则返回False
        """
    @staticmethod
    def getSize(target: str | uia.Control) -> dict:
        '''
        获取窗口大小

        Window.getSize(target)

        :param target: [必选参数]tdRPA拾取器获取的目标窗口元素特征字符串或uia目标窗口元素对象，也可选取窗口内始终存在的元素。
        :return: {"height":int, "width":int, "x":int, "y":int}
        '''
    @staticmethod
    def setSize(target: str | uia.Control, width: int, height: int) -> None:
        """
        改变窗口大小

        Window.setSize(target, 800, 600)

        :param target: [必选参数]tdRPA拾取器获取的目标窗口元素特征字符串或uia目标窗口元素对象，也可选取窗口内始终存在的元素。
        :param width: [必选参数]窗口宽度
        :param height: [必选参数]窗口高度
        :return: None
        """
    @staticmethod
    def move(target: str | uia.Control, x: int, y: int) -> None:
        """
        移动窗口位置

        Window.move(target, 0, 0)

        :param target: [必选参数]tdRPA拾取器获取的目标窗口元素特征字符串或uia目标窗口元素对象，也可选取窗口内始终存在的元素。
        :param x: [必选参数]移动到新位置的横坐标
        :param y: [必选参数]移动到新位置的纵坐标
        :return: None
        """
    @staticmethod
    def topMost(target: str | uia.Control, isTopMost: bool = True) -> bool:
        """
        窗口置顶

        Window.topMost(target, isTopMost=True)

        :param target: [必选参数]tdRPA拾取器获取的目标窗口元素特征字符串或uia目标窗口元素对象，也可选取窗口内始终存在的元素。
        :param isTopMost: [可选参数]是否使窗口置顶，窗口置顶:true 窗口取消置顶:false。默认True
        :return: bool值，设置成功返回True，否则返回False
        """
    @staticmethod
    def getClass(target: str | uia.Control) -> str:
        """
        获取窗口类名

        Window.getClass(target)

        :param target: [必选参数]tdRPA拾取器获取的目标窗口元素特征字符串或uia目标窗口元素对象，也可选取窗口内始终存在的元素。
        :return: 窗口的类名称
        """
    @staticmethod
    def getPath(target: str | uia.Control) -> str:
        """
        获取窗口程序的文件路径

        Window.getPath(target)

        :param target: [必选参数]tdRPA拾取器获取的目标窗口元素特征字符串或uia目标窗口元素对象，也可选取窗口内始终存在的元素。
        :return: 文件绝对路径
        """
    @staticmethod
    def getPID(target: str | uia.Control) -> int:
        """
        获取进程PID

        Window.getPID(target)

        :param target: [必选参数]tdRPA拾取器获取的目标窗口元素特征字符串或uia目标窗口元素对象，也可选取窗口内始终存在的元素。
        :return: PID
        """
