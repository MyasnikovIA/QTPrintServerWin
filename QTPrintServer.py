# sys.stdout = sys.stderr = open(os.devnull, 'w')
from flask import Flask
from flask_cors import CORS, cross_origin
from json import dumps
from win32print import EnumPrinters, PRINTER_ENUM_LOCAL, PRINTER_ENUM_CONNECTIONS, GetDefaultPrinter
from flask import request
from urllib.parse import unquote
from traceback import format_exc
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtPrintSupport import QPrinter
from htmlPage.index import index

from lib.extlib1 import extlib1
from lib.extlib2 import extlib2
from lib.locale_ru import locale_ru
from lib.css.theme_classic import theme_classic

widthPage = 300
heightPage = 100
printer_name = ""
portServer = 51003
version = '0.1'
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.errorhandler(404)
def not_found(error):
    return "no service", 404


def parseHead():
    """
     Чтение входных пользовательских аргументов в заголовке запроса
    """
    requestMessage = {}
    for rec in request.headers:
        if "X-My-" in rec[0]:
            message = unquote(unquote(request.headers.get(rec[0])))
            key = rec[0][5:len(rec[0])]
            requestMessage[key] = message
    return requestMessage


def get_print_list():
    """
    функция получения списка принтеров установленных в системе
    :return:
    """
    requestMessage = {}
    printers = EnumPrinters(PRINTER_ENUM_LOCAL | PRINTER_ENUM_CONNECTIONS)
    requestMessage["Printers"] = [printer[2] for printer in printers]
    return requestMessage


def html_to_image(StrPrintHtml="", printer_name="", widthPage=300, heightPage=100):
    """
    Функция вывода текста на принтер
    :param StrPrintHtml: - Текст HTML
    :param printer_name: - имя принтера
    :return:
    """
    requestMessage = {}
    try:
        if printer_name == "":
            printer_name = GetDefaultPrinter()
    except Exception:
        requestMessage["Error"] = "GetDefaultPrinter:%s" % format_exc()
        return requestMessage
    try:
        app = QApplication([])
        label = QLabel()
        # '<img width="300"  height="100"  alt="" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAALQAAAB2CAIAAADujy7aAAABuUlEQVR42u3YwY7CIBRAUZj4/7/MLEgIFlqf1YwOPWdlsKlVrlDNqVNKSSnlnNvjqo6MR47PjuP9OSNniJw/foWRa4tc7d45n32tyDvtRyLjkWuIfErjGX4S7BAH4kAciANxIA7EgTgQB+JAHCAOxIE4EAfiQByIA3EgDsQB4kAciANxIA7EgTgQB+JAHCAOxIE4EAfiQByIA3EgDsSBOEAciANxIA7EgTgQB+JAHIgDxIE4EAfiQByIA3EgDsSBOEAciANxIA7EgTgQB+JAHIgDcYA4EAfiQByIA3EgDsSBOBAHiANxIA7EgTgQB+JAHIgDcYA4EAfiQByIg0/LpRSfAlYOxMGb3FbbJvPdRplzbo/b+CuD/Ugbnw6K4+vKOA6lTuQrg5tZr684HbStfO+a8alX/PvLEMdjwSmZHtZvDW12T8zxSmVc6IZ0utT3c1n72JvdcXw6stKesuAN6d56ML1tnE726W9/fxvrhvR/7zX9FI5LyHgruvD2ccVt5WCpiM9u5MiVtpKL3nOcWPaX/z3y4O0v8z43X9/Nf1bT/7WmR6bD/7sOinn2d5M4sK0gDsQB4uDQLyTS/Ojjiz5LAAAAAElFTkSuQmCC" />'
        label.setText(StrPrintHtml)
        label.resize(widthPage, heightPage)
        printer = QPrinter()
        printer.setPrinterName(printer_name)
        # printer.setPaperSize(QSizeF(widthPage, heightPage), QPrinter.DevicePixel)
        printer.setPageMargins(0, 0, 0, 0, QPrinter.DevicePixel)
        # printer.setPrinterName("Brother QL-810W")
        # printer.setOutputFileName("D:\\!PythonProject\\Штрихкод_Plagin\\QTPrintServerWin(25-02-2019)\\PrinterFileName.pdf")
        painter = QPainter()
        painter.begin(printer)
        painter.drawPixmap(-15, -15, label.grab())
        painter.end()
    except Exception:
        requestMessage["Error"] = "%s" % (format_exc())
        return requestMessage
    return requestMessage


