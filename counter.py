import time
import asyncio

class Player:
    def __init__(self,user_name, team_name) -> None:
        self.user_name = user_name
        self.health= 100
        self.guns = {'knife': {'name': 'knife', 'price': 0,'loss_life': 43,'kill_cash': 500}}
        self.money = 1000
        self.team_name = team_name
        self.count_kill = 0
        self.count_dead = 0
        self.event = {}
        self.enter_time = None

class Game:
    def __init__(self) -> None:
        self.Terrorist_gun = {'heavy': [{'name': 'AK', 'price': 2700,'loss_life': 31,'kill_cash': 100},{'name': 'AWP', 'price': 4300,'loss_life': 110,'kill_cash': 50}],'pistol':[{'name': 'Revolver', 'price': 600,'loss_life': 51,'kill_cash': 150},{'name': 'Glock-18', 'price': 300,'loss_life': 11,'kill_cash': 200}]}
        self.Counter_Terrorist_gun = {'heavy':[{'name': 'M4A1', 'price': 2700,'loss_life': 29,'kill_cash': 100},{'name': 'AWP', 'price': 4300,'loss_life': 110,'kill_cash': 50}],'pistol':[{'name': 'Desert-Eagle', 'price': 600,'loss_life': 53,'kill_cash': 175},{'name': 'UPS-S', 'price': 300,'loss_life': 13,'kill_cash': 225}]}
        self.team={'Terrorist':[], 'Counter-Terrorist': []}
        self.list_player = []
        self.start_time = None
        self.kill_players = []
        
    
    def add_player(self, username, team):
        if username not in self.get_list_username():
            if len(self.team[team]) <= 10:
                player = Player(username, team)
                if not self.start_time:
                    self.start_time = time.time()
                    self.end_time = self.start_time + 135
                    player.enter_time = time.time()
                    self.team[team].append(player)
                    self.list_player.append(player)
                else:
                    if time.time() - self.start_time > 3:
                        player.health = 0
                        player.enter_time = time.time()
                        self.team[team].append(player)
                        self.list_player.append(player)
                    else:
                        player.enter_time = time.time()
                        self.team[team].append(player)
                        self.list_player.append(player)
                return f'this user added to {team}'
            else:
                return 'this team is full'
        return 'you are already in this game'
    
    def get_list_username(self):
        if self.list_player:
            return [player.user_name for player in self.list_player]
        return []

    def get_player_by_username(self, username):
        return [player for player in self.list_player if player.user_name == username]

    def get_money(self, username):
        if username in self.get_list_username():
            player = self.get_player_by_username(username)
            money = player[0].money
            return money
        return 'invalid username'

    def get_health(self, username):
        if username in self.get_list_username():
            player = self.get_player_by_username(username)
            health = player[0].health
            return health
        return 'invalid username'
    
    def remain_player(self):
        count_live_terrorist=len([player for player in self.team['Terrorist'] if bool(player.health)]) if self.team['Terrorist'] else []
        count_live_counter_terrorist=len([player for player in self.team['Counter-Terrorist'] if bool(player.health)]) if self.team['Counter-Terrorist'] else []
        return count_live_terrorist, count_live_counter_terrorist


    def tap(self, attacker, attacked, gun):
        if attacker not in self.get_list_username() or attacked not in self.get_list_username():
            return 'invalid username'
        attacker = self.get_player_by_username(attacker)[0]
        attacked = self.get_player_by_username(attacked)[0]
        if attacker.health == 0:
            return 'attacker is dead'
        if attacked.health == 0:
            return 'attacked is dead'
        if gun not in attacker.guns:
            return 'no such gun'
        if attacker in self.team[attacked.team_name]:
            return 'friendly fire'
        msg = ''
        if attacked.health - attacker.guns[gun]['loss_life'] <= 0:
            attacked.health = 0
            attacked.guns = {'knife': {'name': 'knife', 'price': 0,'loss_life': 43,'kill_cash': 500}}
            attacked.count_dead += 1
            attacker.count_kill += 1
            self.kill_players.append(attacked)
            if (attacker.money + attacker.guns[gun]['kill_cash']) > 10000:
                attacker.money = 10000
            else:
                attacker.money += attacker.guns[gun]['kill_cash']
            msg = 'nice shot'
        else:
            attacked.health -= attacker.guns[gun]['loss_life']
            msg = 'nice shot'
        return msg

    
    async def end_game(self):
        if self.start_time:
            while time.time() < self.end_time:
                await asyncio.sleep(1)
                live_terrorist , live_counter_terrorist = self.remain_player()
                if not live_counter_terrorist and not live_terrorist:
                    msg = 'Counter-Terrorist won'
                elif not live_counter_terrorist:
                    msg = 'Terrorist won'
                elif not live_terrorist:
                    msg = 'Counter-Terrorist won'
                if time.time() > self.end_time:
                    if live_terrorist and live_counter_terrorist:
                        msg = 'Counter-Terrorist won'
                return msg

    def buy(self, username, gun_name, time):
        time = time.split(':')
        time = sum([int(time[0])*1000*60, int(time[1])*1000, int(time[2])])
        Terrorist_gun =[*[gun.get('name') for gun in self.Terrorist_gun['heavy']], *[gun.get('name') for gun in self.Terrorist_gun['pistol']]]
        Counter_Terrorist_gun =[*[gun.get('name') for gun in self.Counter_Terrorist_gun['heavy']], *[gun.get('name') for gun in self.Counter_Terrorist_gun['pistol']]]
        if username not in self.get_list_username():
            return 'invalid username'
        user = self.get_player_by_username(username)[0]
        gun_user = list(user.guns)
        type_gun = None
        if user.health == 0:
            return 'player is dead'
        if 45*1000 < time:
            return 'you are out of time'
        if user.team_name == 'Terrorist':
            if gun_name not in Terrorist_gun:
                return 'invalid category gun'
            else:
                num = Terrorist_gun.index(gun_name)
                if num in [0,1]:
                    if 'heavy' in gun_user:
                        return 'you have a heavy'
                    type_gun = 'heavy'
                elif  num in [2,3] :
                    if 'pistol' in gun_user:
                        return 'you have a pistol'
                    type_gun='pistol'
                else:
                    select_gun = [gun for gun in self.Terrorist_gun[type_gun] if gun['name'] == gun_name]
                    if user.money < select_gun['price']:
                        return 'no enough money'
                    user.guns[type_gun] = select_gun
                    return 'I hope you can use it'

        if user.team_name == 'Counter-Terrorist':
            if gun_name not in Counter_Terrorist_gun:
                    return 'invalid category gun'
            else:
                num = Counter_Terrorist_gun.index(gun_name)
                if num in [0,1]:
                    if 'heavy' in gun_user:
                        return 'you have a heavy'
                    type_gun = 'heavy'
                elif  num in [2,3] :
                    if 'pistol' in gun_user:
                        return 'you have a pistol'
                    type_gun='pistol'
                else:
                    select_gun = [gun for gun in self.Counter_Terrorist_gun[type_gun] if gun['name'] == gun_name]
                    if user.money < select_gun['price']:
                        return 'no enough money'
                    user.guns[type_gun] = select_gun 
                    return 'I hope you can use it'   

    def score_board(self):
        terrorist  = self.team['Terrorist'].copy()
        counter_terrorist = self.team['Counter-Terrorist'].copy()
        terrorist_rank = []
        counter_terrorist_rank = []
        for player in terrorist:
            terrorist_rank.append({
                'username': player.user_name,
                'kills': player.count_kill,
                'death': player.count_dead,
                'enter_time': player.enter_time
            })
        terrorist_rank = sorted(terrorist_rank, key =lambda x: (x['kills'], -x['death'], -x['enter_time']), reverse=True)
        
        for player in counter_terrorist:
            counter_terrorist_rank.append({
                'username': player.user_name,
                'kills': player.count_kill,
                'death': player.count_dead,
                'enter_time': player.enter_time
            })
        counter_terrorist_rank = sorted(counter_terrorist_rank, key =lambda x: (x['kills'], -x['death'], -x['enter_time']), reverse=True)

        print('Counter-Terrorist-Players')
        for _,player in enumerate(counter_terrorist_rank):
            print(_,player['username'],player['kills'],player['death'])

        print('Terrorist-Players')
        for _,player in enumerate(terrorist_rank):
            print(_,player['username'],player['kills'],player['death'])

    
def Execute():
    exec = Game()
    for i in range(5):
        print(exec.add_player(username='King2Krazy', team='Counter-Terrorist'))
        print(exec.add_player('Cat', 'Terrorist'))
        print(exec.add_player('soheil', 'Counter-Terrorist'))
        print(exec.add_player('omid', 'Terrorist'))
        print(exec.add_player('farhad', 'Terrorist'))
        print(exec.add_player('maryam', 'Counter-Terrorist'))
        print(exec.add_player('akbar', 'Counter-Terrorist'))
        print(exec.get_health('omid'))
        print(exec.get_money('soheil'))
        asyncio.ensure_future(exec.end_game)
        for i in range(5):
            time.sleep(10)
            print(exec.tap('King2Krazy', 'Cat', 'knife'))
        print(exec.buy('omid','Desert-Eagle', '00:11:343'))
        print(exec.get_health('Cat'))
        print(exec.get_money('King2Krazy'))
        print(exec.score_board())

Execute()





                



        
    

                


        
        
    

