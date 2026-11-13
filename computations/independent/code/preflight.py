"""In-container preflight: print and assert the effective cgroup limits and network isolation.

Imported first by every audit job. It performs no mathematics.
"""
import json
from pathlib import Path


def check(max_pids=64):
    cg = Path('/sys/fs/cgroup')
    lim = {k: (cg / k).read_text().strip()
           for k in ('memory.max', 'memory.swap.max', 'cpu.max', 'pids.max')}
    q, p = lim['cpu.max'].split()
    ok = (lim['memory.max'] != 'max' and int(lim['memory.max']) <= 2_000_000_000
          and lim['memory.swap.max'] == '0' and q != 'max' and 0 < int(q) <= int(p)
          and lim['pids.max'] != 'max' and int(lim['pids.max']) <= max_pids)
    ifaces = [l.split(':', 1)[0].strip() for l in Path('/proc/net/dev').read_text().splitlines() if ':' in l]
    up = {n: int(Path('/sys/class/net', n, 'flags').read_text(), 16) & 1 for n in ifaces}
    routes = Path('/proc/net/route').read_text().splitlines()[1:]
    net_ok = set(ifaces) <= {'lo'} or all(v == 0 for n, v in up.items() if n != 'lo')
    net_ok = net_ok and not routes
    print('PREFLIGHT ' + json.dumps({'cgroup': lim, 'interfaces_up': up, 'ipv4_routes': len(routes),
                                     'limits_ok': ok, 'network_isolated': net_ok}), flush=True)
    assert ok, 'cgroup limits not as required'
    assert net_ok, 'network isolation not verified'
    return lim
