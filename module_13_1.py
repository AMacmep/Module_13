# Домашнее задание по теме "Асинхронность на практике
# Цель: приобрести навык использования асинхронного запуска функций на практике
import asyncio


async def start_strongman(name, power):
    print(f'Силач {name} начал соревнования')
    for n in range(1, 6):
        await asyncio.sleep(1 / power)
        print(f'Силач {name} поднял {n} шар')
    print(f'Силач {name} закончил соревнования')


async def start_tournament():
    task_1 = asyncio.create_task(start_strongman('Pasha', 3))
    task_2 = asyncio.create_task(start_strongman('Denis', 4))
    task_3 = asyncio.create_task(start_strongman('Apollon', 5))
    await task_1
    await task_2
    await task_3


if __name__ == '__main__':
    asyncio.run(start_tournament())
