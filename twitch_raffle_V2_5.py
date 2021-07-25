# -*- coding: utf-8 -*-
"""
Created on Sun May 23 21:12:07 2021

@author: tis05
"""


import sys,PyQt5, os, csv,random
import pandas as pd
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QMessageBox, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QStandardItem
from PyQt5 import QtGui
from twitch_sub_v205 import Ui_Form


class Subscriber:
    def __init__(self, file_name):
        self.load_file(file_name)
        self.find_streamer()
        
        
    def load_file(self, file_name):
        df = pd.read_csv(file_name)
        df['Subscribe Date'] = pd.to_datetime(df['Subscribe Date'])
        df['Subscribe Date'] = df.apply(lambda x : pd.Series(x['Subscribe Date'].timestamp()), axis=1)
        self.subscriber_raw = df
        
        
        
    def find_streamer(self):
        self.streamer = self.subscriber_raw['Username'].iloc[self.subscriber_raw['Subscribe Date'].idxmin()]
        
        
    # def 




class Tier:
    def __init__(self):
        self.all = []
        self.month = {}
        self.tenure = {}
        self.streak = {}
        self.sub_type = {}
    def month_flow(self,month,tlist):
        if month not in self.month :
            self.month[month] = [tlist]
        else:
            self.month[month].append(tlist)
            
    def tenure_flow(self,month,tlist):
        if month not in self.tenure :
            self.tenure[month] = [tlist]
        else:
            self.tenure[month].append(tlist)
    def streak_flow(self,month,tlist):
        if month not in self.streak :
            self.streak[month] = [tlist]
        else:
            self.streak[month].append(tlist)
            
class AppWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        self.file_name = ''
        
        self.tier1 = Tier()
        self.tier2 = Tier()
        self.tier3 = Tier()
        
        self.ui.time_group.horizontalHeader().setStretchLastSection(True)
        self.ui.time_group.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        
        self.path = os.getcwd()
        self.ui.new_award_n.setValidator(QtGui.QIntValidator())
        self.ui.lineEdit_1.setValidator(QtGui.QDoubleValidator())
        self.ui.lineEdit_2.setValidator(QtGui.QDoubleValidator())
        self.ui.lineEdit_3.setValidator(QtGui.QDoubleValidator())
        
        self.ui.init_time.clicked.connect(self.init_timegroup)
        self.ui.add_time.clicked.connect(self.add_time)
        self.ui.del_time.clicked.connect(self.del_time)
        self.ui.time_all.clicked.connect(self.time_all)
        self.ui.time_group.cellChanged.connect(self.cell_change)
        
        
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
        
        self.ui.check_gift.stateChanged.connect(self.type_check)
        self.ui.gift_month.textChanged.connect(self.type_check)
        
                                ### 訂閱時間 ###        
        
        self.sub_date = []
        self.sub_rate = []
        
        # self.sub_date_dict = {0:'0to2',1:'3to5',2:'6to8',3:'9to12',4:'12',5:'24',6:'36',7:'48'}
        
        
                                ### 訂閱名單 ###        
        self.header_list = ['ID','月份','層級','類別']
        self.table_model = PyQt5.QtGui.QStandardItemModel(self.ui.sub_list)
        self.table_model.setColumnCount(4)
        self.table_model.setHorizontalHeaderLabels(self.header_list)
        self.ui.sub_list.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
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
        self.ui.awarder_out_all.clicked.connect(self.awarder_all)
        self.ui.clear_awarder.clicked.connect(self.awarder_clear)
        self.ui.save_awarder.clicked.connect(self.out_awarder)
        
        
        self.show()
    def add_time_item(self, row, start, end):
        
        self.ui.time_group.cellChanged.disconnect(self.cell_change)
        
        
        _translate = PyQt5.QtCore.QCoreApplication.translate
        item = QTableWidgetItem()
        self.ui.time_group.setVerticalHeaderItem(row, item)
        self.ui.time_group.verticalHeaderItem(row).setText(_translate("Form", "{}".format(row+1)))
        item = QTableWidgetItem()
        item.setCheckState(PyQt5.QtCore.Qt.Checked)
        self.ui.time_group.setItem(row, 0, item)
        item = QTableWidgetItem()
        self.ui.time_group.setItem(row, 1, item)
        self.ui.time_group.item(row,1).setText(_translate("Form", "{}".format(start)))
        item = QTableWidgetItem()
        self.ui.time_group.setItem(row, 2, item)
        self.ui.time_group.item(row,2).setText(_translate("Form", "{}".format(end)))
        item = QTableWidgetItem()
        self.ui.time_group.setItem(row, 3, item)
        self.ui.time_group.item(row,3).setText(_translate("Form", "1.0"))
        
        self.ui.time_group.cellChanged.connect(self.cell_change)
        
        
    def init_timegroup(self):
        self.ui.time_group.setRowCount(8)
        self.add_time_item(0, 1, 3)
        self.add_time_item(1, 4, 6)
        self.add_time_item(2, 7, 9)
        self.add_time_item(3, 10, 12)
        self.add_time_item(4, 13, 24)
        self.add_time_item(5, 25, 36)
        self.add_time_item(6, 37, 48)
        self.add_time_item(7, 49, 200)
        self.type_check()
        
            
    def add_time(self):
        row_position = self.ui.time_group.rowCount()
        start_month = self.ui.time_group.item(row_position-1,1).text()
        end_month = int(start_month)+2
        self.ui.time_group.insertRow(row_position)
        self.add_time_item(row_position-1, start_month, end_month)
        self.add_time_item(row_position, end_month+1, 200)
        self.type_check()
        
    def del_time(self):
        row_position = self.ui.time_group.rowCount()
        if row_position == 1:
            QMessageBox.information(self, "錯誤", "再刪乾脆別抽獎啦~~~", QMessageBox.Yes)
            pass
        else:
            start_month = self.ui.time_group.item(row_position-2,1).text()
            self.ui.time_group.removeRow(row_position-1)
            self.add_time_item(row_position-2, start_month, 200)
        
        
        self.type_check()
        pass
    
    def time_all(self):
        row_position = self.ui.time_group.rowCount()
        for row in range(row_position):
            item = self.ui.time_group.item(row,0)
            item.setCheckState(2)
        self.type_check()
        pass
    
    def cell_change(self,row,column):
        if (row == 0 and column == 1) or (row == self.ui.time_group.rowCount()-1 and column == 2):
            pass
        else:
            if column == 1:
                start_month = int(self.ui.time_group.item(row,column).text())
                last_start_month = self.ui.time_group.item(row-1,column).text()
                self.add_time_item(row-1, last_start_month, start_month-1)
            elif column == 2:
                end_month = int(self.ui.time_group.item(row,column).text())
                next_end_month = self.ui.time_group.item(row+1,column).text()
                self.add_time_item(row+1, end_month+1, next_end_month)
        self.type_check()
    def awarder_clear(self):
        self.ui.awarder_list.setRowCount(0)
        if self.file_name != '':
            self.init_file()
        


    def awarder(self):
        if self.ui.award_list_n.currentIndex().row() == -1:
            return
        else:
            self.sub_type_check = [self.ui.checkBox_1.checkState(),self.ui.checkBox_2.checkState(),self.ui.checkBox_3.checkState()]
            self.sub_type_rate = [float(self.ui.lineEdit_1.text()),float(self.ui.lineEdit_2.text()),float(self.ui.lineEdit_3.text())]
            
            gift = self.ui.check_gift.checkState()
            gift_month = int(self.ui.gift_month.text())

            sub_award_list = []
            tier_rate = [i/2*j for i,j in zip(self.sub_type_check, self.sub_type_rate)]
            # date_rate = self.sub_rate
            # total_rate = [[int(100*i*j) for i in date_rate] for j in tier_rate]
            # print(total_rate)
            if self.ui.tenure.isChecked():
                    
                for ind, month in enumerate(self.sub_date):
                    rate1 = int(100*tier_rate[0]*self.sub_rate[ind])
                    if month in self.tier1.tenure:
                        for j1 in self.tier1.tenure[month]:
                            if gift == 2 and j1[3] == 'gift' and month < gift_month:
                                continue
                            sub_award_list.extend([[j1[0],0,month]]*rate1)
                        
                    rate2 = int(100*tier_rate[1]*self.sub_rate[ind])
                    if month in self.tier2.tenure:
                        for j2 in self.tier2.tenure[month]:
                            if gift == 2 and j2[3] == 'gift' and month < gift_month:
                                continue
                            sub_award_list.extend([[j2[0],1,month]]*rate2)
                        
                    rate3 = int(100*tier_rate[2]*self.sub_rate[ind])
                    if month in self.tier3.tenure:
                        for j3 in self.tier3.tenure[month]:
                            if gift == 2 and j3[3] == 'gift' and month < gift_month:
                                continue
                            sub_award_list.extend([[j3[0],2,month]]*rate3)
                    
                
            elif self.ui.streak.isChecked():
                
                for ind, month in enumerate(self.sub_date):
                    rate1 = int(100*tier_rate[0]*self.sub_rate[ind])
                    if month in self.tier1.streak:
                        for j1 in self.tier1.streak[month]:
                            if gift == 2 and j1[3] == 'gift' and month < gift_month:
                                continue
                            sub_award_list.extend([[j1[0],0,month]]*rate1)
                        
                    rate2 = int(100*tier_rate[1]*self.sub_rate[ind])
                    if month in self.tier2.streak:
                        for j2 in self.tier2.streak[month]:
                            if gift == 2 and j2[3] == 'gift' and month < gift_month:
                                continue
                            sub_award_list.extend([[j2[0],1,month]]*rate2)
                        
                    rate3 = int(100*tier_rate[2]*self.sub_rate[ind])
                    if month in self.tier3.streak:
                        for j3 in self.tier3.streak[month]:
                            if gift == 2 and j3[3] == 'gift' and month < gift_month:
                                continue
                            sub_award_list.extend([[j3[0],2,month]]*rate3)
                    
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
            
            self.type_check()
            ind = self.ui.award_list_n.currentIndex()
            index = self.ui.award_list_n.currentIndex().row()
            #index_con = self.ui.award_list_n.currentIndex()
            award_names = self.ui.award_list_n.model().stringList()
            award_numels = self.ui.award_list_c.model().stringList()

            row_position = self.ui.awarder_list.rowCount()
            self.ui.awarder_list.insertRow(row_position)
            _translate = PyQt5.QtCore.QCoreApplication.translate
            item = QTableWidgetItem()
            self.ui.awarder_list.setVerticalHeaderItem(row_position, item)
            self.ui.awarder_list.verticalHeaderItem(row_position).setText(_translate("Form", "{}".format(row_position+1)))
            item = QTableWidgetItem()
            self.ui.awarder_list.setItem(row_position, 0, item)
            self.ui.awarder_list.item(row_position,0).setText(_translate("Form", "{}".format(award_names[index])))
            item = QTableWidgetItem()
            self.ui.awarder_list.setItem(row_position, 1, item)
            self.ui.awarder_list.item(row_position,1).setText(_translate("Form", "{}".format(awarder[0])))
            item = QTableWidgetItem()
            self.ui.awarder_list.setItem(row_position, 2, item)
            self.ui.awarder_list.item(row_position,2).setText(_translate("Form", "Tier {}".format(awarder[1]+1)))
            item = QTableWidgetItem()
            self.ui.awarder_list.setItem(row_position, 3, item)
            self.ui.awarder_list.item(row_position,3).setText(_translate("Form", "{} months".format(awarder[2])))
            
            
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
            
        
    def awarder_all(self):
        
        if self.ui.award_list_n.currentIndex().row() == -1:
            return
        else:
            index = self.ui.award_list_n.currentIndex().row()
            award_numels = self.ui.award_list_c.model().stringList()
            for i in range(int(award_numels[index])):
                self.awarder()
                if self.table_model.rowCount() == 0:
                    return
                
    def open_file(self):
        file = QFileDialog.getOpenFileUrl(self, 'Sub csv', "", "sub file (*.csv)")
        if file[0].url() == '':
            return
        # print(file)
        self.file_name = file[0].fileName()
        file_path = file[0].path()
        # print('Path:',file[0].path())
        # print('URL:',file[0].url())
        self.path = file_path[1:-len(self.file_name)]
        self.init_file()
    def init_file(self):
        os.chdir(self.path)
        self.subcriber_list = Subscriber(self.file_name)
        
        self.tier1 = Tier()
        self.tier2 = Tier()
        self.tier3 = Tier()
        
        self.sub_id_list = []
        self.sub_dates_list = []
        self.sub_tier_list = []
        self.tenure_list = []
        self.streak_list = []
        self.sub_type = []
        
        
        for ind,row in self.subcriber_list.subscriber_raw.iterrows():
            username, tier, tenure, streak, sub_type = row['Username'], row['Current Tier'], row['Tenure'], row['Streak'], row['Sub Type']
            if username == self.subcriber_list.streamer:
                continue
            self.sub_id_list.append(username)
            self.sub_dates_list.append('{} months'.format(tenure))
            self.sub_tier_list.append(tier)
            self.tenure_list.append(tenure)
            self.streak_list.append(streak)
            self.sub_type.append(sub_type)
            if tier[-1] == '1':
                self.tier1.month_flow(int(tenure), [username, '{} months'.format(tenure), tier, sub_type])
                self.tier1.tenure_flow(int(tenure), [username, '{} months'.format(tenure), tier, sub_type])
                self.tier1.streak_flow(int(streak), [username, '{} months'.format(streak), tier, sub_type])
                self.tier1.all.append([username, tenure, tier, sub_type])
            elif tier[-1] == '2':
                self.tier2.month_flow(int(tenure), [username, '{} months'.format(tenure), tier, sub_type])
                self.tier2.tenure_flow(int(tenure), [username, '{} months'.format(tenure), tier, sub_type])
                self.tier2.streak_flow(int(streak), [username, '{} months'.format(streak), tier, sub_type])
                self.tier2.all.append([username, tenure, tier, sub_type])
                
            elif tier[-1] == '3':
                self.tier3.month_flow(int(tenure), [username, '{} months'.format(tenure), tier, sub_type])
                self.tier3.tenure_flow(int(tenure), [username, '{} months'.format(tenure), tier, sub_type])
                self.tier3.streak_flow(int(streak), [username, '{} months'.format(streak), tier, sub_type])
                self.tier3.all.append([username, tenure, tier, sub_type])
        self.type_check()
        self.ui.tenure.setChecked(True)
    
    def list_click_3(self,index):
        self.ui.award_list_n.selectionModel().setCurrentIndex(index,PyQt5.QtCore.QItemSelectionModel.SelectCurrent)
        #self.ui.award_list_n.setSelection(index)
    def list_click_4(self,index):
        self.ui.award_list_c.selectionModel().setCurrentIndex(index,PyQt5.QtCore.QItemSelectionModel.SelectCurrent)

    def type_check(self):
        
        if self.tier1.all == [] :
            return
        
        self.table_model.clear()
        self.sub_type_check = [self.ui.checkBox_1.checkState(),self.ui.checkBox_2.checkState(),self.ui.checkBox_3.checkState()]
        gift = self.ui.check_gift.checkState()
        gift_month = int(self.ui.gift_month.text())
        # print(gift_month)
        self.sub_date = []
        self.sub_rate = []
        
        row_position = self.ui.time_group.rowCount()
        for row in range(row_position):
            item = self.ui.time_group.item(row,0)
            start_month = int(self.ui.time_group.item(row,1).text())
            end_month = int(self.ui.time_group.item(row,2).text())
            rate = float(self.ui.time_group.item(row,3).text())
            if item.checkState() == 2:
                month = list(range(start_month, end_month+1))
                rate_l = [rate]*len(month)
                self.sub_date.extend(month)
                self.sub_rate.extend(rate_l)
            
        inde = 0
        if self.ui.tenure.isChecked():
            for i,c in enumerate(self.sub_type_check):
                if i == 0 and c == 2:
                    for i2 in self.sub_date:
                        if i2 in self.tier1.tenure:
                            for j in self.tier1.tenure[i2]:
                                if gift == 2 and j[3] == 'gift' and i2 < gift_month:
                                    continue
                                self.table_model.setItem(inde,0,QStandardItem(j[0]))
                                self.table_model.setItem(inde,1,QStandardItem(j[1]))
                                self.table_model.setItem(inde,2,QStandardItem(j[2]))
                                self.table_model.setItem(inde,3,QStandardItem(j[3]))
                                inde += 1
                if i == 1 and c == 2:
                    for i2 in self.sub_date:
                        if i2 in self.tier2.tenure:
                            for j in self.tier2.tenure[i2]:
                                if gift == 2 and j[3] == 'gift' and i2 < gift_month:
                                    continue
                                self.table_model.setItem(inde,0,QStandardItem(j[0]))
                                self.table_model.setItem(inde,1,QStandardItem(j[1]))
                                self.table_model.setItem(inde,2,QStandardItem(j[2]))
                                self.table_model.setItem(inde,3,QStandardItem(j[3]))
                                inde += 1
                if i == 2 and c == 2:
                    for i2 in self.sub_date:
                        if i2 in self.tier3.tenure:
                            for j in self.tier3.tenure[i2]:
                                if gift == 2 and j[3] == 'gift' and i2 < gift_month:
                                    continue
                                self.table_model.setItem(inde,0,QStandardItem(j[0]))
                                self.table_model.setItem(inde,1,QStandardItem(j[1]))
                                self.table_model.setItem(inde,2,QStandardItem(j[2]))
                                self.table_model.setItem(inde,3,QStandardItem(j[3]))
                                inde += 1
                            
        elif self.ui.streak.isChecked():
            for i,c in enumerate(self.sub_type_check):
                if i == 0 and c == 2:
                    for i2 in self.sub_date:
                        if i2 in self.tier1.streak:
                            for j in self.tier1.streak[i2]:
                                if gift == 2 and j[3] == 'gift' and i2 < gift_month:
                                    continue
                                self.table_model.setItem(inde,0,QStandardItem(j[0]))
                                self.table_model.setItem(inde,1,QStandardItem(j[1]))
                                self.table_model.setItem(inde,2,QStandardItem(j[2]))
                                self.table_model.setItem(inde,3,QStandardItem(j[3]))
                                inde += 1
                if i == 1 and c == 2:
                    for i2 in self.sub_date:
                        if i2 in self.tier2.streak:
                            for j in self.tier2.streak[i2]:
                                if gift == 2 and j[3] == 'gift' and i2 < gift_month:
                                    continue
                                self.table_model.setItem(inde,0,QStandardItem(j[0]))
                                self.table_model.setItem(inde,1,QStandardItem(j[1]))
                                self.table_model.setItem(inde,2,QStandardItem(j[2]))
                                self.table_model.setItem(inde,3,QStandardItem(j[3]))
                                inde += 1
                if i == 2 and c == 2:
                    for i2 in self.sub_date:
                        if i2 in self.tier3.streak:
                            for j in self.tier3.streak[i2]:
                                if gift == 2 and j[3] == 'gift' and i2 < gift_month:
                                    continue
                                self.table_model.setItem(inde,0,QStandardItem(j[0]))
                                self.table_model.setItem(inde,1,QStandardItem(j[1]))
                                self.table_model.setItem(inde,2,QStandardItem(j[2]))
                                self.table_model.setItem(inde,3,QStandardItem(j[3]))
                                inde += 1
        self.table_model.setHorizontalHeaderLabels(['ID','月份','層級','類別'])
        self.ui.sub_list.setModel(self.table_model)
        
        
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
        if file[-3:] == 'txt':
            with open(file, 'w', encoding='utf-8') as f:
                for i in range(self.ui.awarder_list.rowCount()):
                    award = self.ui.awarder_list.item(i,0).text()
                    awarder = self.ui.awarder_list.item(i,1).text()
                    tier = self.ui.awarder_list.item(i,2).text()
                    date = self.ui.awarder_list.item(i,3).text()
                    f.write('{},{}, {}, {}\n'.format(awarder, award, tier, date))
                    # f.write(i.split('(')[0].replace(' ','').split('-')[0]+','+i.split('(')[0].replace(' ','').split('-')[1]+'\n')
            QMessageBox.information(self, "成功", "存檔成功", QMessageBox.Yes)
        elif file[-3:] == 'csv':
            with open(file, 'w', newline = '') as csvf:
                writer = csv.writer(csvf)
                if csvf.tell() == 0:
                    writer.writerow(['獎項','中獎者','層級','訂閱月份'])
                for i in range(self.ui.awarder_list.rowCount()):
                    award = self.ui.awarder_list.item(i,0).text()
                    awarder = self.ui.awarder_list.item(i,1).text()
                    tier = self.ui.awarder_list.item(i,2).text()
                    date = self.ui.awarder_list.item(i,3).text()
                    writer.writerow([award, awarder, tier, date])
            QMessageBox.information(self, "成功", "存檔成功", QMessageBox.Yes)
        else:
            QMessageBox.information(self, "錯誤", "檔案不是csv或txt", QMessageBox.Yes)
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = AppWindow()
    # w.show()
    # sys.exit(app.exec_())