from __future__ import annotations
from datetime import datetime
import time
from collectors import COLLECTORS
from .findings import dedupe, risk_counts
from .recommendations import merge as merge_recommendations
from .scoring import overall_score, label, score_class
from .version import __version__, PRODUCT_NAME, TAGLINE


def run_collectors() -> dict:
    started=time.time(); collectors=[]
    for mod in COLLECTORS:
        cstart=time.time()
        try:
            result=mod.collect()
            result['duration_seconds']=round(time.time()-cstart,2)
        except Exception as exc:
            result={'id':mod.__name__,'title':mod.__name__,'category':'Internal','health':0,'status':'Error','summary':str(exc),'findings':[{'severity':'high','title':f'Collector failed: {mod.__name__}','detail':str(exc),'action':'Review collector error.'}], 'recommendations':[], 'positive':[], 'data':{}, 'duration_seconds':round(time.time()-cstart,2)}
        collectors.append(result)
    findings=dedupe([f for c in collectors for f in c.get('findings',[])])
    recs=merge_recommendations(collectors)
    score=overall_score(collectors)
    positives=[]
    for c in collectors: positives.extend([p for p in c.get('positive',[]) if p])
    return {'product':PRODUCT_NAME,'tagline':TAGLINE,'version':__version__,'generated_at':datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'runtime_seconds':round(time.time()-started,2),'collectors':collectors,'findings':findings,'recommendations':recs,'risk_counts':risk_counts(findings),'overall_score':score,'overall_label':label(score),'score_class':score_class(score),'positives':positives}
