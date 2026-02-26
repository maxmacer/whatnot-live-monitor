import asyncio, json

class FileManager:
    def __init__(self):
        self.lock = asyncio.Lock()
        
    async def _write_to_file(self, file_path, input):
        async with self.lock:
            with open(file_path,'r+') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
                    
                if not isinstance(data, dict):
                    data = []
                        
                data.append(input)
                json.dump(data, f)

    async def _read_from_file(self, file_path):
        async with self.lock:
            with open(file_path, 'r+') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
            return data
                