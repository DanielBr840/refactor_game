import random
import sys

PLAYER_START_HP = 100
PLAYER_START_ATTACK = 10
PLAYER_START_DEFENSE = 5
DAMAGE_VARIANCE = (-2, 2)

class Character:
    def __init__(self, name, hp, attack, defense):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        damage_taken = max(0, damage - self.defense)
        self.hp -= damage_taken
        print(f"{self.name} takes {damage_taken} damage. HP left: {self.hp}")
        return damage_taken

class Player(Character):
    def __init__(self, name):
        super().__init__(name, PLAYER_START_HP, PLAYER_START_ATTACK, PLAYER_START_DEFENSE)
        self.gold = 0
        self.inventory = []

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        damage_taken = max(0, damage - self.defense)
        self.hp -= damage_taken
        print(f"{self.name} отримав {damage_taken} ушкоджень. Залишилось HP: {self.hp}")
        return damage_taken

    def heal(self, amount):
        self.hp += amount
        if self.hp > 100:
            self.hp = 100
        print(f"{self.name} відновив {amount} HP. Зараз HP: {self.hp}")

    def add_gold(self, amount):
        self.gold += amount
        print(f"{self.name} отримав {amount} золота. Зараз золота: {self.gold}")

    def add_item(self, item):
        self.inventory.append(item)
        print(f"{self.name} знайшов {item}!")

class Enemy(Character):
    def __init__(self, name, hp, attack, defense, gold_reward):
        super().__init__(name, hp, attack, defense)
        self.gold_reward = gold_reward

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        damage_taken = max(0, damage - self.defense)
        self.hp -= damage_taken
        print(f"{self.name} отримав {damage_taken} ушкоджень. Залишилось HP: {self.hp}")
        return damage_taken

    def attack_player(self, player):
        damage = self.attack + random.randint(*DAMAGE_VARIANCE)
        print(f"{self.name} атакує {player.name}!")
        player.take_damage(damage)

class Room:
    def __init__(self, description, enemy=None, treasure=None):
        self.description = description
        self.enemy = enemy
        self.treasure = treasure
        self.visited = False

    def enter(self, player):
        print("\n" + "="*40)
        print(f"Ви увійшли в кімнату: {self.description}")
        self.visited = True
        if self.enemy and self.enemy.is_alive():
            print(f"На вас напав {self.enemy.name}!")
            battle(player, self.enemy)
        if self.treasure:
            print(f"Ви знайшли скарб: {self.treasure}")
            if self.treasure == "Зілля":
                player.heal(20)
            elif self.treasure == "Меч":
                player.attack += 5
                print(f"{player.name} отримав бонус до атаки!")
            elif self.treasure == "Щит":
                player.defense += 3
                print(f"{player.name} отримав бонус до захисту!")
            elif self.treasure == "Золото":
                player.add_gold(50)
            player.add_item(self.treasure)
            self.treasure = None

def battle(player, enemy):
    while player.is_alive() and enemy.is_alive():
        choice = get_player_choice()
        if choice == "1":
            attack_enemy(player, enemy)
        elif choice == "2":
            if attempt_escape(player, enemy):
                return
        if enemy.is_alive():
            enemy.attack_player(player)

def get_player_choice():
    print("\nChoose an action: [1] Attack, [2] Run")
    return input("Your choice: ")

def attack_enemy(player, enemy):
    damage = player.attack + random.randint(*DAMAGE_VARIANCE)
    print(f"{player.name} attacks {enemy.name}!")
    enemy.take_damage(damage)

def attempt_escape(player, enemy):
    if random.random() > 0.5:
        print(f"{player.name} successfully ran away from {enemy.name}!")
        return True
    else:
        print(f"{player.name} failed to escape!")
        return False


def random_event(player):
    event_chance = random.random()
    if event_chance < 0.3:
        print("\nВи відчули дивне коливання повітря...")
        bonus = random.choice(["heal", "gold", "trap"])
        if bonus == "heal":
            print("Чарівне зілля наповнило вас силою!")
            player.heal(15)
        elif bonus == "gold":
            gold_found = random.randint(10, 30)
            print(f"Ви знайшли {gold_found} золота на підлозі!")
            player.add_gold(gold_found)
        elif bonus == "trap":
            print("Але це була пастка! Ви отримали ушкодження.")
            player.take_damage(10)
    else:
        print("\nНічого не змінилося... продовжуйте рухатися.")

