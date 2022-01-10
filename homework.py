from dataclasses import dataclass

M_IN_KM: int = 1000

@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration_h: float
    distance: float
    speed: float
    calories: float
    
    MESSAGE_STR = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration_h:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )
    
    def get_message(self) -> str:
        message = self.MESSAGE_STR.format(
            training_type = self.training_type,
            duration_h = self.duration_h,
            distance = self.distance,
            speed = self.speed,
            calories = self.calories
        )
        return message


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int
    duration_h: float
    weight: float
    LEN_STEP = 0.65

    def hour_in_min(self) -> float:
        duration_m = self.duration_h * 60
        return duration_m
        
    def get_training_type(self) -> str:
        return type(self).__name__

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        distance = self.get_distance()
        speed = distance / self.duration_h
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info = InfoMessage(
            self.get_training_type(),
            self.duration_h,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )
        return info


@dataclass
class Running(Training):
    action: int
    duration_h: float
    weight: float
    coeff_calor1: int = 18
    coeff_calor1: int = 20

    def get_spent_calories(self) -> float:
        speed = self.get_mean_speed()
        duration_m = self.hour_in_min()
        calories = ((self.coeff_calor1 * speed - self.coeff_calor1) * 
                    self.weight / M_IN_KM * duration_m)
        return calories


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    action: int
    duration_h: float
    weight: float
    height: float
    coeff_calor1: float = 0.035
    coeff_calor2: float = 0.029

    def get_spent_calories(self) -> float:
        speed = self.get_mean_speed()
        duration_m = self.hour_in_min()
        calories = (self.coeff_calor1 * self.weight + 
                    (speed ** 2 // self.height) * 
                    self.coeff_calor2 * self.weight * duration_m)
        return calories


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    action: int
    duration_h: float
    weight: float
    length_pool: float
    count_pool: int
    LEN_STEP: float = 1.38
    value1: float = 1.1

    def get_mean_speed(self) -> float:
        speed = (self.length_pool * self.count_pool /
                M_IN_KM / self.duration_h)
        return speed

    def get_spent_calories(self) -> float:
        speed = self.get_mean_speed()
        calories = (speed + self.value1) * 2 * self.weight
        return calories

PACKAGE_TYPE = {
    'SWM': Swimming,
    'RUN': Running,
    'WLK': SportsWalking
}

def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_class = PACKAGE_TYPE[workout_type]
    return training_class(*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)