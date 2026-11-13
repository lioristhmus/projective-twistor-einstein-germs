"""Container-only entry point. Resource preflight precedes all math imports."""
import importlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import sys
import traceback
import report

MEMORY=1999998976
ROOT=Path(__file__).resolve().parents[1]

def preflight():
    if not __debug__:raise RuntimeError('Optimized Python is not supported')
    cg=Path('/sys/fs/cgroup')
    lim={k:(cg/k).read_text().strip() for k in ('memory.max','memory.swap.max','cpu.max','pids.max')}
    q,p=map(int,lim['cpu.max'].split())
    if not (int(lim['memory.max'])<=MEMORY and lim['memory.swap.max']=='0' and 0<q<=p and int(lim['pids.max'])<=32):
        raise RuntimeError('Resource limits not enforced: '+str(lim))
    interfaces={line.split(':',1)[0].strip() for line in Path('/proc/net/dev').read_text().splitlines() if ':' in line}
    flags={n:int(Path('/sys/class/net',n,'flags').read_text(),16) for n in interfaces}
    routes=Path('/proc/net/route').read_text().splitlines()
    ipv6=Path('/proc/net/if_inet6').read_text().splitlines()+Path('/proc/net/ipv6_route').read_text().splitlines()
    if not ('lo' in interfaces and all(not (f&1) for n,f in flags.items() if n!='lo') and len(routes)==1 and all(l.split()[-1]=='lo' for l in ipv6)):
        raise RuntimeError('Network isolation not verified')
    report.emit({'record':'preflight','cgroup':lim,'interface_flags':flags,'ipv4_route_rows':len(routes)-1,'ipv6_only_loopback':True})

def main():
    job=sys.argv[1]
    jobs=json.loads((ROOT/'jobs.json').read_text())
    if job=='failure-probe':entry={'check_ids':['RUNNER-FAILURE-PROBE']}
    else:entry=jobs[job]
    report.configure(job,entry['check_ids'])
    error=None;versions={}
    try:
        preflight()
        versions={'python':platform.python_version(),'sympy':importlib.metadata.version('sympy'),
                  'platform':platform.system(),'machine':platform.machine(),'numpy':importlib.metadata.version('numpy')}
        from sage.env import SAGE_VERSION
        versions['sage']=SAGE_VERSION
        if job=='failure-probe':
            report.check('RUNNER-FAILURE-PROBE','Intentional false check: must exit nonzero',False)
        else:
            module=importlib.import_module(entry['module'])
            function=getattr(module,entry['function'])
            if 'family' in entry:
                label=entry['family'];function(label,getattr(module,'h'+label))
            elif 'profile' in entry:function(entry['profile'])
            else:function()
    except BaseException as exc:
        error=type(exc).__name__+': '+str(exc)[:4096]
        traceback.print_exc(limit=8)
    metrics={}
    for name in ('memory.peak','pids.peak','cpu.stat'):
        path=Path('/sys/fs/cgroup')/name
        if path.exists():metrics[name]=path.read_text().strip()
    return report.finish(versions,metrics,error)

if __name__=='__main__':sys.exit(main())
