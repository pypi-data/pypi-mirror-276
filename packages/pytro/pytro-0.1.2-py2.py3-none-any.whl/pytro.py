import eel
import os
import webview
import threading

'''Pytron is symbios of eel and pywebview'''

class Application:
    def __init__(self, content_dir: str, window_title: str, resizable: bool = False, width: int = 800, height: int =800):
        self.window = webview.create_window(window_title, 'http://localhost:8080', resizable=resizable, height=height, width=width)
        eel.init(content_dir)

    def expose(self, function: callable):
        '''Expose python function in javascript'''

        eel.expose(function)

    def use(self, function_name: str, **args):
        return getattr(eel, function_name)(**args)
    
    def kill(self):
        print('Killing main process...')
        os.system('kill %d' % os.getpid())

    def __server(self, file):
        eel.start(file, port=8080, mode=False)

        
    
    def start(self, file, debug: bool = False):
        threading.Thread(target=self.__server, args=(file,)).start()
        self.window.events.closed+=self.kill
        webview.start(debug=debug)
            
        