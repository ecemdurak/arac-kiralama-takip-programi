    # -*- coding: utf-8 -*-
    """
    Created on Sun Jun  2 04:21:22 2024
    
    @author: ecem
    """
    #--------kütüphane----------------#
    import sys
    from PyQt5 import QtGui, QtWidgets, QtCore
    from PyQt5.QtWidgets import *
    from widgets_arac_kiralama import Ui_MainWindow
    import sqlite3
    
    
    #-------uygulama----------------------#
    Uygulama=QApplication(sys.argv)
    penarac_kiralama=QMainWindow()
    ui=Ui_MainWindow()
    ui.setupUi(penarac_kiralama)
    penarac_kiralama.show()
    
    #-----------veri tabanı ekleme-------#
    import sqlite3
    global curs
    global conn
    conn=sqlite3.connect('veritabanı.db')
    curs=conn.cursor()
    
    
    
    conn.commit()
    #-------------kaydet------------------#
    
    def EKLE():
        _lneTCKimlikNo = ui.lneTCKimlikNo.text()
        _lneAd = ui.lneAd.text()
        _lneSoyad = ui.lneSoyad.text()
        _lneTelefonNumarasi = ui.lneTelefonNumarasi.text()
        _lneEPosta = ui.lneEPosta.text()
        _dteDogumTarihi = ui.dteDogumTarihi.date().toString(QtCore.Qt.ISODate)  
        _cmbVites = ui.cmbVites.currentText()
        _cmbAracSinifi = ui.cmbAracSinifi.currentText()
        _cmbYakit = ui.cmbYakit.currentText()
        _cmbAracMarka = ui.cmbAracMarka.currentText()
        _cmbKMLimit = ui.cmbKMLimit.currentText()
        _cmbFiyatAraligi = ui.cmbFiyatAraligi.currentText()
        _rdbBebekKoltugu = ui.rdbBebekKoltugu.isChecked()
        _dteTeslimAlisTarih = ui.dteTeslimAlisTarih.date().toString(QtCore.Qt.ISODate)  
        _dteTeslimEdisTarih = ui.dteTeslimEdisTarih.date().toString(QtCore.Qt.ISODate)  
        _textAlis = ui.txtAlis.toPlainText()
        _textEdis = ui.txtEdis.toPlainText()
        _chkFarkliYer = ui.chkFarkliYer.isChecked() 
        _chkKurumsalArac = ui.chkKurumsalArac.isChecked()  
        
        try:
            curs.execute("INSERT INTO kayıt \
                          (tc_no, ad, soyad, tel_no, e_posta, doğum_tarihi, vites, sınıf, yakıt, marka, km_limit, fiyat, bebek_koltuk, teslim_alış_tarih_saat, teslim_ediş_tarih_saat, teslim_alış_yeri, teslim_ediş_yeri, farklı_yer, kurumsal_araç) \
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                         (_lneTCKimlikNo, _lneAd, _lneSoyad, _lneTelefonNumarasi, _lneEPosta, _dteDogumTarihi, _cmbVites, _cmbAracSinifi, _cmbYakit, _cmbAracMarka, _cmbKMLimit, _cmbFiyatAraligi, _rdbBebekKoltugu,
                          _dteTeslimAlisTarih, _dteTeslimEdisTarih, _textAlis, _textEdis, _chkFarkliYer, _chkKurumsalArac))
            conn.commit()
            QMessageBox.information(penarac_kiralama, "Bilgi", "Kayıt başarıyla eklendi.")
        except sqlite3.Error as e:
            QMessageBox.critical(penarac_kiralama, "Hata", f"Veritabanına ekleme sırasında bir hata oluştu: {e}")
    
    def listele ():
        ui.tblwMusteriBilgi.clear()
        ui.tblwMusteriBilgi.setHorizontalHeaderLabels(('ıd','tc_no','ad','soyad','tel_no','e_posta','doğum_tarihi','vites','sınıf','yakıt','marka','km_limit','fiyat','bebek_koltuk','teslim_alış_tarih_saat','teslim_ediş_tarih_saat','teslim_alış_yeri','teslim_ediş_yeri','farklı_yer','kurumsal_araç')) \
                                                       
        ui.tblwMusteriBilgi.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        curs.execute("SELECT * FROM kayıt " )
        for satirIndeks, satirVeri in enumerate (curs):
            for sutunIndeks, sutunVeri in enumerate (satirVeri):
                ui.tblwMusteriBilgi.setItem(satirIndeks,sutunIndeks,QTableWidgetItem(str(sutunVeri)))
                
                
    listele()
    #---------sil-------#
    def SIL():
        cevap = QMessageBox.question(penarac_kiralama, "KAYIT SİL", "Kaydı silmek istediğinize emin misiniz?",\
                               QMessageBox.Yes | QMessageBox.No)
        if cevap == QMessageBox.Yes:
            try:
                secili = ui.tblwMusteriBilgi.selectedItems()
                if secili:
                    silinecek = secili[0].text()  
                    curs.execute("DELETE FROM kayıt WHERE ıd=?", (silinecek,))
                    conn.commit()
                    listele()
                    ui.statusbar.showMessage("KAYIT SİLME İŞLEMİ BAŞARIYLA GERÇEKLEŞTİ...", 10000)
                else:
                    ui.statusbar.showMessage("Silinecek bir kayıt seçilmedi.", 10000)
            except sqlite3.Error as Hata:
                ui.statusbar.showMessage("Şöyle bir hata ile karşılaşıldı: " + str(Hata))
        else:
            ui.statusbar.showMessage("Silme işlemi iptal edildi....", 10000)

                   
    
    #--------------GÜNCELLE-----------#
    def güncelle():
        cevap=QMessageBox.question(penarac_kiralama,"KAYIT GÜNCELLE","Kayıt Güncellemek İstediğinize Emin Misiniz?",QMessageBox.Yes | QMessageBox.No)
        if cevap==QMessageBox.Yes:
            try:
                _lneTCKimlikNo = ui.lneTCKimlikNo.text()
                _lneAd = ui.lneAd.text()
                _lneSoyad = ui.lneSoyad.text()
                _lneTelefonNumarasi = ui.lneTelefonNumarasi.text()
                _lneEPosta = ui.lneEPosta.text()
                _dteDogumTarihi = ui.dteDogumTarihi.date().toString(QtCore.Qt.ISODate)  
                _cmbVites = ui.cmbVites.currentText()
                _cmbAracSinifi = ui.cmbAracSinifi.currentText()
                _cmbYakit = ui.cmbYakit.currentText()
                _cmbAracMarka = ui.cmbAracMarka.currentText()
                _cmbKMLimit = ui.cmbKMLimit.currentText()
                _cmbFiyatAraligi = ui.cmbFiyatAraligi.currentText()
                _rdbBebekKoltugu = ui.rdbBebekKoltugu.isChecked()
                _dteTeslimAlisTarih = ui.dteTeslimAlisTarih.date().toString(QtCore.Qt.ISODate)  
                _dteTeslimEdisTarih = ui.dteTeslimEdisTarih.date().toString(QtCore.Qt.ISODate)  
                _textAlis = ui.txtAlis.toPlainText()
                _textEdis = ui.txtEdis.toPlainText()
                _chkFarkliYer = ui.chkFarkliYer.isChecked()  
                _chkKurumsalArac = ui.chkKurumsalArac.isChecked()  
                curs.execute("INSERT INTO kayıt \
                                  (tc_no, ad, soyad, tel_no, e_posta, doğum_tarihi, vites, sınıf, yakıt, marka, km_limit, fiyat, bebek_koltuk, teslim_alış_tarih_saat, teslim_ediş_tarih_saat, teslim_alış_yeri, teslim_ediş_yeri, farklı_yer, kurumsal_araç) \
                                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                 (_lneTCKimlikNo, _lneAd, _lneSoyad, _lneTelefonNumarasi, _lneEPosta, _dteDogumTarihi, _cmbVites, _cmbAracSinifi, _cmbYakit, _cmbAracMarka, _cmbKMLimit, _cmbFiyatAraligi, _rdbBebekKoltugu,
                                  _dteTeslimAlisTarih, _dteTeslimEdisTarih, _textAlis, _textEdis, _chkFarkliYer, _chkKurumsalArac))
             
                conn.commit()
                
            except Exception as Hata:
                QMessageBox.critical(penarac_kiralama,"Hata",f"veri tabanı hatası: {Hata}")
           
                
                
                
                
                
                
                
                
              
                
    listele() 
             
    ui.btnEkle.clicked.connect(EKLE)
    ui.btnListele.clicked.connect(listele)
    ui.btnSil.clicked.connect(SIL)
    ui.btnGuncelle.clicked.connect(güncelle)
    ui.btncikis.clicked.connect(penarac_kiralama.close)  
    sys.exit(Uygulama.exec_())