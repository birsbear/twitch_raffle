import sys,PyQt5, os, csv,random
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.QtGui import QStandardItem
from twitch_sub import Ui_Form
from datetime import datetime
from dateutil.relativedelta import relativedelta
class Tier():
    def __init__(self):
        self.all = []
        self.month = {'0to2':[],'3to5':[],'6to8':[],'9to12':[],
                      '12':[],'24':[],'36':[],'48':[]}

    def month_flow(self,month,tlist):
        if month < 3:
            self.month['0to2'].append(tlist)
        elif month < 6:
            self.month['3to5'].append(tlist)
        elif month < 9:
            self.month['6to8'].append(tlist)
        elif month < 12:
            self.month['9to12'].append(tlist)
        elif month <24:
            self.month['12'].append(tlist)
        elif month <36:
            self.month['24'].append(tlist)
        elif month <48:
            self.month['36'].append(tlist)
        else:
            self.month['48'].append(tlist)

class AppWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        #self.award_list = []
        #self.award_list_numel = []
        
        #self.ui.pushButton.clicked.connect(self.on_Click)
                                ### 訂閱類型 ###
        self.ui.pushButton_4.clicked.connect(lambda : self.ui.checkBox_1.setChecked(True))
        self.ui.pushButton_4.clicked.connect(lambda : self.ui.checkBox_2.setChecked(True))
        self.ui.pushButton_4.clicked.connect(lambda : self.ui.checkBox_3.setChecked(True))
        
        self.ui.pushButton_5.clicked.connect(lambda : self.ui.lineEdit_1.setText('1.0'))
        self.ui.pushButton_5.clicked.connect(lambda : self.ui.lineEdit_2.setText('1.0'))
        self.ui.pushButton_5.clicked.connect(lambda : self.ui.lineEdit_3.setText('1.0'))
        
        self.sub_type_check = [self.ui.checkBox_1.checkState(),self.ui.checkBox_2.checkState(),self.ui.checkBox_3.checkState()]
        self.sub_type_rate = [float(self.ui.lineEdit_1.text()),float(self.ui.lineEdit_2.text()),float(self.ui.lineEdit_3.text())]
        
        self.ui.checkBox_1.stateChanged.connect(self.type_check)
        self.ui.checkBox_2.stateChanged.connect(self.type_check)
        self.ui.checkBox_3.stateChanged.connect(self.type_check)
        
        #print(self.sub_type_check,self.sub_type_rate)
        #self.ui.pushButton_5.clicked.connect(self.test)
                                ### 訂閱時間 ###        
        self.ui.pushButton_2.clicked.connect(lambda : self.ui.checkBox_7.setChecked(True))
        self.ui.pushButton_2.clicked.connect(lambda : self.ui.checkBox_8.setChecked(True))
        self.ui.pushButton_2.clicked.connect(lambda : self.ui.checkBox_9.setChecked(True))
        self.ui.pushButton_2.clicked.connect(lambda : self.ui.checkBox_10.setChecked(True))
        self.ui.pushButton_2.clicked.connect(lambda : self.ui.checkBox_11.setChecked(True))
        self.ui.pushButton_2.clicked.connect(lambda : self.ui.checkBox_12.setChecked(True))
        self.ui.pushButton_2.clicked.connect(lambda : self.ui.checkBox_13.setChecked(True))
        self.ui.pushButton_2.clicked.connect(lambda : self.ui.checkBox_14.setChecked(True))

        self.ui.pushButton_3.clicked.connect(lambda : self.ui.lineEdit_7.setText('1.0'))
        self.ui.pushButton_3.clicked.connect(lambda : self.ui.lineEdit_8.setText('1.0'))
        self.ui.pushButton_3.clicked.connect(lambda : self.ui.lineEdit_9.setText('1.0'))        
        self.ui.pushButton_3.clicked.connect(lambda : self.ui.lineEdit_10.setText('1.0'))
        self.ui.pushButton_3.clicked.connect(lambda : self.ui.lineEdit_11.setText('1.0'))
        self.ui.pushButton_3.clicked.connect(lambda : self.ui.lineEdit_12.setText('1.0'))
        self.ui.pushButton_3.clicked.connect(lambda : self.ui.lineEdit_13.setText('1.0'))
        self.ui.pushButton_3.clicked.connect(lambda : self.ui.lineEdit_14.setText('1.0'))
        
        self.ui.checkBox_7.stateChanged.connect(self.type_check)
        self.ui.checkBox_8.stateChanged.connect(self.type_check)
        self.ui.checkBox_9.stateChanged.connect(self.type_check)
        self.ui.checkBox_10.stateChanged.connect(self.type_check)
        self.ui.checkBox_11.stateChanged.connect(self.type_check)
        self.ui.checkBox_12.stateChanged.connect(self.type_check)
        self.ui.checkBox_13.stateChanged.connect(self.type_check)
        self.ui.checkBox_14.stateChanged.connect(self.type_check)
        
        self.sub_date_check = [self.ui.checkBox_7.checkState(),self.ui.checkBox_8.checkState(),self.ui.checkBox_9.checkState(),
                               self.ui.checkBox_10.checkState(),self.ui.checkBox_11.checkState(),self.ui.checkBox_12.checkState(),
                               self.ui.checkBox_13.checkState(),self.ui.checkBox_14.checkState()]
        self.sub_date_rate = [float(self.ui.lineEdit_7.text()),float(self.ui.lineEdit_8.text()),float(self.ui.lineEdit_9.text()),
                              float(self.ui.lineEdit_10.text()),float(self.ui.lineEdit_11.text()),float(self.ui.lineEdit_12.text()),
                              float(self.ui.lineEdit_13.text()),float(self.ui.lineEdit_14.text())]
        self.sub_date_dict = {0:'0to2',1:'3to5',2:'6to8',3:'9to12',4:'12',5:'24',6:'36',7:'48'}
        #print(self.sub_date_check,self.sub_date_rate)
        
                                ### 訂閱名單 ###        
        self.header_list = ['ID', '日期','Tier']
        self.table_model = PyQt5.QtGui.QStandardItemModel(self.ui.tableView_2)
        #self.table_model.setRowCount(17)
        self.table_model.setColumnCount(3)
        #self.tabel_model.setHeaderData(0,PyQt5.QtCore.Qt.)
        self.table_model.setHorizontalHeaderLabels(self.header_list)
        self.ui.tableView_2.setModel(self.table_model)
        self.ui.pushButton_6.clicked.connect(self.open_file)
                                ### 獎品名單 ###
        self.ui.pushButton.clicked.connect(self.add_award)

        self.slm_award_l = PyQt5.QtCore.QStringListModel()
        self.slm_award_ln = PyQt5.QtCore.QStringListModel()
        self.ui.listView_3.setModel(self.slm_award_ln)
        self.ui.listView_4.setModel(self.slm_award_l)      
        self.ui.listView_3.clicked.connect(self.list_click_3)
        self.ui.listView_4.clicked.connect(self.list_click_4)
        
                                ### 分子區 ###     
        self.ui.pushButton_7.clicked.connect(self.awarder)
        self.slm_awarder = PyQt5.QtCore.QStringListModel()
        self.ui.listView.setModel(self.slm_awarder)
        #self.qlist = a
        #self.slm.setStringList(self.qlist)
        #self.ui.listView.setModel(self.slm)     
        
        
        #self.ui.listWidget.addItem('123')
        #self.ui.listWidget.addItem('asd')
        self.show()
        


    #def test(self):
        

    #def check_change(self):
        
    def awarder(self):
        if self.ui.listView_4.currentIndex().row() == -1:
            return
        else:
            self.sub_type_check = [self.ui.checkBox_1.checkState(),self.ui.checkBox_2.checkState(),self.ui.checkBox_3.checkState()]
            self.sub_type_rate = [float(self.ui.lineEdit_1.text()),float(self.ui.lineEdit_2.text()),float(self.ui.lineEdit_3.text())]
            self.sub_date_check = [self.ui.checkBox_7.checkState(),self.ui.checkBox_8.checkState(),self.ui.checkBox_9.checkState(),
                               self.ui.checkBox_10.checkState(),self.ui.checkBox_11.checkState(),self.ui.checkBox_12.checkState(),
                               self.ui.checkBox_13.checkState(),self.ui.checkBox_14.checkState()]
            self.sub_date_rate = [float(self.ui.lineEdit_7.text()),float(self.ui.lineEdit_8.text()),float(self.ui.lineEdit_9.text()),
                              float(self.ui.lineEdit_10.text()),float(self.ui.lineEdit_11.text()),float(self.ui.lineEdit_12.text()),
                              float(self.ui.lineEdit_13.text()),float(self.ui.lineEdit_14.text())]
            
            

            sub_award_list = []
            tier_rate = [i/2*j for i,j in zip(self.sub_type_check, self.sub_type_rate)]
            date_rate = [i/2*j for i,j in zip(self.sub_date_check, self.sub_date_rate)]
            total_rate = [[int(100*i*j) for i in date_rate] for j in tier_rate]
            
                        

                    
            #print(total_rate)
            for i in range(8):
                rate = total_rate[0][i]
                for ind_j,j in enumerate(self.tier1.month[self.sub_date_dict[i]]):
                    ite = 0
                    while ite < rate:
                        sub_award_list.append([j[0],0,i,ind_j]) #(ID,tier,dates,indx)
                        ite+=1
            for i in range(8):
                rate = total_rate[1][i]
                for ind_j,j in enumerate(self.tier2.month[self.sub_date_dict[i]]):
                    ite = 0
                    while ite < rate:
                        sub_award_list.append([j[0],1,i,ind_j])
                        ite+=1
            for i in range(8):
                rate = total_rate[2][i]
                for ind_j,j in enumerate(self.tier3.month[self.sub_date_dict[i]]):
                    ite = 0
                    while ite < rate:
                        sub_award_list.append([j[0],2,i,ind_j])
                        ite+=1                        
            random.shuffle(sub_award_list)
            rand_system = random.SystemRandom()
            awarder = rand_system.choice(sub_award_list) 
            
            #print(self.tier3.month)
            if awarder[1] == 0:
                self.tier1.month[self.sub_date_dict[awarder[2]]].pop(awarder[3])
            elif awarder[1] == 1:    
                self.tier2.month[self.sub_date_dict[awarder[2]]].pop(awarder[3])
            else:
                self.tier3.month[self.sub_date_dict[awarder[2]]].pop(awarder[3])
            
            double_index = 0
            
            
            if self.sub_id_list.count(awarder[0]) >= 2:
                for i in range(self.sub_id_list.count(awarder[0])):
                    d_list_index = self.sub_id_list.index(awarder[0],double_index)

                    if int(self.sub_tier_list[d_list_index][-1])-1 != awarder[1]:
                        print(d_list_index)
                        print(int(self.sub_tier_list[d_list_index][-1]))
                        print(awarder[1])                        
                        if int(self.sub_tier_list[d_list_index][-1]) == 1:
                            d_list = list(self.tier1.month.values())
                            for d_i,d_n in enumerate(d_list):
                                for d_i_i , d_n_n in enumerate(d_n):
                                    if awarder[0] in d_n_n:
                                        self.tier1.month[self.sub_date_dict[d_i]].pop(d_i_i)
                        elif int(self.sub_tier_list[d_list_index][-1]) == 2:
                            d_list = list(self.tier2.month.values())
                            for d_i,d_n in enumerate(d_list):
                                for d_i_i , d_n_n in enumerate(d_n):
                                    if awarder[0] in d_n_n:
                                        self.tier2.month[self.sub_date_dict[d_i]].pop(d_i_i)
                        else:
                            d_list = list(self.tier3.month.values())
                            for d_i,d_n in enumerate(d_list):
                                for d_i_i , d_n_n in enumerate(d_n):
                                    if awarder[0] in d_n_n:
                                        self.tier3.month[self.sub_date_dict[d_i]].pop(d_i_i)
                        
                    
                    double_index = self.sub_id_list.index(awarder[0],double_index) +1
                
            self.type_check()
            index = self.ui.listView_4.currentIndex().row()
            #index_con = self.ui.listView_4.currentIndex()
            award_names = self.ui.listView_4.model().stringList()
            award_numels = self.ui.listView_3.model().stringList()                    
            awarder_list = self.ui.listView.model().stringList()
            awarder_list.append(awarder[0]+' - '+award_names[index])#+' ( Tier '+str(awarder[1]+1)+', '+self.sub_date_dict[awarder[2]]+' months)')
            self.slm_awarder.setStringList(awarder_list)
            self.ui.listView.setModel(self.slm_awarder)
            if int(award_numels[index])-1 == 0:
                award_numels.pop(index)
                award_names.pop(index)
                index = -1
            else:
                award_numels[index] = str(int(award_numels[index])-1)
            self.slm_award_ln.setStringList(award_numels)
            self.slm_award_l.setStringList(award_names)
            self.ui.listView_3.setModel(self.slm_award_ln)
            self.ui.listView_4.setModel(self.slm_award_l)
            #print(type(index))
            #self.ui.listView_3.selectionModel().setCurrentIndex(int(index),PyQt5.QtCore.QItemSelectionModel.SelectCurrent)
            #self.ui.listView_4.selectionModel().setCurrentIndex(int(index),PyQt5.QtCore.QItemSelectionModel.SelectCurrent)
            #for i in range(self.ui.tableView_2.model().rowCount()):
                #table_list.append(self.ui.tableView_2.model().item(i,0).text())
            
        
    
    def open_file(self):
        file = QFileDialog.getOpenFileUrl(self, 'Sub csv', "", "sub file (*.csv)")
        if file[0].url() == '':
            return
        
        self.name = file[0].fileName()
        file_url = file[0].url()
        self.url = file_url[8:-len(self.name)]
        os.chdir(self.url)
        self.slm_sublist = PyQt5.QtCore.QStringListModel()
        self.tier1 = Tier()
        self.tier2 = Tier()
        self.tier3 = Tier()
        with open(self.name,newline = '') as pf:
            pc = csv.reader(pf)
            #sub_list = []
            self.MainId = [0,0,'']
            for i,p in enumerate(pc):
                if i > 0:
                    day,sec = p[1][:-1].split('T')
                    dates = [int(x) for x in day.split('-')+sec.split(':')]
                    t = datetime(dates[0],dates[1],dates[2],dates[3],dates[4],dates[5])
                    t_now = datetime.now()
                    if (t_now-t).total_seconds() > self.MainId[0]:
                        self.MainId[0] = (t_now-t).total_seconds()
                        self.MainId[1] = i
                        self.MainId[2] = p[0]
        with open(self.name,newline = '') as f:
            self.sub_id_list = []
            self.sub_dates_list = []
            self.sub_tier_list = []
            c = csv.reader(f)
            for i,p in enumerate(c):
                if i > 0 and p[0] != self.MainId[2]:
                    day,sec = p[1][:-1].split('T')
                    dates = [int(x) for x in day.split('-')+sec.split(':')]
                    t = datetime(dates[0],dates[1],dates[2],dates[3],dates[4],dates[5])
                    t_now = datetime.now()
                    sub_term = relativedelta(t_now,t)

                    #sub_list.insert(-1,[p[0],p[1][:10],p[2]])
                    self.sub_id_list.append(p[0])
                    self.sub_dates_list.append(str(sub_term.years*12+sub_term.months+1)+' months')
                    self.sub_tier_list.append(p[2])
                    if int(p[2][-1]) == 1:
                        self.tier1.month_flow(sub_term.years*12+sub_term.months+1,[p[0],str(sub_term.years*12+sub_term.months+1)+' months',p[2]])
                        self.tier1.all.append([p[0],str(sub_term.years*12+sub_term.months+1),p[2]])
                    elif int(p[2][-1]) == 2:
                        self.tier2.month_flow(sub_term.years*12+sub_term.months+1,[p[0],str(sub_term.years*12+sub_term.months+1)+' months',p[2]])
                        self.tier2.all.append([p[0],str(sub_term.years*12+sub_term.months+1),p[2]])
                    else:
                        self.tier3.month_flow(sub_term.years*12+sub_term.months+1,[p[0],str(sub_term.years*12+sub_term.months+1)+' months',p[2]])
                        self.tier3.all.append([p[0],str(sub_term.years*12+sub_term.months+1),p[2]])
                    self
          

            

            #self.tier1 = [t for t in total_list]
            #for i in range(len(self.sub_id_list)):
                #self.table_model.setItem(i,0,QStandardItem(self.sub_id_list[i]))
                #self.table_model.setItem(i,1,QStandardItem(self.sub_dates_list[i]))
                #self.table_model.setItem(i,2,QStandardItem(self.sub_tier_list[i]))                
            
            #print(self.sub_type_check)
            inde = 0
            for i,c in enumerate(self.sub_type_check):
                if i == 0 and c == 2:
                    for i2,c2 in enumerate(self.sub_date_check):
                        if c2 == 2:
                            for j in self.tier1.month[self.sub_date_dict[i2]]:
                                self.table_model.setItem(inde,0,QStandardItem(j[0]))
                                self.table_model.setItem(inde,1,QStandardItem(j[1]))
                                self.table_model.setItem(inde,2,QStandardItem(j[2]))
                                inde += 1
                if i == 1 and c == 2:
                    for i2,c2 in enumerate(self.sub_date_check):
                        if c2 == 2:
                            for j in self.tier2.month[self.sub_date_dict[i2]]:
                                self.table_model.setItem(inde,0,QStandardItem(j[0]))
                                self.table_model.setItem(inde,1,QStandardItem(j[1]))
                                self.table_model.setItem(inde,2,QStandardItem(j[2]))
                                inde += 1
                if i == 2 and c == 2:
                    for i2,c2 in enumerate(self.sub_date_check):
                        if c2 == 2:
                            for j in self.tier3.month[self.sub_date_dict[i2]]:
                                self.table_model.setItem(inde,0,QStandardItem(j[0]))
                                self.table_model.setItem(inde,1,QStandardItem(j[1]))
                                self.table_model.setItem(inde,2,QStandardItem(j[2]))
                                inde += 1
                    
        #self.slm_sublist.setStringList(sub_list)
        self.ui.tableView_2.setModel(self.table_model)
        #self.ui.listView_2.setModel(self.slm_sublist)
    
    def list_click_3(self,index):
        self.ui.listView_4.selectionModel().setCurrentIndex(index,PyQt5.QtCore.QItemSelectionModel.SelectCurrent)
        #self.ui.listView_4.setSelection(index)
    def list_click_4(self,index):
        self.ui.listView_3.selectionModel().setCurrentIndex(index,PyQt5.QtCore.QItemSelectionModel.SelectCurrent)

    def type_check(self):
        self.table_model.clear()
        self.sub_type_check = [self.ui.checkBox_1.checkState(),self.ui.checkBox_2.checkState(),self.ui.checkBox_3.checkState()]
        self.sub_date_check = [self.ui.checkBox_7.checkState(),self.ui.checkBox_8.checkState(),self.ui.checkBox_9.checkState(),
                               self.ui.checkBox_10.checkState(),self.ui.checkBox_11.checkState(),self.ui.checkBox_12.checkState(),
                               self.ui.checkBox_13.checkState(),self.ui.checkBox_14.checkState()]
        inde = 0
        for i,c in enumerate(self.sub_type_check):
            if i == 0 and c == 2:
                for i2,c2 in enumerate(self.sub_date_check):
                    if c2 == 2:
                        for j in self.tier1.month[self.sub_date_dict[i2]]:
                            self.table_model.setItem(inde,0,QStandardItem(j[0]))
                            self.table_model.setItem(inde,1,QStandardItem(j[1]))
                            self.table_model.setItem(inde,2,QStandardItem(j[2]))
                            inde += 1
            if i == 1 and c == 2:
                for i2,c2 in enumerate(self.sub_date_check):
                    if c2 == 2:
                        for j in self.tier2.month[self.sub_date_dict[i2]]:
                            self.table_model.setItem(inde,0,QStandardItem(j[0]))
                            self.table_model.setItem(inde,1,QStandardItem(j[1]))
                            self.table_model.setItem(inde,2,QStandardItem(j[2]))
                            inde += 1
            if i == 2 and c == 2:
                for i2,c2 in enumerate(self.sub_date_check):
                    if c2 == 2:
                        for j in self.tier3.month[self.sub_date_dict[i2]]:
                            self.table_model.setItem(inde,0,QStandardItem(j[0]))
                            self.table_model.setItem(inde,1,QStandardItem(j[1]))
                            self.table_model.setItem(inde,2,QStandardItem(j[2]))
                            inde += 1
        self.ui.tableView_2.setModel(self.table_model)
        '''
    def date_check(self):
        self.table_model.clear()
        self.sub_type_check = [self.ui.checkBox_1.checkState(),self.ui.checkBox_2.checkState(),self.ui.checkBox_3.checkState()]
        self.sub_date_check = [self.ui.checkBox_7.checkState(),self.ui.checkBox_8.checkState(),self.ui.checkBox_9.checkState(),
                               self.ui.checkBox_10.checkState(),self.ui.checkBox_11.checkState(),self.ui.checkBox_12.checkState(),
                               self.ui.checkBox_13.checkState(),self.ui.checkBox_14.checkState()]
        inde = 0
        for i,c in enumerate(self.sub_type_check):
            if i == 0 and c == 2:
                for i2,c2 in enumerate(self.sub_date_check):
                    if c2 == 2:
                        for j in self.tier1.month[self.sub_date_dict[i2]]:
                            self.table_model.setItem(inde,0,QStandardItem(j[0]))
                            self.table_model.setItem(inde,1,QStandardItem(j[1]))
                            self.table_model.setItem(inde,2,QStandardItem(j[2]))
                            inde += 1
            if i == 1 and c == 2:
                for i2,c2 in enumerate(self.sub_date_check):
                    if c2 == 2:
                        for j in self.tier2.month[self.sub_date_dict[i2]]:
                            self.table_model.setItem(inde,0,QStandardItem(j[0]))
                            self.table_model.setItem(inde,1,QStandardItem(j[1]))
                            self.table_model.setItem(inde,2,QStandardItem(j[2]))
                            inde += 1
            if i == 2 and c == 2:
                for i2,c2 in enumerate(self.sub_date_check):
                    if c2 == 2:
                        for j in self.tier3.month[self.sub_date_dict[i2]]:
                            self.table_model.setItem(inde,0,QStandardItem(j[0]))
                            self.table_model.setItem(inde,1,QStandardItem(j[1]))
                            self.table_model.setItem(inde,2,QStandardItem(j[2]))
                            inde += 1
        self.ui.tableView_2.setModel(self.table_model)
        '''
    def add_award(self):
        if self.ui.lineEdit_4.text() == '' or self.ui.lineEdit_4.text().isspace() == True:
            return
        elif self.ui.lineEdit_5.text() == '' or self.ui.lineEdit_5.text().isspace() == True or self.ui.lineEdit_5.text().isdigit() == False:
            return
        else:
            award_name = self.ui.lineEdit_4.text()
            award_numel = self.ui.lineEdit_5.text()
            #self.award_list.append(award_name)
            #self.award_list_numel.append(award_numel)
            lv3 = self.ui.listView_3.model().stringList()
            lv4 = self.ui.listView_4.model().stringList()
            lv4.append(award_name)
            lv3.append(award_numel)
            self.ui.lineEdit_4.setText('')
            self.ui.lineEdit_5.setText('')
            self.slm_award_l.setStringList(lv4)
            self.slm_award_ln.setStringList(lv3)
            self.ui.listView_3.setModel(self.slm_award_ln)
            self.ui.listView_4.setModel(self.slm_award_l)
            
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = AppWindow()
    w.show()
    sys.exit(app.exec_())