class Game:
    def __init__(self, player):
        self.player = player
        self.rooms = []
        self.current_room_index = 0
        self.setup_rooms()

    def setup_rooms(self):
        goblin = Enemy("Гоблін", 30, 8, 2, 20)
        skeleton = Enemy("Скелет", 40, 10, 3, 30)
        orc = Enemy("Орк", 50, 12, 4, 40)

        treasures = ["Зілля", "Меч", "Щит", "Золото", None]
        descriptions = [
            "Темна печера",
            "Стара бібліотека",
            "Залишки замку",
            "Підземелля",
            "Таємна кімната",
            "Забута гробниця",
            "Покинута вежа",
            "Кімната з таємними дверима"
        ]
        enemies = [goblin, skeleton, orc, None, None, goblin, skeleton, None]
        for i in range(len(descriptions)):
            room = Room(
                description=descriptions[i],
                enemy=enemies[i] if i < len(enemies) and enemies[i] is not None else None,
                treasure=random.choice(treasures)
            )
            self.rooms.append(room)

    def next_room(self):
        if self.current_room_index < len(self.rooms):
            room = self.rooms[self.current_room_index]
            room.enter(self.player)
            print("\nВипадкова подія:")
            random_event(self.player)
            self.current_room_index += 1
        else:
            print("Ви пройшли всі кімнати! Вітаємо з перемогою!")
            sys.exit(0)

    def play(self):
        print(f"Ласкаво просимо, {self.player.name}, у гру Dungeon Adventure!")
        while self.player.is_alive():
            print("\nЩо робити далі?")
            print("[1] Перейти до наступної кімнати")
            print("[2] Переглянути статус гравця")
            print("[3] Вийти з гри")
            choice = input("Ваш вибір: ")
            if choice == "1":
                self.next_room()
            elif choice == "2":
                self.show_status()
            elif choice == "3":
                print("Дякуємо за гру! До побачення!")
                sys.exit(0)
            else:
                print("Невірний вибір, спробуйте ще раз.")

    def show_status(self):
        print("\n--- Статус гравця ---")
        print(f"Ім'я: {self.player.name}")
        print(f"HP: {self.player.hp}")
        print(f"Атака: {self.player.attack}")
        print(f"Захист: {self.player.defense}")
        print(f"Золото: {self.player.gold}")
        print(f"Інвентар: {', '.join(self.player.inventory) if self.player.inventory else 'Порожній'}")
        print("----------------------")

def main():
    print("Вітаємо у Dungeon Adventure!")
    player_name = input("Введіть ім'я вашого героя: ")
    player = Player(player_name)
    game = Game(player)
    game.play()

if __name__ == "__main__":
    main()

def print_credits():
    print("\n" + "="*40)
    print("          Дякуємо за гру!")
    print("     Розроблено ChatGPT (цундере версія)")
    print("="*40)

def print_treasure_chest():
    art = [
        "      __________",
        "     /________/|",
        "    |        ||",
        "    |  TREASURE||",
        "    |  CHEST  ||",
        "    |________|/",
    ]
    for line in art:
        print(line)

def print_monster():
    art = [
        "      .-\"\"\"-.",
        "     /       \\",
        "     \\       /",
        "      '-...-'",
        "       (o o)",
        "       | O |",
        "        \\_/",
    ]
    for line in art:
        print(line)

def fake_pause():
    print("\n...")

def extra_info():
    print("\nІнформація про гру:")
    print("Це текстова пригода, де ви зустрінете небезпеки та скарби.")
    print("Кожен ваш вибір має значення.")
    print("Гра створена для тих, хто любить пригоди та виклики.")

def instructions():
    print("\nІнструкції:")
    print("1. Введіть ваші команди згідно з меню.")
    print("2. Вивчайте статус героя та приймайте мудрі рішення.")
    print("3. Якщо загинете, гра закінчиться.")
    print("4. Насолоджуйтесь грою!")

def future_enhancements():
    print("\nМайбутні вдосконалення:")
    print("- Нові типи ворогів")
    print("- Більше кімнат з загадками")
    print("- Розширена система інвентарю")
    print("- Мультиплеєрний режим")

