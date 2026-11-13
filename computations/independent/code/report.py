"""Bounded JSON-lines reporting; failures and missing checks force nonzero exit."""
import json
import time

_expected=[]
_seen=[]
_failures=[]
_start=0
_job=None

def configure(job,expected):
    global _job,_expected,_start
    _job=job
    _expected=list(expected)
    _start=time.monotonic()

def emit(value):
    print(json.dumps(value,sort_keys=True,default=str),flush=True)

def check(cid,title,ok,info='',**details):
    if cid not in _expected or cid in _seen:
        raise RuntimeError('Unknown or repeated check ID: '+cid)
    value=bool(ok)
    _seen.append(cid)
    if not value:_failures.append(cid)
    emit({'record':'check','id':cid,'status':'PASS' if value else 'FAIL',
          'title':title,'info':str(info)[:4096],**details})

def passed(cid,title,scope,**details):
    # A calls this only after all residual checks have returned without error.
    check(cid,title,True,scope=scope,**details)

def finish(versions=None,metrics=None,error=None):
    missing=sorted(set(_expected)-set(_seen))
    ok=not (_failures or missing or error)
    emit({'record':'summary','job':_job,'status':'PASS' if ok else 'FAIL',
          'expected_count':len(_expected),'observed_count':len(_seen),
          'failed':_failures,'missing':missing,'error':error,
          'worker_seconds':round(time.monotonic()-_start,3),
          'versions':versions or {},'metrics':metrics or {}})
    return 0 if ok else 1
