
#小金库 MyFund
#账单 Billsrunning 表的 属性账单编号 paybillscount，金额 money ，地点 place ，支付方式 payway，备注 remarks, 状态 status
#本程序只修改 MyFund数据库中的Billsrunning 表中的内容
import pymssql       #导入pymssql库
import tkinter       #导入tkinter库
#给tkinter.ttk内部包，并起别名为ttk
import tkinter.ttk as ttk  
#from tkinter import StringVar

#导入tkinter库中全部函数
from tkinter import * 


#定义treeview控件子节点数据清空
def delButton(tree):       
    x=tree.get_children()
    for item in x:
        tree.delete(item)


#刷新小金库系统界面
# #delete ( first, last=None )删除文本框里直接位置值
def refresh():
    entrypaybills.delete(0,END)     #delete（0，END） 删除文本框的所有内容 
    entrymoney.delete(0,END)   
    entryplace.delete(0,END)
    entryremarks.delete(0,END)
    delButton(treeview)

#查询账单信息 getpaybills()
def getpaybills():
      #链接数据库    
      db=pymssql.connect(host='127.0.0.1',user='sa',password='12345',database='MyFund',charset="UTF-8")
      print(db)
      print('连接成功!')
      # 使用cursor()方法获取操作游标
      cursor=db.cursor()
      #执行sql语句，输出全部账单信息
      sql="select * from Billsrunning"
      #如果输入框中的字符串长度大于0(输入框中间有内容)，则执行该条语句
      if len(paybillsvar.get().strip())>0:
       sql=' select * from Billsrunning where sname like '+'\'%'+paybillsvar.get().strip()+'%\''  #模糊查询
      print(sql)   #在终端输出该条sql语句
      cursor.execute(sql)      #查询账单信息
      delButton(treeview)      #清空界面文本框数据
      for row in cursor:
          treeview.insert('','end',values=row)
      cursor.close()   #关闭游标
      db.close()       #关闭数据库

#增加账单信息 addpaybills()
def addpaybills():
      #链接数据库
      conn=pymssql.connect(host='127.0.0.1',user='sa',password='12345',database='MyFund',charset="UTF-8")
      print(conn)
      print('连接成功!')
      cursor1=conn.cursor()   #获取游标
      #在程序中插入账单数据
      #sql="insert into paybillscount values('1000000001','129.1','沃尔玛','微信支付','江夏店'，'支出')"
      #插入账单信息
      mn='insert into Billsrunning values(%s,%s,%s,%s,%s,%s)'  #此处的%s为占位符，而不是格式化字符串，所以sage用%s
      #以元组的形式传入五个值
      data=(paybillsvar.get().strip(),moneyvar.get().strip(),placevar.get().strip(),paywayvar.get().strip(),remarksvar.get().strip(),statusvar.get().strip())
      try:
          cursor1.execute(mn,data)  #执行插入
          conn.commit()       #执行完成后需执行commit进行事务提交
      except:           # 发生错误时回滚
          conn.rollback()
      #输出账单信息
      sql='select * from Billsrunning'                       
      print(sql)
      cursor1.execute(sql)
      delButton(treeview)
      for row in cursor1:
          treeview.insert('','end',values=row)
      cursor1.close()   #关闭游标
      conn.close()       #关闭数据库

#删除账单信息 deletepaybills()
def deletepaybills():
      db=pymssql.connect(host='127.0.0.1',user='sa',password='12345',database='MyFund',charset="UTF-8")
      print(db)
      print('连接成功!')
      cursor=db.cursor()
      sql='delete from Billsrunning where paybillscount like '+'\'%'+paybillsvar.get().strip()+'%\''
      try:
          cursor.execute(sql)
          db.commit()
      except:
          db.rollback()
      #输出账单信息
      sql='select * from Billsrunning'                        
      print(sql)
      cursor.execute(sql)
      delButton(treeview)
      for row in cursor:
          treeview.insert('','end',values=row)
      cursor.close()   #关闭游标
      db.close()       #关闭数据库

