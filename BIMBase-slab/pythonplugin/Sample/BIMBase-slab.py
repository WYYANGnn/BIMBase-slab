from pyp3d import *
import math
# 定义参数化模型
class GAIBAN(Component):
    # 定义各个参数及其默认值
    def __init__(self):
        Component.__init__(self)
        self['跨度1'] = Attr(5400, obvious = True, combo = [5400,4300])
        # obvious 属性的可见性 True时可见，False为不可见。默认为False
        # readonly 属性的只读性 True时不可调，为置灰状态，False为可调状态。默认为False
        self['跨度2'] = Attr(1000, obvious = True, combo = [1000,3300])
        self['高'] = Attr(170, obvious = True, combo = [120,170,200,250])
        self['混凝土板'] = Attr(None, show = True)
        self['保护层厚度'] = Attr(35, obvious = True)
        self['钢筋直径'] = Attr(12, obvious = True)
        self['钢筋间距'] = Attr(150, obvious = True)
        self['钢筋'] = Attr(None, show = True)

        self['平均温升热电偶'] = Attr(None, show = True)
        self['最高温度热电偶'] = Attr(None, show = True)
        self['挠度测量位置'] = Attr(None, show = True)
        self.replace()
    @export
    # 模型造型
    def replace(self): 
        # 设置变量，同时调用参数(简化书写过程)
        L = self['跨度1']
        W = self['跨度2']
        H = self['高']
        c = self['保护层厚度']
        d = self['钢筋直径']
        gj_down1 = c+d/2
        gj_down2 = c+d*3/2
       
        # 绘制模型
        TestCube = scale(L,W,H) * Cube().color(1,1,1,0)
        self['混凝土板'] = TestCube
        gj1 = Cone(Vec3(0,0,0),Vec3(L,0,0),d/2,d/2).color(210/255,1/255,3/255,1)
        gj2 = Cone(Vec3(0,0,0),Vec3(0,W,0),d/2,d/2).color(210/255,1/255,3/255,1)

        test_GJ1 = Array(gj1)
        test_GJ2 = Array(gj2)
        n = self['钢筋间距']
        N1 = math.floor(W/n)
        N2 = math.floor(L/n)
        bj1 = (W-(N1-1)*n)/2
        bj2 = (L-(N2-1)*n)/2
        # for 循环  线性排布
        for i in linspace(Vec3(0,bj1,0),Vec3(0,bj1+n*(N1-1),0),N1):
            test_GJ1.append(translate(i))
        for j in linspace(Vec3(bj2,0,0),Vec3(bj2+n*(N2-1),0,0),N2):
            test_GJ2.append(translate(j))
        self['钢筋'] = trans(0,0,gj_down1)*test_GJ1 + trans(0,0,H-gj_down1)*test_GJ1 + trans(0,0,gj_down2)*test_GJ2 + trans(0,0,H-gj_down2)*test_GJ2
        #仪器布置
        r = 20
        T1 = trans(L/4,W/4,H) * scale(r) * Sphere().color(6/255,2/255,112/255,1)
        T2 = trans(L/4,W*3/4,H) * scale(r) * Sphere().color(6/255,2/255,112/255,1)
        T3 = trans(L/2,W/2,H) * scale(r) * Sphere().color(6/255,2/255,112/255,1)
        T4 = trans(L*3/4,W/4,H) * scale(r) * Sphere().color(6/255,2/255,112/255,1)
        T5 = trans(L*3/4,W*3/4,H) * scale(r) * Sphere().color(6/255,2/255,112/255,1)
        self['平均温升热电偶'] = Combine(T1,T2,T3,T4,T5)
        # DJ1 = trans(L/4,W/4,c) * scale(r) * Sphere().color(210/255,1/255,3/255,1) #S200
        # DJ1 = trans(L*3/4,W/4,c) * scale(r) * Sphere().color(210/255,1/255,3/255,1) #S170
        DJ1 = trans(L*3/4,W/2,c) * scale(r) * Sphere().color(210/255,1/255,3/255,1) #D170
        DJ2 = trans(L/2,W/2,c) * scale(r) * Sphere().color(210/255,1/255,3/255,1)   
        # DJ3 = trans(L*3/4,W*3/4,c) * scale(r) * Sphere().color(210/255,1/255,3/255,1) #S200
        # DJ3 = trans(L*1/4,W*3/4,c) * scale(r) * Sphere().color(210/255,1/255,3/255,1)   #S170
        DJ3 = trans(L*1/4,W/2,c) * scale(r) * Sphere().color(210/255,1/255,3/255,1) #D170
        BZ = trans(L/2,W/2,H/2) * scale(r) * Sphere().color(210/255,1/255,3/255,1)
        # MJ = trans(L/2,W/2,H-c) * scale(r) * Sphere().color(210/255,1/255,3/255,1)    #S
        MJ = trans(L/4,W/2,H-c) * scale(r) * Sphere().color(210/255,1/255,3/255,1)  #170
        self['最高温度热电偶'] = Combine(DJ1,DJ2,DJ3,BZ,MJ)
        ND = trans(L/2-r,W/2-r,H) * scale(2*r) *Cube().color(139/255,101/255,8/255,0.5)
        self['挠度测量位置'] = ND

# 输出模型
if __name__ == "__main__":
    FinalGeometry = GAIBAN()
    place(FinalGeometry)
