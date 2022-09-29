from PyQt5.QtCore import QObject,pyqtSignal
from GameWidget import GameWidget
from GameCore import GameCore
from GobangAlgorithm import GobangAlogrithm
'''
人机对战的模式，游戏逻辑控制
'''
class SinglePlayer(QObject):
    exit_clicked=pyqtSignal()

    def __init__(self):
        super(SinglePlayer, self).__init__()
        #游戏界面
        self.game_widget=GameWidget()
        #游戏核心对象
        self.game_core=GameCore()
        #默认棋子颜色
        self.current_color='Black'
        #定义状态 判断是否可以落子
        self.is_active=False
        #定义落子位置坐标
        self.history=[]

        #连接信号与槽函数
        #退出游戏并返回
        self.game_widget.goback_clicked.connect(self.stop_game)
        #开始游戏
        self.game_widget.start_clicked.connect(self.start_game)
        #悔棋
        self.game_widget.regret_clicked.connect(self.regret)
        #认输
        self.game_widget.lose_clicked.connect(self.lose_game)
        #落子
        self.game_widget.position_clicked.connect(self.down_chess)


    #输出相反的棋子颜色
    def get_reverse_color(self,color):
        if color=='Black':
            return 'White'
        else:
            return 'Black'

    #落子逻辑控制
    def down_chess(self,position):
        #判断胜利状态，如果已有输赢显示，无法下棋
        if not self.is_active:
            return
        #判断当前位置是否可以落子
        res=self.game_core.down_chessman(position[0],position[1],self.current_color)
        if res is None:
            return
        #执行实际的界面落子逻辑
        self.game_widget.down_chess(position,self.current_color)
        #将落子位置进行记录
        self.history.append(position)
        #切换棋子颜色
        self.current_color=self.get_reverse_color(self.current_color)
        #判断输赢状态
        if res !='Down':
            self.game_widget.show_win(res)
            #重置状态
            self.is_active=False

        #电脑落子
        self.computer_down_chess()

    #电脑落子方法
    def computer_down_chess(self):
        #1.判断电脑能否落子
        if not self.is_active:
            return
        #2.核心逻辑的落子操作，改变chessboard
        #2.1获取电脑落子的交点坐标
        #人机算法返回的最大分数的坐标位置
        position=GobangAlogrithm(self.game_core.chessboard).get_point()
        res=self.game_core.down_chessman(position[0],position[1],self.current_color)
        if res is None:
            return
        #3.实际的界面落子操作
        self.game_widget.down_chess(position,self.current_color)
        #4.改变history
        self.history.append(position)
        #5.改变颜色
        self.current_color=self.get_reverse_color(self.current_color)
        #6.判断继续游戏，还是返回输赢
        if res!='Down':
            self.game_widget.show_win(res)
            self.is_active=False

    #悔棋的逻辑
    def regret(self):
        if not self.is_active:
            return
        #判断棋盘中有没有棋子
        if len(self.history)<=0:
            return
        if not self.game_core.regret(*self.history.pop()):
            return
        self.game_widget.goback()

        if not self.game_core.regret(*self.history.pop()):
            return
        self.game_widget.goback()


    #认输，另一方获胜
    def lose_game(self):
        self.game_widget.show_win(self.get_reverse_color(self.current_color))
        #重置状态
        self.is_active=False
    #游戏初始化
    def init_game(self):
        self.history.clear()
        self.current_color='Black'
        #将二维列表重置为空
        self.game_core.init_game()
        self.game_widget.reset()  # 界面初始化

    #开始游戏
    def start_game(self):
        #展示游戏界面
        self.game_widget.show()
        self.init_game()
        self.is_active=True
    #退出游戏
    def stop_game(self):
        #发射退出信号
        print('退出游戏')
        self.exit_clicked.emit()
        self.game_widget.close()



