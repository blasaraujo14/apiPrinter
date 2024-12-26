from flask import Flask, request, jsonify
from datetime import datetime
import requests
import json
import cups
from PIL import Image
import numpy as np

app = Flask(__name__)

printer_name = ""
tmp_file = "tmpFile.txt"
conn = cups.Connection()

def genCommands(data, template):
    cmd = "^XA\n^FWR"
    if template == 1:
        cmd += "\n^CF0,25\n^FO517,36^FD" + data.get("nombre_empresa", "")+"^FS"
        cmd += "\n^CF0,20\n^FO522,362^FDDENOMINACION COMERCIAL:^FS\n^CF0,25\n^FO482,370^FD" + data.get("den_comercial", "")+"^FS"
        cmd += "\n^CF0,20\n^FO447,362^FDNOMBRE CIENTIFICO:^FS\n^CF0,25\n^FO407,370^FD" + data.get("nombre_cientifico", "")+"^FS"
        #cmd += "\n^CF0,25\n^FO459,656^FDHKE^FS"
        cmd += "\n^CF0,20\n^FO372,362^FDZONA DE CAPTURA:^FS\n^FO372,600^FD" + data.get("zona_captura", "")+"^FS"
        cmd += "\n^FO337,362^FDFAO^FS\n^CF0,25\n^FO302,410^FD" + data.get("fao", "")+"^FS"
        cmd += "\n^CF0,20\n^FO267,362^FDPESO NETO:^FS\n^CF0,25\n^FO232,410^FD" + data.get("peso_neto", "")+"^FS"
        cmd += "\n^CF0,20\n^FO212,540^FDKG^FS\n^CF0,15\n^FO155,295^FDCAPTURADO:^FS\n^CF0,20\n^FO150,408^FD" + data.get("fecha_capturado", "")+"^FS"
        cmd += "\n^CF0,15\n^FO155,613^FDENVASADO:^FS\n^CF0,20\n^FO150,719^FD" + data.get("fecha_envasado", "")+"^FS"
        cmd += "\n^CF0,15\n^FO155,908^FDCADUCIDAD:^FS\n^CF0,20\n^FO150,1016^FD" + data.get("fecha_caducidad", "") + "^FS"
        cmd += "\n^FO307,612^FDPRESENTACION:^FS\n^FO267,620^FD" + data.get("presentacion", "") + "^FS\n^FO212,620^FD"+ data.get("conservacion", "") + "^FS"
        cmd += "\n^FO307,882^FDMETODO PRODUCCION:^FS\n^FO267,890^FD" + data.get("metodo_prod", "") + "^FS"
        cmd += "\n^CF0,15\n^FO527,804^FD" + data.get("direccion1", "") + "^FS\n^FO503,804^FD" +  data.get("direccion2", "") + "^FS\n^FO479,804^FD" +  data.get("direccion3", "") + "^FS"
        cmd += "\n^CF0,20\n^FO450,804^FDCALIBRE:^FS\n^CF0,15\n^FO427,804^FDARTE DE PESCA:^FS\n^FO407,812^FD" + data.get("arte_pesca", "") + "^FS"
        cmd += "\n^CF0,20\n^FO382,804^FDLOTE:^FS\n^FO382,875^FD" + data.get("lote", "") + "^FS"
        cmd += "\n^FO354,804^FDBUQUE:^FS\n^FO354,894^FD" + data.get("buque", "") + "^FS"
        cmd += "\n^BY2,2,1^BQR,2,5^FO246,35^FDQ0" + data.get("codigo_qr") + "^FS"
        cmd += "\n^BY2,2,90^BC^FO40,128^FD" + data.get("codigo_barras") + "^FS"
        cmd += "\n^FO15,23^GB540,1,1^FS\n^FO195,349^GB360,1,1^FS\n^FO350,791^GB205,1,1^FS\n^FO201,599^GB130,1,1^FS\n^FO247,869^GB84,1,1^FS"
    elif template == 2:
        cmd += "\n^BY2,2,1^BQR,2,5^FO339,798^FDQ0" + data.get("codigo_qr") + "^FS"
        cmd += "\n^BY2,2,90^BC^FO44,105^FD" + data.get("codigo_barras") + "^FS"
        cmd += "\n^CF0,15\n^FO519,32^FDPRODUCTO DISTRIBUIDO POR:^FS\n^CF0,20\n^FO440,132^FD{IMG}^FS" # Añadir codigo para imagen
        cmd += "\n^CF0,15\n^FO339,32^FDPRODUCTO^FS\n^FO320,32^FDELABORADO POR:^FS" # Añadir imagen?
        cmd += "\n^FO275,32^FDFECHA EXPEDICION^FS\n^FO275,203^FD" + data.get("fecha_expedicion", "") + "^FS"
        cmd += "\n^FO247,32^FDFECHA CADUCIDAD^FS\n^FO247,203^FD" + data.get("fecha_caducidad", "") + "^FS"
        cmd += "\n^CF0,20\n^FO514,362^FDZONA DE CAPTURA:^FS\n^FO514,593^FD" + data.get("zona_captura", "") + "^FS"
        cmd += "\n^FO484,362^FDFAO^FS\n^FO484,424^FD" + data.get("fao", "") + "^FS"
        cmd += "\n^FO454,362^FDNOMBRE COMERCIAL:^FS\n^CF0,25\n^FO424,370^FD" + data.get("den_comercial", "") + "^FS"
        cmd += "\n^CF0,20\n^FO389,362^FDNOMBRE CIENTIFICO:^FS\n^CF0,25\n^FO359,370^FD" + data.get("nombre_cientifico", "") + "^FS"
        cmd += "\n^CF0,20^FO324,362^FDARTE DE PESCA:^FS\n^FO299,366^FD" + data.get("arte_pesca", "") + "^FS"
        cmd += "\n^FO259,362^FDPESO NETO:^FS\n^CF0,25\n^FO224,406^FD" + data.get("peso_neto", "") + "^FS\n^CF0,20\n^FO204,552^FDKG^FS"
        cmd += "\n^FO299,634^FDPIEZAS^FS\n^CF0,15\n^FO264,656^FDPRESENTACION:^FS\n^CF0,20\n^FO229,664^FD" + data.get("presentacion", "") + "^FS\n^CF0,15\n^FO204,664^FD" + data.get("conservacion", "") + "^FS"
        cmd += "\n^FO264,920^FDPRODUCCION:^FS\n^FO234,920^FDCAPTURADO:^FS\n^FO214,960^FD" +data.get("fecha_capturado", "") + "^FS"
        cmd += "\n^CF0,20\n^FO154,32^FDLOTE^FS\n^FO154,100^FD" + data.get("lote", "") + "^FS"
        cmd += "\n^FO154,290^FDBARCO:^FS\n^FO154,386^FD" + data.get("barco", "") + "^FS"
        cmd += "\n^FO154,746^FDIDENT. EXT:^FS\n^FO154,886^FD" + data.get("ident_ext", "") + "^FS"
        cmd += "\n^FO8,19^GB540,1,1^FS\n^FO187,349^GB360,1,1^FS\n^FO305,789^GB242,1,1^FS\n^FO101,1134^GB446,1,1^FS\n^FO195,643^GB91,1,1^FS"
    elif template == 3:
       cmd += "\n^BY2,2,90^BC^FO58,24^FD" + data.get("codigo_barras") + "^FS"
       cmd += "\n^CF0,20\n^FO518,28^FD" + data.get("nombre_empresa", "") + "^FS"
       cmd += "\n^CF0,15\n^FO466,28^FD" + data.get("direccion", "") + "^FS"
       cmd += "\n^FO279,28^FDEMBALAMENTO:^FS\n^FO279,187^FD" + data.get("fecha_embalamento", "") + "^FS"
       cmd += "\n^FO251,28^FDEXPEDIÇAO:^FS\n^FO251,187^FD" + data.get("fecha_expedicion", "") + "^FS"
       cmd += "\n^FO223,28^FDCONSUMIR ATÉ:^FS\n^FO223,187^FD" + data.get("fecha_caducidad", "") + "^FS"
       cmd += "\n^CF0,20\n^FO518,358^FDDENOMINAÇAO COMERCIAL:^FS\n^CF0,25\n^FO489,366^FD" + data.get("den_comercial", "") + "^FS"
       cmd += "\n^CF0,20\n^FO454,358^FDNOMBRE CIENTÍFICO:^FS\n^CF0,25\n^FO424,366^FD" + data.get("nombre_cientifico", "") + "^FS"
       cmd += "\n^CF0,20\n^FO367,360^FDZONA DE CAPTURA:^FS\n^FO367,585^FD" + data.get("zona_captura", "") + "^FS"
       cmd += "\n^FO337,360^FDFAO^FS\n^FO337,417^FD" + data.get("fao", "") + "^FS"
       cmd += "\n^FO438,798^FDCALIBRE:^FS\n^FO408,798^FDARTE DE PESCA:^FS\n^FO383,806^FD" + data.get("arte_pesca", "") + "^FS"
       cmd += "\n^FO318,798^FDLOTE:^FS\n^FO318,869^FD" + data.get("lote", "") + "^FS"
       cmd += "\n^FO263,358^FDPESO NETO:^FS\n^CF0,25^FO228,402^FD" + data.get("peso_neto", "") + "^FS\n^CF0,20\n^FO208,548^FDKG^FS"
       cmd += "\n^CF0,15\n^FO268,652^FDPRESENTAÇAO:^FS\n^FO238,660^FD" + data.get("presentacion", "") + "^FS\n^FO208,660^FD" + data.get("conservacion", "") + "^FS"
       cmd += "\n^FO271,880^FDMETODO DE PRODUÇAO:^FS\n^FO247,888^FD" + data.get("metodo_prod", "") + "^FS"
       cmd += "\n^CF0,20\n^FO158,28^FDBUQUE:^FS\n^FO158,124^FD" + data.get("buque", "") + "^FS"
       cmd += "\n^FO158,810^FDPAIS DE ORIGEM:^FS\n^FO158,1002^FD" + data.get("pais", "") + "^FS"
       cmd += "\n^FO11,15^GB540,1,1^FS\n^FO191,345^GB360,1,1^FS\n^FO309,785^GB242,1,1^FS\n^FO105,1130^GB446,1,1^FS\n^FO195,639^GB98,1,1^FS\n^FO234,867^GB59,1,1^FS"
    cmd += "\n^XZ"
    return cmd

