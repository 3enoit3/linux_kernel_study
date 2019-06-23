from bottle import run, get

symbols = ["sched_tick", "tick", "update_tick"]

@get('/symbols/<pattern>')
def getSymbols(pattern):
    return {'symbols': [s for s in symbols if pattern in s]}

run(reloader=True, debug=True)
