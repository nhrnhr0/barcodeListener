
import threading
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from threading import Thread
import configparser
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BarcodeManager:
    conf = None
    browser = None
    last_barcode_scaned_thread = None
    
    class CancleableTimeoutThreasd(threading.Thread):
        def cancle(self):
            self.stop = True
        def __init__(self,sleep, code, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.sleep = sleep
            self.code = code
            self.stop = False
        def run(self) -> None:
            print('run is starting')
            time.sleep(self.sleep)
            if self.stop == False:
                print('executing code')
                self.code()
            else:
                print('code was canceled')
                
            
    
    def __init__(self) -> None:
        self.conf = BarcodeManager.load_config()
        chrome_options = webdriver.ChromeOptions(); 
        # TODO: uncommenct to fullscreen
        chrome_options.add_argument("--start-fullscreen")
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation']);

        self.browser = webdriver.Chrome(self.conf['chromeDriver'],options=chrome_options)
        #self.mainDriver.fullscreen_window()
        self.browser.get(self.conf['url'])
        #self.browser.fullscreen_window()
        
        
        self.main_window  = self.browser.current_window_handle
        self.browser.execute_script(f"window.open('{self.conf['productUrl']}')")
        WebDriverWait(self.browser, 10).until(EC.number_of_windows_to_be(2))
        browser_windows = self.browser.window_handles
        self.barcode_window = [x for x in browser_windows if x != self.main_window][0]
        # browser.switch_to_window(new_window) <!---deprecated>
        #self.browser.switch_to.window(new_window)
        #self.barcodeDriver.get(self.conf['productUrl'] + '123')
        #self.barcodeDriver.executeScript('alert("Focus window")')
        #self.barcodeDriver.switch
        #time.sleep(4) 
        #self.mainDriver.execute_script('window.focus();')
        self.browser.switch_to.window(self.main_window)

    def switch_to_main_window(self):
        self.browser.switch_to.window(self.main_window)
    def load_config():
        config = configparser.ConfigParser()
        config.read('config.ini')
        return config['BarcodeManager']

    def open_barcode(self, barcode: str):
        print('start show barcode', barcode)
        self.browser.switch_to.window(self.barcode_window)
        
        self.browser.get(self.conf['productUrl'] + barcode)
        print('done show barcode', barcode)
        if self.last_barcode_scaned_thread != None:
            if self.last_barcode_scaned_thread.is_alive():
                self.last_barcode_scaned_thread.cancle()
                print(self.last_barcode_scaned_thread, ' is canceled')
            else:
                print(self.last_barcode_scaned_thread, ' is dead')
        else: 
            print('barcode scaned thread was never set')
        t = BarcodeManager.CancleableTimeoutThreasd(5, self.switch_to_main_window)
        self.last_barcode_scaned_thread = t        
        self.last_barcode_scaned_thread.start()
    
    def close(self):
        self.browser.close()
def main():
    bm = BarcodeManager()
    print('done bm')
    time.sleep(5)
    bm.open_barcode('676525053151')
    time.sleep(1)
    bm.open_barcode('676525097827')
    time.sleep(1)
    bm.open_barcode('676525090170')
    time.sleep(1)
    bm.open_barcode('676525078215')
    while True:
        time.sleep(3)
    bm.close()
    #print('conf', conf)
    

    #driver.get(conf['url'])
    #time.sleep(2)
    #open_barcode_window(driver, '123')
    #print('all done')
    #driver.close()

if __name__ == '__main__':
    main()