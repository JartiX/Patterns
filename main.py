from flask import Flask, request
from Src.settings_manager import settings_manager
from Src.Storage.storage import storage
from Src.errors import error_proxy
from Src.Logics.report_factory import report_factory
from Src.Logics.start_factory import start_factory
from datetime import datetime
from Src.Logics.storage_service import storage_service
from Src.Models.nomenclature_model import nomenclature_model


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# Сформировать начальный набор данных
options = settings_manager() 
start = start_factory(options.settings)
start.create()


@app.route("/api/report/<storage_key>", methods = ["GET"])
def get_report(storage_key: str):
    """
        Сформировать отчет
    Args:
        storage_key (str): Ключ - тип данных: номенклатура, группы и т.д.
    """
    
    keys = storage.storage_keys( start.storage )
    if storage_key == "" or  storage_key not in keys:
        return error_proxy.create_error_response(app, f"Некорректный передан запрос! Необходимо передать: /api/report/<storage_key>. Список ключей (storage_key): {keys}.", 400)
    
    # Создаем фабрику
    report = report_factory()
    data = start.storage.data
    
    # Формируем результат
    try:
        result = report.create_response( options.settings.report_mode, data, storage_key, app )  
        return result
    except Exception as ex:
        return error_proxy.create_error_response(app, f"Ошибка при формировании отчета {ex}", 500)

@app.route("/api/storage/turns", methods = ["GET"] )
def get_turns():
    # Получить параметры
    args = request.args
    if "start_period" not in args.keys():
        return error_proxy.create_error_response(app, "Необходимо передать параметры: start_period, stop_period!")
        
    if "stop_period" not in args.keys():
        return error_proxy.create_error_response(app, "Необходимо передать параметры: start_period, stop_period!")
    
    start_date = datetime.strptime(args["start_period"], "%Y-%m-%d")
    stop_date = datetime.strptime(args["stop_period"], "%Y-%m-%d")
          
    source_data = start.storage.data[  storage.storage_transaction_key()   ]      
    data = storage_service( source_data   ).create_turns( start_date, stop_date )      
    result = storage_service.create_response( data, app )
    return result
      
      
@app.route("/api/storage/<nomenclature_id>/turns", methods = ["GET"] )
def get_turns_nomenclature(nomenclature_id):
    
    # Получить параметры
    args = request.args
    if "start_period" not in args.keys():
        return error_proxy.create_error_response(app, "Необходимо передать параметры: start_period, stop_period!")

    if "stop_period" not in args.keys():
        return error_proxy.create_error_response(app, "Необходимо передать параметры: start_period, stop_period!")

    start_date = datetime.strptime(args["start_period"], "%Y-%m-%d")
    stop_date = datetime.strptime(args["stop_period"], "%Y-%m-%d")

    transactions_data = start.storage.data[  storage.storage_transaction_key()   ]   
    nomenclature_data =  start.storage.data[  storage.nomenclature_key()   ]   
    
    nomenclatures = {}
    for i in nomenclature_data:
        nomenclatures[i.id] = i

    ids = [item.id for item in nomenclatures.values()]
    if nomenclature_id not in ids:
        return error_proxy.create_error_response(app, "Некорректно передан код номенклатуры!")
    nomenclature = nomenclatures[nomenclature_id]
      
    data = storage_service( transactions_data  ).create_turns_by_nomenclature( start_date, stop_date, nomenclature )      
    result = storage_service.create_response( data, app )
    return result      

@app.route("/api/storage/<storage_id>/get_turns", methods = ["GET"] )
def get_turns_storage(storage_id):
    args = request.args
    if "start_period" not in args.keys():
        return error_proxy.create_error_response(app, "Необходимо передать параметры: start_period, stop_period, nomenclature_id!")

    if "stop_period" not in args.keys():
        return error_proxy.create_error_response(app, "Необходимо передать параметры: start_period, stop_period, nomenclature_id!")
    
    if "nomenclature_id" not in args.keys():
        return error_proxy.create_error_response(app, "Необходимо передать параметры: start_period, stop_period, nomenclature_id!")
    
    start_date = datetime.strptime(args["start_period"], "%Y-%m-%d")
    stop_date = datetime.strptime(args["stop_period"], "%Y-%m-%d")
    nomenclature_id = args['nomenclature_id']
    
    transactions_data = start.storage.data[  storage.storage_transaction_key()   ]   
    nomenclature_data =  start.storage.data[  storage.nomenclature_key()   ]   
    
    nomenclature_dict = {}
    for i in nomenclature_data:
        nomenclature_dict[i.id] = i
    
    
    ids = [item.id for item in nomenclature_dict.values()]
    if nomenclature_id not in ids:
        return error_proxy.create_error_response(app, "Некорректно передан код номенклатуры!")
    nomenclature = nomenclature_dict[nomenclature_id]

    storage_dict = {}
    for i in transactions_data:
        storage_dict[i.storage.id] = i.storage

    ids = [item.id for item in storage_dict.values()]
    if storage_id not in ids:
        return error_proxy.create_error_response(app, "Некорректно передан код склада!")
    storage_ = storage_dict[storage_id]

    
    data = storage_service( transactions_data  ).create_turns_by_nomenclature_and_storage( start_date, stop_date, nomenclature, storage_)
    
    result = storage_service.create_response( data, app )

    return result


@app.route("/api/storage/storages", methods = ["GET"] )
def get_storage():
    transactions_data = start.storage.data[  storage.storage_transaction_key()   ]  
    storages = []
    for i in transactions_data:
        if i.storage.id not in storages:
            storages.append(i.storage.id)
    result = storage_service.create_response( storages, app )

    return result
    

if __name__ == "__main__":
    app.run(debug = True)