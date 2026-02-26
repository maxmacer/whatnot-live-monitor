import json
import asyncio
from config import MONITOR_DELAY, ONLINE_DELAY
from whatnot.whatnot_services import Whatnot
from utils.notifications import Notifications
from utils.presence_manager import PresenceManager
from utils.file_manager import FileManager

MONITORED_USERS_PATH = 'whatnot/monitored_users.json'

class Monitor:
    def __init__(self, notifications: Notifications, presence: PresenceManager, files: FileManager) -> None:
        self.notifications = notifications
        self.presence = presence
        self.files = files

        self.whatnot = Whatnot()
        self.currently_monitoring = []
        self.monitoring_tasks = []
        self.active_monitor_data = {}
        
    async def start_when_ready(self):
        await self.set_currently_monitoring()
        await self.start_monitoring()

    async def add_user_to_monitoring(self, user: str) -> bool:
        if user not in self.currently_monitoring:
            self.currently_monitoring.append(user)
        
            await self.files._write_to_file(MONITORED_USERS_PATH,user)
        
            await self.restart_monitoring()
            return True
        else:
            return False

    async def remove_user_from_monitoring(self, user: str) -> bool:
        if user in self.currently_monitoring:
            self.currently_monitoring.remove(user)
            
            await self.files._write_to_file(MONITORED_USERS_PATH,self.currently_monitoring)
            
            await self.restart_monitoring()
            return True
        else:
            return False

    async def set_currently_monitoring(self) -> None:
        self.currently_monitoring = await self.files._read_from_file(MONITORED_USERS_PATH)

    async def get_currently_monitored(self) -> dict:
        return self.currently_monitoring
            
    async def start_monitoring(self) -> None:
        await self.presence.set_presence(f'Monitoring {str(len(self.currently_monitoring))} Whatnot Sellers!')
        for user in self.currently_monitoring:
            self.monitoring_tasks.append(asyncio.create_task(self.monitor_user(user))) 

    async def restart_monitoring(self) -> None:
        for task in self.monitoring_tasks:
            task.cancel()
        await self.start_when_ready()

    async def monitor_user(self,user: str):
        while True:
            new_data = self.whatnot.check_if_user_live(user)

            if not new_data:
                continue
            
            if user in self.active_monitor_data:
                old_data = self.active_monitor_data[user]
            else:
                old_data = {'live': False, 'details': {}, 'error': False}
            self.active_monitor_data.update({user: new_data})

            live_status = new_data['live']
            live_status_old = old_data['live']

            if live_status != live_status_old:
                if live_status == True:
                    print(f'[/] {user} is live!')
                    
                    stream_title = new_data['details']['title']
                    stream_id = new_data['details']['id']
                    user_pic = 'https://images.whatnot.com/fit-in/3840x0/filters:format(webp)/' + new_data['details']['user']['profileImage']['key']
                    stream_image = new_data['details']['thumbnail']['smallImage']
                else:
                    print(f'[/] {user} went offline.')
                
                    stream_title = old_data['details']['title']
                    stream_id = old_data['details']['id']
                    user_pic = 'https://images.whatnot.com/fit-in/3840x0/filters:format(webp)/' + old_data['details']['user']['profileImage']['key']
                    stream_image = old_data['details']['thumbnail']['smallImage']

                await self.notifications.send_notification(live_status,user,stream_title,stream_id,stream_image,user_pic)
                
            if live_status:
                await asyncio.sleep(ONLINE_DELAY * 60)
            else:
                await asyncio.sleep(MONITOR_DELAY * 60)
