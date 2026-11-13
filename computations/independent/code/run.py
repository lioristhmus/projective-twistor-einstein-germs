"""Host-only serial Docker controller. All mathematics runs in the container."""
import argparse
import datetime
from hashlib import sha256
import json
import os
from pathlib import Path
import platform
import resource
import subprocess
import sys
import time
import uuid

ROOT=Path(__file__).resolve().parents[1]
ENV=json.loads((ROOT/'environment.lock.json').read_text())
MEM=ENV['memory_bytes']
MAXLOG=ENV['log_bytes']
LOCK=Path.home()/'.local/state/math-job.lock'

def command(argv,check=True,timeout=30):
    proc=subprocess.run(argv,check=False,capture_output=True,text=True,timeout=timeout)
    if check and proc.returncode:
        # Do not copy full Docker diagnostics or host paths into distributed metadata.
        raise RuntimeError('Command failed: '+argv[0]+' '+argv[1]+'; exit '+str(proc.returncode))
    return proc

def docker(*argv,check=True):return command(['docker',*argv],check=check)

def inspect(name):
    p=docker('container','inspect',name,check=False)
    if p.returncode:
        if 'no such' in (p.stderr+p.stdout).lower():return None
        raise RuntimeError('Cannot establish container state')
    return json.loads(p.stdout)[0]

def digest(path):return sha256(path.read_bytes()).hexdigest()

def check_services(allowed):
    names=docker('ps','--format','{{.Names}}').stdout.splitlines()
    if not set(names)<=set(allowed):raise RuntimeError('Unapproved running containers; no job started')
    data=json.loads(docker('inspect',*names).stdout) if names else []
    # Preserve resource facts without copying service names or other host configuration.
    limits=[{'alias':'service-'+str(i+1),'memory':x['HostConfig']['Memory'],
       'memory_swap':x['HostConfig']['MemorySwap'],'nano_cpus':x['HostConfig']['NanoCpus'],
       'pids_limit':x['HostConfig'].get('PidsLimit')} for i,x in enumerate(data)]
    stats=[]
    for name in names:
        d=json.loads(docker('stats','--no-stream','--format','{{json .}}',name).stdout)
        stats.append({k:d[k] for k in ('MemUsage','CPUPerc','PIDs')})
    return {'limits':limits,'usage':stats}

