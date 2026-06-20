# C:\Umbra\core\runtime\umbra_runtime_spine.py  v2.1
import os,sys,time,logging
log=logging.getLogger("umbra.spine")
_ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class _StubGen:
    def generate(self,r): return {"status":"stub","file_path":None,"asset_id":None}
class _StubBoss:
    def run_cycle(self): return {"status":"idle"}
    def execute_next(self): return None
    def plan(self,goal): return [{"step":goal,"type":"direct"}]
class _StubTask:
    def create_task(self,g): return type("T",(),{"id":"stub","goal":g,"status":"pending"})()
    def run_task(self,t): return {"task_id":t,"status":"completed","result":{}}
class _StubAsset:
    def save(self,a): return a
    def list(self): return []

class UmbraRuntimeSpine:
    def __init__(self,base_path="C:\\Umbra"):
        self.base_path=base_path
        self._task_queue=[]
        self._history=[]
        # generation engine
        try:
            from core.runtime.umbra_generation_engine import UmbraGenerationEngine
            self.generation_engine=UmbraGenerationEngine()
        except Exception: self.generation_engine=_StubGen()
        # boss agent — NO bridge.analyze() call anywhere
        try:
            from core.agents.boss_agent import BossAgent
            self.boss_agent=BossAgent(base_path)
        except Exception: self.boss_agent=_StubBoss()
        # task engine
        try:
            from core.runtime.umbra_task_engine import UmbraTaskEngine
            self.task_engine=UmbraTaskEngine()
        except Exception: self.task_engine=_StubTask()
        # asset store
        try:
            from core.runtime.umbra_asset_store import UmbraAssetStore
            self.asset_store=UmbraAssetStore()
        except Exception: self.asset_store=_StubAsset()
        log.info("UmbraRuntimeSpine ready at %s",base_path)

    def run_task(self,task):
        if not isinstance(task,dict): return {"status":"error","error":"task must be dict"}
        task_type=task.get("type","code"); prompt=task.get("prompt",""); name=task.get("name","untitled")
        if not prompt: return {"status":"error","error":"no prompt"}
        try: steps=self.boss_agent.plan(prompt)
        except Exception: steps=[{"step":prompt,"type":task_type}]
        results=[]
        for step in steps:
            req={"type":step.get("type",task_type),"prompt":step.get("step",prompt),"name":name}
            try: results.append(self.generation_engine.generate(req))
            except Exception as e: results.append({"status":"error","error":str(e)})
        ok=[r for r in results if r.get("status")=="success"]
        final={"status":"success" if ok else "partial","task_type":task_type,"prompt":prompt,
               "results":results,"file_path":ok[-1].get("file_path") if ok else None,
               "asset_id":ok[-1].get("asset_id") if ok else None,"timestamp":time.time()}
        self._history.append(final); return final

    def queue_task(self,task): self._task_queue.append(task)
    def tick(self):
        if self._task_queue: return self.run_task(self._task_queue.pop(0))
        try:
            self.boss_agent.run_cycle()
            nt=self.boss_agent.execute_next()
            if nt and isinstance(nt,dict) and nt.get("status")!="idle": return self.run_task(nt)
        except Exception: pass
        return {"status":"idle","queue_depth":len(self._task_queue)}
    def get_history(self): return list(self._history)
    def get_queue_depth(self): return len(self._task_queue)
    def status(self):
        return {"base_path":self.base_path,"queue_depth":len(self._task_queue),
                "history_len":len(self._history),"gen_engine":type(self.generation_engine).__name__,
                "boss_agent":type(self.boss_agent).__name__}