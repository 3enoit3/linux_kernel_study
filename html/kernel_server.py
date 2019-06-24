from bottle import run, get, response, request

symbols = ["sched_tick", "tick", "update_tick"]

# based upon https://stackoverflow.com/a/42956815
def jsonp(dictionary):
    if (request.query.callback):
        return "%s(%s)" % (request.query.callback, dictionary)
    return dictionary

@get('/symbols/<pattern>')
def getSymbols(pattern):
    if (request.query.callback):
        response.content_type = "application/javascript"
    return jsonp({'symbols': [s for s in symbols if pattern in s]})

run(reloader=True, debug=True)
