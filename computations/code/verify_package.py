"""Host-side file and saved-record QA only; no mathematical imports or execution."""
import argparse
import ast
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import re
import sys

ROOT=Path(__file__).resolve().parents[1]
def digest(p):return sha256(p.read_bytes()).hexdigest()
def read(name):return json.loads((ROOT/name).read_text())
def require(ok,message):
    if not ok:raise RuntimeError(message)


def verify_independent(files):
    """Check saved source/record correspondence; never run mathematical code."""
    group=read('checks.json')['independent_evidence']
    require(len(group)==1,'Independent evidence group count')
    entry=group[0];cid='IW-GEOMETRY-CONTROLS-R2'
    require(entry['id']==cid and entry['classification']=='finite-exact','Independent evidence ID/type')
    require(entry['evidence_role']=='independent-implementation-witness','Independent role')
    require(entry['adapter_enforces_witness_negative_controls'] is True
            and entry['upstream_printed_controls_are_pass_conditions'] is False,'Independent control attribution')
    base=ROOT/'independent';job='witness-r2'
    jobs=json.loads((base/'jobs.json').read_text())
    require(set(jobs)=={job} and jobs[job]['check_ids']==[cid],'Independent jobs')
    for name in ('code/run.py','code/worker.py','code/report.py','environment.lock.json'):
        require((base/name).read_bytes()==(ROOT/name).read_bytes(),'Independent harness differs: '+name)
    env=read(entry['environment']);result=read(entry['result'])
    required={'code/run.py','code/worker.py','code/report.py','jobs.json','inputs.json','environment.lock.json'}
    required|={'code/'+n for n in jobs[job]['dependencies']}
    require(set(env['input_hashes'])==required,'Independent executed dependency set')
    for name,value in env['input_hashes'].items():
        require(digest(base/name)==value,'Independent executed input hash: '+name)
    log=ROOT/entry['log']
    require(digest(log)==result['log_sha256'],'Independent log digest')
    records=[json.loads(line) for line in log.read_text().splitlines()]
    summaries=[x for x in records if x.get('record')=='summary']
    pre=[x for x in records if x.get('record')=='preflight']
    checks=[x for x in records if x.get('record')=='check']
    require(len(summaries)==len(pre)==len(checks)==1,'Independent log record counts')
    require(summaries[0]==result['worker_summary'] and checks==result['checks'],'Independent log/result correspondence')
    require(result['job']==env['job']==job and checks[0]['id']==cid,'Independent job/ID mismatch')
    require(result['status']==summaries[0]['status']==checks[0]['status']=='PASS','Independent run not PASS')
    require(result['client_exit_code']==env['container_state']['ExitCode']==0,'Independent nonzero exit')
    require(not summaries[0]['failed'] and not summaries[0]['missing'] and summaries[0]['error'] is None,'Independent summary failure')
    require(result['error'] is None and env['error'] is None,'Independent controller error')
    require(all(result[k] for k in ('stopped','removed','lock_released')),'Independent cleanup')
    require(all(env[k] for k in ('container_stopped','container_removed','lock_released')),'Independent environment cleanup')
    require(env['mathematics_on_host'] is False,'Independent host isolation')
    require(env['limits']==read('environment.lock.json'),'Independent limits')
    h=env['host_config'];cg=pre[0]['cgroup'];q,p=map(int,cg['cpu.max'].split())
    require(h['Memory']==h['MemorySwap']==1_999_998_976,'Independent memory cap')
    require(h['NanoCpus']==1_000_000_000 and h['PidsLimit']==32,'Independent CPU/PID cap')
    require(h['NetworkMode']=='none' and h['ReadonlyRootfs'] and not h['OomKillDisable'],'Independent isolation')
    require(h['RestartPolicy']['Name']=='no','Independent restart policy')
    require(0<int(cg['memory.max'])<=2_000_000_000 and cg['memory.swap.max']=='0','Independent cgroup memory')
    require(0<q<=p and 0<int(cg['pids.max'])<=32,'Independent cgroup CPU/PIDs')
    require(pre[0]['ipv4_route_rows']==0 and pre[0]['ipv6_only_loopback'],'Independent network preflight')
    require(env['container_state']['Running'] is False and not env['container_state']['OOMKilled'],'Independent stopped/OOM')
    require(env['controller_seconds']<300,'Independent wall deadline')
    require(env['image']['Id']==env['limits']['local_image_id'],'Independent pinned image')
    require(checks[0]['classification']=='finite-exact' and checks[0]['max_r']==2,'Independent result scope')
    reps=checks[0]['witnesses']
    positive={'kasner','two-wave','single-wave-1','single-wave-2','kottler'}
    negative={'non-Einstein-kasner','non-Einstein-trial'}
    require(set(reps)==positive|negative,'Independent witness set')
    expected_rows={'r1+','r1-','r2+','r2-'}
    nc1,nc3='NC1 sign(R_U)->-1','NC3 Lambda/3->2Lambda/3'
    for name,w in reps.items():
        require(set(w['poly_Q_vs_geometric_Q'])==expected_rows,'Independent order scope')
        require(set(w['geometric_ricci_identity(any metric)'])==expected_rows
                and all(w['geometric_ricci_identity(any metric)'].values()),'Independent geometric identity')
        if name in positive:
            require(w['einstein_residual_terms']==0 and all(w['Q0_zero(Bianchi)'].values()),'Independent Einstein/Q0')
            require(all(v['mismatches']==0 for v in w['poly_Q_vs_geometric_Q'].values()),'Independent positive mismatch')
        else:
            require(w['einstein_residual_terms']>0 and not any(w['Q0_zero(Bianchi)'].values()),'Independent non-Einstein/Q0')
            require(all(v['mismatches']>0 for v in w['poly_Q_vs_geometric_Q'].values()),'Independent negative not detected')
    for name in ('kasner','kottler'):
        require(all(v>0 for v in reps[name]['wrong_convention_mismatches'][nc1].values()),'Independent NC1 not detected')
    require(reps['two-wave']['wrong_convention_mismatches'][nc1]['r2+']>0,'Independent mixed NC1')
    require(all(v>0 for v in reps['kottler']['wrong_convention_mismatches'][nc3].values()),'Independent NC3 not detected')
    for name in ('kasner','two-wave'):
        require(all(v==0 for v in reps[name]['wrong_convention_mismatches'][nc3].values()),'Independent Lambda-zero control')
    require(str(reps['kottler']['Lambda'])=='-1/10','Independent Lambda convention')
    require(reps['single-wave-1']['U0_plus_nonzero'] and not reps['single-wave-1']['U0_minus_nonzero'],'Independent first wave')
    require(reps['single-wave-2']['U0_minus_nonzero'] and not reps['single-wave-2']['U0_plus_nonzero'],'Independent second wave')
    require(digest(ROOT/entry['code'])==entry['code_sha256'],'Independent mapped adapter hash')
    require(digest(ROOT/entry['library'])==entry['library_sha256'],'Independent mapped library hash')
    source=(ROOT/entry['code']).read_text();tree=ast.parse(source)
    calls={(n.lineno,n.end_lineno):ast.get_source_segment(source,n) for n in ast.walk(tree)
           if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='require'}
    require(len(calls)==len(entry['actual_guards']) and len(calls)>=15,'Independent guard map coverage')
    for guard in entry['actual_guards']:
        require(guard['file']==entry['code'] and calls.get((guard['line'],guard['end_line']))==guard['predicate'],'Independent guard source')
    history=read('independent/prior-audit/PROVENANCE.json')
    for name,value in history['selected_historical_logs'].items():
        require(digest(ROOT/name)==value,'Historical audit log hash')
        last=(ROOT/name).read_text().splitlines()[-1]
        require('MATHJOB_END' in last and 'oom=false' in last and 'container_exit=0' in last
                and 'outer_timeout=0' in last and 'lock_released=1' in last,'Historical run terminal record')
    return {'groups':1,'id':cid,'status':'PASS','max_r':2,'witness_metrics':7,
            'classification':'finite-exact','role':'independent-implementation-witness',
            'negative_controls_enforced_by_adapter':True,'primary_ab_backend_executed':False,
            'historical_logs_are_fresh_runs':False}


