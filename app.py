from flask import Flask, request, jsonify
import cups
import numpy as np

app = Flask(__name__)

printer_name = ""
tmp_file = "tmpFile.txt"
conn = cups.Connection()

def genCommands(data, template):
    cmd = "^Q150,0,0\n^W70\n^H5\n^P1\n^S2\n^AD\n^C1\n^R0\n~Q+0\n^O0\n^D0\n^E12\n~R255\n^XSET,ROTATION,0\n^L\nDy2-me-dd\nTh:m:s\nDy2-me-dd\nTh:m:s"
    if template == 1:
        cmd += "\nAC,28,1174,1,1,0,3,"+ data.get("nombre_empresa", "")
        cmd += "\nAB,28,848,1,1,0,3,DENOMINACION COMERCIAL\nAC,63,840,1,1,0,3," + data.get("den_comercial", "")
        cmd += "\nAB,103,848,1,1,0,3,NOMBRE CIENTIFICO:\nAC,138,840,1,1,0,3," + data.get("nombre_cientifico", "")
        cmd += "\nAB,178,848,1,1,0,3,ZONA DE CAPTURA:\nAB,178,610,1,1,0,3," + data.get("zona_captura", "")
        cmd += "\nAB,213,848,1,1,0,3,FAO\nAC,243,800,1,1,0,3," + data.get("fao", "")
        cmd += "\nAB,283,848,1,1,0,3,PESO NETO:\nAC,313,800,1,1,0,3,"+ data.get("peso_neto", "") + "\nAB,338,670,1,1,0,3,KG"
        cmd += "\nAA,400,915,1,1,0,3,CAPTURADO:\nAB,400,802,1,1,0,3," + data.get("fecha_capturado", "")
        cmd += "\nAA,400,597,1,1,0,3,ENVASADO:\nAB,400,491,1,1,0,3," + data.get("fecha_envasado", "")
        cmd += "\nAA,400,302,1,1,0,3,CADUCIDAD:\nAB,400,194,1,1,0,3," + data.get("fecha_caducidad", "")
        cmd += "\nAB,243,598,1,1,0,3,PRESENTACION:\nAB,283,590,1,1,0,3," + data.get("presentacion", "") + "\nAB,338,590,1,1,0,3," + data.get("conservacion", "")
        cmd += "\nAB,243,328,1,1,0,3,METODO PRODUCCION:\nAB,283,320,1,1,0,3," + data.get("metodo_prod", "")
        cmd += "\nAA,28,406,1,1,0,3," + data.get("direccion1", "") + "\nAA,52,406,1,1,0,3," + data.get("direccion2", "") + "\nAA,76,406,1,1,0,3," + data.get("direccion3", "")
        cmd += "\nAB,100,406,1,1,0,3,CALIBRE:\nAA,128,406,1,1,0,3,ARTE DE PESCA:\nAA,148,398,1,1,0,3," + data.get("arte_pesca", "")
        cmd += "\nAB,168,406,1,1,0,3,LOTE:\nAB,168,335,1,1,0,3," + data.get("lote", "")
        cmd += "\nAB,196,406,1,1,0,3,BUQUE:\nAB,196,316,1,1,0,3," + data.get("buque", "")
        cmd += "\nLo,14,1186,554,1186\nLo,14,860,374,860\nLo,14,418,219,418\nLo,238,610,368,610\nLo,238,340,322,340"
        cmd += "\nBQ,442,1091,2,5,66,3,1," + data.get("codigo_barras", "")
        if data.get("codigo_qr", "") != "":
            cmd += "\nW125,1180,5,2,M,8,7,41,3\n" + data.get("codigo_qr")
    elif template == 2:
        cmd += "\nAA,28,1174,1,1,0,3,PRODUCTO DISTRIBUIDO POR:" # Añadir codigo para imagen
        cmd += "\nAA,208,1174,1,1,0,3,PRODUCTO\nAA,227,1174,1,1,0,3,ELABORADO POR:" # Añadir imagen?
        cmd += "\nAA,272,1174,1,1,0,3,FECHA EXPEDICION\nAA,272,1003,1,1,0,3," + data.get("fecha_expedicion", "")
        cmd += "\nAA,300,1174,1,1,0,3,FECHA CADUCIDAD\nAA,300,1003,1,1,0,3," + data.get("fecha_caducidad", "")
        cmd += "\nAB,28,844,1,1,0,3,ZONA DE CAPTURA:\nAB,28,613,1,1,0,3," + data.get("zona_captura", "")
        cmd += "\nAB,58,844,1,1,0,3,FAO\nAB,58,782,1,1,0,3," + data.get("fao", "")
        cmd += "\nAB,88,844,1,1,0,3,NOMBRE COMERCIAL:\nAC,113,836,1,1,0,3," + data.get("den_comercial", "")
        cmd += "\nAB,153,844,1,1,0,3,NOMBRE CIENTIFICO:\nAC,178,836,1,1,0,3," + data.get("nombre_cientifico", "")
        cmd += "\nAB,218,844,1,1,0,3,ARTE DE PESCA:\nAB,243,840,1,1,0,3," + data.get("arte_pesca", "")
        cmd += "\nAB,283,844,1,1,0,3,PESO NETO:\nAC,313,800,1,1,0,3," + data.get("peso_neto", "") + "\nAB,338,654,1,1,0,3,KG"
        cmd += "\nAB,243,572,1,1,0,3,PIEZAS\nAA,283,550,1,1,0,3,PRESENTACION:\nAB,313,542,1,1,0,3," + data.get("presentacion", "") + "\nAA,343,542,1,1,0,3," + data.get("conservacion", "")
        cmd += "\nAA,283,286,1,1,0,3,PRODUCCION:\nAA,313,286,1,1,0,3," + data.get("produccion", "")
        cmd += "\nAB,388,1174,1,1,0,3,LOTE\nAB,388,1106,1,1,0,3," + data.get("lote", "")
        cmd += "\nAB,388,916,1,1,0,3,BARCO:\nAB,388,820,1,1,0,3," + data.get("barco", "")
        cmd += "\nAB,388,460,1,1,0,3,IDENT. EXT:\nAB,388,320,1,1,0,3," + data.get("ident_ext", "")
        cmd += "\nLo,14,1186,554,1186\nLo,14,856,374,856\nLo,14,416,256,416\nLo,14,71,460,71\nLo,275,562,366,562"
        cmd += "\nBQ,433,1097,2,5,79,3,1," + data.get("codigo_barras", "")
        if data.get("codigo_qr", "") != "":
            cmd += "\nW28,404,5,2,M,8,7,32,3\n" + data.get("codigo_qr", "")
    elif template == 3:
        cmd += "\nAB,28,1174,1,1,0,3," + data.get("nombre_empresa", "")
        cmd += "\nAA,85,1174,1,1,0,3," + data.get("direccion", "")
        cmd += "\nAA,272,1174,1,1,0,3,EMBALAMENTO:\nAA,272,1015,1,1,0,3," + data.get("fecha_embalamento", "")
        cmd += "\nAA,300,1174,1,1,0,3,EXPEDIÇAO:\nAA,300,1015,1,1,0,3," + data.get("fecha_expedicion", "")
        cmd += "\nAA,328,1174,1,1,0,3,CONSUMIR ATÉ:\nAA,328,1015,1,1,0,3," + data.get("fecha_caducidad", "")
        cmd += "\nAB,28,844,1,1,0,3,DENOMINAÇAO COMERCIAL:\nAC,52,836,1,1,0,3," + data.get("den_comercial", "")
        cmd += "\nAB,92,844,1,1,0,3,NOMBRE CIENTÍFICO:\nAC,117,836,1,1,0,3," + data.get("nombre_cientifico", "")
        cmd += "\nAB,179,842,1,1,0,3,ZONA DE CAPTURA:\nAB,179,617,1,1,0,3," + data.get("zona_captura", "")
        cmd += "\nAB,209,842,1,1,0,3,FAO\nAB,209,785,1,1,0,3," + data.get("fao", "")
        cmd += "\nAB,108,404,1,1,0,3,CALIBRE:\nAB,138,404,1,1,0,3,ARTE DE PESCA:\nAB,163,396,1,1,0,3," + data.get("arte_pesca", "")
        cmd += "\nAB,228,404,1,1,0,3,LOTE:\nAB,228,333,1,1,0,3," + data.get("lote", "")
        cmd += "\nAB,283,844,1,1,0,3,PESO NETO:\nAC,313,800,1,1,0,3," + data.get("peso_neto", "") + "\nAB,338,654,1,1,0,3,KG"
        cmd += "\nAA,283,550,1,1,0,3,PRESENTAÇAO:\nAA,313,542,1,1,0,3," + data.get("presentacion", "") + "\nAA,343,542,1,1,0,3," + data.get("conservacion", "")
        cmd += "\nAA,280,322,1,1,0,3,METODO DE PRODUÇAO:\nAA,304,314,1,1,0,3," + data.get("metodo_prod", "")
        cmd += "\nAB,388,1174,1,1,0,3,BUQUE:\nAB,388,1078,1,1,0,3," + data.get("buque", "")
        cmd += "\nAB,388,392,1,1,0,3,PAIS DE ORIGEM:\nAB,388,200,1,1,0,3," + data.get("pais", "")
        cmd += "\nLo,14,1186,554,1186\nLo,14,856,374,856\nLo,14,416,256,416\nLo,14,71,460,71\nLo,272,562,370,562\nLo,272,334,331,334"
        cmd += "\nBQ,426,1170,2,5,79,3,1," + data.get("codigo_barras", "")
    cmd += "\nE"
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

    template = data.get("template", 0)
    if template not in [1,2,3]:
        return jsonify({"message": "Template does not exist"}), 400

    if "printer" not in data:
        return jsonify({"message": "printer not selected"}), 400
    printer = data.get("printer")
    try:
        printers = conn.getPrinters()
    except:
        return jsonify({"message": ""}), 400
    if printer not in printers:
        # guardar nueva impresora
        dev_name = ""
        try:
            devices = conn.getDevices()
        except:
            return jsonify(), 400
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
            return jsonify({}), 400

    # Campos obligatorios?
    '''
    if not (nombre_empresa and nombre_cientifico and zona_captura and fao and peso_neto and
            fecha_capturado and fecha_envasado and fecha_caducidad and direccion and
            codigo_barras and codigo_qr):
        return jsonify({"error": "Faltan datos en el formulario"}), 400
    '''

    # generar etiqueta con los datos de la request
    commands = genCommands(data.get("fields", {}), template)
    options = {"raw": "true"}

    with open(tmp_file, "w") as f:
        f.write(commands)

    try:
        conn.printFile(printer, tmp_file, "Trabajo raw", options)
        return jsonify({"message": "Impresion exitosa"}), 200
    except:
        return jsonify({"message": ""}), 400
    

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


if __name__ == '__main__':
    app.run(debug=True)