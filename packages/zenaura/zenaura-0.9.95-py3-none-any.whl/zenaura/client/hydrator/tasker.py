from collections import defaultdict
import asyncio
class HydratorTasker:
    """
        manage tasks coming from zenaura diffing algorithm:
            for:
                1. updating real dom.
                2. updating virtual dom.
            do: 
             1. create task queue if not created for component id.
             2. return task queue by component id.
            task queue:
             3. enqueue tasks for components.
             4. dequeue tasks for components.

        component-id : asyncio-task-queue
    """
    queue_lookup = defaultdict(lambda : None)

    def __init__(self):
        pass

    def hyd_tsk_get_or_create_task_queue(self, component_id) -> asyncio.Queue:
        """
            gets or create task queue for component_id
            args:
                component_id: str
            returns:
                task queue
        """
        try :
            if component_id not in self.queue_lookup:
                self.queue_lookup[component_id] = asyncio.Queue()
                return self.queue_lookup[component_id]
            else:
                return self.queue_lookup[component_id]
        except KeyError:
            return False

    
    def hyd_tsk_enqueue_task(self, component_id, task):
        """
            enque task for component if not full and exists
            returns True if task is enqueued else False
        """
        comp_queue = self.queue_lookup[component_id]
        try :
            comp_queue.put_nowait(task)
            return True
        except asyncio.QueueFull:
            return False

    async def hyd_tsk_do_nothing(self):
        """
            final call to queue tasks when que is empty
        """
        pass
    
    def hyd_tsk_dequeue_task(self, component_id):
        """
            dequeue task for component if exists
            else return False        
        """
        comp_queue = self.queue_lookup[component_id]
        try :
            task = comp_queue.get_nowait()
            return task
        except asyncio.QueueEmpty:
            # clean up and return empty function
            del self.queue_lookup[component_id]
            return self.hyd_tsk_do_nothing