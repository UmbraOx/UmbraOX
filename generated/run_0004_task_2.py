import random

class Player:
    def __init__(self, name):
        self.name = name
        self.level = 1
        self.health = 100
        self.attack = 10
        self.defense = 5
        self.gold = 0
        self.inventory = {}

    def level_up(self):
        """Level up the player, increasing stats."""
        self.level += 1
        self.health += 10
        self.attack += 2
        self.defense += 1

class Enemy:
    def __init__(self, name, health, attack, defense):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense

def combat(player, enemy):
    """Simulate a battle between the player and an enemy."""
    while player.health > 0 and enemy.health > 0:
        # Player attacks
        damage = max(0, player.attack - enemy.defense)
        enemy.health -= damage
        print(f"{player.name} attacks {enemy.name} for {damage} damage.")
        
        if enemy.health <= 0:
            print(f"{enemy.name} has been defeated!")
            player.level_up()
            player.gold += random.randint(10, 30)
            return True
        
        # Enemy attacks
        damage = max(0, enemy.attack - player.defense)
        player.health -= damage
        print(f"{enemy.name} attacks {player.name} for {damage} damage.")
        
        if player.health <= 0:
            print(f"{player.name} has been defeated!")
            return False

def main_game_loop(player):
    """Main game loop."""
    while True:
        print("\nWhat would you like to do?")
        print("1. Explore")
        print("2. Craft")
        print("3. View stats")
        print("4. Quit")

        choice = input("Enter your choice: ")
        
        if choice == '1':
            # Simulate enemy encounter
            enemies = ["Goblin", "Orc", "Dragon"]
            enemy_name = random.choice(enemies)
            enemy_health = random.randint(20, 50) + player.level * 5
            enemy_attack = random.randint(5, 10) + player.level * 2
            enemy_defense = random.randint(3, 7) + player.level
            enemy = Enemy(enemy_name, enemy_health, enemy_attack, enemy_defense)
            
            if not combat(player, enemy):
                break
        
        elif choice == '2':
            # Crafting logic (simple example)
            print("Crafting menu:")
            print("1. Heal Potion (Cost: 5 gold)")
            print("2. Upgrade Sword (Cost: 20 gold)")
            
            craft_choice = input("Enter your crafting choice: ")
            if craft_choice == '1' and player.gold >= 5:
                player.health += 20
                player.gold -= 5
                print("You crafted a Heal Potion and restored some health.")
            elif craft_choice == '2' and player.gold >= 20:
                player.attack += 3
                player.gold -= 20
                print("You upgraded your sword, increasing attack power.")
        
        elif choice == '3':
            # View stats
            print(f"Name: {player.name}")
            print(f"Level: {player.level}")
            print(f"Health: {player.health}")
            print(f"Attack: {player.attack}")
            print(f"Defense: {player.defense}")
            print(f"Gold: {player.gold}")
        
        elif choice == '4':
            break

if __name__ == "__main__":
    player = Player("Hero")
    main_game_loop(player)
