from flask import abort 

def valid_response(data, parameter, model=None):
    if data:
        if str(parameter) in data:
            if str(data[parameter]).isdigit():
                if str(parameter) == "category":
                    try:
                        category = model.query.get(int(data[parameter]))
                        if not category or category == None:
                            abort(400)
                        else:
                            return True
                    except:
                        abort(400)
                elif str(parameter) == "difficulty":
                    if str(data[parameter]).isdigit():
                        return True 
                    else:
                        abort(400)
            else:
                if parameter != "type":
                    if len(str(data[parameter])) > 5:
                        return True 
                    else:
                        abort(400)
                elif parameter == "type":
                    if len(str(data[parameter])) > 3:
                        return True 
                    else:
                        abort(400)