@app.route("/")
@cross_origin()
def requestFun():
    """
    Функция обработки входящих команд с сервера
    :return:
    """
    global printer_name
    global widthPage
    global heightPage
    if request.host[:9] != "127.0.0.1":
        if request.host[:9] != "localhost":
            return "no service", 404
    requestMessage = parseHead()
    if "WidthPage" in requestMessage:
        widthPage = requestMessage.get("WidthPage")
    if "HeightPage" in requestMessage:
        heightPage = requestMessage.get("HeightPage")
    if "PrinterName" in requestMessage:
        printer_name = requestMessage.get("PrinterName")
    if "Print" in requestMessage:
        res = html_to_image(requestMessage["Print"], printer_name, widthPage, heightPage)
        return dumps(res), 200, {'content-type': 'application/json'}
    if "Getprinterlist" in requestMessage:
        return dumps(get_print_list()), 200, {'content-type': 'application/json'}
    if "Message" in requestMessage:
        if '[GetPrinterList]' in requestMessage["Message"]:
            return dumps(get_print_list()), 200, {'content-type': 'application/json'}
    if "Version" in requestMessage:
        requestMessage["Version"] = version
        return dumps(get_print_list()), 200, {'content-type': 'application/json'}

    res = index.replace("[printerList]",getJsonPage())
    return res, 200


def getJsonPage():
    printers = EnumPrinters(PRINTER_ENUM_LOCAL | PRINTER_ENUM_CONNECTIONS)
    printerList = [printer[2] for printer in printers]
    res = []
    # res = [{'text': 'book report', 'leaf': True}, {'text': 'algebra', 'leaf': True}]
    for prn in printerList:
        res.append({'text': prn, 'leaf': True})
    return str(dumps(res))


@app.errorhandler(404)
def not_found(error):
    return "No content", 404


@app.route('/<path:the_path>')
def all_other_routes(the_path):
    if (the_path == "ext.js"):
        txt = "%s%s" % (extlib1, extlib2)
        head = {'content-type': 'application/javascript; charset=utf-8', 'Content-Length': len(txt)}
        return txt, 200, head

    if (the_path == "locale-ru.js"):
        head = {'content-type': 'application/javascript; charset=utf-8', 'Content-Length': len(locale_ru)}
        return locale_ru, 200, head

    if (the_path == "theme_classic"):
        head = {'content-type': 'text/css; charset=utf-8', 'Content-Length': len(theme_classic)}
        return theme_classic, 200, head
    return "no content", 404


if __name__ == '__main__':
    _svc_description_ = """
    Сервис предназначен для доступа к локальным ресурсам рабочей станции (Принтеры , сканеры , и.т.д),
    через крос-доменные запросов на хоси 127.0.0.1 (localhost)
    URL:  http://127.0.0.1:%s/
    Пример обращение к сервису через JS:
    BarsPySend= function(messageObject,FunCallBack ){
        var host = "http://127.0.0.1:51003/";
        var cspBindRequestCall = new XMLHttpRequest();
        cspBindRequestCall.open('GET',host, true);
        if (typeof FunCallBack === 'function'){ 
             cspBindRequestCall.onreadystatechange = function() {
             if (this.readyState == 4 && this.status == 200) {
                if (typeof FunCallBack === 'function'){
    		    try {
    				FunCallBack(JSON.parse(decodeURIComponent(this.responseText)));
    			} catch (err) {
    			    FunCallBack(decodeURIComponent(this.responseText));
    			}
              }
             };
           };
        }
        cspBindRequestCall.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        if (typeof messageObject == "object"){
            for (var prop in messageObject) {
               cspBindRequestCall.setRequestHeader("X-My-"+prop, encodeURI(messageObject[prop]));
            }
        } else{
            cspBindRequestCall.setRequestHeader("X-My-message", encodeURI(messageObject));
        }
        cspBindRequestCall.send();
        return cspBindRequestCall; 
    }
    BarsPySend({"GetPrinterList":1},function(dat){console.log(dat);}) // получить список принтеров установленных в системе
    BarsPySend({"Print":"<h1>Привет Мир-HelloWorld</h1>","widthPage":300,"heightPage":100,"PrinterName":"Brother QL-810W"},function(dat){console.log(dat);})
    BarsPySend({"Print":"<h1>Привет Мир-HelloWorld</h1>"+Date(Date.now()).toString()}) // отправека на печать без получения ответа
    BarsPySend({"PrintUrl":"http://127.0.0.1/sprint.png" },function(dat){console.log(dat);}) // Печать сайта по URL адресу
        """ % portServer
    print(_svc_description_)
    app.run(host='0.0.0.0', port=portServer)
