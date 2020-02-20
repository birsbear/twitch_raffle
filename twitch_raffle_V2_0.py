import sys,PyQt5, os, csv,random
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QMessageBox
from PyQt5.QtGui import QStandardItem
from PyQt5 import QtGui
from twitch_sub import Ui_Form
from datetime import datetime
from dateutil.relativedelta import relativedelta
class Tier():
    def __init__(self):
        self.all = []
        self.month = {'0to2':[],'3to5':[],'6to8':[],'9to12':[],'12':[],'24':[],'36':[],'48':[]}
        self.tenure = {'0to2':[],'3to5':[],'6to8':[],'9to12':[],'12':[],'24':[],'36':[],'48':[]}
        self.streak = {'0to2':[],'3to5':[],'6to8':[],'9to12':[],'12':[],'24':[],'36':[],'48':[]}
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
            
    def tenure_flow(self,month,tlist):
        if month < 3:
            self.tenure['0to2'].append(tlist)
        elif month < 6:
            self.tenure['3to5'].append(tlist)
        elif month < 9:
            self.tenure['6to8'].append(tlist)
        elif month < 12:
            self.tenure['9to12'].append(tlist)
        elif month <24:
            self.tenure['12'].append(tlist)
        elif month <36:
            self.tenure['24'].append(tlist)
        elif month <48:
            self.tenure['36'].append(tlist)
        else:
            self.tenure['48'].append(tlist)
            
    def streak_flow(self,month,tlist):
        if month < 3:
            self.streak['0to2'].append(tlist)
        elif month < 6:
            self.streak['3to5'].append(tlist)
        elif month < 9:
            self.streak['6to8'].append(tlist)
        elif month < 12:
            self.streak['9to12'].append(tlist)
        elif month <24:
            self.streak['12'].append(tlist)
        elif month <36:
            self.streak['24'].append(tlist)
        elif month <48:
            self.streak['36'].append(tlist)
        else:
            self.streak['48'].append(tlist)
            
class AppWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.path = os.getcwd()
        self.ui.new_award_n.setValidator(QtGui.QIntValidator())
        self.ui.lineEdit_1.setValidator(QtGui.QDoubleValidator())
        self.ui.lineEdit_2.setValidator(QtGui.QDoubleValidator())
        self.ui.lineEdit_3.setValidator(QtGui.QDoubleValidator())
        self.ui.lineEdit_t1.setValidator(QtGui.QDoubleValidator())
        self.ui.lineEdit_t2.setValidator(QtGui.QDoubleValidator())
        self.ui.lineEdit_t3.setValidator(QtGui.QDoubleValidator())
        self.ui.lineEdit_t4.setValidator(QtGui.QDoubleValidator())
        self.ui.lineEdit_t5.setValidator(QtGui.QDoubleValidator())
        self.ui.lineEdit_t6.setValidator(QtGui.QDoubleValidator())
        self.ui.lineEdit_t7.setValidator(QtGui.QDoubleValidator())
        self.ui.lineEdit_t8.setValidator(QtGui.QDoubleValidator())
        #self.award_list = []
        #self.award_list_numel = []
        
        #self.ui.add_award.clicked.connect(self.on_Click)
                                ### 訂閱類型 ###
        self.ui.tier_all.clicked.connect(lambda : self.ui.checkBox_1.setChecked(True))
        self.ui.tier_all.clicked.connect(lambda : self.ui.checkBox_2.setChecked(True))
        self.ui.tier_all.clicked.connect(lambda : self.ui.checkBox_3.setChecked(True))
        
        self.ui.tier_reset.clicked.connect(lambda : self.ui.lineEdit_1.setText('1.0'))
        self.ui.tier_reset.clicked.connect(lambda : self.ui.lineEdit_2.setText('1.0'))
        self.ui.tier_reset.clicked.connect(lambda : self.ui.lineEdit_3.setText('1.0'))
        
        self.sub_type_check = [self.ui.checkBox_1.checkState(),self.ui.checkBox_2.checkState(),self.ui.checkBox_3.checkState()]
        self.sub_type_rate = [float(self.ui.lineEdit_1.text()),float(self.ui.lineEdit_2.text()),float(self.ui.lineEdit_3.text())]
        
        self.ui.checkBox_1.stateChanged.connect(self.type_check)
        self.ui.checkBox_2.stateChanged.connect(self.type_check)
        self.ui.checkBox_3.stateChanged.connect(self.type_check)
        
        #print(self.sub_type_check,self.sub_type_rate)
        #self.ui.tier_reset.clicked.connect(self.test)
                                ### 訂閱時間 ###        
        self.ui.time_all.clicked.connect(lambda : self.ui.checkBox_t1.setChecked(True))
        self.ui.time_all.clicked.connect(lambda : self.ui.checkBox_t2.setChecked(True))
        self.ui.time_all.clicked.connect(lambda : self.ui.checkBox_t3.setChecked(True))
        self.ui.time_all.clicked.connect(lambda : self.ui.checkBox_t4.setChecked(True))
        self.ui.time_all.clicked.connect(lambda : self.ui.checkBox_t5.setChecked(True))
        self.ui.time_all.clicked.connect(lambda : self.ui.checkBox_t6.setChecked(True))
        self.ui.time_all.clicked.connect(lambda : self.ui.checkBox_t7.setChecked(True))
        self.ui.time_all.clicked.connect(lambda : self.ui.checkBox_t8.setChecked(True))

        self.ui.time_reset.clicked.connect(lambda : self.ui.lineEdit_t1.setText('1.0'))
        self.ui.time_reset.clicked.connect(lambda : self.ui.lineEdit_t2.setText('1.0'))
        self.ui.time_reset.clicked.connect(lambda : self.ui.lineEdit_t3.setText('1.0'))        
        self.ui.time_reset.clicked.connect(lambda : self.ui.lineEdit_t4.setText('1.0'))
        self.ui.time_reset.clicked.connect(lambda : self.ui.lineEdit_t5.setText('1.0'))
        self.ui.time_reset.clicked.connect(lambda : self.ui.lineEdit_t6.setText('1.0'))
        self.ui.time_reset.clicked.connect(lambda : self.ui.lineEdit_t7.setText('1.0'))
        self.ui.time_reset.clicked.connect(lambda : self.ui.lineEdit_t8.setText('1.0'))
        
        self.ui.checkBox_t1.stateChanged.connect(self.type_check)
        self.ui.checkBox_t2.stateChanged.connect(self.type_check)
        self.ui.checkBox_t3.stateChanged.connect(self.type_check)
        self.ui.checkBox_t4.stateChanged.connect(self.type_check)
        self.ui.checkBox_t5.stateChanged.connect(self.type_check)
        self.ui.checkBox_t6.stateChanged.connect(self.type_check)
        self.ui.checkBox_t7.stateChanged.connect(self.type_check)
        self.ui.checkBox_t8.stateChanged.connect(self.type_check)
        
        self.sub_date_check = [self.ui.checkBox_t1.checkState(),self.ui.checkBox_t2.checkState(),self.ui.checkBox_t3.checkState(),
                               self.ui.checkBox_t4.checkState(),self.ui.checkBox_t5.checkState(),self.ui.checkBox_t6.checkState(),
                               self.ui.checkBox_t7.checkState(),self.ui.checkBox_t8.checkState()]
        self.sub_date_rate = [float(self.ui.lineEdit_t1.text()),float(self.ui.lineEdit_t2.text()),float(self.ui.lineEdit_t3.text()),
                              float(self.ui.lineEdit_t4.text()),float(self.ui.lineEdit_t5.text()),float(self.ui.lineEdit_t6.text()),
                              float(self.ui.lineEdit_t7.text()),float(self.ui.lineEdit_t8.text())]
        self.sub_date_dict = {0:'0to2',1:'3to5',2:'6to8',3:'9to12',4:'12',5:'24',6:'36',7:'48'}
        #print(self.sub_date_check,self.sub_date_rate)
        
                                ### 訂閱名單 ###        
        self.header_list = ['ID', '日期','Tier']
        self.table_model = PyQt5.QtGui.QStandardItemModel(self.ui.sub_list)
        #self.table_model.setRowCount(17)
        self.table_model.setColumnCount(3)
        #self.tabel_model.setHeaderData(0,PyQt5.QtCore.Qt.)
        self.table_model.setHorizontalHeaderLabels(self.header_list)
        self.ui.sub_list.setModel(self.table_model)
        self.ui.load_sub.clicked.connect(self.open_file)
        self.ui.tenure.toggled.connect(lambda:self.type_check())
        self.ui.streak.toggled.connect(lambda:self.type_check())
                                ### 獎品名單 ###
        self.ui.add_award.clicked.connect(self.add_award)
        self.ui.load_award.clicked.connect(self.load_award)

        self.slm_award_l = PyQt5.QtCore.QStringListModel()
        self.slm_award_ln = PyQt5.QtCore.QStringListModel()
        self.ui.award_list_c.setModel(self.slm_award_ln)
        self.ui.award_list_n.setModel(self.slm_award_l)      
        self.ui.award_list_c.clicked.connect(self.list_click_3)
        self.ui.award_list_n.clicked.connect(self.list_click_4)
        
                                ### 分子區 ###     
        self.ui.awarder_out.clicked.connect(self.awarder)
        self.slm_awarder = PyQt5.QtCore.QStringListModel()
        self.ui.awarder_list.setModel(self.slm_awarder)
        self.ui.clear_awarder.clicked.connect(self.awarder_clear)
        self.ui.save_awarder.clicked.connect(self.out_awarder)
        #self.qlist = a
        #self.slm.setStringList(self.qlist)
        #self.ui.awarder_list.setModel(self.slm)     
        
        
        self.show()
        
    def awarder_clear(self):
        self.slm_awarder = PyQt5.QtCore.QStringListModel()
        self.ui.awarder_list.setModel(self.slm_awarder)

    #def test(self):
        

    #def check_change(self):
        
    def awarder(self):
        if self.ui.award_list_n.currentIndex().row() == -1:
            return
        else:
            self.sub_type_check = [self.ui.checkBox_1.checkState(),self.ui.checkBox_2.checkState(),self.ui.checkBox_3.checkState()]
            self.sub_type_rate = [float(self.ui.lineEdit_1.text()),float(self.ui.lineEdit_2.text()),float(self.ui.lineEdit_3.text())]
            self.sub_date_check = [self.ui.checkBox_t1.checkState(),self.ui.checkBox_t2.checkState(),self.ui.checkBox_t3.checkState(),
                               self.ui.checkBox_t4.checkState(),self.ui.checkBox_t5.checkState(),self.ui.checkBox_t6.checkState(),
                               self.ui.checkBox_t7.checkState(),self.ui.checkBox_t8.checkState()]
            self.sub_date_rate = [float(self.ui.lineEdit_t1.text()),float(self.ui.lineEdit_t2.text()),float(self.ui.lineEdit_t3.text()),
                              float(self.ui.lineEdit_t4.text()),float(self.ui.lineEdit_t5.text()),float(self.ui.lineEdit_t6.text()),
                              float(self.ui.lineEdit_t7.text()),float(self.ui.lineEdit_t8.text())]
            
            

            sub_award_list = []
            tier_rate = [i/2*j for i,j in zip(self.sub_type_check, self.sub_type_rate)]
            date_rate = [i/2*j for i,j in zip(self.sub_date_check, self.sub_date_rate)]
            total_rate = [[int(100*i*j) for i in date_rate] for j in tier_rate]
            #print(total_rate)
            if self.ui.tenure.isChecked():
                for i in range(8):
                    rate = total_rate[0][i]
                    for ind_j,j in enumerate(self.tier1.tenure[self.sub_date_dict[i]]):
                        ite = 0
                        while ite < rate:
                            sub_award_list.append([j[0],0,i,ind_j]) #(ID,tier,dates,indx)
                            ite+=1
                for i in range(8):
                    rate = total_rate[1][i]
                    for ind_j,j in enumerate(self.tier2.tenure[self.sub_date_dict[i]]):
                        ite = 0
                        while ite < rate:
                            sub_award_list.append([j[0],1,i,ind_j])
                            ite+=1
                for i in range(8):
                    rate = total_rate[2][i]
                    for ind_j,j in enumerate(self.tier3.tenure[self.sub_date_dict[i]]):
                        ite = 0
                        while ite < rate:
                            sub_award_list.append([j[0],2,i,ind_j])
                            ite+=1    
            elif self.ui.streak.isChecked():
                for i in range(8):
                    rate = total_rate[0][i]
                    for ind_j,j in enumerate(self.tier1.streak[self.sub_date_dict[i]]):
                        ite = 0
                        while ite < rate:
                            sub_award_list.append([j[0],0,i,ind_j]) #(ID,tier,dates,indx)
                            ite+=1
                for i in range(8):
                    rate = total_rate[1][i]
                    for ind_j,j in enumerate(self.tier2.streak[self.sub_date_dict[i]]):
                        ite = 0
                        while ite < rate:
                            sub_award_list.append([j[0],1,i,ind_j])
                            ite+=1
                for i in range(8):
                    rate = total_rate[2][i]
                    for ind_j,j in enumerate(self.tier3.streak[self.sub_date_dict[i]]):
                        ite = 0
                        while ite < rate:
                            sub_award_list.append([j[0],2,i,ind_j])
                            ite+=1
            else:
                return
                        
            random.shuffle(sub_award_list)
            rand_system = random.SystemRandom()
            awarder = rand_system.choice(sub_award_list) 
            ### tier1 ###
            for i in self.tier1.tenure:
                if list(filter(lambda j:j[0]==awarder[0],self.tier1.tenure[i])) != []:
                    w.tier1.tenure[i].pop(self.tier1.tenure[i].index(list(filter(lambda j:j[0]==awarder[0],self.tier1.tenure[i]))[0]))
            for i in self.tier1.streak:
                if list(filter(lambda j:j[0]==awarder[0],self.tier1.streak[i])) != []:
                    w.tier1.streak[i].pop(self.tier1.streak[i].index(list(filter(lambda j:j[0]==awarder[0],self.tier1.streak[i]))[0]))
            ### tier2 ###
            for i in self.tier2.tenure:
                if list(filter(lambda j:j[0]==awarder[0],self.tier2.tenure[i])) != []:
                    w.tier2.tenure[i].pop(self.tier2.tenure[i].index(list(filter(lambda j:j[0]==awarder[0],self.tier2.tenure[i]))[0]))
            for i in self.tier2.streak:
                if list(filter(lambda j:j[0]==awarder[0],self.tier2.streak[i])) != []:
                    w.tier2.streak[i].pop(self.tier2.streak[i].index(list(filter(lambda j:j[0]==awarder[0],self.tier2.streak[i]))[0]))
            ### tier3 ###
            for i in self.tier3.tenure:
                if list(filter(lambda j:j[0]==awarder[0],self.tier3.tenure[i])) != []:
                    w.tier3.tenure[i].pop(self.tier3.tenure[i].index(list(filter(lambda j:j[0]==awarder[0],self.tier3.tenure[i]))[0]))
            for i in self.tier3.streak:
                if list(filter(lambda j:j[0]==awarder[0],self.tier3.streak[i])) != []:
                    w.tier3.streak[i].pop(self.tier3.streak[i].index(list(filter(lambda j:j[0]==awarder[0],self.tier3.streak[i]))[0]))
            #print(self.tier3.month)
            '''
            if awarder[1] == 0:
                #self.tier1.month[self.sub_date_dict[awarder[2]]].pop(awarder[3])
                self.tier1.tenure[self.sub_date_dict[awarder[2]]].pop(awarder[3])
                self.tier1.streak[self.sub_date_dict[awarder[2]]].pop(awarder[3])
            elif awarder[1] == 1:    
                #self.tier2.month[self.sub_date_dict[awarder[2]]].pop(awarder[3])
                self.tier2.tenure[self.sub_date_dict[awarder[2]]].pop(awarder[3])
                self.tier2.streak[self.sub_date_dict[awarder[2]]].pop(awarder[3])
            else:
                #self.tier3.month[self.sub_date_dict[awarder[2]]].pop(awarder[3])
                self.tier3.tenure[self.sub_date_dict[awarder[2]]].pop(awarder[3])
                self.tier3.streak[self.sub_date_dict[awarder[2]]].pop(awarder[3])
            '''    
            self.type_check()
            ind = self.ui.award_list_n.currentIndex()
            index = self.ui.award_list_n.currentIndex().row()
            #index_con = self.ui.award_list_n.currentIndex()
            award_names = self.ui.award_list_n.model().stringList()
            award_numels = self.ui.award_list_c.model().stringList()                    
            awarder_list = self.ui.awarder_list.model().stringList()
            awarder_list.append(awarder[0]+' - '+award_names[index]+' ( Tier '+str(awarder[1]+1)+', '+self.sub_date_dict[awarder[2]]+' months)')
            self.slm_awarder.setStringList(awarder_list)
            self.ui.awarder_list.setModel(self.slm_awarder)
            if int(award_numels[index])-1 == 0:
                award_numels.pop(index)
                award_names.pop(index)
                index = -1
            else:
                award_numels[index] = str(int(award_numels[index])-1)
            self.slm_award_ln.setStringList(award_numels)
            self.slm_award_l.setStringList(award_names)
            self.ui.award_list_c.setModel(self.slm_award_ln)
            self.ui.award_list_n.setModel(self.slm_award_l)
            if ind.row()< len(award_names):
                self.list_click_3(ind)#index))
                self.list_click_4(ind)
            #print(type(index))
            #self.ui.award_list_c.selectionModel().setCurrentIndex(int(index),PyQt5.QtCore.QItemSelectionModel.SelectCurrent)
            #self.ui.award_list_n.selectionModel().setCurrentIndex(int(index),PyQt5.QtCore.QItemSelectionModel.SelectCurrent)
            #for i in range(self.ui.sub_list.model().rowCount()):
                #table_list.append(self.ui.sub_list.model().item(i,0).text())
            
        
    
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
        self.ui.tier_all.click()
        self.ui.tier_reset.click()
        self.ui.time_all.click()
        self.ui.time_reset.click()
        #---偵測台主名稱---#
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
        #--------------------#
        
        with open(self.name,newline = '') as f:
            self.sub_id_list = []
            self.sub_dates_list = []
            self.sub_tier_list = []
            self.tenure_list = []
            self.streak_list = []
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
                    self.tenure_list.append(p[3])
                    self.streak_list.append(p[4])
                    if int(p[2][-1]) == 1:
                        self.tier1.month_flow(sub_term.years*12+sub_term.months+1,[p[0],str(sub_term.years*12+sub_term.months+1)+' months',p[2]])
                        self.tier1.tenure_flow(int(p[3]),[p[0],p[3]+' months',p[2]])
                        self.tier1.streak_flow(int(p[4]),[p[0],p[4]+' months',p[2]])
                        self.tier1.all.append([p[0],p[3],p[2]])
                    elif int(p[2][-1]) == 2:
                        self.tier2.month_flow(sub_term.years*12+sub_term.months+1,[p[0],str(sub_term.years*12+sub_term.months+1)+' months',p[2]])
                        self.tier2.tenure_flow(int(p[3]),[p[0],p[3]+' months',p[2]])
                        self.tier2.streak_flow(int(p[4]),[p[0],p[4]+' months',p[2]])
                        self.tier2.all.append([p[0],p[3],p[2]])
                    else:
                        self.tier3.month_flow(sub_term.years*12+sub_term.months+1,[p[0],str(sub_term.years*12+sub_term.months+1)+' months',p[2]])
                        self.tier3.tenure_flow(int(p[3]),[p[0],p[3]+' months',p[2]])
                        self.tier3.streak_flow(int(p[4]),[p[0],p[4]+' months',p[2]])
                        self.tier3.all.append([p[0],p[3],p[2]])
                    
          
            
            
            

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
                            for j in self.tier1.tenure[self.sub_date_dict[i2]]:
                                self.table_model.setItem(inde,0,QStandardItem(j[0]))
                                self.table_model.setItem(inde,1,QStandardItem(j[1]))
                                self.table_model.setItem(inde,2,QStandardItem(j[2]))
                                inde += 1
                if i == 1 and c == 2:
                    for i2,c2 in enumerate(self.sub_date_check):
                        if c2 == 2:
                            for j in self.tier2.tenure[self.sub_date_dict[i2]]:
                                self.table_model.setItem(inde,0,QStandardItem(j[0]))
                                self.table_model.setItem(inde,1,QStandardItem(j[1]))
                                self.table_model.setItem(inde,2,QStandardItem(j[2]))
                                inde += 1
                if i == 2 and c == 2:
                    for i2,c2 in enumerate(self.sub_date_check):
                        if c2 == 2:
                            for j in self.tier3.tenure[self.sub_date_dict[i2]]:
                                self.table_model.setItem(inde,0,QStandardItem(j[0]))
                                self.table_model.setItem(inde,1,QStandardItem(j[1]))
                                self.table_model.setItem(inde,2,QStandardItem(j[2]))
                                inde += 1
                    
        #self.slm_sublist.setStringList(sub_list)
        self.ui.sub_list.setModel(self.table_model)
        self.ui.tenure.setChecked(True)
        #self.ui.listView_2.setModel(self.slm_sublist)
    
    def list_click_3(self,index):
        self.ui.award_list_n.selectionModel().setCurrentIndex(index,PyQt5.QtCore.QItemSelectionModel.SelectCurrent)
        #self.ui.award_list_n.setSelection(index)
    def list_click_4(self,index):
        self.ui.award_list_c.selectionModel().setCurrentIndex(index,PyQt5.QtCore.QItemSelectionModel.SelectCurrent)

    def type_check(self):
        self.table_model.clear()
        self.sub_type_check = [self.ui.checkBox_1.checkState(),self.ui.checkBox_2.checkState(),self.ui.checkBox_3.checkState()]
        self.sub_date_check = [self.ui.checkBox_t1.checkState(),self.ui.checkBox_t2.checkState(),self.ui.checkBox_t3.checkState(),
                               self.ui.checkBox_t4.checkState(),self.ui.checkBox_t5.checkState(),self.ui.checkBox_t6.checkState(),
                               self.ui.checkBox_t7.checkState(),self.ui.checkBox_t8.checkState()]
        inde = 0
        
        if self.ui.tenure.isChecked():
            for i,c in enumerate(self.sub_type_check):
                if i == 0 and c == 2:
                    for i2,c2 in enumerate(self.sub_date_check):
                        if c2 == 2:
                            for j in self.tier1.tenure[self.sub_date_dict[i2]]:
                                self.table_model.setItem(inde,0,QStandardItem(j[0]))
                                self.table_model.setItem(inde,1,QStandardItem(j[1]))
                                self.table_model.setItem(inde,2,QStandardItem(j[2]))
                                inde += 1
                if i == 1 and c == 2:
                    for i2,c2 in enumerate(self.sub_date_check):
                        if c2 == 2:
                            for j in self.tier2.tenure[self.sub_date_dict[i2]]:
                                self.table_model.setItem(inde,0,QStandardItem(j[0]))
                                self.table_model.setItem(inde,1,QStandardItem(j[1]))
                                self.table_model.setItem(inde,2,QStandardItem(j[2]))
                                inde += 1
                if i == 2 and c == 2:
                    for i2,c2 in enumerate(self.sub_date_check):
                        if c2 == 2:
                            for j in self.tier3.tenure[self.sub_date_dict[i2]]:
                                self.table_model.setItem(inde,0,QStandardItem(j[0]))
                                self.table_model.setItem(inde,1,QStandardItem(j[1]))
                                self.table_model.setItem(inde,2,QStandardItem(j[2]))
                                inde += 1
        elif self.ui.streak.isChecked():
            for i,c in enumerate(self.sub_type_check):
                if i == 0 and c == 2:
                    for i2,c2 in enumerate(self.sub_date_check):
                        if c2 == 2:
                            for j in self.tier1.streak[self.sub_date_dict[i2]]:
                                self.table_model.setItem(inde,0,QStandardItem(j[0]))
                                self.table_model.setItem(inde,1,QStandardItem(j[1]))
                                self.table_model.setItem(inde,2,QStandardItem(j[2]))
                                inde += 1
                if i == 1 and c == 2:
                    for i2,c2 in enumerate(self.sub_date_check):
                        if c2 == 2:
                            for j in self.tier2.streak[self.sub_date_dict[i2]]:
                                self.table_model.setItem(inde,0,QStandardItem(j[0]))
                                self.table_model.setItem(inde,1,QStandardItem(j[1]))
                                self.table_model.setItem(inde,2,QStandardItem(j[2]))
                                inde += 1
                if i == 2 and c == 2:
                    for i2,c2 in enumerate(self.sub_date_check):
                        if c2 == 2:
                            for j in self.tier3.streak[self.sub_date_dict[i2]]:
                                self.table_model.setItem(inde,0,QStandardItem(j[0]))
                                self.table_model.setItem(inde,1,QStandardItem(j[1]))
                                self.table_model.setItem(inde,2,QStandardItem(j[2]))
                                inde += 1
                            
        self.ui.sub_list.setModel(self.table_model)
        '''
    def date_check(self):
        self.table_model.clear()
        self.sub_type_check = [self.ui.checkBox_1.checkState(),self.ui.checkBox_2.checkState(),self.ui.checkBox_3.checkState()]
        self.sub_date_check = [self.ui.checkBox_t1.checkState(),self.ui.checkBox_t2.checkState(),self.ui.checkBox_t3.checkState(),
                               self.ui.checkBox_t4.checkState(),self.ui.checkBox_t5.checkState(),self.ui.checkBox_t6.checkState(),
                               self.ui.checkBox_t7.checkState(),self.ui.checkBox_t8.checkState()]
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
        self.ui.sub_list.setModel(self.table_model)
        '''
    def add_award(self):
        if self.ui.new_award.text() == '' or self.ui.new_award.text().isspace() == True:
            return
        elif self.ui.new_award_n.text() == '' or self.ui.new_award_n.text().isspace() == True or self.ui.new_award_n.text().isdigit() == False:
            return
        else:
            award_name = self.ui.new_award.text()
            award_numel = self.ui.new_award_n.text()
            #self.award_list.append(award_name)
            #self.award_list_numel.append(award_numel)
            lv3 = self.ui.award_list_c.model().stringList()
            lv4 = self.ui.award_list_n.model().stringList()
            lv4.append(award_name)
            lv3.append(award_numel)
            self.ui.new_award.setText('')
            self.ui.new_award_n.setText('')
            self.slm_award_l.setStringList(lv4)
            self.slm_award_ln.setStringList(lv3)
            self.ui.award_list_c.setModel(self.slm_award_ln)
            self.ui.award_list_n.setModel(self.slm_award_l)
            
        
    def load_award(self):
        file, _ = QFileDialog.getOpenFileUrl(self, '開啟', "", "Text File (*.txt)")
        if file.url() == '':
            return
        n_l = -len(file.fileName())
        os.chdir(file.path()[1:n_l])
        with open(file.fileName(), 'r', encoding = 'utf-8') as f:
            data = f.readlines()
            ls = [l.replace(' ', '').replace('\n', '').split(',') for l in data]

        lv3 = [s[1] for s in ls]
        lv4 = [s[0] for s in ls]
        self.slm_award_l.setStringList(lv4)
        self.slm_award_ln.setStringList(lv3)
        self.ui.award_list_c.setModel(self.slm_award_ln)
        self.ui.award_list_n.setModel(self.slm_award_l)
    def out_awarder(self):
        f_url, _ = QFileDialog.getSaveFileUrl(self, '存檔', "", "CSV File (*.csv);;Text File (*.txt)")
        
        if f_url.url() == '':
            return
        n_l = -len(f_url.fileName())
        os.chdir(f_url.path()[1:n_l])
        
        file = f_url.fileName()
        awarder_list = self.ui.awarder_list.model().stringList()
        if file[-3:] == 'txt':
            with open(file, 'w', encoding='utf-8') as f:
                for i in awarder_list:
                    f.write(i.split('(')[0].replace(' ','').split('-')[0]+','+i.split('(')[0].replace(' ','').split('-')[1]+'\n')
        elif file[-3:] == 'csv':
            with open(file, 'w', newline = '') as csvf:
                writer = csv.writer(csvf)
                for i in awarder_list:
                    writer.writerow([i.split('(')[0].replace(' ','').split('-')[0],i.split('(')[0].replace(' ','').split('-')[1]])
        else:
            QMessageBox.information(self, "錯誤", "檔案不是csv或txt", QMessageBox.Yes)
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = AppWindow()
    w.show()
    sys.exit(app.exec_())