@app.route('/printData', methods=['POST'])
def printData():
    global tmp_file
    # Nombres de tamplates en un archivo de configuración?
    '''
    with open('printConfig.json', 'r') as file:
        dataFile = json.load(file)
    templates = dataFile.get("templates")
    '''

    # Obtener los datos de la request
    if not request.is_json:
        data = {}
    else:
        data = request.get_json()

    #template = templates.get(data.get("template", ""))
    template = data.get("template", 0)
    if template not in [1,2,3]:
        return jsonify({"message": "Template does not exist"}), 400

    if "printer" not in data:
        return jsonify({"message": "printer not selected"}), 400
    printer = data.get("printer")
    try:
        printers = conn.getPrinters()
    except:
        return jsonify({"message": "CUPS error: getPrinters()"}), 400
    if printer not in printers:
        dev_name = ""
        try:
            devices = conn.getDevices()
        except:
            return jsonify({"message": "CUPS error: getDevices()"}), 400
        for device_uri, device_info in devices.items():
            dev_name = device_info.get("device-info", "Impresora sin nombre").replace(" ", "_")
            dev_uri = device_uri
            dev_info = device_info
            if printer == dev_name:
                break
        if printer != dev_name:
            return jsonify({"message": "printer not found"}), 400
        try:
            conn.addPrinter(
                name=printer,
                device=dev_uri,
                location=dev_info.get("device-location", ""),
                info=printer
            )
            conn.enablePrinter(printer)
            conn.acceptJobs(printer)
        except:
            return jsonify({"message": "CUPS error: addPrinter()"}), 400

    # Campos obligatorios?
    '''
    if not (nombre_empresa and nombre_cientifico and zona_captura and fao and peso_neto and
            fecha_capturado and fecha_envasado and fecha_caducidad and direccion and
            codigo_barras and codigo_qr):
        return jsonify({"error": "Faltan datos en el formulario"}), 400
    '''

    # generar etiqueta con los datos de la request
    commands = genCommands(data.get("fields", {}), template)
    print(commands)
    options = {"raw": "true"}

    with open(tmp_file, "w") as f:
        f.write(commands)
        f.close()

    try:
        conn.printFile(printer, tmp_file, "Trabajo raw", options)
        return jsonify({"message": "Impresion exitosa"}), 200
    except:
        return jsonify({"message": "CUPS error: printFile()"}), 400