def run(args):
    jobs=json.loads((ROOT/'jobs.json').read_text())
    if args.job not in jobs and args.job!='failure-probe':raise RuntimeError('Unknown job')
    info=json.loads(docker('info','--format','{{json .}}').stdout)
    if not (info['MemoryLimit'] and info['SwapLimit'] and info['PidsLimit'] and info['CgroupVersion']=='2'):
        raise RuntimeError('Required cgroup enforcement unavailable')
    if info['MemTotal']<6_000_000_000:raise RuntimeError('VM headroom below the retained profile')
    im=json.loads(docker('image','inspect',ENV['image_reference']).stdout)[0]
    if im['Id']!=ENV['local_image_id'] or im['Os']+'/'+im['Architecture']!=ENV['image_platform']:
        raise RuntimeError('Pinned existing image/platform mismatch; no pull is attempted')
    services=check_services(args.allow_service)
    out=Path(args.out).resolve() if args.out else ROOT/'results'/args.job
    out.mkdir(parents=True,exist_ok=False)
    name='local-twistor-supp-'+uuid.uuid4().hex[:12]
    utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
    owner={'executor':'computational-supplement runner','utc_start':utc,'job':args.job,'container':name}
    command(['mkdir',str(LOCK)])  # Atomic machine-wide exclusion; never remove another owner's lock.
    (LOCK/'owner').write_text(json.dumps(owner)+'\n')
    env={'job':args.job,'utc_start':utc,'mathematics_on_host':False,
      'vm':{k:info[k] for k in ('OperatingSystem','ServerVersion','CgroupVersion','MemTotal','NCPU')},
      'host':{'system':platform.system(),'machine':platform.machine()},
      'other_services':services,'image':{k:im[k] for k in ('Id','RepoDigests','Architecture','Os')},
      'limits':ENV,'input_hashes':{str(p.relative_to(ROOT)):digest(p) for p in
          sorted([ROOT/'code'/n for n in ['run.py','worker.py','report.py']+(jobs[args.job]['dependencies'] if args.job!='failure-probe' else [])]+[ROOT/'inputs.json',ROOT/'jobs.json',ROOT/'environment.lock.json'])}}
    attempted=False;stopped=False;removed=False;released=False
    client_exit=None;error=None;started=time.monotonic()
    try:
        # Recheck after obtaining the global lock, before creating the container.
        check_services(args.allow_service)
        attempted=True
        argv=['create','--name',name,'--pull=never','--platform',ENV['image_platform'],
          '--network=none','--read-only','--memory',str(MEM),'--memory-swap',str(MEM),
          '--cpus','1','--pids-limit','32','--restart=no','--cap-drop=ALL',
          '--security-opt=no-new-privileges','--ulimit','nofile=256:256',
          '--ulimit','fsize=1048576:1048576','--ulimit','core=0:0',
          '--log-driver=local','--log-opt','max-size=1m','--log-opt','max-file=1','--log-opt','compress=false',
          '--tmpfs','/tmp:rw,nosuid,nodev,size=67108864,mode=1777',
          '--tmpfs','/work:rw,nosuid,nodev,size=201326592,mode=1777',
          '--mount','type=bind,src='+str(ROOT)+',dst=/supplement,readonly','--workdir','/work']
        for nameval in ('HOME=/tmp/home','XDG_CACHE_HOME=/tmp/cache','SAGE_DOT_SAGE=/tmp/dot_sage',
              'PYTHONDONTWRITEBYTECODE=1','OMP_NUM_THREADS=1','OPENBLAS_NUM_THREADS=1',
              'MKL_NUM_THREADS=1','SAGE_NUM_THREADS=1','NUMEXPR_MAX_THREADS=1'):
            argv+=['--env',nameval]
        argv+=['--entrypoint','/bin/sh',ENV['image_reference'],'-c',
          'mkdir -p /tmp/home /tmp/cache /tmp/dot_sage && exec timeout -s TERM -k 3s 297s timeout -s TERM -k 3s 117s sage -python /supplement/code/worker.py '+args.job]
        docker(*argv)
        data=inspect(name);hc=data['HostConfig']
        if not (hc['Memory']==hc['MemorySwap']==MEM and hc['NanoCpus']==1_000_000_000 and hc['PidsLimit']==32 and
            hc['NetworkMode']=='none' and hc['ReadonlyRootfs'] and not hc.get('OomKillDisable',False) and hc['RestartPolicy']['Name']=='no'):
            raise RuntimeError('Docker HostConfig does not enforce requested limits')
        env['host_config']={k:hc.get(k) for k in ('Memory','MemorySwap','NanoCpus','PidsLimit','NetworkMode',
           'ReadonlyRootfs','OomKillDisable','RestartPolicy','Tmpfs','Ulimits','LogConfig','CapDrop','SecurityOpt')}
        print('Verified limits; foreground job '+args.job,flush=True)
        def caplog():resource.setrlimit(resource.RLIMIT_FSIZE,(MAXLOG,MAXLOG))
        with (out/'log.jsonl').open('x') as log:
            try:
                proc=subprocess.run(['docker','start','--attach',name],stdout=log,stderr=subprocess.STDOUT,
                  timeout=max(1,300-(time.monotonic()-started)),preexec_fn=caplog)
                client_exit=proc.returncode
            except subprocess.TimeoutExpired:error='host deadline'
    except BaseException as exc:
        error=type(exc).__name__+': '+str(exc)[:512]
    finally:
        try:
            data=inspect(name) if attempted else None
            if data is not None:
                if data['State']['Running']:
                    docker('kill','--signal=KILL',name);docker('wait',name)
                    data=inspect(name)
                if data['State']['Running']:raise RuntimeError('Container still running')
                stopped=True
                env['container_state']={k:data['State'][k] for k in ('Status','Running','ExitCode','OOMKilled','StartedAt','FinishedAt')}
                docker('rm',name)
                if inspect(name) is not None:raise RuntimeError('Container removal not confirmed')
                removed=True
            else:
                stopped=True;removed=True
            if json.loads((LOCK/'owner').read_text())!=owner:raise RuntimeError('Lock ownership changed')
            (LOCK/'owner').unlink();LOCK.rmdir();released=True
        except BaseException as exc:
            error=(error+'; ' if error else '')+'cleanup: '+type(exc).__name__+': '+str(exc)[:512]
        env.update(client_exit_code=client_exit,container_stopped=stopped,container_removed=removed,
          lock_released=released,controller_seconds=round(time.monotonic()-started,3),error=error)
        (out/'environment.json').write_text(json.dumps(env,indent=2)+'\n')
    records=[]
    log=out/'log.jsonl'
    if log.exists() and log.stat().st_size<MAXLOG:
        for line in log.read_text().splitlines():
            try:records.append(json.loads(line))
            except json.JSONDecodeError:pass
    checks=[x for x in records if x.get('record')=='check']
    summaries=[x for x in records if x.get('record')=='summary']
    expected=jobs[args.job]['check_ids'] if args.job!='failure-probe' else ['RUNNER-FAILURE-PROBE']
    observed=[x['id'] for x in checks]
    summary=summaries[-1] if len(summaries)==1 else None
    ok=bool(client_exit==0 and not error and stopped and removed and released and summary and summary['status']=='PASS' and
       len(observed)==len(expected) and set(observed)==set(expected) and all(x['status']=='PASS' for x in checks) and
       env.get('container_state',{}).get('ExitCode')==0 and not env.get('container_state',{}).get('OOMKilled'))
    result={'job':args.job,'status':'PASS' if ok else 'FAIL','client_exit_code':client_exit,
      'checks':checks,'worker_summary':summary,'stopped':stopped,'removed':removed,'lock_released':released,
      'log_sha256':digest(log) if log.exists() else None,'error':error}
    (out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'job':args.job,'status':result['status'],'exit':client_exit,
      'container_removed':removed,'lock_released':released,'controller_seconds':env['controller_seconds']}),flush=True)
    return 0 if ok else 1

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--job',required=True)
    ap.add_argument('--out',help='New output directory; existing directories are refused')
    ap.add_argument('--allow-service',action='append',default=[],help='Explicit known non-mathematical service; all other running containers block execution')
    args=ap.parse_args()
    try:sys.exit(run(args))
    except Exception as exc:
        print(type(exc).__name__+': '+str(exc),file=sys.stderr);sys.exit(2)