def verify():
    files={str(p.relative_to(ROOT)):p for p in ROOT.rglob('*')
           if p.is_file() and not p.is_relative_to(ROOT/'reproduced')}
    require(not any(p.is_symlink() for p in ROOT.rglob('*')),'Symlink found')
    sums={}
    for line in (ROOT/'SHA256SUMS.txt').read_text().splitlines():
        value,name=line.split('  ',1)
        require(name not in sums,'Duplicate checksum path')
        require(name in files,'Missing checksum target: '+name)
        require(digest(files[name])==value,'Hash mismatch: '+name)
        sums[name]=value
    require(set(sums)==set(files)-{'SHA256SUMS.txt'},'Checksum coverage differs')
    jobs=read('jobs.json');mapped=read('checks.json')['checks']
    ids=[c['id'] for c in mapped]
    require(len(ids)==len(set(ids))==28,'Check index IDs')
    require(set(ids)=={x for j in jobs.values() for x in j['check_ids']},'Job/index mismatch')
    for c in mapped:
        require(c['id'] in jobs[c['job']]['check_ids'],'Wrong job for check')
        require(c['code'] in files and c['adapter'] in files and c['result'] in files,'Unresolved check path')
    index={c['id']:c for c in mapped};count=Counter();runs=[]
    for job,entry in list(jobs.items())+[('failure-probe',{'check_ids':['RUNNER-FAILURE-PROBE']})]:
        result=read('results/'+job+'/result.json')
        env=read('results/'+job+'/environment.json')
        require(result['job']==env['job']==job,'Job metadata mismatch')
        require(env['mathematics_on_host'] is False,'Missing isolation record')
        for path,value in env['input_hashes'].items():
            require(path in files and digest(files[path])==value,'Executed input mismatch: '+path)
        required={'code/run.py','code/worker.py','code/report.py','jobs.json','inputs.json','environment.lock.json'}
        if job!='failure-probe':required|={'code/'+n for n in entry['dependencies']}
        require(required<=set(env['input_hashes']),'Execution dependency hashes incomplete')
        log=ROOT/'results'/job/'log.jsonl'
        require(log.stat().st_size<1_048_576,'Log bound exceeded')
        require(digest(log)==result['log_sha256'],'Log digest mismatch')
        records=[json.loads(line) for line in log.read_text().splitlines()]
        summaries=[v for v in records if v.get('record')=='summary']
        checks=[v for v in records if v.get('record')=='check']
        pre=[v for v in records if v.get('record')=='preflight']
        require(len(summaries)==len(pre)==1,'Summary/preflight count')
        require(summaries[0]==result['worker_summary'] and checks==result['checks'],'Saved result/log mismatch')
        require(Counter(v['id'] for v in checks)==Counter(entry['check_ids']),'Missing/duplicate/extra check')
        require(summaries[0]['missing']==[],'Worker missing IDs')
        require(all(result[k] for k in ('stopped','removed','lock_released')),'Cleanup unconfirmed')
        require(all(env[k] for k in ('container_stopped','container_removed','lock_released')),'Environment cleanup unconfirmed')
        require(result['error'] is None and env['error'] is None,'Execution/controller error')
        h=env['host_config'];cg=pre[0]['cgroup'];q,p=map(int,cg['cpu.max'].split())
        require(h['Memory']==h['MemorySwap']==1_999_998_976,'Docker memory cap')
        require(h['NanoCpus']==1_000_000_000 and h['PidsLimit']==32,'Docker CPU/PID cap')
        require(h['NetworkMode']=='none' and h['ReadonlyRootfs'] and not h['OomKillDisable'],'Docker isolation')
        require(h['RestartPolicy']['Name']=='no','Restart policy')
        require(0<int(cg['memory.max'])<=2_000_000_000 and cg['memory.swap.max']=='0','Actual memory cgroup')
        require(0<q<=p and 0<int(cg['pids.max'])<=32,'Actual CPU/PID cgroup')
        require(pre[0]['ipv4_route_rows']==0 and pre[0]['ipv6_only_loopback'],'Network preflight')
        require(env['container_state']['Running'] is False and not env['container_state']['OOMKilled'],'Stopped/OOM state')
        require(env['limits']==read('environment.lock.json'),'Environment profile mismatch')
        require(env['controller_seconds']<900,'Saved wall bound')
        if job=='failure-probe':
            require(result['status']==summaries[0]['status']=='FAIL','Failure probe passed incorrectly')
            require(result['client_exit_code']!=0 and env['container_state']['ExitCode']!=0,'Probe exit must be nonzero')
            require(checks[0]['status']=='FAIL' and summaries[0]['failed']==['RUNNER-FAILURE-PROBE'],'Wrong probe failure')
        else:
            require(result['status']==summaries[0]['status']=='PASS','Mathematical job not passed')
            require(result['client_exit_code']==env['container_state']['ExitCode']==0,'Nonzero mathematical exit')
            require(summaries[0]['failed']==[] and all(c['status']=='PASS' for c in checks),'Failed check')
            for c in checks:
                require(c['classification']==index[c['id']]['classification'],'Check classification mismatch')
                count[c['classification']]+=1
        if job in ('b-low4','b-low8'):
            guards=[v for v in records if v.get('record')=='reporting-guard-regression']
            require(len(guards)==1 and guards[0]['status']=='PASS','Missing reporting guard regression')
            require(len(guards[0]['negative_controls'])==14 and guards[0]['mathematical_programs_called'] is False,'Guard-control coverage')
        runs.append({'job':job,'status':result['status'],'checks':len(checks)})
    # Verify exact assertion snippets against the distributed current source.
    assertion_cache={}
    for c in mapped:
        require(digest(ROOT/c['code'])==c['code_sha256'],'Mapped code hash differs')
        if c['classification']!='numerical-diagnostic':require(bool(c['actual_assertions']),'Missing assertion mapping')
        for a in c['actual_assertions']:
            source=(ROOT/a['file']).read_text().splitlines()
            require(1<=a['line']<=a['end_line']<=len(source),'Invalid assertion source lines')
            # The ast source segment can begin after indentation; line numbering
            # and first assertion token must agree without executing the source.
            if a['file'] not in assertion_cache:
                text=(ROOT/a['file']).read_text()
                assertion_cache[a['file']]={(n.lineno,n.end_lineno):ast.get_source_segment(text,n) for n in ast.walk(ast.parse(text)) if isinstance(n,ast.Assert)}
            require(assertion_cache[a['file']].get((a['line'],a['end_line']))==a['assertion'],'Assertion source segment mismatch')
        emission=c['report_predicate'];source=(ROOT/emission['file']).read_text().splitlines()
        require('report.check(' in source[emission['line']-1],'Report emission source line differs')
    # Relative Markdown links only; remote links and inline anchors are accepted.
    link_count=0
    for name,path in files.items():
        if path.suffix!='.md':continue
        markdown=path.read_text()
        markdown=re.sub(r'(?ms)^```.*?^```\s*$', '', markdown)
        markdown=re.sub(r'\$\$.*?\$\$', '', markdown, flags=re.S)
        markdown=re.sub(r'(?<!\\)\$[^\n$]*\$', '', markdown)
        for target in re.findall(r'\]\(([^)]+)\)',markdown):
            if re.match(r'^[a-z]+:',target) or target.startswith('#'):continue
            require((path.parent/target.split('#')[0]).exists(),'Broken link in '+name+': '+target)
            link_count+=1
    for name,path in files.items():
        require(path.stat().st_size<=1_048_576,'Package file too large: '+name)
        if path.suffix in {'.py','.md','.json','.jsonl','.txt','.cff'}:
            content=path.read_text()
            require(not re.search(r'\x2fUsers\x2f|\x2fhome\x2f(?:studio|lior)|codex:\x2f\x2fthreads\x2f|chatgpt\.com\x2fc\x2f|(?:sk\x2dproj\x2d|sk\x2dant\x2d)',content),
                    'Private path/session/credential pattern in '+name)
    require(count==Counter({'finite-exact':8,'symbolic-exact':14,'numerical-diagnostic':6}),'Classification totals')
    require(Counter(c['evidence_role'] for c in mapped)==Counter({'paper-exact-check':20,'external-exact-comparison':2,'finite-numerical-residual-or-crosscheck':4,'numerical-observation-record':2}),'Evidence-role totals')
    independent=verify_independent(files)
    review=read('REVIEW-STATUS.json')
    require(review['status']=='FINAL_LOCAL_RECONCILIATION_COMPLETED'
            and review['candidate_revision']==3,'Final review status')
    require(review['secondary_independent_audit_completed'] is True
            and review['secondary_full_line_audit_of_final_code_completed'] is False,'Secondary audit scope')
    require(review['secondary_final_recommendations_reconciled'] is True
            and review['direct_geometric_witness_test_of_primary_ab_exact'] is False,'Reconciliation/primary scope')
    require(review['publication_performed'] is False and review['whole_paper_verified'] is False,'Publication/proof scope')
    require(review['registered_primary_record_ids']==len(mapped)
            and review['independent_evidence_groups']==1,'Review record counts')
    return {'classification':'document-and-package-QA','status':'PASS',
            'scope':'File integrity and correspondence of saved executions; no mathematics rerun or proof verification.',
            'checked_files':len(files),'checksums':len(sums),'local_markdown_links':link_count,
            'execution_record_classifications':dict(count),'evidence_role_counts':dict(Counter(c['evidence_role'] for c in mapped)),'runs':runs,
            'private_path_session_credential_patterns':'none detected in inspected text files',
            'manuscript_anchor_count':len(read('MANUSCRIPT-LOCATORS.json')['locators']),
            'primary_registered_records':len(mapped),'independent_evidence':independent,
            'final_secondary_reconciliation_completed':True,
            'final_code_full_secondary_line_audit_completed':False}


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.parse_args()
    try:print(json.dumps(verify(),indent=2))
    except Exception as exc:
        print(json.dumps({'classification':'document-and-package-QA','status':'FAIL','error':str(exc)}));sys.exit(1)
