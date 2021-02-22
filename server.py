# from queue import Queue
#
# from flask import Flask, jsonify
# from flask import request
#
# app = Flask(__name__)
#
#
# def historical_data_server(
#         symbols,
#         queue_request_from_store: Queue,
#         queue_pipe_store_to_request: Queue,
# ):
#     with app.app_context():
#         invalid_symbol = jsonify({"text": "no symbol by this name found!"})
#         no_symbol_given = jsonify({"text": "no symbol given"})
#
#         @app.route('/')
#         def hello_world():
#             symbol = request.args.get('symbol')
#             if symbol is None:
#                 return no_symbol_given
#             symbol = symbol.lower()
#             symbol = symbol if symbol.endswith("btc") else f"{symbol}btc"
#             if symbol not in symbols:
#                 return invalid_symbol
#             queue_request_from_store.put(symbol)
#             data = queue_pipe_store_to_request.get()
#             return data["data"]
#             # return jsonify({"data": [x["event_time"] for x in data["data"]]})
#
#         app.run(debug=True)
#
#
#
#
#
#
