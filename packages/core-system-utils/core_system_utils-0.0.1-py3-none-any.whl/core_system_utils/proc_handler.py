from typing import List, Tuple, Optional, NoReturn, TypeAlias, Any, TypedDict
from pathlib import Path
from abc import ABC, abstractmethod

File_Contents: TypeAlias = str

import re

# Get the general idea of what the memory/cpu environment is... asynchroneous ops
class ProcHandler(ABC):    
    
    @classmethod
    def read_file(cls, path_of_interest: Path) -> File_Contents:        
        with open(str(path_of_interest)) as reader:
            return reader.read().strip()              
    
    def __init__(self):
        self.data = None
        
    @abstractmethod    
    def pull_info(self):
        pass
        
    def __str__(self):
        return "\n".join([line.strip() for line in self.data.split('\n')])
        
    def __repr__(self):
        return self.__str__() 
        
    def __enter__(self):
        self.pull_info()
        
        return self
        
    def __exit__(self, exc_type, exc, tb):
        pass  
        
class MemoryHandler(ProcHandler):
    mem_info: Path = Path('/proc/meminfo')
    
    def pull_info(self):
        self.data = self.read_file(self.mem_info)
        
    def get_json(self):
        result_json = {}
        
        for line in self.data.split('\n'):
            name, value = line.strip().split(':')
            value = value.strip()
            result_json[name] = value
        
        return result_json

class CpuHandler(ProcHandler):
    cpu_info: Path = Path('/proc/cpuinfo')
    
    def pull_info(self):
        self.data = self.read_file(self.cpu_info)
        
    def get_json(self):
        result_json = {}
        # processor_section_matches 
        p = [m for m in re.finditer(f'^processor.*:', self.data, re.MULTILINE)]
        
        processor_section_ranges = [(p[i].start(), p[i + 1].start()) for i in range(len(p) - 1)] + [(p[-1].start(), -1)]
        processor_sections = [self.data[r[0]:r[1]] for r in processor_section_ranges][0]
        #print(processor_sections.split('\n'))
        for line in processor_sections.split('\n'):
            try:
                name, value = line.split(':')
                if not value:
                    raise Exception(f'{name} has a bad value!')
                
                name = name.strip()
                value = value.strip()
                result_json[name] = value
            except:
                pass

        return result_json 

class SystemUtils(ABC):
    @abstractmethod
    def get_data(self) -> None:
        raise NotImplementedError("Implement this!")
        
SystemPtr: TypeAlias = Tuple[str, SystemUtils]
Data: TypeAlias = Tuple[Any]
        
class CompositeSystem(SystemUtils):
    def __init__(self) -> None:
        self.system_ptrs: List[SystemPtr] = []
        
    def get_data(self) -> None:
        for name, system_ptr in self.system_ptrs:
            with system_ptr() as item:
                print(f'{name} has the following data: {item.get_json()}')
     
    def get_jsons(self) -> Any:
        data = {}
        
        for name, system_ptr in self.system_ptrs:
            with system_ptr() as item:
                data[name] = item.get_json()
                
        return data
    
    def add(self, system_ptr: SystemPtr) -> None:
        self.system_ptrs.append(system_ptr)
        
    def remove(self, system_ptr: SystemPtr) -> None:
        self.system_ptrs.remove(system_ptr)
        
class Ex_Metrics(TypedDict):
    total_memory: str
    free_memory: str
    available_memory: str
    
    available_processors: int # Shouldn't change unless in a cloud-type environment... just for effect here
    
    def __str__(self):
        print("Memory: total {self.total_memory}, free {self.free_memory}, avail {self.available_memory}\nCPUs available {self.available_processors}\n")
        
class MachineState:
    def __init__(self):
        self.composite = CompositeSystem()
        
    def load_fxn_ptr(self, name: str, fxn_ptr: SystemPtr) -> bool:
        try:
            self.composite.add((name, fxn_ptr))
        except:
            return False
        return True
    
    def facade_layer(self) -> Data:
        return self.composite.get_jsons()
    
    def simple_format(self, data: Data, _return: bool = False) -> NoReturn:
        metrics = Ex_Metrics({'total_memory': data['Memory']['MemTotal'], 'free_memory': data['Memory']['MemFree'], 'available_memory': data['Memory']['MemAvailable'], 'available_processors': len(data['CPU'])})
    
        if _return:
            return metrics
        return print(metrics)
        
    def display_format(self) -> NoReturn:
        self.simple_format(self.facade_layer())

        
if __name__ == "__main__":
    machine_state = MachineState()

    machine_state.load_fxn_ptr('Memory', MemoryHandler)
    machine_state.load_fxn_ptr('CPU', CpuHandler)

    machine_state.display_format()
    print(machine_state.facade_layer())