@app.route('/getPrinters', methods=['GET'])
def getPrinters():
    printers = list(conn.getPrinters().keys())

    try:
        devices = conn.getDevices()
    except:
        return jsonify(), 400
    for _, device_info in devices.items():
        device_name = device_info.get("device-info", "Impresora sin nombre").replace(" ", "_")
        if device_name not in printers:
            printers.append(device_name)
    return jsonify({"printers": printers}), 200

@app.route('/statusPrinter', methods=['GET'])
def statusPrinter():
    if not request.is_json:
        data = {}
    else:
        data = request.get_json()
    if "printer" not in data:
        return jsonify({"message": "printer not selected"}), 400
    printer = data.get("printer")
    try:
        printers = conn.getPrinters()
    except:
        return jsonify({"message": "CUPS error: getPrinters()"}), 400
    if printer not in printers:
        dev_name = ""
        try:
            devices = conn.getDevices()
        except:
            return jsonify({"message": "CUPS error: getDevices()"}), 400
        for device_uri, device_info in devices.items():
            dev_name = device_info.get("device-info", "Impresora sin nombre").replace(" ", "_")
            dev_uri = device_uri
            dev_info = device_info
            if printer == dev_name:
                break
        if printer != dev_name:
            return jsonify({"message": "printer not found"}), 400
        try:
            conn.addPrinter(
                name=printer,
                device=dev_uri,
                location=dev_info.get("device-location", ""),
                info=printer
            )
            conn.enablePrinter(printer)
            conn.acceptJobs(printer)
        except:
            return jsonify({"message": "CUPS error: addPrinter()"}), 400
    try:
        attr = conn.getPrinterAttributes(printer)
    except:
        return jsonify({"message": "CUPS error: getPrinterAttributes()"}), 400
    msg = attr.get("printer-state-message", "")
    state = {
        3: "Idle",
        4: "Processing",
        5: "Stopped"
    }.get(attr.get("printer-state", 0), "Desconocido")
    return jsonify({"message": msg, "state": state}), 200

if __name__ == '__main__':
    app.run(debug=True)