#修改账单信息 updatepaybills()
def updatepaybills():
      db=pymssql.connect(host='127.0.0.1',user='sa',password='12345',database='MyFund',charset="UTF-8")
      print(db)
      print('连接成功!')
      cursor=db.cursor()
      
      try:
          sql='update Billsrunning set remarks=%s where paybillscount=%s'
          data=(remarksvar.get().strip(),paybillsvar.get().strip())   #以元组的形式赋值
          cursor.execute(sql,data)
          db.commit()
      except:
          db.rollback()

      sql='select * from Billsrunning'   #输出全部账单信息
      print(sql)
      cursor.execute(sql)
      delButton(treeview)
      for row in cursor:
          treeview.insert('','end',values=row)
      cursor.close()   #关闭游标
      db.close()       #关闭数据库
     
if __name__ =='__main__':


    window=tkinter.Tk()
    window.title('我的小金库系统')
    window.geometry('1100x500')

    stulist_s_Frame=tkinter.Frame(height=500,width=700)
    #stuBtn_Frame=tkinter.Frame(height=500,width=600,bg="yellow")
    stuBtn_Frame=tkinter.Frame(height=500,width=380)

    stulist_s_Frame.grid(row=0,column=0)
    stuBtn_Frame.grid(row=0,column=1)

    columns=("账单编号","消费金额","消费地点","支付方式","备注","消费类型")
    treeview=ttk.Treeview(stulist_s_Frame,height=18,show="headings",columns=columns)
    
    treeview.column("账单编号",width=100,anchor='center')
    treeview.column("消费金额",width=80,anchor='center')
    treeview.column("消费地点",width=150,anchor='center')
    treeview.column("支付方式",width=100,anchor='center')
    treeview.column("备注",width=150,anchor='center')
    treeview.column("消费类型",width=100,anchor='center')


    treeview.heading("账单编号",text="账单编号")
    treeview.heading("消费金额",text="消费金额")
    treeview.heading("消费地点",text="消费地点")
    treeview.heading("支付方式",text="支付方式")
    treeview.heading("备注",text="备注")
    treeview.heading("消费类型",text="消费类型")

    treeview.place(x=20,y=10,anchor='nw')

    labpaybills=tkinter.Label(stuBtn_Frame,text="账单编号：")
    labpaybills.place(x=20,y=30,anchor='nw')
    paybillsvar=StringVar()
    entrypaybills=tkinter.Entry(stuBtn_Frame,textvariable=paybillsvar,width=20)
    entrypaybills.place(x=80,y=30,anchor='nw')

    labmoney=tkinter.Label(stuBtn_Frame,text="消费金额：")
    labmoney.place(x=20,y=70,anchor='nw')
    moneyvar=StringVar()
    entrymoney=tkinter.Entry(stuBtn_Frame,textvariable=moneyvar,width=20)
    entrymoney.place(x=80,y=70,anchor='nw')

    labplace=tkinter.Label(stuBtn_Frame,text="消费地点：")
    labplace.place(x=20,y=110,anchor='nw')
    placevar=StringVar()
    entryplace=tkinter.Entry(stuBtn_Frame,textvariable=placevar,width=20)
    entryplace.place(x=80,y=110,anchor='nw')

    
    labpayway=tkinter.Label(stuBtn_Frame,text="支付方式：")
    labpayway.place(x=20,y=150,anchor='nw')
    paywayvar = tkinter.StringVar()     #创建变量，便于取值
    menuepayway=ttk.Combobox(stuBtn_Frame, textvariable=paywayvar,width=17)    # #创建下拉菜单
    menuepayway.place(x=80,y=150,anchor='nw')     # #将下拉菜单绑定到窗体
    menuepayway["value"] = ("微信支付", "支付宝支付", "信用卡支付","现金支付")    #给下拉菜单设定值
    menuepayway.current(1)    #设定下拉菜单的默认值为第1个，即微信支付
    menuepayway.bind("<<ComboboxSelected>>", paywayvar.get())     # #给下拉菜单绑定事件

    '''原本不是下拉框的代码（自己输入支付方式）
    labpayway=tkinter.Label(stuBtn_Frame,text="支付方式：")
    labpayway.place(x=20,y=150,anchor='nw')
    paywayvar=StringVar()
    entrypayway=tkinter.Entry(stuBtn_Frame,textvariable=paywayvar,width=20)
    entrypayway.place(x=80,y=150,anchor='nw')
    '''
    labremarks=tkinter.Label(stuBtn_Frame,text="备注：")
    labremarks.place(x=20,y=190,anchor='nw')
    remarksvar=StringVar()
    entryremarks=tkinter.Entry(stuBtn_Frame,textvariable=remarksvar,width=20)
    entryremarks.place(x=80,y=190,anchor='nw')
    
    labstatus=tkinter.Label(stuBtn_Frame,text="消费类型：")
    labstatus.place(x=20,y=230,anchor='nw')
    statusvar = tkinter.StringVar()     #创建变量，便于取值
    menuestatus=ttk.Combobox(stuBtn_Frame, textvariable=statusvar,width=17)     # #创建下拉菜单
    menuestatus.place(x=80,y=230,anchor='nw')     # #将下拉菜单绑定到窗体
    menuestatus["value"] = ("支出", "收入")    #给下拉菜单设定值
    menuestatus.current(1)    #设定下拉菜单的默认值为第1个，即支出
    menuestatus.bind("<<ComboboxSelected>>", statusvar.get())     # #给下拉菜单绑定事件
    
    '''源代码 输入框（自己输入消费类型）
    labstatus=tkinter.Label(stuBtn_Frame,text="消费类型：")
    labstatus.place(x=20,y=230,anchor='nw')
    statusvar=StringVar()
    entrystatus=tkinter.Entry(stuBtn_Frame,textvariable=statusvar,width=20)
    entrystatus.place(x=80,y=230,anchor='nw')
    '''

    text = tkinter.Text(stuBtn_Frame, width=45, height=9,bg="yellow") 
    text.place(x=20,y=270,anchor='nw')
    text.insert(INSERT, '小金库系统注意事项：\n')  #INSERT表示输入光标所在的位置，初始化后的输入光标默认在左上角
    text.insert(INSERT, '1.在文本框输入新数据时，由于账单编号为主键，故账单编号唯一\n\n') 
    text.insert(INSERT, '2.在文本框输入新数据时，可以点击刷新界面按钮，清空输入框\n\n') 
    text.insert(INSERT, '3.删除账单信息功能时是按照输入账单编号，已达到删除目的\n\n') 
    text.insert(END, '4.修改账单信息功能是按照账单编号修改备注\n') 


    stuget_Btn=tkinter.Button(stuBtn_Frame,text="    刷新界面  ",command=refresh)
    stuget_Btn.place(x=280,y=30,anchor='nw')

    stuget_Btn1=tkinter.Button(stuBtn_Frame,text="查找账单信息",command=getpaybills)
    stuget_Btn1.place(x=280,y=70,anchor='nw')

    stuget_Btn2=tkinter.Button(stuBtn_Frame,text="增加账单信息",command=addpaybills)
    stuget_Btn2.place(x=280,y=110,anchor='nw')

    stuget_Btn3=tkinter.Button(stuBtn_Frame,text="删除账单信息",command=deletepaybills)
    stuget_Btn3.place(x=280,y=150,anchor='nw')

    stuget_Btn4=tkinter.Button(stuBtn_Frame,text="修改账单信息",command=updatepaybills)
    stuget_Btn4.place(x=280,y=190,anchor='nw')

    window.mainloop()