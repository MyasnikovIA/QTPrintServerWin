index = """<!DOCTYPE html>
<html>
<head>
    <link href="theme_classic" rel="stylesheet"/>
    <script type="text/javascript" src="ext.js"></script>
    <script type="text/javascript" src="locale-ru.js"></script>

    <script type="text/javascript">
        Ext.onReady(function () {
            var store = Ext.create('Ext.data.TreeStore', {
                root: {
                    expanded: true,
                    children: [
                        {
                            text: 'Printers', expanded: true,
                            children: [{
                                "text": "Fax (\u043f\u0435\u0440\u0435\u043d\u0430\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u043e 1)",
                                "leaf": true
                            }, {
                                "text": "\u041e\u0442\u043f\u0440\u0430\u0432\u0438\u0442\u044c \u0432 OneNote 16 (\u043f\u0435\u0440\u0435\u043d\u0430\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u043e 1)",
                                "leaf": true
                            }, {
                                "text": "Microsoft XPS Document Writer (\u043f\u0435\u0440\u0435\u043d\u0430\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u043e 1)",
                                "leaf": true
                            }, {
                                "text": "Microsoft Print to PDF (\u043f\u0435\u0440\u0435\u043d\u0430\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u043e 1)",
                                "leaf": true
                            }, {
                                "text": "OneNote",
                                "leaf": true
                            }, {
                                "text": "\u041e\u0442\u043f\u0440\u0430\u0432\u0438\u0442\u044c \u0432 OneNote 16",
                                "leaf": true
                            }, {
                                "text": "NPIB9358E (HP LaserJet MFP M426fdn)",
                                "leaf": true
                            }, {
                                "text": "Microsoft XPS Document Writer",
                                "leaf": true
                            }, {"text": "Microsoft Print to PDF", "leaf": true}, {
                                "text": "Fax",
                                "leaf": true
                            }, {"text": "Brother QL-810W", "leaf": true}]  /* список принтеров */
                        }
                    ]
                }
            });

            var selectPrinterName = ""
            treePanel = Ext.create('Ext.tree.Panel', {
                width: "100%",
                height: "100%",
                store: store,
                rootVisible: false,
                region: 'west',
                listeners: {
                    itemclick: function (tree, record, item, index, e, options) {
                        var nodeText = record.data.text;
                        selectPrinterName = nodeText
                        centerPanel.update('<h3>Принтер: ' + nodeText + '</h3>WidthPage<input id="widthPage" type="number" placeholder="" value=300 /><br/>HeightPage<input id="heightPage" type="number" placeholder="" value=100 /> <br/><textarea id="contentPrint" rows="4" style="width:100%;"></textarea><br/><button onclick="sendPrint()">Печать</button><br/><pre id="resPrint"></pre>');
                    }
                }
            });

            Ext.create('Ext.container.Viewport', {
                layout: 'fit',
                items: [
                    {

                        layout: 'border',
                        bodyBorder: false,
                        defaults: {
                            collapsible: true,
                            split: true,
                            bodyPadding: 15
                        },
                        items: [
                            {
                                title: '',
                                region: 'west',
                                floatable: false,
                                margins: '5 0 0 0',
                                width: 275,
                                minWidth: 100,
                                maxWidth: 450,
                                id: "NavPanel",
                            }, {
                                title: '',
                                collapsible: false,
                                region: 'center',
                                margins: '5 0 0 0',
                                id: "bodyPanel",
                            }]

                    },
                ]
            });
            console.log(Ext.getCmp('NavPanel'));
            //Ext.getCmp('NavPanel').removeAll(true);
            Ext.getCmp('NavPanel').add(treePanel);
            var centerPanel = Ext.create('Ext.panel.Panel', {
                region: 'center'
            });
            Ext.getCmp('bodyPanel').add(centerPanel);

            var BarsPySend = function (messageObject, FunCallBack) {
                var host = "http://127.0.0.1:51003/";
                var cspBindRequestCall = new XMLHttpRequest();
                cspBindRequestCall.open('GET', host, true);
                if (typeof FunCallBack === 'function') {
                    cspBindRequestCall.onreadystatechange = function () {
                        if (this.readyState == 4 && this.status == 200) {
                            if (typeof FunCallBack === 'function') {
                                try {
                                    FunCallBack(JSON.parse(decodeURIComponent(this.responseText)));
                                } catch (err) {
                                    FunCallBack(decodeURIComponent(this.responseText));
                                }
                            }
                        }
                        ;
                    };
                }
                cspBindRequestCall.onerror = function (e) {
                    document.getElementById("resPrint").innerHTML = "Error " + e.target.status + " occurred while receiving the document.";
                }
                cspBindRequestCall.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
                if (typeof messageObject == "object") {
                    for (var prop in messageObject) {
                        cspBindRequestCall.setRequestHeader("X-My-" + prop, encodeURI(messageObject[prop]));
                    }
                } else {
                    cspBindRequestCall.setRequestHeader("X-My-message", encodeURI(messageObject));
                }
                cspBindRequestCall.send();
                return cspBindRequestCall;
            }
            sendPrint = function () {
                BarsPySend({
                    "Print": document.getElementById("contentPrint").value,
                    "widthPage": 300,
                    "heightPage": 100,
                    "PrinterName": selectPrinterName,
                    "widthPage":document.getElementById("widthPage").value ,
                    "heightPage":document.getElementById("heightPage").value 
                }, function (dat) {
                    document.getElementById("resPrint").innerHTML = JSON.stringify(dat)
                })
            }
        });
    </script>
</head>
<body></body>"""
