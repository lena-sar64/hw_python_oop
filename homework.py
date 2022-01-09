import inspect

class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, 
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories
                     
    def get_message(self) -> str:
        return f'Тип тренировки: {self.training_type}; Длительность: {self.duration:.3f} ч.; Дистанция: {self.distance:.3f} км; Ср. скорость: {self.speed:.3f} км/ч; Потрачено ккал: {self.calories:.3f}.'


class Training:
    """Базовый класс тренировки."""
    M_IN_KM = 1000
    LEN_STEP = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
    
    def get_training_type(self) -> str:
        return type(self).__name__
    
    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        distance = self.get_distance()
        speed = distance / self.duration 
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info = InfoMessage(self.get_training_type(), self.duration, self.get_distance(), self.get_mean_speed(), self.get_spent_calories())
        return info


class Running(Training):
    """Тренировка: бег."""
    def __init__(self, 
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)
         
    def get_spent_calories(self) -> float:
        k1 = 18
        k2 = 20
        speed = self.get_mean_speed()
        calories = (k1 * speed - k2) * self.weight / self.M_IN_KM * self.duration * 60
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self, 
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height
  
    def get_spent_calories(self) -> float:
        k1 = 0.035
        k2 = 0.029
        speed = self.get_mean_speed()
        calories = (k1 * self.weight + (speed ** 2 // self.height) * k2 * self.weight) * self.duration * 60
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
    
    def get_mean_speed(self) -> float:
        speed = self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        return speed
    
    def get_spent_calories(self) -> float:
        k1 = 1.1
        speed = self.get_mean_speed()
        calories = (speed + k1) * 2 * self.weight
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type == 'SWM':
        return Swimming(data[0], data[1], data[2], data[3], data[4])
    if workout_type == 'RUN':
        return Running(data[0], data[1], data[2])
    if workout_type == 'WLK':
        return SportsWalking(data[0], data[1], data[2], data[3])
    
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

