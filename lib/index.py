
index = """<!DOCTYPE html>
<html>
<head>
    <link href="theme_classic.css" rel="stylesheet"/>
    <script type="text/javascript" src="ext.js"></script>
    <script type="text/javascript" src="locale-ru.js"></script>
    <script type="text/javascript">
       
        Ext.onReady(function () {

            var panel1 = Ext.create('Ext.panel.Panel', {
                xtype: 'panel',
                title: 'Внутренняя панель 1',
                height: 100,
                width: '100%',
                id: "Panel1"
            });

            var panel2 = Ext.create('Ext.panel.Panel', {
                xtype: 'panel',
                title: 'Внутренняя панель 2',
                height: 600,
                width: '100%'
            });

            Ext.create('Ext.panel.Panel', {
                renderTo: Ext.getBody(),
                width: '100%',
                height: '100%',
                padding: 10,
                title: 'Основной контейнер',
                items: [panel1, panel2]
            });
            panel2.update('<h3>Вы выбрали: </h3>');
            panel2.add({
                title: 'Внутренняя панель',
                width: 300,
                height: 300,
                html: 'Привет мир!'
            });

                  var menustore = Ext.create('Ext.data.TreeStore', {
                      root: {
                          text: "Языки программирования",
                          expanded: true,
                          children: [{
                              text: "C#",
                              leaf: true
                          }, {
                              text: "C++",
                              leaf: true
                          }, {
                              text: "Java",
                              leaf: true
                          }]
                      }
                  });
                  var treemenu = Ext.create('Ext.tree.Panel', {
                      title: 'Языки программирования',
                      store: menustore,
                      width: 170,
                      rootVisible: false,
                      region: 'west',
                      listeners: {
                          itemclick: function (tree, record, item, index, e, options) {
                              var nodeText = record.data.text;
                              centerPanel.update('<h3>Вы выбрали: ' + nodeText + '</h3>');
                          }
                      }
                  });
                  var centerPanel = Ext.create('Ext.panel.Panel', {
                      title: 'Выбранный язык',
                      region: 'center'
                  });

             panel2.add(  treemenu )
             panel2.add(  centerPanel )
        });
    </script>
</head>
<body></body>
</html>"""