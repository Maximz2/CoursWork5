from __future__ import annotations
from abc import ABC, abstractmethod
from equipment import Equipment, Weapon, Armor
from classes import UnitClass
from random import randint
from typing import Optional


class BaseUnit(ABC):
    """
    Базовый класс юнита
    """
    def __init__(self, name: str, unit_class: UnitClass):
        """
        При инициализации класса Unit используем свойства класса UnitClass
        """
        self.name = name
        self.unit_class = unit_class
        self.hp = unit_class.max_health
        self.stamina = unit_class.max_stamina
        self.weapon = ...
        self.armor = ...
        self._is_skill_used = False


    @abstractmethod
    def hit(self, target: BaseUnit) -> str:
        """
        этот метод будет переопределен ниже
        """
        pass

    @property
    def health_points(self):
        return round(self.hp,1)

    @property
    def stamina_points(self):
        return  round(self.stamina, 1)

    def equip_weapon(self, weapon: Weapon):
        self.weapon = weapon
        return f"{self.name} экипирован оружием {self.weapon.name}"

    def equip_armor(self, armor: Armor):
        self.armor = armor
        return f"{self.name} экипирован броней {self.armor.name}"

    def _count_damage(self, target: BaseUnit) -> int:
        self.stamina -= self.weapon.stamina_per_hit * self.unit_class.stamina
        damage = self.weapon.damage * self.unit_class.attack
        # Проверка. Сможет ли противник блокировать удар броней
        if target.stamina > target.armor.stamina_per_turn * target.unit_class.stamina:
            target.stamina -= target.armor.stamina_per_turn * target.unit_class.stamina
            damage -= target.armor.defence * target.unit_class.armor
        return target.get_damage(damage)

    def get_damage(self, damage: int) -> Optional[int]:
        if damage > 0:
            self.hp -= damage
            return round(damage, 1)
        return 0


    def use_skill(self, target: BaseUnit) -> str:
        if self._is_skill_used:
            return 'Навык уже использован'
        self._is_skill_used = True
        return self.unit_class.skill.use(self,target)

class PlayerUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        if self.stamina * self.unit_class.stamina < self.weapon.stamina_per_hit:
            return (
                f"{self.name} попытался использовать {self.weapon.name},"
                f" но у него не хватило выносливости."
            )
        damage = self._count_damage(target)
        if damage > 0:
            return (
                f"{self.name} используя {self.weapon.name} пробивает"
                f"{target.armor.name} соперника и наносит {damage} урона."
            )
        return (
            f"{self.name} используя {self.weapon.name} наносит удар,"
            f"но {target.armor.name} cоперника его останавливает."
        )

class EnemyUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        if not self._is_skill_used and self.stamina >= self.unit_class.skill.stamina and randint(0,100) < 10:
            return self.use_skill(target)

        if self.stamina * self.unit_class.stamina < self.weapon.stamina_per_hit:
            return (
                f"{self.name} попытался использовать {self.weapon.name},"
                f" но у него не хватило выносливости."
            )
        damage = self._count_damage(target)
        if damage > 0:
            return (
                f"{self.name} используя {self.weapon.name} пробивает"
                f"{target.armor.name} соперника и наносит Вам {damage} урона."
            )
        return (
            f"{self.name} используя {self.weapon.name} наносит удар,"
            f"но Ваш(а) {target.armor.name} его останавливает."
        )